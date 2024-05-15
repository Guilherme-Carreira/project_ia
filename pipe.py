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

    def __init__(self, grid: tuple): # definir o grid como um tuplo
        self.grid = grid
      
    def get_value(self, row: int, col: int):
        return self.grid[row][col]
    
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
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        pass

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
