# Imports
import pygame
import HelperFunctions

# Initialize Pygame
pygame.init()

# Color Constants -----------------------------------------------------------------------
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)

# Screen Size Constants -----------------------------------------------------------------
SCREEN_WIDTH, SCREEN_HEIGHT = HelperFunctions.get_screen_dimensions()

# Player Paddle Properties --------------------------------------------------------------
PADDLE_SPEED_CONSTANT = 3
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 200
PADDLE1_X = 10
PADDLE2_X = SCREEN_WIDTH - (PADDLE1_X + PADDLE_WIDTH)
paddle1_Y = SCREEN_HEIGHT / 2 - (PADDLE_HEIGHT / 2)
paddle2_Y = SCREEN_HEIGHT / 2 - (PADDLE_HEIGHT / 2)
paddle1_Y_speed = 0
paddle2_Y_speed = 0

# Ball Properties -----------------------------------------------------------------------
INITIAL_BALL_SPEED_MULTIPLIER = 3
ball_speed_multiplier = INITIAL_BALL_SPEED_MULTIPLIER
BALL_WIDTH = 30
BALL_HEIGHT = 30
ball_X = SCREEN_WIDTH / 2 - (BALL_WIDTH / 2)
ball_Y = SCREEN_HEIGHT / 2 - (BALL_HEIGHT / 2)
ball_X_speed = 0
ball_Y_speed = 0

# Points and Scores ---------------------------------------------------------------------
player1_score = -1
player2_score = 0
POINTS_NEEDED_TO_WIN = 5

# Reset Game Flag -----------------------------------------------------------------------
reset_flag = False

# Ball Trail Properties -----------------------------------------------------------------
ball_trail = []
trail_timer = 0
TRAIL_INTERVAL = 30
MAX_TRAIL_LIST_SIZE = 5

# Print Instructions
HelperFunctions.print_instructions(POINTS_NEEDED_TO_WIN)

# Set starting x and y ball speed based on ball speed multiplier
ball_X_speed, ball_Y_speed = HelperFunctions.starting_ball_direction(
    INITIAL_BALL_SPEED_MULTIPLIER)

