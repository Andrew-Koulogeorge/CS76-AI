# Chess Report
## Minimax 
We see that for the basic MinimaxAI, the number of minimax calls grows extrememly quickly. For any depth larger than $3$, the algorithm gets rather slow. At depth $4$ its still possible butslower... after just a few moves at depth 4, Minimax is looking at over $1$ million states! At a depth of 5, the MinimaxAI has no shot of even finding the first move. (I waited it out... it called minimax $10,190,798$ times! See test_chess.py for examples)

## Evaluation Function
To estimate the quality of a board without looking to a terminal state, I used the material evaluation function. As an implementation detail, I assume that white is always seeking to maximize the score on the board and black is always trying to minimize it. We pass into all our choose move functions a boolean which selects if its white or blacks turn to move. Based on this flag, we are able to start the minimax call either maximizing or minimizing according to if its white or blacks turn to move. This functionality is built into the ChessGame file where we keep track of whose turn it is and pass it in as a parameter to choose move.

If white has won, I return $1000$ (larger than the sum of all the material, signaling to the AI that this is always the best move. Also positive because white is maximizing!) and $-1000$ for black. If its a draw I return $0$. Otherwise, we loop over all of the material on the board and check if its white or black. I keep a lookup table as an instance variable of the class and sum the total material value of the white and black peices. By taking the difference, we get a approximation for the quality of the position! For example, big material advantage for white = positive number from evaluation function = good position, which is consistent with our white player who is trying to maximize the score!

## Looking for Intelligence
--- > At max depth 1, we see that the AI is not able to see ahead on its moves; it acts greedily and tries to take any material that it can! It pays the price for its inability to look ahead and I take the knight with my queen.
```text
__________________________
EXAMPLE 1 (look at .md file)

r n b q k b r .
p p p p p p p p
. . . . . . . n
. . . . P . . .
. . . . . . P .
. . . . . . . .
P P P P . P . P
R N B Q K B N R
----------------
a b c d e f g h

Black to move
```

MinimaxAI Made 19 moves to find the move h6g4 while searching to a depth of 1
```text
r n b q k b r .
p p p p p p p p
. . . . . . . .
. . . . P . . .
. . . . . . n .
. . . . . . . .
P P P P . P . P
R N B Q K B N R
----------------
a b c d e f g h

White to move
```

```text
r n b q k b r .
p p p p p p p p
. . . . . . . .
. . . . P . . .
. . . . . . Q .
. . . . . . . .
P P P P . P . P
R N B . K B N R
----------------
a b c d e f g h
__________________________
```
--- > With a little bit deeper of a depth, the AI is able to see that this is a bad idea and does not capture!

__________________________
```text
EXAMPLE 2 
r n b q k b . r
p p p p p p p p
. . . . . . . n
. . . . . . . .
. . . . P . P .
. . . . . . . .
P P P P . P . P
R N B Q K B N R
----------------
a b c d e f g h

Black to move
```text
 MinimaxAI Made 13481 calls to minimax to find the move f7f6 while searching to a depth of 3
```text
r n b q k b . r
p p p p p . p p
. . . . . p . n
. . . . . . . .
. . . . P . P .
. . . . . . . .
P P P P . P . P
R N B Q K B N R
----------------
a b c d e f g h

White to move
__________________________
```

--- > The Minimax AI does take easy wins. In this example we see the AI finds the mate in 1!
```text
__________________________
EXAMPLE 3 (look at .md file)
r n b . k b n r
p p p . p p p p
. . . . . . . .
. . p . . . . .
. . . . P q . .
P . . . . P . .
P P P P B . . P
R N . Q K B N R
----------------
a b c d e f g h
```
Black to move

 MinimaxAI Made 29054 calls to minimax to find the move f4h4 while searching to a depth of 3
```text
r n b . k b n r
p p p . p p p p
. . . . . . . .
. . p . . . . .
. . . . P . . q
P . . . . P . .
P P P P B . . P
R N . Q K B N R
----------------
a b c d e f g h
```
White to move
0-1
__________________________

