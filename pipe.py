# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 05:
# 106492 Marcio Filipe Simoes
# 106965 Joao Guilherme Carreira

import copy
import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id


class Piece:
    def __init__(self, piece: str, row: int, col: int):
        self.config = piece # CONFIGURACAO DA PECA
        self.row = row
        self.col = col
        self.solved = False
            
    def change_orientation(self, new_piece: str):
        if new_piece[0] == self.config[0]:
            self.config = new_piece
            
    def connects_top(self, config: str):
        if config in ["FC", "BC", "BE", "BD", "VC", "VD", "LV"]:
            return True
        return False
    
    def connects_bottom(self, config: str):
        if config in ["FB", "BB", "BE", "BD", "VB", "VE", "LV"]:
            return True
        return False
    
    def connects_left(self, config: str):
        if config in ["FE", "BC", "BB", "BE", "VC", "VE", "LH"]:
            return True
        return False
    
    def connects_right(self, config: str):
        if config in ["FD", "BC", "BB", "BD", "VB", "VD", "LH"]:
            return True
        return False
    
    """shows the type of piece"""
    def get_piece(self):
        return self.config


class Board:

    def __init__(self, grid: list): # definir o grid como um tuplo
        self.grid = grid
        self.size = len(grid)
    
    """"""
    def adjacent_vertical_values(self, row: int, col: int): # acima e abaixo
        if row == 0: # se for a primeira linha
          return (None, self.grid[row + 1][col])
        elif row == len(self.grid) - 1: # se for a ultima linha
            return (self.grid[row - 1][col], None)
        else: # se for qualquer outra linha no meio
          return (self.grid[row - 1][col], self.grid[row + 1][col])

    """"""
    def adjacent_horizontal_values(self, row: int, col: int): # esquerda e direita
        if col == 0:
            return (None, self.grid[row][col + 1])
        elif col == len(self.grid) - 1:
            return (self.grid[row][col - 1], None)
        else:
            return (self.grid[row][col - 1], self.grid[row][col + 1])
        
    """"""    
    def pre_process(self):
        grid = board.grid
        size = len(grid)
        if grid[0][0].config == "VB": # TOP LEFT CORNER
            grid[0][0].solved = True
        if grid[0][size-1].config == "VE": # TOP RIGHT CORNER
            grid[0][size-1].solved = True
        if grid[size-1][0].config == "VD": # BOTTOM LEFT CORNER
            grid[size-1][0].solved = True
        if grid[size-1][size-1].config == "VC": # BOTTOM RIGHT CORNER
            grid[size-1][size-1].solved = True
            
        for i in range(1, size - 1):
            if grid[0][i].config == "LH" or grid[0][i].config == "BB": # TOP WALL
                grid[0][i].solved = True
            if grid[size-1][i].config == "LH" or grid[size-1][i].config == "BC": # BOTTOM WALL
                grid[size-1][i].solved = True
            if grid[i][0].config == "LV" or grid[i][0].config == "BD": # LEFT WALL
                grid[i][0].solved = True
            if grid[i][size-1].config == "LV" or grid[i][size-1].config == "BE": # RIGHT WALL
                grid[i][size-1].solved = True

    """"""
    def in_corner(self, piece: Piece):
        row = piece.row
        col = piece.col
        left, right = self.adjacent_horizontal_values(row, col)
        top, bottom = self.adjacent_vertical_values(row, col)
        if left == None:
            if top == None:
                return "CE" # CIMA ESQUERDA
            elif bottom == None:
                return "BE" # BAIXO ESQUERDA
        elif right == None:
            if top == None:
                return "CD" # CIMA DIREITA
            elif bottom == None:
                return "BD" # BAIXO DIREITA
        return False
    
    """"""
    def in_wall(self, piece: Piece):
        row = piece.row
        col = piece.col
        left, right = self.adjacent_horizontal_values(row, col)
        top, bottom = self.adjacent_vertical_values(row, col)
        if left == None:
            return "E" # ESQUERDA
        elif right == None:
            return "D" # DIREITA
        elif top == None:
            return "C" # CIMA
        elif bottom == None:
            return "B" # BAIXO
        return False

    """"""
    def print_board(self):
        for i in range(self.size):
            if (i != 0):
                print('\n')
            for j in range(self.size):
                if (j != 0):
                    print('\t', end = '')
                print(self.grid[i][j].get_piece(), end = '')

    """"""
    @staticmethod
    def parseinstance(): 
        grid = []
        row = 0
        col = 0
        for line in sys.stdin: # le do stdin e o line e cada linha 
            current_line = line.strip().split('\t') # strip() remove \n e \t do tuplo e split() divide 
            if not current_line:
                break
            row_pieces = []
            for piece in current_line:
                row_pieces.append(Piece(piece, row, col))
                col += 1
            grid.append(row_pieces)
            row += 1
            col = 0
        return Board(grid)