# Display the screen of appropriate size using screen constants
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Game Loop -----------------------------------------------------------------------------
running = True      # Flag that remains true while the game is still running
while running:
    screen.fill(BLACK)      # Make the screen black

    # Manage Keyboard Inputs ------------------------------------------------------------
    for event in pygame.event.get():        # Capture keyboard inputs
        if event.type == pygame.QUIT:       # If input is the quit button
            running = False                 # end game loop
        if event.type == pygame.KEYDOWN:    # If input is a keyboard key press
            
            # If key press is ENTER and reset_flag is True
            if event.key == pygame.K_RETURN and reset_flag:
                
                # Reset the ball speed
                ball_X_speed, ball_Y_speed = HelperFunctions.starting_ball_direction(
                    INITIAL_BALL_SPEED_MULTIPLIER
                ) 
                reset_flag = False          # Reset the flag

    keys = pygame.key.get_pressed()                # If a key is pressed, detect it

    if keys[pygame.K_w]:                           # Player 1 UP key
        paddle1_Y_speed = -PADDLE_SPEED_CONSTANT
    elif keys[pygame.K_s]:                         # Player 1 DOWN key
        paddle1_Y_speed = PADDLE_SPEED_CONSTANT
    else:                                          # Any other case
        paddle1_Y_speed = 0

    if keys[pygame.K_UP]:                          # Player 2 UP key
        paddle2_Y_speed = -PADDLE_SPEED_CONSTANT
    elif keys[pygame.K_DOWN]:                      # Player 2 DOWN key
        paddle2_Y_speed = PADDLE_SPEED_CONSTANT
    else:                                          # Any other case
        paddle2_Y_speed = 0

    # Manage and Draw Ball Trail --------------------------------------------------------
    trail_timer += 1        # For every frame, increment counter
    
    # Once a sufficient amount of time has passed (based on counter), add the x and y 
    # positions of the ball to the dictionary
    if trail_timer >= TRAIL_INTERVAL:
        ball_trail.append({"x": ball_X, "y": ball_Y})
        trail_timer = 0     # Reset the trail timer to 0

    # If ball_trail exceeds its max size, remove the oldest stored position
    if len(ball_trail) > MAX_TRAIL_LIST_SIZE:
        ball_trail.pop(0)           # removes the oldest trail after-image

    # Draw the ball trail
    HelperFunctions.draw_ball_trail(screen, ball_trail, BALL_WIDTH, BALL_HEIGHT)

    # Drawing Objects and Setting Hitboxes ----------------------------------------------
    
    # Thin dividing line in the center
    pygame.draw.rect(screen, WHITE, 
                     ((SCREEN_WIDTH // 2) - 1, 0, 2, screen.get_height()))

    # Draw paddle 1 and set paddle 1's hitbox
    pygame.draw.rect(screen, GREEN, 
                     (PADDLE1_X, paddle1_Y, PADDLE_WIDTH, PADDLE_HEIGHT)) 
    paddle1_hitbox = pygame.Rect(PADDLE1_X, paddle1_Y, PADDLE_WIDTH, PADDLE_HEIGHT)       

    # Draw paddle 2 and set paddle 2's hitbox
    pygame.draw.rect(screen, GREEN, 
                     (PADDLE2_X, paddle2_Y, PADDLE_WIDTH, PADDLE_HEIGHT))
    paddle2_hitbox = pygame.Rect(PADDLE2_X, paddle2_Y, PADDLE_WIDTH, PADDLE_HEIGHT)

    # Draw the ball and set the ball's hitbox
    pygame.draw.rect(screen, RED, (ball_X, ball_Y, BALL_WIDTH, BALL_HEIGHT))
    ball_hitbox = pygame.Rect(ball_X, ball_Y, BALL_WIDTH, BALL_HEIGHT)

    # Updating Paddle Positions Based on Keyboard Inputs --------------------------------
    paddle1_Y = HelperFunctions.update_paddle_position(paddle1_Y, paddle1_Y_speed, 
                                                       SCREEN_HEIGHT, PADDLE_HEIGHT)
    paddle2_Y = HelperFunctions.update_paddle_position(paddle2_Y, paddle2_Y_speed, 
                                                       SCREEN_HEIGHT, PADDLE_HEIGHT)

    # Update the Ball's Speed if it Collides with Upper or Lower Wall -------------------
    if ball_hitbox.top < 0:
        ball_Y_speed = -ball_Y_speed
        ball_Y = 0
    if ball_hitbox.bottom > SCREEN_HEIGHT:
        ball_Y_speed = -ball_Y_speed
        ball_Y = SCREEN_HEIGHT - BALL_HEIGHT

    # Update the Ball's Position and Speed Upon Collision with Paddle -------------------
    if ball_hitbox.colliderect(paddle1_hitbox) and ball_X_speed < 0:
        # Reset the ball's X position to the paddle's right to avoid phasing
        ball_X = paddle1_hitbox.right
        
        # Update the ball's speed based on collision
        ball_X_speed, ball_Y_speed = HelperFunctions.collision_ball_direction(
            ball_Y, BALL_HEIGHT, paddle1_Y, PADDLE_HEIGHT, 
            ball_speed_multiplier, True
        )
        # Speed up the ball (for shorter and more action-packed games)
        ball_speed_multiplier += 0.1

    if ball_hitbox.colliderect(paddle2_hitbox) and ball_X_speed > 0:
        # Reset the ball's X position to the paddle's left to avoid phasing
        ball_X = paddle2_hitbox.left - BALL_WIDTH
        
        # Update the ball's speed based on collision
        ball_X_speed, ball_Y_speed = HelperFunctions.collision_ball_direction(
            ball_Y, BALL_HEIGHT, paddle2_Y, PADDLE_HEIGHT, 
            ball_speed_multiplier, False
        )
        # Speed up the ball (for shorter and more action-packed games)
        ball_speed_multiplier += 0.1

    # Reset the Game if a Player Scores -------------------------------------------------
    
    # If the ball hits the right wall, increment player 1's score, reset ball
    # to the center, reset the speed multiplier, set ball speed to 0,
    # and set the reset flag to True so the [ENTER] key can restart the game
    if ball_hitbox.right > SCREEN_WIDTH:
        player1_score += 1
        ball_X = SCREEN_WIDTH / 2 - (BALL_WIDTH / 2)
        ball_Y = SCREEN_HEIGHT / 2 - (BALL_HEIGHT / 2)
        ball_speed_multiplier = INITIAL_BALL_SPEED_MULTIPLIER
        ball_X_speed = 0
        ball_Y_speed = 0
        reset_flag = True

    # If the ball hits the left wall, increment player 2's score, reset ball
    # to the center, reset the speed multiplier, set ball speed to 0,
    # and set the reset flag to True so the [ENTER] key can restart the game
    if ball_hitbox.left < 0:
        player2_score += 1
        ball_X = SCREEN_WIDTH / 2 - (BALL_WIDTH / 2)
        ball_Y = SCREEN_HEIGHT / 2 - (BALL_HEIGHT / 2)
        ball_speed_multiplier = INITIAL_BALL_SPEED_MULTIPLIER
        ball_X_speed = 0
        ball_Y_speed = 0
        reset_flag = True

    # Update the Score Board Every Frame ------------------------------------------------
    HelperFunctions.print_score(player1_score, player2_score, screen)

    # Add the Speed to the Ball's Position ----------------------------------------------
    ball_X += ball_X_speed
    ball_Y += ball_Y_speed

    # Stop the Game if a Player Wins ----------------------------------------------------
    if (player1_score >= POINTS_NEEDED_TO_WIN or player2_score >= POINTS_NEEDED_TO_WIN):
        # Print the winner and the score
        HelperFunctions.print_winner(player1_score, player2_score)
        # Stop the game loop
        running = False

    # Update the Display Every Frame ----------------------------------------------------
    pygame.display.update()