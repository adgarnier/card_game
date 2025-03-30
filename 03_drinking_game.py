import pygame
import random
import os

class GameWindow():
    def __init__(self):
        # pygame setup
        pygame.init()

        # Set up the game window dimensions
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Set the title of the window
        pygame.display.set_caption("Drinking Game")

        # Define colors
        self.WHITE = (255, 255, 255)
        self.GREY = (178, 190, 181)
        self.BLACK = (0, 0, 0)
        self.RED = (210, 43, 43)
        self.GREEN = (49, 146, 54)
        self.BLUE = (76, 81, 247)
        self.PURPLE = (157, 77, 187)
        self.GOLD = (243, 175, 25)
        self.GREY2 = (100, 100, 100)
        self.BROWN = (137, 81, 41)

        # Initialize font
        self.font = pygame.font.SysFont(None, 55)
        self.dt = 0

        self.beer_images = self.load_beer_images('beers')
        self.selected_beer_images = []
        
        # Initialize selected hat
        self.selected_hat = None  # This will store the hat selected for the game
        self.speed_max = 1400
        self.mouse_held_down = False  # Track if the mouse button is held down

        self.reset_game()

    def reset_game(self):
        # Resets the game state
        self.player_total_points = 0
        self.gamestate = True

        # Reset selected beer images
        self.selected_beer_images = self.select_unique_random_beer_images()

        # Pick a hat once per game
        hat_images = [f for f in os.listdir("fishhats") if f.endswith(".png")]
        if hat_images:
            random_hat = random.choice(hat_images)
            self.selected_hat = pygame.image.load(os.path.join("fishhats", random_hat))
            self.selected_hat = pygame.transform.scale(self.selected_hat, (150, 150))  # Resize if needed

        # Pattern game specific
        self.sequence = []
        self.user_sequence = []
        self.generate_sequence()

    def load_beer_images(self, folder):
        beer_images = {}
        image_list = [
            'alexanderkeiths', 'becks', 'budweiser', 'budlight', 'busch', 'carlsberg', 'chambly', 'coorslight', 
            'corona', 'heineken', 'hoegaarden', 'hofbrau', 'iceberg', 'labattblue', 'michelobultra', 'millerlite', 
            'modelo', 'molsoncanadian', 'moosehead', 'sapporo', 'stellaartois', 'tsingtao'
            ]
        for image in image_list:
            image_path = os.path.join(folder, f'{image}.png')
            if os.path.exists(image_path):
                beer_images[image] = pygame.image.load(image_path)
            else:
                print(f'Warning: Image not found for {image}')  # Fix: More descriptive warning
        return beer_images  # Fix: Move return outside the loop

    def select_unique_random_beer_images(self):
        image_keys = list(self.beer_images.keys())
        return random.sample(image_keys, 7)

    def generate_sequence(self):
        self.sequence.append(random.randint(0, 6))
        self.show_sequence()

    def background(self):
        self.screen.fill(self.GREY)
        # Man's body
        pygame.draw.circle(self.screen, self.RED, (self.screen_width // 2, self.screen_height // 4), 80)
        pygame.draw.circle(self.screen, self.PURPLE, (self.screen_width // 2, self.screen_height), 400)
        # Load a random hat from the "fishhats" folder
        # Draw the hat only if one was selected
        if self.selected_hat:
            hat_rect = self.selected_hat.get_rect(midtop=(self.screen_width // 2, 20))
            self.screen.blit(self.selected_hat, hat_rect)
        # Table
        pygame.draw.rect(self.screen, self.BROWN, [0, self.screen_height // 1.25, self.screen_width, 300])
        # Display points
        player_points_text = f'{int(self.player_total_points)}'
        self.draw_text(player_points_text, self.screen_width - 200, self.screen_height // 10, self.BLACK)

    def show_sequence(self):
        self.background()
        pygame.display.flip()

        for idx, i in enumerate(self.sequence):
            beer_image_key = self.selected_beer_images[i]
            beer_image = self.beer_images.get(beer_image_key, None)
            if beer_image:
                # Calculate the new dimensions
                new_height = 300
                aspect_ratio = beer_image.get_width() / beer_image.get_height()
                new_width = int(new_height * aspect_ratio)
                # Rotate images for left/right drinking
                beer_image = pygame.transform.scale(beer_image, (new_width, new_height))
                beer_image_drink_left = pygame.transform.rotate(beer_image, 245)
                beer_image_drink_right = pygame.transform.rotate(beer_image, 115)
                # Define positions for left and right drinking
                image_rect_mouth_left = beer_image_drink_right.get_rect(center=(250, 100))  # Adjust as needed
                image_rect_mouth_right = beer_image_drink_right.get_rect(center=(550, 100))  # Adjust as needed
                # Define random table position
                random_x = random.randint(100, self.screen_width - 100)
                random_y = random.randint(self.screen_height - 200, self.screen_height - 150)
                image_rect_table = beer_image.get_rect(center=(random_x, random_y))
                # Randomly choose left or right drinking
                left_or_right = [
                    (beer_image_drink_left, image_rect_mouth_left),
                    (beer_image_drink_right, image_rect_mouth_right)
                ]
                drink_image, drink_rect = random.choice(left_or_right)
                # Display chosen drinking image
                self.background()
                self.screen.blit(drink_image, drink_rect)
                pygame.display.flip()
                # Drink for ~1 second
                drink_time = random.randint(500, self.speed_max)
                pygame.time.delay(drink_time) 
                self.background()
                self.screen.blit(beer_image, image_rect_table)
                pygame.display.flip()
                # Go away for ~0.4 seconds
                wait_time = random.randint(100, 500)
                pygame.time.delay(wait_time)

    def draw_text(self, text, x, y, color):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_button(self, text, x, y, width, height, color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        rect = pygame.Rect(x, y, width, height)

        pygame.draw.rect(self.screen, color, rect)
        self.draw_text(text, x + 10, y + 10, self.BLACK)

        if rect.collidepoint(mouse):
            if click[0] == 1 and not self.mouse_held_down:
                self.mouse_held_down = True
                if action:
                    action()
            elif click[0] == 0:
                self.mouse_held_down = False

    def button_clicked(self, button_index):
        self.user_sequence.append(button_index)
        self.player_total_points += 1
        if self.user_sequence == self.sequence[:len(self.user_sequence)]:
            if len(self.user_sequence) == len(self.sequence):
                if self.speed_max > 425:
                    self.speed_max = round(self.speed_max * 0.95)
                self.user_sequence = []
                self.generate_sequence()
        else:
            print("Incorrect sequence!")
            self.player_total_points -= 1
            self.gamestate = False

    # Main game loop
    def main(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            # Poll for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        print('Restarting...')
                        self.reset_game()                        

            # Fill the screen with a color to wipe away anything from last frame
            self.background()

            if self.gamestate == True:
                # logic
                # Set beers
                self.beer_click_width = self.screen_width // 10
                self.beer_click_height = self.screen_height // 3 + 100
                self.first_beer_position_x = self.screen_width // 10 - 20
                self.beer_position_y = self.screen_height // 2 - 20

                # Define the colors for the buttons
                colors = [self.GREY2, self.RED, self.BLUE, self.GOLD, self.BLACK, self.WHITE, self.PURPLE]

                # Function to draw a beer button and its icon
                def draw_beer_button(x_offset, beer_image_key, button_index):
                    # Create an invisible button (just a hitbox)
                    button_rect = pygame.Rect(
                        self.first_beer_position_x + x_offset,
                        self.beer_position_y,
                        self.beer_click_width,
                        self.beer_click_height
                    )

                    # Check for clicks on the invisible button
                    mouse = pygame.mouse.get_pos()
                    click = pygame.mouse.get_pressed()
                    if button_rect.collidepoint(mouse) and click[0] == 1 and not self.mouse_held_down:
                        self.mouse_held_down = True
                        self.button_clicked(button_index)
                    elif click[0] == 0:
                        self.mouse_held_down = False

                    # Draw the beer image (no background color)
                    beer_image = self.beer_images.get(beer_image_key, None)
                    if beer_image:
                        # Resize the beer image
                        new_height = 300
                        aspect_ratio = beer_image.get_width() / beer_image.get_height()
                        new_width = int(new_height * aspect_ratio)
                        beer_image = pygame.transform.scale(beer_image, (new_width, new_height))
                        image_rect = beer_image.get_rect(center=(self.first_beer_position_x + x_offset + 40, self.beer_position_y + 150))
                        self.screen.blit(beer_image, image_rect)

                # Loop to draw all beer buttons
                for i, color in enumerate(colors):
                    draw_beer_button(600 - 100 * i, self.selected_beer_images[i], i) 

            # end screens
            elif self.player_total_points > 50:
                self.screen.fill(self.GREY)
                player_points_text = f'BEER SCORE: '
                player_points_number = f'{int(self.player_total_points)}'
                player_points_text_2 = f'finals SCORE: '
                self.draw_text(player_points_text, self.screen_width // 5, self.screen_height // 2, self.BLACK)
                self.draw_text(player_points_number, self.screen_width // 2 + 60, self.screen_height // 2 - 10, self.BLACK)
                self.draw_text(player_points_number, self.screen_width // 2 + 30, self.screen_height // 2 - 100, self.BLACK)
                pygame.draw.rect(self.screen, self.RED, [self.screen_width // 5 - 20, self.screen_height // 2 + 15, 300, 5])
                self.draw_text(player_points_text_2, self.screen_width // 5, self.screen_height // 3, self.BLACK)
                
            elif self.player_total_points > 20:
                self.screen.fill(self.GREY)
                player_points_text = f'BEER SCORE: '
                player_points_number = f'{int(self.player_total_points)}'
                self.draw_text(player_points_text, self.screen_width // 5, self.screen_height // 2, self.BLACK)
                self.draw_text(player_points_number, self.screen_width // 2 + 60, self.screen_height // 2 + 10, self.BLACK)

            else:
                self.screen.fill(self.GREY)
                player_points_text = f'FINAL SCORE: {int(self.player_total_points)}'
                self.draw_text(player_points_text, self.screen_width // 5, self.screen_height // 2, self.BLACK)

            # Flip the display to put your work on screen
            pygame.display.flip()

            # Limits FPS to 60
            self.dt = clock.tick(60) / 1000

        pygame.quit()

if __name__ == "__main__":
    game = GameWindow()
    game.main()