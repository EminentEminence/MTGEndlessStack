import os
import re
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from system.cardhandling.card import Card
from system.cardhandling.printings import printings, printing
from system.logger import logger, LogLevel

MSElogger = logger("MSE Importer")

def MSEImport() -> tuple[list[Card], list[printings]] | None:
    '''
    A function to import cards from Magic Set Editor (MSE).

    Returns:
        tuple[list[Card], list[printings]]: A tuple containing the imported cards and printings.
    '''
    
    AvailableMods = [mod for mod in os.listdir("Mods/") if os.path.isdir(os.path.join("Mods/", mod))]
    DisabledMods = [] #This will be used to store any mods that the user has disabled in the settings menu (this is just a placeholder, actual implementation will depend on how you want to handle mod settings)
    EnabledMods = [mod for mod in AvailableMods if mod not in DisabledMods]

    MSElogger.log(f"{len(EnabledMods)} mods enabled.", LogLevel.INFO)
    moddedCards = []
    moddedPrintings = []
    for mod in EnabledMods:
        cards,printings = LoadMod(mod)

        if cards is not None:
            moddedCards.extend(cards)
        else:
            MSElogger.log(f"Failed to load cards from mod '{mod}'.", LogLevel.ERROR)
            print(f"Failed to load cards from mod '{mod}'.")

        if printings is not None:
            moddedPrintings.extend(printings)
        else:
            MSElogger.log(f"Failed to load printings from mod '{mod}'.", LogLevel.ERROR)
            print(f"Failed to load printings from mod '{mod}'.")
    if len(moddedCards) == 0:
        MSElogger.log("No cards were loaded from any mods.", LogLevel.WARNING)
        print("No cards were loaded from any mods.")
        return None
    return moddedCards, moddedPrintings
    

def LoadMod(modName: str) -> tuple[list[Card] | None, list[printings] | None]:
    '''
    A function to load a mod from the Mods directory.
    
    Args:
        modName (str): The name of the mod to load.

    Returns:
        tuple[list[Card] | None, list[printings] | None]:
            A tuple containing the loaded cards and grouped printings for the mod.
            Returns (None, None) if card data could not be loaded.
    '''
    
    MSElogger.log(f"Loading mod '{modName}'...", LogLevel.INFO)
    print(f"Loading mod '{modName}'...")

    modCards = getCardsFromFile(modName)
    modPrintings = getPrintings(modName)

    if modCards is None:
        MSElogger.log(f"Failed to load mod '{modName}'.", LogLevel.ERROR)
        print(f"Failed to load mod '{modName}'.")
        return None, None
    
    MSElogger.log(f"Loaded {len(modCards)} cards from mod '{modName}'.", LogLevel.INFO)
    print(f"Loaded {len(modCards)} cards from mod '{modName}'.")

    return modCards, modPrintings

def getPrintings(modName: str) -> list[printings]:
    '''
    A function to get all of the printings included in the MSE mod. These will be mapped onto the cards in the full card loader.

    Args:
        modName (str): The name of the mod to get the printings from.

    Returns:
        list[printings]: A list of printings objects, each containing the printings for a specific card.
    '''

    all_printings = []
    mod_path = os.path.join("Mods/", modName)

    for root, _, files in os.walk(mod_path):
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



def getCardsFromFile(modName: str) -> list[Card] | None:
    '''
    A function to get the card details from the cardData file in the MSE mod.
    
    Args:
        modName (str): The name of the mod to get the card details from.

    Returns:
        list[Card] | None: A list of Card objects with the details from the cardData file, or None if there was an error loading the file.
    '''

    loadedCards = []
    cardDataPath = os.path.join("Mods/", modName, "cardData.txt")

    if not os.path.exists(cardDataPath):
        MSElogger.log(f"cardData.txt file not found for mod '{modName}'.", LogLevel.ERROR)
        print(f"cardData.txt file not found for mod '{modName}'.")
        return None
    
    #Remove first 2 lines since it is the setcode and headers
    with open(cardDataPath, "r", encoding="utf-8") as f:
        lines = f.readlines()[2:]

        if len(lines) == 0:
            MSElogger.log(f"No card data found in cardData.txt for mod '{modName}'.", LogLevel.WARNING)
            print(f"No card data found in cardData.txt for mod '{modName}'.")
            return []
        
        for line in lines:
            cardDetails = line.strip().split(" || ")
            if len(cardDetails) < 9:
                MSElogger.log(f"Invalid card data format for mod '{modName}': {line}", LogLevel.WARNING)
                print(f"Invalid card data format for mod '{modName}': {line}")
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
                MSElogger.log(f"Incomplete card data for card '{card.name}' in mod '{modName} - Skipping'.", LogLevel.WARNING)
                print(f"Incomplete card data for card '{card.name}' in mod '{modName} - Skipping'.")
                continue

            loadedCards.append(card)
            MSElogger.log(f"Loaded card '{card.name}' from mod '{modName}'.", LogLevel.INFO)
            print(f"Loaded card '{card.name}' from mod '{modName}'.")

    return loadedCards

if __name__ == "__main__":
    LoadMod("Deadlock")
