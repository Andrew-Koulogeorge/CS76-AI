"""
Script representing the Aussie map problem as a subclass of our CSP problem
"""
from CSP_Solver import CSP_Solver
from CSP import CSP
from collections import defaultdict
import random
import time

class CSP_Aussie(CSP):
    """
    - Regions is a list of the names of the states of Aussie
    - Neighbors is a list of tuples representing which states are next to eachother
    - Colors is a list of the colors that we are going to color the map with
    """
    def __init__(self, regions, neighbors, colors):

        self.problem_name = "Aussie Map Problem"

        # can keep a dictonary that maps the names of the regions to there variable index
        variable_lookup = {}
        value_lookup = {}

        # region_to_index needed to construct the general CSP problem from our input
        self.region_to_index = {}

        for i, region in enumerate(regions):
            variable_lookup[i] = region
            self.region_to_index[region] = i

        for i, color in enumerate(colors):
            value_lookup[i] = color
        
        assignment, domains, constraints = self.transform_to_CSP(regions, neighbors, colors)

        super().__init__(assignment, domains, constraints, variable_lookup, value_lookup)
  

    """
    Given the map as an input, want to transform in a general CSP problem 
    """
    def transform_to_CSP(self, regions, neighbors, colors):
        # first need to construct the general list thats going to hold variables for assignment. will represent a variable without an assigned value by *
        assignment = ["*"]*len(regions)

        # now need to construct the legal values for each of the countries
        domains = defaultdict(set)

        # need how many colors we are allowed to color the map with
        num_colors = len(colors)

        # adding a set of every color we have avalible to each variable domain; any region could take on any color!
        for i in range(len(assignment)):
            for color in range(num_colors):
                domains[i].add(color)

        # now we need to create a map of constraints between variables
        constraints = defaultdict(set)

        # looping over tuples that represent states that are next to eachother on the map
        for neighbor in neighbors:
            state_1,state_2 = neighbor
            var_1,var_2 = self.region_to_index[state_1],self.region_to_index[state_2]

            for c_1 in range(num_colors):
                for c_2 in range(num_colors):
                    if c_1 != c_2:
                        constraints[(var_1,var_2)].add((c_1,c_2))
                    
        return (assignment, domains, constraints)
        
def tester(regions, neighbors, colors, naive_next_var=True, naive_next_val=True, naive_inf=True):
    """
    Code to automate testing different parts and board dims
    """
    random.shuffle(regions)
    random.shuffle(neighbors)
    random.shuffle(colors)

    problem = CSP_Aussie(regions, neighbors, colors)
    solver = CSP_Solver(problem)

    start_time = time.time()
    solution = solver.backtrack(naive_next_var,naive_next_val,naive_inf)
    print(f"It took {time.time()-start_time} to run and I called the backtracking algorithm {solver.states_visited} number of times!\n")

    if solution == "Failure":
        print("Not possible!")
    else:
        print(solution)

if __name__ == "__main__":

    regions = ["WA", "NT", "SA", "Q", "NSW", "V", "T"]
    neighbors = [("WA","NT"),("WA","SA"),("SA","NT"), ("Q","NT"),("Q","SA"),("Q","NSW"),("SA","NSW"),("V","NSW"),("SA","V")]
    colors = ["red","blue","green"]

    # Consider the different methods
    naive_next_var = True
    naive_next_val = True
    naive_inf = True

    tester(regions,neighbors,colors)

    