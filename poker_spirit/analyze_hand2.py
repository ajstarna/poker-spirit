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

# States of the hand
class HAND_STATE(Enum):
    COMPULSORY_BETS = 1
    PRE_FLOP = 2
    FLOP = 3
    TURN = 4
    RIVER = 5
    SHOWDOWN = 6
    END = 7

    @staticmethod
    def toString(hand_state):
        if hand_state == HAND_STATE.COMPULSORY_BETS:
            return 'COMPULSORY_BETS'
        elif hand_state == HAND_STATE.PRE_FLOP:
            return 'PRE_FLOP'
        elif hand_state == HAND_STATE.FLOP:
            return 'FLOP'
        elif hand_state == HAND_STATE.TURN:
            return 'TURN'
        elif hand_state == HAND_STATE.RIVER:
            return 'RIVER'
        elif hand_state == HAND_STATE.SHOWDOWN:
            return 'SHOWDOWN'
        else:
            return 'UNKNOWN'

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

class Fraction:
    def __init__(self, n = 0, d = 0):
        self._n = n
        self._d = d

    @property
    def numerator(self):
        return self._n

    @numerator.setter
    def numerator(self, val):
        self._n = val

    @property
    def denominator(self):
        return self._d

    @denominator.setter
    def denominator(self, val):
        self._d = val

    def getPercent(self, precision=1):
        if self._d == 0:
            return 0.0
        
        return round(100*self._n/self._d, precision)

    def __str__(self):
        return f'{self._n}/{self._d}'

# Player info for hand
# Used for parsing file
class PlayerHand:
    def __init__(self, name):
        # Info
        self._name = name
        self._starting_chips = 0
        self._seat_at_table = 0
        self._real_money = False
        self._cards = []

        # Stats
        self._folded = False
        self._folded_state = 0
        # Flops Seen (FS)
        self._fs = False
        # Voluntarily Put $ in Pot (VPiP)
        self._vpip = False
        # Preflop Raise (PFR)
        self._pfr = False
        # Called Preflop Raise (CPFR)
        self._cpfr = False
        self._opt_cpfr = False
        # Unopened Preflop Raise (UOPFR)
        self._uopfr = False
        self._opt_uopfr = False
        # Three-bet Pre-flop (3B)
        self._3b = False
        self._opt_3b = False
        # Folded to Three-Bet Preflop (F3B)
        self._f3b = False
        self._opt_f3b = False
        # Four-bet Pre-flop (4B)
        self._4b = False
        self._opt_4b = False
        # Folded to Four-Bet Preflop (F4B)
        self._f4b = False
        self._opt_f4b = False

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

    ## Stats ##

    # Folded
    def hasFolded(self):
        return self._folded

    def foldedInHandState(self):
        return self._folded_state

    def fold(self, hand_state):
        self._folded = True
        self._folded_state = hand_state

    # Flops Seen (FS)
    def hasSeenFlop(self):
        return self._fs

    def seenFlop(self):
        self._fs = True
    
    # Voluntarily Put $ in Pot (VPiP)
    def hasVPiP(self):
        return self._vpip

    def vpip(self):
        self._vpip = True
    
    # Preflop Raise (PFR)
    def hasPFR(self):
        return self._pfr

    def pfr(self):
        self._pfr = True

    # Called Preflop Raise (CPFR)
    def hasCPFR(self):
        return self._cpfr
    
    def hasOptCPFR(self):
        return self._opt_cpfr
    
    def cpfr(self):
        self._cpfr = True

    def optCPFR(self):
        self._opt_cpfr = True

    # Unopened Preflop Raise (UOPFR)
    def hasUOPFR(self):
        return self._uopfr
    
    def hasOptUOPFR(self):
        return self._opt_uopfr
    
    def uopfr(self):
        self._uopfr = True

    def optUOPFR(self):
        self._opt_uopfr = True
    
    # Three-bet Pre-flop (3B)
    def has3B(self):
        return self._3b

    def p3b(self):
        self._3b = True

    # Opt for 3B
    def hasOpt3B(self):
        return self._opt_3b

    def opt3B(self):
        self._opt_3b = True
    
    # Folded to Three-Bet Preflop (F3B)
    def hasF3B(self):
        return self._f3b

    def f3b(self):
        self._f3b = True

    # Opt to fold 3B
    def hasOptF3B(self):
        return self._opt_f3b

    def optF3B(self):
        self._opt_f3b = True

    # Four-bet Pre-flop (4B)
    def has4B(self):
        return self._4b

    def p4b(self):
        self._4b = True

    # Opt for 4B
    def hasOpt4B(self):
        return self._opt_4b

    def opt4B(self):
        self._opt_4b = True

    # Folded to Four-Bet Preflop (F4B)
    def hasF4B(self):
        return self._f4b

    def f4b(self):
        self._f4b = True

    # Opt to fold 4B
    def hasOptF4B(self):
        return self._opt_f4b

    def optF4B(self):
        self._opt_f4b = True

    def __str__(self):
        # Info
        output = f'Player Hand Stats for {self._name}\n'

        currancy = ''
        if self._real_money:
            currancy = '$'
        
        output += f'Seat #{self._seat_at_table} with {currancy}{self._starting_chips} in chips\n'
        output += f'Dealt {self._cards}\n'

        # Stats
        if self._folded:
            output += f'Player folded in {HAND_STATE.toString(self._folded_state)}\n'

        if self._fs:
            output += f'Player has seen flop\n'

        if self._vpip:
            output += f'Player has voluntarily put money in pot (VPiP)\n'

        if self._pfr:
            output += f'Player has preflop raised (PFR)\n'

        if self._cpfr:
            output += f'Player has called preflop raised (CPFR)\n'
        elif self._opt_cpfr:
            output += f'Player had an opportunity to call preflop raise but didn\'t\n'

        if self._uopfr:
            output += f'Player has made an unopened preflop raise (UOPFR)\n'
        elif self._opt_uopfr:
            output += f'Player had an opportunity to make unopened preflop raise but didn\'t\n'

        '''
        # Three-bet Pre-flop (3B)
        # Folded to Three-Bet Preflop (F3B)
        self._3b = False
        self._f3b = False
        self._opt_3b = False
        # Four-bet Pre-flop (4B)
        # Folded to Four-Bet Preflop (F4B)
        self._4b = False
        self._f4b = False
        self._opt_4b = False
        '''

        return output

