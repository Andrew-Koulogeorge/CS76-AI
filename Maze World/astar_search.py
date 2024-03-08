from SearchSolution import SearchSolution
from heapq import heappush, heappop

class AstarNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, heuristic, direction = "Start", parent=None, g_n=0):
        self.state = state
        self.parent = parent
        self.h_n = heuristic
        self.g_n = g_n
        self.direction = direction


    # going to be a sum of the actual cost to that point g(n) + heuristic function h(n)
    def priority(self):
        return self.h_n + self.g_n

    # comparison operator,
    # needed for heappush and heappop to work with AstarNodes:
    def __lt__(self, other):
        return self.priority() < other.priority()


# take the current node, and follow its parents back
#  as far as possible. Grab the states from the nodes,
#  and reverse the resulting list of states.
def backchain(node):
    states = []
    directions = []
    current = node
    while current:
        states.append(current.state)
        directions.append(current.direction)
        current = current.parent

    states.reverse()
    directions.reverse()
    return states, directions


def astar_search(search_problem, cost_fn, heuristic_fn):
    goal = search_problem.goal_state
    
    start_node = AstarNode(state=search_problem.start_state, heuristic = heuristic_fn(search_problem.start_state, goal))

    if isinstance(start_node.state,frozenset): blind = True

    pqueue = []
    heappush(pqueue, start_node)

    solution = SearchSolution(search_problem, "Astar with heuristic " + heuristic_fn.__name__)

    visited_cost = {}
    visited_cost[start_node.state] = 0 # keys to our cost look up table are frozen sets

    while pqueue:
        min_node = heappop(pqueue) # get the lowest f(n) node from the priority queue

        solution.nodes_visited += 1

        print(f"Nodes we have visited so far! {solution.nodes_visited}")

        # if the min priority node is the goal state, backchain and return.
        if search_problem.is_goal(min_node.state):
            solution.path, solution.directions = backchain(min_node)
            solution.cost = visited_cost[min_node.state]
            return solution

        next_directions, next_states = search_problem.get_successors(min_node.state)

        assert len(next_directions) == len(next_states), " Error in the way we are generating directions to new states"

        for direction_to_child, child in zip(next_directions, next_states): # get_successors returns a set of tuples (child is already in state form)
            # compute the cost to get to the child node
            child_cost = visited_cost[min_node.state] + cost_fn(child,min_node.state)

            # if we have not visited this node yet, or we have found a shorter path to this node, update the cost in the map
            if (child not in visited_cost) or (child in visited_cost and visited_cost[child] > child_cost): 
                # marking the entry as removed by updating this cost????????????
                visited_cost[child] = child_cost

                # make node that sends the heuristic from this node to the goal state, its parent, and the actual cost to the node so far
                child_node = AstarNode(child, heuristic_fn(child, goal), direction_to_child, min_node, child_cost)
                heappush(pqueue,child_node)        
    return solution



if __name__ == "__main__":
    x = set([1,2,3])
    y = set([1,2,3])     
    print(x == y)     
                


