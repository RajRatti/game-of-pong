# Imports
import tkinter as tk
import pygame
import random
import math

"""
print_instructions(POINTS_NEEDED_TO_WIN)

Prints the instructions of Pong before the game GUI appears. The parameter is used to 
variably print the points required to win. The player controls are also printed.
"""
def print_instructions(POINTS_NEEDED_TO_WIN):
    # Instructions
    print("\n" + 91 * "=")
    print("THE GAME OF PONG:")
    print(
        "1. Pong is a tennis-like game where players wield paddles and take " 
        "turns hitting a ball.")
    print(
        "2. A player scores a point if they manage to get the ball past their "
        "opponent's paddle.")
    print(
        "3. Once a player scores a point, the ball will reset. Press [ENTER] "
        "to restart the match.")
    print("4. The ball gets faster with each successive hit.")
    print(f"5. First player to {POINTS_NEEDED_TO_WIN} points wins.")
    print(91 * "=")
    print(
        "CONTROLS:\n"
        "Player 1 Paddle Movement: w/s\n"
        "Player 2 Paddle Movement: up/down arrow key")
    print(91 * "=")

"""
get_screen_dimensions()

Uses Tkinter to get the screen width and height, stores them, and returns them to the 
main program.
"""
def get_screen_dimensions():
    root = tk.Tk()                              # initialize root
    SCREEN_WIDTH = root.winfo_screenwidth()     # get screen width using root
    SCREEN_HEIGHT = root.winfo_screenheight()   # get screen height using root
    root.destroy()                              # destroy root
    
    return SCREEN_WIDTH, SCREEN_HEIGHT          # return screen width and height

"""
starting_ball_direction(INITIAL_BALL_SPEED_MULTIPLIER)

Upon the ball's reset, a random angle from a list of valid angles is chosen to be the 
ball's starting direction. The ball's x and y speeds are determined from the angle and
returned to the main program.
"""
def starting_ball_direction(INITIAL_BALL_SPEED_MULTIPLIER):
    # Choose a random angle between [-60,60] or [120,240] degrees
    valid_angles = list(range(-60, 60)) + list(range(120, 240))
    # Convert the angle to radians
    angle = math.radians(random.choice(valid_angles))
    # Set ball_X_speed and ball_Y_speed using the cosine and sine of the angle
    ball_X_speed = INITIAL_BALL_SPEED_MULTIPLIER * math.cos(angle)
    ball_Y_speed = INITIAL_BALL_SPEED_MULTIPLIER * math.sin(angle)
    
    # Return ball_X_speed and ball_Y_speed
    return ball_X_speed, ball_Y_speed

"""
update_paddle_position(paddle_Y, paddle_Y_speed, SCREEN_HEIGHT, PADDLE_HEIGHT)

Uses the paddle's speed (set by player input) and its current position to determine the
updated position. Bounds checking is performed, and the new position is returned to the 
main program.
"""
def update_paddle_position(paddle_Y, paddle_Y_speed, SCREEN_HEIGHT, PADDLE_HEIGHT):
    # Increase paddle position by speed (change based on input)
    paddle_Y += paddle_Y_speed
    # If new paddle position exceeds the screen height, set it back to screen height
    # If new paddle position is negative, set it back to 0
    paddle_Y = max(0, min(paddle_Y, SCREEN_HEIGHT - PADDLE_HEIGHT))
    
    # Return the updated and checked position
    return paddle_Y

"""
collision_ball_direction(ball_Y, BALL_HEIGHT, paddle_Y, PADDLE_HEIGHT, 
                         BALL_SPEED_MULTIPLIER, going_left)

When the ball (in play) collides with a paddle, the collision position is used to 
determine the new ball direction. The closer the collision is to the ends of the paddle, 
the sharper the ball's angle will be. A going_left flag is used to return the appropriate
speeds of the ball to the main program.
"""
def collision_ball_direction(ball_Y, BALL_HEIGHT, paddle_Y, PADDLE_HEIGHT, 
                             BALL_SPEED_MULTIPLIER, going_left):

    # Determine the y-position of the collision relative to the paddle's center
    hit_pos = (ball_Y + BALL_HEIGHT / 2) - (paddle_Y + PADDLE_HEIGHT / 2)
    # Based on hit position, create a rebound angle between [-60,60] degrees
    # and convert it to radians
    angle = math.radians(60 * (hit_pos / PADDLE_HEIGHT) * 2)
    
    # Set ball_X_speed and ball_Y_speed using the cosine and sine of the angle
    ball_X_speed = BALL_SPEED_MULTIPLIER * math.cos(angle)
    ball_Y_speed = BALL_SPEED_MULTIPLIER * math.sin(angle)

    # If ball hit the left paddle, set x-speed to positive
    if going_left:
        return ball_X_speed, ball_Y_speed
    # If ball hit the right paddle, set x-speed to negative
    else:
        return -ball_X_speed, ball_Y_speed

"""
draw_ball_trail(surface, trail, BALL_WIDTH, BALL_HEIGHT)

Using a dictionary that stores the ball's previous positions, fading rectangles are drawn
behind the ball's current position to create a ball trail effect. The rectangle opacities
are determined by their recency, and the rectangles are drawn onto the GUI surface. Any
transparent rectangles are not drawn.
"""
def draw_ball_trail(surface, trail, BALL_WIDTH, BALL_HEIGHT):
    # Iterate through each position in the trail dictionary
    for i, pos in enumerate(trail):
        # The older the position, the fainter the trail color
        alpha = int(255 * (i / len(trail)))
        if alpha > 0:      # Skip fully transparent trail segments
            # Draw the after-image using the trail color
            pygame.draw.rect(surface, (alpha, 0, 0), 
                             (pos["x"], pos["y"], BALL_WIDTH, BALL_HEIGHT))

"""
print_score(player1_score, player2_score, screen)

Using a pygame font, the scores of each player are drawn onto the bottom-middle of the
screen. 
"""
def print_score(player1_score, player2_score, screen):
    WHITE = (255,255,255)           # Constants for appearance and structure
    FONT_SIZE = 128
    PADDING_BOTTOM = 50
    SPACING = 100

    font = pygame.font.Font(None, FONT_SIZE)        # font

    p1_text = font.render(f"{player1_score}", True, WHITE)  # Create player 1 score text
    p2_text = font.render(f"{player2_score}", True, WHITE)  # Create player 2 score text

    p1_rect = p1_text.get_rect()        # Get a rectangle outline of the texts
    p2_rect = p2_text.get_rect()

    # Find the horizontal center of the screen
    center_x = screen.get_width() // 2
    # Find the appropriate vertical location for the scores
    bottom_y = screen.get_height() - PADDING_BOTTOM

    # Set the rectangle positions
    p1_rect.midright = (center_x - SPACING // 2, bottom_y)
    p2_rect.midleft  = (center_x + SPACING // 2, bottom_y)

    screen.blit(p1_text, p1_rect)       # print player 1's score
    screen.blit(p2_text, p2_rect)       # print player 2's score

"""
print_winner(player1_score, player2_score)

When a player scores the winning amount of points, the game ends, both scores are 
displayed, and the winner is determined.
"""
def print_winner(player1_score, player2_score):
    print(f"FINAL SCORE: {player1_score} - {player2_score}")        # Print final score
    
    # Print "PLAYER ONE WINS!" if player 1 had the higher score
    if (player1_score > player2_score): 
        print("PLAYER ONE WINS!")
        
    # Print "PLAYER TWO WINS!" if player 2 had the higher score
    elif(player2_score > player1_score):
        print("PLAYER TWO WINS!")
    
    print(91 * "=" + "\n")