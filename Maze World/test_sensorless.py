from SensorlessProblem import SensorlessProblem
from Maze import Maze

from astar_search import astar_search

"""
Cost function for the blind robot problem.
Treating the cost of the search to be the number of moves that the robot has to make in order to find the goal state. Even if its up against a wall and its not moving, it still takes the blind robot time to figure it out
"""
def time_cost(state,parent):
    return 1

# want to be following paths that reduce the search space as much as possible. once we know where we are, we can find the goal!
def cardinality_heuristic(state,goal):
    return len(state)

def L1(x_1,y_1,x_2,y_2):
    return abs(x_1-x_2) + abs(y_1-y_2)

def card_and_closeness_heuristic(state,goal):
    card = len(state)

    # want to loop over all of the goast robots and compute the distance between all of them
    states = list(state)
    dist = 0
    for i in range(len(states)):
        for j in range(i+1,len(states)):
            dist += L1(states[i][0],states[i][1],states[j][0],states[j][1])
    
    return dist + card

def closeness_heuristic(state,goal):
    # want to loop over all of the goast robots and compute the distance between all of them
    states = list(state)
    dist = 0
    for i in range(len(states)):
        for j in range(i+1,len(states)):
            dist += L1(states[i][0],states[i][1],states[j][0],states[j][1])
    
    return dist 


# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(state,goal):
    return 0

def tester(maze_path,goal_locations, cost_fn=time_cost,h_n=cardinality_heuristic):

    test_maze2 = Maze(maze_path)
    test_mp2 = SensorlessProblem(maze=test_maze2, goal_location=goal_locations)

    print(test_mp2.start_location)

    result2 = astar_search(test_mp2, cost_fn, h_n)
    print(result2)
    test_mp2.animate_path(result2.directions) # directions contains the direction in which we need to turn to get to the goal state


if __name__ == "__main__":
    # tester("maze1_blind.maz",(1,0)) # winner!
    # tester("maze1_blind.maz",(3,0),h_n=card_and_closeness_heuristic) # very fast winner!


    # tester("maze3_blind.maz",(2,5)) # winner!
    # tester("maze3_blind.maz",(2,5),h_n=card_and_closeness_heuristic) # very fast winner!

    
    # tester("maze3.5_blind.maz",(2, 5)) # winner!
    # tester("maze3.5_blind.maz",(2, 5),h_n=card_and_closeness_heuristic) # very fast winner!

    # tester("maze4_blind.maz", (1,5)) # winner!
    # tester("maze4_blind.maz", (1,5),h_n=card_and_closeness_heuristic) # very fast winner!

    # tester("maze4_blind.maz", (8,5)) # winner!
    # tester("maze4_blind.maz", (8,5), h_n=card_and_closeness_heuristic) # very fast winner!

    # ## SEE THIS TEST CASE FOR HOW GREAT OUR h(n) is!
    # tester("maze5_blind.maz", (15,7), h_n=card_and_closeness_heuristic) # very fast!!
    # tester("maze5_blind.maz", (15,7), h_n=closeness_heuristic) # very fast!!

    # tester("maze5_blind.maz", (15,7)) # CANT SOLVE !!! Not clever enough when only considering the cardinality of the set
    pass
