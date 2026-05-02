from system.cardhandling.card import Card

'''
THIS IS A TEMPORARY FILE
THESE FUNCTIONS WILL NEED TO BE DEFINED ELSEWHERE
'''


def activeAbility(*actions, cost='0', tap=False, sacrifice=False, discard=False, exile=False, returnToHand=False, returnToGraveyard=False):
    '''
    Function which allows for an ability to be triggered by the player by paying a cost

    Args:
        actions (function): The functions which will be executed when the ability is activated
        cost (str, optional): The mana cost to activate the ability. Defaults to '0'.
        tap (bool, optional): Whether the card must be tapped to activate the ability. Defaults to False.
        sacrifice (bool, optional): Whether the card must be sacrificed to activate the ability. Defaults to False.
        discard (bool, optional): Whether a card must be discarded to activate the ability. Defaults to False.
        exile (bool, optional): Whether a card must be exiled to activate the ability. Defaults to False.
        returnToHand (bool, optional): Whether a card must be returned to hand to activate the ability. Defaults to False.
        returnToGraveyard (bool, optional): Whether a card must be returned to graveyard to activate the ability. Defaults to False.
    '''

def forEach(targets: list[Card], action, end=False):
    '''
    Function which allows for an action to be performed on each of a group of targets

    Args:
        targets (list): A list of targets to perform the action on
        action (function): The function which will be executed on each target
        end (Condition, optional): A condition which, when met, will end the loop. Defaults to False.

    Parameters:
        forEachTarget - The current target being acted upon in the loop
    '''

def target(num=1, repeat=False, filter=None) -> list[Card]:
    '''
    Function which allows for a player to select a target for an ability or spell with restrictions on the number and type of targets

    Args:
        num (int, optional): The number of targets to select. Defaults to 1.
        repeat (bool, optional): Whether the player can select the same target multiple times. Defaults to False.
        filter (String, optional): A string representing the restrictions on the type of targets that can be selected. Defaults to None.
    
    Returns:
        list[Card]: The selected target(s) as Card object(s), or an empty list if no valid target was selected.
    '''
    return [Card()]

def damage(target: list[Card], value):
    '''
    Function which allows for damage to be dealt to a target

    Args:
        target (list[Card]): The target(s) to deal damage to
        value (int): The amount of damage to deal
    '''

def isIllegal(target: list[Card]) -> bool:
    '''
    Function which checks if a target is illegal for an ability or spell

    Args:
        target (list[Card]): The target(s) to check for legality
    Returns:
        bool: True if the target is illegal, False otherwise
    '''
    return False

def beforeCast(function):
    '''
    A decorator function which allows for a function to be executed before a spell is cast

    Args:
        function (function): The function to execute before the spell is cast
    '''

def reduceCostForEach(target, cost='0', zone=None, filter=None):
    '''
    Function which reduces a spell's cost by an amount for each matching object in a zone

    Args:
        target (Card): The spell/card whose cost is being reduced.
        cost (str, optional): Reduction amount per match. Defaults to '0'.
        zone (str, optional): Zone to count matches in. Defaults to None.
        filter (str, optional): Restriction for counted objects. Defaults to None.
    '''

def condition(value, comparative, comparison='Equal', onFalse=None, onTrue=None):
    '''
    Function which checks a condition and executes different functions based on the result

    Args:
        value (object): The value to check the condition against
        comparison (str, optional): The type of comparison to perform. Defaults to 'Equal'. options: 'Equal', 'NotEqual', 'Greater', 'Less', 'GreaterEqual', 'LessEqual', 'Contains', 'NotContains'
        comparative (object): The value to compare against
        onFalse (function, optional): The function to execute if the condition is false. Defaults to None.
        onTrue (function, optional): The function to execute if the condition is true. Defaults to None.
    '''

def onCast(function):
    '''
    A decorator function which allows for a function to be executed when a spell is cast

    Args:
        function (function): The function to execute when the spell is cast
    '''

def onAttack(function):
    '''
    A decorator function which allows for a function to be executed when a creature attacks

    Args:
        function (function): The function to execute on attack
    '''

def divide(num, div, round='Avg'):
    '''
    Function which divides a number into a specified number of parts and rounds the result in a specified way

    Args:
        num (int): The number to divide
        div (int): The number of parts to divide into
        round (str, optional): The method to use for rounding. Defaults to 'Avg'. options: 'Up', 'Down', 'Avg'
    
    Returns:
        int: The result of the division
    '''

def multiply(num1: int, num2: int) -> int:
    '''
    Function which multiplies two numbers

    Args:
        num1 (int): The first number
        num2 (int): The second number

    Returns:
        int: The result of the multiplication
    '''
    return num1 * num2

def counterspell(target: list[Card]):
    '''
    Function which counters a spell...
    Args:
        target (list[Card]): The target(s) to counter
    '''

def counterUnlessPay(target, cost='0'):
    '''
    Function which counters a spell or ability unless its controller pays a cost

    Args:
        target (Card | list[Card]): The spell/ability target(s) to counter
        cost (str, optional): The mana cost the controller may pay to prevent the counter. Defaults to '0'.
    '''

def tapCard(target: list[Card]):
    '''
    Function which taps a card
    Args:
        target (list[Card]): The target(s) to tap
    '''

def removeAbilities(target: list[Card], until):
    '''
    Function which removes all abilities from a card until a specified condition is met
    Args:
        target (list[Card]): The target(s) to remove abilities from
        until (Condition): The condition until which the abilities will be removed
    '''