## Iterative deepening
For each move in iterative deepening, we print out how many calls were made to Minimax for this depth level and we also output what the AI thinks is the best move for that partiuclar depth. In the following example, we see evidence that the AI is doing what humans call "calculation" and trying to weigh tradeoffs with taking vs not taking a particular peice. We can see that with only a depth of 1, the AI cannot take into account what the other player is going to do so the AI votes to take the pawn on g4. With a depth of 2, it sees that if it did indeed capture the pawn, then it would love a peice more valuable than a pawn to whites queen (weather they take with the rook or knight does not realy matter). With a depth of 3, however, the AI is able to see that indeed that square g4 would be protected by another one of its peices and the AI would be able to capture whites queen if it took back. Thus, the AI swtiches its move choice back to the greedy strategy and takes the pawn!
```text
__________________________
r n b q k b r . (look at .md file)
p p p p p p . p
. . . . . . . n
. . . . . . . .
. . . P P P P p
. . . . . . . .
P P P . . . . .
R N B Q K B N R
----------------
a b c d e f g h
```
Black to move

 MinimaxAI Made 24 moves to find the move None while searching to a depth of 3
Picked our first move : g8g4 

 MinimaxAI Made 830 moves to find the move g8g4 while searching to a depth of 3
Found a new move! Now the AI bot wants to move g8h8 instead of g8g4

 MinimaxAI Made 21345 moves to find the move g8h8 while searching to a depth of 3
Found a new move! Now the AI bot wants to move g8g4 instead of g8h8
```
r n b q k b . .
p p p p p p . p
. . . . . . . n
. . . . . . . .
. . . P P P r p
. . . . . . . .
P P P . . . . .
R N B Q K B N R
----------------
a b c d e f g h
__________________________
```

## Alpha-Beta Pruning
With a depth of 5, vanilla alpha-beta pruning is able to make a first move in around a second. With a depth of 6, alpha-beta returns a move in around 10 seconds (around the same time as it takes standard to do 4). This kills the standard Minimax we were working with before that was not even able to compute 5 moves deep.

Let us consider a randomly generated board that is well developed. For the same depth, we want to ensure that our alpha beta search is doing its job and cutting away branches that we know are bad. We consider both Minimax and AlphaBeta from this location with the same depth and compare the moves found by both AIs. Its great news to see that our two AI's found the same move and that Alpha Beta did it in signifcantly less calls. This is what we want!
```
__________________________
r . b q . r k . (look at .md file)
p p p . p p b p
. . n p . n . .
. B . . . . p .
. . . . P . . .
. . N P . N P .
P P P . Q P . P
R . B . . R K .
----------------
a b c d e f g h
```
Black to move

MinimaxAI Made 39436 calls to minimax to find the move c8h3 while searching to a depth of 3 

```text
r . . q . r k .
p p p . p p b p
. . n p . n . .
. B . . . . p .
. . . . P . . .
. . N P . N P b
P P P . Q P . P
R . B . . R K .
----------------
a b c d e f g h
__________________________
__________________________

r . b q . r k . (look at .md file)
p p p . p p b p
. . n p . n . .
. B . . . . p .
. . . . P . . .
. . N P . N P .
P P P . Q P . P
R . B . . R K .
----------------
a b c d e f g h
```
Black to move

AlphaBetaAI Made 2545 calls to minimax to find the move c8h3 while searching to a depth of 3 
```text
r . . q . r k .
p p p . p p b p
. . n p . n . .
. B . . . . p .
. . . . P . . .
. . N P . N P b
P P P . Q P . P
R . B . . R K .
----------------
a b c d e f g h
__________________________
```
What if we tried to increase the depth of both of the AIs? Well, we know that the standard Minimax cannot see anything past 4 layers. For a position that is as complicated as this one, it will be even worst. What about Alpha Beta? It does not disappoint! We can see from the iterative deepening output of the algorithm, the algorithm is able to identify a stronger move than the one at 3 layers deep by leveraging its ability to search deeper in the tree.
```text
__________________________
r . b q . r k . (look at .md file)
p p p . p p b p 
. . n p . n . .
. B . . . . p .
. . . . P . . .
. . N P . N P .
P P P . Q P . P
R . B . . R K .
----------------
a b c d e f g h
```text
Black to move

