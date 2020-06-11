import sys, os

# Merge test and src folders to allow test to import needed modules
testdir = os.path.dirname(__file__)
srcdir = '../poker_spirit'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import unittest

from player_hand import PlayerHand
from hand import Hand
from game import Game

from analyze_hand2 import parse_file

class TestParser(unittest.TestCase):

    ### Test Hands ###

    # Test Flops Seen (FS)
    def test_fs(self):
        print(f'\n\nTesting FS')
        
        path_to_test_file = 'test_files/hand_crafted/fs_test.txt'

        # Check if test file exists
        self.assertTrue(os.path.exists(path_to_test_file), f'Missing file: {path_to_test_file}')

        # Parse File
        game = parse_file(path_to_test_file)

        # Get first hand
        hand1 = game._hands[0]

        player1 = hand1.get_player('Player1')
        player2 = hand1.get_player('Player2')
        player3 = hand1.get_player('Player3')

        self.assertFalse(player1.has_seen_flop(), 'FS - Hand 1 - Player 1')
        self.assertTrue(player2.has_seen_flop(), 'FS - Hand 1 - Player 2')
        self.assertTrue(player3.has_seen_flop(), 'FS - Hand 1 - Player 3')

    # Test Voluntarily Put $ in Pot (VPiP)
    def test_vpip(self):
        print(f'\n\nTesting VPiP')

        path_to_test_file = 'test_files/hand_crafted/vpip_test.txt'

        # Check if test file exists
        self.assertTrue(os.path.exists(path_to_test_file), f'Missing file: {path_to_test_file}')

        # Parse File
        game = parse_file(path_to_test_file)

        # Get first hand
        hand1 = game._hands[0]

        player1 = hand1.get_player('Player1')
        player2 = hand1.get_player('Player2')
        player3 = hand1.get_player('Player3')
        player4 = hand1.get_player('Player4')

        # In first hand all players but Player4 has a vpip
        self.assertFalse(player1.has_vpip(), 'VPiP - Hand 1 - Player 1')
        self.assertTrue(player2.has_vpip(), 'VPiP - Hand 1 - Player 2')
        self.assertTrue(player3.has_vpip(), 'VPiP - Hand 1 - Player 3')
        self.assertTrue(player4.has_vpip(), 'VPiP - Hand 1 - Player 4')

        # Get second hand
        hand2 = game._hands[1]

        player1 = hand2.get_player('Player1')
        player2 = hand2.get_player('Player2')
        player3 = hand2.get_player('Player3')
        player4 = hand2.get_player('Player4')

        # In second hand everyone folds and the big blind checks
        # No one should have a vpip
        self.assertFalse(player1.has_vpip(), 'VPiP - Hand 2 - Player 1')
        self.assertFalse(player2.has_vpip(), 'VPiP - Hand 2 - Player 2')
        self.assertFalse(player3.has_vpip(), 'VPiP - Hand 2 - Player 3')
        self.assertFalse(player4.has_vpip(), 'VPiP - Hand 2 - Player 4')

        # Get third hand
        hand3 = game._hands[2]

        player1 = hand3.get_player('Player1')
        player2 = hand3.get_player('Player2')
        player3 = hand3.get_player('Player3')
        player4 = hand3.get_player('Player4')

        # In third hand the small blind calls big blind
        # The big blind checks and then bets in the flop
        self.assertFalse(player1.has_vpip(), 'VPiP - Hand 3 - Player 1')
        self.assertTrue(player2.has_vpip(), 'VPiP - Hand 3 - Player 2')
        self.assertTrue(player3.has_vpip(), 'VPiP - Hand 3 - Player 3')
        self.assertFalse(player4.has_vpip(), 'VPiP - Hand 3 - Player 4')

    # Test Preflop Raise (PFR)
    def test_pfr(self):
        print(f'\n\nTesting PFR')

        path_to_test_file = 'test_files/hand_crafted/pfr_test.txt'

        # Check if test file exists
        self.assertTrue(os.path.exists(path_to_test_file), f'Missing file: {path_to_test_file}')

        # Parse File
        game = parse_file(path_to_test_file)

        # Get first hand
        hand1 = game._hands[0]

        player1 = hand1.get_player('Player1')
        player2 = hand1.get_player('Player2')
        player3 = hand1.get_player('Player3')
        player4 = hand1.get_player('Player4')

        # In first hand player 2 Raised Pre-Flop
        self.assertFalse(player1.has_pfr(), 'PFR - Hand 1 - Player 1')
        self.assertTrue(player2.has_pfr(), 'PFR - Hand 1 - Player 2')
        self.assertFalse(player3.has_pfr(), 'PFR - Hand 1 - Player 3')
        self.assertFalse(player4.has_pfr(), 'PFR - Hand 1 - Player 4')

        # Get first hand
        hand2 = game._hands[1]

        player1 = hand2.get_player('Player1')
        player2 = hand2.get_player('Player2')
        player3 = hand2.get_player('Player3')
        player4 = hand2.get_player('Player4')

        # In second hand player 2 Raised Pre-Flop
        self.assertFalse(player1.has_pfr(), 'PFR - Hand 2 - Player 1')
        self.assertTrue(player2.has_pfr(), 'PFR - Hand 2 - Player 2')
        self.assertFalse(player3.has_pfr(), 'PFR - Hand 2 - Player 3')
        self.assertFalse(player4.has_pfr(), 'PFR - Hand 2 - Player 4')

    # Test Call Preflop Raise (CPFR)
    def test_cpfr(self):
        print(f'\n\nTesting CPFR')

        path_to_test_file = 'test_files/hand_crafted/pfr_test.txt'

        # Check if test file exists
        self.assertTrue(os.path.exists(path_to_test_file), f'Missing file: {path_to_test_file}')

        # Parse File
        game = parse_file(path_to_test_file)

        # Get first hand
        hand1 = game._hands[0]

        player1 = hand1.get_player('Player1')
        player2 = hand1.get_player('Player2')
        player3 = hand1.get_player('Player3')
        player4 = hand1.get_player('Player4')

        # In first hand Player 4 called the PFR by Player 2
        self.assertFalse(player1.has_cpfr(), 'CPFR - Hand 1 - Player 1')
        self.assertFalse(player2.has_cpfr(), 'CPFR - Hand 1 - Player 2')
        self.assertFalse(player3.has_cpfr(), 'CPFR - Hand 1 - Player 3')
        self.assertTrue(player4.has_cpfr(), 'CPFR - Hand 1 - Player 4')

        # All players but Player 2 had a chance to call the PFR
        self.assertTrue(player1.has_opt_cpfr(), 'Opt for CPFR - Hand 1 - Player 1')
        self.assertFalse(player2.has_opt_cpfr(), 'Opt for CPFR - Hand 1 - Player 2')
        self.assertTrue(player3.has_opt_cpfr(), 'Opt for CPFR - Hand 1 - Player 3')
        self.assertTrue(player4.has_opt_cpfr(), 'Opt for CPFR - Hand 1 - Player 4')

    # Test Unopened Preflop Raise (UOPFR)
    def test_uopfr(self):
        print(f'\n\nTesting UOPFR')

        path_to_test_file = 'test_files/hand_crafted/uopfr_test.txt'

        # Check if test file exists
        self.assertTrue(os.path.exists(path_to_test_file), f'Missing file: {path_to_test_file}')

        # Parse File
        game = parse_file(path_to_test_file)

        # Get first hand
        hand1 = game._hands[0]

        player1 = hand1.get_player('Player1')
        player2 = hand1.get_player('Player2')
        player3 = hand1.get_player('Player3')
        player4 = hand1.get_player('Player4')

        # In first hand Player 2 made an Unopened Preflop Raise (UOPFR) 
        self.assertFalse(player1.has_uopfr(), 'UOPFR - Hand 1 - Player 1')
        self.assertTrue(player2.has_uopfr(), 'UOPFR - Hand 1 - Player 2')
        self.assertFalse(player3.has_uopfr(), 'UOPFR - Hand 1 - Player 3')
        self.assertFalse(player4.has_uopfr(), 'UOPFR - Hand 1 - Player 4')

        # Player 1 and 2 had opportunities for an UOPFR
        self.assertTrue(player1.has_opt_uopfr(), 'Opt for UOPFR - Hand 1 - Player 1')
        self.assertTrue(player2.has_opt_uopfr(), 'Opt for UOPFR - Hand 1 - Player 2')
        self.assertFalse(player3.has_opt_uopfr(), 'Opt for UOPFR - Hand 1 - Player 3')
        self.assertFalse(player4.has_opt_uopfr(), 'Opt for UOPFR - Hand 1 - Player 4')

if __name__ == '__main__':
    unittest.main()
