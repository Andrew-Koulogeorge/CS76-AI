from collections import defaultdict
from collections import deque
from Kinematics import *
from drawing import *
import random
from math import pi, pow, sqrt
import annoy
import numpy as np
import time

"""
Class for the Probabilistic Roadmap algorithm which will be used to find a path in the configuration space so that the robot can get to its goal 

 Roadmap generation: 
    - Create the graph by sampling points in the configuration space
    - Method to translate the point in the configuration space to a point in the physical space, and then check if this 
    arm configuration intersects with any obstacles (functions in Kinematics).
    - Local Planner function which attempts to make connections between other existing points in the config space.
        - If we store the graph as a dictonary, at each sample we can loop over all the nodes in the graph and sort that array by the distance from
        the point to the sample. We can then loop over this list in order of points closest to the sample and try and make a linesegment between them.
        If this linesegment is legal, then we add the connection sample --> node, node --> sample to our default dict map and decrease our count. We
        Do this until we either run out of points or we make k connections. 

    -? Keep the graph represented as dictonary? Are we going to store this graph in memory? A: Yes, we are
    node --> [neighborhood]
    -? How fine do we need to sample these points. A: Just sample using random from 0-2pi

    ____ROADMAP_____

    -Visibility graph does not extend well at all to higher dim. Works nice for 2D. Plus, obstacles not polygons in obstacle space.
    -Exact cell decomposotion --> Same problem is that the configuration space obstacles are not polygons. 

    What do people actually do? PRM and RRT.

    ---> PRM
    - Sample the space. Pick each of the variables at random between [0,2pi]
    - For each sample, check if its in a boundary or not. For the configuration, create the lines and then check if they collide with the shapes.
        Brute force just loop over
    - Start and End states are only used for query.
    - Assume that we sample all the points at once. Really expensive to connect to all other verticies. We can pick the KNN of a vertex (maybe 5)
    WATCH OUT for the topology of the search space. Want to get the shorest path between two points. 
    - Need to connect them. Steering method. Check between the two lines for collision. Need to check wrapping around on the torus.
    - If two points are close enough, hopefully the path between them is also legal. 
    - Most basic way is to only connect an edge if it is "short enough". Could also check a point inbetween

  
"""

class KNN():

    def __init__(self, data_points):
        self.data_list = data_points
        self.dimension = data_points.shape[1]
        self.vectors = data_points.astype('float32') 

   
    def build(self, number_of_trees=1):

        self.index = annoy.AnnoyIndex(self.dimension, metric='euclidean')

        for i, vec in enumerate(self.vectors):
            self.index.add_item(i, list(vec))

        self.index.build(number_of_trees)
        
    def query(self, vector, num_neighbors=10, distances=False):

        indices = self.index.get_nns_by_vector(vector=vector.tolist(), n=k, include_distances=distances)                                           
        
        data_points = [tuple(self.data_list[i]) for i in indices]

        return data_points


