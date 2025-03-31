import math
import pygame
import random
import os

class GameWindow():
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Maze")
        self.colors = {"WHITE": (255, 255, 255), "GREY": (178, 190, 181), "BLACK": (0, 0, 0), 
                       "RED": (210, 43, 43), "GREEN": (49, 146, 54), "BLUE": (76, 81, 247),
                       "PURPLE": (157, 77, 187), "GOLD": (243, 175, 25), "GREY2": (100, 100, 100)}
        self.font = pygame.font.SysFont(None, 55)
        self.dt = 0
        self.player_total_points = 0
        self.gamestate = True
        self.maze_setup()

        self.total_position = 0
        self.top_condition = False
        self.bottom_condition = False
        self.left_condition = False
        self.right_condition = False

    def maze_setup(self):
        # Maze setup
        self.width, self.height = 5, 5  # Maze size (10x10)
        self.cell_size = 60  # Each cell (room) will be 50x50 pixels
        self.maze = self.create_maze(self.width, self.height)

        # Define start and end positions
        self.start_x, self.start_y = random.randint(0, self.width - 1), self.height - 1
        end_x_corner = random.choice([0, self.height - 1])
        end_y_corner = 0
        self.end_x, self.end_y = end_x_corner, end_y_corner 

        # Player position starts at the start room
        self.player_x, self.player_y = self.start_x, self.start_y

    def create_maze(self, width, height):
        # Maze grid initialized with all walls present
        maze = [[{'top': True, 'bottom': True, 'left': True, 'right': True, 'visited': False}
                 for _ in range(width)] for _ in range(height)]

        def get_neighbors(x, y):
            """Returns a list of unvisited neighbors with their directions."""
            neighbors = []
            directions = [(0, -1, 'top', 'bottom'), (0, 1, 'bottom', 'top'),
                          (-1, 0, 'left', 'right'), (1, 0, 'right', 'left')]

            for dx, dy, wall, opposite in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height and not maze[ny][nx]['visited']:
                    neighbors.append((nx, ny, wall, opposite))

            return neighbors

        def carve_maze(x, y):
            """Recursive function to generate the maze."""
            maze[y][x]['visited'] = True
            neighbors = get_neighbors(x, y)
            random.shuffle(neighbors)

            for nx, ny, wall, opposite in neighbors:
                if not maze[ny][nx]['visited']:
                    maze[y][x][wall] = False  # Remove wall from current room
                    maze[ny][nx][opposite] = False  # Remove opposite wall from next room
                    carve_maze(nx, ny)

        # Start maze generation from a random position
        start_x, start_y = random.randint(0, width - 1), random.randint(0, height - 1)
        carve_maze(start_x, start_y)

        return maze

    def draw_maze(self):
        """Render the maze on the Pygame screen."""
        for y in range(self.height):
            for x in range(self.width):
                room = self.maze[y][x]
                room_x = x * self.cell_size
                room_y = y * self.cell_size

                # Draw walls
                if room['top']:
                    pygame.draw.line(self.screen, self.colors['BLACK'], (room_x, room_y), 
                                     (room_x + self.cell_size, room_y), 2)
                if room['bottom']:
                    pygame.draw.line(self.screen, self.colors['BLACK'], (room_x, room_y + self.cell_size), 
                                     (room_x + self.cell_size, room_y + self.cell_size), 2)
                if room['left']:
                    pygame.draw.line(self.screen, self.colors['BLACK'], (room_x, room_y), 
                                     (room_x, room_y + self.cell_size), 2)
                if room['right']:
                    pygame.draw.line(self.screen, self.colors['BLACK'], (room_x + self.cell_size, room_y), 
                                     (room_x + self.cell_size, room_y + self.cell_size), 2)
                    
        end_x_pos = self.end_x * self.cell_size
        end_y_pos = self.end_y * self.cell_size
        pygame.draw.rect(self.screen, self.colors["GREEN"], (end_x_pos, end_y_pos, self.cell_size, self.cell_size))

    def draw_player(self):
        """Draw the player as a red circle."""
        player_x_pos = self.player_x * self.cell_size + self.cell_size // 2
        player_y_pos = self.player_y * self.cell_size + self.cell_size // 2
        pygame.draw.circle(self.screen, self.colors["RED"], (player_x_pos, player_y_pos), 10)

    def reset_game(self):
        self.total_position = 4
        self.player_total_points = 0
        self.gamestate = True
        self.maze_setup()
    
    def draw_text(self, text, x, y, color):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
    
    def top(self):
        self.top_condition = True

    def reset_top_condition(self):
        self.top_condition = False

    def bottom(self):
        self.bottom_condition = True

    def reset_bottom_condition(self):
        self.bottom_condition = False

    def left(self):
        self.left_condition = True

    def reset_left_condition(self):
        self.left_condition = False

    def right(self):
        self.right_condition = True

    def reset_right_condition(self):
        self.right_condition = False       

    def main(self):
        running = True
        clock = pygame.time.Clock()
        time_elapsed = 0

        while running:
            self.screen.fill(self.colors["GREY"])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.reset_game()
                elif event.type == pygame.KEYDOWN:
                    # Move player with arrow keys
                    if event.key == pygame.K_UP and not self.maze[self.player_y][self.player_x]['top']:
                        self.total_position += 0
                        self.player_y -= 1
                    elif event.key == pygame.K_DOWN and not self.maze[self.player_y][self.player_x]['bottom']:
                        self.total_position += 2
                        self.player_y += 1
                    elif event.key == pygame.K_LEFT and not self.maze[self.player_y][self.player_x]['left']:
                        self.total_position -= -1
                        self.player_x -= 1
                    elif event.key == pygame.K_RIGHT and not self.maze[self.player_y][self.player_x]['right']:
                        self.total_position += 1
                        self.player_x += 1

                    print(self.total_position)
                    if self.total_position % 4 == 0 or self.total_position == 0:
                        print('straight')
                    elif self.total_position % 2 == 0:
                        print('backwards')
                    elif self.total_position % 4 == 3 or self.total_position == -1:
                        print('left')
                    elif self.total_position % 4 == 1 or self.total_position == 1:
                        print('right')

                    if self.maze[self.player_y][self.player_x]['top']:
                        self.top()
                    else:
                        self.reset_top_condition()

                    if self.maze[self.player_y][self.player_x]['bottom']:
                        self.bottom()
                    else:
                        self.reset_bottom_condition()                    

                    if self.maze[self.player_y][self.player_x]['left']:
                        self.left()
                    else:
                        self.reset_left_condition()     

                    if self.maze[self.player_y][self.player_x]['right']:
                        self.right()
                    else:
                        self.reset_right_condition()     

            if self.top_condition:
                self.draw_text('t', self.screen_width - 250, self.screen_height // 10, self.colors["BLACK"])
            if self.bottom_condition:
                self.draw_text('b', self.screen_width - 200, self.screen_height // 10, self.colors["BLACK"])
            if self.left_condition:
                self.draw_text('l', self.screen_width - 150, self.screen_height // 10, self.colors["BLACK"])
            if self.right_condition:
                self.draw_text('r', self.screen_width - 100, self.screen_height // 10, self.colors["BLACK"])

            if self.gamestate:
                time_elapsed += self.dt
                # Game logic

                self.draw_maze()
                self.draw_player()
                # self.draw_text(f'{int(self.player_total_points)}', self.screen_width - 200, self.screen_height // 10, self.colors["BLACK"])

                # Check if the player reached the end
                if self.player_x == self.end_x and self.player_y == self.end_y:
                    self.gamestate = False  # End the game if player reaches the end room

            else:
                self.screen.fill(self.colors["GREY"])
                self.draw_text(f"FINAL SCORE: {self.player_total_points}", self.screen_width // 5, self.screen_height // 2, self.colors["BLACK"])

            pygame.display.flip()
            self.dt = clock.tick(60) / 1000
        
        pygame.quit()

if __name__ == "__main__":
    game = GameWindow()
    game.main()
