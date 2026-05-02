from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CARDHANDLING_PATH = PROJECT_ROOT / "system" / "cardhandling"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(CARDHANDLING_PATH) not in sys.path:
    sys.path.insert(0, str(CARDHANDLING_PATH))

try:
    from . import MTGFunctions as MTG_FUNCTIONS_MODULE  # type: ignore
    from .MTGFunctions import *  # type: ignore  # noqa: F401,F403
except ImportError:
    import MTGFunctions as MTG_FUNCTIONS_MODULE
    from MTGFunctions import *  # noqa: F401,F403 - runtime mapping source


def _discover_mtg_functions() -> dict[str, Any]:
    discovered: dict[str, Any] = {}
    for name, value in vars(MTG_FUNCTIONS_MODULE).items():
        if name.startswith("_"):
            continue
        if callable(value):
            discovered[name] = value
    return discovered


MTG_FUNCTIONS = _discover_mtg_functions()

# Toggle this to control whether the translator should load a saved model
# or re-learn from testCases.txt each run.
USE_SAVED_LEARNING = False

TEST_CASES_PATH = Path(__file__).with_name("testCases.txt")
MODEL_PATH = Path(__file__).with_name("learned_rules_model.json")


@dataclass
class LearnedExample:
    rules_text: str
    dsl_output: str


@dataclass
class LearnedTemplate:
    rules_segment: str
    output_segment: str


