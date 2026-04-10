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
        power (str): The power of the card (if applicable).
        toughness (str): The toughness of the card (if applicable).
        loyalty (str): The loyalty of the card (if applicable).
        frontPrintings (printings): The printings of the front face of the card.
        
        name2 (str): The name of the back face of the card (if applicable).
        manaCost2 (str): The mana cost of the back face of the card (if applicable).
        type2 (str): The type of the back face of the card (if applicable).
        rarity2 (str): The rarity of the back face of the card (if applicable).
        rulesText2 (str): The rules text of the back face of the card (if applicable).
        flavourText2 (str): The flavor text of the back face of the card (if applicable).
        power2 (str): The power of the back face of the card (if applicable).
        toughness2 (str): The toughness of the back face of the card (if applicable).
        loyalty2 (str): The loyalty of the back face of the card (if applicable).
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

    def get(self,attribute: str,side="front") -> object:
        '''
        gets the value of the specified attribute for the specified side of the card.
        Replaces the need for having multiple Getters for each attribute and handles the special case of calculating CMC without needing to store it as an attribute.
        Also simplifies getting information for the back face of the card by using the same references as the front.

        Args:
            attribute (str): The name of the attribute to get.
            side (str, optional): The side of the card to get the attribute from ("front" or "back"). Defaults to "front".
        
        Returns:
            object: The value of the specified attribute for the specified side of the card.
        '''
        if not hasattr(self, attribute):
            raise AttributeError(f"'Card' object has no attribute '{attribute}'")
        elif attribute == "cmc":
            if side == "front":
                return Card._calcCMC(self, self.manaCost)
            elif side == "back":
                return Card._calcCMC(self, self.manaCost2) if self.manaCost2 is not None else None
            else:
                raise ValueError(f"Invalid side '{side}'")
        
        return getattr(self, attribute if side == "front" else attribute+"2")

    def set(self,attribute: str,value : object ,side="front"):
        '''
        sets the value of the specified attribute for the specified side of the card.

        Args:
            attribute (str): The name of the attribute to set.
            value (object): The value to set for the attribute.
            side (str, optional): The side of the card to set the attribute for ("front" or "back"). Defaults to "front".
        '''
        if not hasattr(self, attribute):
            raise AttributeError(f"'Card' object has no attribute '{attribute}'")
        
        setattr(self, attribute if side == "front" else attribute+"2", value)
