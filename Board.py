from collections import defaultdict

class BoardTypes:
    NEW = 'New'
    EMPTY = 'Empty'

class Piece:
    DARK = 'X'
    LIGHT = 'O'
    def opponent(self):
        if self == 'O':
            return self.LIGHT 
        elif self == 'X':
            return self.DARK
        # else:
        #     raise Exception("no opponent for", self)

class Board:

    def __init__(self, turn, board_type= BoardTypes.NEW) -> None:
        self.turn = turn
        self.board = self.new_board(board_type)

    def new_board(self, b_type: BoardTypes):
        board = []
        board.append([None]*9)
        if b_type == BoardTypes.NEW:
            checkers = [None] + ['X','O','X','O','X','O','X','O']
            ch_reversed = [None] + list(reversed(checkers[1:]))
            for i in range(8):
                if i%2 == 0:
                    board.append(checkers.copy())
                else:
                    board.append(ch_reversed.copy())
        elif b_type == BoardTypes.EMPTY: 
            board = board + [[None]+[" " for i in range(8)] for i in range(8)]
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
            raise Exception("Illegal Move: from" + from_tile + "to", to_tile)
        
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
                while 1 <= move < 9:
                    #x + (d-1) > opponent to be removed
                    #x + d next location
                    if self.board[jump][y] == self.opponent(piece) and self.board[move][y] == " ":
                        # map from/to location with removed piece
                        # if (x,y) == (8,4):
                        #     print(stop, op)
                        legal[ ((x, y), (move, y)) ].append( (jump, y) )
                        move = move + stop
                        jump = jump + op
                    else:
                        break
                #moving horzontally
                if 1 <= y + stop < 9: 
                    if self.board[x][y + op] == self.opponent(piece) and self.board[x][y + stop] == " ":
                        # map from/to location with removed piece
                        legal[ ((x, y), (x, y + stop)) ].append( (x, y + op) )

        return legal
    
    #gets locations of the type of piece given
    def getPiecePositions(self, piece: Piece):
        positions = []
        for x in range (1,9):
            for y in range(1,9):
                if self.board[x][y] == piece:
                    positions.append((x,y))
        return positions

