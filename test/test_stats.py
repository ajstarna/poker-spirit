import sys, os

# Merge test and src folders to allow test to import needed modules
testdir = os.path.dirname(__file__)
srcdir = '../poker_spirit'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import unittest

from analyze_hand2 import parse_file

class TestStats(unittest.TestCase):

    # Test Micro Game 1
    def test_micro_game_1(self):
        print(f'\n\nTesting Micro Game 1')
        
        path_to_test_file = 'test_files/hand_crafted/games/micro_game_1.txt'

        # Check if test file exists
        self.assertTrue(os.path.exists(path_to_test_file), f'Missing file: {path_to_test_file}')

        # Parse File
        game = parse_file(path_to_test_file)

        # Test Player 1
        # Player1 / #h 4 / fs 2/4 / VPiP 1/4
        # pfr 0/4 / cpfr 0/1 / uopfr 0/2
        # 3B 0/1 / F3B 0/0 / 4B 0/0 / F4B 0/0
        player = game.get_player_stats('Player1')
        self.assertEqual(player.hands_played, 4, f'Micro Game 1 - {player.name} - #h')
        self.assertEqual(player.fs.numerator, 2, f'Micro Game 1 - {player.name} - fs - numerator')
        self.assertEqual(player.fs.denominator, 4, f'Micro Game 1 - {player.name} - fs - denominator')
        self.assertEqual(player.vpip.numerator, 1, f'Micro Game 1 - {player.name} - vpip - numerator')
        self.assertEqual(player.vpip.denominator, 4, f'Micro Game 1 - {player.name} - vpip - denominator')
        self.assertEqual(player.pfr.numerator, 0, f'Micro Game 1 - {player.name} - pfr - numerator')
        self.assertEqual(player.pfr.denominator, 4, f'Micro Game 1 - {player.name} - pfr - denominator')
        self.assertEqual(player.cpfr.numerator, 0, f'Micro Game 1 - {player.name} - cpfr - numerator')
        self.assertEqual(player.cpfr.denominator, 1, f'Micro Game 1 - {player.name} - cpfr - denominator')
        self.assertEqual(player.uopfr.numerator, 0, f'Micro Game 1 - {player.name} - uopfr - numerator')
        self.assertEqual(player.uopfr.denominator, 2, f'Micro Game 1 - {player.name} - uopfr - denominator')
        self.assertEqual(player.p3b.numerator, 0, f'Micro Game 1 - {player.name} - 3b - numerator')
        self.assertEqual(player.p3b.denominator, 1, f'Micro Game 1 - {player.name} - 3b - denominator')
        self.assertEqual(player.f3b.numerator, 0, f'Micro Game 1 - {player.name} - f3b - numerator')
        self.assertEqual(player.f3b.denominator, 0, f'Micro Game 1 - {player.name} - f3b - denominator')
        self.assertEqual(player.p4b.numerator, 0, f'Micro Game 1 - {player.name} - 4b - numerator')
        self.assertEqual(player.p4b.denominator, 0, f'Micro Game 1 - {player.name} - 4b - denominator')
        self.assertEqual(player.f4b.numerator, 0, f'Micro Game 1 - {player.name} - f4b - numerator')
        self.assertEqual(player.f4b.denominator, 0, f'Micro Game 1 - {player.name} - f4b - denominator')

        # Test Player 2
        # Player2 / #h 4 / fs 1/4 / VPiP 2/4
        # pfr 0/4 / cpfr 1/1 / uopfr 0/2
        # 3B 0/1 / F3B 0/0 / 4B 0/0 / F4B 0/0
        player = game.get_player_stats('Player2')
        self.assertEqual(player.hands_played, 4, f'Micro Game 1 - {player.name} - #h')
        self.assertEqual(player.fs.numerator, 1, f'Micro Game 1 - {player.name} - fs - numerator')
        self.assertEqual(player.fs.denominator, 4, f'Micro Game 1 - {player.name} - fs - denominator')
        self.assertEqual(player.vpip.numerator, 2, f'Micro Game 1 - {player.name} - vpip - numerator')
        self.assertEqual(player.vpip.denominator, 4, f'Micro Game 1 - {player.name} - vpip - denominator')
        self.assertEqual(player.pfr.numerator, 0, f'Micro Game 1 - {player.name} - pfr - numerator')
        self.assertEqual(player.pfr.denominator, 4, f'Micro Game 1 - {player.name} - pfr - denominator')
        self.assertEqual(player.cpfr.numerator, 1, f'Micro Game 1 - {player.name} - cpfr - numerator')
        self.assertEqual(player.cpfr.denominator, 1, f'Micro Game 1 - {player.name} - cpfr - denominator')
        self.assertEqual(player.uopfr.numerator, 0, f'Micro Game 1 - {player.name} - uopfr - numerator')
        self.assertEqual(player.uopfr.denominator, 2, f'Micro Game 1 - {player.name} - uopfr - denominator')
        self.assertEqual(player.p3b.numerator, 0, f'Micro Game 1 - {player.name} - 3b - numerator')
        self.assertEqual(player.p3b.denominator, 1, f'Micro Game 1 - {player.name} - 3b - denominator')
        self.assertEqual(player.f3b.numerator, 0, f'Micro Game 1 - {player.name} - f3b - numerator')
        self.assertEqual(player.f3b.denominator, 0, f'Micro Game 1 - {player.name} - f3b - denominator')
        self.assertEqual(player.p4b.numerator, 0, f'Micro Game 1 - {player.name} - 4b - numerator')
        self.assertEqual(player.p4b.denominator, 0, f'Micro Game 1 - {player.name} - 4b - denominator')
        self.assertEqual(player.f4b.numerator, 0, f'Micro Game 1 - {player.name} - f4b - numerator')
        self.assertEqual(player.f4b.denominator, 0, f'Micro Game 1 - {player.name} - f4b - denominator')

        # Test Player 3
        # Player3 / #h 4 / fs 1/4 / VPiP 2/4
        # pfr 1/4 / cpfr 0/1 / uopfr 0/2
        # 3B 1/1 / F3B 0/0 / 4B 0/0 / F4B 0/0
        player = game.get_player_stats('Player3')
        self.assertEqual(player.hands_played, 4, f'Micro Game 1 - {player.name} - #h')
        self.assertEqual(player.fs.numerator, 1, f'Micro Game 1 - {player.name} - fs - numerator')
        self.assertEqual(player.fs.denominator, 4, f'Micro Game 1 - {player.name} - fs - denominator')
        self.assertEqual(player.vpip.numerator, 2, f'Micro Game 1 - {player.name} - vpip - numerator')
        self.assertEqual(player.vpip.denominator, 4, f'Micro Game 1 - {player.name} - vpip - denominator')
        self.assertEqual(player.pfr.numerator, 1, f'Micro Game 1 - {player.name} - pfr - numerator')
        self.assertEqual(player.pfr.denominator, 4, f'Micro Game 1 - {player.name} - pfr - denominator')
        self.assertEqual(player.cpfr.numerator, 0, f'Micro Game 1 - {player.name} - cpfr - numerator')
        self.assertEqual(player.cpfr.denominator, 1, f'Micro Game 1 - {player.name} - cpfr - denominator')
        self.assertEqual(player.uopfr.numerator, 0, f'Micro Game 1 - {player.name} - uopfr - numerator')
        self.assertEqual(player.uopfr.denominator, 2, f'Micro Game 1 - {player.name} - uopfr - denominator')
        self.assertEqual(player.p3b.numerator, 1, f'Micro Game 1 - {player.name} - 3b - numerator')
        self.assertEqual(player.p3b.denominator, 1, f'Micro Game 1 - {player.name} - 3b - denominator')
        self.assertEqual(player.f3b.numerator, 0, f'Micro Game 1 - {player.name} - f3b - numerator')
        self.assertEqual(player.f3b.denominator, 0, f'Micro Game 1 - {player.name} - f3b - denominator')
        self.assertEqual(player.p4b.numerator, 0, f'Micro Game 1 - {player.name} - 4b - numerator')
        self.assertEqual(player.p4b.denominator, 0, f'Micro Game 1 - {player.name} - 4b - denominator')
        self.assertEqual(player.f4b.numerator, 0, f'Micro Game 1 - {player.name} - f4b - numerator')
        self.assertEqual(player.f4b.denominator, 0, f'Micro Game 1 - {player.name} - f4b - denominator')

        # Test Player 4
        # Player4 / #h 4 / fs 1/4 / VPiP 2/4
        # pfr 1/4 / cpfr 0/1 / uopfr 0/2
        # 3B 0/0 / F3B 1/1 / 4B 0/0 / F4B 0/0
        player = game.get_player_stats('Player4')
        self.assertEqual(player.hands_played, 4, f'Micro Game 1 - {player.name} - #h')
        self.assertEqual(player.fs.numerator, 1, f'Micro Game 1 - {player.name} - fs - numerator')
        self.assertEqual(player.fs.denominator, 4, f'Micro Game 1 - {player.name} - fs - denominator')
        self.assertEqual(player.vpip.numerator, 2, f'Micro Game 1 - {player.name} - vpip - numerator')
        self.assertEqual(player.vpip.denominator, 4, f'Micro Game 1 - {player.name} - vpip - denominator')
        self.assertEqual(player.pfr.numerator, 1, f'Micro Game 1 - {player.name} - pfr - numerator')
        self.assertEqual(player.pfr.denominator, 4, f'Micro Game 1 - {player.name} - pfr - denominator')
        self.assertEqual(player.cpfr.numerator, 0, f'Micro Game 1 - {player.name} - cpfr - numerator')
        self.assertEqual(player.cpfr.denominator, 1, f'Micro Game 1 - {player.name} - cpfr - denominator')
        self.assertEqual(player.uopfr.numerator, 0, f'Micro Game 1 - {player.name} - uopfr - numerator')
        self.assertEqual(player.uopfr.denominator, 2, f'Micro Game 1 - {player.name} - uopfr - denominator')
        self.assertEqual(player.p3b.numerator, 0, f'Micro Game 1 - {player.name} - 3b - numerator')
        self.assertEqual(player.p3b.denominator, 0, f'Micro Game 1 - {player.name} - 3b - denominator')
        self.assertEqual(player.f3b.numerator, 1, f'Micro Game 1 - {player.name} - f3b - numerator')
        self.assertEqual(player.f3b.denominator, 1, f'Micro Game 1 - {player.name} - f3b - denominator')
        self.assertEqual(player.p4b.numerator, 0, f'Micro Game 1 - {player.name} - 4b - numerator')
        self.assertEqual(player.p4b.denominator, 0, f'Micro Game 1 - {player.name} - 4b - denominator')
        self.assertEqual(player.f4b.numerator, 0, f'Micro Game 1 - {player.name} - f4b - numerator')
        self.assertEqual(player.f4b.denominator, 0, f'Micro Game 1 - {player.name} - f4b - denominator')

if __name__ == '__main__':
    unittest.main()
