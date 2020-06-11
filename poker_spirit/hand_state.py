from enum import Enum

# States of the hand
class HAND_STATE(Enum):
    COMPULSORY_BETS = 1
    PRE_FLOP = 2
    FLOP = 3
    TURN = 4
    RIVER = 5
    SHOWDOWN = 6
    END = 7

    @staticmethod
    def to_string(hand_state):
        if hand_state == HAND_STATE.COMPULSORY_BETS:
            return 'COMPULSORY_BETS'
        elif hand_state == HAND_STATE.PRE_FLOP:
            return 'PRE_FLOP'
        elif hand_state == HAND_STATE.FLOP:
            return 'FLOP'
        elif hand_state == HAND_STATE.TURN:
            return 'TURN'
        elif hand_state == HAND_STATE.RIVER:
            return 'RIVER'
        elif hand_state == HAND_STATE.SHOWDOWN:
            return 'SHOWDOWN'
        else:
            return 'UNKNOWN'
