# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 05:
# 106492 Marcio Filipe Simoes
# 106965 Joao Guilherme Carreira

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
        self.type = piece[0]
        self.orientation = piece[1]
        self.connections = self.calculate_connections(piece)
        self.row = row
        self.col = col
        self.solved = False
        self.actions = []
            
    def change_orientation(self, new_piece: str):
        if new_piece[0] == self.type:
            self.connections = self.calculate_connections(new_piece)
            self.orientation = new_piece[1]
    
    """function that updates the connections of the piece"""
    def calculate_connections(self, new_piece: str):
        new_connections = [False, False, False, False] # [CIMA, DIREITA, BAIXO, ESQUERDA]
        
        if new_piece[1] == "C": # orientacao CIMA
            new_connections[0] = True
            direction = 0
        elif new_piece[1] == "D": # orientacao DIREITA
            new_connections[1] = True
            direction = 1
        elif new_piece[1] == "B": # orientacao BAIXO
            new_connections[2] = True
            direction = 2
        elif new_piece[1] == "E": # orientacao ESQUERDA
            new_connections[3] = True
            direction = 3
        elif new_piece[1] == "H": # orientacao HORIZONTAL
            new_connections[1] = True
            new_connections[3] = True
        elif new_piece[1] == "V": # orientacao VERTICAL
            new_connections[0] = True
            new_connections[2] = True
            
        if new_piece[0] == "B": # peca BIFURCACAO    
            new_connections[(direction - 1) % 4] = True # direita - 1 fica CIMA
            new_connections[(direction + 1) % 4] = True # direita + 1 fica BAIXO
        elif new_piece[0] == "V": # peca VOLTA
            new_connections[(direction - 1) % 4] = True
            
        return new_connections
    
    """function that checks if the piece is solved"""
    def is_solved(self):
        return self.solved
    
    """functions that gets the connection"""
    def get_connection(self, index: int):
        return self.connections[index]
    
    def number_actions(self):
        return len(self.actions)
    
    """shows the type of piece"""
    def print_piece(self):
        print(self.type + self.orientation)


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
    def get_restrictions(self, piece: Piece):
        row = piece.row
        col = piece.col
        left, right = self.adjacent_horizontal_values(row, col)
        top, bottom = self.adjacent_vertical_values(row, col)
        restrictions = [None, None, None, None]
        
        if top != None:
            if top.is_solved():
                restrictions[0] = left.get_connection(2)
            else:
                restrictions[0] = False
        elif top == None:
            restrictions[0] = False
            
        if right != None:
            if right.is_solved():
                restrictions[1] = left.get_connection(3)
            else:
                restrictions[1] = False
        elif right == None:
            restrictions[1] = False
            
        if bottom != None:
            if bottom.is_solved():
                restrictions[2] = left.get_connection(0)
            else:
                restrictions[2] = False
        elif bottom == None:
            restrictions[2] = False
            
        if left != None:
            if left.is_solved():
                restrictions[3] = left.get_connection(1)
            else:
                restrictions[3] = False
        elif left == None:
            restrictions[3] = False
        return restrictions

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
        board = self.grid
        for i in range(0, self.size):
            if (i != 0):
               print('\n')
            for j in range(0, self.size):
                if (j != 0):
                    print('\t', end = '')
                print(board[i][j].print_piece(), end = '')

    """"""
    @staticmethod
    def parseinstance(): 
        grid = []
        row = 0
        col = 0
        for line in sys.stdin: # le do stdin e o line e cada linha 
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


