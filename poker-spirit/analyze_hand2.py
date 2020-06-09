import re
from enum import Enum

# PokerStar line patterns
'''
Some of these regex patterns should return mutiple groups.
For example the seat pattern should return 4 groups:
    Group 1: The seat number
    Group 2: The player name
    Group 3: The currancy ($ or not)
    Group 4: The amount of chips

So be careful changing any of the regex patterns.

Using https://regex101.com/ for testing.
'''

# Pattern for reading number of chips or money in dollars
# If '$' appears then an integer or float
# Examples of accepted formats $1.50, $2, 10200
# Returns two groups currancy format and value
MONEY_PATTERN = '([$]?)(\\d*.?\\d+)'
# New Hand
HAND_START_PATTERN = re.compile(f'PokerStars.*Hand #(\\d+)')
# Table Info
TABLE_PATTERN = re.compile(f'Table \\\'(.+)\\\' (\\d)-max Seat #(\\d) is the button')
# Seat pattern
SEAT_PATTERN = re.compile(f'Seat (\\d): (.+) \\({MONEY_PATTERN} in chips\\)')
# Ante
POSTS_ANTE_PATTERN = re.compile(f'(.+): posts the ante {MONEY_PATTERN}')
# Blinds
POSTS_BLIND_PATTERN = re.compile(f'(.+): posts (.+) blind {MONEY_PATTERN}')
# Card string
# Card value [2 to 9 or T J Q K A] followed by card suit
CARD_PATTERN = '([2-9TJKQA])([dhsc])'
# Delt cards
DELT_CARDS_PATTERN = re.compile(f'Dealt to (.+) \\[{CARD_PATTERN} {CARD_PATTERN}\\]')
# Game States
PRE_FLOP_PATTERN = re.compile(f'\\*\\*\\* HOLE CARDS \\*\\*\\*')
FLOP_PATTERN = re.compile(f'\\*\\*\\* FLOP \\*\\*\\* \\[{CARD_PATTERN} {CARD_PATTERN} {CARD_PATTERN}\\]')
TURN_PATTERN = re.compile(f'\\*\\*\\* TURN \\*\\*\\* \\[{CARD_PATTERN} {CARD_PATTERN} {CARD_PATTERN}\\] \\[{CARD_PATTERN}\\]')
RIVER_PATTERN = re.compile(f'\\*\\*\\* RIVER \\*\\*\\* \\[{CARD_PATTERN} {CARD_PATTERN} {CARD_PATTERN} {CARD_PATTERN}\\] \\[{CARD_PATTERN}\\]')
SHOWDOWN_PATTERN = re.compile(f'\\*\\*\\* SHOW DOWN \\*\\*\\*')
SUMMARY_PATTERN = re.compile(f'\\*\\*\\* SUMMARY \\*\\*\\*')
# Actions
CALL_PATTERN = re.compile(f'(.+): calls {MONEY_PATTERN}(and is all-in|)')
BET_PATTERN = re.compile(f'(.+): bets {MONEY_PATTERN}')
RAISE_PATTERN = re.compile(f'(.+): raises {MONEY_PATTERN} to {MONEY_PATTERN}')
FOLD_PATTERN = re.compile(f'(.+): folds')
CHECK_PATTERN = re.compile(f'(.+): checks')

# States of the hand
class HAND_STATE(Enum):
    COMPULSORY_BETS = 1
    PRE_FLOP = 2
    FLOP = 3
    TURN = 4
    RIVER = 5
    SHOWDOWN = 6

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

# Player info for hand
class Player:
    def __init__(self, name):
        self._name = name
        self._starting_chips = 0
        self._seat_at_table = 0
        self._real_money = False
        self._cards = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def starting_chips(self):
        return self._starting_chips

    @starting_chips.setter
    def starting_chips(self, chips):
        self._starting_chips = chips

    @property
    def seat_at_table(self):
        return self._seat_at_table

    @seat_at_table.setter
    def seat_at_table(self, seat):
        self._seat_at_table = seat

    @property
    def cards(self):
        return self._cards

    def setCards(self, card1, card2):
        self._cards = [card1, card2]

    # True if the chips are in dollars and should have '$' in front
    def usingRealMoney(self, currancy_format):
        self._real_money = currancy_format

