from Maze import Maze
from time import sleep

class SensorlessProblem:

    
    """
    No initial state that we need to worry because the robot does not know where it is. Start state will always be the same
    Need to worry about the final state to know if we have got to where we need to go
    Need the maze object to know about walls and when we are out of bounds
    """
    def __init__(self,maze, goal_location):
        # build all possible starting states for the blind robot in the maze. set containing tuples!
        init_state = set()
        for i in range(maze.width): # height is num rows
            for j in range(maze.height): # width is num cols
                if maze.is_floor(i,j): init_state.add((i,j))

        self.start_location = tuple(maze.robotloc) # where the blind robot starts in the maze

        self.start_state = frozenset(init_state)
        self.maze = maze
        self.goal_state = goal_location


    """
    State is represented as a set of tuples (x,y) that represent possible locations that the robot could be in
    """
    def get_successors(self,state): # state is a frozen set of possible locations we could be on the grid
        next_states = [] # set that will contain the next states (which are also frozensets!)
        direction_tracker = [] # keeping track of the direction traveled to get to the next state

        directions = [("left",-1,0),("right",1,0),("up",0,1),("down",0,-1)]
            

        for direction, dx,dy in directions:
            next_state = set()
            for x,y in state:
                new_x, new_y = dx + x, dy + y
                if self.maze.is_floor(new_x, new_y) and self.in_bounds(new_x,new_y): 
                    next_state.add((new_x,new_y))
                else: 
                    next_state.add((x,y))

            next_states.append(frozenset(next_state))
            direction_tracker.append(direction) 
        
        return direction_tracker, next_states

    def in_bounds(self,x,y):
        return 0 <= x < self.maze.width and 0 <= y < self.maze.height
    
    """
    Have found the goal if the robot knows that its on the goal! (only state in set)
    """
    def is_goal(self,frozen_set_state):
        # want to get the tuple state out of the frozen set 
        if len(frozen_set_state) == 1:
            mutable_set = set(frozen_set_state)
            return mutable_set.pop() == self.goal_state


    def __str__(self):
        string =  "Blind robot problem: "
        return string


        # given a sequence of states (including robot turn), modify the maze and print it out.
        # (Be careful, this does modify the maze!)

    def animate_path(self, path):
        r_x,r_y = self.start_location # starts out with its init state
        print("Start:\n")
        for direction in path:

            if direction != "Start": print(f"Try {direction}!\n")

            if direction == "up" and self.in_bounds(r_x,r_y + 1) and self.maze.is_floor(r_x,r_y + 1):
                r_x,r_y = r_x,r_y + 1
            
            if direction == "down" and self.in_bounds(r_x,r_y - 1) and self.maze.is_floor(r_x,r_y - 1):
                r_x,r_y = r_x,r_y - 1
            
            if direction == "left" and self.in_bounds(r_x-1,r_y) and self.maze.is_floor(r_x-1,r_y):
                r_x,r_y = r_x-1,r_y 
            
            if direction == "right" and self.in_bounds(r_x+1,r_y) and self.maze.is_floor(r_x+1,r_y):
                r_x,r_y = r_x+1,r_y
            
            self.maze.robotloc = (r_x,r_y)
            print(str(self.maze))
            sleep(1)
        print("Yay!")



## A bit of test code

if __name__ == "__main__":

    blind_test_maze1 = Maze("maze3_blind.maz")
    test_problem = SensorlessProblem(blind_test_maze1,(3,0))
    print(test_problem.start_state)



    # print(test_problem.start_state) correct!
    # print(test_problem.get_successors(test_problem.start_state)) correct!

    # blind_test_maze3 = Maze("maze3_blind.maz")
    # test_problem = SensorlessProblem(blind_test_maze3,(2,5))

    # print(test_problem.get_successors(test_problem.start_state))
