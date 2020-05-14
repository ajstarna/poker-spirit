#!/usr/bin/env python3
from tinydb import TinyDB, Query
from collections import defaultdict

DB_FILE_NAME = 'player_stats.db'
GAME_STATS_TABLE = 'gamestats'

def load_player_history(player_names, db_file_name=None):
    if db_file_name is None:
        db_file_name = DB_FILE_NAME
    db = TinyDB(db_file_name)
    table = db.table(GAME_STATS_TABLE)
    Player = Query()
    career_stats_by_player = {}
    for player_name in player_names:
        career_stats = defaultdict(int)
        for stats in table.search(Player.player_name == player_name):
            for field, val in stats.items():
                if type(val) is int:
                    career_stats[field] += val
        career_stats_by_player[player_name] = career_stats
    return career_stats_by_player

def insert_all_player_stats(game, db_file_name):
    if db_file_name is None:
        db_file_name = DB_FILE_NAME
    
    db = TinyDB(db_file_name)
    table = db.table(GAME_STATS_TABLE)
    GAME_STATS = Query()
    print('sdfdsfdsf')
    print(game.game_stats)
    for player_name, stats in game.game_stats.items():
        game_id = stats.get('game_id')
        table.upsert(stats, (GAME_STATS.player_name == player_name) & (GAME_STATS.game_id == player_name))

if __name__ == "__main__":
    db_file_name = 'player_stats.db'
    career_stats_by_player = load_player_history(db_file_name, {'sleep evil'})
    print(career_stats_by_player)
                                                 
