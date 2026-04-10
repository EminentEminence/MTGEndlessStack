import os
import re
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from system.cardhandling.card import Card
from system.cardhandling.printings import printings, printing
from system.logger import logger, LogLevel

LocalLogger = logger("Local Importer")

ACTIVE_CARDS_DIR = os.path.join("system", "activeCards")
ACTIVE_CARDS_DATA = os.path.join(ACTIVE_CARDS_DIR, "cardData.txt")
ACTIVE_CARDS_IMAGES = os.path.join(ACTIVE_CARDS_DIR, "Images")

def LocalImport() -> tuple[list[Card], list[printings]] | None:
    '''
    A function to import cards from the system/activeCards directory.

    Returns:
        tuple[list[Card], list[printings]]: A tuple containing the imported cards and printings.
    '''

    LocalLogger.log("Loading cards from active cards directory...", LogLevel.INFO)
    print("Loading cards from active cards directory...")

    cards = getCardsFromFile()
    cardPrintings = getPrintings()

    if cards is None:
        LocalLogger.log("Failed to load cards from active cards directory.", LogLevel.ERROR)
        print("Failed to load cards from active cards directory.")
        return None

    if len(cards) == 0:
        LocalLogger.log("No cards were loaded from the active cards directory.", LogLevel.WARNING)
        print("No cards were loaded from the active cards directory.")
        return None

    LocalLogger.log(f"Loaded {len(cards)} cards.", LogLevel.INFO)
    print(f"Loaded {len(cards)} cards.")

    return cards, cardPrintings


def getPrintings() -> list[printings]:
    '''
    A function to get all printings from the system/activeCards/Images directory.

    Returns:
        list[printings]: A list of printings objects, each containing the printings for a specific card.
    '''

    all_printings = []

    for root, _, files in os.walk(ACTIVE_CARDS_IMAGES):
        for file_name in files:
            if not file_name.lower().endswith(".png"):
                continue

            image_path = os.path.join(root, file_name)
            printing_type = os.path.basename(root)
            file_stem = os.path.splitext(file_name)[0]
            stem_without_duplicate = re.sub(r"-\d+$", "", file_stem)
            split_parts = stem_without_duplicate.rsplit("-", 1)
            if len(split_parts) == 2:
                card_name = split_parts[0]
                artist = split_parts[1]
            else:
                card_name = stem_without_duplicate
                artist = ""

            grouped_printings = None
            for existing_group in all_printings:
                if existing_group.cardName == card_name:
                    grouped_printings = existing_group
                    break

            if grouped_printings is None:
                grouped_printings = printings()
                grouped_printings.cardName = card_name
                all_printings.append(grouped_printings)

            grouped_printings.printings.append(
                printing(image_path, printing_type, artist)
            )

    return all_printings


def getCardsFromFile() -> list[Card] | None:
    '''
    A function to get the card details from system/activeCards/cardData.txt.

    Returns:
        list[Card] | None: A list of Card objects, or None if there was an error loading the file.
    '''

    loadedCards = []

    if not os.path.exists(ACTIVE_CARDS_DATA):
        LocalLogger.log("cardData.txt file not found in active cards directory.", LogLevel.ERROR)
        print("cardData.txt file not found in active cards directory.")
        return None

    #Remove first 2 lines since it is the setcode and headers
    with open(ACTIVE_CARDS_DATA, "r", encoding="utf-8") as f:
        lines = f.readlines()[2:]

        if len(lines) == 0:
            LocalLogger.log("No card data found in cardData.txt.", LogLevel.WARNING)
            print("No card data found in cardData.txt.")
            return []

        for line in lines:
            cardDetails = line.strip().split(" || ")
            if len(cardDetails) < 9:
                LocalLogger.log(f"Invalid card data format: {line}", LogLevel.WARNING)
                print(f"Invalid card data format: {line}")
                continue

            card = Card()
            card.set("name", cardDetails[0])
            card.set("manaCost", cardDetails[1])
            card.set("type", cardDetails[2])
            card.set("rarity", cardDetails[3])
            card.set("rulesText", cardDetails[4])
            card.set("flavourText", cardDetails[5])
            card.set("power", cardDetails[6] if cardDetails[6] != "" else None)
            card.set("toughness", cardDetails[7] if cardDetails[7] != "" else None)
            card.set("loyalty", cardDetails[8] if cardDetails[8] != "" else None)

            #Check for Incomplete Cards
            if card.get("type") == "" or str(card.get("power")) + str(card.get("toughness")) + str(card.get("loyalty")) + str(card.get("rulesText")) == "":
                LocalLogger.log(f"Incomplete card data for card '{card.name}' - Skipping.", LogLevel.WARNING)
                print(f"Incomplete card data for card '{card.name}' - Skipping.")
                continue

            loadedCards.append(card)
            LocalLogger.log(f"Loaded card '{card.name}'.", LogLevel.INFO)
            print(f"Loaded card '{card.name}'.")

    return loadedCards

if __name__ == "__main__":
    LocalImport()
