# Andrew Koulogeorge
## Code Overview
CSP.py holds the general strcuture of how we model the CSP problem: an assignment of variables is represented as an array where $i$ is the variable number and $A[i]$ is the variables value, domains is a hashmap from variable to a set of possible values, and constraints is a hashmap from pairs of variables $(i,j)$ to a set of pairs of values $(x,y)$ where $A[i]=x, A[j]=y$ is a legal assignment of the variables $i$ and $j$. 

CSP_Aussie.py and CSP_CircuitBoard.py both expend the CSP class and their main purpose is to map their respective problems into th CSP format laid out in CSP.py.

CSP_Solver.py uses CSP an instance variable and contains all of the algorithms for solving the general CSP problem, randing from a simple approach to applying inference and heuristic techniques.

## CSP Solver
The solver uses an instance of CSP as well as keeps track of the number of calls made to backtrack for testing algorithm effiency. Lets walk through the backtracking algorithm first:

Our base case is when we have assigned a value to each variable. We keep track of a set of variables that have not been assined in a set in the CSP class which is always initilized to all the variables at the start. If this is empty, we return the solution. 

We check our input flags to see which clever tricks we should turn on or off.

For picking the next variable, if we are being naive then we will just cast the not assigned variable set to a list and pick the first element from it. If we are being clever, we use the MRV heuristic to find the variable that is most constrained.
    
For picking the next values, if we are being naive we consider the values in the order which they are being originally stored in our domain value. If we are being clever, we consider all of the values and order them based on which one is the least constrained. 

For inference, if we are being naive we dont consider how the most recent variable assignment effects other variables- we only care that it did not break any of the constraints locally. If we are being smart, we apply AC-3 and propogate the most recent assignment to all the other variables. If during inference we find that in fact this variable assignment was illegal, we change the domains of each of the variables back to their previous state, unassign the most recent value, and add this variable back to our set of unassigned variables! If this variable works, we recursivley call backtrack and assign a value to the next variable!


## Aussie Map Problem
I create a hashmap that enables us to go back and forth from the human readbable region names and colors to the array indexs and the value labels. This ensures consistent processing of the human readable input.

Domains: At the start, each region could be any color. Thus, the domain map's values are R,B,G for each of the regions

Constraints: For each region, no two can be the same. For each of the regions $(i,j)$, we loop over all color values where the two states dont have the same color and add them to the value of the constraints map at key=$(i,j)$.

When considering how the speed of the solution differs with various inference and heuristic techniques, I tracked both the number of backtrack function calls our solver makes by adding an instance variable to the class and incrementing it each time backtrack is called and I imported the time module to track how long each function call took. When testing, these metrics will be printed to the screen along with the solution. We observe that for the map problem, we dont observe signifcant time speed ups when we toggle the knobs for variable selection, value selection, or inference. Why might this be? First, due to the symetry of the problem, which specifc color any of the regions are does not matter. Put another way, the colors of the regions are arbitrary, and could be swapped around so long as no 2 regions that are connected have the same color. Therefore, there is a lot of possible solutions for the naive backtracking algorithm to find! Additionally, the graph of the aussie problem is very small. So, even when the naive backtrack does make an invalid assignment, it does not take very long for it to correct its mistake. In fact, when we use the smart inference and heuristic techniques, the solution ends up being slower because these clever algorithms take longer than the naive way!

Something thats very important to note is how much the order in which we input matters. With a very purposeful choice of input variables, we are effectivley encoding some heuristic! Therefore, we observe that the speed of the algorithm depends heavily input order. To combat this, I shuffle the order input before running backtrack. This is going to be very important for Circuit Board!

## Circuit Board Problem
The input is the dimensions of the board as well as the dimensions of each of the parts we need to place. We use ASCII charachters to label each of the parts. Just like in the Aussie Problem, the main work, now that we have the fully powered backtracking algorithm with all the clever tricks, is just to map the Circuit Board Problem to be a CSP. Then we will just throw it to the solver and be done!