Picked our first move : f6e4 

AlphaBetaAI Made 33 moves to find the move f6e4 while searching to a depth of 1

Found a new move! Now the AI bot wants to move c6b8 instead of f6e4

AlphaBetaAI Made 198 moves to find the move c6b8 while searching to a depth of 2

Found a new move! Now the AI bot wants to move c8h3 instead of c6b8

AlphaBetaAI Made 2545 moves to find the move c8h3 while searching to a depth of 3

Found a new move! Now the AI bot wants to move c8g4 instead of c8h3

AlphaBetaAI Made 15246 moves to find the move c8g4 while searching to a depth of 4

Found a new move! Now the AI bot wants to move g5g4 instead of c8g4

AlphaBetaAI Made 332254 moves to find the move g5g4 while searching to a depth of 5

Found a new move! Now the AI bot wants to move c8g4 instead of g5g4

AlphaBetaAI Made 1510983 moves to find the move c8g4 while searching to a depth of 6
```text
r . . q . r k .
p p p . p p b p
. . n p . n . .
. B . . . . p .
. . . . P . b .
. . N P . N P .
P P P . Q P . P
R . B . . R K .
----------------
a b c d e f g h
__________________________
```
What if we tried to use our ordering theory on this complicated position? We would hope that by ordering the childen nodes in Alpha Beta, that we would be able to chop off more branches of the tree and significantly reduce our search time. Indeed, this is exatly what we see! We end up making over 1 million less calls to Minimax by sorting the next states by which states look most appealing for the current player (based on the evaluation function). Note that the fact that the two different AIs found different moves for this board does not mean there is a wrentch in the code. At each level, the AI starts a brand new search. If two states have the same evaluation function score, then whichever move that comes first will be the move that is played by the AI. Since in the OrderingAI we order each of the actions before we consider which one to explore, the order in which we explore actions is different and thus the two AIs could just have discovered 2 moves with equal evaluation score in different orders!
```text
__________________________
r . b q . r k .
p p p . p p b p
. . n p . n . .
. B . . . . p .
. . . . P . . .
. . N P . N P .
P P P . Q P . P
R . B . . R K .
----------------
a b c d e f g h
```
Black to move

Picked our first move : f6e4 

AlphaBetaAIOrdering Made 33 moves to find the move f6e4 while searching to a depth of 1

Found a new move! Now the AI bot wants to move c6b4 instead of f6e4

AlphaBetaAIOrdering Made 138 moves to find the move c6b4 while searching to a depth of 2

Found a new move! Now the AI bot wants to move c8h3 instead of c6b4

AlphaBetaAIOrdering Made 1302 moves to find the move c8h3 while searching to a depth of 3

Found a new move! Now the AI bot wants to move g5g4 instead of c8h3

AlphaBetaAIOrdering Made 5729 moves to find the move g5g4 while searching to a depth of 4

We are staying with our current best move g5g4

AlphaBetaAIOrdering Made 44435 moves to find the move g5g4 while searching to a depth of 5

We are staying with our current best move g5g4

AlphaBetaAIOrdering Made 233037 moves to find the move g5g4 while searching to a depth of 6
```text
r . b q . r k .
p p p . p p b p
. . n p . n . .
. B . . . . . .
. . . . P . p .
. . N P . N P .
P P P . Q P . P
R . B . . R K .
----------------
a b c d e f g h
__________________________
```

