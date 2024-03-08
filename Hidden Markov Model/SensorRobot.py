"""
Implement the filtering algorithm to estimate where the robot is located at time step T given sensor information about the color of the square that it is on at each time slice
"""
from Maze import Maze
import numpy as np
from numpy import linalg
import random
import matplotlib.pyplot as plt
from math import log10
from math import inf

class SensorRobotSolver:

    def __init__(self, maze:Maze, random_start=False, perfect_information=False, time_steps=100) -> None:
        """
        X_t is our state vector which takes on 16 possible values corresponding to where the robot might be on the board. 
        E_t is our sensor data which outputs what color we observe 
        """
        # adding a variable to make our sensor perfect
        self.perfect_information = perfect_information

        # want to know how many values our state variable can take on
        self.maze = maze
        self.size = self.maze.width * self.maze.height 
        self.total_steps = time_steps

         # randomly select an index on the maze, get its location, and update the robots location
        looking = True
        if random_start:
            while looking:
                locations = [i for i in range(self.size)]
                start = random.choice(locations)
                random_x, random_y = self.index_to_location(start)
                if self.maze.legal_loc(random_x, random_y):
                    self.maze.robotloc = (random_x, random_y)
                    looking = False
             
        self.sensor_correctness = []

        # inital belif about where we are located in the maze
        self.f_0 = self.construct_inital_distribution()

        # initilization for the backwards messaging
        self.b_T = np.array([1]*maze.size) 
        
        x,y = self.maze.robotloc

        self.start_x = x
        self.start_y = y

        # want to keep track of the ground truth about where the robot actually is
        self.true_location = [self.location_to_index(x,y)]
        self.init_color = self.maze.get_color(x,y)

        # memory efficent to keep information we are going to reuse globally
        self.directions = [(0,1),(1,0),(-1,0),(0,-1)]
        self.color_to_index = {
            "R":0,
            "B":1,
            "G":2,
            "Y":3 }

        # precompute T, T transpose, and the 4 possible O diag matrixs to be used for the forward message pass and the backwards pass
        self.construct_transition_matrix()
        self.construct_observation_matrixs()

        # variable to keep track of if the forward pass has been made; cannot 
        self.has_filtered = False


    

    def construct_inital_distribution(self):
        """
        Based on the maze and where the legal states are, we want to compute the prior distribution
        """

        f_0 = np.array([1]*self.maze.size)

        for i in range(self.maze.size):
            x,y = self.index_to_location(i)
            if not self.maze.legal_loc(x,y): 
                f_0[i] = 0

        total = np.sum(f_0)
        f_0 = f_0/total
        return f_0


    def filter(self):
        self.forward_message()
        self.has_filtered = True
    
    def forward_message(self):
        """
        Want a function that will output the probability distribution of where the robot thinks he is at each time step
        """
        # want to be cashing the messages as well as the colors observed at each time step to be used later for backward smoothing and viterbi 
        self.forward_messages = [self.f_0]
        self.colors_observed = []

        # we start out with the inital distribution computed in the initilzation 
        f_t = self.f_0 

        # print(f"Here is our inital distro: {f_t}\n") 
        # print(self.maze)
        # print(f"Robot Starting Location: {self.maze.robotloc}")

        for step in range(self.total_steps):
            
            # pick a direction to move at random
            self.robot_step()

            
            x,y = self.maze.robotloc
            index = self.location_to_index(x,y)
            
            # cache true location of robot and record true color the square the robot is standing on
            self.true_location.append(index)
            true_color = self.maze.get_color(x,y)


            # check if we are checking for perfect information from the sensor
            if self.perfect_information:
                observed = true_color
                self.sensor_correctness.append(True)
            else:
                # use the sensor that has some noise in it to generate an observation; we also record the correctness of the sensor output to later understand our viterbi
                epsilon = random.randint(1,100)
                if epsilon < 88:
                    # 88% of the time, we want to have the sensor read the true color
                    observed = true_color
                    self.sensor_correctness.append(True)
                else:
                    # the other 12% of the time, we want to pick at random one of the other colors
                    colors = ["R", "G", "B", "Y"]
                    colors.remove(true_color)
                    observed = random.choice(colors)
                    self.sensor_correctness.append(False)

            self.colors_observed.append(observed)

            # get it from the cashe! dont recompute!
            O_tplus1  = self.observations[observed]
            
            # matrix mult --> Quickly compute the next state and normalize !
            intermediate = np.linalg.multi_dot([O_tplus1,self.T_transpose,f_t]) 
            total = np.sum(intermediate)
            f_t = intermediate/total

            # cache this distribution to be used later for smoothing
            copy_to_cashe = f_t.copy()
            self.forward_messages.append(copy_to_cashe)

            # print(f"-> Here is our robots new location after trying to move! {self.maze.robotloc}")
            # print(f"-> Color we observed! {observed}. This observation is {self.sensor_correctness[-1]}")
            # print(f"-> Here is the updated distro: {list(f_t)}\n")
            # print(f"-> Here is the probability of being in the true location: {f_t[index]}\n")
            # print(self.maze)
            # print("_____________________")


            if max(f_t) == 1: 
                # print(f"CONVERGED TO DETERMINISTC IN {step} steps!\n")
                return (self.location_to_index(self.start_x,self.start_y) ,step)
            
        # print(f"During simulation to test nummber of steps until convergence, the robot not able to find where it was in {self.total_steps} steps!")
        return None

    def smooth(self):
        """
        Compute new probability distributions based on the forward information
        """
        
        # first, make sure we have computed all of the forward messages
        if not self.has_filtered:
            self.forward_message()
            self.has_filtered = True
        
        # then, make sure we have backwards messages
        self.backward_message()

        # compute the smooth probability distribution at each time step by getting the element wise product of the forward and backward message
        total_boost = 0 # keep track of the total probability contribution on the most likley state
        self.smooth_boost_data = [] # and the specifc value 
        for k in range(self.total_steps+1):

            smooth_k = np.multiply(self.forward_messages[k], self.backward_messages[k])

            # want to normalize the new, smoothened probability distro 
            total = np.sum(smooth_k)
            smooth_k = smooth_k/total

            index = self.true_location[k]

            # compute how much impact the backwards message had on the probability of our ground truth location and include this into our data trackers
            improvment = smooth_k[index] - self.forward_messages[k][index]
            self.smooth_boost_data.append(improvment)
            total_boost += improvment

            # print('\n')
            # print(f"-> Did our sensor get this color correct? {self.sensor_correctness[k-1]}")
            # print(f"-> Count: {k}")
            # print(f"-> Here is where the robot actualy was in the maze: {self.true_location[k]}")
            # print(f"-> Impact from the smoothing on the true location : {improvment}")
            # print(f"-> How confident is the robot he is in the correct spot? {smooth_k[index]}")

            # # UNCOMMENT IF YOU WANT TO SEE THE 3 DIFFERENT PROBABILITY DISTROS
            # #print(f"-> Forward message: {self.forward_messages[k]}\n")
            # #print(f"-> Backward message: {self.backward_messages[k]}\n")
            # print(f"-> Smoothed message: {smooth_k}")
            # print('-------------------\n')
        
        self.average_smoothing = (total_boost/self.total_steps)
        print(f"This is how much extra probability we get on average from using smoothing! {self.average_smoothing}")


    def backward_message(self) -> None:
        """
        Given all of the evidence that we observed in the forward pass, compute the backwards messages. We will compute there backwards messages from the last time step to the first
        """

        # storing all the backwards messages in a list; first message is initilized to all 1s
        backward_messages = [self.b_T]

        # loop over the evidence from the last observation to the first
        reverse_evidence = list(reversed(self.colors_observed))
    
        b_kplus1 = self.b_T
        for evidence in reverse_evidence:
            # get the observation matrix corresponding to the evidence seen at this timestep
            O_tplus1  = self.observations[evidence]

            # fast mat mult calculation to get the backwards message at this step; normalize
            b_k = np.linalg.multi_dot([self.T, O_tplus1, b_kplus1])
            total = np.sum(b_k)
            b_k = b_k/total

            # save this message in our cache list for smoothing
            copy_to_cashe = b_k.copy()
            backward_messages.append(copy_to_cashe)

            # prepare for next iteration
            b_kplus1 = b_k
        
        backward_messages.reverse()
        self.backward_messages = backward_messages


    def robot_step(self):
        """
        Robot randomly picking a direction to move ands stepping there. We only update the robots location if it steps into a legal sqaure, otherwise we keep the location the same
        """
        
        x,y = self.maze.robotloc
        dx,dy = random.choice(self.directions)
        new_x,new_y = x + dx, y + dy
        
        if self.maze.legal_loc(new_x,new_y):
            self.maze.robotloc = (new_x, new_y)


    def construct_transition_matrix(self):
        """
        Mant to construct the transition matrix P(X_k|X_k-1) where each row represents P(X_k) for a fixed value of P(X_k-1)
        In other words, the transition matrix T[i,j] is the probability of transitioning from state i to state j
        ONLY NEED TO COMPUTE THIS ONCE! This is because we are assuming that our transition model is not a function of time
        """
        
        T = np.zeros((self.size,self.size))

        for i in range(self.size):
            # i is the location we are assuming the robot to have been in at the previous time step

            # want a helper function to compute the 4 locations that the robot can get to from this location
            next_locs = self.get_legal_next_locations(i)

            for loc in next_locs:
                T[i][loc] += 0.25
        
        self.T = T
        self.T_transpose = np.transpose(T)
                

    def get_legal_next_locations(self, index):
        """
        Helper function for determining the probability distribution for the next state given the roadmap of the maze
        """

        x,y = self.index_to_location(index)

        # want to return a list of the where the robot could be next
        next_locs = []

        for dx, dy in self.directions:
            new_x, new_y = x + dx, y + dy
            if self.maze.legal_loc(new_x,new_y):
                next_locs.append(self.location_to_index(new_x,new_y))
            else:
                next_locs.append(self.location_to_index(x,y))

        return next_locs


    def index_to_location(self, index):
        """
        Locations in the Maze object consider (0,0) to be in the bottom left and (width,height) to be the top right
        We will label the spots that the robot could be in following this same structure
        index --> (x,y)
        """
        # get the location of where the robot is in the maze
        y,x = divmod(index, self.maze.width)
        return (x,y)

    def location_to_index(self,x,y):
        """
        (x,y) --> index
        """
        index = y*self.maze.width + x
        #print(f"Here is the cords: {(x,y)} | Here is the index: {index}")
        return index

    def construct_observation_matrixs(self):
        """
        Want to construct the observation matrix. P(e_k|X_k) for every possible value of X_k (how every many slots there are in the maze), what is the probability that we saw the color from the sensor
        - observed_data = {R,B,G,Y} is what the sensor picked up. Want to consider all of the locations on the board (row i is index i, just like it is in the T matrix)
            Does the color at this location match what we observed? If it does, then there is an .88 probability that we could be at that slot and otherwise its .04

        There are only 4 possible values for this matrix. can just precompute them and then call them as neede
        """
        self.observations = {}
        for observed_data in ["R", "G", "B", "Y"]:
            O = np.zeros(self.size)

            for i in range(self.size):
                # check what the color of the maze is at index i and see if it matches with the color we observed
                x,y = self.index_to_location(i)

                if self.maze.legal_loc(x,y): # want to make sure there isnt a wall here!

                    if self.perfect_information:

                        if observed_data == self.maze.get_color(x,y):
                            O[i] = 1
                        else:
                            O[i] = 0
                    else:

                        if observed_data == self.maze.get_color(x,y):
                            O[i] = 0.88
                        else:
                            O[i] = 0.04

            total = np.sum(O)
            O = O/total
            self.observations[observed_data] =  np.diag(O)


    def viterbi(self) -> list:
        """
        A DP algorithm that we can solve in O(TK^2) time where T is the number of time steps and K is the size of our variable space (in this case 16)
        As we predict the most likley sequence deeper and deeper into the timesteps, the probability of a sequence gets vanishingly small due to mult of numbers less than 1
        We take the log of each of the posteriors to transform small positive numbers into normal sized negative numbers. Monotonicity of log to the rescue!

        Observation Space Y--> Can either observe that the floor is {R, B, G Y}
        State Space --> The robot can be on any of the 16 tiles of the maze: {0,1,...,15}
        Prior Distribution (1x16) --> Assume a uniform prior
        Observation Sequence (1xT) --> What the robot actually observed as it was walking around the maze. A vector of [R,B,G,Y,G,...,]
        Transition Matrix (16x16) --> T, already computed!
        Emission Matrix (16x4) --> For each state (row), what is the liklihood that we observe a given color? (column)
        """
        
        Y = np.zeros(self.total_steps, dtype=np.int64)

        # First, we need to construct the observation matrix Y based on the colors that were observed from the sensor and our color to index map
        for i, color in enumerate(self.colors_observed):
            Y[i] = self.color_to_index[color]

        # We also need our Emission matrix
        E = self.construct_emission_matrix()
        

        # initilize DP tables; T_1 will be used to construct the most likley sequence at each time step and T_2 will be used to backtrack and obtain the globaly most likley solution
        T_1 = np.zeros((self.size,self.total_steps),dtype=np.int64)
        T_2 = np.zeros((self.size,self.total_steps),dtype=np.int64)

        # initilize the posterior for the first observation
        for state in range(16):
            # make sure that this state is a legal, reachable state
            tester = self.f_0[state] * E[state][Y[0]]
            if tester == 0:
                T_1[state][0] = -1000000000
            else:
                T_1[state][0] = log10(self.f_0[state]) + log10(E[state][Y[0]])

            T_2[state][0] = 0
        

        # outer loop goes over the length of the observation sequence. Graphically, we are moving to the right in our markov model
        for observation in range(1,self.total_steps):
            # at a given observation, we loop over each state the robot could be in 
            for state in range(16):
                max_prob_so_far = -1000000000 # this is the MAX --> will store this probability in T_1
                max_state_so_far = 0 # this is the ARGMAX --> will store this variable in T_2

                for k in range(16):
                    # if the probability of something is zero, 
                    tester = T_1[k][observation-1] * self.T[k][state] * E[state][Y[observation]]
                    if tester == 0:
                        transition_from_k = -1000000000
                    else:
                        transition_from_k = T_1[k][observation-1] + log10(self.T[k][state]) + log10(E[state][Y[observation]])
                    if transition_from_k > max_prob_so_far:
                        # update most likley previous state 
                        max_prob_so_far = transition_from_k
                        max_state_so_far = k

                T_1[state][observation] = max_prob_so_far
                T_2[state][observation] = max_state_so_far
        
        # now, we need to do the backtracking to consturct the best sequence of moves!

        # X will hold the sequence of most probably locations at each time step
        X = []

        # get the most probably location at the end of the robot walk
        most_likley_at_end = list(np.argmax(T_1,axis=0))[-1]
        X.append(most_likley_at_end) # axis 0 is col | axis 1 is row
        z_k = most_likley_at_end

        for timestep in range(self.total_steps-1,0,-1):
            z_kmin1 = T_2[z_k][timestep]
            X.append(z_kmin1)
            z_k = z_kmin1
        
        X.reverse()
        print(f"This is how many times the sensor got it right out of {self.total_steps}: {sum(self.sensor_correctness)}\n")
        print(f"Colors that the robot saw: {self.colors_observed}")
        print("_____________")
        print(f"Where did the sensor lead us wrong? {self.sensor_correctness}")
        print(f"Predicted: {X}")
        print(f"Ground Truth: {self.true_location[1:]}")


    def construct_emission_matrix(self):
        """
        Matrix constructed for viterbi forward pass. Enables us to incorperate the evidence obersed at that time step
        """
        E = np.zeros((self.size,4))
    
        for i in range(self.size):
            x,y = self.index_to_location(i)

            # want to make sure there isnt a wall here! If we cant legally be in a location, then we cant observe a color
            if self.maze.legal_loc(x,y): 
                # looping over the columns
                for color in ["R", "B", "G", "Y"]:


                    if self.perfect_information:
                        if color == self.maze.get_color(x,y):
                            E[i][self.color_to_index[color]] = 1
                        else:
                            E[i][self.color_to_index[color]] = 0

                    else:
                        if color == self.maze.get_color(x,y):
                            E[i][self.color_to_index[color]] = 0.88
                        else:
                            E[i][self.color_to_index[color]] = 0.04
        return E


