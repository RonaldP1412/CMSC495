# The `TetrisLogic` class manages the game logic for a Tetris game, handling piece movement, collision
# detection, scoring, and game over conditions.
from grid import Grid
from pieces import *
import random
import pygame

# The `TetrisLogic` class manages the game logic for a Tetris game, handling piece movement, collision
# detection, scoring, and game state.
class TetrisLogic:
    def __init__(self):
        self.grid = Grid(1)
        self.available_pieces = []
        self.current_piece = self.random_piece()
        self.next_piece = self.random_piece()
        self.game_over = False
        self.movement = True
        self.AUTO_MOVE = pygame.USEREVENT + 1
        self.counter = 0
        self.score = 0  # New score attribute
        pygame.time.set_timer(self.AUTO_MOVE, 200)

    def random_piece(self):
        if len(self.available_pieces) == 0:
            self.available_pieces = [IPiece(), JPiece(), LPiece(), OPiece(), SPiece(), TPiece(), ZPiece()]
        piece = random.choice(self.available_pieces)
        self.available_pieces.remove(piece)
        return piece

    def collision(self):
        cells = self.current_piece.get_position()
        for x, y in cells:
            if not self.grid.border_collision(x, y):
                return False
        return True

    def move_left(self):
        self.current_piece.move(-1, 0)
        if not self.collision() or not self.empty_space():
            self.current_piece.move(1, 0)

    def move_right(self):
        self.current_piece.move(1, 0)
        if not self.collision() or not self.empty_space():
            self.current_piece.move(-1, 0)

    def move_down(self):
        self.current_piece.move(0, 1)
        if not self.collision() or not self.empty_space():
            self.current_piece.move(0, -1)
            self.lock()

    def lock(self):
        cells = self.current_piece.get_position()
        for x, y in cells:
            self.grid.grid[x][y] = self.current_piece.piece_type
        self.current_piece = self.next_piece
        self.next_piece = self.random_piece()
        
        rows_cleared = self.grid.clear_rows()  # Get number of cleared rows
        if rows_cleared > 0:
            self.update_score(rows_cleared)  # Update score based on cleared rows

        if not self.empty_space():
            self.game_over = True

    def update_score(self, rows_cleared):
        # Score increases based on the number of cleared rows (e.g., 100 points per row)
        points = {1: 100, 2: 300, 3: 500, 4: 800}
        self.score += points.get(rows_cleared, 0)

    def empty_space(self):
        cells = self.current_piece.get_position()
        for x, y in cells:
            if not self.grid.empty_space(x, y):
                return False
        return True

    def auto_move(self, event):
        if event.type == self.AUTO_MOVE and not self.game_over:
            self.move_down()

    def rotate_right(self):
        self.current_piece.right_rotate()
        if not self.collision() or not self.empty_space():
            self.current_piece.left_rotate()

    def rotate_left(self):
        self.current_piece.left_rotate()
        if not self.collision() or not self.empty_space():
            self.current_piece.right_rotate()

    def draw_ghost(self, screen):
        # Code for drawing the ghost piece (no changes)
        pass

    def draw(self, screen):
        self.grid.draw(screen)
        self.current_piece.draw(screen)
        self.draw_ghost(screen)

    def reset(self):
        self.grid.reset()
        self.available_pieces = []
        self.current_piece = self.random_piece()
        self.next_piece = self.random_piece()
        self.score = 0  # Reset score
