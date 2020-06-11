from hand_state import HAND_STATE

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

    def set_cards(self, card1, card2):
        self._cards = [card1, card2]

    # True if the chips are in dollars and should have '$' in front
    def using_real_money(self, currancy_format):
        self._real_money = currancy_format

    ## Stats ##

    # Folded
    def has_folded(self):
        return self._folded

    def folded_in_hand_state(self):
        return self._folded_state

    def fold(self, hand_state):
        self._folded = True
        self._folded_state = hand_state

    # Flops Seen (FS)
    def has_seen_flop(self):
        return self._fs

    def seen_flop(self):
        self._fs = True
    
    # Voluntarily Put $ in Pot (VPiP)
    def has_vpip(self):
        return self._vpip

    def vpip(self):
        self._vpip = True
    
    # Preflop Raise (PFR)
    def has_pfr(self):
        return self._pfr

    def pfr(self):
        self._pfr = True

    # Called Preflop Raise (CPFR)
    def has_cpfr(self):
        return self._cpfr
    
    def has_opt_cpfr(self):
        return self._opt_cpfr
    
    def cpfr(self):
        self._cpfr = True

    def opt_cpfr(self):
        self._opt_cpfr = True

    # Unopened Preflop Raise (UOPFR)
    def has_uopfr(self):
        return self._uopfr
    
    def has_opt_uopfr(self):
        return self._opt_uopfr
    
    def uopfr(self):
        self._uopfr = True

    def opt_uopfr(self):
        self._opt_uopfr = True
    
    # Three-bet Pre-flop (3B)
    def has_3b(self):
        return self._3b

    def p3b(self):
        self._3b = True

    # Opt for 3B
    def has_opt_3b(self):
        return self._opt_3b

    def opt_3b(self):
        self._opt_3b = True
    
    # Folded to Three-Bet Preflop (F3B)
    def has_f3b(self):
        return self._f3b

    def f3b(self):
        self._f3b = True

    # Opt to fold 3B
    def has_opt_f3b(self):
        return self._opt_f3b

    def opt_f3b(self):
        self._opt_f3b = True

    # Four-bet Pre-flop (4B)
    def has_4b(self):
        return self._4b

    def p4b(self):
        self._4b = True

    # Opt for 4B
    def has_opt_4b(self):
        return self._opt_4b

    def opt_4b(self):
        self._opt_4b = True

    # Folded to Four-Bet Preflop (F4B)
    def has_f4b(self):
        return self._f4b

    def f4b(self):
        self._f4b = True

    # Opt to fold 4B
    def has_opt_f4b(self):
        return self._opt_f4b

    def opt_f4b(self):
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
            output += f'Player folded in {HAND_STATE.to_string(self._folded_state)}\n'

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