def visualize_smoothing(data_points,average):
    plt.figure()
    for i, value in enumerate(data_points):
        if value > 0:
            plt.plot(i, value, 'go', markersize=1)  # 'go' means green color, circle marker
        elif value < 0:
            plt.plot(i, value, 'ro', markersize=1)  # 'ro' means red color, circle marker

    plt.xlabel('Time step')
    plt.ylabel('Impact of future observations')
    plt.title('Smoothing Analysis')

    plt.axhline(y=average, color='b', linestyle='--', label=f'Average: {average:.2f}')

    plt.grid(True)
    plt.show()

def test_random_walker(trails,steps):

    num_steps = []
    didnt_converge = 0
    total_steps = 0
    for _ in range(trails):
        solver = SensorRobotSolver(maze3, random_start=True, perfect_information=True, time_steps=steps)
        steps_to_converge = solver.forward_message()

        if steps_to_converge == None:
            s_x,s_y = solver.start_x, solver.start_y
            start_index = solver.location_to_index(s_x,s_y)
            num_steps.append((start_index, 0))
            didnt_converge += 1
        else:
            total_steps += steps_to_converge[1]
            num_steps.append(steps_to_converge)
    
    print(f"{didnt_converge} of the random walkers didnt converge with {steps} steps around the maze our of {trails} total random walkers")
    if didnt_converge == 0:
        print(f"Average Number of steps taken to converge: {total_steps/trails}")
    
    # now we have an array of tuples where the first element if the starting index and the second element is how many steps it took to finish

    start_location = [x[0] for x in num_steps]
    step_ = [x[1] for x in num_steps]
    plt.figure()
    plt.scatter(start_location, step_, color="g")
    plt.axhline(y=0, color='r', linestyle='--', label=f'Did not converge in {steps} steps')

    plt.xlabel('Start Location')
    plt.ylabel('Steps to Converge')
    plt.title('Random Walker Analysis')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    
    maze1 = Maze("no_walls.text", )
    maze2 = Maze("unique_neighbors.text")
    maze3 = Maze("wizard_of_oz.text")
    
    solver1 = SensorRobotSolver(maze1, random_start=False, perfect_information=False, time_steps=500)
    # solver1.filter()
    # solver1.smooth()
    # solver1.viterbi() # MAKE SURE YOU RUN FILTER BEFORE VITERBI! NEED TO GET ALL THE OBSERVATIONS

    solver2 = SensorRobotSolver(maze2, random_start=False, perfect_information=False, time_steps=500)
    # solver2.filter()
    # solver2.smooth()
    # solver2.viterbi() # MAKE SURE YOU RUN FILTER BEFORE VITERBI! NEED TO GET ALL THE OBSERVATIONS

    solver3 = SensorRobotSolver(maze3, random_start=False, perfect_information=False, time_steps=50000)
    # solver3.filter()
    # solver3.smooth()
    # solver3.viterbi() # MAKE SURE YOU RUN FILTER BEFORE VITERBI! NEED TO GET ALL THE OBSERVATIONS
 
    # CODE FOR VISUALIZING THE EFFECTS OF SMOOTHING. MAKE SURE TO RUN SMOOTHING BEFORE !
    # visualize_smoothing(solver1.smooth_boost_data,solver1.average_smoothing)
    # visualize_smoothing(solver2.smooth_boost_data,solver2.average_smoothing)
    # visualize_smoothing(solver3.smooth_boost_data,solver3.average_smoothing)
    

    # code to generate the number of steps taken for the robot to find out its location in the wizard of oz maze
    # test_random_walker(trails=500,steps=10)
    # test_random_walker(trails=500,steps=100)
    # test_random_walker(trails=500,steps=500)
    # test_random_walker(trails=500,steps=1000)
    # test_random_walker(trails=500,steps=2000)
    # test_random_walker(trails=500,steps=5000)
    # test_random_walker(trails=500,steps=10000)
        
