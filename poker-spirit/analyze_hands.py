#!/usr/bin/env python3
'''
This script reads and processes hands written by PokerStars to their text file
'''

import re
from collections import defaultdict, OrderedDict


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

    STAGE_TO_NEXT = {
        'pre-flop': 'flop',
        'flop': 'turn',
        'turn': 'river',
        'river': 'finish-hand'
    }
    
    
    def __init__(self, sb_index=None):
        self.players = {}
        self.player_order = []
        self.stage = 'pre-flop'
        self.sb_index= sb_index
        
        # pre flop stats
        self.num_pre_flop_raises = 0

        # flop stats
        self.num_flop_raises = 0
        self.active_flop_c_bet = False


    def advance_stage(self):
        if self.stage == 'finish-hand':
            print('already over!')
            return
        print(f'advancing from {self.stage}')
        self.stage = self.STAGE_TO_NEXT[self.stage]
        print(f'new stage = {self.stage}')
        
    def add_player(self, player_name):
        self.players[player_name] = PlayerHand(name=player_name)        
        self.player_order.append(player_name)
        
    def get_player(self, player_name):
        return self.players.get(player_name)

            
    def get_next_player(self):
        if self.stage == 'pre-flop':
            start_index = self.sb_index+2 # add 2 since UTG starts pre_flop
        else:
            start_index = self.sb_index
            
        for index in range(start_index, 1000000): # effectively infinite
            true_index = index % len(self.player_order) # want to keep wrapping around the players in a circle
            player_name = self.player_order[true_index]
            player = self.get_player(player_name)
            if player.folded:
                continue
            yield player_name

    '''
    def get_next_default_player(self):
        for index in range(self.sb_index, 100000): # effectively infinite
            true_index = index % len(self.player_order) # want to keep wrapping around the players in a circle
            player_name = self.player_order[true_index]
            player = self.get_player(player_name)
            if player.folded:
                continue
            yield player_name
    '''
    
    def set_sb(self, player_name, sb=1):
        self.players[player_name].sb = sb
        self.sb_index = self.player_order.index(player_name)
        
    def set_bb(self, player_name, bb):
        self.players[player_name].bb = bb                
        

    def player_checks(self, player_name):
        player = self.players[player_name]
        if self.stage == 'pre-flop':
            player.checks_flop()


    def player_raises(self, player_name):
        player = self.players[player_name]
        if self.stage == 'pre-flop':
            player.raises_pre_flop(num_raises=self.num_pre_flop_raises)
            self.num_pre_flop_raises += 1
        elif self.stage == 'flop':
            player.raises_flop(num_raises=self.num_flop_raises, active_c_bet=self.active_flop_c_bet)
            self.num_flop_raises += 1
            if player.c_bet:
                self.active_flop_c_bet = True
            else:
                self.active_flop_c_bet = False

    
    def player_folds(self, player_name):
        player = self.players[player_name]
        if self.stage == 'pre-flop':
            player.folds_pre_flop(num_raises=self.num_pre_flop_raises)
        elif self.stage == 'flop':
            player.folds_flop(active_c_bet=self.active_flop_c_bet)            
    
    def player_calls(self, player_name):
        player = self.players[player_name]        
        if self.stage == 'pre-flop':
            print('pre flop call baby!')
            player.calls_pre_flop(num_raises=self.num_pre_flop_raises)
        elif self.stage == 'flop':        
            player.calls_flop(active_c_bet=self.active_flop_c_bet)
        

def assign_stats_from_hand(game_stats, hand):
    '''
    Looks through hand information, and adds to the stats for each
    corresponding player in game_stats.
    If a player in the hand is not in game_stats, then add them.
    '''

    for player_name, player in hand.players.items():
        if player_name not in game_stats:
            player_stats = defaultdict(int)
            game_stats[player_name] = player_stats
            # for storage, we want the stats dictionary to know the player/game info
            #game_stats[player_name]['player_name'] = player_name
            #game_stats[player_name]['game_id'] = self.game_id
        else:
            player_stats = game_stats[player_name]
            
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

            


