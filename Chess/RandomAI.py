#import chess
import random
from time import sleep

class RandomAI():
    def __init__(self):
        pass

    def choose_move(self, board, white_to_play):
        moves = list(board.legal_moves)
        move = random.choice(moves) # move by the random Ai chosen by using a random number generator
        sleep(1)   # I'm thinking so hard.
        print("Random AI recommending move " + str(move))
        return move
    