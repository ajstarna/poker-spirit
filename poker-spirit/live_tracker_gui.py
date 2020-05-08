#!/usr/bin/env python3

'''
This script helps to track players by entering hand information on the fly
'''

from functools import partial

import tkinter as tk
from tkinter import ttk

from analyze_hands import PlayerHand, assign_stats_from_hand, print_stats




class App:

    '''
    def input_small_blind(game_stats):
        while True:
            sb = input ("Who is the small blind? ")
            if sb not in game_stats['current_players']:
                print(f'{sb} not in players list!')
            else:
                game_stats['current_sb'] = sb
                break
    '''

    def destroy(self, window):
        window.destroy()
        
    def add_player(self, player_entry, var):
        player_name = player_entry.get()
        if player_name in self.current_players:
            print("No duplicate player names!")
        elif player_name == "":
            # we assume a typo
            print("empty player name")
        else:
            self.current_players.append(player_name)
        var.set(f"Begin by entering all players (in order that they are sitting)\nPlayers = {self.current_players}")            
        
    def init_game(self):
        '''
        The user is prompted to enter all player names (in order that they are sitting)
        and the current small blind player to start the game.
        '''
        self.game_stats = {}
        self.current_players = []

        init_window = tk.Toplevel(self.window)
        #init_window.geometry("165x60")
        #init_window.title("Game Setup")

        var = tk.StringVar()
        var.set(f"Begin by entering all players (in order that they are sitting)\nPlayers = {self.current_players}")
        
        tk.Label(init_window, 
                 textvariable=var).grid(row=0)
        
        
        tk.Label(init_window, 
                 text="Player Name").grid(row=2)
        e1 = ttk.Entry(init_window)   
        e1.grid(row=2, column=1)

        button_select = ttk.Button(init_window,
                                   text="Enter",
                                   command= partial(self.add_player, e1, var)
        ).grid(row=4, column=0)

        button_quit = ttk.Button(init_window,
                                 text="Done",
                                 command=partial(self.destroy,init_window)
        ).grid(row=4, column=1)
        
        print('blah4')                
        #init_window.mainloop()

        print('blah5')
        ''' 
        game_stats['current_players'] = current_players
        input_small_blind(game_stats)
        '''
        
        return


    '''
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
    '''

    def quit(self):
        self.window.destroy()
        #for window in self.player_windows.values():
        #    window.destroy()
            
    def main(self):
        self.window = tk.Tk()
        self.window.geometry("575x100")
        
        self.window.title( "Poker Spirit - Live Tracker")

        button_select = ttk.Button(self.window,
                                   text="Start",
                                   command=self.init_game,
        ).pack()

        button_quit = ttk.Button(self.window,
                                 text="Quit",
                                 command=self.quit
        ).pack()

        self.window.mainloop()


app = App()
app.main()



 