class PipeMania(Problem):
    def __init__(self, state: PipeManiaState):
        self.state = state

    def actions(self, state: PipeManiaState):
        board = state.board
        grid = board.grid
        for row in grid:
            for piece in row:
                corner = board.in_corner(piece)
                wall = board.in_wall(piece)
                if corner != False:
                    if corner == "CE":
                        if piece.type == "V":
                            if piece.orientation != "B":
                                piece.actions.append(["VB", piece.row, piece.col])
                        elif piece.type == "F":
                            if piece.orientation == "B":
                                piece.actions.append(["FD", piece.row, piece.col])
                            elif piece.orientation == "D":
                                piece.actions.append(["FB", piece.row, piece.col])
                            else:
                                piece.actions.append(["FB", piece.row, piece.col])
                                piece.actions.append(["FD", piece.row, piece.col])
                    elif corner == "CD":
                        if piece.type == "V":
                            if piece.orientation != "E":
                                piece.actions.append(["VE", piece.row, piece.col])
                        elif piece.type == "F":
                            if piece.orientation == "E":
                                piece.actions.append(["FB", piece.row, piece.col])
                            elif piece.orientation == "B":
                                piece.actions.append(["FE", piece.row, piece.col])
                            else:
                                piece.actions.append(["FE", piece.row, piece.col])
                                piece.actions.append(["FB", piece.row, piece.col])
                    elif corner == "BE":
                        if piece.type == "V":
                            if piece.orientation != "D":
                                piece.actions.append(["VD", piece.row, piece.col])
                        elif piece.type == "F":
                            if piece.orientation == "C":
                                piece.actions.append(["FD", piece.row, piece.col])
                            elif piece.orientation == "D":
                                piece.actions.append(["FC", piece.row, piece.col])
                            else:
                                piece.actions.append(["FC", piece.row, piece.col])
                                piece.actions.append(["FD", piece.row, piece.col])
                    elif corner == "BD":
                        if piece.type == "V":
                            if piece.orientation != "C":
                                piece.actions.append(["VC", piece.row, piece.col])
                        elif piece.type == "F":
                            if piece.orientation == "C":
                                piece.actions.append(["FE", piece.row, piece.col])
                            elif piece.orientation == "E":
                                piece.actions.append(["FC", piece.row, piece.col])
                            else:
                                piece.actions.append(["FC", piece.row, piece.col])
                                piece.actions.append(["FE", piece.row, piece.col])
                            
                if wall != False and corner == False:
                    if piece.type == "F":
                        if wall == "E":
                            if piece.orientation == "D":
                                piece.actions.append(["FC", piece.row, piece.col])
                                piece.actions.append(["FB", piece.row, piece.col])
                            elif piece.orientation == "C":
                                piece.actions.append(["FD", piece.row, piece.col])
                                piece.actions.append(["FB", piece.row, piece.col])
                            elif piece.orientation == "B":
                                piece.actions.append(["FD", piece.row, piece.col])
                                piece.actions.append(["FC", piece.row, piece.col])
                            else:
                                piece.actions.append(["FD", piece.row, piece.col])
                                piece.actions.append(["FB", piece.row, piece.col])
                                piece.actions.append(["FC", piece.row, piece.col])
                        elif wall == "D":
                            if piece.orientation == "E":
                                piece.actions.append(["FC", piece.row, piece.col])
                                piece.actions.append(["FB", piece.row, piece.col])
                            elif piece.orientation == "C":
                                piece.actions.append(["FE", piece.row, piece.col])
                                piece.actions.append(["FB", piece.row, piece.col])
                            elif piece.orientation == "B":
                                piece.actions.append(["FE", piece.row, piece.col])
                                piece.actions.append(["FC", piece.row, piece.col])
                            else:
                                piece.actions.append(["FC", piece.row, piece.col])
                                piece.actions.append(["FE", piece.row, piece.col])
                                piece.actions.append(["FB", piece.row, piece.col])
                        elif wall == "C":                         
                            if piece.orientation == "D":
                                piece.actions.append(["FE", piece.row, piece.col])
                                piece.actions.append(["FB", piece.row, piece.col])
                            elif piece.orientation == "E":
                                piece.actions.append(["FD", piece.row, piece.col])
                                piece.actions.append(["FB", piece.row, piece.col])
                            elif piece.orientation == "B":
                                piece.actions.append(["FD", piece.row, piece.col])
                                piece.actions.append(["FE", piece.row, piece.col])
                            else:
                                piece.actions.append(["FE", piece.row, piece.col])
                                piece.actions.append(["FB", piece.row, piece.col])
                                piece.actions.append(["FD", piece.row, piece.col])
                        elif wall == "B":
                            if piece.orientation == "D":
                                piece.actions.append(["FC", piece.row, piece.col])
                                piece.actions.append(["FE", piece.row, piece.col])
                            elif piece.orientation == "C":
                                piece.actions.append(["FD", piece.row, piece.col])
                                piece.actions.append(["FE", piece.row, piece.col])
                            elif piece.orientation == "E":
                                piece.actions.append(["FD", piece.row, piece.col])
                                piece.actions.append(["FC", piece.row, piece.col])
                            else:
                                piece.actions.append(["FE", piece.row, piece.col])
                                piece.actions.append(["FC", piece.row, piece.col])
                                piece.actions.append(["FD", piece.row, piece.col])
                    elif piece.type == "B":
                        if wall == "E":
                            if piece.orientation != "D":
                                piece.actions.append(["BD", piece.row, piece.col])
                        elif wall == "D":
                            if piece.orientation != "E":
                                piece.actions.append(["BE", piece.row, piece.col])
                        elif wall == "C":                         
                            if piece.orientation != "B":
                                piece.actions.append(["BB", piece.row, piece.col])
                        elif wall == "B":
                            if piece.orientation != "C":
                                piece.actions.append(["BC", piece.row, piece.col])
                    elif piece.type == "V":
                        if wall == "E":
                            if piece.orientation == "B":
                                piece.actions.append(["VD", piece.row, piece.col])
                            elif piece.orientation == "D":
                                piece.actions.append(["VB", piece.row, piece.col])
                            else:
                                piece.actions.append(["VD", piece.row, piece.col])
                                piece.actions.append(["VB", piece.row, piece.col])
                        elif wall == "D":
                            if piece.orientation == "C":
                                piece.actions.append(["VE", piece.row, piece.col])
                            elif piece.orientation == "E":
                                piece.actions.append(["VC", piece.row, piece.col])
                            else:
                                piece.actions.append(["VC", piece.row, piece.col])
                                piece.actions.append(["VE", piece.row, piece.col])
                        elif wall == "C":                         
                            if piece.orientation == "B":
                                piece.actions.append(["VE", piece.row, piece.col])
                            elif piece.orientation == "E":
                                piece.actions.append(["VB", piece.row, piece.col])
                            else:
                                piece.actions.append(["VB", piece.row, piece.col])
                                piece.actions.append(["VE", piece.row, piece.col])
                        elif wall == "B":
                            if piece.orientation == "C":
                                piece.actions.append(["VD", piece.row, piece.col])
                            elif piece.orientation == "D":
                                piece.actions.append(["VC", piece.row, piece.col])
                            else:
                                piece.actions.append(["VC", piece.row, piece.col])
                                piece.actions.append(["VD", piece.row, piece.col])
                    elif piece.type == "L":
                        if wall == "E" or wall == "D":
                            if piece.orientation != "V":
                                piece.actions.append(["LV", piece.row, piece.col])
                        elif wall == "C" or wall == "B":
                            if piece.orientation != "H":
                                piece.actions.append(["LH", piece.row, piece.col])
                    
                if corner == False and wall == False:
                    if piece.type == "F":
                        piece.actions.append(["FE", piece.row, piece.col])
                        piece.actions.append(["FD", piece.row, piece.col])
                        piece.actions.append(["FC", piece.row, piece.col])
                        piece.actions.append(["FB", piece.row, piece.col])
                        if piece.orientation == "E":
                            piece.actions.remove(["FE", piece.row, piece.col])
                        elif piece.orientation == "D":
                            piece.actions.remove(["FD", piece.row, piece.col])
                        elif piece.orientation == "C":
                            piece.actions.remove(["FC", piece.row, piece.col])
                        elif piece.orientation == "B":
                            piece.actions.remove(["FB", piece.row, piece.col])
                    elif piece.type == "B":
                        piece.actions.append(["BE", piece.row, piece.col])
                        piece.actions.append(["BD", piece.row, piece.col])
                        piece.actions.append(["BC", piece.row, piece.col])
                        piece.actions.append(["BB", piece.row, piece.col])
                        if piece.orientation == "E":
                            piece.actions.remove(["BE", piece.row, piece.col])
                        elif piece.orientation == "D":
                            piece.actions.remove(["BD", piece.row, piece.col])
                        elif piece.orientation == "C":
                            piece.actions.remove(["BC", piece.row, piece.col])
                        elif piece.orientation == "B":
                            piece.actions.remove(["BB", piece.row, piece.col])
                    elif piece.type == "V":
                        piece.actions.append(["VE", piece.row, piece.col])
                        piece.actions.append(["VD", piece.row, piece.col])
                        piece.actions.append(["VC", piece.row, piece.col])
                        piece.actions.append(["VB", piece.row, piece.col])
                        if piece.orientation == "E":
                            piece.actions.remove(["VE", piece.row, piece.col])
                        elif piece.orientation == "D":
                            piece.actions.remove(["VD", piece.row, piece.col])
                        elif piece.orientation == "C":
                            piece.actions.remove(["VC", piece.row, piece.col])
                        elif piece.orientation == "B":
                            piece.actions.remove(["VB", piece.row, piece.col])
                    elif piece.type == "L":
                        if piece.orientation == "H":
                            piece.actions.append(["LV", piece.row, piece.col])
                        elif piece.orientation == "V":
                            piece.actions.append(["LH", piece.row, piece.col])
                            
                if piece.type == "F":
                    left, right = board.adjacent_horizontal_values(piece.row, piece.col)
                    top, bottom = board.adjacent_vertical_values(piece.row, piece.col)
                    if top != None and top.type == "F":
                        if ["FC", piece.row, piece.col] in piece.actions:
                            piece.actions.remove(["FC", piece.row, piece.col])
                    if bottom != None and bottom.type == "F":
                        if ["FB", piece.row, piece.col] in piece.actions:
                            piece.actions.remove(["FB", piece.row, piece.col])
                    if left != None and left.type == "F":
                        if ["FE", piece.row, piece.col] in piece.actions:
                            piece.actions.remove(["FE", piece.row, piece.col])
                    if right != None and right.type == "F":
                        if ["FD", piece.row, piece.col] in piece.actions:
                            piece.actions.remove(["FD", piece.row, piece.col])
                            
                print(piece.actions, ":", piece.number_actions())

                    

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: PipeManiaState):
        board = state.board
        grid = board.grid
        for row in grid:
            for piece in row:
                adjacent_connections = [None, None, None, None]
                left, right = board.adjacent_horizontal_values(piece.row, piece.col)
                top, bottom = board.adjacent_vertical_values(piece.row, piece.col)
                if top != None:
                    adjacent_connections[0] = top.get_connection(2)
                if right != None:
                    adjacent_connections[1] = right.get_connection(3)
                if bottom != None:
                    adjacent_connections[2] = bottom.get_connection(0)
                if left != None:
                    adjacent_connections[3] = left.get_connection(1)
                
                if piece.get_connection(0) != adjacent_connections[0] and (piece.get_connection(0) != False or adjacent_connections[0] != None):
                    return False
                if piece.get_connection(1) != adjacent_connections[1] and (piece.get_connection(1) != False or adjacent_connections[1] != None):
                    return False
                if piece.get_connection(2) != adjacent_connections[2] and (piece.get_connection(2) != False or adjacent_connections[2] != None):
                    return False
                if piece.get_connection(3) != adjacent_connections[3] and (piece.get_connection(3) != False or adjacent_connections[3] != None):
                    return False
                
        return True
            

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe

if __name__ == "__main__":
    # TODO:
    board = Board.parseinstance()
    state = PipeManiaState(board)
    pipemania = PipeMania(state)
    print(pipemania.goal_test(state))
    pipemania.actions(state)
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
