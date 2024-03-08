import chess
from chess import BaseBoard, Piece
from math import inf


class AlphaBetaAIOrdering():
    def __init__(self, max_depth=3, iterative_deepening=False):

        self.name = "AlphaBetaAIOrdering"
        self.iterative_deepening = iterative_deepening
        self.total_states_seen = 0
        self.max_depth = max_depth

        self.material_value = {
            "P": 1, # Pawn
            "p": 1,
            "N": 3, # Knight
            "n": 3, 
            "B": 3, # Bishop
            "b": 3, 
            "R": 5, # Rook
            "r": 5, 
            "Q": 9, # Queen
            "q": 9, 
            "K": 100, # King
            "k": 100 
            }


    def choose_move(self, board, white_to_move):

        if not self.iterative_deepening:

            _, best_move_so_far = self.mini_max(board, self.max_depth, maximize=white_to_move, alpha=-inf, beta=inf)
            print(f"{self.name} Made {self.total_states_seen} calls to minimax to find the move {best_move_so_far} while searching to a depth of {self.max_depth} \n")
            self.total_states_seen = 0
        else:
            # run mini_max search at various depth levels
            _, best_move_so_far = 0, None
            global_visited = 0
            for depth in range(1, self.max_depth+1):

                _, move = self.mini_max(board, depth, maximize=white_to_move, alpha=-inf, beta=inf)
                global_visited += self.total_states_seen

                if not best_move_so_far:
                    best_move_so_far = move
                    print(f"Picked our first move : {best_move_so_far} \n")

                elif best_move_so_far != move:
                    print(f"Found a new move! Now the AI bot wants to move {move} instead of {best_move_so_far}\n")
                    best_move_so_far = move
                
                else:
                    print(f"We are staying with our current best move {best_move_so_far}\n")
                
                print(f"{self.name} Made {self.total_states_seen} moves to find the move {best_move_so_far} while searching to a depth of {depth}\n")

                self.total_states_seen = 0
                
        return best_move_so_far
    

    """
    finds the best move at the current board position. Returns both the best action and its value
    """
    def mini_max(self,board, levels_to_go, maximize, alpha, beta):
        alpha_curr, beta_curr = alpha, beta
        self.total_states_seen +=1

        # if we are at the max depth, lets cut off the search and return the value of h(n)
        if levels_to_go == 0 or board.is_checkmate() or board.is_stalemate():
            return self.evaluation_function(board), None
        
        # first, we want to order the next possible states with the "best" states for the max player first
        sorted_actions = self.order_moves(board)

        # if its whites turn to move, we want to max the value of the state we go to
        if maximize: 
            
            best_value = float('-inf')
            best_action = None

            sorted_actions = self.order_moves(board)

            # loop over all possible actions from this state and run min_value from those states
            for legal_move in sorted_actions:
                
                # make this move on the board  
                board.push(legal_move)

                curr_value, _ = self.mini_max(board, levels_to_go-1, maximize=False, alpha=alpha_curr, beta=beta_curr)

                if curr_value > best_value:
                    best_value, best_action = curr_value, legal_move
                    alpha_curr = max(alpha_curr, best_value)
                
                if best_value >= beta_curr:
                    board.pop() 
                    return best_value, best_action

                # want to undo the move we just did before we try out other legal moves from this position
                board.pop()
        else:
            
            best_value = float('inf')
            best_action = None

            # otherwise, loop over all possible actions from this state and run min_value from those states
            for legal_move in reversed(sorted_actions):
                
                # make this move on the board  
                board.push(legal_move)

                curr_value, _ = self.mini_max(board, levels_to_go-1, maximize=True, alpha=alpha_curr, beta=beta_curr)

                if curr_value < best_value:
                    best_value, best_action = curr_value, legal_move
                    beta_curr = min(beta_curr, best_value)

                if best_value <= alpha_curr:
                    board.pop() 
                    return best_value, best_action
                    
                # want to undo the move we just did before we try out other legal moves from this position
                board.pop()

        return best_value, best_action


    """
    Given a current board position, we want to consider all possible board position and order the positions in terms of the evaluation function
    For example, for the player trying to maximize his score (white) will want to have the largest states first and black the smallest states first.
    This helps the alpha beta pruning illiminate more branches!
    
    """
    def order_moves(self, board):
        # get the list of possible actions
        sorted_actions = []

        for legal_move in list(board.legal_moves):

            # for each legal move, first we need to get what the board would look like if we made that move
            board.push(legal_move)

            h = self.evaluation_function(board)
            sorted_actions.append((h,legal_move))

            # clean the board of this attempt
            board.pop()
        
        # print(f"these are all legal moves not sorted: {sorted_actions}")

        # sorting list of tuples in python does it by fault by the first entry which is the value of the evaluation
        sorted_actions.sort(reverse=True, key=lambda x: x[0]) 

        # print(f"Here they are if they are sorted: {sorted_actions}")

        # sorted_actions.reverse()
        # print(f"Here is the order we look at the peices if we are doing it from the POV of min: {sorted_actions}")
        return [x[1] for x in sorted_actions] # returning legal moves sorted in order




    def evaluation_function(self,board):
        # if we are at a terminal state, see whose turn it is and return terminal value. Terminal value much higher than sum of parts!
        if board.is_checkmate():
            if board.outcome().winner == chess.WHITE: 
                return 1000
            else:
                return -1000
        
        if board.is_stalemate():
            return 0

        # loop over the board and collect all of the material that is white and black in different lists
        white_val = black_val = 0

        # squares of the board are represented as [0-63]
        for square in chess.SQUARES:
            if board.piece_at(square):

                piece_symbol = Piece.symbol(board.piece_at(square))

                if piece_symbol.isupper(): # WHITE is uppercase 
                    white_val += self.material_value[piece_symbol]
                else:
                    black_val += self.material_value[piece_symbol]
        
        return white_val - black_val
    

if __name__ == "__main__":
        pass
        ai = AlphaBetaAIOrdering()

        # Ruy-Lopez opening
        Ruy_Lopez = "r1bqkb1r/pppp1ppp/2n2n2/4p3/B3P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 5"
        white_to_avoid_mate = "rnb1kbnr/ppp1pppp/8/2p5/4Pq2/5P2/PPPPR1PP/1NBQKBNR"
  
        board = chess.Board(fen=white_to_avoid_mate)
        print(board)
