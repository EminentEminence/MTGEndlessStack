from printings import printings
class Card:
    '''
    A class for a Magic: The Gathering card. This is used to store all relevant information about a card, including its name, mana cost, type, rarity, rules text, flavor text, power, toughness, loyalty, and printings.
    
    Attributes:
        name (str): The name of the card.
        manaCost (str): The mana cost of the card.
        type (str): The type of the card.
        rarity (str): The rarity of the card.
        rulesText (str): The rules text of the card.
        flavourText (str): The flavor text of the card.
        power (int): The power of the card (if applicable).
        toughness (int): The toughness of the card (if applicable).
        loyalty (int): The loyalty of the card (if applicable).
        frontPrintings (printings): The printings of the front face of the card.
        
        name2 (str): The name of the back face of the card (if applicable).
        manaCost2 (str): The mana cost of the back face of the card (if applicable).
        type2 (str): The type of the back face of the card (if applicable).
        rarity2 (str): The rarity of the back face of the card (if applicable).
        rulesText2 (str): The rules text of the back face of the card (if applicable).
        flavourText2 (str): The flavor text of the back face of the card (if applicable).
        power2 (int): The power of the back face of the card (if applicable).
        toughness2 (int): The toughness of the back face of the card (if applicable).
        loyalty2 (int): The loyalty of the back face of the card (if applicable).
        backPrintings (printings): The printings of the back face of the card (if applicable).
        '''
    
    def __init__(self):
        '''
        Initializes a new instance of the Card class with default values.
        The front face of the card is initialized with default values, while the back face is initialized with None values to indicate that it may not be present for all cards.
        The printings for both faces of the card are initialized as empty printings objects.
        '''

        self.name = "Empty Card"
        self.manaCost = "0"
        self.type = None
        self.rarity = "Special"
        self.rulesText = "No rules text."
        self.flavourText = ""
        self.power = None
        self.toughness = None
        self.loyalty = None
        self.frontPrintings = printings()

        self.name2 = None
        self.manaCost2 = None
        self.type2 = None
        self.rarity2 = None
        self.rulesText2 = None
        self.flavourText2 = None
        self.power2 = None
        self.toughness2 = None
        self.loyalty2 = None
        self.backPrintings = printings()

    
    #CMC Calculation
    def _calcCMC(self, manaCost: str) -> int:
        '''
        Calculates the converted mana cost (CMC) of a card based on its mana cost string.

        Args:
            manaCost (str): The mana cost string of the card.
        
        Returns:
            int: The calculated converted mana cost (CMC) of the card.
        '''

        cmc = 0

        #Exit early for 0 cost cards
        if manaCost == "0":
            return 0
        
        for char in manaCost:
            if char == '/':
                cmc -= 1
                continue
            elif char.isdigit():
                cmc += int(char)
            elif char.upper() in ['W','U','B','R','G','C']:
                    cmc += 1
            else:
                raise ValueError(f"Invalid character '{char}' in mana cost '{manaCost}'")
            
        return cmc

    def _coerce_optional_int(self, value: int | str | None) -> int | None:
        '''
        Converts value to an int when possible. Empty strings and None become None.
        '''
        if value is None:
            return None

        if isinstance(value, str):
            stripped = value.strip()
            if stripped == "":
                return None
            return int(stripped)

        return int(value)

    def getName(self) -> str:
        return self.name

    def setName(self, value: object) -> None:
        self.name = str(value)

    def getManaCost(self) -> str:
        return self.manaCost

    def setManaCost(self, value: object) -> None:
        self.manaCost = str(value)

    def getType(self) -> str | int:
        return self.type if self.type is not None else -1

    def setType(self, value: object) -> None:
        self.type = None if value is None else str(value)

    def getRarity(self) -> str | int:
        return self.rarity if self.rarity is not None else -1

    def setRarity(self, value: object) -> None:
        self.rarity = None if value is None else str(value)

    def getRulesText(self) -> str | int:
        return self.rulesText if self.rulesText is not None else -1

    def setRulesText(self, value: object) -> None:
        self.rulesText = None if value is None else str(value)

    def getFlavourText(self) -> str | int:
        return self.flavourText if self.flavourText is not None else -1

    def setFlavourText(self, value: object) -> None:
        self.flavourText = None if value is None else str(value)

    def getPower(self) -> int:
        return self.power if self.power is not None else -1

    def setPower(self, value: int | str | None) -> None:
        self.power = self._coerce_optional_int(value)

    def getToughness(self) -> int:
        return self.toughness if self.toughness is not None else -1

    def setToughness(self, value: int | str | None) -> None:
        self.toughness = self._coerce_optional_int(value)

    def getLoyalty(self) -> int:
        return self.loyalty if self.loyalty is not None else -1

    def setLoyalty(self, value: int | str | None) -> None:
        self.loyalty = self._coerce_optional_int(value)

    def getFrontPrintings(self) -> printings | int:
        return self.frontPrintings if self.frontPrintings is not None else -1

    def setFrontPrintings(self, value: printings) -> None:
        self.frontPrintings = value

    def getName2(self) -> str | int:
        return self.name2 if self.name2 is not None else -1

    def setName2(self, value: object) -> None:
        self.name2 = None if value is None else str(value)

    def getManaCost2(self) -> str | int:
        return self.manaCost2 if self.manaCost2 is not None else -1

    def setManaCost2(self, value: object) -> None:
        self.manaCost2 = None if value is None else str(value)

    def getType2(self) -> str | int:
        return self.type2 if self.type2 is not None else -1

    def setType2(self, value: object) -> None:
        self.type2 = None if value is None else str(value)

    def getRarity2(self) -> str | int:
        return self.rarity2 if self.rarity2 is not None else -1

    def setRarity2(self, value: object) -> None:
        self.rarity2 = None if value is None else str(value)

    def getRulesText2(self) -> str | int:
        return self.rulesText2 if self.rulesText2 is not None else -1

    def setRulesText2(self, value: object) -> None:
        self.rulesText2 = None if value is None else str(value)

    def getFlavourText2(self) -> str | int:
        return self.flavourText2 if self.flavourText2 is not None else -1

    def setFlavourText2(self, value: object) -> None:
        self.flavourText2 = None if value is None else str(value)

    def getPower2(self) -> int:
        return self.power2 if self.power2 is not None else -1

    def setPower2(self, value: int | str | None) -> None:
        self.power2 = self._coerce_optional_int(value)

    def getToughness2(self) -> int:
        return self.toughness2 if self.toughness2 is not None else -1

    def setToughness2(self, value: int | str | None) -> None:
        self.toughness2 = self._coerce_optional_int(value)

    def getLoyalty2(self) -> int:
        return self.loyalty2 if self.loyalty2 is not None else -1

    def setLoyalty2(self, value: int | str | None) -> None:
        self.loyalty2 = self._coerce_optional_int(value)

    def getBackPrintings(self) -> printings | int:
        return self.backPrintings if self.backPrintings is not None else -1

    def setBackPrintings(self, value: printings) -> None:
        self.backPrintings = value

    def getCMC(self) -> int:
        return Card._calcCMC(self, self.manaCost)

    def getCMC2(self) -> int:
        if self.manaCost2 is None:
            return -1
        return Card._calcCMC(self, self.manaCost2)
