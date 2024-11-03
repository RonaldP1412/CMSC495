
"""" 
CMSC 495 7384 Capstone in Computer Science (2248)
Project: Tetris game made with pygame
University of Maryland Global Campus
Group 3:Ronald Parra De Jesus, Anthony Petrowich, Colton Purdy, Kelvin Ruvio-Amaya, Asher Russell, Phillip Seisman
and Julian Sotelo
Professor Davis
"""
from grid import Grid
from pieces import *
import random
import pygame
import os

class TetrisLogic:
    def __init__(self, line_clear_sound, collision_sound, game_over_sound):
        self.grid = Grid(1)
        self.available_pieces = []
        self.current_piece = self.random_piece()
        self.next_piece = self.random_piece()
        self.game_over = False
        self.game_over_sound_played = False  # Track if game-over sound has been played
        self.movement = True
        self.AUTO_MOVE = pygame.USEREVENT + 1
        self.counter = 0
        self.score = 0  # Current score
        self.high_score = self.load_high_score()  # Load high score from file
        self.line_clear_sound = line_clear_sound
        self.collision_sound = collision_sound
        self.game_over_sound = game_over_sound
        self.set_auto_move_timer(2000)  # Set initial drop speed to 2000 ms (2 seconds)

    def load_high_score(self):
        """Loads the high score from a file if it exists."""
        if os.path.exists("high_score.txt"):
            with open("high_score.txt", "r") as file:
                return int(file.read())
        return 0  # Default high score if file doesn't exist

    def save_high_score(self):
        """Saves the high score to a file if the current score exceeds it."""
        if self.score > self.high_score:
            self.high_score = self.score
            with open("high_score.txt", "w") as file:
                file.write(str(self.high_score))

    def set_auto_move_timer(self, interval):
        """Sets the interval for the AUTO_MOVE timer."""
        pygame.time.set_timer(self.AUTO_MOVE, interval)

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
            self.collision_sound.play()  # Play collision sound when piece locks

    def lock(self):
        cells = self.current_piece.get_position()
        for x, y in cells:
            self.grid.grid[x][y] = self.current_piece.piece_type
        self.current_piece = self.next_piece
        self.next_piece = self.random_piece()
        
        rows_cleared = self.grid.clear_rows()  # Get number of cleared rows
        if rows_cleared > 0:
            self.update_score(rows_cleared)
            self.line_clear_sound.play()  # Play line clear sound if rows are cleared

        # Check for game over condition
        if not self.empty_space():
            self.game_over = True
            if not self.game_over_sound_played:
                self.game_over_sound.play()  # Play only if it hasn't been played
                self.game_over_sound_played = True
            self.save_high_score()  # Save high score when game over

    def update_score(self, rows_cleared):
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
        pass  # Code for drawing the ghost piece (if needed)

    def draw_next_piece(self, screen):
        """Draws the next piece in a designated area on the side of the screen."""
        next_piece_position = (420, 100)  # Position for the next piece box
        box_size = 120  # Size of the "Next" box

        # Draw the "Next" box border
        pygame.draw.rect(screen, (255, 255, 255), (next_piece_position[0], next_piece_position[1], box_size, box_size), 2)

        # Draw the next piece within the box
        for x, y in self.next_piece.get_rotation():  # Get the shape of the piece in its initial rotation
            # Center the piece in the "Next" box
            piece_x = next_piece_position[0] + x * self.grid.cell_size + 20
            piece_y = next_piece_position[1] + y * self.grid.cell_size + 20
            pygame.draw.rect(screen, self.next_piece.color[self.next_piece.piece_type],
                             (piece_x, piece_y, self.grid.cell_size - 2, self.grid.cell_size - 2))

    def draw(self, screen):
        """Draws the main game grid, current piece, and upcoming piece."""
        self.grid.draw(screen)
        self.current_piece.draw(screen)
        self.draw_ghost(screen)
        self.draw_next_piece(screen)  # Draw the "Next" piece on the side

    def reset(self):
        self.grid.reset()
        self.available_pieces = []
        self.current_piece = self.random_piece()
        self.next_piece = self.random_piece()
        self.score = 0
        self.game_over = False
        self.game_over_sound_played = False  # Reset game-over sound flag
        self.set_auto_move_timer(2000)  # Reset auto move timer to initial speed
