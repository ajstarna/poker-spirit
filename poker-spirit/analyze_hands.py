#!/usr/bin/env python3
'''
This script reads and processes hands written by PokerStars to their text file
'''

import re
from collections import defaultdict


CASH_GAME = True
HAND_START_PATTERN = re.compile("PokerStars.*Hand #(\d+)")
if CASH_GAME:
    MONEY = ".+"
else:
    MONEY = "/w+"
    
SEAT_PATTERN = re.compile(f"Seat (\d): (.+) \(({MONEY}) in chips\)")

SMALL_PATTERN = re.compile(f"(.+): posts small blind ({MONEY})")
BIG_PATTERN = re.compile(f"(.+): posts big blind ({MONEY})")

FLOP_PATTERN = re.compile(f"\*\*\* FLOP \*\*\* \[(\w+) (\w+) (\w+)\]")

CALL_PATTERN = re.compile(f"(.+): calls ({MONEY})")
RAISE_PATTERN = re.compile(f"(.+): raises ({MONEY}) to ({MONEY})")
FOLD_PATTERN = re.compile(f"(.+): folds")
CHECK_PATTERN = re.compile(f"(.+): checks")

TURN_PATTERN = re.compile(f"\*\*\* TURN \*\*\* \[(\w+) (\w+) (\w+)\] \[(\w+)\]")


class PlayerHand:
    __slots__ = 'name', 'sb', 'bb', 'folded', \
        'vpip', 'pfr', 'first_to_raise_pre_flop', \
        '_3_bet', 'calls_3_bet_opp', 'folds_3_bet_opp', \
        '_4_bet', '_5_bet', \
        'folds_to_3_bet', 'calls_3_bet', \
        'c_bet', 'checks_c_bet_opp',  \
        'folds_to_c_bet', 'calls_c_bet', 'raises_c_bet', \
    
    def __init__(self, name):
        self.name = name
        self.sb = None
        self.bb = None
        self.folded = False
        self.vpip = False
        self.pfr = False
        self.first_to_raise_pre_flop = False
        self._3_bet = False
        self.calls_3_bet_opp = False
        self.folds_3_bet_opp = False                
        self._4_bet = False
        self._5_bet = False
        self.folds_to_3_bet = False
        self.calls_3_bet = False        
        self.c_bet = False
        self.checks_c_bet_opp = False
        self.folds_to_c_bet = False
        self.calls_c_bet = False
        self.raises_c_bet = False

    def calls_pre_flop(self, num_raises):
        if num_raises == 1:
            self.calls_3_bet_opp = True            
        elif num_raises == 2:
            self.calls_3_bet = True
        self.vpip = True
        
    def raises_pre_flop(self, num_raises):
        self.vpip = True
        self.pfr = True            
        if num_raises == 0:
            self.first_to_raise_pre_flop = True
        elif num_raises == 1:
            # if already a raise, and we raising again, it's a 3 bet
            self._3_bet = True
        elif num_raises == 2:
            self._4_bet = True                
        elif num_raises == 3:
            self._5_bet = True
        elif num_raises == 4:
            self._5_bet = True

    def folds_pre_flop(self, num_raises):
        self.folded = True
        if num_raises == 1:
            self.folds_3_bet_opp = True                                
        elif num_raises == 2:
            self.folds_to_3_bet = True                                
            
    def checks_flop(self):
        if self.pfr:
            self.checks_c_bet_opp = True

    def calls_flop(self, active_c_bet:bool):
        if active_c_bet:
            self.calls_c_bet = True
        
    def raises_flop(self, num_raises, active_c_bet:bool):
        if active_c_bet:
            self.raises_c_bet = True
        if num_raises == 0 and self.pfr:               
            self.c_bet = True

    def folds_flop(self, active_c_bet:bool):
        self.folded = True            
        if active_c_bet:
            self.folds_to_c_bet = True



