from player_hand import PlayerHand
from hand import Hand

from player_stats import PlayerStats


class Game:
    def __init__(self):
        self._hands = []
        self._player_stats = {}

    def add_hand(self, hand):
        # Add hand to array list for testing and history
        self._hands.append(hand)

        # Update stats
        # Get players in hand
        players = hand.get_all_players()
        for player_hand in players:
            # Get player
            player_name = player_hand.name
            player_stats = self.get_player_stats(player_name)

            # Update stats
            # Increase the number of hands played by 1
            player_stats.increase_hands_played()

            # Has seen flop?
            if player_hand.has_seen_flop():
                player_stats.increase_fs()

            # VPiP
            if player_hand.has_vpip():
                player_stats.increase_vpip()

            # PFR
            if player_hand.has_pfr():
                player_stats.increase_pfr()

            # CPFR
            if player_hand.has_cpfr():
                player_stats.increase_cpfr()

            if player_hand.has_opt_cpfr():
                player_stats.increase_opt_cpfr()

            # UOPFR
            if player_hand.has_uopfr():
                player_stats.increase_uopfr()

            if player_hand.has_opt_uopfr():
                player_stats.increase_opt_uopfr()

            # 3B
            if player_hand.has_3b():
                player_stats.increase_3b()

            if player_hand.has_opt_3b():
                player_stats.increase_opt_3b()

            # F3B
            if player_hand.has_f3b():
                player_stats.increase_f3b()

            if player_hand.has_opt_f3b():
                player_stats.increase_opt_f3b()

            # 4B
            if player_hand.has_4b():
                player_stats.increase_4b()

            if player_hand.has_opt_4b():
                player_stats.increase_opt_4b()

            # F4B
            if player_hand.has_f4b():
                player_stats.increase_f4b()

            if player_hand.has_opt_f4b():
                player_stats.increase_opt_f4b()

    def get_player_stats(self, player_name):
        # Return player stats if already exists
        if player_name in self._player_stats:
            return self._player_stats[player_name]
        
        # Create new player and add them to player stats dict
        player_stats = PlayerStats(player_name)
        self._player_stats[player_name] = player_stats
        
        return player_stats

    def __str__(self):
        output = f'Game Stats:\n\n'
        for player in self._player_stats.values():
            output += f'{player}\n\n'

        return output
