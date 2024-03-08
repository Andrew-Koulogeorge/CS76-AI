from MazeworldProblem import MazeworldProblem
from Maze import Maze

from astar_search import astar_search

"""
Cost function for the multi robot problem.
A robot expends one unit of fuel if it moves, and no fuel if it waits a turn
Given two nodes, return 1 if a robot moved from the parent to the state and return 0 otherwise.
"""
def fuel_changed_state(state,parent):
    for x,y in zip(state[:-1],parent[:-1]):
        if x != y: return True
    return False

# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(state,goal):
    return 0

"""
Given a state in the problem and the goal state, return estimated cost from current state to the goal state
"""
def fuel_heuristic(current_state,goal_state):

    ### Estimate the fuel cost from the current state to the goal state to be the sum of the L1 distances for each of the robots to its goal state.
    h_current_state = 0

    for i in range(0,len(current_state)-1,2):
        # grab robot's current x and y location along with its goal location
        r_x,r_y = current_state[i],current_state[i+1]
        g_x,g_y = goal_state[i],goal_state[i+1]

        # compute the L1 distance between robot's current location and its goal location
        h_current_state += L1(r_x,r_y,g_x,g_y)
    
    return h_current_state


def L1(x_1,y_1,x_2,y_2):
    return abs(x_1-x_2) + abs(y_1-y_2)

def tester(maze_path,goal_locations, cost_fn=fuel_changed_state,h_n=fuel_heuristic):

    test_maze2 = Maze(maze_path)
    test_mp2 = MazeworldProblem(maze=test_maze2, goal_locations=goal_locations)

    result2 = astar_search(test_mp2, cost_fn, h_n)
    print(result2)
    test_mp2.animate_path(result2.path) # path contains states of the problem!

if __name__ == "__main__":
    # tester("maze1.maz",(1, 1, 1, 0, 2, 1))
    # tester("maze2.maz",(1, 0, 1, 1, 2, 1))
    # tester("maze3.maz",(2, 5, 2, 3, 2, 0))
    # tester("maze4.maz", (8, 5, 8, 0, 1, 5, 1, 0)) # slow, but it gets there. Would want to experiment with trying a different h(n) if more time was allocated.
    # tester("maze5.maz", (39,39)) # dont feel bad cutting the animation short, it takes a while

    pass

