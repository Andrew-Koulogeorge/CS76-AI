"""
Script representing the Circuit problem as a subclass of our CSP problem
"""
from CSP_Solver import CSP_Solver
from CSP import CSP
from collections import defaultdict
import time
import random


class CSP_CircuitBoard(CSP):
  
    def __init__(self, board, parts):
        self.width, self.height = board

        self.problem_name = "Circuit Board Problem"

        # keep a dict for output that maps the index of the part to an ASCII letter
        self.array_loc_to_letter = {}
        letter_code = ord("a")

        # can keep a dictonary that maps the dim of the parts to there variable index
        self.part_lookup = {}

        self.part_representation = "\nPART DIM --> ASCII LETTER REPRESENTATION!\n"
        
        for i, part in enumerate(parts):
            self.part_lookup[i] = part
            letter = chr(letter_code)
            self.array_loc_to_letter[i] = letter

            self.part_representation += f"{part} --> {letter} \n"
            letter_code += 1

        assignment, domains, constraints = self.transform_to_CSP(parts)

        # maps the index where each part is at to its location on board (human readable)
        value_lookup = self.index_to_loc_map()

        super().__init__(assignment, domains, constraints, self.part_lookup, value_lookup)
    

    def transform_to_CSP(self, parts):
        """
        Given the dim of the big board as well as the dim of all the parts that we have to place on the board, we need to 
        Map the problem to a general CSP. That is, we need to construct:
        1) Variables -->  We will have len(parts) variables where each value will be the the bottom left corner of the rectangular part placed in the big board
        2) Domains --> We will compute each of the domains of each the parts based on the dim of the board and the dim of the part
            part --> set containing the legal locations for the part on the board
        3) Constraints --> Each of the variables will be constrained against each other --> No two parts placed on the board can intersect
                index of 2 parts (i,j) --> set of tuples (A,B) where A is the lower left index of part & B is the lower left index of part j
        """
        num_parts = len(parts)

        # CONSTRUCT VARIABLES #
        assignment = ["*"]*num_parts

        # CONSTRUCT DOMAINS #
        domains = defaultdict(set)

        part_number = 0
        for part_width, part_height in parts:
            # take the difference between the board width and the part_width, height and part_height
            diff_width, diff_height = self.width - part_width, self.height - part_height
            
            for x in range(diff_width + 1):
                for y in range(diff_height + 1):
        
                    # grab index of the location on the board and store it in the domain of this part
                    index = self.get_index((x,y))
                    domains[part_number].add(index)
            
            part_number +=1


        # CONSTRUCT CONSTRAINTS  #

        constraints = defaultdict(set)
        
        # looping over each pair of parts
        for p1 in range(num_parts):
            for p2 in range(p1+1,num_parts):

                # given these two part indexs, lets grab the part dims (x,y) cord pairs
                part1, part2 = self.part_lookup[p1], self.part_lookup[p2]

                # now we want to loop over all possible locations that each of the parts can take on. these legal values lie in there domain!
                for legal1 in domains[p1]:
                    for legal2 in domains[p2]:

                        if not self.intersecting_parts(part1,legal1,part2,legal2):
                            constraints[(p1,p2)].add((legal1,legal2))
        
        return (assignment,domains,constraints)



    def intersecting_parts(self,part1,index1,part2,index2):
        """
        part is of the form (x,y) where x is the width of the part and y is the height of the part
        Given part1 at index loc1 on the board and part2 at index loc2, are the two parts intersecting eachother?
        """

        # given the location of part 1 and its dim, we can compute the indexs on the board that it is covering up

        # get the x,y cords
        x_1,y_1 = self.get_location(index1)
        x_2,y_2 = self.get_location(index2)

        # get the width and height of the parts
        width1, height1 = part1
        width2, height2 = part2

        # we know the locations that this part takes up is from (x_1 to x_1 + width1 - 1) and (y_1 to y_1 + height1 - 1)
        # loop over all of these values, get there index, and put them in a set. 
        covered_by_part1 = set()
        for i in range(x_1, x_1 + width1):
            for j in range(y_1, y_1 + height1):
                index = self.get_index((i,j))
                covered_by_part1.add(index)

        for i in range(x_2, x_2 + width2):
            for j in range(y_2, y_2 + height2):
                index = self.get_index((i,j))
                if index in covered_by_part1: return True

        return False
    
    def get_index(self,location):
        """
        Need a function that, given a (x,y) cord on the board, we can map it to a single index. 
        We consider the bottom left of the board to be (0,0) and the top right to be (width,height)
        """
        x,y = location
        return x + y*self.width
    

    def get_location(self,index):
        """
        Want to be able to go back to the cords from the index. 
        """
        y, x = divmod(index,self.width)
        return (x,y)
    
    def index_to_loc_map(self):
        map = {}
        for i in range(self.width):
            for j in range(self.height):
                loc = (i,j)
                map[self.get_index(loc)] = (i,j)
        return map

    def print_circuit_solution(self):
        """
        Given the assignment of the solutions, the width of each part, there letter code, and the width of the board,
        display what the solution looks like!
        """

        # first, lets make a list of all . and then print it out as a test
        # THE CORDS OF THE BOARD ARE GOING TO MATCH UP WITH THE BOTTOM LEFT CONVENTION !!!

        ascii_board = [["." for _ in range(self.width)] for _ in range(self.height)] 

        # need to fill in the board for each part
        placement = "ASCII LETTER REPRESENTATION --> LOWER LEFT CORNER OF PART ON SOLUTION BOARD\n"
        for part_index, part_loc_index in enumerate(self.assignment):
            # get the letter corresponding to this parts num
            part_letter = self.array_loc_to_letter[part_index]
            part_width, part_height = self.part_lookup[part_index]
            x, y = self.get_location(part_loc_index)

            placement += f"{part_letter} --> ({x},{y})\n"

            for i in range(y, y + part_height): 
                for j in range(x, x + part_width):
                    ascii_board[i][j] = part_letter
        
        
        board = self.board_to_string(ascii_board)

        print(self.part_representation)        
        print(placement)
        print(board)
        print("What a pretty board!\n")

        
    def board_to_string(self, ascii_board):
        """
        Given a matrix with the parts filled in, print them out in ascii format!
        """
        output = f"FILLED IN BOARD THATS IS {self.width} x {self.height}! \n"
        for i in range(self.height-1,-1,-1):
            row = ""
            for j in range(self.width):
                row += ascii_board[i][j]
            output += row
            output += '\n'
        return output

