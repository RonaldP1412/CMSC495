import pygame
from color import Color

class Piece:
    def __init__(self,piece_type):
        self.piece_type = piece_type
        self.color = Color.get_color()
        self.cells = {}
        self.cell_size = 40
        self.current_rotation = 0
        self.x_offset = 0
        self.y_offset = 0

    def draw(self,screen):
        cells = self.get_position()
        for x,y  in  cells:
            cells_rect = pygame.Rect(x*self.cell_size + 1, y * self.cell_size + 1, self.cell_size -1, self.cell_size -1)
            pygame.draw.rect(screen,self.color[self.piece_type],cells_rect)

    def get_x_offset(self):
        return self.x_offset

    def move(self,x,y):
        self.x_offset +=x
        self.y_offset +=y

    def get_position(self):
        cells = self.cells[self.current_rotation]
        offset_cell =[]
        for x,y in cells:
            x = x + self.x_offset
            y = y + self.y_offset
            offset_cell.append((x,y))

        return offset_cell

    def get_rotation(self):
        cells = self.cells[self.current_rotation]
        return cells

    def right_rotate(self):
        if self.current_rotation == 3:
            self.current_rotation = 0
        else:
            self.current_rotation += 1

    def left_rotate(self):
        if self.current_rotation == 0:
            self.current_rotation = 3
        else:
            self.current_rotation -= 1


#Cell positions relative to starting position
#----------DO NOT CHANGE-----------
class IPiece(Piece):
    def __init__(self):
        super().__init__(piece_type = 1)
        self.cells = {
            0:[(0,1),(1,1),(2,1),(3,1)],
            1:[(2,0),(2,1),(2,2),(2,3)],
            2:[(0,2),(1,2),(2,2),(3,2)],
            3:[(1,0),(1,1),(1,2),(1,3)]
        }
        self.move(3,-1)

class JPiece(Piece):
    def __init__(self):
        super().__init__(piece_type=2)
        self.cells = {
            0: [(0,0),(0,1),(1,1),(2,1)],
            1: [(1,0),(2,0),(1,1),(1,2)],
            2: [(0,1),(1,1),(2,1),(2,2)],
            3: [(1,0),(1,1),(0,2),(1,2)]
        }
        self.move(3, 0)
class LPiece(Piece):
    def __init__(self):
        super().__init__(piece_type=3)
        self.cells = {
            0: [(2,0),(0,1),(1,1),(2,1)],
            1: [(1,0),(1,1),(1,2),(2,2)],
            2: [(0,1),(1,1),(2,1),(0,2)],
            3: [(0,0),(1,0),(1,1),(1,2)]
        }
        self.move(3, 0)
class OPiece(Piece):
    def __init__(self):
        super().__init__(piece_type=4)
        self.cells = {
            0: [(0,0),(0,1),(1,0),(1,1)],
            1: [(0,0),(0,1),(1,0),(1,1)],
            2: [(0,0),(0,1),(1,0),(1,1)],
            3: [(0,0),(0,1),(1,0),(1,1)]
        }
        self.move(4, 0)
class SPiece(Piece):
    def __init__(self):
        super().__init__(piece_type=5)
        self.cells = {
            0: [(1,0),(2,0),(0,1),(1,1)],
            1: [(1,0),(1,1),(2,1),(2,2)],
            2: [(1,1),(2,1),(0,2),(1,2)],
            3: [(0,0),(0,1),(1,1),(1,2)]
        }
        self.move(3, 0)

class TPiece(Piece):
    def __init__(self):
        super().__init__(piece_type=6)
        self.cells = {
            0: [(1,0),(0,1),(1,1),(2,1)],
            1: [(1,0),(1,1),(2,1),(1,2)],
            2: [(0,1),(1,1),(2,1),(1,2)],
            3: [(1,0),(0,1),(1,1),(1,2)]
        }
        self.move(3, 0)

class ZPiece(Piece):
    def __init__(self):
        super().__init__(piece_type=7)
        self.cells = {
            0: [(0,0),(1,0),(1,1),(2,1)],
            1: [(2,0),(1,1),(2,1),(1,2)],
            2: [(0,1),(1,1),(1,2),(2,2)],
            3: [(1,0),(0,1),(1,1),(0,2)]
        }
        self.move(3, 0)
