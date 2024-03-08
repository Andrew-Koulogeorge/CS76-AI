# Andrew Koulogeorge: 9/17/2023

"""
FoxProlem Class contains some more general functionality:
    - Variable Boat Size
    - Goal and Start State
    - Total number of Foxes and Chickens can be different than the start State
"""
class FoxProblem:
    def __init__(self, max_boat_size = 2, start_state=(3, 3, -1), goal_state = (0,0,1),total_chickens = 0, total_foxes = 0):

        if total_chickens and total_foxes: # if a custom number of chickens and foxes are passed in, set totals accordingly
            self.total_foxes, self.total_chickens = total_chickens,total_foxes
        else: # otherwise, set equal to the starting number 
            self.total_foxes, self.total_chickens,_ = start_state
            
        self.max_boat_size = max_boat_size
        self.start_state = start_state
        self.goal_state = goal_state

    """
    Given a current state in the game, this function returns a set of the the next possible legal states
    """
    def get_successors(self, state):

        valid_out_neighbors = set() # set that will hold the valid next states
        left_fox,left_chicken, boat = state # extract information from state

        for delta_fox in range(self.max_boat_size+1):
            for delta_chicken in range(self.max_boat_size+1):
                # ensure there is at least 1 Fox or chicken in the boat and no more than the size of the boat
                if (delta_fox > 0 or delta_chicken > 0) and (delta_fox + delta_chicken <=self.max_boat_size): 
                    next_state = (left_fox + boat*delta_fox, left_chicken + boat*delta_chicken, -boat)
                    if self.is_valid(next_state): valid_out_neighbors.add(next_state)
        
        return valid_out_neighbors

    """
    Returns True if state is legal and False otherwise
    """
    def is_valid(self,state): 
        left_fox,left_chicken, _ = state
        right_fox, right_chicken = self.total_foxes - left_fox, self.total_chickens - left_chicken 

        # not a legal state if the fox or chicken count is ever larger than total or negative
        if (left_fox > self.total_foxes or left_fox < 0 or left_chicken > self.total_chickens or left_chicken < 0): return False

        # checking if there are ever more foxes than chickens on a side with at least 1 chicken
        if (left_fox > left_chicken > 0) or (right_fox > right_chicken > 0): return False

        return True

    """
    Returns True if state is the goal and False otherwise
    """
    def is_goal(self,state):
        return state == self.goal_state
    
    def __str__(self):
        string =  "Foxes and chickens problem: " + str(self.start_state)
        string += "\n"
        string += "Total number of foxes in this game: " + str(self.total_foxes)
        string += "\n"
        string += "Total number of chickens in this game: " + str(self.total_chickens)
        string += "\n"
        string += "Max boat size: " + str(self.max_boat_size)
        return string

if __name__ == "__main__":
    test_cp = FoxProblem(start_state = (3, 3, -1))
    print(test_cp.get_successors(state = (3, 3, -1)))
    print(test_cp)
