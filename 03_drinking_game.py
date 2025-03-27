import pygame
import random
import time
import threading
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

        # Initialize font
        self.font = pygame.font.SysFont(None, 55)
        self.dt = 0

        self.beer_images = self.load_beer_images('beers')
        self.selected_beer_images = []

        self.mouse_held_down = False  # Track if the mouse button is held down

        self.reset_game()

    def reset_game(self):
        # Resets the game state
        self.player_total_points = 0
        self.gamestate = True
        self.timer = ''
        self.ball_size = 20
        self.player_ball_size = 20
        self.bomb_size = 20
        self.player_speed = 400
        self.interval = 0.02
        self.point_multiplier = 0.05

        # Reset selected beer images
        self.selected_beer_images = self.select_unique_random_beer_images()

        # Pattern game specific
        self.sequence = []
        self.user_sequence = []
        self.generate_sequence()

    def load_beer_images(self, folder):
        beer_images = {}
        image_list = ['budweiser', 'budlight', 'busch', 'coorslight', 'corona', 'heineken', 'millerlite', 'moosehead']
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

    def show_sequence(self):
        self.screen.fill(self.GREY)
        for idx, i in enumerate(self.sequence):
            beer_image_key = self.selected_beer_images[i]
            beer_image = self.beer_images.get(beer_image_key, None)
            if beer_image:
                # Calculate the new dimensions
                new_height = 100
                aspect_ratio = beer_image.get_width() / beer_image.get_height()
                new_width = int(new_height * aspect_ratio)
                beer_image = pygame.transform.scale(beer_image, (new_width, new_height))
                image_rect = beer_image.get_rect(center=(100 + idx * 120, 100))
                self.screen.blit(beer_image, image_rect)
        pygame.display.flip()
        time.sleep(1)
        self.screen.fill(self.GREY)
        pygame.display.flip()

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
        if self.user_sequence == self.sequence[:len(self.user_sequence)]:
            if len(self.user_sequence) == len(self.sequence):
                self.user_sequence = []
                self.generate_sequence()
        else:
            print("Incorrect sequence!")
            self.reset_game()

    def temp(self, message):
        print(message)

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
            self.screen.fill(self.GREY)

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
                def draw_beer_button(x_offset, color, beer_image_key, button_index):
                    self.draw_button("", self.first_beer_position_x + x_offset, self.beer_position_y, self.beer_click_width, self.beer_click_height, color, lambda: self.button_clicked(button_index))
                    beer_image = self.beer_images.get(beer_image_key, None)
                    if beer_image:
                        # Calculate the new dimensions
                        new_height = 300
                        aspect_ratio = beer_image.get_width() / beer_image.get_height()
                        new_width = int(new_height * aspect_ratio)
                        beer_image = pygame.transform.scale(beer_image, (new_width, new_height))
                        image_rect = beer_image.get_rect(center=(self.first_beer_position_x + x_offset + 40, self.beer_position_y + 150))
                        self.screen.blit(beer_image, image_rect)

                # Man's body
                pygame.draw.circle(self.screen, self.RED, (self.screen_width // 2, self.screen_height // 4), 80)
                pygame.draw.circle(self.screen, self.BLUE, (self.screen_width // 2, self.screen_height), 400)

                # Loop to draw all beer buttons
                for i, color in enumerate(colors):
                    draw_beer_button(600 - 100 * i, color, self.selected_beer_images[i], i)

            else:
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