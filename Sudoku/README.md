# Andrew Koulogeorge | Sudoku


## SAT.py Overview
The SAT class takes a path to a .cnf file and has several instance variables to help solve the Sudoku puzzle:

(1) *assignment*, similar to the CSP solver, represents each of boolean variables and there value. As noted in the implementation details, we represent the $729$ variables between $1$ and $729$ so we can use the negative of each of these numbers to represent the NOT of that variable (not possible if we $0$ index!). Thus, index $i$ in *assignment* corresponds to variable $i+1$. The value of *assignment* at index $i$ is True/False if variable $i+1$ is True/False. Note that SAT always represents every variable even if not every variable is constrained in the .cnf file

(2) *variable_to_string* is a hashmap that helps us keep track of the string representation for each variable. This comes in handy for when we write the solution output

(3) *variables* is a set thatkeeps track of the actual variables we used for a given .cnf file. For some of the earlier and simpler examples, we dont always have to consider the value of every variable.

(4) *constraints* is a list of sets where each set in the list contains a single constraint. Each element of the set is an integer x where the abs(x) coresponds to the variable x. If x is negative its NOT(x). 

We map the cnf file to the *constraints* list with the helper function *convert_cnf_file*:

(1) We read in each line of the cnf file which represents the OR of several variables. We split each of the variables into an array where each entry is its own variable and then apply and indexing function to transform each string representation of a variable to an integer between 1-729.
(2) If the variable in string form starts with a "-", this variable is NOTed and we store it as a negative number in the constraint.
(3) We compute the variable of each string with the function (dig_1-1)*81 + (dig_2-1)*9 + dig_3 where dig_i is the ith digit of the constraint. We then add this constraint set to our master list


## GSAT
My implementation directly follows psudocode from wiki and the problem set. Paramters max_iterations upper bounds how long we can search for a solution before we terminate and threshold is the value we use to determin a random action. Overview of each helper function:

(1) *get_random_assignment* loops over all possible variables in assignment and randomly picks True or False for each.
(2) Enter a while loop that continues so long as we have not found a solution and we have not exceeded the max iteration count. We check constraint satisfcation with *is_SAT* which just loops over each constraint and checks if any of the clauses have $0$ true variables. If such a clause exists, return False otherwise return True.
(3) We randomly generate a float between $0$ and $1$. If this value is larger than our threshold, we randomly pick a variable from our variable set. Recall that we store the variables starting at $1$ in the constraints for "NOT" reasons but we look up there assignment value starting at $0$ so we need to shift this value to the left $1$.
(4) If our random float is not above the threshold, we call *score_variables* to select a variable.
(5) Whichever variable we select, we flip its value and then return to While loop.

*score_variables* keeps a set *best_variables* which satisfy the most constraints if they are flipped. Depending on if we are doing GSAT or Walk_SAT we consider a different set of variables to flip. If its GSAT, we consider all the variables for this game (which is why we keep the *variables* IV). Looping over each variable, we see how many conditions would be satisfied, X, if we flipped its value. We use the helper function *num_SAT* which is very similar to *is_SAT* just with an integer return instead of boolean. If X is larger than the largest we have seen so far, we empty our current best index set and make a fresh one that only includes the best new variable. If the best so far equals X, we add the current variable to our set. Note that before we consider another variable, we reset the value of the variable under consideration! Only are going to change one variable at a time- looking for how many constraints are satisfied if we JUST change a single variable. After we have considered all variables, we pick a random variable from *best_variables* to flip and return it.

## WalkSAT
As is noted in the assignment, WalkSAT is very similar to GSAT. The main difference is that when we check if a given assignment is satisfied, we store all of the unsatisfied clauses in a list and randomly pick a clause from this list to narrow down our variable consideration universe. Thus, instead of considering all variables we only consider the ones in a given set. We then score these variables the same way we scored them in GSAT.

## Commentary on Solutions
Since each of these Boolean Solvers are randomized algorithms, I use the Time module as well as printing out how many constraints have yet to be satisfied for each iteration of the solver. I then tested, for a given random seed, how the outputs vary as a function of the randomness threshold.

I found that for the puzzle1.cnf, WalkSAT with a threshold of .6 solved it in $1$ min and for puzzle2.cnf WalkSAT with  a threshold of .6 solved it in around $6$ min. I found that when the threshold was too low there was to much random action and the solver wasnt able to get the number of constraints left down low enough, at least in a short amount of time. Intuitivly, more randomness means that the solver spends more time searching around the space. While this might lead to the solution taking longer to complete, it should be more robust to eventually finding a solution. I found that when the threshold was too high, it got bottle necked into a "local minimum" and the number of constraints left to meet would hover around $1$ but we would never solve the puzzle outright.

