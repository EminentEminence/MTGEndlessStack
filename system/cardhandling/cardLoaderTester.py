import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
	sys.path.insert(0, PROJECT_ROOT)

from system.cardhandling.card import Card
from system.cardhandling.cardLoader import compileActiveCards
from system.logger import LogLevel, logger

CardLoadingTesterLogger = logger("Card Loading Tester")


def _safe_text(value: object) -> str:
	"""Normalize card values for table output."""
	return "" if value is None else str(value)


def _fit_text(value: object, width: int) -> str:
	"""Fit text into a fixed column width using ellipsis when needed."""
	text = _safe_text(value).replace("\n", " ").replace("\r", " ").strip()
	if len(text) <= width:
		return text.ljust(width)
	if width <= 3:
		return "." * width
	return f"{text[: width - 3]}..."


def log_loaded_cards_table(cards: list[Card] | None = None) -> list[Card]:
	"""
	Load cards (if not provided) and print/log a fixed-width diagnostics table.

	Args:
		cards (list[Card] | None): Optional pre-loaded cards. If None, cards are loaded
			by running compileActiveCards().

	Returns:
		list[Card]: The cards that were logged.
	"""

	loaded_cards = compileActiveCards() if cards is None else cards

	columns: list[tuple[str, int, str]] = [
		("Name", 28, "name"),
		("Mana", 10, "manaCost"),
		("Type", 28, "type"),
		("Rarity", 10, "rarity"),
		("Power", 7, "power"),
		("Tough", 7, "toughness"),
		("Loyalty", 8, "loyalty"),
		("Rules Text", 55, "rulesText"),
		("Face 2", 26, "name2"),
	]

	header = " | ".join(_fit_text(title, width) for title, width, _ in columns)
	separator = "-+-".join("-" * width for _, width, _ in columns)

	summary = f"Loaded {len(loaded_cards)} card(s)."
	print(summary)
	CardLoadingTesterLogger.log(summary, LogLevel.INFO)

	print(header)
	print(separator)
	CardLoadingTesterLogger.log(header, LogLevel.INFO)
	CardLoadingTesterLogger.log(separator, LogLevel.INFO)

	for card in loaded_cards:
		row = " | ".join(
			_fit_text(card.get(attribute), width)
			for _, width, attribute in columns
		)
		print(row)
		CardLoadingTesterLogger.log(row, LogLevel.INFO)

	return loaded_cards


if __name__ == "__main__":
	log_loaded_cards_table()
