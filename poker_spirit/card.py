from enum import Enum

# Card suit
class CARD_SUIT(Enum):
    SPADE = 1
    CLUB = 2
    HEART = 3
    DIAMOND = 4

# Cards
class CARDS(Enum):
    CARD_2 = 2
    CARD_3 = 3
    CARD_4 = 4
    CARD_5 = 5
    CARD_6 = 6
    CARD_7 = 7
    CARD_8 = 8
    CARD_9 = 9
    CARD_T = 10
    CARD_J = 11
    CARD_Q = 12
    CARD_K = 13
    CARD_A = 14

# Card
class Card:
    def __init__(self, card, suit):
        self._card = card
        self._suit = suit

    @property
    def card(self):
        return self._card

    @property
    def suit(self):
        return self._suit

    def __str__(self):
        # Get suit
        suit_string = ''
        if self._suit == CARD_SUIT.SPADE:
            suit_string = 's'
        elif self._suit == CARD_SUIT.CLUB:
            suit_string = 'c'
        elif self._suit == CARD_SUIT.HEART:
            suit_string = 'h'
        elif self._suit == CARD_SUIT.DIAMOND:
            suit_string = 'd'

        # Get card
        card_string = 0
        if self._card == CARDS.CARD_2:
            card_string = '2'
        elif self._card == CARDS.CARD_3:
            card_string = '3'
        elif self._card == CARDS.CARD_4:
            card_string = '4'
        elif self._card == CARDS.CARD_5:
            card_string = '5'
        elif self._card == CARDS.CARD_6:
            card_string = '6'
        elif self._card == CARDS.CARD_7:
            card_string = '7'
        elif self._card == CARDS.CARD_8:
            card_string = '8'
        elif self._card == CARDS.CARD_9:
            card_string = '9'
        elif self._card == CARDS.CARD_T:
            card_string = 'T'
        elif self._card == CARDS.CARD_J:
            card_string = 'J'
        elif self._card == CARDS.CARD_Q:
            card_string = 'Q'
        elif self._card == CARDS.CARD_K:
            card_string = 'K'
        elif self._card == CARDS.CARD_A:
            card_string = 'A'

        return f'{card_string}{suit_string}'

    def __repr__(self):
        return self.__str__()