class Hand:            
    def __init__(self):
        self.players = {}

        # pre flop stats
        self.num_pre_flop_raises = 0

        # flop stats
        self.num_flop_raises = 0
        self.active_flop_c_bet = False


    def add_player(self, player_name):
        self.players[player_name] = PlayerHand(name=player_name)        

    def set_sb(self, player_name, sb):
        self.players[player_name].sb = sb
        
    def set_bb(self, player_name, bb):
        self.players[player_name].bb = bb                
        
    def player_calls_pre_flop(self, player_name):
        player = self.players[player_name]
        player.calls_pre_flop(num_raises=self.num_pre_flop_raises)

    def player_raises_pre_flop(self, player_name):
        player = self.players[player_name]
        player.raises_pre_flop(num_raises=self.num_pre_flop_raises)
        self.num_pre_flop_raises += 1

    def player_folds_pre_flop(self, player_name):
        player = self.players[player_name]
        player.folds_pre_flop(num_raises=self.num_pre_flop_raises)
        
    def player_checks_flop(self, player_name):
        player = self.players[player_name]
        player.checks_flop()

    def player_calls_flop(self, player_name):
        player = self.players[player_name]
        player.calls_flop(active_c_bet=self.active_flop_c_bet)

    def player_raises_flop(self, player_name):
        player = self.players[player_name]
        player.raises_flop(num_raises=self.num_flop_raises, active_c_bet=self.active_flop_c_bet)
        self.num_flop_raises += 1
        if player.c_bet:
            self.active_flop_c_bet = True
        else:
            self.active_flop_c_bet = False

    def player_folds_flop(self, player_name):
        player = self.players[player_name]
        player.folds_flop(active_c_bet=self.active_flop_c_bet)
        

