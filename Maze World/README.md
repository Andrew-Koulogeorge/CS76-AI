# Andrew Koulogeorge HW 2: Maze World

## A* Search

### Set-Up
* My implementation of A* takes in a generic SearchProblem, Cost Function, and Heuristic Function. 
* The goal state of the two search problems is a tuple representing the end locations for the robot(s). 
* For the blind robot problem, each state is represented by a frozen set containing possible locations that the robot could be in in the maze. The use of a frozen set is required because we need the keys of our cost map to be hashable and thus not mutable.
* The AstarNode holds the state, a pointer to its parent state, and the values of the current lowest cost to reach the node $g(n)$ as well as the heuristic distance to the goal $h(n)$. The value (priority key) which is used to compare the nodes in $g(n) + h(n)$.
* In each of the nodes, I included direction so that the path the robot takes can be easily reconstructed and then translated into a maze visualization. 

### Algorithm 
* We begin with the start state node in our priority queue with the visisted cost of $0$. At each step we remove the node from the queue with the lowest $g(n) + h(n)$ value. If this node is our goal state then we backchain on this final node $x$, set the cost of the solution to be $g(x)$, and return the solution
    * Backchain will backtrack through the nodes of the solution path and reconstruct both the directions used to get to the solution as well as the states. 
* Otherwise, we want to loop over the neighboring states. 
    * For $k$ robots, there will always be $5$ new states representing the option of moving in any of the $4$ directions or staying still. This is because we are moving the robots one at a time!
    * For blind robots, there will always be $4$ new states. The robot will never stand still since it gains no new information about its location on the board from standing still!
* For each neighboring state, we then compute the cost to reach this state (cost to get to the parent + cost to get from parent to child). 
    * For the $k$ robots problem, cost_fn does a check to see if any of the robots moved since the last turn. If they have not, no additional fuel was used and cost_fn returns 0. If a robot has moved, we add $1$ to the parents cost since no robot can ever move by more than $1$ sqaure in a given turn.
    * For the blind robot, we always add $1$ to the parents cost since the robot is always moving.
* If we have found a new state, or we have found a cheaper path to a state we have already seen, we update the *visited_cost* map with this new cost. We then create a new node that holds a state, a parent and direction instance for backtracking, and a $g(n)$ and $h(n)$ for cleverly picking states from the priority queue.
    * Note that if we find a better path to a state that we do not remove the worst node from the priority queue. We just update the better cost in our map and push the cheaper node onto the priority queue.

## Multi Robot Coordination
*  The state for the $k$ robots problem is a $2k+1$ tuple where the first $2k$ elements represent the $(x,y)$ cordinates of the $kth$ robot's location and the last element indicates which robots turn it is to move.
    * In a one robot world, one state would be $(1,1,0)$ where our robot is at $(1,1)$ on the grid and it is his turn to move.
* Given an n x n maze and $k$ robots, there are $n^2$ possible locations that each of the $k$ robots could be in and there is also $k$ options for whose turn it could be. A rough estimate for the number of states would be $n^{2*k}*k$ where we are counting sequences of length $k+1$ where we have $n^2$ options for the first $k$ elements as $k$ options for the last element. We could make a more accurate estimate by observing that robots can not occupy the same space, so many of these states are invalid. A better estimate would be $(n^2)(n^2-1)...(n^2-k+1)(k)$ where there are $n^2$ locations that the first robot can be in and $(n^2-i+1)$ locations that the $i$ th robot can be in.
* If we have $w$ walls in our maze, then a state represents a collision if at least one of these robots is on a wall. The number of states where at least $1$ robot in the maze has crashed into a wall is the same as the total number of legal states minus the number of states where no robots have crashed into a wall $(X-Y)$
    * Total number of legal states with no walls: $X = (n^2)(n^2-1)...(n^2-k+1)(k)$ 
    * Number of state with no crashes with $w$ walls in the maze: $Y = (n^2-w)(n^2-w-1)...(n^2-w-k+1)(k)$. We just reduce the number of choices each robot has for a space by $w$ since they cannot legally be on a wall. 
