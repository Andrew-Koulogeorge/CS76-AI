from Maze import Maze
from collections import deque
from MazeworldProblem import MazeworldProblem
from SensorlessProblem import SensorlessProblem
from astar_search import astar_search
from test_mazeworld import fuel_changed_state,fuel_heuristic,L1

""""
Given the Maze object, we first want to make an array that represents the game.
"""
class PolynomialSolution:

    def __init__(self,maze,goal_location):
        self.maze = maze
        self.nrows, self.ncols = maze.height,maze.width
        self.maze_array = [["#" for _ in range(self.ncols)] for _ in range(self.nrows)]
        self.X = (0,self.ncols-1)
        
        for x in range(self.nrows):
            for y in range(self.ncols):
                if self.maze.is_floor(y,x): self.maze_array[x][y] = "."
        
        self.bfs()
        self.guide_to_sight()
        self.go_to_goal(goal_location)
        self.master_guide_for_blind_robot = self.guide_to_X + self.guide_to_goal

    def in_range(self,x,y):
        return 0 <= x < self.nrows and 0 <= y < self.ncols

    def bfs(self):
        queue = deque()
        seen = set()

        queue.append(self.X)
        seen.add(self.X)

        directions = [(0,1),(1,0),(-1,0),(0,-1)]
        self.maze_array[0][self.ncols-1] = 0 # distance to the bottom right is nothing becuase this is our goal state

        # Do BFS from this node to every other node in the matrix
        while queue:
            x,y = queue.popleft()
            prev_cost = self.maze_array[x][y]

            for dx,dy in directions:
                new_x,new_y = x + dx, y + dy
                loc = (new_x,new_y)
                if loc not in seen and self.in_range(new_x,new_y) and self.maze.is_floor(new_y,new_x):
                    seen.add(loc)
                    queue.append(loc)
                    self.maze_array[new_x][new_y] = prev_cost + 1
        self.heat_map = self.maze_array
                    
    def gradient_decent(self,start_point):
        # loop over every element in the heat map and take the step in the direction of the steepest decent
        x,y = start_point
        if not self.maze.is_floor(y,x): return "Not a legal starting state"

        directions = [("right",0,1),("up",1,0),("down",-1,0),("left",0,-1)]
        curr_cost = self.heat_map[x][y]
        compass = []
        while curr_cost:
            for direction,dx,dy in directions:
                new_x,new_y = x + dx, y + dy
                if self.in_range(new_x,new_y) and self.maze.is_floor(new_y,new_x) and self.heat_map[new_x][new_y] < curr_cost:
                    compass.append(direction)
                    curr_cost = self.heat_map[new_x][new_y]
                    x,y = new_x,new_y
                    break
        return compass

    def guide_to_sight(self):
        master = []
        for x in range(self.nrows):
            for y in range(self.ncols):
                if self.maze.is_floor(y,x):
                    path = self.gradient_decent((x,y))
                    master.extend(path)
        self.guide_to_X = master
    
    """
    Once we our state space has been reduced to just a single element, we can now run A* search from this point to the goal node.
    We will make an instance of the A* search problem and set the position of the robot to start to be at location X. We will then get the 
    """
    def go_to_goal(self,goal_location):
        # make an instance of the problem
        seeing_robot = MazeworldProblem(self.maze,goal_location)
        start_x, start_y = self.X[1], self.X[0]
        seeing_robot.start_state = (start_x,start_y,0)

        self.solution = astar_search(seeing_robot,fuel_changed_state,fuel_heuristic)
        self.guide_to_goal = self.solution.directions[1:]

def tester(maze_path, goal):
    poly = PolynomialSolution(Maze(maze_path),goal)
    animator = SensorlessProblem(Maze(maze_path),goal)
    print(f"Here are the moves the robot took to ensure that it knew where it was in the maze. It took {len(poly.guide_to_X)} moves: {poly.guide_to_X}")
    print(f"Here are the moves the robot took to get to the goal once it knew if was at the solutuion! It took {len(poly.guide_to_goal)} moves: {poly.guide_to_goal}")

    animator.animate_path(poly.master_guide_for_blind_robot) # uncomment this if you want to see the animation

if __name__ == "__main__":
    maze1 = "maze1_blind.maz"
    goal1 = (1,0)

    maze2 = "maze3.5_blind.maz"
    goal2 = (2,5)

    maze4 = "maze4_blind.maz" 
    goal4 = (8,5)

    maze5 = "maze5_blind.maz" 
    goal5 = (15,7)
   
    # tester(maze1,goal1)
    # tester(maze2,goal2)
    # tester(maze4,goal4) #this is going to run visualize!!!!!!!! but, we found a path very quickly. the path itself is not so quick...
    # tester(maze5,goal5) #this is going to run visualize!!!!!!!! but, we found a path very quickly. the path itself is not so quick...