# A single hand
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

        self._pre_flop_first_action = True
        self._flop_first_action = True
        self._turn_first_action = True
        self._river_first_action = True

        self._pre_flop_bet = False
        self._flop_bet = False
        self._turn_bet = False
        self._river_bet = False

        self._number_of_raises_pre_flop = 0
        self._number_of_raises_flop = 0
        self._number_of_raises_turn = 0
        self._number_of_raises_river = 0
    
    def getPlayer(self, player_name):
        # Return player if already exists
        if player_name in self._players:
            return self._players[player_name]
        
        # Create new player and add them to player dict
        player = PlayerHand(player_name)
        self._players[player_name] = player
        
        return player

    def getAllPlayers(self):
        return self._players.values()

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

    # True if the chips are in dollars and should have '$' in front
    def usingRealMoney(self, currancy_format):
        self._real_money = currancy_format

    @property
    def hand_state(self):
        return self._hand_state

    def initPreFlop(self):
        self._hand_state = HAND_STATE.PRE_FLOP

    def endPreFlop(self):
        for player in self._players.values():
            # Has folded? If not then they have seen the flop
            if not player.hasFolded():
                player.seenFlop()

    def initFlop(self):
        # End Pre-Flop
        self.endPreFlop()

        # Update state of hand
        self._hand_state = HAND_STATE.FLOP

    def initTurn(self):
        self._hand_state = HAND_STATE.TURN

    def initRiver(self):
        self._hand_state = HAND_STATE.RIVER

    def initShowdown(self):
        self._hand_state = HAND_STATE.SHOWDOWN

    def finalizeHand(self):
        self._hand_state = HAND_STATE.END

    def playerCalls(self, player_name, amount, all_in = False):
        # Get Player
        player = self.getPlayer(player_name)
        
        # Update VPiP
        player.vpip()

        # Is this before the flop?
        if self._hand_state == HAND_STATE.PRE_FLOP:
            # Check if player called a pre-flop raise
            if self._number_of_raises_pre_flop > 0:
                player.cpfr()
                player.optCPFR()

            # Check if opportunity for Unopened Preflop Raise (UOPFR)
            # No one before has bet or raised, everyone has called or folded
            if self._number_of_raises_pre_flop == 0 \
                and not self._pre_flop_bet \
                and not self._pre_flop_first_action:
                player.optUOPFR()

            # Check if someone already raised and opportunity for 3B
            if self._number_of_raises_pre_flop == 1:
                player.opt3B()
                player.optF3B()

            # Check if two people already raised and opportunity for 4B
            if self._number_of_raises_pre_flop == 2:
                player.opt4B()
                player.optF4B()

            # Should be called last
            self._pre_flop_first_action = False

    def playerBets(self, player_name, ammount):
         # Get Player
        player = self.getPlayer(player_name)
        
        # Update VPiP
        player.vpip()

        # Is this before the flop?
        # This might be immposible code
        if self._hand_state == HAND_STATE.PRE_FLOP:
            # Check if opportunity for Unopened Preflop Raise (UOPFR)
            # No one before has bet or raised, everyone has called or folded
            if self._number_of_raises_pre_flop == 0 \
                and not self._pre_flop_bet \
                and not self._pre_flop_first_action:
                player.optUOPFR()

            self._pre_flop_bet = True

            # Should be called last
            self._pre_flop_first_action = False

        # Is this post flop?
        elif self._hand_state == HAND_STATE.FLOP:
            self._flop_bet = True

        # Is this after the turn?
        elif self._hand_state == HAND_STATE.TURN:
            self._turn_bet = True
        
        # Is this after the river?
        elif self._hand_state == HAND_STATE.RIVER:
            self._river_bet = True

    def playerRaises(self, player_name, current_ammount, new_ammount):
        # Get Player
        player = self.getPlayer(player_name)
        
        # Update VPiP
        player.vpip()

        # Is this before the flop?
        if self._hand_state == HAND_STATE.PRE_FLOP:
            # This is a pre-flop raise (pfr)
            player.pfr()

            # Check if player raised to a pre-flop raise
            if self._number_of_raises_pre_flop > 0:
                player.optCPFR()

            # Check if Unopened Preflop Raise (UOPFR)
            # No one before has bet or raised, everyone has called or folded
            if self._number_of_raises_pre_flop == 0 \
                and not self._pre_flop_bet \
                and not self._pre_flop_first_action:
                player.uopfr()
                player.optUOPFR()

            # Check if someone already raised (3B)
            if self._number_of_raises_pre_flop == 1:
                player.p3b()
                player.opt3B()
                player.optF3B()

            # Check if two people already raised (4B)
            if self._number_of_raises_pre_flop == 2:
                player.p4b()
                player.opt4B()
                player.optF4B()

            # Increase number of raises in pre-flop
            self._number_of_raises_pre_flop += 1

            # Should be called last
            self._pre_flop_first_action = False

    def playerFolds(self, player_name):
        player = self.getPlayer(player_name)
        player.fold(self._hand_state)

        # Is this before the flop?
        if self._hand_state == HAND_STATE.PRE_FLOP:
            # Check if player folded to a pre-flop raise
            if self._number_of_raises_pre_flop > 0:
                player.optCPFR()

            # Check if opportunity for Unopened Preflop Raise (UOPFR)
            # No one before has bet or raised, everyone has called or folded
            if self._number_of_raises_pre_flop == 0 \
                and not self._pre_flop_bet \
                and not self._pre_flop_first_action:
                player.optUOPFR()

            # Check if someone already raised and opportunity for 3B
            if self._number_of_raises_pre_flop == 1:
                player.f3b()
                player.opt3B()
                player.optF3B()

            # Check if two people already raised and opportunity for 4B
            if self._number_of_raises_pre_flop == 2:
                player.f4b()
                player.opt4B()
                player.optF4B()

            # Should be called last
            self._pre_flop_first_action = False

    def playerChecks(self, player_name):
        player = self.getPlayer(player_name)

        # Is this before the flop?
        if self._hand_state == HAND_STATE.PRE_FLOP:
            # Check if opportunity for Unopened Preflop Raise (UOPFR)
            # No one before has bet or raised, everyone has called or folded
            if self._number_of_raises_pre_flop == 0 \
                and not self._pre_flop_bet \
                and not self._pre_flop_first_action:
                player.optUOPFR()
            
            # Should be called last
            self._pre_flop_first_action = False

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

    def __str__(self):
        output = f'Hand Stats for Table {self._table_name}\n'
        output += f'{self._max_players}-max players and ante {self._ante_value}\n'
        currancy = ''
        if self._real_money:
            currancy = '$'
            output += f'Game is played with real money.\n'
        for player in self._players.values():
            output += f'Seat #{player.seat_at_table}: {player.name} with ({currancy}{player.starting_chips} in chips)\n'
        output += f'Button in seat #{self._button_position}\n'
        output += f'{self._player_who_posted_sb} posted small blind of {self._sb_value}\n'
        output += f'{self._player_who_posted_bb} posted big blind of {self._bb_value}\n'
        
        for player in self._players.values():
            output += f'{player}'

        output += f'Final board: {self.board()}'

        return output