class PipeMania(Problem):
    def __init__(self, state: PipeManiaState):
        self.initial = state
        self.next_piece = None                    

    def actions(self, state: PipeManiaState):
        board = state.board
        if state.state_id <= 10:
            print("State", state.state_id)
            board.print_board()
            print("\n")
        grid = board.grid
        return_actions = []
        for row in grid:
            for piece in row:
                if not piece.solved:
                    piece_actions = []
                    corner = board.in_corner(piece)
                    wall = board.in_wall(piece)
                    if corner != False:
                        if corner == "CE":
                            if piece.config[0] == "F":
                                piece_actions.append(["FB", piece.row, piece.col])
                                piece_actions.append(["FD", piece.row, piece.col])
                            elif piece.config[0] == "V":
                                piece_actions.append(["VB", piece.row, piece.col])
                        elif corner == "CD":
                            if piece.config[0] == "F":
                                piece_actions.append(["FB", piece.row, piece.col])
                                piece_actions.append(["FE", piece.row, piece.col])
                            elif piece.config[0] == "V":
                                piece_actions.append(["VE", piece.row, piece.col])
                        elif corner == "BE":
                            if piece.config[0] == "F":
                                piece_actions.append(["FC", piece.row, piece.col])
                                piece_actions.append(["FD", piece.row, piece.col])
                            elif piece.config[0] == "V":
                                piece_actions.append(["VD", piece.row, piece.col])
                        elif corner == "BD":
                            if piece.config[0] == "F":
                                piece_actions.append(["FC", piece.row, piece.col])
                                piece_actions.append(["FE", piece.row, piece.col])
                            elif piece.config[0] == "V":
                                piece_actions.append(["VC", piece.row, piece.col])
                    if wall != False and corner == False:
                        if wall == "E":
                            if piece.config[0] == "F":
                                piece_actions.append(["FC", piece.row, piece.col])
                                piece_actions.append(["FD", piece.row, piece.col])
                                piece_actions.append(["FB", piece.row, piece.col])
                            elif piece.config[0] == "V":
                                piece_actions.append(["VD", piece.row, piece.col])
                                piece_actions.append(["VB", piece.row, piece.col])
                            elif piece.config[0] == "L":
                                piece_actions.append(["LV", piece.row, piece.col])
                            elif piece.config[0] == "B":
                                piece_actions.append(["BD", piece.row, piece.col])
                        if wall == "D":
                            if piece.config[0] == "F":
                                piece_actions.append(["FC", piece.row, piece.col])
                                piece_actions.append(["FB", piece.row, piece.col])
                                piece_actions.append(["FE", piece.row, piece.col])
                            elif piece.config[0] == "V":
                                piece_actions.append(["VC", piece.row, piece.col])
                                piece_actions.append(["VE", piece.row, piece.col])
                            elif piece.config[0] == "L":
                                piece_actions.append(["LV", piece.row, piece.col])
                            elif piece.config[0] == "B":
                                piece_actions.append(["BE", piece.row, piece.col])
                        if wall == "C":
                            if piece.config[0] == "F":
                                piece_actions.append(["FE", piece.row, piece.col])
                                piece_actions.append(["FB", piece.row, piece.col])
                                piece_actions.append(["FD", piece.row, piece.col])
                            elif piece.config[0] == "V":
                                piece_actions.append(["VB", piece.row, piece.col])
                                piece_actions.append(["VE", piece.row, piece.col])
                            elif piece.config[0] == "L":
                                piece_actions.append(["LH", piece.row, piece.col])
                            elif piece.config[0] == "B":
                                piece_actions.append(["BB", piece.row, piece.col])
                        if wall == "B":
                            if piece.config[0] == "F":
                                piece_actions.append(["FC", piece.row, piece.col])
                                piece_actions.append(["FE", piece.row, piece.col])
                                piece_actions.append(["FD", piece.row, piece.col])
                            elif piece.config[0] == "V":
                                piece_actions.append(["VC", piece.row, piece.col])
                                piece_actions.append(["VD", piece.row, piece.col])
                            elif piece.config[0] == "L":
                                piece_actions.append(["LH", piece.row, piece.col])
                            elif piece.config[0] == "B":
                                piece_actions.append(["Bc", piece.row, piece.col])    
                    if corner == False and wall == False:
                        if piece.config[0] == "F":
                            piece_actions.append(["FC", piece.row, piece.col])
                            piece_actions.append(["FD", piece.row, piece.col])
                            piece_actions.append(["FB", piece.row, piece.col])
                            piece_actions.append(["FE", piece.row, piece.col])
                        elif piece.config[0] == "B":
                            piece_actions.append(["BC", piece.row, piece.col])
                            piece_actions.append(["BD", piece.row, piece.col])
                            piece_actions.append(["BB", piece.row, piece.col])
                            piece_actions.append(["BE", piece.row, piece.col])
                        elif piece.config[0] == "V":
                            piece_actions.append(["VC", piece.row, piece.col])
                            piece_actions.append(["VD", piece.row, piece.col])
                            piece_actions.append(["VB", piece.row, piece.col])
                            piece_actions.append(["VE", piece.row, piece.col])
                        elif piece.config[0] == "L":
                            piece_actions.append(["LH", piece.row, piece.col])
                            piece_actions.append(["LV", piece.row, piece.col])
                        
                    left, right = board.adjacent_horizontal_values(piece.row, piece.col)
                    top, bottom = board.adjacent_vertical_values(piece.row, piece.col)
                    
                    if top != None:
                        if top.solved:
                            if top.connects_bottom(top.config):
                                if piece.config[0] == "F":
                                    piece_actions = [["FC", piece.row, piece.col]]
                                else:
                                    for element in piece_actions[:]:
                                        if not top.connects_top(element[0]):
                                            piece_actions.remove(element)
                            else:
                                for element in piece_actions[:]:
                                    if top.connects_top(element[0]):
                                        piece_actions.remove(element)
                        if piece.config[0] == "F" and top.config[0] == "F":
                            if ["FC", piece.row, piece.col] in piece_actions:
                                piece_actions.remove(["FC", piece.row, piece.col])
                    if bottom != None:
                        if bottom.solved:
                            if bottom.connects_top(bottom.config):
                                if piece.config[0] == "F":
                                    piece_actions = [["FB", piece.row, piece.col]]
                                else:
                                    for element in piece_actions[:]:
                                        if not bottom.connects_bottom(element[0]):
                                            piece_actions.remove(element)
                            else:
                                for element in piece_actions[:]:
                                    if bottom.connects_bottom(element[0]):
                                        piece_actions.remove(element)  
                        if piece.config[0] == "F" and bottom.config[0] == "F":
                            if ["FB", piece.row, piece.col] in piece_actions:
                                piece_actions.remove(["FB", piece.row, piece.col]) 
                    if left != None:
                        if left.solved:
                            if left.connects_right(left.config):
                                if piece.config[0] == "F":
                                    piece_actions = [["FE", piece.row, piece.col]]
                                else:
                                    for element in piece_actions[:]:
                                        if not left.connects_left(element[0]):
                                            piece_actions.remove(element)
                            else:
                                for element in piece_actions[:]:
                                    if left.connects_left(element[0]):
                                        piece_actions.remove(element)
                        if piece.config[0] == "F" and left.config[0] == "F":
                            if ["FE", piece.row, piece.col] in piece_actions:
                                piece_actions.remove(["FE", piece.row, piece.col]) 
                    if right != None:
                        if right.solved:
                            if right.connects_left(right.config):
                                if piece.config[0] == "F":
                                    piece_actions = [["FD", piece.row, piece.col]]
                                else:
                                    for element in piece_actions[:]:
                                        if not right.connects_right(element[0]):
                                            piece_actions.remove(element)
                            else:
                                for element in piece_actions[:]:
                                    if right.connects_right(element[0]):
                                        piece_actions.remove(element)
                        if piece.config[0] == "F" and right.config[0] == "F" and piece.config != "FD":
                            if ["FD", piece.row, piece.col] in piece_actions:
                                piece_actions.remove(["FD", piece.row, piece.col]) 

                    if len(piece_actions) == 1:
                        if piece_actions[0][0] != piece.config:
                            return_actions.append(piece_actions[0])
        return [return_actions]
                                          
    def result(self, state: PipeManiaState, actions: list):
        board = state.board
        new_board = copy.deepcopy(board)
        grid = new_board.grid
        for action in actions:
            piece = grid[action[1]][action[2]]
            piece.change_orientation(action[0])
            piece.solved = True
        new_state = PipeManiaState(new_board)
        return new_state

    def goal_test(self, state: PipeManiaState):
        board = state.board
        grid = board.grid
        for row in grid:
            for piece in row:
                left, right = board.adjacent_horizontal_values(piece.row, piece.col)
                top, bottom = board.adjacent_vertical_values(piece.row, piece.col)
                
                if (top == None and piece.connects_top(piece.config)) or (top != None and (top.connects_bottom(top.config) != piece.connects_top(piece.config))):
                    return False
                if (bottom == None and piece.connects_bottom(piece.config)) or (bottom != None and (bottom.connects_top(bottom.config) != piece.connects_bottom(piece.config))):
                    return False
                if (left == None and piece.connects_left(piece.config)) or (left != None and (left.connects_right(left.config) != piece.connects_left(piece.config))):
                    return False
                if (right == None and piece.connects_right(piece.config)) or (right != None and (right.connects_left(right.config) != piece.connects_right(piece.config))):
                    return False
                      
        return True
            
    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass


if __name__ == "__main__":
    board = Board.parseinstance()
    board.pre_process()
    state = PipeManiaState(board)
    pipemania = PipeMania(state)
    goal = depth_first_tree_search(pipemania)
    solved_board = goal.state.board
    solved_board.print_board()
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
