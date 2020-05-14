#!/usr/bin/env python3
from tinydb import TinyDB, Query
from collections import defaultdict

GAME_STATS_TABLE = 'gamestats'

def load_player_history(db_file_name, player_names):
    db = TinyDB(db_file_name)
    table = db.table(GAME_STATS_TABLE)
    Player = Query()
    career_stats_by_player = {}
    for player_name in player_names:
        career_stats = defaultdict(int)
        for stats in table.search(Player.player_name == player_name):
            for field, val in stats:
                if type(val) is int:
                    career_stats[field] += val
        career_stats_by_player[player_name] = career_stats
    return career_stats_by_player

def insert_all_player_stats(db_file_name, game):
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
    conn = sqlite3.connect(db_file_name)    
    cursor = conn.execute("SELECT player_name, game_id, hands_played, vpip from GAME_STATS")
    for row in cursor:
        print(row)