class Hand:
    def __init__(self):
        self._players = {}

        self._table_name = ''
        self._max_players = 9
        self._button_position = 1

        self._ante_value = 0
        self._sb_value = 0
        self._bb_value = 0
        self._player_who_posted_sb = ''
        self._player_who_posted_bb = ''
        self._real_money = False

        self._hand_state = HAND_STATE.COMPULSORY_BETS

        self._flop_cards = []
        self._turn_card = None
        self._river_card = None
    
    def getPlayer(self, player_name):
        # Return player if already exists
        if player_name in self._players:
            return self._players[player_name] 
        
        # Create new player and add them to player dict
        player = Player(player_name)
        self._players[player_name] = player
        
        return player

    @property
    def table_name(self):
        return self._table_name

    @table_name.setter
    def table_name(self, table_name):
        self._table_name = table_name

    @property
    def max_players(self):
        return self._max_players

    @max_players.setter
    def max_players(self, max_players):
        self._max_players = max_players

    @property
    def button_position(self):
        return self._button_position

    @button_position.setter
    def button_position(self, button_position):
        self._button_position = button_position

    @property
    def sb(self):
        return self._player_who_posted_sb

    @sb.setter
    def sb(self, player_name):
        self._player_who_posted_sb = player_name

    @property
    def bb(self):
        return self._player_who_posted_bb

    @bb.setter
    def bb(self, player_name):
        self._player_who_posted_bb = player_name

    @property
    def ante_value(self):
        return self._ante_value

    @ante_value.setter
    def ante_value(self, value):
        self._ante_value = value

    @property
    def sb_value(self):
        return self._sb_value

    @sb_value.setter
    def sb_value(self, value):
        self._sb_value = value

    @property
    def bb_value(self):
        return self._bb_value

    @bb_value.setter
    def bb_value(self, value):
        self._bb_value = value

    @property
    def hand_state(self):
        return self._hand_state

    @hand_state.setter
    def hand_state(self, state):
        self._hand_state = state

    # True if the chips are in dollars and should have '$' in front
    def usingRealMoney(self, currancy_format):
        self._real_money = currancy_format

    @property
    def flop_cards(self):
        return self._flop_cards

    def setFlopCards(self, card1, card2, card3):
        self._flop_cards = [card1, card2, card3]

    @property
    def turn_card(self):
        return self._turn_card

    def setTurnCard(self, card):
        self._turn_card = card

    @property
    def river_card(self):
        return self._river_card

    def setRiverCard(self, card):
        self._river_card = card

    def board(self):
        return self._flop_cards + [self._turn_card, self._river_card]

def string_to_number(string):
    string = string.strip()
    if string.isdigit():
        return int(string)
    else:
        return float(string)

def create_card_from_string(card_string, suit_string):
    # Get suit
    suit = 0
    if suit_string == 's':
        suit = CARD_SUIT.SPADE
    elif suit_string == 'c':
        suit = CARD_SUIT.CLUB
    elif suit_string == 'h':
        suit = CARD_SUIT.HEART
    elif suit_string == 'd':
        suit = CARD_SUIT.DIAMOND

    # Get card
    card_val = 0
    if card_string == '2':
        card_val = CARDS.CARD_2
    elif card_string == '3':
        card_val = CARDS.CARD_3
    elif card_string == '4':
        card_val = CARDS.CARD_4
    elif card_string == '5':
        card_val = CARDS.CARD_5
    elif card_string == '6':
        card_val = CARDS.CARD_6
    elif card_string == '7':
        card_val = CARDS.CARD_7
    elif card_string == '8':
        card_val = CARDS.CARD_8
    elif card_string == '9':
        card_val = CARDS.CARD_9
    elif card_string == 'T':
        card_val = CARDS.CARD_T
    elif card_string == 'J':
        card_val = CARDS.CARD_J
    elif card_string == 'Q':
        card_val = CARDS.CARD_Q
    elif card_string == 'K':
        card_val = CARDS.CARD_K
    elif card_string == 'A':
        card_val = CARDS.CARD_A

    return Card(card_val, suit)
    
