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
        self.maze_orientations = ["straight", "right", "backwards", "left"]
        self.current_maze_index = 0
        
        self.top_wall = False
        self.bottom_wall = False
        self.right_wall = False
        self.left_wall = False
        
        self.images = self.load_images()
        self.minimap = False
        self.start = False
        self.end = False

    def maze_setup(self):
        # Maze setup
        self.width, self.height = 3, 3  # Maze size (6x6)
        self.cell_size = 60  # Each cell (room) will be 60x60 pixels
        self.base_maze = self.create_maze(self.width, self.height)
        self.mazes = [
            self.base_maze,
            self.rotate_maze(self.base_maze),
            self.rotate_maze(self.rotate_maze(self.base_maze)),
            self.rotate_maze(self.rotate_maze(self.rotate_maze(self.base_maze)))
        ]

        # Define a single start position
        start_x, start_y = random.randint(0, self.width - 1), self.height - 1

        # Transform the start position for each maze orientation
        self.start_positions = [
            (start_x, start_y),  # Original
            (self.height - 1 - start_y, start_x),  # 270 degrees clockwise
            (self.width - 1 - start_x, self.height - 1 - start_y),  # 180 degrees
            (start_y, self.width - 1 - start_x)  # 90 degrees clockwise
        ]

        # Define a single end position
        end_x, end_y = random.choice([0, self.width - 1]), 0

        # Transform the end position for each maze orientation
        self.end_s = [
            (end_x, end_y),  # Original
            (self.height - 1 - end_y, end_x),  # 270 degrees clockwise
            (self.width - 1 - end_x, self.height - 1 - end_y),  # 180 degrees
            (end_y, self.width - 1 - end_x)  # 90 degrees clockwise
        ]

        # Initialize player positions
        self.end_positions = list(self.end_s)
        self.player_positions = list(self.start_positions)

    def rotate_maze(self, maze):
        """Rotate the maze 90 degrees clockwise."""
        width, height = len(maze[0]), len(maze)
        rotated_maze = [[None for _ in range(width)] for _ in range(height)]
        
        for y in range(height):
            for x in range(width):
                room = maze[y][x]
                rotated_maze[x][height - 1 - y] = {
                    'top': room['left'],
                    'bottom': room['right'],
                    'left': room['bottom'],
                    'right': room['top'],
                    'visited': room['visited']
                }
        
        return rotated_maze

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

    def draw_maze(self, maze):
        """Render the maze on the Pygame screen."""
        for y in range(self.height):
            for x in range(self.width):
                room = maze[y][x]
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
                    
        end_x_pos = self.end_positions[self.current_maze_index][0] * self.cell_size
        end_y_pos = self.end_positions[self.current_maze_index][1] * self.cell_size
        # pygame.draw.rect(self.screen, self.colors["GREEN"], (end_x_pos, end_y_pos, self.cell_size, self.cell_size))

    def draw_player(self, player_pos):
        """Draw the player as a red circle."""
        player_x_pos = player_pos[0] * self.cell_size + self.cell_size // 2
        player_y_pos = player_pos[1] * self.cell_size + self.cell_size // 2
        pygame.draw.circle(self.screen, self.colors["RED"], (player_x_pos, player_y_pos), 10)

    def reset_game(self):
        self.total_position = 0
        self.player_total_points = 0
        self.current_maze_index = 0
        self.gamestate = True
        self.top_wall = False
        self.bottom_wall = False
        self.right_wall = False
        self.left_wall = False
        self.start = False
        self.end = False
        self.maze_setup()
    
    def draw_text(self, text, x, y, color):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
    
    def load_images(self):
        all_images = [
            'start', 'left', 'left_right', 'left_straight', 'left_straight_right', 'none', 'right', 'straight', 'straight_right', 'end'
        ]
        images = {}
        for wall in all_images:
            path = os.path.join("doors", f"{wall}.png")
            try:
                image = pygame.image.load(path)
                image = pygame.transform.scale(image, (800, 600))
                print(image)
                if wall == 'start':
                    image = pygame.transform.scale(image, (200, 200))
                if wall == 'end':
                    image = pygame.transform.scale(image, (200, 200))
                images[wall] = image 
                
            except pygame.error as e:
                print(f"Error loading {wall}.png: {e}")
                images[wall] = None  # Placeholder for missing images
        return images
    
    def draw_wall_images(self):
        wall_position = (0, 0)
        
        # Determine the image key based on the wall conditions
        if self.top_wall and self.right_wall and self.left_wall:
            image_key = "none"
        elif self.top_wall and self.left_wall:
            image_key = "left"
        elif self.top_wall and self.right_wall:
            image_key = "right"
        elif self.top_wall:
            image_key = "left_right"
        elif self.left_wall and self.right_wall:
            image_key = "straight"
        elif self.left_wall:
            image_key = "left_straight"
        elif self.right_wall:
            image_key = "straight_right"
        else:
            image_key = "left_straight_right"

        # Check if the image exists in the images dictionary and blit it to the screen
        if image_key in self.images and self.images[image_key]:
            self.screen.blit(self.images[image_key], wall_position)

        # Draw the start image at a different position if self.start is True
        if self.start:
            start_position = (300, 300)  # You can set this to any position you want
            start_key = "start"
            if start_key in self.images and self.images[start_key]:
                self.screen.blit(self.images[start_key], start_position)  

        # Draw the start image at a different position if self.start is True
        if self.end:
            end_position = (300, 300)  # You can set this to any position you want
            end_key = "end"
            if end_key in self.images and self.images[end_key]:
                self.screen.blit(self.images[end_key], end_position)  

    
    def toggle_minimap(self):
        self.minimap = not self.minimap

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
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    self.toggle_minimap()
                elif event.type == pygame.KEYDOWN:
                    self.start = False
                    self.end = False
                    # Move player with arrow keys
                    self.top_wall = False
                    self.bottom_wall = False
                    self.right_wall = False
                    self.left_wall = False
                    if event.key == pygame.K_UP and not self.mazes[self.current_maze_index][self.player_positions[self.current_maze_index][1]][self.player_positions[self.current_maze_index][0]]['top']:
                        self.total_position += 0
                        print('arrow up')
                        print(self.player_positions)
                        if self.current_maze_index == 0:
                            self.player_positions = [
                                (self.player_positions[0][0], self.player_positions[0][1] - 1),
                                (self.player_positions[1][0] + 1, self.player_positions[1][1]),
                                (self.player_positions[2][0], self.player_positions[2][1] + 1),
                                (self.player_positions[3][0] - 1, self.player_positions[3][1])
                                ]
                        if self.current_maze_index == 2:
                            self.player_positions = [
                                (self.player_positions[0][0], self.player_positions[0][1] + 1),
                                (self.player_positions[1][0] - 1, self.player_positions[1][1]),
                                (self.player_positions[2][0], self.player_positions[2][1] - 1),
                                (self.player_positions[3][0] + 1, self.player_positions[3][1])
                                ]
                        # left
                        if self.current_maze_index == 3:
                            self.player_positions = [
                                (self.player_positions[0][0] + 1, self.player_positions[0][1]),
                                (self.player_positions[1][0], self.player_positions[1][1] + 1),
                                (self.player_positions[2][0] - 1, self.player_positions[2][1]),
                                (self.player_positions[3][0], self.player_positions[3][1] - 1)
                                ]
                        # right
                        if self.current_maze_index == 1:
                            self.player_positions = [
                                (self.player_positions[0][0] - 1, self.player_positions[0][1]),
                                (self.player_positions[1][0], self.player_positions[1][1] - 1),
                                (self.player_positions[2][0] + 1, self.player_positions[2][1]),
                                (self.player_positions[3][0], self.player_positions[3][1] + 1)
                                ]
                            
                        print(self.player_positions)
                        
                    elif event.key == pygame.K_DOWN and not self.mazes[self.current_maze_index][self.player_positions[self.current_maze_index][1]][self.player_positions[self.current_maze_index][0]]['bottom']:
                        self.total_position += 2
                        print('arrow down')
                        print(self.player_positions)
                        if self.current_maze_index == 0:
                            self.player_positions = [
                                (self.player_positions[0][0], self.player_positions[0][1] + 1),
                                (self.player_positions[1][0] - 1, self.player_positions[1][1]),
                                (self.player_positions[2][0], self.player_positions[2][1] - 1),
                                (self.player_positions[3][0] + 1, self.player_positions[3][1])
                            ]
                        if self.current_maze_index == 2:
                            self.player_positions = [
                                (self.player_positions[0][0], self.player_positions[0][1] - 1),
                                (self.player_positions[1][0] + 1, self.player_positions[1][1]),
                                (self.player_positions[2][0], self.player_positions[2][1] + 1),
                                (self.player_positions[3][0] - 1, self.player_positions[3][1])
                            ]
                        if self.current_maze_index == 1:
                            self.player_positions = [
                                (self.player_positions[0][0] + 1, self.player_positions[0][1]),
                                (self.player_positions[1][0], self.player_positions[1][1] + 1),
                                (self.player_positions[2][0] - 1, self.player_positions[2][1]),
                                (self.player_positions[3][0], self.player_positions[3][1] - 1)
                                ]
                        if self.current_maze_index == 3:
                            self.player_positions = [
                                (self.player_positions[0][0] - 1, self.player_positions[0][1]),
                                (self.player_positions[1][0], self.player_positions[1][1] - 1),
                                (self.player_positions[2][0] + 1, self.player_positions[2][1]),
                                (self.player_positions[3][0], self.player_positions[3][1] + 1)
                                ]
                            
                        print(self.player_positions)
                        
                        # self.player_positions[self.current_maze_index] = (self.player_positions[self.current_maze_index][0], self.player_positions[self.current_maze_index][1] + 1)
                    elif event.key == pygame.K_LEFT and not self.mazes[self.current_maze_index][self.player_positions[self.current_maze_index][1]][self.player_positions[self.current_maze_index][0]]['left']:
                        self.total_position -= 1
                        print('arrow left')
                        print(self.player_positions)
                        # straight
                        if self.current_maze_index == 0:
                            self.player_positions = [
                                (self.player_positions[0][0] - 1, self.player_positions[0][1]),
                                (self.player_positions[1][0], self.player_positions[1][1] - 1),
                                (self.player_positions[2][0] + 1, self.player_positions[2][1]),
                                (self.player_positions[3][0], self.player_positions[3][1] + 1)
                            ]
                        # backwards
                        if self.current_maze_index == 2:
                            self.player_positions = [
                                (self.player_positions[0][0] + 1, self.player_positions[0][1]),
                                (self.player_positions[1][0], self.player_positions[1][1] + 1),
                                (self.player_positions[2][0] - 1, self.player_positions[2][1]),
                                (self.player_positions[3][0], self.player_positions[3][1] - 1)
                            ]   
                        # left
                        if self.current_maze_index == 3:
                            self.player_positions = [
                                (self.player_positions[0][0], self.player_positions[0][1] - 1),
                                (self.player_positions[1][0] + 1, self.player_positions[1][1]),
                                (self.player_positions[2][0], self.player_positions[2][1] + 1),
                                (self.player_positions[3][0] - 1, self.player_positions[3][1])
                                ]
                        # right
                        if self.current_maze_index == 1:
                            self.player_positions = [
                                (self.player_positions[0][0], self.player_positions[0][1] + 1),
                                (self.player_positions[1][0] - 1, self.player_positions[1][1]),
                                (self.player_positions[2][0], self.player_positions[2][1] - 1),
                                (self.player_positions[3][0] + 1, self.player_positions[3][1])
                                ]
                        print(self.player_positions)
                        
                        # self.player_positions[self.current_maze_index] = (self.player_positions[self.current_maze_index][0] - 1, self.player_positions[self.current_maze_index][1])
                    elif event.key == pygame.K_RIGHT and not self.mazes[self.current_maze_index][self.player_positions[self.current_maze_index][1]][self.player_positions[self.current_maze_index][0]]['right']:
                        self.total_position += 1
                        print('arrow right')
                        print(self.player_positions)
                        # straight
                        if self.current_maze_index == 0:
                            self.player_positions = [
                                (self.player_positions[0][0] + 1, self.player_positions[0][1]),
                                (self.player_positions[1][0], self.player_positions[1][1] + 1),
                                (self.player_positions[2][0] - 1, self.player_positions[2][1]),
                                (self.player_positions[3][0], self.player_positions[3][1] - 1)
                            ]
                        # backwards
                        if self.current_maze_index == 2:
                            self.player_positions = [
                                (self.player_positions[0][0] - 1, self.player_positions[0][1]),
                                (self.player_positions[1][0], self.player_positions[1][1] - 1),
                                (self.player_positions[2][0] + 1, self.player_positions[2][1]),
                                (self.player_positions[3][0], self.player_positions[3][1] + 1)
                            ]
                        # left
                        if self.current_maze_index == 3:
                            self.player_positions = [
                                (self.player_positions[0][0], self.player_positions[0][1] + 1),
                                (self.player_positions[1][0] - 1, self.player_positions[1][1]),
                                (self.player_positions[2][0], self.player_positions[2][1] - 1),
                                (self.player_positions[3][0] + 1, self.player_positions[3][1])
                                ]
                        # right
                        if self.current_maze_index == 1:
                            self.player_positions = [
                                (self.player_positions[0][0], self.player_positions[0][1] - 1),
                                (self.player_positions[1][0] + 1, self.player_positions[1][1]),
                                (self.player_positions[2][0], self.player_positions[2][1] + 1),
                                (self.player_positions[3][0] - 1, self.player_positions[3][1])
                                ]
                        print(self.player_positions)
                        
                        # self.player_positions[self.current_maze_index] = (self.player_positions[self.current_maze_index][0] + 1, self.player_positions[self.current_maze_index][1])
                    # print(f'Current position: {self.player_positions[self.current_maze_index]}')

                    # if self.total_position % 4 == 0 or self.total_position == 0:
                    #     self.current_maze_index = 0
                    # elif self.total_position % 2 == 0:
                    #     self.current_maze_index = 2
                    # elif self.total_position % 4 == 3 or self.total_position == -1:
                    #     self.current_maze_index = 1
                    # elif self.total_position % 4 == 1 or self.total_position == 1:
                    #     self.current_maze_index = 3

                    # print(f"Total position: {self.total_position}")
                    # print(f"Current maze: {self.maze_orientations[self.current_maze_index]}/{self.current_maze_index}\n")

                    # if self.mazes[self.current_maze_index][self.player_positions[self.current_maze_index][1]][self.player_positions[self.current_maze_index][0]]['top']:
                    #     print('top wall')
                    #     self.top_wall = True
                    # if self.mazes[self.current_maze_index][self.player_positions[self.current_maze_index][1]][self.player_positions[self.current_maze_index][0]]['bottom']:
                    #     print('bottom wall')
                    #     self.bottom_wall = True
                    # if self.mazes[self.current_maze_index][self.player_positions[self.current_maze_index][1]][self.player_positions[self.current_maze_index][0]]['right']:
                    #     print('left wall')
                    #     self.left_wall = True
                    # if self.mazes[self.current_maze_index][self.player_positions[self.current_maze_index][1]][self.player_positions[self.current_maze_index][0]]['left']:
                    #     print('right wall')
                    #     self.right_wall = True

            if self.gamestate:
                time_elapsed += self.dt

                print(f'Current position: {self.player_positions[self.current_maze_index]}')

                if self.total_position % 4 == 0 or self.total_position == 0:
                    self.current_maze_index = 0
                elif self.total_position % 2 == 0:
                    self.current_maze_index = 2
                elif self.total_position % 4 == 3 or self.total_position == -1:
                    self.current_maze_index = 1
                elif self.total_position % 4 == 1 or self.total_position == 1:
                    self.current_maze_index = 3

                # print(f"Total position: {self.total_position}")
                print(f"Current maze: {self.maze_orientations[self.current_maze_index]}/{self.current_maze_index}\n")

                if self.mazes[self.current_maze_index][self.player_positions[self.current_maze_index][1]][self.player_positions[self.current_maze_index][0]]['top']:
                    print('top wall')
                    self.top_wall = True
                if self.mazes[self.current_maze_index][self.player_positions[self.current_maze_index][1]][self.player_positions[self.current_maze_index][0]]['bottom']:
                    print('bottom wall')
                    self.bottom_wall = True
                if self.mazes[self.current_maze_index][self.player_positions[self.current_maze_index][1]][self.player_positions[self.current_maze_index][0]]['right']:
                    print('left wall')
                    self.left_wall = True
                if self.mazes[self.current_maze_index][self.player_positions[self.current_maze_index][1]][self.player_positions[self.current_maze_index][0]]['left']:
                    print('right wall')
                    self.right_wall = True


                # Check if the player is at the start
                if self.player_positions[self.current_maze_index] == self.start_positions[self.current_maze_index]:
                    self.start = True

                # Check if the player reached the end
                if self.player_positions[self.current_maze_index] == self.end_positions[self.current_maze_index]:
                    self.end = True
                    # self.gamestate = False  # End the game if player reaches the end room

                self.draw_wall_images()

                if self.minimap == True:
                    self.draw_maze(self.mazes[self.current_maze_index])
                    self.draw_player(self.player_positions[self.current_maze_index])

                # if self.player_positions == self.start_positions

                if self.top_wall == False:
                    self.draw_text('t', self.screen_width - 500, self.screen_height // 10, self.colors["BLACK"])
                if self.bottom_wall == False:
                    self.draw_text('b', self.screen_width - 450, self.screen_height // 10, self.colors["BLACK"])
                if self.right_wall == False:
                    self.draw_text('l', self.screen_width - 400, self.screen_height // 10, self.colors["BLACK"])
                if self.left_wall == False:
                    self.draw_text('r', self.screen_width - 350, self.screen_height // 10, self.colors["BLACK"])
                
            else:
                self.screen.fill(self.colors["GREY"])
                self.draw_text(f"FINAL SCORE: {self.player_total_points}", self.screen_width // 5, self.screen_height // 2, self.colors["BLACK"])

            pygame.display.flip()
            self.dt = clock.tick(60) / 1000
        
        pygame.quit()

if __name__ == "__main__":
    game = GameWindow()
    game.main()