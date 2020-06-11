from hand_state import HAND_STATE
from player_hand import PlayerHand

# A single hand
class Hand:
    def __init__(self):
        self._players = {}

        self._table_name = ''
        self._max_players = 9
        self._button_position = 1

        self._real_money = False
        self._hand_state = HAND_STATE.COMPULSORY_BETS

        self._flop_cards = []
        self._turn_card = None
        self._river_card = None

        self._ante_value = 0
        self._sb_value = 0
        self._bb_value = 0

        self._player_who_posted_sb = ''
        self._player_who_posted_bb = ''
        self._player_who_2_bet = ''
        self._player_who_3_bet = ''
        self._player_who_4_bet = ''

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
    
    def get_player(self, player_name):
        # Return player if already exists
        if player_name in self._players:
            return self._players[player_name]
        
        # Create new player and add them to player dict
        player = PlayerHand(player_name)
        self._players[player_name] = player
        
        return player

    def get_all_players(self):
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
    def using_real_money(self, currancy_format):
        self._real_money = currancy_format

    @property
    def hand_state(self):
        return self._hand_state

    def init_pre_flop(self):
        self._hand_state = HAND_STATE.PRE_FLOP

    def end_pre_flop(self):
        for player in self._players.values():
            # Has folded? If not then they have seen the flop
            if not player.has_folded():
                player.seen_flop()

    def init_flop(self):
        # End Pre-Flop
        self.end_pre_flop()

        # Update state of hand
        self._hand_state = HAND_STATE.FLOP

    def init_turn(self):
        self._hand_state = HAND_STATE.TURN

    def init_river(self):
        self._hand_state = HAND_STATE.RIVER

    def init_showdown(self):
        self._hand_state = HAND_STATE.SHOWDOWN

    def finalize_hand(self):
        self._hand_state = HAND_STATE.END

    def player_calls(self, player_name, amount, all_in = False):
        # Get Player
        player = self.get_player(player_name)
        
        # Update VPiP
        player.vpip()

        # Is this before the flop?
        if self._hand_state == HAND_STATE.PRE_FLOP:
            # Check if player called a pre-flop raise
            if self._number_of_raises_pre_flop > 0:
                player.cpfr()
                player.opt_cpfr()

            # Check if opportunity for Unopened Preflop Raise (UOPFR)
            # No one before has bet or raised, everyone has called or folded
            if self._number_of_raises_pre_flop == 0 \
                and not self._pre_flop_bet \
                and not self._pre_flop_first_action:
                player.opt_uopfr()

            # Check if someone already raised and opportunity for 3B
            if self._number_of_raises_pre_flop == 1:
                player.opt_3b()

            # Fold to someones 3B opportunity
            # You are only considered to have a “fold to 3-bet” opportunity if you made the initial raise
            if self._number_of_raises_pre_flop == 2 and \
                self._player_who_2_bet == player_name:
                player.opt_f3b()

            # Should be called last
            self._pre_flop_first_action = False

    def player_bets(self, player_name, ammount):
         # Get Player
        player = self.get_player(player_name)
        
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
                player.opt_uopfr()

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

    def player_raises(self, player_name, current_ammount, new_ammount):
        # Get Player
        player = self.get_player(player_name)
        
        # Update VPiP
        player.vpip()

        # Is this before the flop?
        if self._hand_state == HAND_STATE.PRE_FLOP:
            # This is a pre-flop raise (pfr)
            player.pfr()

            # Check if player raised to a pre-flop raise
            if self._number_of_raises_pre_flop > 0:
                player.opt_cpfr()

            if self._number_of_raises_pre_flop == 0:
                self._player_who_2_bet = player.name

            # Check if Unopened Preflop Raise (UOPFR)
            # No one before has bet or raised, everyone has called or folded
            if self._number_of_raises_pre_flop == 0 \
                and not self._pre_flop_bet \
                and not self._pre_flop_first_action:
                player.uopfr()
                player.opt_uopfr()

            # Check if someone already raised (3B)
            if self._number_of_raises_pre_flop == 1:
                self._player_who_3_bet = player.name
                player.p3b()
                player.opt_3b()

            # Fold to someones 3B opportunity
            # You are only considered to have a “fold to 3-bet” opportunity if you made the initial raise
            if self._number_of_raises_pre_flop == 2 and \
                self._player_who_2_bet == player_name:
                player.opt_f3b()

            # Increase number of raises in pre-flop
            self._number_of_raises_pre_flop += 1

            # Should be called last
            self._pre_flop_first_action = False

    def player_folds(self, player_name):
        player = self.get_player(player_name)
        player.fold(self._hand_state)

        # Is this before the flop?
        if self._hand_state == HAND_STATE.PRE_FLOP:
            # Check if player folded to a pre-flop raise
            if self._number_of_raises_pre_flop > 0:
                player.opt_cpfr()

            # Check if opportunity for Unopened Preflop Raise (UOPFR)
            # No one before has bet or raised, everyone has called or folded
            if self._number_of_raises_pre_flop == 0 \
                and not self._pre_flop_bet \
                and not self._pre_flop_first_action:
                player.opt_uopfr()

            # Check if someone already raised and opportunity for 3B
            if self._number_of_raises_pre_flop == 1:
                player.opt_3b()

            # Fold to someones 3B
            # You are only considered to have a “fold to 3-bet” opportunity if you made the initial raise
            if self._number_of_raises_pre_flop == 2 and \
                self._player_who_2_bet == player_name:
                player.f3b()
                player.opt_f3b()

            # Should be called last
            self._pre_flop_first_action = False

    def player_checks(self, player_name):
        player = self.get_player(player_name)

        # Is this before the flop?
        if self._hand_state == HAND_STATE.PRE_FLOP:
            # Check if opportunity for Unopened Preflop Raise (UOPFR)
            # No one before has bet or raised, everyone has called or folded
            # This can only happen if everyone calls or folds and it gets
            # back to the big blind and they check
            if self._number_of_raises_pre_flop == 0 \
                and not self._pre_flop_bet \
                and not self._pre_flop_first_action:
                player.opt_uopfr()
            
            # Should be called last
            self._pre_flop_first_action = False

    @property
    def flop_cards(self):
        return self._flop_cards

    def set_flop_cards(self, card1, card2, card3):
        self._flop_cards = [card1, card2, card3]

    @property
    def turn_card(self):
        return self._turn_card

    def set_turn_card(self, card):
        self._turn_card = card

    @property
    def river_card(self):
        return self._river_card

    def set_river_card(self, card):
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