Domains: For each of the parts we are given, each part needs to fit on the board and not fall off! With the assumption that each of the parts is rectangular, along with the big board, we can do some quick math to calculate all of the legal spots. Consider a big board of width n and height m and a part with width w and height h. Assuming that the part fits on the board in the first place, we know that we can shift over the part a distance of $n-w$ times and still have it be on the board. The same logic applies shifting vertically over a distance of $m-h$. Therefore, we know that we have $n-w+1$ legal horizontal locations for the part and $m-h+1$ legal values for the vertical componenet of the part (dont forget to count the starting location!). If we moved even a single slot beyond either vertically or horizontally, we would fall off the board. Thus, the cartesian product of these two sets of values gives all possible positions for the peice to be placed: $(x,y) = X ~x~ Y$ where $X =\{0,1,...,n-w+1\}~ Y =\{0,1,...,m-h+1\}$

Constraints: For every pair of parts that we could place on the board, we need to ensure that they are not taking up the same space! For every pair of parts (i,j), we loop over all legal positions for part $i$. For a given legal spot for part $i$, we consider all legal positions for part $j$. We compute with a helper function based on the parts current location, its dim, and the dim of the board exactly what locations on the board it is sitting on. I wrote $2$ helper functions for enabling us to easily index in and out of the board from location $(x,y)$ to index that we store in our assignment array. We store location values in sets and if $2$ variables every overlap, then we do not add those locations to our constraint map. The constraint map for circuit board takes exactly the same format as the one from the map problem! We have pairs of variables that are constrained as keys (i,j) and the value of each of these keys is a set that contains legal positions for part i and part j to be on the board while not intersecting. Thus, when we try and place a part on the board, we loop over all other parts we have already placed and ensure that the location we are placing the new part is in the legal set of values for all other parts.

 Constraints on the components a and b on a 10x3 board where part a has been given index $0$ and part b has been given index $1$. The dim of part a is $(3,2)$ and the dim of part $b$ is $(5,2)$. The board has $30$ total spaces on it labeled $0-29$ where $0$ is in the bottom left and $29$ is in the top right. Following the format explained, we have $(0,1)$ mapping to a set of values $(iVal,jVal)$ corresponding to legal spots where each of the parts can be placed without intersecting. Note how the solution has location $(0,3)$ which is in our set!

 (0, 1): {(17, 0), (5, 10), (17, 12), (0, 5), (10, 3), (11, 5), (2, 5), (0, 14), (11, 14), (16, 1), (10, 15), (7, 1), (1, 15), (16, 10), (6, 11), (7, 10), (5, 0), 
 (17, 2), (12, 15), (17, 11), (11, 4), (10, 5), (0, 4), (16, 0), (1, 5), (10, 14), (0, 13), (6, 1), (7, 0), (1, 14), (15, 10), (7, 12), (6, 10), (12, 5), (17, 1), (17, 10), (10, 4), (0, 3), (1, 4), (10, 13), (15, 0), (0, 15), (11, 15), (7, 2), (6, 0), (2, 15), (7, 11), (16, 11)}

 When considering the speed of different solutions based on our "clever" flags, we see a lot of variance. See the main method in the CSP_CircuitBoard.py file for several different test cases. We use various boolean flags to indicate when we want to turn on the clever logic in algorithm. These flags enable us to compare how the hueristics are doing! For each of the text cases, we will run the solver 5 times. See the main method in CSP_CircuitBoard.py. Once will all of the naive implementations, one call enabling each of the three clever tricks (one for MRV, one for LCV, and one for inference using AC-3), and then a final call using all 3 of the heuristics. We keep track of both speed and function calls. To make the output of the comparison easier, comment out the solution.print() in the tester function. See code comments for this. Lets compare!

*Testcase 1* (Example from assignment): Recall how the inital order of the input changes the way our naive methods will choose the next variable and value. for a problem thats as small as example 1, we dont see big differences in performance. If the input is "bad" and the naive method picks a variable first, it might make it backtrack a couple more times but the time will still be very quick becuase the problem is small. For the smart solution, it takes longer than all others but will never backtrack more than $4$ times. Its slower because the clever tricks take time to run. Another thing I noticed is if you have naive variable on with clever value, you are going to be picking a random variable and trying to pick the least constraining value for that random variable. This could slow down our search a lot of the variable we picked was wrong! Its like making our bad variable choice longer! See the non random example one for this.