class Planner:

    def __init__(self, start_config: tuple, goal_config: tuple, R:int, lengths: list, 
                 obstacles: list, k=10, num_samples=15000, epsilon=0.1, nn=True, knn_tree_number=1) -> None:
        """
        - R is the number of DoF for our robot
        """

        assert R == len(lengths), "Make sure you are sending in the right number of lengths and DoF!"

        self.nn = nn
        self.length = lengths
        self.R = R
        self.start_config = start_config
        self.goal_config = goal_config

        # we want to be epsilon close to the final solution
        self.epison = epsilon

        # going to store the graph explicitly in memory
        self.road_map = defaultdict(list) 

        # store the obstacles globally so we dont need to recompute on the fly
        self.shapely_obstacles = convert_shapely_obstacles(obstacles)

        # sample random points in the c space (nodes in the roadmap graph)
        print(f"Getting the samples in the c space...")
        self.sample_points(num_samples)
        print(f"Done \n")


        #### ADDING IN THE KNN FUNCTIONALITY SO WE CAN QUICKLY CONSIDER THE NEAREST POINTS AROUND ####
        self.nearest_neighbors = KNN(self.data_points)
        self.nearest_neighbors.build(number_of_trees=knn_tree_number)


        # create the outline for the graph we are going to search
        print(f"Constructing the edges of the graph...")
        self.create_edges(k)
        print(f"Done \n")

        # add the start and goal points to the graph and connect them with near by regions
        print(f"Adding the start and goal nodes and connections to the graph \n")
        self.include_query(k)
        print(f"Done \n")


    def sample_points(self, num_samples):
        """
        Randomly sample points from the configuration space. We are just going to sample all of the points at one time 
        - num_samples: how many numbers are we going to sample
        - R is the dimention of the points we are sampling 
        """

        # all_points = []
        for _ in range(num_samples):
            # randomly pick R points between [0,2pi]
            c_space_point = []
            for _ in range(self.R):

                c_space_point.append(random.uniform(0,2*pi))
            
            # compute what the endpoints look like in the physcial space
            endpoints = compute_endpoints(c_space_point, self.length)

            # get robot arms represented as shapely lines
            shapely_lines = convert_shapely_lines(endpoints)

            # check if this robot config is intersecting with the shapes
            if not collision(shapely_lines, self.shapely_obstacles):

                # if its not, add the point to the graph
                self.road_map[tuple(c_space_point)] = []
            else:
                # print(f"Found a collision with this point {c_space_point}")
                # all_points.append(c_space_point)
                pass
        
        self.data_points = np.array(list(self.road_map.keys()))
        
        ### THIS IS FOR TESTING ###
        # return all_points
    
    def create_edges(self, k):
        """
        Given points in the space that we have randomly sampled and a way to measure the shortest distance between the points in the space, we want to create edges between the points that are closest
        """

        # loop over each node in the graph
        nodes = list(self.road_map.keys())

        num_edges = 0
        for i in range(len(nodes)):


            # old functionality that loops over all of the points and sorts them by distance. instead, we want to make a 
            # query to the k nearest neighbors of our tree
            # we grab more than just k of the nearest points because maybe some of them are not legal! we want to still have k edges connected
            
            
            point1 = nodes[i]

            # USING KNN
            if self.nn:

                other_points = self.nearest_neighbors.query(np.array(nodes[i]), num_neighbors=2*k)
            
            # NOT USING KNN
            else:

                # i is the node we are considering connections for. Make a list for each i that contains other points on the graph as well as the distance between them
                other_points = []

                for j in range(len(nodes)):
                    if i != j:

                        dist_i_j = self.angular_distance(point1,nodes[j])
                        other_points.append((dist_i_j, nodes[j]))
                        
            
                # with a list of tuples, .sort() will sort in place based on the first element of the tuple
                other_points.sort()

                other_points = [x[1] for x in other_points]
            

            # connect the k closest points in our graph. for now, we assume that if both points are legal and they are the k closest to eachother, 
            # then all points in the line segment between them are also legal
            count = 0
            for nearest_point in other_points:

                # FUNCTIONALITY THAT CHECKS IF THE POINT INBETWEEN THESE TWO IS LEGAL. IF ITS NOT, MOVE TO NEXT ONE


                # we dont want to just take the midpoint. What we really want to do is check a certain number of points along the line between them
                # compute the array of distances between the two points. D = [qi-pi] where we have two points P and Q.
                # compute z points along this line between P and Q. do this by computing point X that lies inbetween P and Q
                # xi = pi +(qi-pi/)z where z ranges from Z to 2
                
                Z = 5

                # nearest_point and point1 live in R^DoF

                ###mid_point = []
                for cord1, cord2 in zip(point1,nearest_point):
                    pass
                    # mid_point.append((cord1 + cord2)/2)

                legal = False
                for z in range(Z,2,-1):
                    point_on_line = []

                    for cord1, cord2 in zip(point1,nearest_point):
                        point_on_line.append(cord1 + (cord2-cord1)/z)

                    point_on_line = tuple(point_on_line)
                ###mid_point = tuple(mid_point)


                        # check if the midpoint in the c space is a legal config
                    endpoints = compute_endpoints(point_on_line, self.length)

                    # get robot arms represented as shapely lines
                    shapely_lines = convert_shapely_lines(endpoints)

                    # check if this robot config is intersecting with the shapes
                    if collision(shapely_lines, self.shapely_obstacles):
                        #print(f"Found a connection at point {i} between two points in the c space at mid point number {z} that would have been illegal!")
                        legal = False
                        break
                    legal = True
                        
                if legal:
                    self.road_map[point1].append(nearest_point)
                    count += 1
                    num_edges += 1
                    #if num_edges % 10000 == 0: print(f"We just generated edge number: {num_edges}")


                if count >= k: break

                """
                # check if the midpoint in the c space is a legal config
                endpoints = compute_endpoints(mid_point, self.length)

                  # get robot arms represented as shapely lines
                shapely_lines = convert_shapely_lines(endpoints)

                # check if this robot config is intersecting with the shapes
                if not collision(shapely_lines, self.shapely_obstacles):

                    self.road_map[point1].append(nearest_point)
                    count += 1
                else:
                    print(f"Found a connection between two points in the c space that would have been illegal!")
                
                if count >= k: break
                """

    def include_query(self, k):
        """
        One way to could be smarter about this is consider more of the points to connect the start and the goal to?
        """
        
        nodes_to_add = [self.start_config, self.goal_config]
        nodes = list(self.road_map.keys())

        for i in [0,1]:
            other_points = []
            
            for j in range(len(nodes)):

                    dist_i_j = self.angular_distance(nodes_to_add[i],nodes[j])
                    other_points.append((dist_i_j, nodes[j]))
            
            # with a list of tuples, .sort() will sort in place based on the first element of the tuple
            other_points.sort()

            for nearest_point in range(20*k):
                self.road_map[nodes_to_add[i]].append(other_points[nearest_point][1])
        

    def angular_distance(self, c_space_point1, c_space_point2):
        """
        - Want to define a notion of distance between points in our c space so that we can connect points which are close
        - Because the c space is on a torus, we need to check which direction is closer to go towards
        - We are going to use a L2 distance in the c space between points
        """
        sum = 0
        for cord1, cord2 in zip(c_space_point1, c_space_point2):

            # determind which direction is the "shortest"
            D = abs(cord1-cord2)
            shorter_path = pow(min(D, 2*pi - D), 2)
            sum += shorter_path

        return sqrt(sum)


    def bfs(self):
        """
        Given the roadmap construced, lets now search the c space and look for the goal 
        Note that because of floating point, we are not going to be able to get exactly to the goal. We might be able to get close enough, however!
        Instead of checking if 
        """
        queue = deque()
        queue.append(self.start_config)
        
        visited = defaultdict()
        visited[self.start_config] = None

        print(f"Searching for a final configuration...")
        while queue:
            
            node = queue.popleft()

            for neighbor in self.road_map[node]:
                
                if neighbor not in visited.keys():
                    
                    visited[neighbor] = node
                    queue.append(neighbor)

                    if self.angular_distance(neighbor, self.goal_config) < self.epison:
                        shortest_path = self.backtrack(neighbor, visited)
                        print(f"Found! \n")
                        return shortest_path
        
        return None

    def backtrack(self, goal, visited):
        """
        Given the goal state and the visited backchaining dict, can reconstruct the path of nodes from the start state to the goal state
        """
        solution_path = [goal]
        prev = visited[goal]
        
        while prev:
            solution_path.append(prev)
            prev = visited[prev]
        
        solution_path.reverse()

        return solution_path


