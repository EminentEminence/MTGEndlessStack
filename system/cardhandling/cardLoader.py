import os
import shutil
import sys
from typing import Callable

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
	sys.path.insert(0, PROJECT_ROOT)

from system.cardhandling.card import Card
from system.cardhandling.printings import printing, printings
from system.importers.MSEImporter import MSEImport
from system.logger import LogLevel, logger

CardLoaderLogger = logger("Card Loader")

ACTIVE_CARDS_DIR = os.path.join("system", "activeCards")
ACTIVE_CARDS_DATA = os.path.join(ACTIVE_CARDS_DIR, "cardData.txt")
ACTIVE_CARDS_IMAGES = os.path.join(ACTIVE_CARDS_DIR, "Images")

DEFAULT_CARDDATA_HEADER = (
	"Name || Mana Cost || Type || Rarity || Rules Text || Flavor Text || Power || Toughness || "
	"Loyalty || Illustrator || Card Number || Notes || [BACK FACE] || Name 2 || Mana Cost 2 || "
	"Type 2 || Rules Text 2 || Flavor Text 2 || Power 2 || Toughness 2 || Loyalty 2 || "
	"Illustrator 2 || Card Number 2 || Notes 2 || "
)

# Register enabled importers here. This keeps the loader extensible for future importers.
ImporterFn = Callable[[], tuple[list[Card], list[printings]] | None]
IMPORTERS: list[tuple[str, ImporterFn]] = [
	("MSEImporter", MSEImport),
]


def _safe_str(value: object) -> str:
	"""Return a string value, converting None to an empty string."""
	return "" if value is None else str(value)


def _card_signature(card: Card) -> tuple[str, ...]:
	"""Build a normalized tuple of comparable card fields used for duplicate validation."""
	# Signature excludes name so duplicate-name cards can be validated for equality.
	return (
		_safe_str(card.getManaCost()),
		_safe_str(card.getType()),
		_safe_str(card.getRarity()),
		_safe_str(card.getRulesText()),
		_safe_str(card.getFlavourText()),
		_safe_str(card.getPower()),
		_safe_str(card.getToughness()),
		_safe_str(card.getLoyalty()),
		_safe_str(card.getName2()),
		_safe_str(card.getManaCost2()),
		_safe_str(card.getType2()),
		_safe_str(card.getRarity2()),
		_safe_str(card.getRulesText2()),
		_safe_str(card.getFlavourText2()),
		_safe_str(card.getPower2()),
		_safe_str(card.getToughness2()),
		_safe_str(card.getLoyalty2()),
	)


def _get_carddata_header() -> str:
	"""Return the default header used when writing the compiled cardData file."""
	return DEFAULT_CARDDATA_HEADER


def _build_carddata_row(card: Card) -> str:
	"""Serialize a Card object into a single cardData.txt line using the expected column order."""
	# Match the Deadlock cardData structure while filling only known fields.
	columns = [
		_safe_str(card.getName()),
		_safe_str(card.getManaCost()),
		_safe_str(card.getType()),
		_safe_str(card.getRarity()),
		_safe_str(card.getRulesText()),
		_safe_str(card.getFlavourText()),
		_safe_str(card.getPower()),
		_safe_str(card.getToughness()),
		_safe_str(card.getLoyalty()),
		"",
		"",
		"",
		"",
		_safe_str(card.getName2()),
		_safe_str(card.getManaCost2()),
		_safe_str(card.getType2()),
		_safe_str(card.getRulesText2()),
		_safe_str(card.getFlavourText2()),
		_safe_str(card.getPower2()),
		_safe_str(card.getToughness2()),
		_safe_str(card.getLoyalty2()),
		"",
		"",
		"",
		"",
	]

	return " || ".join(columns)


def _reserve_destination_path(destination_path: str) -> str:
	"""Return a non-colliding file path by appending -N before the file extension when needed."""
	if not os.path.exists(destination_path):
		return destination_path

	root, ext = os.path.splitext(destination_path)
	counter = 1
	candidate = f"{root}-{counter}{ext}"

	while os.path.exists(candidate):
		counter += 1
		candidate = f"{root}-{counter}{ext}"

	return candidate


def _prepare_active_cards_dir() -> None:
	"""Recreate system/activeCards as a clean output directory for a fresh compilation."""
	if os.path.exists(ACTIVE_CARDS_DIR):
		shutil.rmtree(ACTIVE_CARDS_DIR)
	os.makedirs(ACTIVE_CARDS_DIR, exist_ok=True)
	os.makedirs(ACTIVE_CARDS_IMAGES, exist_ok=True)


