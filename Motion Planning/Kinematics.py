from math import cos, sin, pi
from shapely.geometry import Polygon, LineString
import matplotlib.pyplot as plt


def compute_endpoints(angles:list, lengths:list) -> list:
    """
    given a list of angles, wish to compute the endpoints for each of the arms
    """

    # starting point is the origin
    endpoints = [(0,0)]

    # want to have computed the cords of the last point to base the next cords off of
    theta_sum, x_last, y_last = 0,0,0
    
    for angle, length in zip(angles, lengths):
        x = x_last + length*cos(angle + theta_sum)
        y = y_last + length*sin(angle + theta_sum)
        
        endpoints.append([x,y])

        theta_sum += angle
        x_last, y_last = x, y

    return endpoints

def get_obstacles() -> list:
    """
    Returns shapes in list format (great for the visualizer)
    """

    """
    ###TEST CASE R = 2
    
    shape1 = [(.25, 2.5), (.25, 3.5), (1.25,2.5), (1.25, 2.5), (.25, 2.5)]
    shape2 = [(.25, .25), (.25, .9), (.9,.9), (.9, .25), (.25, .25)]

    return [shape1, shape2] 
    """

    """
    ### TEST CASE R = 3
    shape1 = [(0, 0.2), (.8, .8), (0, .8), (0,0.2)]
    shape2 = [(2, 0.8), (2, .5), (2.2, .5), (2.2, 0.8)]
    shape3 = [(1.25, 1.25), (1.25, 1.75), (1.75,1.75), (1.75, 1.25), (1.25, 1.25)]

    return [shape1, shape2, shape3] 
    """
    
    
    ### TEST CASE R = 4
    shape1 = [(0, 0.2), (.8, .8), (0, .8), (0,0.2)]
    shape2 = [(3.2, 0.8), (3.2, .5), (3.5, .5), (3.5, 0.8)]
    shape3 = [(1.5, 2), (1.5, 2.5), (2, 2.5), (2, 2), (1.5, 2)]
    

    return [shape1, shape2, shape3] 
    

def convert_shapely_lines(endpoints):
    shapely_lines = []

    for i in range(1,len(endpoints)):
        line = LineString([endpoints[i-1],endpoints[i]])
        shapely_lines.append(line)
    
    return shapely_lines


def convert_shapely_obstacles(obstacles):
        shapely_obstacles = []

        for obstacle in obstacles:
            polygon = Polygon(obstacle)
            shapely_obstacles.append(polygon)
        
        return shapely_obstacles

def collision(shape_lines, shape_obstacles) -> bool:
    """
    Given the current config of the arm and the shapes which are in the physical world, check if there is an intersection!
    -- Look over each of the obstacles in our list. Look over all of the lines and check if there is an intersection.
    """

    for obstacle in shape_obstacles:
        for arm in shape_lines:
            if obstacle.intersects(arm) and not obstacle.touches(arm):
                return True
    return False

    
def kinematics(angles, lengths, legal_point_checker=False):
    endpoints = compute_endpoints(angles, lengths)
    obstacles = get_obstacles()
    new_lines, new_obstacles = convert_shapely_lines(endpoints), convert_shapely_obstacles(obstacles)
    collide = collision(new_lines, new_obstacles)
    
    if legal_point_checker:
        return collide
    else:
        return (endpoints, obstacles, collide)

def visualize_all_configs(multiple_angles, lengths):
    
    obstacles = get_obstacles()
    new_obstacles = convert_shapely_obstacles(obstacles)
    collide = False
    multiple_endpoints = []

    for angle in multiple_angles:

        endpoints = compute_endpoints(angle, lengths)
        new_lines = convert_shapely_lines(endpoints)
        intersected = collision(new_lines, new_obstacles)
        
        if intersected:
            collide = True

        multiple_endpoints.append(endpoints)
    
    return (multiple_endpoints, obstacles, collide)

    
if __name__ == "__main__":

    ### TEST CASE1 ###

    # CORRECTLY COMPUTES LOCATIONS AND VISUALIZES THE ARMS AND SHAPES. IF INTERSECTION, RED!
    angles = [pi/4, 0, pi/2]
    lengths = [1, 1, 1]

    endpoints, obstacles, collide = kinematics(angles, lengths, False)



