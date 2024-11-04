""""
CMSC 495 7384 Capstone in Computer Science (2248)
Project: Tetris game made with pygame
University of Maryland Global Campus
Group 3: Ronald Parra De Jesus, Anthony Petrowich, Colton Purdy, Kelvin Ruvio-Amaya, Asher Russell, Phillip Seisman
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
        self.grid = Grid(1)  # Initialize the game grid
        self.available_pieces = []  # List to hold available Tetris pieces
        self.current_piece = self.random_piece()  # Set the current piece to a random piece
        self.next_piece = self.random_piece()  # Set the next piece to a random piece
        self.game_over = False  # Game over state
        self.game_over_sound_played = False  # Track if game-over sound has been played
        self.movement = True  # Track whether movement is allowed
        self.AUTO_MOVE = pygame.USEREVENT + 1  # Custom event for automatic piece movement
        self.counter = 0  # Counter for piece movement
        self.score = 0  # Current score
        self.high_score = self.load_high_score()  # Load high score from file
        self.line_clear_sound = line_clear_sound  # Sound for clearing lines
        self.collision_sound = collision_sound  # Sound for collision
        self.game_over_sound = game_over_sound  # Sound for game over
        self.set_auto_move_timer(2000)  # Set initial drop speed to 2000 ms (2 seconds)

    def load_high_score(self):
        """Loads the high score from a file if it exists."""
        if os.path.exists("high_score.txt"):  # Check if high score file exists
            with open("high_score.txt", "r") as file:
                return int(file.read())  # Return the high score
        return 0  # Default high score if file doesn't exist

    def save_high_score(self):
        """Saves the high score to a file if the current score exceeds it."""
        if self.score > self.high_score:  # Check if current score exceeds high score
            self.high_score = self.score  # Update high score
            with open("high_score.txt", "w") as file:
                file.write(str(self.high_score))  # Write high score to file

    def set_auto_move_timer(self, interval):
        """Sets the interval for the AUTO_MOVE timer."""
        pygame.time.set_timer(self.AUTO_MOVE, interval)  # Set timer for automatic piece movement

    def random_piece(self):
        """Generates a random Tetris piece."""
        if len(self.available_pieces) == 0:  # Check if no available pieces
            self.available_pieces = [IPiece(), JPiece(), LPiece(), OPiece(), SPiece(), TPiece(), ZPiece()]  # List of Tetris pieces
        piece = random.choice(self.available_pieces)  # Randomly select a piece
        self.available_pieces.remove(piece)  # Remove piece from available list
        return piece  # Return selected piece

    def collision(self):
        """Checks for collision of the current piece with the grid borders."""
        cells = self.current_piece.get_position()  # Get current piece's occupied cells
        for x, y in cells:
            if not self.grid.border_collision(x, y):  # Check for border collisions
                return False  # Return false if collision occurs
        return True  # Return true if no collision

    def move_left(self):
        """Moves the current piece left if no collision occurs."""
        self.current_piece.move(-1, 0)  # Move piece left
        if not self.collision() or not self.empty_space():  # Check for collision
            self.current_piece.move(1, 0)  # Move back if collision occurred

    def move_right(self):
        """Moves the current piece right if no collision occurs."""
        self.current_piece.move(1, 0)  # Move piece right
        if not self.collision() or not self.empty_space():  # Check for collision
            self.current_piece.move(-1, 0)  # Move back if collision occurred

    def move_down(self):
        """Moves the current piece down, locking it if it can't move further."""
        self.current_piece.move(0, 1)  # Move piece down
        if not self.collision() or not self.empty_space():  # Check for collision
            self.current_piece.move(0, -1)  # Move back if collision occurred
            self.lock()  # Lock the piece in place
            self.collision_sound.play()  # Play collision sound when piece locks

    def lock(self):
        """Locks the current piece into the grid and checks for row clears."""
        cells = self.current_piece.get_position()  # Get occupied cells of the current piece
        for x, y in cells:
            self.grid.grid[x][y] = self.current_piece.piece_type  # Lock the piece in the grid
        self.current_piece = self.next_piece  # Set the next piece as the current piece
        self.next_piece = self.random_piece()  # Generate a new next piece

        rows_cleared = self.grid.clear_rows()  # Get number of cleared rows
        if rows_cleared > 0:  # If any rows are cleared
            self.update_score(rows_cleared)  # Update score based on rows cleared
            self.line_clear_sound.play()  # Play line clear sound if rows are cleared

        # Check for game over condition
        if not self.empty_space():  # Check if there's no space for new pieces
            self.game_over = True  # Set game over state
            if not self.game_over_sound_played:  # Check if game-over sound hasn't been played
                self.game_over_sound.play()  # Play game-over sound
                self.game_over_sound_played = True  # Update flag to prevent replay
            self.save_high_score()  # Save high score when game over

    def update_score(self, rows_cleared):
        """Updates the score based on the number of rows cleared."""
        points = {1: 100, 2: 300, 3: 500, 4: 800}  # Points for clearing rows
        self.score += points.get(rows_cleared, 0)  # Update score

    def empty_space(self):
        """Checks if the current piece has empty space to move into."""
        cells = self.current_piece.get_position()  # Get occupied cells of the current piece
        for x, y in cells:
            if not self.grid.empty_space(x, y):  # Check for empty space
                return False  # Return false if no empty space
        return True  # Return true if all cells have empty space

    def auto_move(self, event):
        """Handles automatic downward movement of the current piece."""
        if event.type == self.AUTO_MOVE and not self.game_over:  # Check for auto move event
            self.move_down()  # Move piece down automatically

    def rotate_right(self):
        """Rotates the current piece to the right."""
        self.current_piece.right_rotate()  # Rotate piece right
        if not self.collision() or not self.empty_space():  # Check for collision
            self.current_piece.left_rotate()  # Move back if collision occurred

    def rotate_left(self):
        """Rotates the current piece to the left."""
        self.current_piece.left_rotate()  # Rotate piece left
        if not self.collision() or not self.empty_space():  # Check for collision
            self.current_piece.right_rotate()  # Move back if collision occurred

    def draw_ghost(self, screen):
        ghost_offset = self.grid.total_y
        ghost_collision = False
        ghost_cells = self.current_piece.get_rotation()
        current_offset = self.current_piece.get_x_offset()

        # Determines what the y offset for the ghost piece can be
        for ghost_x, ghost_y in ghost_cells:
            for i in range(self.grid.total_y):
                if not self.grid.border_collision(ghost_x + current_offset, ghost_y + i) and self.grid.empty_space(
                        ghost_x + current_offset, i):
                    if not ghost_collision:
                        ghost_offset = i - ghost_y
                if not self.grid.empty_space(ghost_x + current_offset, i):
                    ghost_collision = True
                    if i - (ghost_y + 1) < ghost_offset:
                        ghost_offset = i - (ghost_y + 1)
                    break

        # Draws a transparent piece where ghost piece should be
        for ghost_x, ghost_y in ghost_cells:
            surface = pygame.Surface((self.grid.cell_size, self.grid.cell_size))
            surface.set_alpha(155)
            cell_rect = pygame.Rect((ghost_x + current_offset) * self.grid.cell_size + self.grid.offset,
                                    (ghost_y + ghost_offset) * self.grid.cell_size + self.grid.offset,
                                    self.grid.cell_size - 1, self.grid.cell_size - 1)
            surface.fill((92, 97, 102))
            screen.blit(surface, cell_rect)

    def draw_next_piece(self, screen):
        """Draws the next piece preview on the side."""
        # Set the position for the next piece preview box
        next_piece_x = 450  # X position of the next piece preview
        next_piece_y = 80  # Y position of the next piece preview
        box_width = self.next_piece.cell_size * 3  # Width of the box
        box_height = self.next_piece.cell_size * 3  # Height of the box

        # Draw the box for the next piece
        box_color = (255, 255, 255)  # Light gray for the border
        pygame.draw.rect(screen, box_color,
                         pygame.Rect(next_piece_x - 35, next_piece_y - 10, box_width + 45, box_height + 50), 3)

        # Draw the next piece within the box
        for x, y in self.next_piece.cells[self.next_piece.current_rotation]:
            pygame.draw.rect(
                screen,
                self.next_piece.color[self.next_piece.piece_type],
                pygame.Rect(
                    next_piece_x + y * self.next_piece.cell_size,
                    next_piece_y + x * self.next_piece.cell_size,
                    self.next_piece.cell_size -1,
                    self.next_piece.cell_size -1
                )
            )

    def draw(self, screen):
        """Draws the main game grid, current piece, and upcoming piece."""
        self.grid.draw(screen)  # Draw the game grid
        self.current_piece.draw(screen)  # Draw the current piece
        self.draw_ghost(screen)  # Draw ghost piece (if implemented)
        self.draw_next_piece(screen)  # Draw the next piece
        self.draw_score(screen)  # Draw current score

    def draw_score(self, screen):
        # Display current score and high score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        high_score_text = font.render(f"High Score: {self.high_score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))  # Display current score in top left corner
        screen.blit(high_score_text, (420, 10))  # Position high score on the right

    def reset_game(self):
        """Resets the game state to start a new game."""
        self.grid = Grid(1)  # Reset the game grid
        self.available_pieces = []  # Reset available pieces
        self.current_piece = self.random_piece()  # Reset current piece
        self.next_piece = self.random_piece()  # Reset next piece
        self.game_over = False  # Reset game over state
        self.score = 0  # Reset score
        self.save_high_score()  # Save high score

