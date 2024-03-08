import chess

class HumanPlayer():
    def __init__(self, max_depth=3, iterative_deepening=False):
        print("Moves can be entered using four characters. For example, d2d4 moves the piece "
              "at d2 to d4.")
        pass

    def choose_move(self, board, white_to_move): # placeholder
        moves = list(board.legal_moves) # board objects has a IV that holds legal moves from a loc

        uci_move = None

        while not uci_move in moves: # while we have not found a legal move
            print("Please enter your move: ")
            human_move = input() # move for the human player chosen by the users command line

            try:
                uci_move = chess.Move.from_uci(human_move)
            except:
                # illegal move format
                uci_move = None

            if uci_move not in moves:
                print("  That is not a legal move!")

        return uci_move

