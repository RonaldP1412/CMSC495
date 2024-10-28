import pygame
'''The code is a Python program that implements a Tetris game using Pygame library with game
    states for start menu, playing, and paused, along with event handling for controls and interactions.
    
    '''
import sys
from tetris_logic import TetrisLogic

pygame.init()

COLOR = (33, 46, 59)  # Background color
screen = pygame.display.set_mode((400, 800))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)  # Standard font for text

# Game logic and states
logic = TetrisLogic()
START_MENU = 0
PLAYING = 1
PAUSED = 2
game_state = START_MENU  # Initial state is the start menu
normal_drop_speed = 200
fast_drop_speed = 50

# Start menu function with controls
    """
    The function `draw_start_menu` displays the title and options for starting or quitting the game in a
    graphical user interface.
    """
    screen.fill(COLOR)
    title_text = font.render("TETRIS", True, (255, 255, 255))
    start_text = font.render("Press ENTER to Start", True, (255, 255, 255))
    quit_text = font.render("Press Q to Quit", True, (255, 255, 255))
    
    # Control instructions
# The code  is responsible for rendering text elements related to controls on the
# screen in the start menu of the Tetris game. Here's a breakdown of what each part of the code does:
    controls_title = font.render("Controls:", True, (255, 255, 255))
    move_text = font.render("A / D - Move Left / Right", True, (200, 200, 200))
    rotate_text = font.render("W / S - Rotate Right / Left", True, (200, 200, 200))
    drop_text = font.render("DOWN - Speed Up Drop", True, (200, 200, 200))
    pause_text = font.render("P - Pause Game", True, (200, 200, 200))

    # The code is responsible for rendering and displaying
    # text elements on the screen in the start menu of the Tetris game. Here's a breakdown of what
    # each part of the code does:
    # Display title and menu options
    screen.blit(title_text, (150, 200))
    screen.blit(start_text, (100, 300))
    screen.blit(quit_text, (120, 350))
    
    # The code is responsible for displaying control instructions on the screen
    # in the Tetris game. Here's a breakdown of what each part of the code does:
    # Display controls
    screen.blit(controls_title, (150, 450))
    screen.blit(move_text, (100, 500))
    screen.blit(rotate_text, (100, 550))
    screen.blit(drop_text, (100, 600))
    screen.blit(pause_text, (100, 650))
    
    pygame.display.update()

# The `# Main game loop` section in the provided Python code is the central part of the Tetris
# game program. Here's what it does:
# Main game loop
while True:
    if game_state == START_MENU:
        draw_start_menu()
    elif game_state == PLAYING:
        screen.fill(COLOR)
        logic.draw(screen)

       # The code  `score_text = font.render(f"Score: {logic.score}", True, (255, 255, 255))`
       # is rendering the current score of the player in the Tetris game. It uses the `font.render`
       # method to create a text surface with the text "Score: " followed by the actual score value
       # stored in the `logic.score` variable. The `(255, 255, 255)` tuple specifies the color of the
       # text, which in this case is white.
        # Display score
        score_text = font.render(f"Score: {logic.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

       # The code is responsible for displaying a "Game Over" message on the
       # screen when the game over condition is met in the Tetris game. Here's a breakdown of what
       # each part of the code does:
        # Display game over message
        if logic.game_over:
            game_over_text = font.render("Game Over! Press ENTER to restart.", True, (255, 0, 0))
            screen.blit(game_over_text, (20, 400))

        pygame.display.update()
        clock.tick(60)
    # The code block `elif game_state == PAUSED:` is responsible for handling the game state when the
    # Tetris game is paused.
    elif game_state == PAUSED:
        paused_text = font.render("Paused", True, (255, 255, 0))
        screen.blit(paused_text, (150, 400))
        pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Start menu interactions
           # The code  `if game_state == START_MENU:` is checking if the current game state is
           # the start menu state. If this condition is met, the subsequent `if event.key ==
           # pygame.K_RETURN:` is checking if the player has pressed the 'RETURN' key to start the
           # game.
            if game_state == START_MENU:
                if event.key == pygame.K_RETURN:  # Start game
                    game_state = PLAYING
                    logic.reset()
                # The code snippet `elif event.key == pygame.K_q:  # Quit game
                #                     pygame.quit()
                #                     sys.exit()` is handling the event when the player presses the
                # 'Q' key during the start menu state of the game.
                elif event.key == pygame.K_q:  # Quit game
                    pygame.quit()
                    sys.exit()

            # Playing state interactions
            # This block of code is responsible for handling player interactions during the `PLAYING`
            # state of the game in the Tetris program. Here's a breakdown of what each part of the
            # code snippet does:
            elif game_state == PLAYING:
                if logic.game_over:
                    if event.key == pygame.K_RETURN:
                        logic.game_over = False
                        logic.reset()
                elif event.key == pygame.K_a and not logic.game_over:
                    logic.move_left()
                elif event.key == pygame.K_d and not logic.game_over:
                    logic.move_right()
                elif event.key == pygame.K_s and not logic.game_over:
                    logic.move_down()
                elif event.key == pygame.K_w and not logic.game_over:
                    logic.rotate_right()
                elif event.key == pygame.K_p:  # Pause game
                    game_state = PAUSED
                elif event.key == pygame.K_DOWN:
                    pygame.time.set_timer(logic.AUTO_MOVE, fast_drop_speed)

            # Paused state interactions
           # The code is handling the event when the game state is set to
           # `PAUSED` and the player presses the 'P' key.
            elif game_state == PAUSED:
                # When the game state is set to `PAUSED` and the player presses the 'P' key, the code
                # snippet `if event.key == pygame.K_p:  # Unpause game
                #                     game_state = PLAYING` is responsible for changing the game state
                # back to `PLAYING`, effectively unpausing the game and allowing the player to
                # continue playing from where they left off. This allows the player to resume the game
                # after it has been paused by pressing the 'P' key.
                if event.key == pygame.K_p:  # Unpause game
                    game_state = PLAYING

        elif event.type == pygame.KEYUP:
            # Reset drop speed when DOWN key is released
           # The code  `if event.key == pygame.K_DOWN:` is checking if the key pressed by the
           # player is the DOWN arrow key. If the condition is met, the code
           # `pygame.time.set_timer(logic.AUTO_MOVE, normal_drop_speed)` is executed.
            if event.key == pygame.K_DOWN:
                pygame.time.set_timer(logic.AUTO_MOVE, normal_drop_speed)

        if game_state == PLAYING:
            logic.auto_move(event)