class Game:
    def __init__(self):
        self.game_stats = {}
        self.hands = []

    def add_hand(self, hand):
        self.hands.append(hand)
        self.assign_stats_from_hand(hand)

    def assign_stats_from_hand(self, hand):
        '''
        Looks through current hand information, and adds to the stats for each
        corresponding player in game_stats
        '''
        players = hand.players
        self.game_stats['current_players']  = list(players.keys()) # for knowing who is still at the table

        for player_name, player in players.items():
            if player_name not in self.game_stats:
                self.game_stats[player_name] = defaultdict(int)
            player_stats = self.game_stats[player_name]
            player_stats['hands_played'] += 1
            if player.vpip:
                player_stats['vpip'] += 1
            if player.pfr:
                player_stats['pfr'] += 1

            if player._3_bet:
                player_stats['3_bet'] += 1
                player_stats['3_bet_opp'] += 1            
            if player.folds_3_bet_opp:
                player_stats['folds_3_bet_opp'] += 1            
                player_stats['3_bet_opp'] += 1
            if player.calls_3_bet_opp:
                player_stats['calls_3_bet_opp'] += 1            
                player_stats['3_bet_opp'] += 1

            if player._5_bet:
                player_stats['5_bet'] += 1

            if player.folds_to_3_bet:
                player_stats['folds_to_3_bet'] += 1
                player_stats['seen_3_bet'] += 1            
            elif player.calls_3_bet:
                player_stats['calls_3_bet'] += 1
                player_stats['seen_3_bet'] += 1            
            elif player._4_bet:
                player_stats['4_bet'] += 1
                player_stats['seen_3_bet'] += 1            

            if player.c_bet:
                player_stats['c_bet'] += 1
                player_stats['c_bet_opp'] += 1            
            elif player.checks_c_bet_opp:
                player_stats['checks_c_bet_opp'] += 1
                player_stats['c_bet_opp'] += 1

            if player.folds_to_c_bet:
                player_stats['folds_to_c_bet'] += 1
                player_stats['seen_c_bet'] += 1            
            elif player.calls_c_bet:
                player_stats['calls_c_bet'] += 1
                player_stats['seen_c_bet'] += 1            
            elif player.raises_c_bet:
                player_stats['raises_c_bet'] += 1
                player_stats['seen_c_bet'] += 1            

    def hands_played_str(self, player_name):
        stats = self.game_stats[player_name]
        hands_played = stats['hands_played']
        return f'Hands played = {hands_played}'

    def vpip_str(self, player_name):
        stats = self.game_stats[player_name]
        hands_played = stats['hands_played']
        if hands_played > 0:
            return f'VPIP = {stats["vpip"]}/{hands_played} = {round(100*stats["vpip"]/hands_played, 1)}'
        else:
            return f'VPIP = {stats["vpip"]}/{hands_played} = NA'

    def pfr_str(self, player_name):
        stats = self.game_stats[player_name]
        hands_played = stats['hands_played']
        if hands_played > 0:
            return f'PFR = {stats["pfr"]}/{hands_played} = {round(100*stats["pfr"]/hands_played, 1)}'
        else:
            return f'PFR = {stats["pfr"]}/{hands_played} = NA'

    def _3_bet_str(self, player_name):
        stats = self.game_stats[player_name]
        if stats['3_bet_opp'] > 0:        
            return f'3-Bet = {stats["3_bet"]}/{stats["3_bet_opp"]} = {round(100*stats["3_bet"]/stats["3_bet_opp"], 1)}'
        else:
            return f'3-Bet = {stats["3_bet"]}/{stats["3_bet_opp"]} = NA'
        
    def _4_bet_str(self, player_name):
        stats = self.game_stats[player_name]
        if stats['4_bet_opp'] > 0:        
            return f'4-Bet = {stats["3_bet"]}/{stats["4_bet_opp"]} = {round(100*stats["4_bet"]/stats["4_bet_opp"], 1)}'
        else:
            return f'4-Bet = NA'

    def folds_to_3_bet_str(self, player_name):
        stats = self.game_stats[player_name]        
        if stats['seen_3_bet'] > 0:
            return f'Folds to 3-Bet = {stats["folds_to_3_bet"]}/{stats["seen_3_bet"]} = {round(100*stats["folds_to_3_bet"]/stats["seen_3_bet"], 1)}'
        else:
            return f'Folds to 3-Bet = NA'

    def calls_3_bet_str(self, player_name):
        stats = self.game_stats[player_name]        
        if stats['seen_3_bet'] > 0:
            return f'Calls 3-Bet = {stats["calls_3_bet"]}/{stats["seen_3_bet"]} = {round(100*stats["calls_3_bet"]/stats["seen_3_bet"], 1)}'
        else:
            return f'Calls 3-Bet = NA'

    def folds_to_c_bet_str(self, player_name):
        stats = self.game_stats[player_name]        
        if stats['seen_c_bet'] > 0:
            return f'Folds to c-Bet = {stats["folds_to_c_bet"]}/{stats["seen_c_bet"]} = {round(100*stats["folds_to_c_bet"]/stats["seen_c_bet"], 1)}'
        else:
            return f'Folds to c-Bet = NA'

    def calls_c_bet_str(self, player_name):
        stats = self.game_stats[player_name]        
        if stats['seen_c_bet'] > 0:
            return f'Calls c-Bet = {stats["calls_c_bet"]}/{stats["seen_c_bet"]} = {round(100*stats["calls_c_bet"]/stats["seen_c_bet"], 1)}'
        else:
            return f'Calls c-Bet = NA'

    def raises_c_bet_str(self, player_name):
        stats = self.game_stats[player_name]        
        if stats['seen_c_bet'] > 0:
            return f'Raises c-Bet = {stats["raises_c_bet"]}/{stats["seen_c_bet"]} = {round(100*stats["raises_c_bet"]/stats["seen_c_bet"], 1)}'
        else:
            return f'Raises c-Bet = NA'

    def c_bet_str(self, player_name):
        stats = self.game_stats[player_name]        
        if stats['c_bet_opp'] > 0:
            return f'C-Bets = {stats["c_bet"]}/{stats["c_bet_opp"]} = {round(100*stats["c_bet"]/stats["c_bet_opp"], 1)}'
        else:
            return f'C-Bets = NA'

    def checks_c_bet_str(self, player_name):
        stats = self.game_stats[player_name]        
        if stats['c_bet_opp'] > 0:
            return f'Checks C-Bet Opp. = {stats["checks_c_bet_opp"]}/{stats["c_bet_opp"]} = {round(100*stats["checks_c_bet_opp"]/stats["c_bet_opp"], 1)}'
        else:
            return f'Checks C-Bet Opp. = NA'
        
    def print_stats(self):
        for player_name in sorted(self.game_stats['current_players'], key=lambda x: x.lower() ):
            print(f'Player: {player_name}')
            print(self.hands_played_str(player_name))
            print(self.vpip_str(player_name))
            print(self.pfr_str(player_name))
            print(self._3_bet_str(player_name))
            print(self._4_bet_str(player_name))            

            print(self.folds_to_3_bet_str(player_name))
            print(self.calls_3_bet_str(player_name))

            print(self.folds_to_c_bet_str(player_name))
            print(self.calls_c_bet_str(player_name))
            print(self.raises_c_bet_str(player_name))            

            print(self.c_bet_str(player_name))
            print(self.checks_c_bet_str(player_name))
            print()

        