As the assignment said, my GSAT does not solve any of the constraints outside of the first couple. My WalkSAT solution do not appear to solve the bonus puzzle.

See the main method for SAT.py for testing and expirimental results laid out in the comments. Solutions for puzzle1 and puzzle2 have been written to the puzzle1.sol and puzzle2.sol files.



## Optimizing the Conjunctive Normal Form Representation of Sudoku (Annotated pdf attached)
I think a really cool part of this assignment is the representation of Sudoku in cnf. I think this is a super nontrival thing to come up with! I am going to explain the conditions and then review a paper which talks about a way to optimize the cnf encoding for Sudoku that is able to solve much larger problems.

Given an $9x9$ Sudoku board, how many clauses do we have in our standard conjunctive normal form? We can break down this into 2 cases: $1$ case for generating the single cell conditions and another for the row, column and box conditions. 

For each cell on the board, it could be any value 1-9. Take (1,1) as an example. This is a single condition: (111 112 ... 119). When we ensure that no box takes more than one element, we need to ensure no pair of variables are both True. If this happened, we would have $2$ numbers in one box! Since the order of the values does not matter, we have $\binom{9}{2}$ pairs which we need to NOT (-111 -112 ... -118 -119). Thus, we have $(1 + 36)*81 = 2,997$ clauses for the cell condition.

For the row, column, and box condition, we first observe that for there needs to be exactly $1$ of each value in every row, column and box. We represent these conditions by forcing each row, col and box to have a $1$, and to have a $2$, and ... all the way to $9$. We do this by considering that any value could be in any of the elements in each row, col and box. Let us look at the example for a row.

Row --> 111 121 ... 191 (1 needs to go in row 1)
        112 122 ... 192 (2 needs to go in row 1)
        .
        .
        .
        119 129 ... 199 (9 needs to go in row 1)

Forcing at least $1$ element in each row to be each of the $9$ possible values in conjuncture with the condition that no cell can take on more than one value results in the condition that each row must have a unique value! Thus, we have $9$ clauses for a given row and we have $9$ rows which is $81$ clauses. Its not hard to see that the column and box case are exactly symmetric to the row case $\implies~ 81*3 = 243$! 

Thus, the total number of clauses for a $9x9$ board is $2,997 + 243 = 3240$. If we scroll all the way down in our rules.cnf file, we see that this combinatorial argument checks out!

What if we wanted to generalize Sudoku to a board larger than $9x9$? How would the number of clauses scape if the board was $n ~x~ n$?

For our first cases, we have $(1 + \binom{n}{2})*n^2$ where $\binom{n}{2} = O(n^2)$. For our second case, we have $3*n^2$. Thus, the first case dominates the second assymptotically in terms of clause generation and the number of clauses generated given a $n ~x~ n$ board is $O(n^4)$

This is pretty bad! In "Optimized CNF Encoding for Sudoku Puzzles", Kwon and Jain attempt to reduce the number of clauses created by exploiting information given to the puzzle by fixed cells. Observe that in our own implementation of the Sudoku solver, the algorithm used to map the cnf form to the constraints and variable list is the same for the cases when we have fixed cells and when we dont. Kwon and Jain use this additional information to reduce the number of clauses in a given problem before the cnf form is handed off to a solver.

Kwon and Jain motivate this research in Table 1, where they show that given $3$ different ways to encode a Sudoku board, all of them hit a stack overflow error when the puzzles grow beyond $49~x~49$. There method is able to avoid stack overflows by having an intermediate step before solving begins where they can remove entire clauses or variables of the cnf based on the fixed values.

For example, lets say we know that the given board starts with a 9 in the square (1,1). What does this information tell us about other clauses in our csf? Any other variables representing the square (1,1) must be false. Thus, the $\binom{n}{2}$ clauses that were generated to ensure that the square $(1,1)$ does not take on multuple values all are True! Additionally, the clause asserting that one of the values needs to fill the square $(1,1)$ is also always True since we know 119 is True. 

Any clause that has a truth value due to the fixed cell need not be checked at any time during the solvers algorithm since the value of the fixed cell will never change. Additionally, any variable thats proven to be False can be removed from a clause. This yeilds a logically equivalent cnf which represents the sudoku puzzle at hand and that has significantly less clauses and variables to consider!

When emperically testing there results, Kwon and Jain were able to solve an $81~x~81$ puzzle in a fraction of a second while other cnf representations could not solve it at all. They were able to reduce the number of clauses in a cnf compared to another popular encoding by an average of 79x.

