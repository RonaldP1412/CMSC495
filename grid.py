import pygame
from color import Color

#Draws game area
class Grid:
    def __init__(self,screen_offset):
        self.total_x = 10
        self.total_y = 20
        self.offset = screen_offset
        self.grid = [[0 for i in range(self.total_y)] for j in range(self.total_x)]
        self.cell_size = 40
        self.color = Color.get_color()

    #Checks if a cell is outside given grid
    def border_collision(self,x,y):
        if 0 <= x < self.total_x and 0 <= y < self.total_y:
            return True
        return False

    #Checks if given x,y is empty
    def empty_space(self,x,y):
        if self.grid[x][y] == 0:
            return True
        return False

    def complete_line(self,y):
        for x in range(self.total_x):
            if self.grid[x][y] == 0:
                return False
        return True

    def delete_row(self,y):
        for x in range(self.total_x):
            self.grid[x][y] = 0

    def move_rows(self,y,rows):
        for x in range(self.total_x):
           self.grid[x][y+rows] = self.grid[x][y]
           self.grid[x][y] = 0

    def clear_rows(self):
        complete = 0
        for y in range(self.total_y-1,0,-1):
            if self.complete_line(y):
                self.delete_row(y)
                complete += 1
            elif complete > 0:
               self.move_rows(y,complete)
        return complete

    def draw(self,screen):
        for x in range(self.total_x):
            for y in range(self.total_y):
                current_cell = self.grid[x][y]
                cell_rect = pygame.Rect(x*self.cell_size + self.offset, y*self.cell_size+ self.offset,
                                        self.cell_size-1,self.cell_size-1)
                pygame.draw.rect(screen,self.color[current_cell], cell_rect)

    def reset(self):
        for column in range(self.total_x):
            for row in range(self.total_y):
                self.grid[column][row] = 0