* BFS would not be computationally feasible for an $100$ x $100$ grid with $10$ robots because the state space is too massive. If the depth of the goal is deep in the search tree, BFS is going to search most of the state space of roughly $100^{20} = 10^{40}$. If the goal location is only a few moves away for each robot it may work, but will not otherwise. If we wanted any shot at finding the goal in such a massive state, we would need to be more clever about the order we are removing nodes from the queue!
* As seen on page 108 of Norvig, a cost path is monotonic $\iff h(n)$ is consistent. Let us define our $h(n)$ as the sum of the $L1$ distances from each of the robots to its goal state.  Recall that $h(n)$ is consistent $\iff h(n) \leq h(n) + c(n,a,n') + h(n')$ where $h(n)$ is the cost of the heuristic at state $n$, $c(n,a,n')$ is the cost of the action from state $n$ to state $n'$, and $h(n')$ is the cost of the heuristic at state $n'$. We will prove that $h(n)$ is consistent by way of contradiction. Assume that $h(n)$ is not consistent $\implies h(n) > h(n) + c(n,a,n') + h(n') \implies 0 > c(n,a,n') + h(n')$. By the definition of the $L1$ norm (more generally, any metric), $h(n) \geq ~0 ~\forall ~n$. Additionally, $c(n,a,n') \geq 0$ since it equals $1$ when a robot moves and $0$ when it pauses $\implies c(n,a,n') + h(n') \geq 0$, a contradition. Thus, $h(n)$ is a consistent heuristic and thus the cost paths are monotonic.
* I include 5 examples to test my implementation of A* search for the Mazeworld $k$ robots problem. It becomes clear from generating the outputs that it would be a better cost function to use time instead of fuel. This can be seen because it makes no difference to the agent if it waits around vs moving closer to the goal. In each of these illistrations, I have deleted any intermediate maze where nobody moved just to save space. This functionality is implemented on the print out level but under the hood there are pauses going on. If you go to the test_mazeworld.py file all of the test cases are commented out in the main method and you can click run to generate the outputs. Included with the report is a textfile containing all of the robot paths.

    * Maze1: 3 robots using a temporary space to reorganize themselves to get to the goal states. This is pretty clear cut. I could do this in my head!
    * Maze2: 3 robots using a temporary space to reorganize themselfs to get to the goal states but harder! Not as clear. I actually came up with this test case by accident and put the wrong goal locations in, but the algorithm still came up with a cool solution!
    * Maze3: Robots getting out of eachother's way to reach goal state on a larger maze.
    * Maze4: Swapping robots in the corners of a larger maze with lots of walls! 
    * Maze5: Single robot navagating a large maze! (I didnt included in text file because too long for the command line output!)

* We can view the $8$ puzzle problem as being a special case of the $k$ robots problem where we have a $3x3$ grid and $8$ robots. Our goal state is when all of the robots are lined up in correspondance with the numbers 1-8. That is, robot A's goal state is location $(0,2)$, B's goal state is $(1,2)$, and H's goal state is $(1,0)$. The $L1$ heuristic will be very bad for the $8$ puzzle problem because of how many walls there will be in our maze. The $L1$ distance will greatly underestimate the true distance from our current state to the goal state. Additionally, it might not even be possible to reach the goal state from the current state yet the $L1$ heuristic would return some positive value.

* The $8$ puzzle having a state space that contains $2$ connected components is a super interesting result. I (wish I could) dive into the mathematics for why this is true (for some extra points :)) but first lets think about how we would write a program to confirm if this is true. 
* First, how many state's does the $8$ puzzle problem have? I claim that its $8*9!$. Our state is of length $17$ where the first $16$ elements of the sequence are the locations of the robots and the last element signals whose turn it is to move. The first robot can be in $9$ possible locations, the second can be in $8$, and the 8th can be in $2$. Then, it can be anyone turns turn to move (8 more options) $\implies 8*9!$. That is all to say that this state space is small enough where we can hold the states in our memory!
* The program to prove that this state space has two connected components would go like this:
    * Create two sets which represent the two connected components, *comp1* and *comp2*. Starting from the goal state, explore all of the nodes that are reachable from the goal state using a standard traversal algorithm like BFS and store all of the visited nodes in the set *comp1*.
    * Then, loop over all other possible states in the search space. For each node, check if its in *comp1* or *comp2*. If its in *comp1*, then we have already visited this node and we can move onto considering the next state. If its not in *comp1* and *comp2* is empty, explore all of the nodes reachable form this node and store them in the set *comp2*.
    * If the search space is indeed made of two disjoint sets, then we will only run BFS on the space twice and there will not exist a node that is neither in *comp1* or *comp2*. If there was, we would have more than two connected componenets in this space!

* You are probably thinking, who writes a proof with an algorithm? Why would this ever be true? Excellent questions. Lets take a look.

## 8-Puzzle Proof: State Space Contains 2 Connected Componenets
(Wish I had time for this. Proof is very elegant)
## Blind Robot with Pacman Physics

### Sensorless Problem
* The start state is constructed by looping over each entry in the maze and checking which ones are not walls. Each of these locations are added to a set which is then casted to a frozenset. We need all of the states in the blind robot problem to be frozensets so that we can place them in our cost map.
* When generating new successors for a given state, we consider each of the $4$ directions the robot could move for each of its possible states: 
    * For each direction, we loop over each of the possible locations and check to see if the new location is legal. If it is, then the robot could move to that state and we add it to the next state set. If that move wouldnt be legal, then the robot is going to stay still and we add the old location into the new state. Before adding it to the list of next states, we cast it to a frozen set to make sure we can properly hash it. 
    * We also keep track of direction when creating these new states so we know what action was taken to get from one state to another. This ends up being helpful when we visualize the robots path.
* We animate the path the blind robot takes by sending in the list of directions that the robot took to reach its optimal path. We set the robots x and y cords to be there inital values and then loop over the directions array. Based on what action was taken, we change the robots location print out the maze! If I didnt have so much other crap going on, I would want to implement a visualization where we could see all of the goast robots as well.

### Heuristic Discussion
* I used the cardinality of the state space as a heuristic for the estimated distance from node $n$ to the goal state. This heuristic is not optimistic. Consider a $3x3$ grid where the top left corresponds to $1$ and the bottom right corresponds to $9$ and let the goal state be the top right $=3$. Consider a state that only has one possible location in it but is very far away from the goal and another state with more possible locations that is only a couple of moves away from the goal. The state $\{7\}$ has a value of $1$ according to $h(n)$ but its farther from the goal then $\{2,3\}$ which has a heuristic value of 2. Going right from the state $\{2,3\}$ wins on the spot!

* One of the pit falls of using the cardinality of the state space as a heuristic is that it does not take into account two "ghost robots" being very far away from eachother as being a bad thing. We will get into why this is a good thing more formally when we discuss the polynomial time algorithm for solving this problem, but the intution is that in order for a state with 2 "ghost robots" to be collapsed into a state with only one "ghost robot", the two ghosts need to be next to eachother. The cardinality heuristic treats $\{1,300\}$ as being better than $\{1,2,3\}$ even though the second state is much closer to the goal than the first state assuming that $1$ is the goal state. 
* Thus, we could consider a heuristic that takes into consideration the geometry of the problem and compute the distances that each of the ghost robots are away from eachother (sum of $L1$ distances). For our big test case (see test_sensorless), we see that this finds a solution while visiting 11348 states. If we used the cardinality $h(n)$, its so slow we never get to a solution! 
* An optimal heuristic would incorperate both the cardinality and a metric for the closeness of all the robots! We can see in the last test case in the test_sensorless problem this at first hand. When we add in the pairwise distance in addition to having the closeness metric, the search finds the goal in 10264 states! It could be a cool extension to do some hyper parameter tuning and find what the optimal combination of these two levers are. Or, we could just cut the crap and solve the problem in polynomial time!

### Polynomial Time Blind Robot (Explanation)
* Let us consider breaking the problem of the blind robot looking for its goal into two separate phases. We seek to construct two algorithms to solve this problem, both of them working in polynomial time:
    * In the first phase, the robot needs to orient itself. It will not be looking for its goal state right away. Instead, it will be trying to gain its sight!
    * In the second phase, the robot knows where it is. From here, it can use A* search to find a fast way to the goal.
* The second step is no problem. The question is, how can the robot be sure that for any maze, it can arrive at a particular location?
* Observe that the state space of the blind robot shrinks when we have two states that are next to eachother and one of the states is up against a wall or the edge of the maze. When we move in the direction towards the wall or the edge of the maze, the state space shrinks. But what if no $2$ ghosts in the space are next to eachother? How can we come up with a plan such that given any two ghosts, we can get the two ghosts to be next to eachother so we can "ram" the state spaces into a wall or edge and shrink the state space?
* Consider the node in the bottom right corner of the maze, X, and any other node in the maze, Y. How expensive would it be to compute the shortest path in the maze from Y to X? We could run a wavefront BFS from X, storing the distance to X within in maze. Since the input of the problem is a matrix, once we find the node Y, we can run gradient decent to find the shortest path back to X. Therefore, we can find the shortest path from every node in the maze to $X$ in $O(n^2)$ time where the size of the matrix is $n^2$. 
* What happends when we have our blind robot follow the path from $Y$ to $X$ for any $Y$ in the graph? Note that when the blind robot starts out, it could be at location $X$. It has no idea, it is blind! Since $X$ is the right most and lowest node in the maze (more specifically, no node has a smaller y cord and no node as a larger x cord), I claim that any of the moves conducted by the blind robot following the shortest path from Y to X would keep the ghost robot at X in the same location. 
* Why is this true? It relies on the fact that $X$ exists (as we will see in a little bit, this does not need to be the case but lets go with it for now). Any of the moves that the robot acts going right or going down are not going to affect the ghost robot at $X$ at all because X is already at the the right most and bottom most spot. It will just be running into a wall! What about moves that are left and up? Its possible that there are lots of walls in the way, so the ghost at Y might have to go left and up a bunch, right? This is true, but I claim the following: any movment the ghost robot at Y takes that is to the left or up has a corresponding move that is to the right and down. Why is this the case? If Y is going left or up, we know thats its getting farther away from the goal state because we know that there is no location that is father to the right or lower than $X$! 
* Thus, given the shortest path from any node Y to node X, having the robot walk in the shortest path from node Y to node X will keep the ghost at node X the same. If we ran this algorithm on every node in the maze, the robot would know with certainty that it would be at node X. There are $O(n^2)$ nodes in the maze and it takes $O(n^2)$ time to find the shortest path from all nodes in the maze to Y. We will first run wavefront BFS from X to every other node. Then, we will loop over each node in the maze that is not a wall and run gradient decent from that location, keeping track of the directions that the robot moves to get from Y to X. For every Y, we can append these directions into a master list. After running all of the directions in this list, the robot will know for certain that it will belong in the bottom right of the maze. Thus, we have solved the first phase! Right? Actually, no! :( But we are very close. 
* It is not guarentted that such a node X exists in the graph. How come? Imagine an nxn maze that has lots of walls such that it is in the shape of a cross. In this case, there is no node which is the rightmost and lowest. This is not a huge deal (being completely honest here- I am not 100% sure this isnt a big deal. At the time limit for the HW but im almost certain that we can get around it with this following trick). We just need to take more than one node $X'$ that is in a bottom right or bottom left corner. When we are looping over all states in the maze, we just need to make sure that the path that we create from $Y = (y_1,y_2)$ to $X = (x_1,x_2)$ (could be X or X') that either $y_1 < x_1$ and $y_2 > x_2$ (where X is acting at the bottom right node) or $y_1 > x_1$ and $y_2 > x_2$ (where X is acting at the bottom left node). We will run the paths for all of the nodes Y are not below or to the right of X first. Once we have squashed all of them, we will squash the nodes that are below or to the right of X by matching those nodes up with X'. 
* Now, we just run A* search from the corner node that we gradient decented to last. This algorithm is fast with a good $h(n)$ like the $L(1)$ metric!

### Polynomial Time Blind Robot (Implementation) (Assumed that the bottom right corner is not a wall)
For this implementation, we will assume that there exists a rightmost and lowest spot in the maze. We denote this location by X. Here is an overview of my implementation of the polynomial time algorithm.
* I create a matrix representation of the ASCII map. Note that the indexing of the ASCII maze is different than the way we would think about storing a matrix as a data structure so when we make a check to the Maze object, we swap the x and y cords. Kinda annoying, I know. 
* We break the problem into 3 main parts:
    * First, given the location of X, we compute the shortest path from X to all other locations in the maze. We do this by doing a standard call to wavefront BFS. Wavefront BFS creates a new version of the maze where instead of having "." for non wall locations, we have shortest distances from that location to X.
    * Then, we need to create, for each non wall location in the maze, the shortest path from that location to X. We do this by looping over all locations in the maze that are not walls and running gradient decent on the heat map. We keep track of the directions we take back towards X and store those in an array. Note how we had to be clever with which directions correspond to which movments because of the index mis-match with the ASCII mazes. If I hadnt already put too much time into this assigment I would make sure to fix this! After we have returned back to X, we have filled all of our directions and we append it to the end of our master list. After we have done this for all non maze nodes, we have the direction list to ensure that the robot is at X.
    * Once we know that the robot is at X, we simply run A* search from X. To arrive at our final directions list, we combine the directions list needed to get to X with the directions needed to get to the goal. With this, we have constructed a polynomial time algorithm to find a path for the blind robot to the goal!
* Note that this algorithm may be very fast at finding a goal, but it is not an efficent path! Lots of moves are required for big mazes since each locations (in my current implementation) walks a path to X. I am sure there are optimizations to this, but like I said, I have already spent too much time on this!