def passiveAbility(*abilities):
    '''
    Function which grants a card passive abilities

    Args:
        abilities (function): The functions which will be executed as passive abilities i.e every game update tick
    '''
def keyWords(*keywords):
    '''
    Function which grants a card keywords

    Args:
        keywords (str): The keywords to grant to the card
    '''

def pay(cost='0', discard=False, discardHand=False, sacrifice=False, exile=False, onPay=None):
    '''
    Function which allows for a player to pay a cost to activate an ability or cast a spell, and executes a function when the cost is paid

    Args:
        cost (str, optional): The mana cost to pay. Defaults to '0'.
        discard (bool, optional): Whether a card must be discarded to pay the cost. Defaults to False.
        discardHand (bool, optional): Whether the player's entire hand must be discarded to pay the cost. Defaults to False.
        sacrifice (bool, optional): Whether a card must be sacrificed to pay the cost. Defaults to False.
        exile (bool, optional): Whether a card must be exiled to pay the cost. Defaults to False.
        onPay (function): The functions to execute when the cost is paid
    '''

def canBeCommander(value: bool):
    '''
    Function which sets whether a card can be a commander in the commander format

    Args:
        value (bool): Whether the card can be a commander
    '''

def addCounter(target, counterType, num=1):
    '''
    Function which adds counters of a given type to a target

    Args:
        target (Card | list[Card]): The target(s) receiving counters.
        counterType (str): The type/name of counter to add.
        num (int, optional): Number of counters to add. Defaults to 1.
    '''

def colorCount(mana):
    '''
    Function which counts distinct colors present in a mana payment or pool object

    Args:
        mana (object): Mana representation to inspect for colors.
    '''

def scry(amount: int):
    '''
    Function which lets a player scry a number of cards

    Args:
        amount (int): The number of cards to scry
    '''

def castFromHand(filter=None, maxManaValue=None, withoutPay=False, optional=False):
    '''
    Function which allows casting a spell from hand with optional restrictions and cost handling

    Args:
        filter (str, optional): Restrictions on castable card types. Defaults to None.
        maxManaValue (int, optional): Maximum mana value of the castable spell. Defaults to None.
        withoutPay (bool, optional): Whether to cast without paying mana cost. Defaults to False.
        optional (bool, optional): Whether casting is optional. Defaults to False.
    '''

def flashback(cost='0'):
    '''
    Function which grants flashback with an alternate casting cost from graveyard

    Args:
        cost (str, optional): The flashback cost. Defaults to '0'.
    '''

def exileTop(zone, amount=1, exiledWith=None):
    '''
    Function which exiles cards from the top of a library and can tag them to a source

    Args:
        zone (object): The source zone, typically a player's library.
        amount (int, optional): Number of cards to exile from top. Defaults to 1.
        exiledWith (str, optional): Source tag for "exiled with" tracking. Defaults to None.
    '''

def playFromExile(filter=None, exiledWith=None, optional=True):
    '''
    Function which allows cards in exile to be played with optional restrictions

    Args:
        filter (str, optional): Restrictions on playable card types. Defaults to None.
        exiledWith (str, optional): Source tag for cards exiled with a specific object. Defaults to None.
        optional (bool, optional): Whether the play permission is optional. Defaults to True.
    '''

def exile(target):
    '''
    Function which exiles one or more target cards/permanents/spells

    Args:
        target (Card | list[Card]): The target(s) to exile.
    '''

def createCopy(target, legendary=True):
    '''
    Function which creates a copy token of a target object with optional overrides

    Args:
        target (object): The object to copy, including '{cardName}' self-reference.
        legendary (bool, optional): Whether the created copy remains legendary. Defaults to True.
    '''

def atBeginningEndStep(action):
    '''
    Function which schedules an action at the beginning of your end step

    Args:
        action (function): The action to execute at beginning of end step.
    '''

def surveil(amount: int):
    '''
    Function which lets a player surveil a number of cards

    Args:
        amount (int): The number of cards to surveil
    '''

def castFromGraveyard(target, until=None, optional=True, withoutPay=False, exileIfWouldBePutIntoGraveyard=False):
    '''
    Function which allows casting a specific card from graveyard with timing and replacement restrictions

    Args:
        target (Card): The graveyard card that may be cast.
        until (object, optional): Expiration point for permission, e.g. endTurn. Defaults to None.
        optional (bool, optional): Whether casting is optional. Defaults to True.
        withoutPay (bool, optional): Whether to cast without paying mana cost. Defaults to False.
        exileIfWouldBePutIntoGraveyard (bool, optional): Exile it instead of putting it into graveyard. Defaults to False.
    '''

def returnToBattlefield(target):
    '''
    Function which moves one or more target cards to the battlefield

    Args:
        target (Card | list[Card]): The target(s) to return to battlefield.
    '''

def createToken(name=None, type=None, colors=None, power=None, toughness=None, num=1):
    '''
    Function which creates creature or noncreature token(s) with specified characteristics

    Args:
        name (str, optional): Token name. Defaults to None.
        type (str, optional): Token type line, e.g. 'Creature - Spirit'. Defaults to None.
        colors (list[str], optional): Token colors, e.g. ['R', 'W']. Defaults to None.
        power (int, optional): Token power for creatures. Defaults to None.
        toughness (int, optional): Token toughness for creatures. Defaults to None.
        num (int, optional): Number of tokens to create. Defaults to 1.
    '''