class PlayerStats:
    def __init__(self, name):
        self._name = name
        self._hands_played = 0
        # Flops seen
        self._fs = 0
        self._vpip = 0
        self._pfr = 0
        self._cpfr = Fraction()
        self._uopfr = Fraction()
        self._3b = Fraction()
        self._f3b = Fraction()
        self._4b = Fraction()
        self._f4b = Fraction()

    @property
    def name(self):
        return self._name

    @property
    def hands_played(self):
        return self._hands_played

    def increaseHandsPlayed(self):
        self._hands_played += 1

    @property
    def fs(self):
        return Fraction(self._fs, self._hands_played)

    def increaseFS(self):
        self._fs += 1

    @property
    def vpip(self):
        return Fraction(self._vpip, self._hands_played)

    def increaseVPiP(self):
        self._vpip += 1

    @property
    def pfr(self):
        return Fraction(self._pfr, self._hands_played)

    def increasePFR(self):
        self._pfr += 1

    @property
    def cpfr(self):
        return self._cpfr

    def increaseCPFR(self):
        self._cpfr.numerator += 1

    def increaseOptCPFR(self):
        self._cpfr.denominator += 1

    @property
    def uopfr(self):
        return self._uopfr

    def increaseUOPFR(self):
        self._uopfr.numerator += 1

    def increaseOptUOPFR(self):
        self._uopfr.denominator += 1

    @property
    def p3b(self):
        return self._3b

    def increase3B(self):
        self._3b.numerator += 1

    def increaseOpt3B(self):
        self._3b.denominator += 1

    @property
    def f3b(self):
        return self._f3b

    def increaseF3B(self):
        self._f3b.numerator += 1

    def increaseOptF3B(self):
        self._f3b.denominator += 1

    @property
    def p4b(self):
        return self._4b

    def increase4B(self):
        self._4b.numerator += 1

    def increaseOpt4B(self):
        self._4b.denominator += 1

    @property
    def f4b(self):
        return self._f4b

    def increaseF4B(self):
        self._f4b.numerator += 1

    def increaseOptF4B(self):
        self._f4b.denominator += 1

    def __str__(self):
        output = f'{self.name} / #h {self.hands_played} / fs {self.fs} / VPiP {self.vpip}\n'
        output += f'PFR {self.pfr} / CPFR {self.cpfr} / UOPFR {self.uopfr}\n'
        output += f'3B {self.p3b} / F3B {self.f3b} / 4B {self.p4b} / F4B {self.f4b}'
        return output

