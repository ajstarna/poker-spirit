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
        
    
def set_up_hand(hand_lines, players):
    # print('in set up hand')
    for i, line in enumerate(hand_lines):
        # print(f'line = {line}')
        seat_match = SEAT_PATTERN.match(line)
        if seat_match:
            player_name = seat_match.group(2)
            players[player_name] = PlayerHand(name=player_name)
            continue
        
        small_match = SMALL_PATTERN.match(line)
        if small_match:
            player_name = small_match.group(1)
            sb = small_match.group(2)
            # print(f'small blind player is {player_name} in for {sb}')
            players[player_name].sb = sb
            continue
        
        big_match = BIG_PATTERN.match(line)
        if big_match:
            player_name = big_match.group(1)
            bb = big_match.group(2)            
            # print(f'big blind player is {player_name} in for {bb}')
            players[player_name].bb = bb
            # once we found the big blind we break
            break
    return i

    
def analyze_pre_flop(hand_lines, pre_flop_index, players):
    num_raises = 0 
    for j, line in enumerate(hand_lines[pre_flop_index:]):
        flop_match = FLOP_PATTERN.match(line)
        if flop_match:
            break

        call_match = CALL_PATTERN.match(line)
        if call_match:
            player_name = call_match.group(1)                        
            # print(f'player {player_name} called!')
            player = players[player_name]
            if num_raises == 1:
                player.calls_3_bet_opp = True            
            elif num_raises == 2:
                player.calls_3_bet = True
            player.vpip = True

        raise_match = RAISE_PATTERN.match(line)
        if raise_match:
            player_name = raise_match.group(1)                        
            # print(f'player {player_name} raised!')
            player = players[player_name]
            player.vpip = True
            player.pfr = True
            
            if num_raises == 0:
                player.first_to_raise_pre_flop = player
            elif num_raises == 1:
                # if already a raise, and we raising again, it's a 3 bet
                player._3_bet = True
            elif num_raises == 2:
                player._4_bet = True                
            elif num_raises == 3:
                player._5_bet = True
            elif num_raises == 4:
                player._5_bet = True
            num_raises += 1

        fold_match = FOLD_PATTERN.match(line)
        if fold_match:
            player_name = fold_match.group(1)                        
            # print(f'player {player_name} folds!')
            player = players[player_name]
            player.folded = True            
            if num_raises == 1:
                player.folds_3_bet_opp = True                                
            elif num_raises == 2:
                player.folds_to_3_bet = True                                

    return j
        
def analyze_flop(hand_lines, flop_index, players):
    active_c_bet = False
    num_raises = 0
    
    for i, line in enumerate(hand_lines[flop_index:]):
        turn_match = TURN_PATTERN.match(line)
        if turn_match:
            return i

        check_match = CHECK_PATTERN.match(line)
        if check_match:
            player_name = check_match.group(1)                        
            # print(f'player {player_name} checks!')
            player = players[player_name]            
            if player.pfr:
                player.checks_c_bet_opp = True
        
        call_match = CALL_PATTERN.match(line)
        if call_match:
            player_name = call_match.group(1)                        
            # print(f'player {player_name} called!')
            player = players[player_name]            
            if active_c_bet:
                player.calls_c_bet = True
                # player.seen_c_bet += 1
            

        raise_match = RAISE_PATTERN.match(line)
        if raise_match:
            player_name = raise_match.group(1)
            player = players[player_name]
            if active_c_bet:
                player.raises_c_bet = True
                # player['seen_c_bet'] += 1
            
            # print(f'player {player} raised!')

            if num_raises == 0 and player.pfr:               
                # print('ACTIVE C BET')
                active_c_bet = True
                player.c_bet = True
            else:
                active_c_bet = False
                
            num_raises += 1

        fold_match = FOLD_PATTERN.match(line)
        if fold_match:
            player_name = fold_match.group(1)                        
            # print(f'player {player_name} folds!')
            player = players[player_name]
            player.folded = True            
            if active_c_bet:
                player.folds_to_c_bet = True
                # player.seen_c_bet = True

def process_single_hand(hand_lines, game_stats):
    ''' given all the lines of the text file that correspond to a given hand,
    analyze what happens
    '''
    # print('in process_hand_lines')
    # print(hand_lines)
    if hand_lines is None:
        return

    players = {}
    last_set_up_index = set_up_hand(hand_lines, players)
    
    # after the big blind is the line "*** HOLE CARDS ***",
    # so we skip past that
    pre_flop_index = last_set_up_index + 2

    flop_index = analyze_pre_flop(hand_lines, pre_flop_index, players)

    analyze_flop(hand_lines, flop_index, players)
    assign_stats_from_hand(game_stats, players)
    

def assign_stats_from_hand(game_stats, players):
    '''
    Looks through current hand information from players, and adds to the stats for each
    corresponding player in game_stats
    '''
    game_stats['current_players']  = list(players.keys()) # for knowing who is still at the table
    
    for player_name, player in players.items():
        if player_name not in game_stats:
            game_stats[player_name] = defaultdict(int)
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

            
            
def print_stats(game_stats):
    for player in sorted(game_stats['current_players'], key=lambda x: x.lower() ):
        stats = game_stats[player]
        
        print(f'Player: {player}')
        print(f'Hands played = {stats["hands_played"]}')
        
        print(f'VPIP = {round(100*stats["vpip"]/stats["hands_played"], 1)}')
        print(f'PFR = {round(100*stats["pfr"]/stats["hands_played"], 1)}')

        if stats['3_bet_opp'] > 0:        
            print(f'3-Bet = {round(100*stats["3_bet"]/stats["3_bet_opp"], 1)}')
            
        print(f'4-Bet = {round(100*stats["4_bet"]/stats["hands_played"], 1)}')
        
        if stats['seen_3_bet'] > 0:
            print(f'Folds to 3-Bet = {round(100*stats["folds_to_3_bet"]/stats["seen_3_bet"], 1)}')
            print(f'Calls 3-Bet = {round(100*stats["calls_3_bet"]/stats["seen_3_bet"], 1)}')

        if stats['seen_c_bet'] > 0:
            print(f'Folds to C-Bet = {round(100*stats["folds_to_c_bet"]/stats["seen_c_bet"], 1)}')
            print(f'Calls C-Bet = {round(100*stats["calls_c_bet"]/stats["seen_c_bet"], 1)}')
            print(f'Raises C-Bet = {round(100*stats["raises_c_bet"]/stats["seen_c_bet"], 1)}')                    

        if stats['c_bet_opp'] > 0:
            print(f'C-Bets = {round(100*stats["c_bet"]/stats["c_bet_opp"], 1)}')
            print(f'Checks C-Bet Opportunity = {round(100*stats["checks_c_bet_opp"]/stats["c_bet_opp"], 1)}')
            
        print()
        
def run_file(path_to_file):
    print(f"opening file = {path_to_file}")
    game_stats = {}
    with open(path_to_file, 'r') as file:
        lines = file.read().split('\n')
        print(len(lines))
        hand_lines = None

        for line in lines:
            hand_match = HAND_START_PATTERN.match(line)
            if hand_match:
                # print(f'match on line: {line}')
                # print(f'group: {hand_match.group(0)}')
                process_single_hand(hand_lines, game_stats)
                hand_lines = []
                
            if hand_lines is not None:
                hand_lines.append(line)

    print("DONE RUN FILE")
    return game_stats

if __name__ == "__main__":
    game_stats = run_file(PATH_TO_FILE)
    print_stats(game_stats)
