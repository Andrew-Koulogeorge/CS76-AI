# Andrew Koulogeorge: 9/17/2023


# theory.py is to explore the nature of the Fox and Chicken problem with various other inputs
from FoxesProblem import FoxProblem
from uninformed_search import bfs_search 

# When total_foxes = total_chickens = 0, the problem is in a trivial state where all of the animals are already on the other side of the river.

def simulate_small_examples(size=2):
    print(f"Simulating small examples with BOAT SIZE = {size} \n")

    problem111 = FoxProblem(max_boat_size=size, start_state=(1, 1, -1),goal_state = (0,0,1)) 
    print(bfs_search(problem111))

    problem221 = FoxProblem(max_boat_size=size, start_state=(2, 2, -1),goal_state = (0,0,1))
    print(bfs_search(problem221))

    problem331 = FoxProblem(max_boat_size=size, start_state=(3, 3, -1),goal_state = (0,0,1))
    print(bfs_search(problem331))

    problem441 = FoxProblem(max_boat_size=size, start_state=(4, 4, -1),goal_state = (0,0,1))
    print(bfs_search(problem441))

    problem551 = FoxProblem(max_boat_size=size, start_state=(5, 5, -1),goal_state = (0,0,1))
    print(bfs_search(problem551))

def simulate_trend(size):
    print(f"Simulating longer term trends with BOAT SIZE = {size} \n")
     # We see that this pattern repeats for any equal numbers of total_foxes and total_chickens greater than 3
    for i in range(5,20):
        print(bfs_search(FoxProblem(max_boat_size = size, start_state=(i,i,-1),goal_state=(0,0,1))))

def simulate_one_less_fox(n):
    print(f"Simulating less starting foxes than chickens up to {n} chickens \n")
    for i in range(1,n):
        for j in range(5):
            print(bfs_search(FoxProblem(max_boat_size = 2, start_state=(i-j,i,-1),goal_state=(0,0,1))))



if __name__ == "__main__":
    # solutions possible for total_foxes = total_chickens = {1,2,3} if boat_size = 2
    simulate_small_examples(2)
    simulate_trend(2)

    # solutions possibler for total_foxes = total_chickens = {1,2,3,4,5} if boat_size = 3
    simulate_small_examples(3)
    simulate_trend(3)

    # solution always possible for boat_size >= 4 --> SEE PROOF!
    simulate_trend(4)

    # solution always possible if we start with at least 1 less fox than chicken --> SEE PROOF!
    simulate_one_less_fox(10)