def tester(board, parts, naive_next_var=True, naive_next_val=True, naive_inf=True):
    """
    Code to automate testing different parts and board dims
    """
    problem = CSP_CircuitBoard(board,parts)
    solver = CSP_Solver(problem)

    start_time = time.time()
    solution = solver.backtrack(naive_next_var,naive_next_val,naive_inf)
    print(f"It took {time.time()-start_time} to run and I called the backtracking algorithm {solver.states_visited} number of times!\n")

    if solution == "Failure":
        print("Not possible!")
    else:
        print("Possible!")
        #### FOR COMPARING SOLUTIONS, COMMENT THIS LINE OUT ! #####
        solution.print_circuit_solution()
        pass

    #print(solution.constraints)

        
if __name__ == "__main__":
    ### IT MATTERS A LOT THE ORDER IN WHICH THE INPUT IS PLACED IN! IF WE GIVE IT A GOOD INPUT, THIS THIS IS A LITTLE BIT LIKE STARTING OFF WITH A GOOD HEURISTIC

    # randomness is baked into the naive solutions!

    # TEST CASE 1 (from assignment)

    # board1 = (10,3)
    # parts1 = [(3,2),(5,2),(2,3),(7,1)]
    #both solutions are very fast for a simple board like this! naive even a little faster
    # print("All Naive:\n")
    # tester(board1,parts1) 
    
    # print("Smart Next Variable:\n")
    # tester(board1,parts1,False,True,True)

    # print("Smart Next Value:\n")
    # tester(board1,parts1,True,False,True)
    
    # print("Inference:\n")
    # tester(board1,parts1,True,True,False)

    # print("All Smart:\n")
    # tester(board1,parts1,False,False,False)

    # TEST CASE 2 

    # board2 = (7,7)
    # parts2 = [(1,1),(2,3),(2,1),(1,1),(1,4),(3,2),(1,4),(1,3),(2,3),(3,1),(3,1),(2,3),(2,2)]
    # print("All Naive:\n")
    # tester(board2,parts2) 
    
    # print("Smart Next Variable:\n")
    # tester(board2,parts2,False,True,True)

    # print("Smart Next Value:\n")
    # tester(board2,parts2,True,False,True)
    
    # print("Inference:\n")
    # tester(board2,parts2,True,True,False)

    # print("All Smart:\n")
    # tester(board2,parts2,False,False,False)


    # TEST CASE 3 (solver correctly labels when a solution is not possible)
    # board3 = (4,4)
    # parts3 = [(5,5)]
    # print("All Naive:\n")
    # tester(board3,parts3) 
    
    # print("Smart Next Variable:\n")
    # tester(board3,parts3,False,True,True)

    # print("Smart Next Value:\n")
    # tester(board3,parts3,True,False,True)
    
    # print("Inference:\n")
    # tester(board3,parts3,True,True,False)

    # print("All Smart:\n")
    # tester(board3,parts3,False,False,False)


    # # TEST CASE 4 (solver correctly plops down the single part)
    # board4 = (6,6)
    # parts4 = [(6,6)]
    # tester(board4,parts4)

    # # TEST CASE 5 (tuff solution!)
    board5 = (10,10)
    parts5 = [(1,1),(1,3),(9,1),(5,1),(7,1),(3,1),(1,2),(1,2),(5,1),(5,5),(5,1),(5,1),(5,1),(5,1),(5,1),(2,1),(2,2),(7,1)]

    # print("All Naive:\n") TOO SLOW !
    # tester(board5,parts5) 
    
    print("Smart Next Variable:\n")
    tester(board5,parts5,False,True,True)

    # print("Smart Next Value:\n") TOO SLOW !
    # tester(board5,parts5,True,False,True)
    
    # print("Inference:\n") TOO SLOW !
    # tester(board5,parts5,True,True,False)

    print("All Smart:\n")
    tester(board5,parts5,False,False,False)

    pass


