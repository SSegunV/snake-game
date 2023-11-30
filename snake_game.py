import pygame
import random

# Initialize Pygame
pygame.init()

# Define screen dimensions and colors
screen_width = 400
screen_height = 400
GRIDSIZE = 20
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)

# Create the Snake class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(screen_width // 2, screen_height // 2)]
        self.direction = (0, 1)
        self.color = (0, 255, 0)

    def move(self):
        cur = self.positions[0]
        x, y = self.direction
        new_x = (cur[0] + (x * GRIDSIZE)) % screen_width
        new_y = (cur[1] + (y * GRIDSIZE)) % screen_height
        new = (new_x, new_y)

        if new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()


    def change_direction(self, new_direction):
        if new_direction[0] * -1 != self.direction[0] or new_direction[1] * -1 != self.direction[1]:
            self.direction = new_direction

    def eat_food(self):
        self.length += 1

    def reset(self):
        self.length = 1
        self.positions = [(screen_width // 2, screen_height // 2)]
        self.direction = (0, 1)

# Create the Food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = (255, 0, 0)

    def randomize_position(self, snake_positions):
        while True:
            x = random.randrange(0, screen_width // GRIDSIZE) * GRIDSIZE
            y = random.randrange(0, screen_height // GRIDSIZE) * GRIDSIZE
            self.position = (x, y)
            if self.position not in snake_positions:
                break


# Create an instance of the Snake class
snake = Snake()

# Create an instance of the Food class
food = Food()

# Set up the game loop
running = True
clock = pygame.time.Clock()

#Handle user input
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction((0, -1))
            elif event.key == pygame.K_DOWN:
                snake.change_direction((0, 1))
            elif event.key == pygame.K_LEFT:
                snake.change_direction((-1, 0))
            elif event.key == pygame.K_RIGHT:
                snake.change_direction((1, 0))

    snake.move()

    if snake.positions[0] == food.position:
        snake.eat_food()
        food.randomize_position(snake.positions)

    if snake.positions[0][0] < 0 or snake.positions[0][0] >= screen_width or \
       snake.positions[0][1] < 0 or snake.positions[0][1] >= screen_height:
        running = False

    for segment in snake.positions[1:]:
        if segment == snake.positions[0]:
            running = False

    if (snake.positions[0][0] < 0 or snake.positions[0][0] >= screen_width or
        snake.positions[0][1] < 0 or snake.positions[0][1] >= screen_height):
        running = False  # End the game

    screen.fill(black)

    for segment in snake.positions:
        pygame.draw.rect(screen, snake.color, pygame.Rect(segment[0], segment[1], GRIDSIZE, GRIDSIZE))

    pygame.draw.rect(screen, food.color, pygame.Rect(food.position[0], food.position[1], GRIDSIZE, GRIDSIZE))

    pygame.display.update()

    clock.tick(10)

    # After the game loop
# Add a game-over message
game_over_font = pygame.font.Font(None, 36)
game_over_text = game_over_font.render("Game Over", True, white)
game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))

# Clear the screen and display the game-over message
screen.fill(black)
screen.blit(game_over_text, game_over_rect)
pygame.display.update()

# Wait for a few seconds before exiting
pygame.time.wait(2000)

pygame.quit()