def _save_images(
	merged_printings: dict[str, list[printing]],
) -> dict[str, list[printing]]:
	"""Copy collected printing images into activeCards/Images grouped by printing type."""
	os.makedirs(ACTIVE_CARDS_IMAGES, exist_ok=True)

	saved_printings: dict[str, list[printing]] = {}

	for card_name, card_printings in merged_printings.items():
		for card_printing in card_printings:
			source_path = card_printing.image
			printing_type = card_printing.type
			artist = card_printing.artist

			if not os.path.exists(source_path):
				CardLoaderLogger.log(
					f"Printing image missing for '{card_name}': {source_path}",
					LogLevel.ERROR,
				)
				continue

			destination_folder = os.path.join(ACTIVE_CARDS_IMAGES, printing_type)
			os.makedirs(destination_folder, exist_ok=True)

			destination_path = os.path.join(
				destination_folder,
				os.path.basename(source_path),
			)
			destination_path = _reserve_destination_path(destination_path)
			shutil.copy2(source_path, destination_path)

			saved_printing = printing(destination_path, printing_type, artist)
			saved_printings.setdefault(card_name, []).append(saved_printing)

	return saved_printings


def _save_card_data(cards: list[Card]) -> None:
	"""Write the compiled cards to activeCards/cardData.txt with Set:ALL and a fixed header."""
	os.makedirs(ACTIVE_CARDS_DIR, exist_ok=True)
	header_line = _get_carddata_header()

	with open(ACTIVE_CARDS_DATA, "w", encoding="utf-8") as file:
		file.write("Set:ALL\n")
		file.write(f"{header_line}\n")

		for card in cards:
			file.write(f"{_build_carddata_row(card)}\n")


def _collect_sources() -> list[tuple[str, list[Card], list[printings]]]:
	"""Run all registered importers and return successful (name, cards, printings) results."""
	collected_sources: list[tuple[str, list[Card], list[printings]]] = []

	for importer_name, importer_func in IMPORTERS:
		import_result = importer_func()
		if import_result is not None:
			import_cards, import_printings = import_result
			collected_sources.append((importer_name, import_cards, import_printings))
		else:
			CardLoaderLogger.log(
				f"Importer '{importer_name}' returned no data.",
				LogLevel.WARNING,
			)

	return collected_sources


def compileActiveCards() -> list[Card]:
	"""
	Compiles all cards from LocalImporter and MSEImporter into system/activeCards,
	merges duplicate names when card fields match, saves cardData and images,
	attaches printings to cards by card name, and returns the final card list.

	Returns:
		list[Card]: Fully compiled cards with printings attached.
	"""

	CardLoaderLogger.log("Compiling cards from registered importers...", LogLevel.INFO)
	print("Compiling cards from registered importers...")

	_prepare_active_cards_dir()

	sources = _collect_sources()
	if len(sources) == 0:
		CardLoaderLogger.log("No card sources returned cards.", LogLevel.WARNING)
		print("No card sources returned cards.")
		_save_card_data([])
		return []

	merged_cards: dict[str, Card] = {}
	merged_printings: dict[str, list[printing]] = {}

	for source_name, source_cards, source_printing_groups in sources:
		printings_by_name = {
			grouped_printings.cardName: grouped_printings.printings
			for grouped_printings in source_printing_groups
		}
		source_printings_attached: set[str] = set()

		for card in source_cards:
			card_name = _safe_str(card.getName())
			incoming_signature = _card_signature(card)

			if card_name not in merged_cards:
				merged_cards[card_name] = card
				if card_name not in source_printings_attached:
					merged_printings.setdefault(card_name, []).extend(
						printings_by_name.get(card_name, [])
					)
					source_printings_attached.add(card_name)
				continue

			existing_signature = _card_signature(merged_cards[card_name])
			if existing_signature != incoming_signature:
				CardLoaderLogger.log(
					(
						f"Duplicate card mismatch for '{card_name}' from {source_name}. "
						"Card skipped."
					),
					LogLevel.ERROR,
				)
				print(
					(
						f"Duplicate card mismatch for '{card_name}' from {source_name}. "
						"Card skipped."
					)
				)
				continue

			if card_name not in source_printings_attached:
				merged_printings.setdefault(card_name, []).extend(
					printings_by_name.get(card_name, [])
				)
				source_printings_attached.add(card_name)

	sorted_cards = sorted(
		merged_cards.values(),
		key=lambda card: _safe_str(card.getName()).lower(),
	)
	_save_card_data(sorted_cards)
	saved_printings = _save_images(merged_printings)

	for card in sorted_cards:
		name = _safe_str(card.getName())
		front_group = printings()
		front_group.cardName = name
		front_group.printings = saved_printings.get(name, [])
		card.frontPrintings = front_group

	CardLoaderLogger.log(f"Compiled {len(sorted_cards)} cards into active cards.", LogLevel.INFO)
	print(f"Compiled {len(sorted_cards)} cards into active cards.")

	return sorted_cards


if __name__ == "__main__":
	compileActiveCards()