class Game:
    def __init__(self):
        self._hands = []
        self._player_stats = {}

    def addHand(self, hand):
        # Add hand to array list for testing and history
        self._hands.append(hand)

        # Update stats
        # Get players in hand
        players = hand.getAllPlayers()
        for player_hand in players:
            # Get player
            player_name = player_hand.name
            player_stats = self.getPlayerStats(player_name)

            # Update stats
            # Increase the number of hands played by 1
            player_stats.increaseHandsPlayed()

            # Has seen flop?
            if player_hand.hasSeenFlop():
                player_stats.increaseFS()

            # VPiP
            if player_hand.hasVPiP():
                player_stats.increaseVPiP()

            # PFR
            if player_hand.hasPFR():
                player_stats.increasePFR()

            # CPFR
            if player_hand.hasCPFR():
                player_stats.increaseCPFR()

            if player_hand.hasOptCPFR():
                player_stats.increaseOptCPFR()

            # UOPFR
            if player_hand.hasUOPFR():
                player_stats.increaseUOPFR()

            if player_hand.hasOptUOPFR():
                player_stats.increaseOptUOPFR()

            # 3B
            if player_hand.has3B():
                player_stats.increase3B()

            if player_hand.hasOpt3B():
                player_stats.increaseOpt3B()

            # F3B
            if player_hand.hasF3B():
                player_stats.increaseF3B()

            if player_hand.hasOptF3B():
                player_stats.increaseOptF3B()

            # 4B
            if player_hand.has4B():
                player_stats.increase4B()

            if player_hand.hasOpt4B():
                player_stats.increaseOpt4B()

            # F4B
            if player_hand.hasF4B():
                player_stats.increaseF4B()

            if player_hand.hasOptF4B():
                player_stats.increaseOptF4B()

    def getPlayerStats(self, player_name):
        # Return player stats if already exists
        if player_name in self._player_stats:
            return self._player_stats[player_name]
        
        # Create new player and add them to player stats dict
        player_stats = PlayerStats(player_name)
        self._player_stats[player_name] = player_stats
        
        return player_stats

    def __str__(self):
        output = f'Game Stats:\n\n'
        for player in self._player_stats.values():
            output += f'{player}\n\n'

        return output

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

                # Update hand
                current_hand.playerCalls(player_name, player_chips, all_in)

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
                current_hand.playerBets(player_name, player_chips)

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
                current_hand.playerRaises(player_name, current_chips, raised_chips)

                # Debug print info
                if debug:
                    print(f"{player_name} raise {chip_currancy}{current_chips} to {chip_currancy}{raised_chips}")

            elif FOLD_PATTERN.match(line):
                # Search string
                results = re.search(FOLD_PATTERN, line)

                # Information found about seat
                player_name = results.group(1)

                # Update hand
                current_hand.playerFolds(player_name)

                # Debug print info
                if debug:
                    print(f"{player_name} folds")

            elif CHECK_PATTERN.match(line):
                # Search string
                results = re.search(CHECK_PATTERN, line)

                # Information found about seat
                player_name = results.group(1)

                # Update hand
                current_hand.playerChecks(player_name)

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
                current_hand.initPreFlop()

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
                current_hand.setFlopCards(card1, card2, card3)

                # Update hand state
                current_hand.initFlop()

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
                current_hand.setTurnCard(card)

                # Update hand state
                current_hand.initTurn()

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
                current_hand.setRiverCard(card)

                # Update hand state
                current_hand.initRiver()

                # Debug print info
                if debug:
                    print(f"Start of River [{card}]")

            # If Showdown
            elif SHOWDOWN_PATTERN.match(line):
                # Update hand state
                current_hand.initShowdown()

                # Debug print info
                if debug:
                    print(f"Start of Showdown")
           
            # If Summary
            elif SUMMARY_PATTERN.match(line):
                # Update hand state
                current_hand.finalizeHand()

                # Save hand to game
                game.addHand(current_hand)

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
