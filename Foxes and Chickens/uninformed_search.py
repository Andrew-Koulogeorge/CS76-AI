# Andrew Koulogeorge: 9/17/2023


from collections import deque
from SearchSolution import SearchSolution

class SearchNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object
    def __init__(self, state, parent=None):
        self.state = state 
        self.parent = parent # parent node purpose is to follow backchaining to find the shortest path

"""
-Implementation of BFS on the implicit graph where a node is a state of our problem.
"""
def bfs_search(search_problem):
    solution = SearchSolution(search_problem,"BFS")
    queue = deque() 
    start_node = SearchNode(search_problem.start_state) 
    queue.append(start_node) # queue will hold SearchNode class and the states will be stored inside them

    if not search_problem.is_valid(start_node.state): return solution # check if the starting state is a valid state and return and empty solution object if not

    while queue: 
        current = queue.popleft()
        solution.nodes_visited += 1
        # get all of the nodes we could reach from this point that are valid
        for neighbor in search_problem.get_successors(current.state):
            if neighbor not in solution.current_seen:
                new_node = SearchNode(state=neighbor,parent=current) 
                queue.append(new_node)
                solution.current_seen.add(neighbor)
                
                if search_problem.is_goal(neighbor): # check if the state we have gotten to is the winning state. if it is, then we are done!
                    solution.path = backchain(new_node)
                    return solution

    return solution

"""
-Function that inputs the end state and returns the shortest path from the start state to the end state.
-State nodes hold a parent pointer to the node which visisted them. Following these pointers back to the start state
give the shortest path in the graph from Start --> End
"""
def backchain(solution):
    chain = [] # list thats going to hold the nodes starting with the solution node
    curr = solution 
    
    while curr:
        curr_state = curr.state
        chain.append(curr_state) # add the state of the current node to the list
        curr = curr.parent # update pointer of current node to be its parent. Backtracking through the graph!
    
    chain.reverse() # want the list to start with the inital state and end with the ending goal
    return chain

"""
-Recursive implementation of DFS that keeps track of the nodes on the current path.
-We keep both current_seen and path as instance variables of the SearchSolution class. While this does cost extra memory,
it enables fast look ups of if the current node is in our current path since the lookup in a set is O(1)
-We also keep a instance variable dfs_found in SearchSolution which turns true if we have found the solution. The
truth of this variable is what forces the recursive function to bottle up and return the shortest path. 
"""
def dfs_search(search_problem, depth_limit=100, node=None, solution=None):
    # if no node object given, create a new search from starting state
    if node == None:
        node = SearchNode(search_problem.start_state)
        solution = SearchSolution(search_problem, "DFS")

    solution.current_seen.add(node.state) # add the current state to the set of nodes currently in our path
    solution.path.append(node.state) # append current state to our list holding the current path
    solution.nodes_visited += 1 # add 1 to our counter of how many nodes we have seen

    # BASE CASE --> If goal state, mark in the SearchSolution class we have found return the solution path and return the solution
    if search_problem.is_goal(node.state): 
        solution.dfs_found = True
        return solution
    
    # depth of x --> can have up to x + 1 nodes in your path. I consider the node to be at depth 0
    if len(solution.path) <= depth_limit:
        # RECURSIVE CASE --> Considering legal neighbors that are not currently in our path
        for neighbor in search_problem.get_successors(node.state):
            if neighbor not in solution.current_seen:
                new_node = SearchNode(neighbor)
                solution = dfs_search(search_problem, depth_limit, new_node, solution)
                if solution.dfs_found: return solution
    
    # bubbling up from a node: remove the current node from our current path
    solution.current_seen.remove(node.state) 
    solution.path.pop()
    return solution

"""
-Iterarive Deepening Search implementation.
-depth_limit definition enables depth_limit + 1 nodes to be contained in the path. Start node considered depth 0
"""
def ids_search(search_problem, depth_limit=15):

    solution = SearchSolution(search_problem,f"IDS with depth limit {depth_limit}")
    start_node = SearchNode(search_problem.start_state)

    if not search_problem.is_valid(start_node.state): return solution

    for depth in range(depth_limit+1):
        solution = dfs_search(search_problem, depth, start_node, solution)
        if solution.path: return solution

    return solution

