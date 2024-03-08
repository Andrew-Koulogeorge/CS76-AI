import chess
from chess import BaseBoard, Piece
# white is trying to max, black is trying to min!
class MinimaxAI():
    def __init__(self, max_depth=3, iterative_deepening=False):

        self.name = "MinimaxAI"
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
            _, best_move_so_far = self.mini_max(board, self.max_depth, maximize=white_to_move)
            print(f"{self.name} Made {self.total_states_seen} calls to minimax to find the move {best_move_so_far} while searching to a depth of {self.max_depth} \n")
            self.total_states_seen = 0
        else:
            # run mini_max search at various depth levels
            _, best_move_so_far = 0, None
            global_visited = 0
            for depth in range(1, self.max_depth+1):
                _, move = self.mini_max(board, depth, maximize=white_to_move)
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
    def mini_max(self,board,levels_to_go, maximize):
        self.total_states_seen +=1

        # if we are at the max depth or we have reached a terminal state (a win or a draw), lets cut off the search and return the value of h(n)
        if levels_to_go == 0 or board.is_checkmate() or board.is_stalemate():
            return self.evaluation_function(board), None
                
        # if its whites turn to move, we want to max the value of the state we go to
        if maximize: 
            
            best_value = float('-inf')
            best_action = None

            # loop over all possible actions from this state and run min_value from those states
            for legal_move in list(board.legal_moves):
                
                # make this move on the board  
                board.push(legal_move)

                curr_value, _ = self.mini_max(board,levels_to_go-1,maximize=False)

                if curr_value > best_value:
                    best_value = curr_value
                    best_action = legal_move
                
                # want to undo the move we just did before we try out other legal moves from this position
                board.pop()
        else:
            
            best_value = float('inf')
            best_action = None

            # otherwise, loop over all possible actions from this state and run min_value from those states
            for legal_move in list(board.legal_moves):
                
                # make this move on the board  
                board.push(legal_move)

                curr_value, _ = self.mini_max(board,levels_to_go-1,maximize=True)

                if curr_value < best_value:
                    best_value = curr_value
                    best_action = legal_move
                    
                # want to undo the move we just did before we try out other legal moves from this position
                board.pop()

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




def test_evaluation_function(AI):
    board1 = chess.Board()
    board2 = chess.Board()
    board3 = chess.Board()
    board2.remove_piece_at(4)
    board3.remove_piece_at(63)

    print(f"Starting spots should have equal material so this should be zero! {AI.evaluation_function(board1)} \n")
    print(f"Without the white king, black should be winning by 100!: {AI.evaluation_function(board2)}\n")
    print(f"Taking away blacks rook, white should be up 5: {AI.evaluation_function(board3)}\n")


if __name__ == "__main__":
    minimax_ai = MinimaxAI()
    test_board = chess.Board()
    """
    print(test_board)
    print(" _______________________ \n")

    move = list(test_board.legal_moves)[0] # each element of move_list is of type Move
    test_board.push(move)
    print(test_board)

    test_board.pop()
    print(" _______________________ \n") # can push and pop moves to change positions around 
    print(test_board)

    # test_evaluation_function(minimax_ai)
    """