#!/usr/bin/env python3

'''
This script helps to track players by entering hand information on the fly
'''


from analyze_hands import PlayerHand, LiveGame, Hand



class TerminalGame(LiveGame):

    def run(self):
        self.init_game()
        while True:
            self.input_hand()
            self.print_stats()
        
    def input_small_blind(self):
        while True:
            sb = input ("Who is the small blind? ")
            if sb not in self.current_players:
                print(f'{sb} not in players list!')
            else:
                self.set_sb(sb)
                break

    def init_game(self):
        '''
        The user is prompted to enter all player names (in order that they are sitting)
        and the current small blind player to start the game.
        '''
        print("Begin by entering all players (in order that they are sitting)")
        while True:
            print(f"All players = {self.current_players}")        
            player_name = input("please enter in next player name (or D): ")
            if player_name == "D":
                break
            if player_name in self.current_players:
                print("No duplicate player names!")
                continue
            if player_name == "":
                # we assume a typo
                continue
            self.current_players.append(player_name)
        self.input_small_blind()


    def pre_hand(self):
        '''
        Let the user remove any players and optionally reset the sb.
        returns a dictionary mapping player names to their PlayerHand objects
        '''
        hand = Hand()        
        remove = input("Any players to remove? (any key besides 'y' will contine): ")
        if remove == 'y':
            while True:
                player_name = input("please enter in player name to remove (or D): ")
                if player_name == "D":
                    break
                self.current_players.remove(player_name)

        for player_name in self.current_players:
            hand.add_player(player_name)
                
        new_sb = input(f"Change small blind from {self.current_sb}? (any key besides 'y' will contine): ")
        if new_sb == 'y':
            self.input_small_blind()
        hand.set_sb(self.current_sb)
        return hand


    def input_player_action(self, player_name):
        while True:
            action = input(f"What does {player_name} do (ca=call, f=fold, r=raise, cc=check, or D): ")
            if action not in {'ca', 'f', 'r', 'cc', 'D'}:
                print("Not a valid action!")
            else:
                break
        return action


    def run_stage(self):
        for player_name in self.current_hand.get_next_player():
            action = self.input_player_action(player_name)
            if action == 'D':
                break
            
            elif action == 'cc':
                hand.player_checks(player_name)
                
            elif action == 'ca':
                hand.player_calls(player_name)

            elif action == 'r':
                hand.player_raises(player_name)

            elif action == 'f':
                hand.player_folds(player_name)
        hand.advance_stage()


    '''
    def pre_flop(self, hand):

        for player_name in hand.get_next_pre_flop_player():
            action = self.input_player_action(player_name)
            if action == 'D':
                break

            elif action == 'ca':
                hand.player_calls_pre_flop(player_name)

            elif action == 'r':
                hand.player_raises_pre_flop(player_name)

            elif action == 'f':
                hand.player_folds_pre_flop(player_name)

    def flop(self, hand):
        for player_name in hand.get_next_default_player():
            action = self.input_player_action(player_name)
            if action == 'D':
                break
            elif action == 'cc':
                hand.player_checks_flop(player_name)
            
            elif action == 'ca':
                hand.player_calls_flop(player_name)

            elif action == 'r':
                hand.player_raises_flop(player_name)

            elif action == 'f':
                hand.player_folds_flop(player_name)
    '''

    def input_hand(self):
        self.current_hand = self.pre_hand()
        print(f"\nPlayers in hand = {self.current_players}")
        print("Beginning Hand:")
        self.run_stage()
        print("\nBeginning Flop:")
        self.run_stage()
        print("\nEnding Hand:")
        self.finish_hand()

if __name__ == "__main__":
    game = TerminalGame()
    game.run()