## Transposition table
For the transposition table, instead of trying to use a native python set to store each of the boards, I used a dictonary which maps the hashed value of the board string to the most recent look up value. We never need to store terminal state values in the table because there is no recursive work thats required for those boards. We add a value to the table when before we bottle up the Chess tree and return the minimax value of a node to its parent. Before we look into a nodes children, we check the table to see if we have seen this state before. If we have seen it, we are able to just return the value of the board in our hashtable using the key index from hashing the string representation of the board.

Lets now see an example where our transposition table prevent calls in minimax or alpha-beta. I created another random and very complex board so it takes the AIs a little bit more time to find the moves. Note that for the first $3$ depths of the search, the number of function calls for both AIs are the same. This could be because of the complexity of the board given. For only a few moves ahead, its possible that there was no way to reach the same board with a different move ordering. Note, however, that as as the depth grew to 4 and 5, the transposition table prevented almost 1 million function calls! This makes a lot of sense. As we are looking deeper and deeper down the tree, there are going to be more paths the same state using different move orders. Yay! Also, both AIs got to the same move! Looking great!
```text
__________________________
r k r . . . . .
p . . . p p b p
. p n p . n . .
q . p . . . B .
B P . P P . b .
P . P . . N P .
. . . N Q P . P
R . K R . . . .
----------------
a b c d e f g h
```
Black to move

Picked our first move : a5a4 

AlphaBetaAI Made 42 moves to find the move a5a4 while searching to a depth of 1

We are staying with our current best move a5a4

AlphaBetaAI Made 891 moves to find the move a5a4 while searching to a depth of 2

We are staying with our current best move a5a4

AlphaBetaAI Made 8895 moves to find the move a5a4 while searching to a depth of 3

We are staying with our current best move a5a4

AlphaBetaAI Made 500736 moves to find the move a5a4 while searching to a depth of 4

We are staying with our current best move a5a4

AlphaBetaAI Made 3,251,589 moves to find the move a5a4 while searching to a depth of 5
```text
r k r . . . . .
p . . . p p b p
. p n p . n . .
. . p . . . B .
q P . P P . b .
P . P . . N P .
. . . N Q P . P
R . K R . . . .
----------------
a b c d e f g h
__________________________
r k r . . . . .
p . . . p p b p
. p n p . n . .
q . p . . . B .
B P . P P . b .
P . P . . N P .
. . . N Q P . P
R . K R . . . .
----------------
a b c d e f g h

Black to move
```
Picked our first move : a5a4 

AlphaBetaAITable Made 42 moves to find the move a5a4 while searching to a depth of 1

We are staying with our current best move a5a4

AlphaBetaAITable Made 891 moves to find the move a5a4 while searching to a depth of 2

We are staying with our current best move a5a4

AlphaBetaAITable Made 8895 moves to find the move a5a4 while searching to a depth of 3

We are staying with our current best move a5a4

AlphaBetaAITable Made 473946 moves to find the move a5a4 while searching to a depth of 4

We are staying with our current best move a5a4

AlphaBetaAITable Made 2,302,334 moves to find the move a5a4 while searching to a depth of 5
```text
r k r . . . . .
p . . . p p b p
. p n p . n . .
. . p . . . B .
q P . P P . b .
P . P . . N P .
. . . N Q P . P
R . K R . . . .
----------------
a b c d e f g h
__________________________
```
# Litturature Review
It is important to understand the history of problems. For example- Why do we care about this problem? What are ways people have tried to solve this problem in the past? How are people currently solving this problem? How do these solutions compare to eachother? What are the reasons for new solution emergence? In this section, I will be reading and reviewing (in my opinion) the two most important computer science papers in the history of Chess AI. The first is from Shannon where he kicked off the discussion of Chess AIs and proposes some inital methods. The second is from Silver, a Reinforcement Learning expert from Deep Mind, who proposes what is today considered to be the dominant (and very generalizable) method for training AI to win at deterministic, perfect information games. Both of these texts are extremely technical and dense so I will be highlighting key and interesting results and ideas from both papers.

