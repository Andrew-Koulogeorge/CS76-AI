from collections import defaultdict
"""
Scipt that will contain the Class for the general CSP problem
"""
class CSP:
    def __init__(self, assignment, domains, constraints, variable_lookup, value_lookup):

        # array representing the variable assignment. A[i] = j --> variable i takes on value j
        self.assignment = assignment

        # thinking that domains is goign to be a hashmap from the variable number to a set of possible values that that variable is allowed to take on
        self.domains = domains

        # map with a pair of variables as key (i,j) --> set of legal values the two can take on
        self.constraints = constraints

        # map that gives the domain name of the variable from the index we are storing it as (2 --> :"SA")
        self.variable_lookup = variable_lookup

        # map that gives the value name of the value from the index we are storing it as (1 --> "blue")
        self.value_lookup = value_lookup

        # could be a good idea to keep a set containing variables that have not been assigned. As we assign we can remove from set
        self.not_assinged = set()
        for var in range(len(self.assignment)):
            self.not_assinged.add(var)
        
        # also want to make a graph that represents the constraints between variables with an adjlist
        # x --> set of other variables that x is contrained with. doing this for fast lookup of 
        self.directed_constraint_graph = defaultdict(set)

        # loop over the keys in of the constraint map: (x,y) have a constraint 
        for (x,y) in self.constraints.keys():
            self.directed_constraint_graph[x].add(y)
            self.directed_constraint_graph[y].add(x)

    def __str__(self) -> str:
        """
        Want to return the human interpretable solution to the problem we were solving!
        """

        # loop over the variables we assigned and output what the human meaning was
        solution = "Solution: \n"
        for i , value in enumerate(self.assignment):
            variable_name, value_name = self.variable_lookup[i], self.value_lookup[value]
            solution += f"{variable_name} --> {value_name} \n"
        

        return solution


    """
    Want functionality for all of our CSP problems where we can view the variables, domains, and constraints 
    """
    def print_csp(self):
        # show the current state of the variable assignment 
        print(f"Current State of the {len(self.assignment)} variables: {self.assignment}\n")

        print(f"Constraints for the problem: {self.constraints}\n")

        print(f"Domains that each variable can take: {self.domains}")
    
    """
    Loop over the keys of the constraint map (the variables that have a constraint between them) and look up what there representation is
    Print out pairs of human understandable variables which are coupled
    """
    def show_constraints(self):
        keys = self.constraints.keys()
        print(f"Here are the variables that are constrainted! We have a total of {len(keys)} edges in our graph representation of the problem!")
        for index_1,index_2 in keys:
            var_1,var_2 = self.variable_lookup[index_1], self.variable_lookup[index_2]
            print(f"There is a constraint between {var_1} and {var_2}\n")
