"""
Workhorse for General Boolean Satisfiability Solver. Class will take in a general Conjunctive Normal Form file and we able to output an assignment of the boolean variables such that it meets all constraints
"""
import random
from display import display_sudoku_solution
import time

class SAT:

    def __init__(self, cnf_file_path) -> None:
        
        # will represent each of the variables in an array, where the value at index i is 1 if variable (i+1) is True and 0 if it is False
        self.assignment = [0]*729 

        # create a map from the variables index in the assignment array to its representation in the output file
        # 2 --> 112
        self.variable_to_string = {}
        
        # set of the variables actually used for variables
        self.variables = set()
        
        # going to represent each contraint as a set in a list? Check if constraints are satisfied by looking over all and checking the index 
        self.constraints = self.convert_cnf_file(cnf_file_path) 


    def convert_cnf_file(self, filepath) -> list:
        """
        Need a function thats going to read the cnf file line by line and map each of the OR clauses into a constraint
        - We can represent constraints as a list of sets for sudoku. For each constraint, add a set in our list that represent the variables that are constrained
        - Split each of the variables by white space so we have a list of variable constraints that are in string format
            - Cast the string to an integer, pass it into the function that converts it to an index, and add it to the set. Do this for each line and keep adding sets to the constraint list
        """
        constraints = []
        cnf_file = open(filepath, "r")
        
        for clause in cnf_file:
            variables = clause.split()
            constraint = self.transform_to_constraint(variables)
            constraints.append(constraint)
        
        return constraints

    
    def transform_to_constraint(self, variables) -> set:
        """
        Need a function thats going to map the text representation of a variable like 112 or 993 to a numerical index
        - Variable is going to be a string representing of each the variable
        """
        # cast the string to an int
        constraint = set()
        
        for variable in variables:

            number = int(variable)
            is_neg = True if number < 0 else False

            # if we are dealing with a NOT variable, treat it as positive. Extract the digits from the string 
            if is_neg:
                number = -number
                dig_1, dig_2, dig_3 = int(variable[1]), int(variable[2]), int(variable[3])
            else:
                dig_1, dig_2, dig_3 = int(variable[0]), int(variable[1]), int(variable[2])
            
            index = (dig_1-1)*81 + (dig_2-1)*9 + dig_3
            self.variables.add(index)

            if is_neg: variable = variable[1:]
            self.variable_to_string[index] = variable

            constraint.add(-index) if is_neg else constraint.add(index)
        
        return constraint
    
    def walk_sat(self, max_iterations=1000000, threshold=0.3) -> bool:
        """
        Algorithm very similar to gsat.
        (1) pick a random assignment of the variables
        (2) check if this assignment meets all contraints. if not:
            (3) compute which constraints are not satisfied given this assignment and put them in a list (alter existing function for SAT)
            (4) pick one of these constraint sets at random. score these variables and flip the the best one using existing function
        """
        self.get_random_assignment()
        iters = 0
        while not self.is_SAT() and iters <= max_iterations:

            print(f" Number of constraints we have not yet satisfied: {len(self.not_satisfied)}")

            iters += 1

            random_float = random.random()
            if random_float > threshold:
                variable = random.choice(list(self.variables)) - 1
            else:
                # get a random constraint from the list of non satisfied constraints
                constraint = random.choice(self.not_satisfied)
        
                # pick the best variable out of this random unsatisfied constraint and flip it
                variable = self.score_variables(constraint)
            self.assignment[variable] = not self.assignment[variable]
        
        if iters > max_iterations and not self.is_SAT(): return False

        return True


    def gsat(self, max_iterations=1000000, threshold=0.3) -> bool:
        """
        (1) Choose an assignment of the variables at random. 
            get_random_assignment() --> Will do this by looping over each of the entries of the assignment and randomly generating a 1 or a 0

        (2) Check if this assignment satisfies all of the clauses (having a while loop here would be good)
            HELPER METHOD --> Loop over each set in the list the constraints. 
                For each of the varaibles in a constraint, check to see if they are positive or negative
                If positive, look at index val-1 and see if that value = 1, if negaitve see if value = 0. If not, return False. Do this for all constraints

        (3) Randomly generate a float x between 0 and 1. IF x > h, randomly choose an integer between 0 and 728 and change the value of that variable in the assignment

        (4) ELSE (x <= h) compute the number of clauses that would be satisfied if we flipped a given variable. Do this for every variable
            HELPER METHOD --> Loop over each variable in the assignment. 
                For each variable, switch its value and compute the number of constraints that are met. When done looking at each constraint, return variable to old value
                Keep track of the variables that are tied for the most constraints and the number of constraints they are meeting. If we find one with more, clear the set and include new max
                Randomly pick a variable index from this list after we have looped over everthing and return that index
        """

        self.get_random_assignment()
        iters = 0
        while not self.is_SAT() and iters <= max_iterations:
            iters += 1

            print(f"Iteration number: {iters}\n")

            random_float = random.random()

            if random_float > threshold:
                variable = random.choice(list(self.variables)) - 1
            else:
                variable = self.score_variables()

            self.assignment[variable] = not self.assignment[variable]
        
        if iters > max_iterations and not self.is_SAT(): return False

        return True

    def get_random_assignment(self) -> None:
        # for each boolean variable in the assignment, randomly pick either 0 or 1
        for index in range(729):
            self.assignment[index] = random.choice([False, True])
    
    def is_SAT(self) -> bool:
        """
        From the definition of cnf, we need at least one variable in each clause to be True. Once we find a variable that is True, we break out of the constraint and move onto the next one
        If we dont find a variable in the constraint that is True, then we return False
        """
        self.not_satisfied = []
        # loop over each constraint (set) in our constraints list
        for constraint in self.constraints:
            none_true = True
            
            # loop over each variable (integer) in the constraint (set)
            for variable in constraint:
                # if variable is positive, want to check at index (variable - 1) if the assignment is True
                if variable > 0: 
                    # if this variable should be True based on the constraints but its False, we dont have a valid assignment!
                    if self.assignment[variable-1]:
                        none_true = False
                        break
                
                # if variable is negative, want to check at index (variable - 1) if the assignment is False
                else:
                    variable = -variable
                    if not self.assignment[variable-1]:
                        none_true = False
                        break
            
            if none_true:
                self.not_satisfied.append(constraint)
        
        return len(self.not_satisfied) == 0

    def score_variables(self, constraint=False) -> int:

        # need a way to keep track of the variabless which meet the most constraints in a set and a variable that counts how many that is
        max_num_satisfied = 0
        best_variables = set()

        if constraint: 
            variables_to_consider = [abs(x) for x in list(constraint)]
        else:
            variables_to_consider = list(self.variables)
        # loop over each of the variables in the assignment
        for value in variables_to_consider:

            # variables kept in constraint list and index list are the variables not the look up index in the array
            index = value - 1

            # keep track of old value in the assignment
            old_value = self.assignment[index]

            # flip the value of variable (index +1) and temporarily plug it into the new assignment
            new_val = not old_value
            self.assignment[index] = new_val

            # compute how many assignments are satisfied with this new assignment
            num_satisfied = self.num_SAT()

            # if we found an assignment that has more constraints met than our best: 
            if num_satisfied > max_num_satisfied:

                # update best so far 
                max_num_satisfied = num_satisfied

                # make a fresh list with this index
                best_variables = set()
                best_variables.add(index)

            elif num_satisfied == max_num_satisfied:
                best_variables.add(index)
            
            # go back to are original assignment values before we try a different variable to flip
            self.assignment[index] = old_value
        
        # return a random index out of the list which satisfiy the most constraints
        return random.choice(list(best_variables))

    
    def num_SAT(self) -> int:
        """
        Given an assigment of the variables, count the number of constraints are satisfied
        """
        num_satisfied = 0
         # loop over each constraint (set) in our constraints list
        for constraint in self.constraints:
            
            # loop over each variable (integer) in the constraint (set)
            for variable in constraint:
                # if variable is positive, want to check at index (variable - 1) if the assignment is True
                if variable > 0: 
                    # if this variable should be True based on the constraints but its False, we dont have a valid assignment!
                    if self.assignment[variable-1]:
                        num_satisfied += 1
                        break
                
                # if variable is negative, want to check at index (variable - 1) if the assignment is False
                else:
                    variable = -variable
                    if self.assignment[variable-1]:
                        num_satisfied += 1
                        break
        
        return num_satisfied

    def write_solution(self, output_file_name="tester.sol") -> None:
        """
        Function to take an assignment of variables from the Boolean Solver and output them to a solution file
        """

        with open(output_file_name, "w") as output_file:
            for index in self.variables:
                variable_string_representation = self.variable_to_string[index] if self.assignment[index-1] else "-" + self.variable_to_string[index]
                output_file.write(variable_string_representation + '\n')


