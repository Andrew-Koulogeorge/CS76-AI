import chess
from chess import BaseBoard, Piece
from math import inf


class AlphaBetaAITable():
    def __init__(self, max_depth=3, iterative_deepening=False):

        self.name = "AlphaBetaAITable"
        self.iterative_deepening = iterative_deepening
        self.total_states_seen = 0
        self.max_depth = max_depth

        self.t_table = {}

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
            self.t_table = {}
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
                self.t_table = {}
                
        return best_move_so_far
    

    """
    finds the best move at the current board position. Returns both the best action and its value
    """
    def mini_max(self,board, levels_to_go, maximize, alpha, beta):
        
        alpha_curr, beta_curr = alpha, beta
        self.total_states_seen +=1
        key = hash(str(board))

        # if we are at the max depth, lets cut off the search and return the value of h(n)
        if levels_to_go == 0 or board.is_checkmate() or board.is_stalemate():
            return self.evaluation_function(board), None
        
        if key in self.t_table:
            return self.t_table[key], None
                
        # if its whites turn to move, we want to max the value of the state we go to
        if maximize: 
            
            best_value = float('-inf')
            best_action = None

            # loop over all possible actions from this state and run min_value from those states
            for legal_move in list(board.legal_moves):
                
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
            for legal_move in list(board.legal_moves):
                
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
        
        self.t_table[key] = best_value
        return best_value, best_action

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
    
        
