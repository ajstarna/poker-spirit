#!/usr/bin/env python3

'''
This script helps to track players by entering hand information on the fly
'''

from functools import partial

import tkinter as tk
from tkinter import ttk

#from analyze_hands import PlayerHand, assign_stats_from_hand, print_stats
from analyze_hands import Game




class GuiGame(Game):

    def __init__(self):
        super().__init__()
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
        
    def enter_players(self):
        '''
        The user is prompted to enter all player names (in order that they are sitting)
        and the current small blind player to start the game.
        '''
        
        player_window = tk.Toplevel(self.window)
        player_window.title( "Poker Spirit - Player Entry")
        tk.Label(player_window, 
                 textvariable=self.players_var).grid(row=1)
        
        
        tk.Label(player_window, 
                 text="Player Name").grid(row=2)
        e1 = ttk.Entry(player_window)   
        e1.grid(row=2, column=1)

        button_select = ttk.Button(player_window,
                                   text="Enter",
                                   command= partial(self.add_player, e1)
        ).grid(row=4, column=0)

        button_quit = ttk.Button(player_window,
                                 text="Done",
                                 command=partial(self.destroy,player_window)
        ).grid(row=4, column=1)


    def play_game(self):
        '''
        '''
        hand = Hand()
        
        game_window = tk.Toplevel(self.window)

        self.phase_var = tk.StringVar()
        self.phase_var.set(f"{hand.stage}")
        tk.Label(game_window,
                 textvariable=self.phase_var).grid(row=0)


        self.player_name_iter = iter(hand.get_next_pre_flop_player())
        
        self.current_player_name = next(self.player_name_iter)
        self.current_player_var = tk.StringVar()
        self.current_player_var.set(f"{self.current_player_name}")
        tk.Label(init_window, 
                 textvariable=self.current_player_var).grid(row=1)
        
    
        button_select = ttk.Button(init_window,
                                   text="Call",
                                   command=player_calls
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
                                   command=self.enter_players,
        ).grid(row=0)

        button_select = ttk.Button(self.window,
                                   text="Start Game",
                                   command=self.play_game,
        ).grid(row=0, column=1)
        
        tk.Label(self.window, 
                 textvariable=self.players_var).grid(row=1)
        
        button_quit = ttk.Button(self.window,
                                 text="Quit",
                                 command=self.quit
        ).grid(row=0, column=2)

        self.window.mainloop()


app = App()
app.main()



 


