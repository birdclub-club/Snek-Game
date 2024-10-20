import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 500, 600

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
PINK = (255, 20, 147)
ORANGE = (255, 69, 0)
WHITE = (255, 255, 255)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snek Game')

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
chair_image = pygame.transform.scale(chair_image, (50, 50))

# Level properties
level = 1
score = 0
chair_pos = [random.randint(0, WIDTH - 50), random.randint(0, HEIGHT - 50)]
chair_direction = [5, 5]

# Game over function
def game_over():
    # Burn the snake effect
    for block in snake_body:
        pygame.draw.rect(screen, ORANGE, pygame.Rect(block[0], block[1], 10, 10))
        pygame.display.flip()
        pygame.time.wait(50)
    
    # Display game over message
    font = pygame.font.SysFont('courier', 20)
    message = 'Nice try snek, but the $ENT will not be yours today. Try again? Press Enter to play again or Esc to quit.'
    wrapped_text = [message[i:i+35] for i in range(0, len(message), 35)]
    y_offset = HEIGHT / 4
    for line in wrapped_text:
        game_over_surface = font.render(line, True, PINK)
        game_over_rect = game_over_surface.get_rect(center=(WIDTH / 2, y_offset))
        screen.blit(game_over_surface, game_over_rect)
        y_offset += 30
    screen.blit(chair_image, (WIDTH / 2 - 50, HEIGHT / 2))
    pygame.display.flip()
    
    # Wait for player to decide to play again or quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press Enter to play again
                    main()
                elif event.key == pygame.K_ESCAPE:  # Press Escape to quit
                    pygame.quit()
                    sys.exit()

# Main function
def main():
    global snake_pos, snake_body, snake_direction, change_to, food_pos, food_spawn, level, score, chair_pos, chair_direction
    
    # Reset snake properties
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    snake_direction = 'RIGHT'
    change_to = snake_direction
    speed = 15
    score = 0
    level = 1

    # Reset food properties
    food_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
    food_spawn = True

    # Main game loop
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
        if abs(snake_pos[0] - food_pos[0]) < 10 and abs(snake_pos[1] - food_pos[1]) < 10:
            food_spawn = False
            score += 1
            # Make snake flash pink briefly when it eats food
            for _ in range(3):
                screen.fill(WHITE)
                for pos in snake_body:
                    pygame.draw.rect(screen, PINK, pygame.Rect(pos[0], pos[1], 10, 10))
                pygame.display.update()
                pygame.time.wait(100)
        else:
            snake_body.pop()
        
        if not food_spawn:
            food_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
            food_spawn = True

        # Check for level progression
        if score >= 20 and level == 1:
            level = 2

        # Draw the screen
        screen.fill(WHITE)
        for pos in snake_body:
            pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))
        
        # Draw food as little pink square with a black 'E'
        pygame.draw.rect(screen, PINK, pygame.Rect(food_pos[0], food_pos[1], 15, 15))
        font = pygame.font.SysFont('courier', 12, bold=True)
        food_surface = font.render('E', True, WHITE)
        screen.blit(food_surface, (food_pos[0] + 1, food_pos[1] + 1))

        # Level 2: Add a bouncing chair
        if level == 2:
            chair_pos[0] += chair_direction[0]
            chair_pos[1] += chair_direction[1]

            # Bounce chair off the walls
            if chair_pos[0] <= 0 or chair_pos[0] >= WIDTH - 50:
                chair_direction[0] = -chair_direction[0]
            if chair_pos[1] <= 0 or chair_pos[1] >= HEIGHT - 50:
                chair_direction[1] = -chair_direction[1]

            screen.blit(chair_image, (chair_pos[0], chair_pos[1]))

            # Check if snake collides with the chair
            if (chair_pos[0] < snake_pos[0] < chair_pos[0] + 50 or chair_pos[0] < snake_pos[0] + 10 < chair_pos[0] + 50) and \
               (chair_pos[1] < snake_pos[1] < chair_pos[1] + 50 or chair_pos[1] < snake_pos[1] + 10 < chair_pos[1] + 50):
                game_over()

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

# Run the main function
if __name__ == "__main__":
    main()

