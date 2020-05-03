#!/usr/bin/env python3

'''
This script helps to track players by entering hand information on the fly
'''


from analyze_hands import PlayerHand, assign_stats_from_hand, print_stats


def input_small_blind(game_stats):
    while True:
        sb = input ("Who is the small blind? ")
        if sb not in game_stats['current_players']:
            print(f'{sb} not in players list!')
        else:
            game_stats['current_sb'] = sb
            break

def init_game():
    '''
    The user is prompted to enter all player names (in order that they are sitting)
    and the current small blind player to start the game.
    '''
    game_stats = {}
    current_players = []
    print("Begin by entering all players (in order that they are sitting)")
    while True:
        print(f"All players = {current_players}")        
        player_name = input("please enter in next player name (or D): ")
        if player_name == "D":
            break
        if player_name in current_players:
            print("No duplicate player names!")
            continue
        if player_name == "":
            # we assume a typo
            continue
        current_players.append(player_name)

    game_stats['current_players'] = current_players
    input_small_blind(game_stats)
            
    return game_stats

def pre_hand(game_stats):
    '''
    Let the user remove any players and optionally reset the sb.
    returns a dictionary mapping player names to their PlayerHand objects
    '''
    remove = input("Any players to remove? (any key besides 'y' will contine): ")
    if remove == 'y':
        while True:
            player_name = input("please enter in player name to remove (or D): ")
            if player_name == "D":
                break
            game_stats['current_players'].remove(player_name)
            
    new_sb = input(f"Change small blind from {game_stats['current_sb']}? (any key besides 'y' will contine): ")
    if new_sb == 'y':
        input_small_blind(game_stats)

    players = {}
    for player_name in game_stats['current_players']:
        players[player_name] = PlayerHand(name=player_name)
        
    return players


def input_player_action(player_name):
    while True:
        action = input(f"What does {player_name} do (ca=call, f=fold, r=raise, cc=check, or D): ")
        if action not in {'ca', 'f', 'r', 'cc', 'D'}:
            print("Not a valid action!")
        else:
            break
    return action

def pre_flop(game_stats, players):
    num_raises = 0
    current_players = game_stats['current_players']
    start_index = current_players.index(game_stats['current_sb']) + 2 # add 2 since UTG starts pre_flop

    for index in range(start_index, 100000): # effectively infinite. just watch index++ in loop itself
        
        true_index = index % len(current_players) # want to keep wrapping around the players in a circle
        player_name = current_players[true_index]
        player = players[player_name]
        if player.folded:
            continue

        action = input_player_action(player_name)
        if action == 'D':
            break
        
        elif action == 'ca':
            player.calls_pre_flop(num_raises=num_raises)
            
        elif action == 'r':
            player.raises_pre_flop(num_raises=num_raises)
            num_raises += 1

        elif action == 'f':
            player.folds_pre_flop(num_raises=num_raises)            

def flop(game_stats, players):
    active_c_bet = False
    num_raises = 0
    current_players = game_stats['current_players']
    start_index = current_players.index(game_stats['current_sb'])
        
    for index in range(start_index, 100000): # effectively infinite. just watch index++ in loop itself
        
        true_index = index % len(current_players) # want to keep wrapping around the players in a circle
        player_name = current_players[true_index]
        player = players[player_name]
        if player.folded:
            continue

        action = input_player_action(player_name)
        if action == 'D':
            break

        elif action == 'cc':
            player.checks_flop()

        elif action == 'ca':
            player.calls_flop(active_c_bet=active_c_bet)
            
        elif action == 'r':
            player.raises_flop(num_raises=num_raises, active_c_bet=active_c_bet)
            num_raises += 1
            if player.c_bet:
                active_c_bet = True
            else:
                active_c_bet = False
                
        elif action == 'f':
            player.folds_flop(active_c_bet=active_c_bet)
            

def post_hand(game_stats):
    '''
    Update the small blind
    '''
    current_players = game_stats['current_players']
    current_sb = game_stats['current_sb']
    current_sb_index = current_players.index(current_sb)

    next_index = (current_sb_index + 1) % len(current_players)
    next_sb = current_players[next_index]
    game_stats['current_sb'] = next_sb

def run_hand(game_stats):
    players = pre_hand(game_stats)
    print(f"\nPlayers in hand = {game_stats['current_players']}")
    print("Beginning Hand:")
    pre_flop(game_stats, players)
    print("\nBeginning Flop:")    
    flop(game_stats, players)
    print("\nEnding Hand:")            
    assign_stats_from_hand(game_stats, players)
    post_hand(game_stats)
    return game_stats

if __name__ == "__main__":
    game_stats = init_game()
    while True:
        game_stats = run_hand(game_stats)
        print_stats(game_stats)


