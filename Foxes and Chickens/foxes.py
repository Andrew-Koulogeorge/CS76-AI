# Andrew Koulogeorge: 9/17/2023


from FoxesProblem import FoxProblem
from uninformed_search import bfs_search, dfs_search, ids_search

problem331 = FoxProblem(start_state=(3, 3, -1),goal_state = (0,0,1))
problem451 = FoxProblem(start_state=(4, 5, -1),goal_state = (0,0,1))
problem551 = FoxProblem(start_state=(5, 5, -1),goal_state = (0,0,1))
problem551_boat_size3 = FoxProblem(max_boat_size = 3, start_state=(5, 5, -1),goal_state = (0,0,1))

big = FoxProblem(start_state=(100, 100, -1),goal_state = (0,0,1))
test_start_state = FoxProblem(max_boat_size = 3, start_state=(5, 5, -1),goal_state = (0,0,1), total_chickens=10, total_foxes=10)

# print(bfs_search(big))
# print(dfs_search(big))
# print(ids_search(big))

print(bfs_search(problem331))
print(dfs_search(problem331))
print(ids_search(problem331))

print(bfs_search(problem551))
print(dfs_search(problem551))
print(ids_search(problem551))

print(bfs_search(problem451))
print(dfs_search(problem451))
print(ids_search(problem451))

# print(bfs_search(problem551_boat_size3))
# print(dfs_search(problem551_boat_size3))
# print(ids_search(problem551_boat_size3))