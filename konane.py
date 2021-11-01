#ToDO handle errors to allow continuation of game


from collections import defaultdict
from math import pi
import random
import copy
from Board import BoardTypes
from Board import Piece
from Board import Board
from random import shuffle, randint

class MoveNode:
    def __init__(self, from_tile, to_tile, parent):
        self.from_tile = from_tile
        self.to_tile = to_tile
        self.parent = parent

    def getParent(self):
        return self.parent


class Game:
    
    def __init__(self, user_piece: Piece, size: int, depthBound: int) -> None:
        self.game= Board(turn = Piece.DARK, size =size)
        self.depthBound = depthBound
        self.maxNode = self.game.opponent(user_piece) #AI is always a max piece
        self.play(self.game, user_piece)

    def printBoard(self, game: Board):
        print('   ', [str(i)  for i in range(1,game.size+1)], '\n')
        for i in range(1,len(game.board)):
            print(i,":" , game.board[i][1:], '\n')

    def printPossibleMoves(self, moves: list, player: str):
        for i in range(len(moves)): 
            print (i ,": ", moves[i])
        
        if player == 'User':
            print("Please input index of chosen move")
            move = input()
            return moves[int(move)]
        else:
            #ToDO move chosen is given by AlphaBeta
            print("AI is: ", self.maxNode)
            s_eval, move = self.MiniMaxAlphaBeta(self.game, float('-inf'), float('+inf'), 0, None,self.maxNode)
            # move = randint(0,len(moves)-1)
            parent = self.getMove(move)
            for i in moves:
                if (parent.from_tile, parent.to_tile) == i:
                    print("found move")
                    break
                else:
                    print("move not found")
        # assert int(move) in range(len(moves)), "Invalid index" 
            return (parent.from_tile, parent.to_tile)
    
    def getMove(self,node):
        cur = node
        while cur.parent != None:
            
            cur = cur.parent
            
        return cur


    def MiniMaxAlphaBeta(self, n, a, b, depth, move, piece: Piece):
        #TODO: what is a terminal node? 
        # print("depth is:" , depth)
        if depth == self.depthBound or n.endGame(piece):
            # copied_board = copy.deepcopy(self.game)
            # move = MoveNode( , , move)
            return (n.e(piece), move)

        moves = list(n.getLegalActions(piece).keys()) 
        # print(moves)
        if piece == self.maxNode:
            # print("piece is: ", piece, "oppo is:", self.game.opponent(piece))
            bestMove= None
            for move_i in moves:
                ####deep copy 
                successor = copy.deepcopy(n)
                successor.played_move(from_tile= move_i[0], to_tile= move_i[1], piece=piece)
                node = MoveNode(move_i[0],move_i[1], move)
                bv, move = self.MiniMaxAlphaBeta(successor, a,b, depth+1, node,self.game.opponent(piece))
                if bv > a:
                    a = bv
                    bestMove = move
                if a >= b:
                    return (b, bestMove)
            return (a, bestMove)
        #if piece is min node
        else:
            # print("piece is: ", piece, "oppo is:", self.game.opponent(piece))
            bestMove = None
            for move_i in moves:
                successor = copy.deepcopy(n)
                successor.played_move(from_tile= move_i[0], to_tile= move_i[1], piece=piece)
                node = MoveNode(move_i[0],move_i[1], move)
                bv, move = self.MiniMaxAlphaBeta(successor, a,b, depth+1, node,self.game.opponent(piece))
                if bv < b:
                    b = bv
                    bestMove = move
                if b <= a:
                    return (a, bestMove)
            return (b, bestMove)

    def play(self, game: Board, user_piece: Piece):
        game.start_game() #remove first two pieces
        self.printBoard(game)
        roles = {user_piece: 'User', self.maxNode: 'AI'}
        legal = game.getLegalActions(game.turn)

        while len(legal) != 0:
            move = self.printPossibleMoves(list(legal.keys()), roles[game.turn])
            game.played_move(move[0], move[1], game.turn)
            game.reverse()
            legal = game.getLegalActions(game.turn)
            print("Played Move: ", move, '\n')
            self.printBoard(game)
        game.reverse()
        print(roles[game.turn], " WINS!")


#############################
# FRAMEWORK TO START A GAME #
#############################
def choose_a_stone_and_size():
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
    print('Choose a board size:')
    size = input()
    return hands[index[x]], size

if __name__ == '__main__':
    """
    The main function called when pacman.py is run
    from the command line:

    > python konane.py

    See the usage string for more details.

    > python pacman.py --help
    """
    user_piece, size = choose_a_stone_and_size() 
    Game(user_piece, int(size), 3)

    # pass
        






# if __name__ == '__main__':
#     game= Board(turn = 'User', board=BoardTypes.NEW )