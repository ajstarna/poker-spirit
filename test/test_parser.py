import unittest
from os import path

from poker_spirit.analyze_hand2 import parse_file, Game, Hand, PlayerHand

class TestParser(unittest.TestCase):

    ### Test Hands ###

    # Test Flops Seen (FS)
    def test_fs(self):
        print(f'\n\nTesting FS')
        
        path_to_test_file = 'test_files/hand_crafted/fs_test.txt'

        # Check if test file exists
        self.assertTrue(path.exists(path_to_test_file), f'Missing file: {path_to_test_file}')

        # Parse File
        game = parse_file(path_to_test_file)

        # Get first hand
        hand1 = game._hands[0]

        player1 = hand1.getPlayer('Player1')
        player2 = hand1.getPlayer('Player2')
        player3 = hand1.getPlayer('Player3')

        self.assertFalse(player1.hasSeenFlop(), 'FS - Hand 1 - Player 1')
        self.assertTrue(player2.hasSeenFlop(), 'FS - Hand 1 - Player 2')
        self.assertTrue(player3.hasSeenFlop(), 'FS - Hand 1 - Player 3')

    # Test Voluntarily Put $ in Pot (VPiP)
    def test_vpip(self):
        print(f'\n\nTesting VPiP')

        path_to_test_file = 'test_files/hand_crafted/vpip_test.txt'

        # Check if test file exists
        self.assertTrue(path.exists(path_to_test_file), f'Missing file: {path_to_test_file}')

        # Parse File
        game = parse_file(path_to_test_file)

        # Get first hand
        hand1 = game._hands[0]

        player1 = hand1.getPlayer('Player1')
        player2 = hand1.getPlayer('Player2')
        player3 = hand1.getPlayer('Player3')
        player4 = hand1.getPlayer('Player4')

        # In first hand all players but Player4 has a vpip
        self.assertTrue(player1.hasVPiP(), 'VPiP - Hand 1 - Player 1')
        self.assertTrue(player2.hasVPiP(), 'VPiP - Hand 1 - Player 2')
        self.assertTrue(player3.hasVPiP(), 'VPiP - Hand 1 - Player 3')
        self.assertFalse(player4.hasVPiP(), 'VPiP - Hand 1 - Player 4')

        # Get second hand
        hand2 = game._hands[1]

        player1 = hand2.getPlayer('Player1')
        player2 = hand2.getPlayer('Player2')
        player3 = hand2.getPlayer('Player3')
        player4 = hand2.getPlayer('Player4')

        # In second hand everyone folds and the big button checks
        # No one should have a vpip
        self.assertFalse(player1.hasVPiP(), 'VPiP - Hand 2 - Player 1')
        self.assertFalse(player2.hasVPiP(), 'VPiP - Hand 2 - Player 2')
        self.assertFalse(player3.hasVPiP(), 'VPiP - Hand 2 - Player 3')
        self.assertFalse(player4.hasVPiP(), 'VPiP - Hand 2 - Player 4')

    # Test Preflop Raise (PFR)
    def test_pfr(self):
        print(f'\n\nTesting PFR')

        path_to_test_file = 'test_files/hand_crafted/pfr_test.txt'

        # Check if test file exists
        self.assertTrue(path.exists(path_to_test_file), f'Missing file: {path_to_test_file}')

        # Parse File
        game = parse_file(path_to_test_file)

        # Get first hand
        hand1 = game._hands[0]

        player1 = hand1.getPlayer('Player1')
        player2 = hand1.getPlayer('Player2')
        player3 = hand1.getPlayer('Player3')
        player4 = hand1.getPlayer('Player4')

        # In first hand player 2 Raised Pre-Flop
        self.assertFalse(player1.hasPFR(), 'PFR - Hand 1 - Player 1')
        self.assertTrue(player2.hasPFR(), 'PFR - Hand 1 - Player 2')
        self.assertFalse(player3.hasPFR(), 'PFR - Hand 1 - Player 3')
        self.assertFalse(player4.hasPFR(), 'PFR - Hand 1 - Player 4')

        # Get first hand
        hand2 = game._hands[1]

        player1 = hand2.getPlayer('Player1')
        player2 = hand2.getPlayer('Player2')
        player3 = hand2.getPlayer('Player3')
        player4 = hand2.getPlayer('Player4')

        # In second hand player 2 Raised Pre-Flop
        self.assertFalse(player1.hasPFR(), 'PFR - Hand 2 - Player 1')
        self.assertTrue(player2.hasPFR(), 'PFR - Hand 2 - Player 2')
        self.assertFalse(player3.hasPFR(), 'PFR - Hand 2 - Player 3')
        self.assertFalse(player4.hasPFR(), 'PFR - Hand 2 - Player 4')

    # Test Call Preflop Raise (CPFR)
    def test_cpfr(self):
        print(f'\n\nTesting CPFR')

        path_to_test_file = 'test_files/hand_crafted/pfr_test.txt'

        # Check if test file exists
        self.assertTrue(path.exists(path_to_test_file), f'Missing file: {path_to_test_file}')

        # Parse File
        game = parse_file(path_to_test_file)

        # Get first hand
        hand1 = game._hands[0]

        player1 = hand1.getPlayer('Player1')
        player2 = hand1.getPlayer('Player2')
        player3 = hand1.getPlayer('Player3')
        player4 = hand1.getPlayer('Player4')

        # In first hand Player 4 called the PFR by Player 2
        self.assertFalse(player1.hasCPFR(), 'CPFR - Hand 1 - Player 1')
        self.assertFalse(player2.hasCPFR(), 'CPFR - Hand 1 - Player 2')
        self.assertFalse(player3.hasCPFR(), 'CPFR - Hand 1 - Player 3')
        self.assertTrue(player4.hasCPFR(), 'CPFR - Hand 1 - Player 4')

        # All players but Player 2 had a chance to call the PFR
        self.assertTrue(player1.hasOptCPFR(), 'Opt for CPFR - Hand 1 - Player 1')
        self.assertFalse(player2.hasOptCPFR(), 'Opt for CPFR - Hand 1 - Player 2')
        self.assertTrue(player3.hasOptCPFR(), 'Opt for CPFR - Hand 1 - Player 3')
        self.assertTrue(player4.hasOptCPFR(), 'Opt for CPFR - Hand 1 - Player 4')

    # Test Unopened Preflop Raise (UOPFR)
    def test_uopfr(self):
        print(f'\n\nTesting UOPFR')

        path_to_test_file = 'test_files/hand_crafted/uopfr_test.txt'

        # Check if test file exists
        self.assertTrue(path.exists(path_to_test_file), f'Missing file: {path_to_test_file}')

        # Parse File
        game = parse_file(path_to_test_file)

        # Get first hand
        hand1 = game._hands[0]

        player1 = hand1.getPlayer('Player1')
        player2 = hand1.getPlayer('Player2')
        player3 = hand1.getPlayer('Player3')
        player4 = hand1.getPlayer('Player4')

        # In first hand Player 2 made an Unopened Preflop Raise (UOPFR) 
        self.assertFalse(player1.hasUOPFR(), 'UOPFR - Hand 1 - Player 1')
        self.assertTrue(player2.hasUOPFR(), 'UOPFR - Hand 1 - Player 2')
        self.assertFalse(player3.hasUOPFR(), 'UOPFR - Hand 1 - Player 3')
        self.assertFalse(player4.hasUOPFR(), 'UOPFR - Hand 1 - Player 4')

        # Player 1 and 2 had opportunities for an UOPFR
        self.assertTrue(player1.hasOptUOPFR(), 'Opt for UOPFR - Hand 1 - Player 1')
        self.assertTrue(player2.hasOptUOPFR(), 'Opt for UOPFR - Hand 1 - Player 2')
        self.assertFalse(player3.hasOptUOPFR(), 'Opt for UOPFR - Hand 1 - Player 3')
        self.assertFalse(player4.hasOptUOPFR(), 'Opt for UOPFR - Hand 1 - Player 4')

if __name__ == '__main__':
    unittest.main()