class MiniRulesTranslator:
    """
    A very small case-based "AI" translator.

    It learns pairs of (rules text -> DSL output) from test cases, then uses
    lightweight text similarity to choose the best learned example for new input.
    """

    def __init__(self, test_cases_path: Path, model_path: Path, use_saved_learning: bool = True) -> None:
        self.test_cases_path = test_cases_path
        self.model_path = model_path
        self.use_saved_learning = use_saved_learning
        self.examples: list[LearnedExample] = []
        self.templates: list[LearnedTemplate] = []
        self.available_functions: dict[str, Any] = dict(MTG_FUNCTIONS)
        self.counter_function_name = self._resolve_counter_function_name()
        self.keyword_function_name = self._resolve_keyword_function_name()

        if self.use_saved_learning and self.model_path.exists():
            self._load_model()
        else:
            self.relearn()

    def relearn(self) -> None:
        self.examples = self._parse_test_cases(self.test_cases_path)
        self.templates = self._build_templates(self.examples)
        self._save_model()

    def translate_rules_text(self, rules_text: str) -> dict[str, Any]:
        if not self.examples:
            raise RuntimeError("No learned examples loaded. Relearn from test cases first.")

        best = self._best_match(rules_text)
        python_calls = self._compose_from_templates(rules_text)
        if not python_calls:
            python_calls = self._normalize_to_python_calls(best.dsl_output)
        python_calls = self._harmonize_calls_with_available_functions(python_calls)

        function_names = self._extract_known_function_names(python_calls)
        function_map = self._build_function_map(function_names)

        return {
            "input": rules_text,
            "matched_rules_text": best.rules_text,
            "dsl_output": best.dsl_output,
            "python_calls": python_calls,
            "mapped_functions": function_map,
        }

    def _compose_from_templates(self, rules_text: str) -> list[str]:
        if not self.templates:
            return []

        segments = self._split_rules_into_segments(rules_text)
        generated: list[str] = []

        for segment in segments:
            template, score = self._best_template_match(segment)
            if not template or score < 0.34:
                continue

            output = self._apply_lightweight_slots(template, segment)
            if output not in generated:
                generated.append(output)

        return generated

    def _best_template_match(self, rules_segment: str) -> tuple[LearnedTemplate | None, float]:
        norm_input = self._normalize_text(rules_segment)
        best_template: LearnedTemplate | None = None
        best_score = 0.0

        for template in self.templates:
            norm_template = self._normalize_text(template.rules_segment)
            jaccard = self._token_jaccard(norm_input, norm_template)
            seq_ratio = SequenceMatcher(None, norm_input, norm_template).ratio()
            score = (0.65 * jaccard) + (0.35 * seq_ratio)
            if score > best_score:
                best_score = score
                best_template = template

        return best_template, best_score

    def _apply_lightweight_slots(self, template: LearnedTemplate, rules_segment: str) -> str:
        output = template.output_segment

        # Swap activation cost, e.g. "2U:" => cost='2U'.
        input_cost = self._extract_leading_cost(rules_segment)
        template_cost = self._extract_leading_cost(template.rules_segment)
        if input_cost and template_cost:
            output = output.replace(f"cost='{template_cost}'", f"cost='{input_cost}'")
            output = output.replace(f'cost="{template_cost}"', f'cost="{input_cost}"')

        # Update putCounter() argument from text like "put a Frost counter".
        input_counter = self._extract_counter_name(rules_segment)
        template_counter = self._extract_counter_name(template.rules_segment)
        if input_counter and template_counter:
            output = output.replace(f"putCounter('{template_counter}')", f"putCounter('{input_counter}')")
            output = output.replace(f'putCounter("{template_counter}")', f'putCounter("{input_counter}")')
            output = output.replace(
                f"addCounter(forEachTarget,'{template_counter}')",
                f"addCounter(forEachTarget,'{input_counter}')",
            )
            output = output.replace(
                f"addCounter(forEachTarget, '{template_counter}')",
                f"addCounter(forEachTarget, '{input_counter}')",
            )
            output = output.replace(
                f'addCounter(forEachTarget, "{template_counter}")',
                f'addCounter(forEachTarget, "{input_counter}")',
            )
            output = output.replace(f"counter:{template_counter}", f"counter:{input_counter}")

        # Update type filters from text like "target Elf or Soldier creature".
        input_types = self._extract_target_types(rules_segment)
        template_types = self._extract_target_types(template.rules_segment)
        if input_types and template_types:
            output = output.replace(
                self._types_to_filter(template_types),
                self._types_to_filter(input_types),
            )

        # Update keyword lists for lines like "Flying, Vigilance".
        input_keywords = self._extract_keywords_list(rules_segment)
        template_keywords = self._extract_keywords_list(template.rules_segment)
        if input_keywords and template_keywords:
            output = re.sub(r"(?:keyWords|keywords|addKeywords)\([^)]*\)", self._keywords_to_call(input_keywords), output)

        return output

    def _resolve_counter_function_name(self) -> str:
        if "addCounter" in self.available_functions:
            return "addCounter"
        if "putCounter" in self.available_functions:
            return "putCounter"
        return "putCounter"

    def _resolve_keyword_function_name(self) -> str:
        for candidate in ("keyWords", "keywords", "addKeywords"):
            if candidate in self.available_functions:
                return candidate
        return "keyWords"

    def _harmonize_calls_with_available_functions(self, calls: list[str]) -> list[str]:
        normalized: list[str] = []

        for call in calls:
            updated = call

            if "addCounter" in self.available_functions and "putCounter" not in self.available_functions:
                updated = re.sub(
                    r"putCounter\(\s*(['\"])([^'\"]+)\1\s*\)",
                    r"addCounter(forEachTarget, '\2')",
                    updated,
                )
            elif "putCounter" in self.available_functions and "addCounter" not in self.available_functions:
                updated = re.sub(
                    r"addCounter\(\s*forEachTarget\s*,\s*(['\"])([^'\"]+)\1\s*\)",
                    r"putCounter('\2')",
                    updated,
                )

            if self.keyword_function_name != "keyWords":
                updated = re.sub(r"\bkeyWords\(", f"{self.keyword_function_name}(", updated)

            normalized.append(updated)

        return normalized

    def _best_match(self, rules_text: str) -> LearnedExample:
        norm_input = self._normalize_text(rules_text)
        scored = []

        for example in self.examples:
            norm_example = self._normalize_text(example.rules_text)
            jaccard = self._token_jaccard(norm_input, norm_example)
            seq_ratio = SequenceMatcher(None, norm_input, norm_example).ratio()
            score = (0.6 * jaccard) + (0.4 * seq_ratio)
            scored.append((score, example))

        scored.sort(key=lambda item: item[0], reverse=True)
        return scored[0][1]

    @staticmethod
    def _normalize_text(text: str) -> str:
        text = text.lower().replace("/n", " ").replace("\\n", " ")
        text = re.sub(r"^[^—:-]{2,}\s*[—-]\s*", "", text)
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    @staticmethod
    def _split_rules_into_segments(text: str) -> list[str]:
        normalized_newlines = text.replace(" /n ", "\\n").replace("/n", "\\n")
        chunks = [chunk.strip() for chunk in normalized_newlines.split("\\n") if chunk.strip()]
        segments: list[str] = []

        for chunk in chunks:
            parts = [part.strip() for part in re.split(r"(?<=[.!?])\s+", chunk) if part.strip()]
            segments.extend(parts)

        return segments if segments else [text.strip()]

    @staticmethod
    def _build_templates(examples: list[LearnedExample]) -> list[LearnedTemplate]:
        templates: list[LearnedTemplate] = []

        for example in examples:
            rules_segments = MiniRulesTranslator._split_rules_into_segments(example.rules_text)
            output_segments = MiniRulesTranslator._normalize_to_python_calls(example.dsl_output)

            if len(output_segments) == 1:
                templates.append(LearnedTemplate(rules_segment=example.rules_text, output_segment=output_segments[0]))
                continue

            pair_count = min(len(rules_segments), len(output_segments))
            for idx in range(pair_count):
                templates.append(
                    LearnedTemplate(
                        rules_segment=rules_segments[idx],
                        output_segment=output_segments[idx],
                    )
                )

        deduped: dict[tuple[str, str], LearnedTemplate] = {}
        for template in templates:
            key = (
                MiniRulesTranslator._normalize_text(template.rules_segment),
                template.output_segment,
            )
            deduped[key] = template

        return list(deduped.values())

    @staticmethod
    def _extract_leading_cost(text: str) -> str | None:
        match = re.match(r"\s*([0-9WUBRGXTQP/]+)\s*:", text, flags=re.IGNORECASE)
        if not match:
            return None
        return match.group(1).upper()

    @staticmethod
    def _extract_counter_name(text: str) -> str | None:
        match = re.search(
            r"(?:put\s+(?:a|an)\s+|with\s+(?:a|an)\s+)([A-Za-z][A-Za-z\- ]*?)\s+counter",
            text,
            flags=re.IGNORECASE,
        )
        if not match:
            match = re.search(r"(?:a|an)\s+([A-Za-z][A-Za-z\- ]*?)\s+counter", text, flags=re.IGNORECASE)
        if not match:
            return None
        return match.group(1).strip().title()

    @staticmethod
    def _extract_target_types(text: str) -> list[str]:
        match = re.search(r"target\s+([A-Za-z\s]+?)\s+creature", text, flags=re.IGNORECASE)
        if not match:
            return []

        raw = match.group(1)
        parts = re.split(r"\s+(?:or|and)\s+", raw, flags=re.IGNORECASE)
        types = [part.strip().title() for part in parts if part.strip() and part.strip().lower() not in {"a", "an"}]
        return types

    @staticmethod
    def _types_to_filter(types: list[str]) -> str:
        return "type:" + " OR type:".join(types)

    @staticmethod
    def _extract_keywords_list(text: str) -> list[str]:
        if ":" in text or "counter" in text.lower():
            return []
        if "," not in text:
            return []

        items = [item.strip() for item in text.split(",") if item.strip()]
        keywords = [item for item in items if re.match(r"^[A-Za-z][A-Za-z' -]*$", item)]
        if len(keywords) < 2:
            return []
        return [keyword.title() for keyword in keywords]

    def _keywords_to_call(self, keywords: list[str]) -> str:
        quoted = ", ".join(f"'{keyword}'" for keyword in keywords)
        return f"{self.keyword_function_name}({quoted})"

    @staticmethod
    def _token_jaccard(a: str, b: str) -> float:
        a_tokens = set(a.split())
        b_tokens = set(b.split())
        if not a_tokens and not b_tokens:
            return 1.0
        if not a_tokens or not b_tokens:
            return 0.0
        return len(a_tokens & b_tokens) / len(a_tokens | b_tokens)

    @staticmethod
    def _parse_test_cases(path: Path) -> list[LearnedExample]:
        raw_lines = path.read_text(encoding="utf-8").splitlines()
        filtered = []

        for line in raw_lines:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            filtered.append(stripped)

        if len(filtered) % 2 != 0:
            raise ValueError("testCases.txt must contain alternating rules/output lines.")

        pairs = []
        for i in range(0, len(filtered), 2):
            pairs.append(LearnedExample(rules_text=filtered[i], dsl_output=filtered[i + 1]))
        return pairs

    @staticmethod
    def _normalize_to_python_calls(dsl_output: str) -> list[str]:
        dsl_output = dsl_output.replace(" /n ", "\\n").replace("\\n", "\n")
        calls = [line.strip() for line in dsl_output.splitlines() if line.strip()]

        normalized = []
        for call in calls:
            # MTGFunctions.activeAbility takes *actions (positional), not action= keyword.
            call = re.sub(r"activeAbility\(\s*action\s*=", "activeAbility(", call)
            normalized.append(call)

        return normalized

    def _extract_known_function_names(self, python_calls: list[str]) -> set[str]:
        known = set(self.available_functions)
        found: set[str] = set()

        for call in python_calls:
            for name in re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\(", call):
                if name in known:
                    found.add(name)

        return found

    def _build_function_map(self, function_names: set[str]) -> dict[str, Any]:
        return {
            name: self.available_functions[name]
            for name in sorted(function_names)
            if callable(self.available_functions.get(name))
        }

    def _save_model(self) -> None:
        payload = {
            "examples": [
                {"rules_text": example.rules_text, "dsl_output": example.dsl_output}
                for example in self.examples
            ],
            "templates": [
                {
                    "rules_segment": template.rules_segment,
                    "output_segment": template.output_segment,
                }
                for template in self.templates
            ],
        }
        self.model_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def _load_model(self) -> None:
        payload = json.loads(self.model_path.read_text(encoding="utf-8"))
        examples = payload.get("examples", [])
        self.examples = [
            LearnedExample(rules_text=item["rules_text"], dsl_output=item["dsl_output"])
            for item in examples
        ]
        templates = payload.get("templates", [])
        if templates:
            self.templates = [
                LearnedTemplate(
                    rules_segment=item["rules_segment"],
                    output_segment=item["output_segment"],
                )
                for item in templates
            ]
        else:
            self.templates = self._build_templates(self.examples)


def build_translator() -> MiniRulesTranslator:
    return MiniRulesTranslator(
        test_cases_path=TEST_CASES_PATH,
        model_path=MODEL_PATH,
        use_saved_learning=USE_SAVED_LEARNING,
    )


def demo() -> None:
    translator = build_translator()

    example_rules = (
        "{cardName} deals X damage to any target. Draw two cards, then discard a card."
    )

    result = translator.translate_rules_text(example_rules)

    print("INPUT:\n", result["input"], "\n", sep="")
    print("MATCHED RULES:\n", result["matched_rules_text"], "\n", sep="")
    print("PYTHON CALLS:")
    for line in result["python_calls"]:
        print(" -", line)

    print("\nMAPPED FUNCTIONS:")
    for name, func in result["mapped_functions"].items():
        print(f" - {name}: {func}")


if __name__ == "__main__":
    demo()