if __name__ == "__main__":
    random.seed(1)

    # PATHS TO DIFFERENT SOLUTUIONS 
    trivial = "one_cell.cnf"
    cell_test = "all_cells.cnf"
    row_test = "rows.cnf"
    row_and_col_test = "rows_and_cols.cnf"
    rules = "rules.cnf"


    game1 = "puzzle1.cnf" 

    # h = 0.5 --> Speed of Algo: DID NOT FINISH after 20 min with seed(1)
    # intuituon --> Too much randomness while walking around. Not able to pin point solution

    # h = 0.6 --> Speed of Algo: 60.1 with seed(1) 
    # h = 0.7 --> Speed of Algo: 155.3 seconds with seed1

    # h = 0.8 --> Speed of Algo: DID NOT FINISH after 20 min seconds with seed1
    # intuituon --> Not enough randomness. Gets stuck at local minima which is close to a solution but is not THE solution


    game2 = "puzzle2.cnf" 
    # h = 0.5 --> Speed of Algo: DID NOT FINISH with seed(1)
    
    # h = 0.6 --> Speed of Algo: 398 seconds with seed(1) 

    # h = 0.7 --> Speed of Algo: DID NOT FINISH  with seed(1) 

    gamebonus = "puzzle_bonus.cnf" # FAIL

    time1 = time.time()

    ### THIS IS WHERE WE CHANGE WHAT PUZZLE WE ARE TRYING TO SOLVE
    solver = SAT(cnf_file_path=game2)

    ### THIS IS WHERE WE CHANGE WHAT SOLVER WE USE 
    
    #result = solver.gsat(threshold=0.3) 

    result = solver.walk_sat(threshold=0.3) 

    print(f"Speed of Algo: {time.time() - time1}")

    if result:
        solver.write_solution(output_file_name="tester.sol")
        display_sudoku_solution("tester.sol")

    pass