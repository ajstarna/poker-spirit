import unittest
from os import path

from poker_spirit.analyze_hand2 import parse_file, Game, Hand, PlayerHand

class TestParser(unittest.TestCase):

    def test_vpip(self):
        print(f'Testing VPiP')
        
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
        self.assertTrue(player1.hasVPiP(), 'Hand 1 - Player 1')
        self.assertTrue(player2.hasVPiP(), 'Hand 1 - Player 2')
        self.assertTrue(player3.hasVPiP(), 'Hand 1 - Player 3')
        self.assertFalse(player4.hasVPiP(), 'Hand 1 - Player 4')

        # Get second hand
        hand2 = game._hands[1]

        player1 = hand2.getPlayer('Player1')
        player2 = hand2.getPlayer('Player2')
        player3 = hand2.getPlayer('Player3')
        player4 = hand2.getPlayer('Player4')

        # In second hand everyone folds and the big button checks
        # No one should have a vpip
        self.assertFalse(player1.hasVPiP(), 'Hand 2 - Player 1')
        self.assertFalse(player2.hasVPiP(), 'Hand 2 - Player 2')
        self.assertFalse(player3.hasVPiP(), 'Hand 2 - Player 3')
        self.assertFalse(player4.hasVPiP(), 'Hand 2 - Player 4')

if __name__ == '__main__':
    unittest.main()