*Testcase 2* (Bigger input with less solutions): Now that we have a larger search space and less possible solutions, the naive solution is much slower. Now that we have more variance in the outputs, let break each of them down. Note that for the middle 3 cases, we are only turning that cleverness on:

Naive --> 81 seconds and around 1.5 million function calls to backtrack

Smart Next Variable --> .0006 seconds and 13 calls to backtrack (Super, Super effective!)

Smart Next Value --> 196 seconds and 48,000 function calls. This is the same behavior we saw in example $1$ where we are being random about the next variable but then being "smart" about how we pick the next value. This can result in us going down wrong paths (hense the larger function calls) and also taking a lot of time because we have to sort the value which can be computationally heavy 

Inference --> 46 Seconds to run and ran 42081 times. See see that when we are not being smart about which variable to pick, we can still do a lot of work down the rabit hole. The lesson is that we need to not make mistakes early in the tree search! Thats what really costs us.

All Smart --> .1 seconds and function call of 13. We see this is about the same as Smart Next Variable, but it takes a little more time because of the overhead of some of the other clever algos being slow.

*Test case 3* --> All algos correctly pickup that we cant solve this one!

*Test case 4* --> Works even if we only have a single part to place

*Test case 5:*

Naive --> So slow that it cannot finish!

Smart Next Variable --> 0.008 seconds and only 19 function calls. Wow! Totally blows the Naive out of the water.

Smart Next Value --> So slow it cannot finish!

Inference -->  So slow it cannot finish!

All Smart --> 0.622 seconds and 18 function calls. The overhead due to the other, less effective tricks slows us down a little!


In conclusion, it appears that being smart about the order in which you pick your variables to assign in the most important part of a CSP solver. This makes sense- if you pick a bad variable early on, then you could go down the tree a very long way before you realize that this was a bad pick!

## CS1 Extra 
I did not have time to complete an entire solution and run test cases, but I was able to complete most of the CSP sub class for the Assignment Problem (See CSP_SectionAssignment.py) 

Work Completed:
1) I created a random generation function that, given the number of students, number of leaders, and how many slots you want each student to be free in, as well as how many days and times you want each student to consider, would output a list of times for each student and leader. The student and leader avalibility prefferences were expressed as a set of tuples (Day,Time) where Day and Time were both strings. Day varied from Monday to Friday (M-F) and Time varied from 9 - 8 with 30 min increments. 
2) The assignment array holds the student variables in the first n slots and the leaders in the rest of the slots. I keep both n and k as parameters of the class.
3) I create a function that enabled us to represent each (Day,Time) pair as a single index and constructed the domain of each of the students and leaders by making a call to this lookup table. Thus, the domain of each student/leader is a set of natural numbers (following the general structure of our CSP solver)
4) For the constraints, the global solutions about each section having a leader if there is a student in it and there being bounds on how many students can be in a section cannot trivially be expressed as binary constraints. I attempted to convert them to several binary constraints but it wasnt immediate how to do it. For the first constraint, however, we can ensure that all of the leaders are in different sections by looking over the variables from n to the end (only want to look at the leaders!) and considering all pairs of leaders. We add constraints to ensure that for all pairs of leaders, only legal values are ones where they are assigned a different section.
5) In the CSP_Solver_extra.py (I made an extra file not to screw with the existing solver, didnt want accidental bug. Had I finished, I would have merged the two into 1 Solver class) I included several instance variables for how I would have delt with these global constraints had I had more time. 

Outline of Full Backtracking Solution:
I would have created an array of sets with length equal to the number of section leaders and would have used a map from the slot number to the index of this sections array to acess a particular section. In these sections, I would have stored the students or leaders that were currently in that section. I also included a has leader and size_of_section array which would have used the same index as the sections list of sets. These two lists would have helped catch global constraint issues on the fly- being able to terminate early if there was ever more sections with no leaders in them then there were leaders as well as being able to terminate early if there was every more students in a group that n/k + 1.

Wish I had more time !