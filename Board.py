from collections import defaultdict
from math import pi
import copy

class BoardTypes:
    NEW = 'New'
    EMPTY = 'Empty'

class Piece:
    DARK = 'X'
    LIGHT = 'O'

class Board:

    
    def __init__(self, turn, size,board_type= BoardTypes.NEW) -> None:
        self.turn = turn
        self.size = size
        self.board = self.new_board(board_type)

    def new_board(self, b_type: BoardTypes):
        board = []
        size = self.size+1
        board.append([None]*size)
        if b_type == BoardTypes.NEW:
            checkers = [None] + ['X','O']*int(self.size/2)
            ch_reversed = [None] + list(reversed(checkers[1:]))
            for i in range(self.size):
                if i%2 == 0:
                    board.append(checkers.copy())
                else:
                    board.append(ch_reversed.copy())
        elif b_type == BoardTypes.EMPTY: 
            board = board + [[None]+[" " for i in range(self.size)] for i in range(self.size)]
        return board

    def a_board(self, blacks: list[tuple], whites: list[tuple]):
        empty_board = self.new_board(BoardTypes.EMPTY)
        for x,y in blacks:
            empty_board[x][y] = 'X'
        for x,y in whites:
            empty_board[x][y] = 'O'

    def start_game(self):
        # print (self.board[4][4])
        self.board[4][4] = self.board[4][5] = ' '
    
    #updates Board after the given played move
    # maybe update to not rely on calling getLegalActions
    def played_move(self, from_tile: tuple, to_tile: tuple, piece: Piece):
        legalActions = self.getLegalActions(piece)
        if (from_tile, to_tile) not in legalActions: #maybe unneccessary
            raise Exception("Illegal Move: from " , from_tile , " to", to_tile)
        
        removed = legalActions[(from_tile, to_tile)]
        self.board[from_tile[0]][from_tile[1]] = " "
        self.board[to_tile[0]][to_tile[1]] = piece
        for x,y in removed:
            self.board[x][y] = " "
    
    def reverse(self):
        if self.turn == Piece.DARK:
            self.turn = Piece.LIGHT
        else:
            self.turn = Piece.DARK

    def opponent(self, piece: Piece):
        if piece == Piece.DARK:
            return Piece.LIGHT
        return Piece.DARK
        
    #returns a map of key tuples representing legal actions and their list values of removed pieces
    def getLegalActions(self, piece: Piece):
        directions = [(2, 1), (-2,-1)]
        positions = self.getPiecePositions(piece)
        legal = defaultdict(list)
        for x, y in positions: #get legal moves for all Pieces
            
            for stop, op in directions: 
                #moving vertically
                move = x + stop
                jump = x + op
                while 1 <= move < self.size+1:
                    #x + (d-1) > opponent to be removed
                    #x + d next location
                    if self.board[jump][y] == self.opponent(piece) and self.board[move][y] == " ":
                        legal[ ((x, y), (move, y)) ].append( (jump, y) )
                        move = move + stop
                        jump = jump + op
                    else:
                        break
                #moving horzontally
                if 1 <= y + stop < self.size+1: 
                    if self.board[x][y + op] == self.opponent(piece) and self.board[x][y + stop] == " ":
                        # map from/to location with removed piece
                        legal[ ((x, y), (x, y + stop)) ].append( (x, y + op) )

        return legal
    
    #gets locations of the type of piece given
    def getPiecePositions(self, piece: Piece):
        positions = []
        for x in range (1,self.size+1):
            for y in range(1,self.size+1):
                if self.board[x][y] == piece:
                    positions.append((x,y))
        return positions
    
    def endGame(self, piece: Piece):
        if len(self.getLegalActions(piece))==0:
            return True
        return False
    #count number of pieces of this piece in the edges
    def e(self, piece: Piece):        
        # print("given move: ", move)
        # print("from: ", move[0], "to: ", move[1])
        # self.played_move(from_tile=move[0], to_tile= move[1], piece = piece)
        score = 0
        #range avoids corners to handle duplication
        for i in range(2, self.size):
            if self.board[1][i] == piece:
                score+=1
            if self.board[i][1] == piece:
                score+=1
            if self.board[self.size][i] == piece:
                score+=1
            if self.board[i][self.size] == piece:
                score+=1
        #handling corners: 
        corners = [(1,1), (self.size, self.size), (1,self.size), (self.size,1)]
        for x,y in corners:
            if self.board[x][y]== piece:
                score+=1
        return score
