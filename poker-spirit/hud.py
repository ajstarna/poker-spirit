#!/usr/bin/env python3
import os

from collections import defaultdict

import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import ttk

from analyze_hands import PokerStarsGameIO, GameIO, assign_stats_from_hand
from db_management import PokerStarsDBManager
from dotenv import load_dotenv



class PlayerWindowsManager:
    # making this its own class so that we can use this code in the live tracker gui as well
    def __init__(self):
        self.player_windows = {}
        self.player_career_windows = {}        

        
    def destroy(self):
        for window in self.player_windows.values():
            window.destroy()
        for window in self.player_career_windows.values():
            window.destroy()
        
    def insert_stats_into_text(self, text, game_stats, player_name):
        text.delete(0.0, tk.END) # clear what is there
        text.insert(tk.END,
                    GameIO.vpip_str(game_stats, player_name) + "\n"
        )
        text.insert(tk.END,
                    GameIO.pfr_str(game_stats, player_name) + "\n"
        )
        text.insert(tk.END,
                    GameIO._3_bet_str(game_stats, player_name) + "\n"
        )
        text.insert(tk.END,
                    GameIO.folds_to_3_bet_str(game_stats, player_name) + "\n"
        )
        text.insert(tk.END,
                    GameIO.c_bet_str(game_stats, player_name) + "\n"
        )
        text.insert(tk.END,
                    GameIO.folds_to_c_bet_str(game_stats, player_name) + "\n"                    
        )
        text.insert(tk.END,
                    GameIO._4_bet_str(game_stats, player_name) + "\n"                
        )


    def merge_current_and_career_stats(self, game_stats, career_stats):
        '''
        If we have the career stats and the current game stats for a given player,
        we want to display the career stats INCLUDING the current game, so return a new
        dict with the summed values.
        '''
        new_stats = {}
        for player, stats in game_stats.items():
            new_stats[player] = defaultdict(int)
            for stat, game_val in stats.items():
                new_stats[player][stat] = game_val + career_stats[player][stat]
        return new_stats
    
    def populate(self, game, career_stats_by_player):

        new_stats = self.merge_current_and_career_stats(game.game_stats, career_stats_by_player)
        
        for player_name in sorted(game.current_players, key=lambda x: x.lower()):            
            if player_name in self.player_windows:
                window = self.player_windows[player_name]
                text = window.winfo_children()[0]
            else:
                # a new player has entered the table
                window = tk.Tk()
                self.player_windows[player_name] = window                
                window.geometry("185x100")
                window.title(player_name)
                text = tk.Text(window)

            self.insert_stats_into_text(text, game.game_stats, player_name)
            text.pack()

            #####
            #####
            if player_name in self.player_career_windows:
                window = self.player_career_windows[player_name]
                text = window.winfo_children()[0]
            else:
                # a new player has entered the table
                window = tk.Tk()
                self.player_career_windows[player_name] = window                
                window.geometry("185x100")
                window.title(player_name)
                text = tk.Text(window)

            self.insert_stats_into_text(text, new_stats, player_name)
            text.pack()
            
        # don't want to have windows lingering around for players who
        # are no longer at the table
        for player_name in list(self.player_windows.keys()):
            if player_name not in game.current_players:
                del self.player_windows[player_name]
                del self.player_career_windows[player_name]                
        
class App:
    def __init__(self):
        self.filename = None
        self.db_manager = PokerStarsDBManager()
        self.career_stats_by_player = {}
        self.pwm = PlayerWindowsManager()
        load_dotenv()
        # get env vars from .env file
        self.path_to_hands = os.getenv("PATH_TO_HANDS", ".")
        self.path_to_stats_db = os.getenv("PATH_TO_STATS_DB", "player_stats.db")        
                                       
    def get_truncated_name(self, filename):
        if filename is None:
            return None
        print(filename)
        if len(filename) > 75:
            truncated = '....' + filename[-75:]
        else:
            truncated = filename
        return truncated
    
    def select_file(self):
        filename =  askopenfilename(initialdir = self.path_to_hands,
                                    title = "Select file"
        )

        if filename == '':
            return
        else:
            self.filename = filename

        truncated = self.get_truncated_name(filename)
        self.text_var.set(f"filename = {truncated}")
        
    def read_file(self):
        if self.filename is None:
            return
        else:
            self.game = PokerStarsGameIO(self.filename)
            self.game.run_file()
            self.career_stats_by_player = self.db_manager.load_player_history(self.game, self.career_stats_by_player)
            self.pwm.populate(self.game, self.career_stats_by_player)

    def save_data(self):
        self.db_manager.insert_player_stats(self.game)
            
    def quit(self):
        self.window.destroy()
        self.pwm.destroy()
            
    def main(self):
        self.game = None
        self.window = tk.Tk()
        self.window.geometry("575x115")
        
        self.window.title( "Poker Spirit")

        button_select = ttk.Button(self.window,
                                   text="Select File",
                                   command=self.select_file,
        ).pack()

        self.text_var = tk.StringVar()
        truncated = self.get_truncated_name(self.filename)        
        self.text_var.set(f"filename = {truncated}")
        file_label = ttk.Label(self.window, textvariable=self.text_var).pack() #text=f"filename = {self.filename}")

        button_run = ttk.Button(self.window,
                                text="Read and Analyze File",
                                command=self.read_file
        ).pack()
        button_run = ttk.Button(self.window,
                                text="Save Game Data",
                                command=self.save_data
        ).pack()
        button_quit = ttk.Button(self.window,
                                 text="Quit",
                                 command=self.quit
        ).pack()

        self.window.mainloop()

if __name__ == "__main__":
    app = App()
    app.main()
