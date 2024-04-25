from sys import stdin

class Board:

    def __init__(self, grid: tuple): # definir o grid como um tuplo
        self.grid = grid
    
    def adjacent_vertical_values(self, row: int, col: int): # acima e abaixo
        if row == 0: # se for a primeira linha
          return (None, self.grid[row + 1][col])
        elif row == len(self.grid) - 1: # se for a ultima linha
            return (self.grid[row - 1][col], None)
        else: # se for qualquer outra linha no meio
          return (self.grid[row - 1][col], self.grid[row + 1][col])

    def adjacent_horizontal_values(self, row: int, col: int): # esquerda e direita
        if col == 0:
            return (None, self.grid[row][col + 1])
        elif col == len(self.grid) - 1:
            return (self.grid[row][col - 1], None)
        else:
            return (self.grid[row][col - 1], self.grid[row][col + 1])


    @staticmethod
    def parseinstance(): 
        grid = []
        for line in stdin: # le do stdin e o line e cada linha 
            grid.append(tuple(line.strip().split(' '))) # strip() remove \n e \t do tuplo e split() divide 
            if not line:
                break
        return Board(grid)

board = Board.parseinstance()
print(board.adjacent_vertical_values(0, 0))
print(board.adjacent_horizontal_values(0, 0))

print(board.adjacent_vertical_values(1, 1))
print(board.adjacent_horizontal_values(1, 1))
#print(board) #DEBUG 
