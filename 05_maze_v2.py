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
        self.maze_size = 3
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
        self.skeleton = False
        self.painting = False
        self.note = False
        self.grimreaper = False
        self.spider = False
        
    def maze_setup(self):
        # Maze setup
        self.width, self.height = self.maze_size, self.maze_size  # Maze size (6x6)
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
        
        # Define a single start position
        skeleton_x, skeleton_y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
        
        # Transform the start position for each maze orientation
        self.skeleton_s = [
            (skeleton_x, skeleton_y),  # Original
            (self.height - 1 - skeleton_y, skeleton_x),  # 270 degrees clockwise
            (self.width - 1 - skeleton_x, self.height - 1 - skeleton_y),  # 180 degrees
            (skeleton_y, self.width - 1 - skeleton_x)  # 90 degrees clockwise
        ]

        painting_x, painting_y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)

        # Transform the start position for each maze orientation
        self.painting_s = [
            (painting_x, painting_y),  # Original
            (self.height - 1 - painting_y, painting_x),  # 270 degrees clockwise
            (self.width - 1 - painting_x, self.height - 1 - painting_y),  # 180 degrees
            (painting_y, self.width - 1 - painting_x)  # 90 degrees clockwise
        ]

        note_x, note_y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
        self.maze_for_note = random.randint(0,3)
        self.note_position_x = random.randint(200, 540)
        self.note_position_y = random.randint(450, 520)
        self.note_rotation = random.randint(0,360)
        
        # Transform the start position for each maze orientation
        self.note_s = [
            (note_x, note_y),  # Original
            (self.height - 1 - note_y, note_x),  # 270 degrees clockwise
            (self.width - 1 - note_x, self.height - 1 - note_y),  # 180 degrees
            (note_y, self.width - 1 - note_x)  # 90 degrees clockwise
        ]

        grimreaper_x, grimreaper_y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
        
        # Transform the start position for each maze orientation
        self.grimreaper_s = [
            (grimreaper_x, grimreaper_y),  # Original
            (self.height - 1 - grimreaper_y, grimreaper_x),  # 270 degrees clockwise
            (self.width - 1 - grimreaper_x, self.height - 1 - grimreaper_y),  # 180 degrees
            (grimreaper_y, self.width - 1 - grimreaper_x)  # 90 degrees clockwise
        ]

        spider_x, spider_y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
        
        # Transform the start position for each maze orientation
        self.spider_s = [
            (spider_x, spider_y),  # Original
            (self.height - 1 - spider_y, spider_x),  # 270 degrees clockwise
            (self.width - 1 - spider_x, self.height - 1 - spider_y),  # 180 degrees
            (spider_y, self.width - 1 - spider_x)  # 90 degrees clockwise
        ]

        # Initialize player positions
        self.end_positions = list(self.end_s)
        self.skeleton_positions = list(self.skeleton_s)
        self.painting_positions = list(self.painting_s)
        self.note_positions = list(self.note_s)
        self.grimreaper_positions = list(self.grimreaper_s)
        self.spider_positions = list(self.spider_s)
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

    def next_game(self):
        self.load_images()
        if self.player_total_points != 0:
            self.fade_out()
            self.maze_setup()
        self.total_position = 0
        self.current_maze_index = 0
        self.maze_size += 1
        self.gamestate = True
        self.top_wall = False
        self.bottom_wall = False
        self.right_wall = False
        self.left_wall = False
        self.start = False
        self.end = False
        self.skeleton = False
        self.painting = False
        self.note = False
        self.grimreaper = False
        self.spider = False

    def fade_out(self, speed=5):
        fade_surface = pygame.Surface(self.screen.get_size())
        fade_surface.fill((0, 0, 0))  # Black overlay
        if self.grimreaper == True:
            fade_surface.fill((80, 0, 0))

        for alpha in range(0, 256, speed):
            self.draw_wall_images()  # Re-render the scene behind the fade
            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.update()
            pygame.time.delay(10)

    def reset_game(self):
        self.player_total_points = 0
        self.maze_size = 2
        self.next_game()
        self.maze_setup()
    
    def draw_text(self, text, x, y, color):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
    
    def tint_surface(self, surface, tint_color):
        """ Apply a red tint to a surface """
        tinted = surface.copy()
        tint = pygame.Surface(surface.get_size()).convert_alpha()
        tint.fill(tint_color)
        tinted.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        return tinted
    
    def load_images(self):
        all_images = [
            'new_start', 'new_left', 'new_left_right', 'new_left_straight', 'new_left_straight_right', 
            'new_none_dark', 'new_right', 'new_straight_close', 'new_straight_long', 'new_straight_long_2', 
            'new_straight_right', 'new_end', 'ladder', 'skeleton_front', 'skeleton_back', 'skeleton_side_1',
            'skeleton_side_2', 'painting1', 'painting1_side1', 'painting1_side2', 'note', 'grimreaper', 'spider',
            'spider2', 'spider3'
        ]
        images = {}
        for wall in all_images:
            path = os.path.join("images", "doors", f"{wall}.png")
            try:
                image = pygame.image.load(path)
                image = pygame.transform.scale(image, (800, 600))
                if wall == 'new_start':
                    image = pygame.transform.scale(image, (150, 80))
                if wall == 'new_end':
                    image = pygame.transform.scale(image, (150, 80))
                if wall == 'ladder':
                    image = pygame.transform.scale(image, (300, 80))
                if wall == 'skeleton_front':
                    image = pygame.transform.scale(image, (500, 1000))
                if wall == 'skeleton_back':
                    image = pygame.transform.scale(image, (110, 300))
                if wall == 'skeleton_side_1':
                    image = pygame.transform.scale(image, (140, 390))
                if wall == 'skeleton_side_2':
                    image = pygame.transform.scale(image, (110, 300))
                if wall == 'painting1':
                    image = pygame.transform.scale(image, (200, 150))
                if wall == 'painting1_side1':
                    image = pygame.transform.scale(image, (400, 225))
                if wall == 'painting1_side2':
                    image = pygame.transform.scale(image, (400, 225))
                if wall == 'note':
                    image = pygame.transform.scale(image, (60, 60))
                if wall == 'grimreaper':
                    image = pygame.transform.scale(image, (250, 500))
                if wall == 'spider':
                    image = pygame.transform.scale(image, (100, 110))
                if wall == 'spider2':
                    image = pygame.transform.scale(image, (300, 330))
                if wall == 'spider3':
                    image = pygame.transform.scale(image, (100, 110))
                images[wall] = image 
                
            except pygame.error as e:
                print(f"Error loading {wall}.png: {e}")
                images[wall] = None  # Placeholder for missing images
        return images
    
    def draw_wall_images(self):
        wall_position = (0, 0)
        # Determine the image key based on the wall conditions
        if self.top_wall and self.right_wall and self.left_wall:
            image_key = "new_none_dark"
        elif self.top_wall and self.left_wall:
            image_key = "new_left"
        elif self.top_wall and self.right_wall:
            image_key = "new_right"
        elif self.top_wall:
            image_key = "new_left_right"
        elif self.left_wall and self.right_wall:
            if self.player_positions[self.current_maze_index] == self.start_positions[self.current_maze_index]:
                image_key = "new_straight_close"
            elif self.current_maze_index in [0, 1]:
                image_key = "new_straight_long"
            else:
                image_key = "new_straight_long_2"
        elif self.left_wall:
            image_key = "new_left_straight"
        elif self.right_wall:
            image_key = "new_straight_right"
        else:
            image_key = "new_left_straight_right"

        # Check if the image exists in the images dictionary and blit it to the screen
        if image_key in self.images and self.images[image_key]:
            image = self.images[image_key]
            # if self.player_total_points == 5:
            #     image = self.tint_surface(self.images[image_key], (80, 0, 0, 50))  # Reddish overlay
            self.screen.blit(image, wall_position)

        if self.start:
            start_key = "new_start"
            start_position = (320, 480)  # Default position

            if start_key in self.images and self.images[start_key]:
                start_image = self.images[start_key]

                # Rotate the image based on maze index
                if self.current_maze_index == 2:
                    start_image = pygame.transform.rotate(start_image, 180)
                if self.current_maze_index == 1:
                    start_image = pygame.transform.scale(start_image, (100, 80))
                    start_image = pygame.transform.rotate(start_image, 270)
                    start_position = (350, 480)  # Default position
                if self.current_maze_index == 3:
                    start_image = pygame.transform.scale(start_image, (100, 80))
                    start_image = pygame.transform.rotate(start_image, 90)
                    start_position = (350, 480)  # Default position
                self.screen.blit(start_image, start_position)

        if self.end:
            end_position = (320, 480)  # You can set this to any position you want
            end_key = "new_end"
            if end_key in self.images and self.images[end_key]:
                self.screen.blit(self.images[end_key], end_position)  

        if self.painting:
            painting_key = 'painting1'
            painting_position = (800, 800)
            if painting_key in self.images and self.images[painting_key]:
                if self.current_maze_index == 0 and self.top_wall:
                    painting_key = "painting1"
                    painting_position = (300, 200)
                if self.current_maze_index == 2:
                    painting_position = (800, 800)  # You can set this to any position you want
                    painting_key = "painting1"
                if self.current_maze_index == 1 and self.left_wall:
                    painting_position = (500, 200)  # You can set this to any position you want
                    painting_key = "painting1_side2"
                if self.current_maze_index == 3 and self.right_wall:
                    painting_position = (-100, 200)  # You can set this to any position you want
                    painting_key = "painting1_side1"
                self.screen.blit(self.images[painting_key], painting_position) 
                
        if self.note:
            note_key = "note"
            note_position = (self.note_position_x, self.note_position_y)
            if note_key in self.images and self.images[note_key]:
                note = self.images[note_key]
                note = pygame.transform.rotate(note, self.note_rotation)
                self.screen.blit(note, note_position) 
                
        if self.skeleton:
            skeleton_key = "skeleton_front"
            skeleton_position = (240, 170)
            if skeleton_key in self.images and self.images[skeleton_key]:
                if self.current_maze_index == 2 or (self.current_maze_index == 1 and self.left_wall and self.right_wall):
                    skeleton_position = (300, 170)  # You can set this to any position you want
                    skeleton_key = "skeleton_back"
                if self.current_maze_index == 1 and not (self.left_wall and self.right_wall):
                    skeleton_position = (170, 170)  # You can set this to any position you want
                    skeleton_key = "skeleton_side_1"
                if self.current_maze_index == 3 and not (self.left_wall and self.right_wall):
                    skeleton_position = (500, 190)  # You can set this to any position you want
                    skeleton_key = "skeleton_side_2"
                self.screen.blit(self.images[skeleton_key], skeleton_position)                  
        
        if self.grimreaper:
            grimreaper_key = "grimreaper"
            grimreaper_position = (280, 130)
            if grimreaper_key in self.images and self.images[grimreaper_key]:
                self.screen.blit(self.images[grimreaper_key], grimreaper_position)
    
        if self.spider:
            spider_key = "spider"
            spider_position = (230, 100)
            if spider_key in self.images and self.images[spider_key]:
                if self.current_maze_index == 2:
                    spider_position = (self.screen_width, self.screen_height)  # You can set this to any position you want
                    spider_key = "spider"
                if self.current_maze_index == 1 and not (self.left_wall and self.right_wall):
                    spider_position = (550, 110)  # You can set this to any position you want
                    spider_key = "spider3"
                if self.current_maze_index == 3 and not (self.left_wall and self.right_wall):
                    spider_position = (-150, -150)  # You can set this to any position you want
                    spider_key = "spider2"
                self.screen.blit(self.images[spider_key], spider_position)
    
    def toggle_minimap(self):
        self.minimap = not self.minimap

    # Add this method to handle mouse click actions
    def handle_click(self, mouse_pos):      
        # Define areas for left, straight, and right doors based on the screen position
        left_area = (0, self.screen_width // 3)  # Left door
        straight_area = (self.screen_width // 3, 2 * self.screen_width // 3, 0, 500)
        right_area = (2 * self.screen_width // 3, self.screen_width)  # Right door
        backwards_area = (self.screen_height - 100, self.screen_height)
        next_area = (self.screen_height - 150, self.screen_height)

        if next_area[0] <= mouse_pos[1] < next_area[1] \
        and self.player_positions[self.current_maze_index] == self.end_positions[self.current_maze_index]:
            self.player_total_points += 1
            self.next_game()

        self.start = False
        self.end = False
        self.skeleton = False
        self.painting = False
        self.note = False
        # Move player with arrow keys
        self.top_wall = False
        self.bottom_wall = False
        self.right_wall = False
        self.left_wall = False

        if straight_area[0] <= mouse_pos[0] < straight_area[1] \
        and straight_area[2] <= mouse_pos[1] < straight_area[3] \
        and not self.mazes[self.current_maze_index][self.player_positions[self.current_maze_index][1]][self.player_positions[self.current_maze_index][0]]['top']:
            self.total_position += 0  
            # Move straight
            if self.current_maze_index == 0:
                self.player_positions = [
                    (self.player_positions[0][0], self.player_positions[0][1] - 1),(self.player_positions[1][0] + 1, self.player_positions[1][1]),
                    (self.player_positions[2][0], self.player_positions[2][1] + 1),(self.player_positions[3][0] - 1, self.player_positions[3][1])]
            # backwards
            if self.current_maze_index == 2:
                self.player_positions = [
                    (self.player_positions[0][0], self.player_positions[0][1] + 1),(self.player_positions[1][0] - 1, self.player_positions[1][1]),
                    (self.player_positions[2][0], self.player_positions[2][1] - 1),(self.player_positions[3][0] + 1, self.player_positions[3][1])]
            # left
            if self.current_maze_index == 3:
                self.player_positions = [
                    (self.player_positions[0][0] + 1, self.player_positions[0][1]),(self.player_positions[1][0], self.player_positions[1][1] + 1),
                    (self.player_positions[2][0] - 1, self.player_positions[2][1]),(self.player_positions[3][0], self.player_positions[3][1] - 1)]
            # right
            if self.current_maze_index == 1:
                self.player_positions = [
                    (self.player_positions[0][0] - 1, self.player_positions[0][1]), (self.player_positions[1][0], self.player_positions[1][1] - 1), 
                    (self.player_positions[2][0] + 1, self.player_positions[2][1]), (self.player_positions[3][0], self.player_positions[3][1] + 1)]

        elif backwards_area[0] <= mouse_pos[1] < backwards_area[1] and not self.mazes[self.current_maze_index][self.player_positions[self.current_maze_index][1]][self.player_positions[self.current_maze_index][0]]['bottom']:
            self.total_position += 2  # Move backwards
            if self.current_maze_index == 0:
                self.player_positions = [
                    (self.player_positions[0][0], self.player_positions[0][1] + 1),(self.player_positions[1][0] - 1, self.player_positions[1][1]),
                    (self.player_positions[2][0], self.player_positions[2][1] - 1),(self.player_positions[3][0] + 1, self.player_positions[3][1])
                ]
            if self.current_maze_index == 2:
                self.player_positions = [
                    (self.player_positions[0][0], self.player_positions[0][1] - 1),(self.player_positions[1][0] + 1, self.player_positions[1][1]),
                    (self.player_positions[2][0], self.player_positions[2][1] + 1),(self.player_positions[3][0] - 1, self.player_positions[3][1])
                ]
            if self.current_maze_index == 1:
                self.player_positions = [
                    (self.player_positions[0][0] + 1, self.player_positions[0][1]),(self.player_positions[1][0], self.player_positions[1][1] + 1),
                    (self.player_positions[2][0] - 1, self.player_positions[2][1]),(self.player_positions[3][0], self.player_positions[3][1] - 1)
                    ]
            if self.current_maze_index == 3:
                self.player_positions = [
                    (self.player_positions[0][0] - 1, self.player_positions[0][1]),(self.player_positions[1][0], self.player_positions[1][1] - 1),
                    (self.player_positions[2][0] + 1, self.player_positions[2][1]),(self.player_positions[3][0], self.player_positions[3][1] + 1)
                    ]

        elif left_area[0] <= mouse_pos[0] < left_area[1] and not self.mazes[self.current_maze_index][self.player_positions[self.current_maze_index][1]][self.player_positions[self.current_maze_index][0]]['left']:
            self.total_position -= 1  # Move right
            # straight
            if self.current_maze_index == 0:
                self.player_positions = [
                    (self.player_positions[0][0] - 1, self.player_positions[0][1]),(self.player_positions[1][0], self.player_positions[1][1] - 1),
                    (self.player_positions[2][0] + 1, self.player_positions[2][1]),(self.player_positions[3][0], self.player_positions[3][1] + 1)
                ]
            # backwards
            if self.current_maze_index == 2:
                self.player_positions = [
                    (self.player_positions[0][0] + 1, self.player_positions[0][1]),(self.player_positions[1][0], self.player_positions[1][1] + 1),
                    (self.player_positions[2][0] - 1, self.player_positions[2][1]),(self.player_positions[3][0], self.player_positions[3][1] - 1)
                ]   
            # left
            if self.current_maze_index == 3:
                self.player_positions = [
                    (self.player_positions[0][0], self.player_positions[0][1] - 1),(self.player_positions[1][0] + 1, self.player_positions[1][1]),
                    (self.player_positions[2][0], self.player_positions[2][1] + 1),(self.player_positions[3][0] - 1, self.player_positions[3][1])
                    ]
            # right
            if self.current_maze_index == 1:
                self.player_positions = [
                    (self.player_positions[0][0], self.player_positions[0][1] + 1),(self.player_positions[1][0] - 1, self.player_positions[1][1]),
                    (self.player_positions[2][0], self.player_positions[2][1] - 1),(self.player_positions[3][0] + 1, self.player_positions[3][1])
                    ]
            
        elif right_area[0] <= mouse_pos[0] < right_area[1] and not self.mazes[self.current_maze_index][self.player_positions[self.current_maze_index][1]][self.player_positions[self.current_maze_index][0]]['right']:
            self.total_position += 1  # Move left
            # straight
            if self.current_maze_index == 0:
                self.player_positions = [
                    (self.player_positions[0][0] + 1, self.player_positions[0][1]),(self.player_positions[1][0], self.player_positions[1][1] + 1),
                    (self.player_positions[2][0] - 1, self.player_positions[2][1]),(self.player_positions[3][0], self.player_positions[3][1] - 1)
                ]
            # backwards
            if self.current_maze_index == 2:
                self.player_positions = [
                    (self.player_positions[0][0] - 1, self.player_positions[0][1]),(self.player_positions[1][0], self.player_positions[1][1] - 1),
                    (self.player_positions[2][0] + 1, self.player_positions[2][1]),(self.player_positions[3][0], self.player_positions[3][1] + 1)
                ]
            # left
            if self.current_maze_index == 3:
                self.player_positions = [
                    (self.player_positions[0][0], self.player_positions[0][1] + 1),(self.player_positions[1][0] - 1, self.player_positions[1][1]),
                    (self.player_positions[2][0], self.player_positions[2][1] - 1),(self.player_positions[3][0] + 1, self.player_positions[3][1])
                    ]
            # right
            if self.current_maze_index == 1:
                self.player_positions = [
                    (self.player_positions[0][0], self.player_positions[0][1] - 1),(self.player_positions[1][0] + 1, self.player_positions[1][1]),
                    (self.player_positions[2][0], self.player_positions[2][1] + 1),(self.player_positions[3][0] - 1, self.player_positions[3][1])
                    ]

    def handle_key_movement(self, event_key):
        self.start = False
        self.end = False
        self.skeleton = False
        self.painting = False
        self.note = False
        self.grimreaper = False
        self.spider = False
        # Move player with arrow keys
        self.top_wall = False
        self.bottom_wall = False
        self.right_wall = False
        self.left_wall = False
        if event_key == pygame.K_UP and not self.mazes[self.current_maze_index][self.player_positions[self.current_maze_index][1]][self.player_positions[self.current_maze_index][0]]['top']:
            self.total_position += 0
            if self.current_maze_index == 0:
                self.player_positions = [
                    (self.player_positions[0][0], self.player_positions[0][1] - 1),(self.player_positions[1][0] + 1, self.player_positions[1][1]),
                    (self.player_positions[2][0], self.player_positions[2][1] + 1),(self.player_positions[3][0] - 1, self.player_positions[3][1])
                    ]
            if self.current_maze_index == 2:
                self.player_positions = [
                    (self.player_positions[0][0], self.player_positions[0][1] + 1),(self.player_positions[1][0] - 1, self.player_positions[1][1]),
                    (self.player_positions[2][0], self.player_positions[2][1] - 1),(self.player_positions[3][0] + 1, self.player_positions[3][1])
                    ]
            # left
            if self.current_maze_index == 3:
                self.player_positions = [
                    (self.player_positions[0][0] + 1, self.player_positions[0][1]),(self.player_positions[1][0], self.player_positions[1][1] + 1),
                    (self.player_positions[2][0] - 1, self.player_positions[2][1]),(self.player_positions[3][0], self.player_positions[3][1] - 1)
                    ]
            # right
            if self.current_maze_index == 1:
                self.player_positions = [
                    (self.player_positions[0][0] - 1, self.player_positions[0][1]),(self.player_positions[1][0], self.player_positions[1][1] - 1),
                    (self.player_positions[2][0] + 1, self.player_positions[2][1]),(self.player_positions[3][0], self.player_positions[3][1] + 1)
                    ]
                                        
        elif event_key == pygame.K_DOWN and not self.mazes[self.current_maze_index][self.player_positions[self.current_maze_index][1]][self.player_positions[self.current_maze_index][0]]['bottom']:
            self.total_position += 2
            if self.current_maze_index == 0:
                self.player_positions = [
                    (self.player_positions[0][0], self.player_positions[0][1] + 1),(self.player_positions[1][0] - 1, self.player_positions[1][1]),
                    (self.player_positions[2][0], self.player_positions[2][1] - 1),(self.player_positions[3][0] + 1, self.player_positions[3][1])
                ]
            if self.current_maze_index == 2:
                self.player_positions = [
                    (self.player_positions[0][0], self.player_positions[0][1] - 1),(self.player_positions[1][0] + 1, self.player_positions[1][1]),
                    (self.player_positions[2][0], self.player_positions[2][1] + 1),(self.player_positions[3][0] - 1, self.player_positions[3][1])
                ]
            if self.current_maze_index == 1:
                self.player_positions = [
                    (self.player_positions[0][0] + 1, self.player_positions[0][1]),(self.player_positions[1][0], self.player_positions[1][1] + 1),
                    (self.player_positions[2][0] - 1, self.player_positions[2][1]),(self.player_positions[3][0], self.player_positions[3][1] - 1)
                    ]
            if self.current_maze_index == 3:
                self.player_positions = [
                    (self.player_positions[0][0] - 1, self.player_positions[0][1]),(self.player_positions[1][0], self.player_positions[1][1] - 1),
                    (self.player_positions[2][0] + 1, self.player_positions[2][1]),(self.player_positions[3][0], self.player_positions[3][1] + 1)
                    ]
                                        
        elif event_key == pygame.K_LEFT and not self.mazes[self.current_maze_index][self.player_positions[self.current_maze_index][1]][self.player_positions[self.current_maze_index][0]]['left']:
            self.total_position -= 1
            # straight
            if self.current_maze_index == 0:
                self.player_positions = [
                    (self.player_positions[0][0] - 1, self.player_positions[0][1]),(self.player_positions[1][0], self.player_positions[1][1] - 1),
                    (self.player_positions[2][0] + 1, self.player_positions[2][1]),(self.player_positions[3][0], self.player_positions[3][1] + 1)
                ]
            # backwards
            if self.current_maze_index == 2:
                self.player_positions = [
                    (self.player_positions[0][0] + 1, self.player_positions[0][1]),(self.player_positions[1][0], self.player_positions[1][1] + 1),
                    (self.player_positions[2][0] - 1, self.player_positions[2][1]),(self.player_positions[3][0], self.player_positions[3][1] - 1)
                ]   
            # left
            if self.current_maze_index == 3:
                self.player_positions = [
                    (self.player_positions[0][0], self.player_positions[0][1] - 1),(self.player_positions[1][0] + 1, self.player_positions[1][1]),
                    (self.player_positions[2][0], self.player_positions[2][1] + 1),(self.player_positions[3][0] - 1, self.player_positions[3][1])
                    ]
            # right
            if self.current_maze_index == 1:
                self.player_positions = [
                    (self.player_positions[0][0], self.player_positions[0][1] + 1),(self.player_positions[1][0] - 1, self.player_positions[1][1]),
                    (self.player_positions[2][0], self.player_positions[2][1] - 1),(self.player_positions[3][0] + 1, self.player_positions[3][1])
                    ]
            
        elif event_key == pygame.K_RIGHT and not self.mazes[self.current_maze_index][self.player_positions[self.current_maze_index][1]][self.player_positions[self.current_maze_index][0]]['right']:
            self.total_position += 1
            # straight
            if self.current_maze_index == 0:
                self.player_positions = [
                    (self.player_positions[0][0] + 1, self.player_positions[0][1]),(self.player_positions[1][0], self.player_positions[1][1] + 1),
                    (self.player_positions[2][0] - 1, self.player_positions[2][1]),(self.player_positions[3][0], self.player_positions[3][1] - 1)
                ]
            # backwards
            if self.current_maze_index == 2:
                self.player_positions = [
                    (self.player_positions[0][0] - 1, self.player_positions[0][1]),(self.player_positions[1][0], self.player_positions[1][1] - 1),
                    (self.player_positions[2][0] + 1, self.player_positions[2][1]),(self.player_positions[3][0], self.player_positions[3][1] + 1)
                ]
            # left
            if self.current_maze_index == 3:
                self.player_positions = [
                    (self.player_positions[0][0], self.player_positions[0][1] + 1),(self.player_positions[1][0] - 1, self.player_positions[1][1]),
                    (self.player_positions[2][0], self.player_positions[2][1] - 1),(self.player_positions[3][0] + 1, self.player_positions[3][1])
                    ]
            # right
            if self.current_maze_index == 1:
                self.player_positions = [
                    (self.player_positions[0][0], self.player_positions[0][1] - 1),(self.player_positions[1][0] + 1, self.player_positions[1][1]),
                    (self.player_positions[2][0], self.player_positions[2][1] + 1),(self.player_positions[3][0] - 1, self.player_positions[3][1])
                    ]

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
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.player_positions[self.current_maze_index] == self.end_positions[self.current_maze_index]:
                    self.player_total_points += 1
                    self.next_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_pos = event.pos
                        self.handle_click(mouse_pos)
                elif event.type == pygame.KEYDOWN:
                    event_key = event.key
                    self.handle_key_movement(event_key)

            if self.gamestate:
                time_elapsed += self.dt

                if self.total_position % 4 == 0 or self.total_position == 0:
                    self.current_maze_index = 0
                elif self.total_position % 2 == 0:
                    self.current_maze_index = 2
                elif self.total_position % 4 == 3 or self.total_position == -1:
                    self.current_maze_index = 1
                elif self.total_position % 4 == 1 or self.total_position == 1:
                    self.current_maze_index = 3

                if self.mazes[self.current_maze_index][self.player_positions[self.current_maze_index][1]][self.player_positions[self.current_maze_index][0]]['top']:
                    self.top_wall = True
                if self.mazes[self.current_maze_index][self.player_positions[self.current_maze_index][1]][self.player_positions[self.current_maze_index][0]]['bottom']:
                    self.bottom_wall = True
                if self.mazes[self.current_maze_index][self.player_positions[self.current_maze_index][1]][self.player_positions[self.current_maze_index][0]]['right']:
                    self.left_wall = True
                if self.mazes[self.current_maze_index][self.player_positions[self.current_maze_index][1]][self.player_positions[self.current_maze_index][0]]['left']:
                    self.right_wall = True

                # Check if the player is at the start
                if self.player_positions[self.current_maze_index] == self.start_positions[self.current_maze_index]:
                    self.start = True

                # Check if the player reached the end
                if self.player_positions[self.current_maze_index] == self.end_positions[self.current_maze_index]:
                    self.end = True
                    # self.gamestate = False  # End the game if player reaches the end room

                if self.player_positions[self.current_maze_index] == self.skeleton_positions[self.current_maze_index] \
                and not self.start and not self.end:
                    self.skeleton = True

                if self.player_positions[self.current_maze_index] == self.painting_positions[self.current_maze_index] \
                and not self.start and not self.end and not (self.left_wall and self.right_wall):
                    self.painting = True

                if self.player_positions[self.current_maze_index] == self.note_positions[self.current_maze_index] \
                and self.current_maze_index == self.maze_for_note and not self.start and not self.end:
                    self.note = True

                if self.player_positions[self.current_maze_index] == self.grimreaper_positions[self.current_maze_index]\
                and not self.start and not self.end and not self.skeleton and not self.note and not self.painting \
                and self.top_wall and self.right_wall and self.left_wall and self.player_total_points > 0:
                    self.grimreaper = True
                    self.fade_out()
                    self.gamestate = False

                if self.player_positions[self.current_maze_index] == self.spider_positions[self.current_maze_index]:
                    self.spider = True

                self.draw_wall_images()

                if self.end and self.player_total_points == 0:
                    self.draw_text('press SPACE to continue...', self.screen_width - 650, self.screen_height - 50, self.colors["GREY2"])

                if self.minimap == True:
                    self.draw_maze(self.mazes[self.current_maze_index])
                    self.draw_player(self.player_positions[self.current_maze_index])
                
                self.player_points = f'{int(self.player_total_points)}'
                self.draw_text(self.player_points, self.screen_width - 200, self.screen_height // 10, self.colors["BLACK"])
                
            else:
                self.screen.fill(self.colors["GREY"])
                self.draw_text(f"FINAL SCORE: {self.player_total_points}", self.screen_width // 5, self.screen_height // 2, self.colors["BLACK"])

            pygame.display.flip()
            self.dt = clock.tick(60) / 1000
        
        pygame.quit()

if __name__ == "__main__":
    game = GameWindow()
    game.main()