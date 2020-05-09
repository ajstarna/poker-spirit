#!/usr/bin/env python3

'''
This script helps to track players by entering hand information on the fly
'''


from analyze_hands import PlayerHand, Game, Hand



def TerminalGame(Game):

    def input_small_blind(self):
        while True:
            sb = input ("Who is the small blind? ")
            if sb not in self.game_stats['current_players']:
                print(f'{sb} not in players list!')
            else:
                self.game_stats['current_sb'] = sb
                break

    def init_game(self):
        '''
        The user is prompted to enter all player names (in order that they are sitting)
        and the current small blind player to start the game.
        '''
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
        self.input_small_blind()


    def pre_hand(self):
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
                self.game_stats['current_players'].remove(player_name)

        new_sb = input(f"Change small blind from {game_stats['current_sb']}? (any key besides 'y' will contine): ")
        if new_sb == 'y':
            self.input_small_blind()

        hand = Hand()
        for player_name in self.game_stats['current_players']:
            hand.players[player_name] = PlayerHand(name=player_name)

        return hand


    def input_player_action(player_name):
        while True:
            action = input(f"What does {player_name} do (ca=call, f=fold, r=raise, cc=check, or D): ")
            if action not in {'ca', 'f', 'r', 'cc', 'D'}:
                print("Not a valid action!")
            else:
                break
        return action

    def pre_flop(self, hand):
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


    def post_hand(self):
        '''
        Update the small blind
        '''
        current_players = self.game_stats['current_players']
        current_sb = self.game_stats['current_sb']
        current_sb_index = current_players.index(current_sb)

        next_index = (current_sb_index + 1) % len(current_players)
        next_sb = current_players[next_index]
        self.game_stats['current_sb'] = next_sb

    def input_hand(self):
        hand = self.pre_hand()
        print(f"\nPlayers in hand = {self.game_stats['current_players']}")
        print("Beginning Hand:")
        self.pre_flop(hand)
        print("\nBeginning Flop:")    
        self.flop(game_stats, players)
        print("\nEnding Hand:")            
        self.assign_stats_from_hand(hand)
        self.post_hand()

if __name__ == "__main__":
    game = TerminalGame()
    game.init_game()
    while True:
        game.input_hand()
        game.print_stats()