def parse_file(path_to_file, debug = False):
    print(f"opening file = {path_to_file}")

    # Open file for parsing
    with open(path_to_file, 'r') as file:
        # Read file
        lines = file.readlines()

        # Vars for parsing
        current_hand = Hand()
        number_of_hands = 0

        # Read file line by line
        for line in lines:
            # New Hand
            if HAND_START_PATTERN.match(line):

                # Increment number of hands
                number_of_hands = number_of_hands + 1

                # Debug print info
                if debug:
                    print(f'New Hand #{number_of_hands}')

                # TODO: Save old hand to game

                # Create new hand
                current_hand = Hand()

            # Table info
            elif TABLE_PATTERN.match(line):
                # Search string and get information about seat
                results = re.search(TABLE_PATTERN, line)

                # Information found about seat
                table_name = results.group(1)
                max_players = string_to_number(results.group(2))
                button_position = string_to_number(results.group(3))
                
                # Update hand
                current_hand.table_name = table_name
                current_hand.max_players = max_players
                current_hand.button_position = button_position

                if debug:
                    print(f'Table \'{table_name}\' {max_players}-max Seat #{button_position} is the button')

            # Seat
            elif SEAT_PATTERN.match(line):
                # Search string and get information about seat
                results = re.search(SEAT_PATTERN, line)

                # Information found about seat
                player_seat = string_to_number(results.group(1))
                player_name = results.group(2)
                chip_currancy = results.group(3)
                player_chips = string_to_number(results.group(4))

                # Add player to hand
                player = current_hand.getPlayer(player_name)

                # Add seat number to player
                player.seat_at_table = player_seat

                # Add number of chips to player
                player.starting_chips = player_chips

                # Change chip currancy of player if using real money
                if chip_currancy == '$':
                    player.usingRealMoney(True)

                # Debug print info
                if debug:
                    print(f"{player_name} at seat #{player_seat} has {chip_currancy}{player_chips} in chips")
            
            # If Ante
            elif POSTS_ANTE_PATTERN.match(line):
                # Search string
                results = re.search(POSTS_ANTE_PATTERN, line)

                # Information found
                player_name = results.group(1)
                chip_currancy = results.group(2)
                chips = string_to_number(results.group(3))

                # Update hand information
                current_hand.ante_value = chips

                # Change chip currancy of player if using real money
                if chip_currancy == '$':
                    current_hand.usingRealMoney(True)

                # Debug print info
                if debug:
                    print(f"{player_name} posts ante of {chip_currancy}{chips} in chips")

            # If Small or Big Blind
            elif POSTS_BLIND_PATTERN.match(line):
                # Search string
                results = re.search(POSTS_BLIND_PATTERN, line)

                # Information found about blind
                player_name = results.group(1)
                blind = results.group(2) # small or big
                chip_currancy = results.group(3)
                chips = string_to_number(results.group(4))

                # Update hand information
                if blind == 'small':
                    current_hand.sb = player_name
                    current_hand.sb_value = chips
                elif blind == 'big':
                    current_hand.bb = player_name
                    current_hand.bb_value = chips

                # Change chip currancy of player if using real money
                if chip_currancy == '$':
                    current_hand.usingRealMoney(True)

                # Debug print info
                if debug:
                    print(f"{player_name} posts the {blind} blind of {chip_currancy}{chips} in chips")

            elif CALL_PATTERN.match(line):
                # Search string
                results = re.search(CALL_PATTERN, line)

                # Information found about seat
                player_name = results.group(1)
                chip_currancy = results.group(2)
                player_chips = string_to_number(results.group(3))
                all_in_text = results.group(4)

                all_in = False
                if len(all_in_text) > 0:
                    all_in = True

                # TODO : Update hand

                # Debug print info
                if debug:
                    all_in_text = ''

                    if all_in:
                        all_in_text = 'and is all-in'

                    print(f"{player_name} calls {chip_currancy}{player_chips} {all_in_text}")

            elif BET_PATTERN.match(line):
                # Search string
                results = re.search(BET_PATTERN, line)

                # Information found about seat
                player_name = results.group(1)
                chip_currancy = results.group(2)
                player_chips = string_to_number(results.group(3))

                # TODO : Update hand

                # Debug print info
                if debug:
                    print(f"{player_name} bets {chip_currancy}{player_chips}")

            elif RAISE_PATTERN.match(line):
                # Search string
                results = re.search(RAISE_PATTERN, line)

                # Information found about seat
                player_name = results.group(1)
                chip_currancy = results.group(2)
                current_chips = string_to_number(results.group(3))
                raised_chips = string_to_number(results.group(5))

                # TODO : Update hand

                # Debug print info
                if debug:
                    print(f"{player_name} raise {chip_currancy}{current_chips} to {chip_currancy}{raised_chips}")

            elif FOLD_PATTERN.match(line):
                # Search string
                results = re.search(FOLD_PATTERN, line)

                # Information found about seat
                player_name = results.group(1)

                # TODO : Update hand

                # Debug print info
                if debug:
                    print(f"{player_name} folds")

            elif CHECK_PATTERN.match(line):
                # Search string
                results = re.search(CHECK_PATTERN, line)

                # Information found about seat
                player_name = results.group(1)

                # TODO : Update hand

                # Debug print info
                if debug:
                    print(f"{player_name} checks")

            # Dealt Cards
            elif DELT_CARDS_PATTERN.match(line):
                # Search string
                results = re.search(DELT_CARDS_PATTERN, line)

                # Information found about cards dealt
                player_name = results.group(1)
                card1_val = results.group(2) # 2-10 J Q K A
                card1_suit = results.group(3) # s c h d
                card2_val = results.group(4)
                card2_suit = results.group(5)

                # Create cards from string
                card1 = create_card_from_string(card1_val, card1_suit)
                card2 = create_card_from_string(card2_val, card2_suit)

                # Update player cards
                player = current_hand.getPlayer(player_name)
                player.setCards(card1, card2)

                # Debug print info
                if debug:
                    print(f"{player_name} was dealt [{card1} {card2}]")

            # If Pre Flop
            elif PRE_FLOP_PATTERN.match(line):
                # Update hand state
                current_hand.hand_state = HAND_STATE.PRE_FLOP

                # Debug print info
                if debug:
                    print(f"Start of Pre-Flop")

            # If Flop
            elif FLOP_PATTERN.match(line):
                # Update hand state
                current_hand.hand_state = HAND_STATE.FLOP

                # Search string
                results = re.search(FLOP_PATTERN, line)

                # Information found about cards dealt
                card1_val = results.group(1) # 2-10 J Q K A
                card1_suit = results.group(2) # s c h d
                card2_val = results.group(3)
                card2_suit = results.group(4)
                card3_val = results.group(5)
                card3_suit = results.group(6)

                # Create cards from string
                card1 = create_card_from_string(card1_val, card1_suit)
                card2 = create_card_from_string(card2_val, card2_suit)
                card3 = create_card_from_string(card3_val, card3_suit)

                # Add flopped cards to hand
                current_hand.setFlopCards(card1, card2, card3)

                # Debug print info
                if debug:
                    print(f"Start of Flop [{card1} {card2} {card3}]")

            # If Turn
            elif TURN_PATTERN.match(line):
                # Update hand state
                current_hand.hand_state = HAND_STATE.TURN

                # Search string
                results = re.search(TURN_PATTERN, line)

                # Information found about cards dealt
                card_val = results.group(7) # 2-10 J Q K A
                card_suit = results.group(8) # s c h d

                # Create cards from string
                card = create_card_from_string(card_val, card_suit)

                # Add turn card to hand
                current_hand.setTurnCard(card)

                # Debug print info
                if debug:
                    print(f"Start of Turn [{card}]")

            # If River
            elif RIVER_PATTERN.match(line):
                # Update hand state
                current_hand.hand_state = HAND_STATE.RIVER

                # Search string
                results = re.search(RIVER_PATTERN, line)

                # Information found about cards dealt
                card_val = results.group(9) # 2-10 J Q K A
                card_suit = results.group(10) # s c h d

                # Create cards from string
                card = create_card_from_string(card_val, card_suit)

                # Add river card to hand
                current_hand.setRiverCard(card)

                # Debug print info
                if debug:
                    print(f"Start of River [{card}]")

            # If Showdown
            elif SHOWDOWN_PATTERN.match(line):
                # Update hand state
                current_hand.hand_state = HAND_STATE.SHOWDOWN

                # Debug print info
                if debug:
                    print(f"Start of Showdown")
           
            # If Summary
            elif SUMMARY_PATTERN.match(line):
                # Debug print info
                if debug:
                    print(f"Summary")
                    print(f'Final board {current_hand.board()}')


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()
    # get env vars from .env file
    path_to_file = os.getenv("PATH_TO_FILE", ".")

    parse_file(path_to_file, True)

    input('Press any key to continue ...\n')