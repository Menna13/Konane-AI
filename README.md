## Konane
## Name: Menna Khaliel

## Classes: 

Konane consists of two classes: Board and konane. 
    - Board is the state class that includes information and instances of each state of the game, i.e board such as 
    size of the board, kind of pieces on the board, and locations of pieces on the board. It also hold the static evaluation funciton e
    
    - Konane class holds game play related functionalities such as initializing the board, choosing which hand to start first, 
    and giving size of the board. It also holds the MiniMax algorithm with alpha, beta pruning

## Breakdown of Board class: 
    Board class contains several classes:
    - BoardTypes: 
        class representing type of board with NEW and EMPTY. New denotes a new full board. EMPTY denotes an n x n empty board

    -Piece:
        class representing type of pieces in the game: DARK, and LIGHT 

    Board: 
        main class that initializes a state (board) and contains most of helpful functions

        - initializtion is default to a n x n new board
        
        Main methods: 
            - new_board: 
                - creates a n x n 2d array that represents a new board, either new or completly empty
                - only even board sizes are allowed
            
            -a_board:
                takes a list of dark pieces positions and light pieces positions, and populates and empty board with them. 

            -start_game:
                starts the game by removing the middle two pieces [4][4] and [4][5]
            
            -played_move:
                updates the state of the game with the given played move. It also checkes if this move is a legal move in the context of allowed moves for the corresponding player

            -reverse:
                reverses the player turn in the game state. For example, after first move, reverse is called to make game turn for Light player

            - opponent:
                a helpful method that returns the reverse of given piece. For example, if given DARK, opponent returns LIGHT

            - getLegalActions: 
                method that's given a piece type (LIGHT or DARK) and iterates through the 2d array representation of the board to find all legal moves of this piece. It maps every legal move to a list of opponent piece(s) that would be removed if such move is played
                This method returns a dictionary of key as a tuple of (from_tile, to_tile) and value as list of removed opponent pieces

            -getPiecePositions:
                a helpful method that returns a list of all current positions of a given piece type 


### Static Evaluation function (e):
    Board class includes also e, the static evaluation function. 

    The static evaluation function evaluates a board state based on the number of edge pieces available for a piece type in the current game state. The method outputs a score that's based on the number of current pieces of given piece type in the game state. 
            
## Breakdown of Konane class: 
    Konane class contains most of the functions needed for game play. The initialization creates a board with a given piece turn and size of board. It also defines the type of maximization piece, which is the AI piece, aas well as depthBound needed for MiniMax algorithm. It also starts the game. 

    Game class:
        Main methods of Game Class:
            -printBoard:
                a helpful method to print any given board 

            -printPossibleMoves:
                a helpful method to print available moves for a player and can be referenced with an index

                this method also takes the user input of an index representing chosen move to be played. If it's the AI turn, however, it runs MiniMax and sends the returned move to be played

            -getMove: 
                a helpful method to trace a move node returned by MiniMax in order to find the desired move

            -MiniMaxAlphaBeta:
                MiniMax algorithm that takes a game state (board) , alpha and beta, depth which represents current depth, move which is a node that keeps track of parent moves executed to get to that node, and piece which represents which player

                The implementation of MiniMax algorithm is the standard implementation. Successors are created through getting legal moves and for everyone, creating a deep copy of game state and executing every each one. A best move node is then returned and traced till it has no parent move. Hence it's our chosen move

            -play:
                method that starts the game and runs while the game is not over. It prints board after each move, as well as possible moves for a player and their chosen move. It also declares end of game and reverses turns after each move.

            -choose_a_stone_and_size() 
                helpful method that simulates choosing a hand in Konane and deciding on a starting player

            - __main__ method: 
                runs choose_a_stone_and_size to decide on board size and type of user piece, and runs the game with a specifc depth for MiniMax algorithm