As a side note, attached to the zip drive is my annotated copies of the two papers (Just wanted to prove I didnt just GPT-4 this xD)

## Programming a Computer for Playing Chess (CLAUDE E. SHANNON)
Shannon starts his paper by noting that studying the game of chess itself is pointless, but that the ideas developed in Chess AI's would act as a wedge for other applicable AI problems. He then proceeds to list $8$ very applicable AI use cases, all of which are possible by computers today! Pretty cool foreshadowing. Shannon belived Chess was a good proxy becuase of the judgement and general principles required to win.

Shannon briefly talks about a first attempt at making a chess playing machine from 1914 where someone made a machine that was able to play a Rook and King endgame. The rook was able to always checkmate the king no matter what! While this example did not display any judgment by the AI, it did foreshadow ideas such as lookup tables that were used in world champion Chess AIs like Stockfish. 

Shannon provides some interesting theoretical arguments about the set up of the game of chess. He cites von Neumann's proof that since Chess is a deteriministic game, each board position, assuming perfect play, is either won, lost, or a draw. He argues that if one could define this function that computes the value of the state, that a machine could easily play any game perfectly by simply choosing an action that maximizes the value of $f$. Due to the massive size of the state space of chess, which he estimates to be around $10^{120}$, Shannon claims that coming up with this function for chess isnt practicle, even though theoretically possible. Thus, the problem at hand is to define a Chess AI that is better than humans, not an optimal one. [as a side note, he also proves that white would at least tie in every game if you changed the rules of chess to enable a player to pass on a move. Very elegant argument. See pdf.]

Shannon introduces evaluation functions and even provides an example of one thats very similar to the one used in this assigment (difference in material of pieces, along with some other information). He shows how these evaluation functions are worthless in situations where there are lots of captures awaiting, as there will be a lag of the evaluation of the position (function of the board right now cants quantify what it will look like after exchanges). He also begins to talk about the intuition behind the Minimax Algorithm with the two players switching off moves. He then defines this search as a Type A search --> A search where we search we a given depth and then compute the value based on $f$

Shannon goes on in the paper to talk about some implemetation ideas as well as improvements! I am super tired and going to end my review here xD


## Mastering Chess (and Shogi) by Self-Play with a General Reinforcement Learning Algorithm (David Silver)
In this paper the authors present AlphaZero, a generalized Reinforcment Learning algorithm for training chess AIs to dominate the games of Chess, Shogi, and Go. Remarkably, AlphaZero is able to achive this level of dominance from a completely clean state- nothing besides the rules of the game are told to the AI. This element of taking a "fresh start" approach to the game of chess is fundementally different than the previous chess AI champion such as Stockfish which has encoded into it lots of human knoledge and belif about what is a good and bad state. Using this "tabula rasa" approach and only $4$ hours of training time, AlphaZero outperformed stockfish. When playing against eachother 100 times in tournement style play, AlphaZero won $28$ games and lost $0$.

As a side note, *Reinforcement Learning* (RL) is a type of machine learning technique that enables an agent to learn in an interactive environment by trial and error using feedback from its own actions and experiences. It differs from traditional machine learning in that there are rewards and punishment signals assigned to behaviors. It also does not require labeling of input and output data points. The goal of a RL model is to find an optimal policy that enables it to map its states to actions such that its reward function is maximized. I honestly dont know very much about RL, but even with the most basic description, you can see how it would be very applicible for games such as chess. 

Upon reviewing the high level anatomy of the Stockfish chess AI, it is amazing to discover that fundementally it is extremely similar to the program that is construced in this assignment. Now, that is not to say my Chess AI is going to take down world champions anytime soon. But in general, Stockfish is what I beleive to be an extremely optimized, fully loaded up with bells and whistles version of the program in this assigment:

