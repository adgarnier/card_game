import pygame
import sys
import random
import os

class Deck:
    def __init__(self):
        self.cards = self.create_deck()

    def create_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        deck = [{'rank': rank, 'suit': suit} for suit in suits for rank in ranks]
        return deck

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        if not self.cards:
            return None
        return self.cards.pop()

class GameWindow:
    def __init__(self):
        # Initialize the pygame library
        pygame.init()

        # Set up the game window dimensions
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Set the title of the window
        pygame.display.set_caption("My Game")

        # Define colors
        self.WHITE = (255, 255, 255)
        self.GREY = (178, 190, 181)
        self.BLACK = (0, 0, 0)

        # Initialize the deck
        self.deck = Deck()
        self.deck.shuffle()

        # Initialize font
        self.font = pygame.font.SysFont(None, 55)

        # Initialize card display
        self.drawn_card = None

        # Load card images
        self.card_images = self.load_card_images('playing-cards-master')   

        # Game lists
        self.starting_points = 1000000     
        self.new_points_calc = self.starting_points

    def draw_text(self, text, x, y, color):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def load_card_images(self, folder):
        card_images = {}
        for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']:
            for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']:
                card_name = f'{suit}_{rank}'
                image_path = os.path.join(folder, f'{card_name}.png')
                if os.path.exists(image_path):
                    card_images[card_name] = pygame.image.load(image_path)
                else:
                    print(f'Warning: Image not found for {card_name}')
        return card_images

    def get_card_rects(self):
        card_rects = {}
        card_width, card_height = 100, 150
        x, y = 50, 50
        for card in self.deck.cards:
            card_name = f'{card["suit"]}_{card["rank"]}'
            card_rects[card_name] = pygame.Rect(x, y, card_width, card_height)
            x += card_width + 10
            if x + card_width > self.screen_width:
                x = 50
                y += card_height + 10
        return card_rects

    # Main game loop
    def main(self):
        running = True
        clock = pygame.time.Clock()
        card_rects = self.get_card_rects()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Draw card on SPACE key press
                        self.drawn_card = self.deck.draw_card()
                        if self.drawn_card:
                            self.new_points_calc *= 0.85
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for card_name, rect in card_rects.items():
                        if rect.collidepoint(mouse_pos):
                            suit, rank = card_name.split('_')
                            self.drawn_card = {'suit': suit, 'rank': rank}
                            self.new_points_calc *= 0.85
                            break

            # Fill the screen with grey color
            self.screen.fill(self.GREY)

            # Display the points
            points_text = f'Points: {int(self.new_points_calc)}'
            self.draw_text(points_text, self.screen_width // 2 - 100, self.screen_height // 10, self.BLACK)

            # Display the deck of cards
            for card_name, rect in card_rects.items():
                card_image = self.card_images.get(card_name)
                if card_image:
                    self.screen.blit(card_image, rect)

            # Display the drawn card image
            if self.drawn_card:
                card_name = f'{self.drawn_card["suit"]}_{self.drawn_card["rank"]}'
                if card_name in self.card_images:
                    card_image = self.card_images[card_name]
                    image_rect = card_image.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
                    self.screen.blit(card_image, image_rect)

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = GameWindow()
    game.main()