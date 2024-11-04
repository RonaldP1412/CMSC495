""""
CMSC 495 7384 Capstone in Computer Science (2248)
Project: Tetris game made with pygame
University of Maryland Global Campus
Group 3:Ronald Parra De Jesus, Anthony Petrowich, Colton Purdy, Kelvin Ruvio-Amaya, Asher Russell, Phillip Seisman
and Julian Sotelo
Professor Davis
"""

# Merged Tetris Game with Sound, Title Screen Controls, and High Score
import pygame
from tetris_logic import TetrisLogic

# Initialize Pygame and Pygame Mixer
pygame.init()
pygame.mixer.init()

# Load sounds
pygame.mixer.music.load('8bit-music-for-game-68698.mp3')  # Background music
game_over_sound = pygame.mixer.Sound('game-over-arcade-6435.mp3')  # Sound played when game is over
line_clear_sound = pygame.mixer.Sound('076833_magic-sfx-for-games-86023.mp3')  # Sound played when a line is cleared
collision_sound = pygame.mixer.Sound('woosh-230554.mp3')  # Sound played on collision

# Set up the screen
COLOR = (33, 46, 59)
screen_width, screen_height = 640, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tetris: Project Alexey")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Start background music
pygame.mixer.music.play(-1)  # Loop background music indefinitely

# Initialize game logic
game_logic = TetrisLogic(line_clear_sound, collision_sound, game_over_sound)
game_state = "TITLE"  # Set the initial game state to the title screen
normal_drop_speed = 800  # Normal block drop speed in milliseconds
fast_drop_speed = 100  # Speed when dropping block quickly with DOWN key

# Function to draw the title screen with controls
def draw_title_screen():
    screen.fill(COLOR)
    title_text = font.render("Tetris: Project Alexey", True, (255, 255, 255))
    start_text = font.render("Press ENTER to Start", True, (255, 255, 255))
    quit_text = font.render("Press Q to Quit", True, (255, 255, 255))

    # Display game controls
    controls_title = font.render("Controls:", True, (255, 255, 255))
    move_text = font.render("A / D - Move Left / Right", True, (200, 200, 200))
    rotate_text = font.render("W - Rotate Right", True, (200, 200, 200))
    drop_text = font.render("S - Speed Up Drop", True, (200, 200, 200))

    # Center and display all text on the title screen
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 200))
    screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, 300))
    screen.blit(quit_text, (screen_width // 2 - quit_text.get_width() // 2, 350))
    screen.blit(controls_title, (screen_width // 2 - controls_title.get_width() // 2, 450))
    screen.blit(move_text, (screen_width // 2 - move_text.get_width() // 2, 500))
    screen.blit(rotate_text, (screen_width // 2 - rotate_text.get_width() // 2, 550))
    screen.blit(drop_text, (screen_width // 2 - drop_text.get_width() // 2, 600))
    pygame.display.update()

# Main game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Clear the screen for each frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle game states and user input
        if game_state == "TITLE":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start the game
                    game_state = "PLAYING"
                    game_logic.reset_game()  # Reset game logic for a new game
                    pygame.time.set_timer(game_logic.AUTO_MOVE, normal_drop_speed)  # Set normal drop speed
                elif event.key == pygame.K_q:  # Quit the game
                    running = False

        elif game_state == "PLAYING":
            game_logic.auto_move(event)  # Automatically move the piece down

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:  # Move left
                    game_logic.move_left()
                elif event.key == pygame.K_d:  # Move right
                    game_logic.move_right()
                elif event.key == pygame.K_s:  # Speed up the drop
                    pygame.time.set_timer(game_logic.AUTO_MOVE, fast_drop_speed)  # Set fast drop speed
                elif event.key == pygame.K_w:  # Rotate piece
                    game_logic.rotate_right()
                elif event.key == pygame.K_p:  # Pause the game
                    game_state = "PAUSED"
            elif event.type == pygame.KEYUP and event.key == pygame.K_s:  # Reset speed after release
                pygame.time.set_timer(game_logic.AUTO_MOVE, normal_drop_speed)

            # Check if the game is over
            if game_logic.game_over:
                game_state = "GAME_OVER"  # Change state to game over
                game_over_sound.play()  # Play game over sound

        elif game_state == "PAUSED":
            paused_text = font.render("Paused", True, (255, 255, 0))  # Display pause text
            screen.blit(paused_text, (screen_width // 2 - paused_text.get_width() // 2, screen_height // 2))
            pygame.display.update()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:  # Unpause the game
                game_state = "PLAYING"

        elif game_state == "GAME_OVER":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game
                    game_logic.reset_game()
                    game_state = "PLAYING"
                elif event.key == pygame.K_q:  # Quit the game
                    running = False

    # Display the relevant game screen based on the current state
    if game_state == "TITLE":
        draw_title_screen()  # Draw the title screen
    elif game_state == "PLAYING":
        game_logic.draw(screen)  # Draw the game grid and pieces


    elif game_state == "GAME_OVER":
        font_large = pygame.font.Font(None, 74)
        game_over_text = font_large.render("Game Over", True, (255, 0, 0))  # Display game over message
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 3))
        restart_text = font.render("Press 'R' to Restart or 'Q' to Quit", True, (200, 200, 200))
        screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2))

    pygame.display.flip()  # Refresh the screen once per loop iteration
    clock.tick(60)  # Limit the frame rate to 60 FPS

pygame.quit()  # Quit Pygame and clean up
