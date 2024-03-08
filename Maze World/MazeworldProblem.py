from Maze import Maze
from time import sleep

class MazeworldProblem:

    ## you write the constructor, and whatever methods your astar function needs
    """
    Start state format --> A_i and A_i+1 represents the x a y cords of a robot and 
    the last element of the tuple represents which robots turn it is to move. 
    """

    def __init__(self, maze, goal_locations):
        self.num_robots = (len(maze.robotloc))//2
        start = maze.robotloc # grab list of robot locations from the maze object
        start.append(0) # last element of start locations represents which robots turn it is to move. init = 0

        self.start_state = tuple(start)
        self.goal_state = goal_locations
        self.maze = maze
  
    def __str__(self):
        string =  "Mazeworld problem: "
        return string
        # given a sequence of states (including robot turn), modify the maze and print it out.
        # (Be careful, this does modify the maze!)
    

    """
    Given a state in the problem, return possible legal states from the exisiting state
    """
    def get_successors(self,current_state):
        # going to return next states which are legal 
        neighbors = []
        direction_tracker = []

        ### THINK ABOUT THIS MORE LATER ###
        # for now, going to compute a set containing the locations of the robots on the fly. 

        robot_locations = set()

        for i in range(0,len(current_state)-1,2):
            robot_locations.add((current_state[i],current_state[i+1]))

        # which robots turn it is to move
        turn = current_state[-1]

        # grab the index in the current state array of where the robots locations are stored
        x_index, y_index = 2*turn, 2*turn + 1

        # get the location of the robot we are going to try and move.
        moving_robot_loc_x, moving_robot_loc_y  = current_state[x_index],current_state[y_index]

        # left,right,up,down
        directions = [("left",-1,0),("right",1,0),("up",0,1),("down",0,-1)]

        for direction,dx,dy in directions:
            # move robot to this location
            new_x,new_y = moving_robot_loc_x + dx, moving_robot_loc_y + dy

            # check and see if this new location is (1) in bounds (2) doesnt go into a wall (3) doesnt land on another robot
            if self.in_bounds(new_x,new_y) and self.maze.is_floor(new_x,new_y) and (new_x,new_y) not in robot_locations:
                # make a new possible state
                new_state = list(current_state) # all ints in the current_state so a shallow copy should be ok
                new_state[-1] = (turn + 1) % self.num_robots # move onto the next robot's turn
                new_state[x_index],new_state[y_index] = new_x,new_y # update the current robots location

                # add new possible state 
                neighbors.append(tuple(new_state))
                direction_tracker.append(direction)
        
        # you know that the "stay still" option will always result in a legal state! All we have to do is increase the robots turn
        stay_still = list(current_state)
        stay_still[-1] = (turn + 1) % self.num_robots

        neighbors.append(tuple(stay_still))
        direction_tracker.append("Pause")

        
        return direction_tracker,neighbors
    
    def in_bounds(self,x,y):
        return 0 <= x < self.maze.width and 0 <= y < self.maze.height

    def is_goal(self,state):
        # is the state (not including which robots turn it is to move) at the goal state?
        return state[:-1] == self.goal_state
    
    """
    Want to implement the functionality that if the state did not change, we dont print it out
    """
    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state[:-1])
        last_state = (0)*len(self.maze.robotloc)

        for state in path:
            if state[:-1] == last_state: continue # dont want to repeat the print out of a state if nothing happened
            self.maze.robotloc = tuple(state[:-1]) # updating the location of the robots that the maze is storing
            sleep(1)

            print(str(self.maze)) # print the new maze with the updated robot locations
            last_state = self.maze.robotloc
        print("Winner!")


## A bit of test code. You might want to add to it to verify that things
#  work as expected.

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")

    print(test_maze3)

    test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))

    print(test_mp.get_successors((1, 0, 1, 1, 2, 1, 1))) # works !!
    print(test_mp.get_successors((1, 0, 1, 1, 2, 1, 2))) # works !!

    print(test_mp.fuel_heuristic((0, 1, 0, 1, 2, 2, 1))) 
    print(test_mp.fuel_heuristic((1, 4, 1, 3, 1, 2))) 
