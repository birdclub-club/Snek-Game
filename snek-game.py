import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
PINK = (255, 20, 147)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Snake properties
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
snake_direction = 'RIGHT'
change_to = snake_direction
speed = 15

# Food properties
food_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
food_spawn = True

# Load the pixelated chair image
chair_image = pygame.image.load('pixelated_chair.png')
chair_image = pygame.transform.scale(chair_image, (100, 100))

# Game over function
def game_over():
    font = pygame.font.SysFont('times new roman', 35)
    game_over_surface = font.render('You Lost', True, PINK)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (WIDTH / 2, HEIGHT / 4)
    screen.blit(game_over_surface, game_over_rect)
    screen.blit(chair_image, (WIDTH / 2 - 50, HEIGHT / 2 - 50))
    pygame.display.flip()
    
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

# Main logic
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not change_to == 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and not change_to == 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT and not change_to == 'RIGHT':
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT and not change_to == 'LEFT':
                change_to = 'RIGHT'
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Change direction of snake
    snake_direction = change_to

    # Update the position of the snake head
    if snake_direction == 'UP':
        snake_pos[1] -= 10
    if snake_direction == 'DOWN':
        snake_pos[1] += 10
    if snake_direction == 'LEFT':
        snake_pos[0] -= 10
    if snake_direction == 'RIGHT':
        snake_pos[0] += 10

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos == food_pos:
        food_spawn = False
    else:
        snake_body.pop()
        
    if not food_spawn:
        food_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
        food_spawn = True

    # Draw the screen
    screen.fill(BLACK)
    for pos in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))
        
    # Draw food
    font = pygame.font.SysFont('times new roman', 25)
    food_surface = font.render('E', True, PINK)
    screen.blit(food_surface, (food_pos[0], food_pos[1]))

    # Check if snake collides with boundaries
    if snake_pos[0] < 0 or snake_pos[0] > (WIDTH-10):
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > (HEIGHT-10):
        game_over()

    # Check if snake collides with itself
    for block in snake_body[1:]:
        if snake_pos == block:
            game_over()

    # Refresh game screen
    pygame.display.update()

    # Frame Per Second /Refresh Rate
    clock.tick(speed)
