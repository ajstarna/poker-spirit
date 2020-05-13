#!/usr/bin/env python3
import sqlite3

def load_player_history(db_file_name, player_names):
    conn = sqlite3.connect(db_file_name)
    for playername in player_names:
        pass
    conn.close()


def insert_player_stats(db_file_name, game):

    create_games_table_str = """ CREATE TABLE IF NOT EXISTS game_stats (
    player_name text,
    game_id text,
    hands_played integer,
    VPIP integer,
    PFR integer,
    _3_Bet integer,
    Folds_3_Bet integer,
    Calls_3_Bet integer,
    _4_Bet integer,
    C_Bet integer,
    Checks_C_Bet_Opp integer,
    Folds_C_Bet integer,
    Calls_C_Bet integer,
    Raises_C_Bet integer,
    PRIMARY KEY(player_name, game_id)
    ); """    

    conn = sqlite3.connect(db_file_name)
    conn.execute(create_games_table_str)

    for player_name in game.current_players:
        stats = game.game_stats[player_name]
        insert_str = "INSERT INTO game_stats (player_name, game_id, hands_played, VPIP, PFR, _3_bet, Folds_3_Bet, " \
        "Calls_3_Bet, _4_Bet, C_Bet, Checks_C_Bet_Opp, Folds_C_Bet, Calls_C_Bet, Raises_C_Bet) " \
        f"VALUES ('{player_name}', '{game.game_id}', {stats['hands_played']}, {stats['vpip']}, {stats['pfr']}, {stats['3_bet']}, {stats['folds_to_3_bet']}, " \
        f"{stats['calls_3_bet']}, {stats['4_bet']}, {stats['C_bet']}, {stats['checks_c_bet_opp']}, {stats['folds_C_bet']}, {stats['calls_C_bet']}, {stats['raises_c_bet']} )"
        print(insert_str)
        conn.execute(insert_str)
    conn.commit()
    conn.close()
    

if __name__ == "__main__":
    db_file_name = 'player_stats.db'
    conn = sqlite3.connect(db_file_name)    
    cursor = conn.execute("SELECT player_name, game_id, hands_played, vpip from GAME_STATS")
    for row in cursor:
        print(row)
