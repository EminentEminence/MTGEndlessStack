class printings:
    '''
    A class which is used to store printings for any given card.
    Attributes:
        printings (list): A list of printing objects. (The printings of the card)
    '''
    def __init__(self):
        '''
        Initializes the printings class with an empty list of printings.
        '''
        self.printings = []

class printing:
    '''
    A class for an individual printing of a card. This is used to store the image path, type of printing, and artist name (if applicable).
    Attributes:
        image (str): Image path of the card.
        type (str): Type of printing.
        artist (str): Artist name (if applicable).
    '''
    def __init__(self, address: str, type, artist: str = ""):
        '''
        Initializes the printing class with the given image path, type of printing, and artist name (if applicable).

        Args:
            address (str): Image path of the card.
            type (str): Type of printing.
            artist (str, optional): Artist name (if applicable). Defaults to "".
        '''
        self.image = address.replace("\\", "/")
        self.type = type
        self.artist = artist

