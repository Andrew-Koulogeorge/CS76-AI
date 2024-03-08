"""
INCOMPLETE EXTRA CREDIT
"""
from CSP import CSP
from math import inf
from collections import deque
import copy
import random

class CSP_Solver_Extra:

    def __init__(self, csp:CSP, is_assignment=False):
        # takes in problem instance
        self.csp = csp
        self.states_visited = 0

        # instance variables for the assignment problem
        self.is_assignment = is_assignment

        if self.is_assignment:
            """
            INCOMPLETE EXTRA CREDIT --> made instance variables for how we would check the global constraints
            """
             # will keep a dict to map the slot number to the index of where we are keeping track of that section
            self.slots_to_index = {} 
            
            # create a section for each leader of that section. We cannot have more sections than leaders!
            self.sections = [set() for _ in range(self.csp.k)]

            # keep track of which section has a leader and which one does not 
            self.has_leader = [False for _ in range(self.csp.k)]

            # keep track of how many people are in each section.
            self.size_of_section = [0 for _ in range(self.csp.k)]

            self.max_group_size = (self.csp.n // self.csp.k) + 1
            self.min_group_size = (self.csp.n // self.csp.k) - 1
    
    def backtrack(self, naive_next_variable, naive_next_values, naive_inference):
        # if we have given values to every variable, return the csp
        if len(self.csp.not_assinged) == 0: return self.csp
        
        self.states_visited += 1

        # get the next variable we are going to assign (depending on if we want to be smart or not)
        if naive_next_variable:
            variable = self.naive_next_variable()
        else:
            variable = self.MRV_next_variable() 
        
        # loop over different values that the variable can take (maybe in a LCV manner, depending on if we want to be smart or not)
        if naive_next_values:
            next_values = self.naive_next_value(variable)
        else:
            next_values = self.LCV_next_value(variable)

        for value in next_values:
            
            # check if assigning variable <-- value is legal under the constraints
            if self.is_assignment_legal(variable, value):

                # make a copy of the domains we have before this variable assignment
                old_domains = copy.deepcopy(self.csp.domains)

                # if it is, add this value to the current assignment & update our tracker of variables that have not yet been assigned!
                self.csp.assignment[variable] = value
                self.csp.not_assinged.remove(variable)

                self.csp.domains[variable] = {value}

                # We could not do inference on this assignment and just chug along, trying other variables. 
                if naive_inference:
                    legal = True 
                else:
                    # or, update the values that other variables can take on given this assignment. Will return True if this assignment is legal and False otherwise
                    legal = self.AC_3_inference()

                #print(f"Here are the current domains.{self.csp.domains}")
                #print(f"Legal is {legal}")

                if legal:
                    solution = self.backtrack(naive_next_variable,naive_next_values,naive_inference)
                    if solution != "Failure":
                        return solution
                    
                self.csp.domains = old_domains
                self.csp.assignment[variable] = "*"
                self.csp.not_assinged.add(variable)
                # dont forget to remove this from the domain possibility! We know this aint it.
                self.csp.domains[variable].remove(value)
        
        return "Failure"


    def naive_next_variable(self):
        """
        Naive way of picking the next variable we are going to assign
        """
        return list(self.csp.not_assinged)[0]


    def MRV_next_variable(self):
        """
        Used when searching for the next variable to assign a value to. Returns the variable with the smallest legal domain
        """
        
        most_constrained_variable = -1
        min_options_so_far = inf

        # loop over the variables that have not yet been assigned a value
        for var in self.csp.not_assinged:
            # if this variable is more constrained than any we have seen so far (domain of legal values smaller than min so far)
            if len(self.csp.domains[var]) < min_options_so_far:
                # update variable and min options
                most_constrained_variable, min_options_so_far = var, len(self.csp.domains[var])
        
        return most_constrained_variable
    

    def naive_next_value(self,var):
        """
        Just returns the variables that are unassigned
        """
        return list(self.csp.domains[var])

    def LCV_next_value(self,var):
        """
        Used when determining which values for a given variable we should try first.
        Given a variable var, loop over all possible values that it can legally take on (elements currently in its domain)
        For each variable, compute how many choices this assignment rules out for neighboring variables (variables that var is in the constraints map with)
        """ 

        constrained_and_vals = []
        # loop over all possible values that this variable can take on
        for value in self.csp.domains[var]:
            # number of legal combinations choosing value for var creates. 
            num_constrained = 0

            # given a value, want to compute the number of possibilites assigning var <-- value removes. 
            
            # loop over other variables (neighbor nodes)
            for other_var in self.csp.not_assinged:
                if other_var != var:

                    if (var, other_var) in self.csp.constraints:
                        # loop over the possible legal combinations for these two variables
                        for legal_val, legal_other_val in self.csp.constraints[(var, other_var)]:

                            # if we are constraining legal_other_val because value 
                            if legal_other_val in self.csp.domains[other_var] and legal_val != value:
                                num_constrained += 1


                    elif (other_var, var) in self.csp.constraints:
                        # loop over the possible legal combinations for these two variables
                        for legal_other_val, legal_val in self.csp.constraints[(other_var, var)]:
                            
                            # if we are constraining legal_other_val because value 
                            if legal_other_val in self.csp.domains[other_var] and legal_val != value:
                                num_constrained += 1
            
            constrained_and_vals.append((num_constrained,value))
        
        # sort the array of tuples by the number of constrained possibilities
        constrained_and_vals.sort()
        
        return [x[1] for x in constrained_and_vals]
    

    def is_assignment_legal(self, x, x_val):
        """
        Check if assignment of x_val to variable x does is consistent with all other previously assigned variables
        """

        # loop over the variables that x is constrained with which we have already assigned
        for y in self.csp.directed_constraint_graph[x]:
            if y not in self.csp.not_assinged:  
                # if there is a constraint between these two variables
                if (x,y) in self.csp.constraints:
                    # check if value for x and the current value for y are valid for this constraint
                    if (x_val, self.csp.assignment[y]) not in self.csp.constraints[(x,y)]: 
                        # if they are not, this is not a legal assignment !
                        return False
                
                elif (y, x) in self.csp.constraints:
                    # check if value for variable and the current value for other val are valid for this constraint
                    if (self.csp.assignment[y],x_val) not in self.csp.constraints[(y, x)]: 
                        # if they are not, this is not a legal assignment !
                        return False

        return True
    
    def naive_inference(self):
        """
        Does not propogate the restrictions on other variables based on our new assignment. Just keeps searching!
        """
        return True
    
    def AC_3_inference(self):
        """
        Algorithm to handle Arc Consistency between variables in the csp. 
        We will keep a queue of "edges" which we will represent as two variables in our csp that are constrained
        We will start with the keys of our constraint map for our Q (including both ways since the algo works on a directed graph)
        At each iteraion, we will remove the two variables from the Q (x,y):
            Loop over each of the elements in the domain of x, v_x:
                Loop each of the elements in the domain of y, v_y:
                    See if there exists a value v_y such that (v_x,v_y) is a legal value under the constraint between (x,y)
                    If there is not, then remove v_x from the domain of x and add every 
        """
        # make a copy of the domains we have before this variable assignment
        queue = deque()
        # init the queue to hold constraints between all variables that are constrained. 
        # considering the constraints to be directed so add both ways
        for x,y in self.csp.constraints.keys():
            queue.append((x,y))
            queue.append((y,x))
        
        # while we still need to check consitensy for some pair of variables
        while queue:
            # consider a pair of variables
            x,y = queue.popleft() 

            # revise the domains of the variables x and y
            made_changes_to_domain_x = self.revise(x,y)
            if made_changes_to_domain_x:

                # if there are no more legal options that x can take on, there is no solution to our problem and we return False!
                if len(self.csp.domains[x]) == 0:
                    #print(f"We failed, going to restore the old domains: {old_domains}")
                    return False
            
                # otherwise, we need to look over all other constraints that are not y that and add the edge z --> x to the queue. Need to make sure we did not just delete a value another variable was depending on
                for z in self.csp.directed_constraint_graph[x]:
                    if z != y:
                        queue.append((z,x)) 
        
        return True

    def revise(self,x,y):
        """
        Checking the consistency of x --> y. Loop over the domains of x and check if 
        there exists a value in the domain of y that meets constraints
        """

        # loop over the domain of x. we make a copy because we are going to be editing the values in the domain
        copy_of_D_x = self.csp.domains[x].copy()

        # have we made any changes to the domain of x?
        made_changes = False

        # looping over possible values for x
        for val_x in copy_of_D_x:

            # does there exists a val_y that satisfies the constraints with val ?
            legal_match = False

            # checking each val_y looking for a match with val_x
            # dont need to make a copy because we are not making any changes to domain of y
            for val_y in self.csp.domains[y]:

                # how are we storing the constraint between (x,y) in our map? 
                order = -1
                if (x,y) in self.csp.constraints: order = True
                elif (y,x) in self.csp.constraints: order = False

                assert order == True or order == False

                if order:
                    if (val_x,val_y) in self.csp.constraints[(x,y)]:
                        legal_match = True
                        break
                else:
                    if (val_y,val_x) in self.csp.constraints[(y,x)]:
                        legal_match = True
                        break
            
            if not legal_match:
                self.csp.domains[x].remove(val_x)
                made_changes = True
        
        return made_changes


