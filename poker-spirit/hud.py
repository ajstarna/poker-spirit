#!/usr/bin/env python3
import os

import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import ttk

from analyze_hands import FileGame

from dotenv import load_dotenv



class PlayerWindowsManager:
    # making this its own class so that we can use this code in the live tracker gui as well
    def __init__(self):
        self.player_windows = {}

    def destroy(self):
        for window in self.player_windows.values():
            window.destroy()
        
    def insert_stats_into_text(self, text, game, player_name):
        text.delete(0.0, tk.END) # clear what is there
        text.insert(tk.END,
                    game.vpip_str(player_name) + "\n"
        )
        text.insert(tk.END,
                    game.pfr_str(player_name) + "\n"
        )
        text.insert(tk.END,
                    game._3_bet_str(player_name) + "\n"
        )
        text.insert(tk.END,
                    game.folds_to_3_bet_str(player_name) + "\n"
        )
        text.insert(tk.END,
                    game.c_bet_str(player_name) + "\n"
        )
        text.insert(tk.END,
                    game.folds_to_c_bet_str(player_name) + "\n"                    
        )
        text.insert(tk.END,
                    game._4_bet_str(player_name) + "\n"                
        )

        
    def populate(self, game):
        #for player_name in sorted(game.current_players, key=lambda x: x.lower()):
        for player_name in sorted(game.current_players, key=lambda x: x.lower()):            
            if player_name in self.player_windows:
                print(f'player {player_name} already current!')
                window = self.player_windows[player_name]
                text = window.winfo_children()[0]
            else:
                # a new player has entered the table
                window = tk.Tk()
                self.player_windows[player_name] = window                
                window.geometry("185x100")
                window.title(player_name)
                text = tk.Text(window)

            self.insert_stats_into_text(text, game, player_name)
            text.pack()

        # don't want to have windows lingering around for players who
        # are no longer at the table
        for player_name in self.player_windows:
            if player_name not in game.current_players:
                del self.player_windows[player_name]
        
class App:
    def __init__(self):
        self.filename = None
        self.pwm = PlayerWindowsManager()
        load_dotenv()
        # get env vars from .env file
        self.path_to_hands = os.getenv("PATH_TO_HANDS", ".")
                                       
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
            game = FileGame(self.filename)
            game.run_file()
            self.pwm.populate(game)
            
    def quit(self):
        self.window.destroy()
        self.pwm.destroy()
            
    def main(self):
        self.window = tk.Tk()
        self.window.geometry("575x100")
        
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
        button_quit = ttk.Button(self.window,
                                 text="Quit",
                                 command=self.quit
        ).pack()

        self.window.mainloop()

if __name__ == "__main__":
    app = App()
    app.main()