### TESTING FUNCTIONS ### 
def test_point_sampling(c_points, lengths):
    """
    Function that displays each of the physical representations of the points sampled in the c space! The screen goes red
    """

    for c_point in c_points:

        points, shapes, intersection = kinematics(c_point, lengths)

        visualize_robot_arms(points, shapes, False, intersection)


def test_angular_distance(c_space_point1, c_space_point2):
    sum = 0
    for cord1, cord2 in zip(c_space_point1, c_space_point2):
        # determind which direction is the "shortest"
        D = abs(cord1-cord2)
        shorter_path = pow(min(D, 2*pi - D), 2)
        sum += shorter_path
    return sqrt(sum)



if __name__ == "__main__":

    ### CODE FOR TESTING OUR SAMPLING METHOD IN THE C SPACE! ###

    """
    lengths = [2, 1, 3]
    R = 3
    test = Planner(R, lengths)
    c_points = test.sample_points(5)
    test_point_sampling(c_points, lengths)
    """

    ### CODE FOR TESTING OUR DISTANCE FUNCTION IN THE C SPACE! We see that ourt function takes the shorter path around the torus!###
    """
    c_point_1 = (pi/4,pi/4)
    c_point_2 = ((7*pi)/4,(7*pi)/4)

    print(test_angular_distance(c_point_1,c_point_2))
    print(sqrt(2)/2 * (pi))
    """

    ### CODE FOR TESTING OUR EDGE CREATOR
    """
    R = 2
    lengths = [2, 1]
    test = Planner(2, lengths)
    test.create_edges(k=5)
    """

    ### CODE FOR TESTING OUR ADDING IN THE START AND GOAL STATES INTO OUR CONSTRUCTED GRAPH
    """
    R = 2
    lengths = [2, 1]
    start_config = (0,0)
    goal_config = (pi/4,pi/4)
    k=5

    test = Planner(start_config, goal_config, R, lengths)

    test.create_edges(k)
    test.include_query(k)

    print(test.road_map[start_config])
    print(test.road_map[goal_config])
    """


    ### CODE FOR TESTING THE SEARCH FUNCTION TO FIND THE PATH THRU THE C SPACE ###
    # TEST CASE 1 --> R = 2
    """
    R = 2
    lengths = [1, 1]

    shape1 = [(.25, 2.5), (.25, 3.5), (1.25,2.5), (1.25, 2.5), (.25, 2.5)]
    shape2 = [(.25, .25), (.25, .9), (.9,.9), (.9, .25), (.25, .25)]

    obstacles = [shape1, shape2]

    start = (pi/2, 3*pi/2)
    goal = (0, pi/2)

# FOR TESTING DIFFERENT FUNCTIONALITY AS A FUNCTION OF NUMBER OF NEAREST NEIGHBORS 
    k=5
    #k=10
    #k=25
    #k=100
    # k=250

    num_samples=200000
    epsilon = 0.1
    
    ### KNN IMPLEMNTATION 
    nn=True
    #nn=False

    time1 =time.time()

    test = Planner(start, goal, R, lengths, obstacles, k, num_samples, epsilon, nn)

    path = test.bfs()

    time2 =time.time()
    
    if path:
        print(path)
        print(f"This is how long the algorithm took with KNN being {nn}: {time2-time1}")
        test_point_sampling(path, lengths)
    else:
        print("Did not find a path!")
    
    """

    
    """
    # TEST CASE 2 --> R = 3
    R = 3
    lengths = [0.75, 0.75, 0.75]

    shape1 = [(0, 0.2), (.8, .8), (0, .8), (0,0.2)]
    shape2 = [(2, 0.8), (2, .5), (2.2, .5), (2.2, 0.8)]
    shape3 = [(1.25, 1.25), (1.25, 1.75), (1.75,1.75), (1.75, 1.25), (1.25, 1.25)]

    obstacles = [shape1, shape2, shape3]

    # start = (0, 5*pi/4, 3*pi/4)
    start = (0,0,0)
    goal = (1.3*pi/2, 3*pi/2, 10.5*pi/6)
    k=5
    #k=10
    #k=25
    #k=100
    #k=250
    num_samples=100000
    epsilon = 0.3

    ### KNN IMPLEMNTATION 
    nn=True
   # nn=False

    #knn_tree_number=1
    #knn_tree_number=10
    knn_tree_number=25

    time1 =time.time()


    test = Planner(start, goal, R, lengths, obstacles, k, num_samples, epsilon, nn, knn_tree_number)

    path = test.bfs()

    time2 =time.time()

    
    if path:
        print(path)
        print(f"This is how long the algorithm took with KNN being {nn}: {time2-time1}")

        test_point_sampling(path, lengths)
    else:
        print("Did not find a path!")
    """
    

    # TEST CASE 3 --> R = 4
    
    R = 4
    lengths = [0.9, 0.9, 0.9, 0.9]
    
    
    shape1 = [(0, 0.2), (.8, .8), (0, .8), (0,0.2)]
    shape2 = [(3.2, 0.8), (3.2, .5), (3.5, .5), (3.5, 0.8)]
    shape3 = [(1.5, 2), (1.5, 2.5), (2, 2.5), (2, 2), (1.5, 2)]

    obstacles = [shape1, shape2, shape3]
    
    #start = (0,pi,pi,pi)
    start = (0,pi,pi,pi)
    goal = (pi/6, 1.7*pi/6, 0, 11*pi/6)
    
    #k=5
    #k=10
    k=25
    #k=100
    #k=250
    
    #num_samples=10000
    num_samples=100000
    epsilon = 0.50

    ### KNN IMPLEMNTATION 
    nn=True
    #nn=False

    #knn_tree_number=1
    #knn_tree_number=10
    knn_tree_number=25
    #knn_tree_number=100



    time1 =time.time()

    test = Planner(start, goal, R, lengths, obstacles, k, num_samples, epsilon, nn, knn_tree_number)

    time2 =time.time()

    path = test.bfs()
    
    if path:
        print(path)
        print(f"This is how long the algorithm took with KNN being {nn}: {time2-time1}")
        test_point_sampling(path, lengths)
    else:
        print("Did not find a path!")
    
    
    

    pass
    