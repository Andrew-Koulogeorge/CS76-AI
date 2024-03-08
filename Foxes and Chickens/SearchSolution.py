# Andrew Koulogeorge: 9/17/2023

class SearchSolution:
    def __init__(self, problem, search_method):
        self.dfs_found = False
        self.current_seen = set() # going to keep a set of the nodes we currently have in in our path so that we can do fast look up time to see if the current node is in the path
        self.problem_name = str(problem)
        self.search_method = search_method
        self.path = [] # search solution has a built in path that we are going to build the solution from
        self.nodes_visited = 0 # can keep track of how many nodes in the tree we have visisted

    # to string method
    def __str__(self):
        string = "----\n"
        string += "{:s}\n"
        string += "attempted with search method {:s}\n"

        if len(self.path) > 0:

            string += "number of nodes visited: {:d}\n"
            string += "number of moves to reach solution: {:d}\n"
            string += "path: {:s}\n"

            string = string.format(self.problem_name, self.search_method,
                self.nodes_visited, len(self.path)-1, str(self.path))
        else:
            string += "no solution found after visiting {:d} nodes\n"
            string = string.format(self.problem_name, self.search_method, self.nodes_visited)

        return string
