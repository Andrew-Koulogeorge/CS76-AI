# using shapely for collision detection
"""
   ---> RRT
    - Many systems where its not so obvious how to connect points in the config space.

    Car has a config (x,y,theta) for its location and angle with the horizontal. Assume 6 actions (Simulation written already)

    Vorney Diagram: Partition the space into regions (dont compute it)

    Grow the tree of states. Pick a random point in the config space uniformly at random to begin with. Find the vertex on the tree closest to the point 
    using nearest neighbor. That state is the one that we pick to keep growing. By taking the nearest neighbor, picking the V region that is large

    Check if a point is legal and add it. Its a tree so we backchain once we get to the goal

    Method is only approximate. will get you e close to the goal 

    Distance --> multiple some constant k by theta
"""


from shapely.geometry import Polygon, Point
from collections import defaultdict

poly = Polygon(((0, 0), (0, 1), (1, 1), (1, 0)))
point = Point(2, .2)

print(poly)
print(poly.contains(point))

class RRT:


    def __init__(self) -> None:
        
        # Adj list thats going to store the tree we create
        tree = defaultdict(list)


    def rrt(self, starting_config: tuple, goal_config: tuple, num_nodes: int, delta: int, ):
        
        node_counter = 0

        # outer loop tells us how many points we have sampled and connected to our graph
        while node_counter < num_nodes:
            
            # randomly generate a point in our c space of (x,y, theta)




            pass
