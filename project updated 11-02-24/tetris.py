
"""" 
CMSC 495 7384 Capstone in Computer Science (2248)
Project: Tetris game made with pygame
University of Maryland Global Campus
Group 3:Ronald Parra De Jesus, Anthony Petrowich, Colton Purdy, Kelvin Ruvio-Amaya, Asher Russell, Phillip Seisman
and Julian Sotelo
Professor Davis
"""
import pygame
import sys
from tetris_logic import TetrisLogic

pygame.init()
pygame.mixer.init()

# Load sounds
pygame.mixer.music.load('8bit-music-for-game-68698.mp3')  # Background music
game_over_sound = pygame.mixer.Sound('game-over-arcade-6435.mp3')  # Game over sound
line_clear_sound = pygame.mixer.Sound('076833_magic-sfx-for-games-86023.mp3')  # Line clear sound
collision_sound = pygame.mixer.Sound('woosh-230554.mp3')  # Collision sound

# Set up the screen
COLOR = (33, 46, 59)
screen = pygame.display.set_mode((600, 800))  # Increased width for the Next Piece box
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Start background music
pygame.mixer.music.play(-1)  # Loop background music indefinitely

# Game logic and states
logic = TetrisLogic(line_clear_sound, collision_sound, game_over_sound)
START_MENU = 0
PLAYING = 1
PAUSED = 2
game_state = START_MENU
normal_drop_speed = 2000  # Set to 2000 ms (2 seconds) for slower drop
fast_drop_speed = 100     # Fast drop speed when holding DOWN key

def draw_start_menu():
    screen.fill(COLOR)
    title_text = font.render("TETRIS", True, (255, 255, 255))
    start_text = font.render("Press ENTER to Start", True, (255, 255, 255))
    quit_text = font.render("Press Q to Quit", True, (255, 255, 255))

    controls_title = font.render("Controls:", True, (255, 255, 255))
    move_text = font.render("A / D - Move Left / Right", True, (200, 200, 200))
    rotate_text = font.render("W / S - Rotate Right / Left", True, (200, 200, 200))
    drop_text = font.render("DOWN - Speed Up Drop", True, (200, 200, 200))
    pause_text = font.render("P - Pause Game", True, (200, 200, 200))

    screen.blit(title_text, (150, 200))
    screen.blit(start_text, (100, 300))
    screen.blit(quit_text, (120, 350))
    screen.blit(controls_title, (150, 450))
    screen.blit(move_text, (100, 500))
    screen.blit(rotate_text, (100, 550))
    screen.blit(drop_text, (100, 600))
    screen.blit(pause_text, (100, 650))

    pygame.display.update()

# Main game loop
while True:
    if game_state == START_MENU:
        draw_start_menu()
    elif game_state == PLAYING:
        screen.fill(COLOR)
        logic.draw(screen)
        logic.draw_next_piece(screen)  # Draw the next piece box and the upcoming piece

        # Display current score and high score
        score_text = font.render(f"Score: {logic.score}", True, (255, 255, 255))
        high_score_text = font.render(f"High Score: {logic.high_score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (420, 10))  # Position high score on the right

        # Display game over message and play game-over sound once
        if logic.game_over:
            game_over_text = font.render("Game Over! Press ENTER to restart.", True, (255, 0, 0))
            screen.blit(game_over_text, (20, 400))
            if not logic.game_over_sound_played:
                logic.game_over_sound.play()  # Play game-over sound once
                logic.game_over_sound_played = True  # Ensure it plays only once

        pygame.display.update()
        clock.tick(60)
    elif game_state == PAUSED:
        paused_text = font.render("Paused", True, (255, 255, 0))
        screen.blit(paused_text, (150, 400))
        pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if game_state == START_MENU:
                if event.key == pygame.K_RETURN:
                    game_state = PLAYING
                    logic.reset()
                    pygame.time.set_timer(logic.AUTO_MOVE, normal_drop_speed)  # Set normal drop speed on game start
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            elif game_state == PLAYING:
                if logic.game_over:
                    if event.key == pygame.K_RETURN:
                        logic.game_over = False
                        logic.reset()
                        pygame.time.set_timer(logic.AUTO_MOVE, normal_drop_speed)  # Reset timer for new game
                elif event.key == pygame.K_a and not logic.game_over:
                    logic.move_left()
                elif event.key == pygame.K_d and not logic.game_over:
                    logic.move_right()
                elif event.key == pygame.K_s and not logic.game_over:
                    logic.move_down()
                elif event.key == pygame.K_w and not logic.game_over:
                    logic.rotate_right()
                elif event.key == pygame.K_p:
                    game_state = PAUSED
                elif event.key == pygame.K_DOWN:
                    pygame.time.set_timer(logic.AUTO_MOVE, fast_drop_speed)  # Set faster drop speed when DOWN is pressed
            elif game_state == PAUSED:
                if event.key == pygame.K_p:
                    game_state = PLAYING
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pygame.time.set_timer(logic.AUTO_MOVE, normal_drop_speed)  # Reset to normal speed when DOWN is released

    if game_state == PLAYING:
        logic.auto_move(event)
