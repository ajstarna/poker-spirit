#!/usr/bin/env python3
from tinydb import TinyDB, Query
from collections import defaultdict
import datetime
import time


'''
This serialization code is taken directly from https://github.com/msiemens/tinydb-serialization
Needed so that we can use datetime objects within TinyDB

from tinydb_serialization import Serializer

class DateTimeSerializer(Serializer):
    OBJ_CLASS = datetime  # The class this serializer handles

    def encode(self, obj):
        return obj.strftime('%Y-%m-%dT%H:%M:%S')

    def decode(self, s):
        return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')
'''


class DBManager:
    FILE_NAME = None
    GAME_STATS_TABLE = 'gamestats'
    
    def __init__(self):
        self.last_read_date = 0 # seconds since epoch start at zero (beginning of time)
        
    def load_player_history(self, player_names, career_stats_by_player=None):
        if self.FILE_NAME is None:
            # can't call this method from this class, need a subclass            
            raise NotImplementedError
        
        db = TinyDB(self.FILE_NAME)
        table = db.table(self.GAME_STATS_TABLE)
        Player = Query()
        if career_stats_by_player is None:
            career_stats_by_player = {}
        for player_name in player_names:
            if player_name in career_stats_by_player:
                career_stats = career_stats_by_player[player_name]
            else:
                career_stats = defaultdict(int)
            all_stats = table.search((Player.player_name == player_name) & (Player.updated_time > self.last_read_date))
            for stats in all_stats:
                for field, val in stats.items():
                    if type(val) is int:
                        career_stats[field] += val
            career_stats_by_player[player_name] = career_stats
        now = time.time()
        self.last_read_date = now
        return career_stats_by_player

    def insert_player_stats(self, game):
        if self.FILE_NAME is None:
            # can't call this method from this class, need a subclass            
            raise NotImplementedError
        
        db = TinyDB(self.FILE_NAME)
        table = db.table(self.GAME_STATS_TABLE)
        GAME_STATS = Query()
        print(game.game_stats)
        now = time.time()
        now_str = str(datetime.datetime.utcnow())
        print(f'new now str = {now_str}')
        for player_name, stats in game.game_stats.items():
            game_id = stats.get('game_id')
            if 'created_time' not in stats:
                stats['created_time'] = now
                stats['created_date'] = now_str                                
            stats['updated_time'] = now
            stats['updated_date'] = now_str
            print('about to enter stats:')
            print(stats)
            print()
            table.upsert(stats, (GAME_STATS.player_name == player_name) & (GAME_STATS.game_id == game.game_id))
            
class LiveDBManager(DBManager):
    FILE_NAME = 'player_stats_live.db'

class PokerStarsDBManager(DBManager):
    FILE_NAME = 'player_stats_poker_stars.db'    


if __name__ == "__main__":
    manager = PokerStarsDBManager()
    career_stats_by_player = manager.load_player_history(player_names={'sleep evil'})
    print(career_stats_by_player)
                                                 
