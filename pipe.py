from sys import stdin

class Board:
  def adjacent_vertical_values(self, row: int, col, int):
    pass
  def adjacent_horizontal_values(self, row: int, col, int):
    pass

@staticmethod
def parseinstance():
  board = []
  index = 0
  while True:
    line = stdin.readline()
    if not line:
      break
    board[index] = line
    index = index + 1

  return Board(board)