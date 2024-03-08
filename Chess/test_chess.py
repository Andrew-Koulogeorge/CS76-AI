# pip3 install python-chess

import chess
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from AlphaBetaAIOrdering import AlphaBetaAIOrdering
from ChessGame import ChessGame
from AlphaBetaAITable import AlphaBetaAITable
from AlphaBetaAI_all import AlphaBetaAI_all

import sys

""""
white and black are the AI chess classes!
"""
def tester(white, black, custom_to_move = chess.WHITE, custom_start_board = False, white_max_depth=3, white_deepening=False, black_max_depth=3, black_deepening=False):
    
    player1 = white(white_max_depth, white_deepening)
    player2 = black(black_max_depth, black_deepening)

    game = ChessGame(player1, player2)

    if custom_start_board: 
        game.board = chess.Board(fen=custom_start_board)
        game.board.turn = custom_to_move
   


    while not game.is_game_over():
        print(game)
        game.make_move()

    print(game)
    outcome = game.board.outcome()
    print(outcome.result())

if __name__ == "__main__":
    # get all types of AI with the different features for easy comparison
    me = HumanPlayer
    standard = MinimaxAI
    alpha_beta = AlphaBetaAI
    ordering = AlphaBetaAIOrdering 
    table = AlphaBetaAITable 
    kitchen_sink = AlphaBetaAI_all 
    
    # Website Used to generate custom boards : http://www.netreal.de/Forsyth-Edwards-Notation/index.php

    ### MINIMAX AND CUTOFF TESTS --> Experimenting with the depth 

    #tester(me, standard, black_max_depth=1)
    #tester(me, standard, black_max_depth=2)
    #tester(me, standard, black_max_depth=3)
    #tester(me, standard, black_max_depth=4) # takes a long time even to generate the first move!
    #tester(me, standard, black_max_depth=5) # takes a LONG time even to generate the first move!


    ### LOOKING FOR INTELLEGENCE ### 
    # CASE 1 --> AI is greedy with only 1 depth 
    # greedy_ai = "rnbqkb1r/pppppppp/7n/8/4P1P1/8/PPPP1P1P/RNBQKBNR"
    # to_move = chess.BLACK
    # tester(white=me, custom_to_move = to_move, custom_start_board = greedy_ai, black = standard, black_max_depth=1)

    # CASE 2 --> AI with an ability to look a little bit more ahead if able to see that its not a good idea!
    #tester(white=me, custom_to_move = to_move, custom_start_board = greedy_ai, black = standard, black_max_depth=3)

    # CASE 3 --> AI Takes easy checkmate in 1
    # mate_in_1 = "rnb1kbnr/ppp1pppp/8/2p5/4Pq2/P4P2/PPPPB2P/RN1QKBNR"
    # to_move = chess.BLACK
    # tester(white=me, custom_to_move = to_move, custom_start_board = mate_in_1, black = standard, black_max_depth=3, black_deepening=False)

    ### ITERATIVE DEEPENING ### 
    # Iterative deepening shows the chess AI making a calculation and changing its mind as it looks deeper in the tree for the best move.
    # thinker = "rnbqkbr1/pppppp1p/7n/8/3PPPPp/8/PPP5/RNBQKBNR"
    # to_move = chess.BLACK
    # tester(white=me, custom_to_move = to_move, custom_start_board = thinker, black = standard, black_max_depth=3, black_deepening=True)
    
    ### Alpha-Beta Pruning & Move-Reordering ### 
    # tester(me, alpha_beta, black_max_depth=5) # super fast
    # tester(me, alpha_beta, black_max_depth=6)  # around the same time as it takes standard to do 4
    # tester(me, alpha_beta, black_max_depth=7) # takes a LONG time even to generate the first move!

    # Ensuring that minimax is outplaying alpha-beta
    # random_pos = "r1bq1rk1/ppp1ppbp/2np1n2/1B4p1/4P3/2NP1NP1/PPP1QP1P/R1B2RK1"
    # to_move = chess.BLACK
    
    # SAME OUTPUT W SAME DEPTH --\
    # tester(me, standard, custom_to_move = to_move, custom_start_board = random_pos, black_max_depth=3) 
    # tester(me, alpha_beta, custom_to_move = to_move, custom_start_board = random_pos, black_max_depth=3, black_deepening=True)

    # Alpha Beta GETS A STRONGER OUTPUT W LARGER DEPTH --\
    # tester(me, alpha_beta, custom_to_move = to_move, custom_start_board = random_pos, black_max_depth=6, black_deepening=True)

    # Alpha Beta WITH ORDERING has to check many fewer states than just the standard algo --\
    # tester(white=me, black = ordering, custom_to_move = to_move, custom_start_board = random_pos, black_max_depth=6, black_deepening=True)

    ### Transposition table ### 
    random_pos2 = "rkr5/p3ppbp/1pnp1n2/q1p3B1/BP1PP1b1/P1P2NP1/3NQP1P/R1KR4"
    to_move = chess.BLACK
    #tester(white=me, black = alpha_beta, custom_to_move = to_move, custom_start_board = random_pos2, black_max_depth=5, black_deepening=True)
    tester(white=me, black = table, custom_to_move = to_move, custom_start_board = random_pos2, black_max_depth=5, black_deepening=True)



    #tester(white=me, black = standard, black_max_depth=3, black_deepening=True)

    # tester(white=me, white_max_depth=5, white_deepening=True, black = kitchen_sink, black_max_depth=5, black_deepening=True)