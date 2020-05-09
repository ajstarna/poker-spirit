#!/usr/bin/env python3

'''
This script helps to track players by entering hand information on the fly
'''

from functools import partial

import tkinter as tk
from tkinter import ttk

from analyze_hands import PlayerHand, assign_stats_from_hand, print_stats




class App:

    def __init__(self):
        self.game_stats = {}
        self.current_players = []
        self.phase = "Pre Game"
        
        self.window = tk.Tk()
        self.window.geometry("400x75")        
        self.window.title( "Poker Spirit - Live Tracker")
        
        self.players_var = tk.StringVar()
        self.players_var.set(f"Players = {self.current_players}")

        
    def destroy(self, window):
        window.destroy()
        
    def add_player(self, player_entry):
        player_name = player_entry.get()
        if player_name in self.current_players:
            print("No duplicate player names!")
        elif player_name == "":
            # we assume a typo
            print("empty player name")
        else:
            self.current_players.append(player_name)
        self.players_var.set(f"Players = {self.current_players}")            
        
    def init_game(self):
        '''
        The user is prompted to enter all player names (in order that they are sitting)
        and the current small blind player to start the game.
        '''
        
        game_window = tk.Toplevel(self.window)

        tk.Label(init_window, 
                 textvariable=self.phase).grid(row=1)
        
        
        tk.Label(init_window, 
                 text="Player Name").grid(row=2)
        e1 = ttk.Entry(init_window)   
        e1.grid(row=2, column=1)

        button_select = ttk.Button(init_window,
                                   text="Enter",
                                   command= partial(self.add_player, e1)
        ).grid(row=4, column=0)

        button_quit = ttk.Button(init_window,
                                 text="Done",
                                 command=partial(self.destroy,init_window)
        ).grid(row=4, column=1)
        
        #init_window.mainloop()

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



    def play_game(self):
        '''
        '''
        game_window = tk.Toplevel(self.window)

        tk.Label(init_window,
                 text="Begin by entering all players (in order that they are sitting)").grid(row=0)

        tk.Label(init_window, 
                 textvariable=self.players_var).grid(row=1)
        
        
        tk.Label(init_window, 
                 text="Player Name").grid(row=2)
        e1 = ttk.Entry(init_window)   
        e1.grid(row=2, column=1)

        button_select = ttk.Button(init_window,
                                   text="Enter",
                                   command= partial(self.add_player, e1)
        ).grid(row=4, column=0)

        button_quit = ttk.Button(init_window,
                                 text="Done",
                                 command=partial(self.destroy,init_window)
        ).grid(row=4, column=1)
        
        #init_window.mainloop()

        ''' 
        game_stats['current_players'] = current_players
        input_small_blind(game_stats)
        '''
        
        return
    
    def quit(self):
        self.window.destroy()
            
    def main(self):
        button_select = ttk.Button(self.window,
                                   text="Enter Players",
                                   command=self.init_game,
        ).grid(row=0)

        button_select = ttk.Button(self.window,
                                   text="Start Game",
                                   command=self.play_game,
        ).grid(row=0)
        
        tk.Label(self.window, 
                 textvariable=self.players_var).grid(row=1)
        
        button_quit = ttk.Button(self.window,
                                 text="Quit",
                                 command=self.quit
        ).grid(row=2)

        self.window.mainloop()


app = App()
app.main()



 


