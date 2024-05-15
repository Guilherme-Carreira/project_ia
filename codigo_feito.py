from sys import stdin

class Piece:
    def __init__(self, piece: str, row: int, col: int):
        self.row = row
        self.col = col
        if piece[0] == 'F':
            self.type = "FINAL"
        elif piece[0] == 'B':
            self.type = "TRIPLE"
        elif piece[0] == 'V':
            self.type = "DOUBLE"
        elif piece[0] == 'L':
            self.type = "STRAIGHT"

        if piece[1] == 'C':
            self.orientation = "UP"
        elif piece[1] == 'B':
            self.orientation = "DOWN"
        elif piece[1] == 'E':
            self.orientation = "LEFT"
        elif piece[1] == 'D':
            self.orientation = "RIGHT"
        elif piece[1] == 'H':
            self.orientation = "HORIZONTAL"
        elif piece[1] == 'V':
            self.orientation = "VERTICAL"
            
    def get_type(self):
        return self.type
    
    def get_orientation(self):
        return self.orientation        
            
    def get_row(self):
        return self.row
    
    def get_column(self):
        return self.col
    
    def visualize(self):
        return self.orientation + ' ' + self.type
    
    
class Board:

    def __init__(self, grid: list): # definir o grid como um tuplo
        self.grid = grid
    
    def adjacent_vertical_values(self, row: int, col: int): # acima e abaixo
        if row == 0: # se for a primeira linha
          return (None, self.grid[row + 1][col].visualize())
        elif row == len(self.grid) - 1: # se for a ultima linha
            return (self.grid[row - 1][col].visualize(), None)
        else: # se for qualquer outra linha no meio
          return (self.grid[row - 1][col].visualize(), self.grid[row + 1][col].visualize())

    def adjacent_horizontal_values(self, row: int, col: int): # esquerda e direita
        if col == 0:
            return (None, self.grid[row][col + 1].visualize())
        elif col == len(self.grid) - 1:
            return (self.grid[row][col - 1].visualize(), None)
        else:
            return (self.grid[row][col - 1].visualize(), self.grid[row][col + 1].visualize())


    @staticmethod
    def parseinstance(): 
        grid = []
        row = 0
        col = 0
        for line in stdin: # le do stdin e o line e cada linha 
            current_line = line.strip().split() # strip() remove \n e \t do tuplo e split() divide 
            row_pieces = []
            for piece in current_line:
                row_pieces.append(Piece(piece, row, col))
                col += 1
            grid.append(row_pieces)
            row += 1
            col = 0
            if not line:
                break
        return Board(grid)

board = Board.parseinstance()
print(board.adjacent_vertical_values(0, 0))
print(board.adjacent_horizontal_values(0, 0))

print(board.adjacent_vertical_values(1, 1))
print(board.adjacent_horizontal_values(1, 1))
#print(board) #DEBUG 
