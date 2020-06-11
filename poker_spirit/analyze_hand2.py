import re
from enum import Enum

from hand_state import HAND_STATE
from card import CARD_SUIT, CARDS, Card
from fraction import Fraction

from player_hand import PlayerHand
from hand import Hand

from player_stats import PlayerStats
from game import Game


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
HAND_START_PATTERN = re.compile(f'PokerStars Hand #(\\d+): (.+)')
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
    print(f'Parsing file: {path_to_file}')

    game = Game()

    # Open file for parsing
    with open(path_to_file, 'r', encoding='utf-8-sig') as file:
        # Read file
        lines = file.readlines()

        # Vars for parsing
        current_hand = None
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
                player = current_hand.get_player(player_name)

                # Add seat number to player
                player.seat_at_table = player_seat

                # Add number of chips to player
                player.starting_chips = player_chips

                # Change chip currancy of player if using real money
                if chip_currancy == '$':
                    player.using_real_money(True)

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
                    current_hand.using_real_money(True)

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
                    current_hand.using_real_money(True)

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
                if len(all_in_text.strip()) > 0:
                    all_in = True

                # Update hand
                current_hand.player_calls(player_name, player_chips, all_in)

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

                # Update hand
                current_hand.player_bets(player_name, player_chips)

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

                # Update hand
                current_hand.player_raises(player_name, current_chips, raised_chips)

                # Debug print info
                if debug:
                    print(f"{player_name} raise {chip_currancy}{current_chips} to {chip_currancy}{raised_chips}")

            elif FOLD_PATTERN.match(line):
                # Search string
                results = re.search(FOLD_PATTERN, line)

                # Information found about seat
                player_name = results.group(1)

                # Update hand
                current_hand.player_folds(player_name)

                # Debug print info
                if debug:
                    print(f"{player_name} folds")

            elif CHECK_PATTERN.match(line):
                # Search string
                results = re.search(CHECK_PATTERN, line)

                # Information found about seat
                player_name = results.group(1)

                # Update hand
                current_hand.player_checks(player_name)

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
                player = current_hand.get_player(player_name)
                player.set_cards(card1, card2)

                # Debug print info
                if debug:
                    print(f"{player_name} was dealt [{card1} {card2}]")

            # If Pre Flop
            elif PRE_FLOP_PATTERN.match(line):
                # Update hand state
                current_hand.init_pre_flop()

                # Debug print info
                if debug:
                    print(f"Start of Pre-Flop")

            # If Flop
            elif FLOP_PATTERN.match(line):
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
                current_hand.set_flop_cards(card1, card2, card3)

                # Update hand state
                current_hand.init_flop()

                # Debug print info
                if debug:
                    print(f"Start of Flop [{card1} {card2} {card3}]")

            # If Turn
            elif TURN_PATTERN.match(line):
                # Search string
                results = re.search(TURN_PATTERN, line)

                # Information found about cards dealt
                card_val = results.group(7) # 2-10 J Q K A
                card_suit = results.group(8) # s c h d

                # Create cards from string
                card = create_card_from_string(card_val, card_suit)

                # Add turn card to hand
                current_hand.set_turn_card(card)

                # Update hand state
                current_hand.init_turn()

                # Debug print info
                if debug:
                    print(f"Start of Turn [{card}]")

            # If River
            elif RIVER_PATTERN.match(line):
                # Search string
                results = re.search(RIVER_PATTERN, line)

                # Information found about cards dealt
                card_val = results.group(9) # 2-10 J Q K A
                card_suit = results.group(10) # s c h d

                # Create cards from string
                card = create_card_from_string(card_val, card_suit)

                # Add river card to hand
                current_hand.set_river_card(card)

                # Update hand state
                current_hand.init_river()

                # Debug print info
                if debug:
                    print(f"Start of River [{card}]")

            # If Showdown
            elif SHOWDOWN_PATTERN.match(line):
                # Update hand state
                current_hand.init_showdown()

                # Debug print info
                if debug:
                    print(f"Start of Showdown")
           
            # If Summary
            elif SUMMARY_PATTERN.match(line):
                # Update hand state
                current_hand.finalize_hand()

                # Save hand to game
                game.add_hand(current_hand)

                # Debug print info
                if debug:
                    print(f"Summary")
                    print(current_hand)

    return game

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()
    # get env vars from .env file
    path_to_file = os.getenv("PATH_TO_FILE", ".")

    game = parse_file(path_to_file, True)

    print(game)

    input('Press any key to continue ...\n')
