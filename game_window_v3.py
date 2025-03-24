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
            print('Deck is empty')
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
        pygame.display.set_caption("Card Guessing Game")

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
        self.player_total_points = 0
        self.guessed_card_counts = {}

        # Player's guess
        self.suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        self.selected_suit_index = 0
        self.selected_rank_index = 0
        self.is_guess_correct = False

        # Enable key repeat
        pygame.key.set_repeat(200, 50)

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

    def handle_keydown(self, key):
        if key == pygame.K_SPACE:  # Draw card on SPACE key press
            self.drawn_card = self.deck.draw_card()
            if self.drawn_card:
                card_name = f'{self.drawn_card["suit"]}_{self.drawn_card["rank"]}'
                guess = f'{self.suits[self.selected_suit_index]}_{self.ranks[self.selected_rank_index]}'
                
                if guess not in self.guessed_card_counts:
                    self.guessed_card_counts[guess] = 0
                
                if self.guessed_card_counts[guess] < 3:
                    if guess.lower() == card_name.lower():
                        self.is_guess_correct = True
                        self.player_total_points += self.new_points_calc
                        self.new_points_calc = self.starting_points
                        self.deck = Deck()
                        self.deck.shuffle()
                        self.guessed_card_counts = {}
                    else:
                        self.guessed_card_counts[guess] += 1
                        self.is_guess_correct = False
                        self.new_points_calc *= 0.85
        elif key == pygame.K_DOWN:
            self.selected_suit_index = (self.selected_suit_index + 1) % len(self.suits)
        elif key == pygame.K_UP:
            self.selected_suit_index = (self.selected_suit_index - 1) % len(self.suits)
        elif key == pygame.K_RIGHT:
            self.selected_rank_index = (self.selected_rank_index + 1) % len(self.ranks)
        elif key == pygame.K_LEFT:
            self.selected_rank_index = (self.selected_rank_index - 1) % len(self.ranks)

        # Skip the guess if it has been guessed 3 times already
        guess = f'{self.suits[self.selected_suit_index]}_{self.ranks[self.selected_rank_index]}'
        if guess in self.guessed_card_counts and self.guessed_card_counts[guess] >= 3:
            print(f'{guess} has already been guessed 3 times')
            self.selected_rank_index = (self.selected_rank_index + 1) % len(self.ranks)
            self.selected_suit_index = (self.selected_suit_index + 1) % len(self.suits)

    # Main game loop
    def main(self):
        running = True
        clock = pygame.time.Clock()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event.key)
                    if event.key == pygame.K_r:
                        print('Restarting...')
                        self.deck = Deck()
                        self.deck.shuffle()
                        self.player_total_points = 0  # Reset player points if necessary
                        self.new_points_calc = self.starting_points  # Reset round points if necessary

            # Fill the screen with grey color
            self.screen.fill(self.GREY)

            if not self.deck.cards:
                player_points_text = f'FINAL SCORE: {int(self.player_total_points)}'
                self.draw_text(player_points_text, self.screen_width // 5, self.screen_height // 2, self.BLACK) 

            else:
                # Display the total game points
                player_points_text = f'{int(self.player_total_points)}'
                self.draw_text(player_points_text, self.screen_width - 200, self.screen_height // 10, self.BLACK)           

                # Display the round points
                points_text_1 = f'POINTS:'
                self.draw_text(points_text_1, self.screen_width // 10, self.screen_height // 10, self.BLACK)
                if self.new_points_calc == self.starting_points:
                    color = self.GOLD
                elif self.new_points_calc > self.starting_points*.6:
                    color = self.PURPLE
                elif self.new_points_calc > self.starting_points*.12:
                    color = self.BLUE
                elif self.new_points_calc > self.starting_points*.01:
                    color = self.GREEN
                else:
                    color = self.GREY2
                points_text_2 = f'{int(self.new_points_calc)}'
                self.draw_text(points_text_2, self.screen_width // 3, self.screen_height // 10, color)

                # Display the player's guess
                if self.selected_suit_index == 0 or self.selected_suit_index == 1:
                    color = self.RED
                else:
                    color = self.BLACK
                guess_text_1 = f'GUESS:'
                self.draw_text(guess_text_1, self.screen_width // 10, self.screen_height - 100, self.BLACK)
                guess_text_2 = f'{self.ranks[self.selected_rank_index]} of {self.suits[self.selected_suit_index]}'
                self.draw_text(guess_text_2, self.screen_width // 3, self.screen_height - 100, color)

                # Display the drawn card image
                if self.drawn_card:
                    card_name = f'{self.drawn_card["suit"]}_{self.drawn_card["rank"]}'
                    if card_name in self.card_images:
                        card_image = self.card_images[card_name]
                        image_rect = card_image.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
                        self.screen.blit(card_image, image_rect)

                # Display whether the guess was correct
                if self.drawn_card:
                    result_text = 'Correct!' if self.is_guess_correct else ''
                    # self.draw_text(result_text, self.screen_width // 5, self.screen_height - 50, self.BLACK)
                    self.draw_text(result_text, self.screen_width // 2, self.screen_height // 2, self.BLACK)

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = GameWindow()
    game.main()