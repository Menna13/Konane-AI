import random
from Board import BoardTypes
from Board import Piece
from Board import Board
from random import shuffle, randint

class Game:
    def printBoard(self, game: Board):
        print('   ', [str(i)  for i in range(1,9)], '\n')
        for i in range(1,len(game.board)):
            print(i,":" , game.board[i][1:], '\n')

    def printPossibleMoves(self, moves: list, player: str):
        for i in range(len(moves)): 
            print (i ,": ", moves[i])
        
        if player == 'User':
            print("Please input index of chosen move")
            move = input()
        else:
            move = randint(0,len(moves)-1)
        assert int(move) in range(len(moves)), "Invalid index"
        return moves[int(move)]

    def __init__(self, user_piece: Piece) -> None:
        game= Board(turn = Piece.DARK)
        self.play(game, user_piece)



    def play(self, game: Board, user_piece: Piece):
        game.start_game() #remove first two pieces
        self.printBoard(game)
        roles = {user_piece: 'User', game.opponent(user_piece): 'AI'}
        legal = game.getLegalActions(game.turn)

        while len(legal) != 0:
            move = self.printPossibleMoves(list(legal.keys()), roles[game.turn])
            game.played_move(move[0], move[1], game.turn)
            game.reverse()
            legal = game.getLegalActions(game.turn)
            print("Played Move: ", move, '\n')
            self.printBoard(game, '\n')
        game.reverse()
        print(roles[game.turn], " WINS!")


#############################
# FRAMEWORK TO START A GAME #
#############################
def choose_a_stone():
    print("Choose a Hand")
    x = input()
    hands = [Piece.DARK, Piece.LIGHT]
    index = {'L' : 0, 'R': 1}
    shuffle(hands)
    if x != 'L' and x != 'R':
        raise Exception("Invalid Input: ", x, "Please choose right R or left L hand")
    if hands[index[x]] == Piece.DARK:
        print("Dark: You get start move")
    else:
        print("Light: AI gets start move")
    return hands[index[x]]

if __name__ == '__main__':
    """
    The main function called when pacman.py is run
    from the command line:

    > python konane.py

    See the usage string for more details.

    > python pacman.py --help
    """
    user_piece = choose_a_stone() 
    Game(user_piece)

    # pass
        






# if __name__ == '__main__':
#     game= Board(turn = 'User', board=BoardTypes.NEW )