class GameIO:

    def __init__(self):
        self.game_stats = {}
        self.game_id = None
        self.current_hand = None        
        self.current_players = []
        self.__current_sb = None 
        self.current_bb = None
        self.hands = []


    def add_player(self, player_name):
        self.current_players.append(player_name)
        if self.current_hand is not None:
            self.current_hand.add_player(player_name)
            
    @property
    def current_sb(self):
        return self.__current_sb

    @current_sb.setter
    def current_sb(self, player_name):    
        #def set_sb(self, player_name):
        if self.current_hand is not None:
            self.current_hand.set_sb(player_name)
        self.__current_sb = player_name
        self.current_sb_index = self.current_players.index(player_name)
        
    def finish_hand(self):
        '''
        Update the blind positions
        '''
        self.current_players = self.current_hand.player_order # for knowing who is still at the table        
        assign_stats_from_hand(self.game_stats, self.current_hand)
        self.hands.append(self.current_hand)
        
    @staticmethod
    def hands_played_str(game_stats, player_name):
        stats = game_stats[player_name]
        hands_played = stats['hands_played']
        return f'Hands played = {hands_played}'

    @staticmethod    
    def vpip_str(game_stats, player_name):
        stats = game_stats[player_name]
        hands_played = stats['hands_played']
        if hands_played > 0:
            return f'VPIP = {stats["vpip"]}/{hands_played} = {round(100*stats["vpip"]/hands_played, 1)}'
        else:
            return f'VPIP = {stats["vpip"]}/{hands_played} = NA'

    @staticmethod        
    def pfr_str(game_stats, player_name):
        stats = game_stats[player_name]
        hands_played = stats['hands_played']
        if hands_played > 0:
            return f'PFR = {stats["pfr"]}/{hands_played} = {round(100*stats["pfr"]/hands_played, 1)}'
        else:
            return f'PFR = {stats["pfr"]}/{hands_played} = NA'

    @staticmethod        
    def _3_bet_str(game_stats, player_name):
        stats = game_stats[player_name]
        if stats['3_bet_opp'] > 0:        
            return f'3-Bet = {stats["3_bet"]}/{stats["3_bet_opp"]} = {round(100*stats["3_bet"]/stats["3_bet_opp"], 1)}'
        else:
            return f'3-Bet = {stats["3_bet"]}/{stats["3_bet_opp"]} = NA'

    @staticmethod
    def _4_bet_str(game_stats, player_name):
        stats = game_stats[player_name]
        if stats['4_bet_opp'] > 0:        
            return f'4-Bet = {stats["4_bet"]}/{stats["4_bet_opp"]} = {round(100*stats["4_bet"]/stats["4_bet_opp"], 1)}'
        else:
            return f'4-Bet = NA'

    @staticmethod        
    def folds_to_3_bet_str(game_stats, player_name):
        stats = game_stats[player_name]        
        if stats['seen_3_bet'] > 0:
            return f'Folds 3-Bet = {stats["folds_to_3_bet"]}/{stats["seen_3_bet"]} = {round(100*stats["folds_to_3_bet"]/stats["seen_3_bet"], 1)}'
        else:
            return f'Folds 3-Bet = NA'
        
    @staticmethod
    def calls_3_bet_str(game_stats, player_name):
        stats = game_stats[player_name]        
        if stats['seen_3_bet'] > 0:
            return f'Calls 3-Bet = {stats["calls_3_bet"]}/{stats["seen_3_bet"]} = {round(100*stats["calls_3_bet"]/stats["seen_3_bet"], 1)}'
        else:
            return f'Calls 3-Bet = NA'
        
    @staticmethod
    def folds_to_c_bet_str(game_stats, player_name):
        stats = game_stats[player_name]        
        if stats['seen_c_bet'] > 0:
            return f'Folds C-Bet = {stats["folds_to_c_bet"]}/{stats["seen_c_bet"]} = {round(100*stats["folds_to_c_bet"]/stats["seen_c_bet"], 1)}'
        else:
            return f'Folds C-Bet = NA'

    @staticmethod        
    def calls_c_bet_str(game_stats, player_name):
        stats = game_stats[player_name]        
        if stats['seen_c_bet'] > 0:
            return f'Calls C-Bet = {stats["calls_c_bet"]}/{stats["seen_c_bet"]} = {round(100*stats["calls_c_bet"]/stats["seen_c_bet"], 1)}'
        else:
            return f'Calls C-Bet = NA'

    @staticmethod        
    def raises_c_bet_str(game_stats, player_name):
        stats = game_stats[player_name]        
        if stats['seen_c_bet'] > 0:
            return f'Raises C-Bet = {stats["raises_c_bet"]}/{stats["seen_c_bet"]} = {round(100*stats["raises_c_bet"]/stats["seen_c_bet"], 1)}'
        else:
            return f'Raises C-Bet = NA'

    @staticmethod        
    def c_bet_str(game_stats, player_name):
        stats = game_stats[player_name]        
        if stats['c_bet_opp'] > 0:
            return f'C-Bet = {stats["c_bet"]}/{stats["c_bet_opp"]} = {round(100*stats["c_bet"]/stats["c_bet_opp"], 1)}'
        else:
            return f'C-Bet = NA'
        
    @staticmethod
    def checks_c_bet_str(game_stats, player_name):
        stats = game_stats[player_name]        
        if stats['c_bet_opp'] > 0:
            return f'Checks C-Bet Opp. = {stats["checks_c_bet_opp"]}/{stats["c_bet_opp"]} = {round(100*stats["checks_c_bet_opp"]/stats["c_bet_opp"], 1)}'
        else:
            return f'Checks C-Bet Opp. = NA'
        
    def print_stats(self):
        for player_name in sorted(self.current_players, key=lambda x: x.lower() ):
            print(f'Player: {player_name}')
            print(GameIO.hands_played_str(self.game_stats, player_name))
            print(GameIO.vpip_str(self.game_stats, player_name))
            print(GameIO.pfr_str(self.game_stats, player_name))
            print(GameIO._3_bet_str(self.game_stats, player_name))
            print(GameIO._4_bet_str(self.game_stats, player_name))            

            print(GameIO.folds_to_3_bet_str(self.game_stats, player_name))
            print(GameIO.calls_3_bet_str(self.game_stats, player_name))

            print(GameIO.folds_to_c_bet_str(self.game_stats, player_name))
            print(GameIO.calls_c_bet_str(self.game_stats, player_name))
            print(GameIO.raises_c_bet_str(self.game_stats, player_name))            

            print(GameIO.c_bet_str(self.game_stats, player_name))
            print(GameIO.checks_c_bet_str(self.game_stats, player_name))
            print()