Stockfish Overview: 
1) Stockfish represents each state as a vector of human designed features which encode human knoledge about which states are strong and which are not. These features include midgame/endgame-specific material point values, mobility and trapped pieces, pawn structure, king safety, outposts, bishop pair, and other "ideas" about what people think make up a good or bad position on the board. The evaluation of the position is then a linear combination of these features with a vector of weights thaat are both manually and automatically tuned. There is a lot of complexity in this model and hundreds of years of chess experience baked into it, but fundementally it is still just using heuristics like the difference in the board material to try and evaluate position.
2) Stockfish uses Alpha-Beta pruning as its main search algorithm along with several other pruning tricks (including null move pruning which we talked about in class. This idea says that a state is very strong if its still strong conditioned on the current player not moving!)
3) Stockfish uses a transposition table to reuse values and move orders when the same location has been reached with a different path (just like we do, although im sure theres is implemented more efficently)
4) Stockfish uses a robust opening and endgame book that provides optimal moves given specifc board configuations.

Two mindblowing facts: (1) Chess programs such as DeepBlue, the chess AI that shocked the world by beating Garry Kasparov has "very similar architectures" even though many of the bells and whistles differ considerably. (2) None of the above techniques were used by AlphaZero.

Before we dive into AlphaZero, its important to understand the context of the time when Silver wrote this paper. Deep Mind had just developed a Go AI that beat the number one player in the world (an accomplishment many thought years before to be completely impossible). That program, AlphaGo, used Deep Convolutional Neural Networks and took advantage of special properties of the game of Go. The rules of Go are invarient to both board rotations and relections. AlphaGo was able to utilize this property during training by augmenting equivement positions into the dataset as well as randomly applying an invariant action on the board to reduce the bias of the Neural Networks training. Silver wanted to apply the ideas of AlphaGo to games like Chess where we dont have nice properties about symmetry. The goal was to train a single AI using generalizable ideas that could dominate in Go, Chess, and Shogi. And thats what they did!

AlphaZero Overview: 
(1) Instead of using human informed knoledge to represent the quality of a state, AlphaZero uses a Deep Neural Network $f$ with parameters $\theta$. Given any state, AlphaZero returns both a probability and a value estimating the expected outcome from the given state. These probabilities and values are all learned from self play and then utilized during its search.
2) Instead of using Alpha-Beta pruning, AlphaZero uses Monte-Carlo Tree Search (MCTS). MCTS is prefered over Alpha-Beta pruning for Go AIs because Go has such a large branching factor that its not really possible to run Alpha-Beta pruning. The basic idea is to value a state based on the average value of many simulated completed games from the current state. The most basic MCTS algorithm does not use any heuristic evaluation function at all. AlphaZero, however, used $f$ to select a next state to "playout" or simulate. The parameters $\theta$ are trained by playing out games with MCTS and recording the results of the game based on if it was a win, loss, or tie. The values of $\theta$ are updated to minimize the error between the models predicted outcome for a move and its true outcome.

Two more mindblowing facts about the AlphaZero AI: (1) AlphaZero searchs $1000x$ less positions per second than Stockfish. It is able to make up for its lower number of state evaluations by using a $f$ to focus on the most promising move variations. (2) Since AlphaZero was trained from a blank page, Silver was able to analyze how the knoledge of AlphaZero scaled as a function of training time. It is shown in the paper that AlphaZero discovers on its on popular chess openings that have been played by chess masters for hundreds of years. This result has intresting philosophical implications in my opinion. Using formal logic and computation, an AI was able to deduce similar conclusions about the game of chess in a matter of hours, while it took human kind hundreds of years.

It is interestingœ to see that for a very long time the underlying scientific methods underlying Chess AI's were similar; from Shannon to DeepBlue to Stockfish. Enabled by advances in parellel computing (the GPUs that help to train these large models), data avalibility, and the Residual Connection (ResNet) enabling very deep networks in Computer Vision applications, among others, Deep Mind and Silver were able to revolutionize the methodologies used in State of the Art Chess AIs.