class FileGame(Game):
    
    def __init__(self, path_to_file):
        super().__init__()
        self.path_to_file = path_to_file

    
    def set_up_hand(self, hand_lines, hand):
        for i, line in enumerate(hand_lines):
            seat_match = SEAT_PATTERN.match(line)
            if seat_match:
                player_name = seat_match.group(2)
                hand.add_player(player_name)
                continue

            small_match = SMALL_PATTERN.match(line)
            if small_match:
                player_name = small_match.group(1)
                sb = small_match.group(2)
                hand.set_sb(player_name, sb)
                continue

            big_match = BIG_PATTERN.match(line)
            if big_match:
                player_name = big_match.group(1)
                bb = big_match.group(2)
                hand.set_bb(player_name, bb)                
                # once we found the big blind we break
                break
        self.last_set_up_index = i
        # after the big blind is the line "*** HOLE CARDS ***",
        # so we skip past that
        self.pre_flop_index = self.last_set_up_index + 2
    
    def analyze_pre_flop(self, hand_lines, hand):
        for i, line in enumerate(hand_lines[self.pre_flop_index:]):
            flop_match = FLOP_PATTERN.match(line)
            if flop_match:
                break

            call_match = CALL_PATTERN.match(line)
            if call_match:
                player_name = call_match.group(1)
                hand.player_calls_pre_flop(player_name)
                continue

            raise_match = RAISE_PATTERN.match(line)
            if raise_match:
                player_name = raise_match.group(1)
                hand.player_raises_pre_flop(player_name)                
                continue

            fold_match = FOLD_PATTERN.match(line)
            if fold_match:
                player_name = fold_match.group(1)
                hand.player_folds_pre_flop(player_name)
                continue

        self.flop_index = self.pre_flop_index + i

        
    def analyze_flop(self, hand_lines, hand):
        for i, line in enumerate(hand_lines[self.flop_index:]):
            turn_match = TURN_PATTERN.match(line)
            if turn_match:
                break

            check_match = CHECK_PATTERN.match(line)
            if check_match:
                player_name = check_match.group(1)
                hand.player_checks_flop(player_name)
                continue

            call_match = CALL_PATTERN.match(line)
            if call_match:
                player_name = call_match.group(1)
                hand.player_calls_flop(player_name)
                continue
            
            raise_match = RAISE_PATTERN.match(line)
            if raise_match:
                player_name = raise_match.group(1)
                hand.player_raises_flop(player_name)
                continue

            fold_match = FOLD_PATTERN.match(line)
            if fold_match:
                player_name = fold_match.group(1)
                hand.player_folds_flop(player_name)
                continue
            
        self.turn_index = self.flop_index + i
        
    def process_single_hand(self, hand_lines):
        ''' given all the lines of the text file that correspond to a given hand,
        analyze what happens
        '''
        if hand_lines == []:
            return

        hand = Hand()
        self.set_up_hand(hand_lines, hand)
        self.analyze_pre_flop(hand_lines, hand)
        self.analyze_flop(hand_lines, hand)
        self.add_hand(hand)
        

    def run_file(self):
        print(f"opening file = {self.path_to_file}")
        with open(self.path_to_file, 'r') as file:
            lines = file.read().split('\n')
            start_index = 0
            end_index = 0
            for line in lines:
                end_index += 1
                hand_match = HAND_START_PATTERN.match(line)
                if hand_match:
                    hand_lines = lines[start_index: end_index]
                    self.process_single_hand(hand_lines)
                    start_index = end_index

        self.print_stats()        

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()
    # get env vars from .env file
    path_to_file = os.getenv("PATH_TO_FILE", ".")
    
    game = FileGame(path_to_file)
    game.run_file()