class LiveGameIO(GameIO):

    def finish_hand(self):
        # in a live game, we need to manage who the blinds are
        super().finish_hand()
        self.current_sb_index = (self.current_sb_index + 1) % len(self.current_players)
        self.current_sb = self.current_players[self.current_sb_index]

        
class PokerStarsGameIO(GameIO):
    
    def __init__(self, path_to_file):
        super().__init__()
        self.path_to_file = path_to_file
        self.game_id = path_to_file.split("/")[-1].split()[0]
        print(f'game id = {self.game_id}')
    
    def set_up_hand(self, hand_lines):
        for i, line in enumerate(hand_lines):
            seat_match = SEAT_PATTERN.match(line)
            if seat_match:
                player_name = seat_match.group(2)
                self.add_player(player_name)
                continue

            small_match = SMALL_PATTERN.match(line)
            if small_match:
                player_name = small_match.group(1)
                sb = small_match.group(2)
                self.current_hand.set_sb(player_name, sb)
                self.current_sb = player_name
                continue

            big_match = BIG_PATTERN.match(line)
            if big_match:
                player_name = big_match.group(1)
                bb = big_match.group(2)
                self.current_hand.set_bb(player_name, bb)
                self.current_bb = player_name
                # once we found the big blind we break
                break
        self.last_set_up_index = i
        # after the big blind is the line "*** HOLE CARDS ***",
        # so we skip past that
        self.pre_flop_index = self.last_set_up_index + 2
    
    def analyze_pre_flop(self, hand_lines):
        for i, line in enumerate(hand_lines[self.pre_flop_index:]):
            flop_match = FLOP_PATTERN.match(line)
            if flop_match:
                break

            call_match = CALL_PATTERN.match(line)
            if call_match:
                player_name = call_match.group(1)
                self.current_hand.player_calls(player_name)
                continue

            raise_match = RAISE_PATTERN.match(line)
            if raise_match:
                player_name = raise_match.group(1)
                self.current_hand.player_raises(player_name)                
                continue

            fold_match = FOLD_PATTERN.match(line)
            if fold_match:
                player_name = fold_match.group(1)
                self.current_hand.player_folds(player_name)
                continue

        self.current_hand.advance_stage()            
        self.flop_index = self.pre_flop_index + i

        
    def analyze_flop(self, hand_lines):
        for i, line in enumerate(hand_lines[self.flop_index:]):
            turn_match = TURN_PATTERN.match(line)
            if turn_match:
                break

            check_match = CHECK_PATTERN.match(line)
            if check_match:
                player_name = check_match.group(1)
                self.current_hand.player_checks(player_name)
                continue

            call_match = CALL_PATTERN.match(line)
            if call_match:
                player_name = call_match.group(1)
                self.current_hand.player_calls(player_name)
                continue
            
            raise_match = RAISE_PATTERN.match(line)
            if raise_match:
                player_name = raise_match.group(1)
                self.current_hand.player_raises(player_name)
                continue

            fold_match = FOLD_PATTERN.match(line)
            if fold_match:
                player_name = fold_match.group(1)
                self.current_hand.player_folds(player_name)
                continue

        self.current_hand.advance_stage()
        self.turn_index = self.flop_index + i
        
    def process_single_hand(self, hand_lines):
        ''' given all the lines of the text file that correspond to a given hand,
        analyze what happens
        '''
        if hand_lines == []:
            return

        self.current_hand = Hand()
        self.set_up_hand(hand_lines)
        self.analyze_pre_flop(hand_lines)
        self.analyze_flop(hand_lines)
        self.finish_hand()
        #self.add_hand(self.current_hand)
        

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
    
    game = PokerStarsGameIO(path_to_file)
    game.run_file()

