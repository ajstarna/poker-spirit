#!/usr/bin/env python3

'''
This script helps to track players by entering hand information on the fly
'''

from functools import partial

import tkinter as tk
from tkinter import ttk

#from analyze_hands import PlayerHand, assign_stats_from_hand, print_stats
from analyze_hands import Game, Hand




class GuiGame(Game):

    def __init__(self):
        super().__init__()
        self.window = tk.Tk()
        self.window.geometry("500x75")        
        self.window.title( "Poker Spirit - Live Tracker")
        
        self.players_var = tk.StringVar()
        self.players_var.set(f"Players = {self.current_players}")

        self.small_blind_var = tk.StringVar()
        self.small_blind_var.set(f"Small blind = {self.current_sb}")
        
        
    def destroy(self, window):
        window.destroy()
        
    def add_player(self, player_entry):
        player_name = player_entry.get()
        player_entry.delete(0, tk.END) # clear what is there        
        if player_name in self.current_players:
            print("No duplicate player names!")
        elif player_name == "":
            # we assume a typo
            print("empty player name")
        else:
            self.current_players.append(player_name)
        self.players_var.set(f"Players = {self.current_players}")            

    def set_small_blind(self, player_entry):
        player_name = player_entry.get()
        player_entry.delete(0, tk.END) # clear what is there        
        if player_name not in self.current_players:
            print("Must be a name of a current player!")
        else:
            self.set_sb(player_name)
        self.small_blind_var.set(f"Small blind = {self.current_sb}")            
        
        
    def enter_players(self):
        '''
        The user is prompted to enter all player names (in order that they are sitting)
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

    def enter_small_blind(self):
        '''
        The user is prompted to enter who is the small blind
        '''
        
        small_blind_window = tk.Toplevel(self.window)
        small_blind_window.title( "Poker Spirit - Blind Entry")
        tk.Label(small_blind_window, 
                 textvariable=self.small_blind_var).grid(row=1)
        
        
        tk.Label(small_blind_window, 
                 text="Small Blind").grid(row=2)
        e1 = ttk.Entry(small_blind_window)   
        e1.grid(row=2, column=1)

        button_select = ttk.Button(small_blind_window,
                                   text="Enter",
                                   command= partial(self.set_small_blind, e1)
        ).grid(row=4, column=0)

        button_quit = ttk.Button(small_blind_window,
                                 text="Done",
                                 command=partial(self.destroy, small_blind_window)
        ).grid(row=4, column=1)



    def init_hand(self):
        hand = Hand()
        for player_name in self.current_players:
            hand.add_player(player_name)
        hand.set_sb(self.current_sb)            
        return hand


    def end_hand(self, game_window):
        self.finish_hand()
        self.print_stats()
        game_window.destroy()

    def player_calls(self, player_name_var):
        print(f'{player_name_var.get()} calls')
        self.current_hand.player_calls(player_name_var.get())
        self.update_current_player()
        print(f'new player name = {self.current_player_name}')
        
    def player_folds(self, player_name_var):
        self.current_hand.player_folds (player_name_var.get())
        self.update_current_player()        
        
    def player_checks(self, player_name_var):
        self.current_hand.player_checks(player_name_var.get())
        self.update_current_player()        
        
    def player_raises(self, player_name_var):
        self.current_hand.player_raises(player_name_var.get())
        self.update_current_player()        

    def update_current_player(self):
        '''
        we need to get the next player, and then make sure to update the string var,
        since that is passed into the button press commands
        '''
        self.current_player_name = next(self.player_name_iter)        
        self.current_player_var.set(self.current_player_name)


    def advance_stage(self):
        self.current_hand.advance_stage()
        self.phase_var.set(f"{self.current_hand.stage}")
        
    def play_game(self):
        '''
        '''
        game_window = tk.Toplevel(self.window)
        self.current_hand = self.init_hand()
        self.phase_var = tk.StringVar()
        self.phase_var.set(f"{self.current_hand.stage}")
        tk.Label(game_window,
                 textvariable=self.phase_var).grid(row=0)
        tk.Label(game_window,
                 text=f'Hand Number = {len(self.hands) + 1}').grid(row=0, column=1)

        self.player_name_iter = iter(self.current_hand.get_next_player())
        self.current_player_var = tk.StringVar() # need the var to be mutable as we pass it around


        self.update_current_player()
        
        tk.Label(game_window, 
                 textvariable=self.current_player_var).grid(row=1, column=0, columnspan=3)
        

        button_select = ttk.Button(game_window,
                                   text="Fold",
                                   command=partial(self.player_folds, self.current_player_var)
        ).grid(row=4, column=0)
        button_select = ttk.Button(game_window,
                                   text="Check",
                                   command=partial(self.player_checks, self.current_player_var)                                   
        ).grid(row=4, column=1)
        
        button_select = ttk.Button(game_window,
                                   text="Call",
                                   command=partial(self.player_calls, self.current_player_var)                                                                      
        ).grid(row=4, column=2)
        button_select = ttk.Button(game_window,
                                   text="Raise",
                                   command=partial(self.player_raises, self.current_player_var)                                                                                                         
        ).grid(row=4, column=3)

        button_quit = ttk.Button(game_window,
                                 text="Advance Stage",
                                 command=self.advance_stage
        ).grid(row=4, column=4)
        button_quit = ttk.Button(game_window,
                                 text="Finish Hand",
                                 command=partial(self.end_hand, game_window)
        ).grid(row=4, column=5)
        
        #init_window.mainloop()

        ''' 
        game_stats['current_players'] = current_players
        input_small_blind(game_stats)
        '''
        
        return
    
    def quit(self):
        self.window.destroy()
            
    def run(self):
        
        button_select = ttk.Button(self.window,
                                   text="Enter Players",
                                   command=self.enter_players,
        ).grid(row=0)

        button_select = ttk.Button(self.window,
                                   text="Enter Small Blind",
                                   command=self.enter_small_blind,
        ).grid(row=0, column=1)
        
        button_select = ttk.Button(self.window,
                                   text="Play",
                                   command=self.play_game,
        ).grid(row=0, column=2)

        button_quit = ttk.Button(self.window,
                                 text="Quit",
                                 command=self.quit
        ).grid(row=0, column=3)
        
        tk.Label(self.window, 
                 textvariable=self.players_var).grid(row=1, column=1, columnspan=2)
        tk.Label(self.window, 
                 textvariable=self.small_blind_var).grid(row=2, column=1)
        

        self.window.mainloop()


game = GuiGame()
game.run()



 


