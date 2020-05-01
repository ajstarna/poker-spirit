#!/usr/bin/env python3
from functools import partial

import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import ttk

import analyze_hands

class App:
    def __init__(self):
        self.filename = None
        self.player_windows = {}

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
        filename =  askopenfilename(initialdir = ".",
                                    title = "Select file"
        )

        if filename == '':
            return
        else:
            self.filename = filename

        truncated = self.get_truncated_name(filename)
        self.text_var.set(f"filename = {truncated}")


    def insert_stats_into_text(self, text, stats):
        text.delete(0.0, tk.END) # clear what is there

        hands = stats['hands_played']
        
        text.insert(tk.END,
                    f'VPIP = {stats["vpip"]}/{hands} = {round(100*stats["vpip"]/hands, 1)}\n'
        )
        text.insert(tk.END,
                    f'PFR = {stats["pfr"]}/{hands} = {round(100*stats["pfr"]/hands, 1)}\n'
        )
        if stats["3_bet_opp"] > 0:
            text.insert(tk.END,
                        f'3-Bet = {stats["3_bet"]}/{stats["3_bet_opp"]} = {round(100*stats["3_bet"]/stats["3_bet_opp"], 1)}\n'
            )
        else:
            text.insert(tk.END,
                        f'3-Bet = {stats["3_bet"]}/{stats["3_bet_opp"]} = 0\n'
            )
            
        text.insert(tk.END,
                    f'4-Bet = {stats["4_bet"]}/{hands} = {round(100*stats["4_bet"]/hands, 1)}'
        )

        
    def read_file(self):
        if self.filename is None:
            return
        else:
            game_stats = analyze_hands.run_file(self.filename)
            current_players = game_stats['current_players']
            for player in sorted(current_players, key=lambda x: x.lower()):
                stats = game_stats[player]
                if player in self.player_windows:
                    print(f'player {player} already current!')
                    window = self.player_windows[player]
                    print(window.winfo_children())
                    text = window.winfo_children()[0]
                    print()
                else:
                    # a new player has entered the table
                    window = tk.Tk()
                    window.geometry("165x60")
                    window.title(player)
                    text = tk.Text(window)

                    
                self.insert_stats_into_text(text, stats)
                text.pack()
                self.player_windows[player] = window
                    
            # don't want to have windows lingering around for players who
            # are no longer at the table
            for player in self.player_windows:
                if player not in current_players:
                    del self.player_windows[player]
            
    def quit(self):
        self.window.destroy()
        for window in self.player_windows.values():
            window.destroy()
            
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


app = App()
app.main()
