import pygame
import sys
import random
import os

class Deck:
    def __init__(self):
        self.cards = self.create_deck()
        self.removed_cards = []

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
        card = self.cards.pop()
        self.removed_cards.append(card)  # Store removed card
        return card

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
        self.card_images = self.load_card_images('images/playing-cards-master')   
        self.other_images = self.load_other_images('images/playing-cards-master')

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
        
        self.show_removed_cards = False

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

    def load_other_images(self, folder):
        other_images = {}
        image_list = ['win_outline', 'trash_icon_small', 'back_dark', 'back_light', 'back_light_temp']
        for image in image_list:
            image_path = os.path.join(folder, f'{image}.png')
            if os.path.exists(image_path):
                other_images[image] = pygame.image.load(image_path)
            else:
                print(f'Warning: Image not found for {image}')  # Fix: More descriptive warning
        return other_images  # Fix: Move return outside the loop

    def handle_keydown(self, key):
        if key == pygame.K_SPACE:  # Draw card on SPACE key press
            self.gamestate = True
            self.drawn_card = self.deck.draw_card()
            if self.drawn_card:
                self.points_added = False
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
        elif key == pygame.K_DOWN or key == pygame.K_s:
            self.points_added = True
            self.selected_suit_index = (self.selected_suit_index + 1) % len(self.suits)
        elif key == pygame.K_UP or key == pygame.K_w:
            self.points_added = True
            self.selected_suit_index = (self.selected_suit_index - 1) % len(self.suits)
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            self.points_added = True
            self.selected_rank_index = (self.selected_rank_index + 1) % len(self.ranks)
        elif key == pygame.K_LEFT or key == pygame.K_a:
            self.points_added = True
            self.selected_rank_index = (self.selected_rank_index - 1) % len(self.ranks)

        # Skip the guess if it has been guessed 3 times already
        guess = f'{self.suits[self.selected_suit_index]}_{self.ranks[self.selected_rank_index]}'
        if guess in self.guessed_card_counts and self.guessed_card_counts[guess] >= 3:
            print(f'{guess} has already been guessed 3 times')
            self.selected_rank_index = (self.selected_rank_index + 1) % len(self.ranks)
            self.selected_suit_index = (self.selected_suit_index + 1) % len(self.suits)

    def draw_button(self, text, x, y, width, height, color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        rect = pygame.Rect(x, y, width, height)

        pygame.draw.rect(self.screen, color, rect)
        self.draw_text(text, x + 10, y + 10, self.BLACK)

        if rect.collidepoint(mouse) and click[0] == 1 and action:
            action()

    def open_removed_cards_window(self):
        removed_window = RemovedCardsWindow(self.deck.removed_cards, self.card_images)
        removed_window.run()

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
                        self.guessed_card_counts = {}
                        self.gamestate = False

            # Fill the screen with grey color
            self.screen.fill(self.GREY)

            if not self.deck.cards:
                player_points_text = f'FINAL SCORE: {int(self.player_total_points)}'
                self.draw_text(player_points_text, self.screen_width // 5, self.screen_height // 2, self.BLACK) 

            else:
                # Display card back
                other_image = self.other_images.get("back_light_temp", None)
                if other_image:
                    image_rect = other_image.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
                    self.screen.blit(other_image, image_rect)

                # Set trash to open trash and display icon
                self.draw_button("", self.screen_width - 150 , self.screen_height - 150, 100, 100, self.GREY, self.open_removed_cards_window)
                other_image = self.other_images.get("trash_icon_small", None)
                if other_image:
                    image_rect = other_image.get_rect(center=(self.screen_width - 100, self.screen_height - 100))
                    self.screen.blit(other_image, image_rect)
                
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
                if self.drawn_card and self.gamestate == True:
                    card_name = f'{self.drawn_card["suit"]}_{self.drawn_card["rank"]}'
                    if card_name in self.card_images:
                        card_image = self.card_images[card_name]
                        image_rect = card_image.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
                        self.screen.blit(card_image, image_rect)

                # Display whether the guess was correct
                if self.drawn_card:
                    if self.suits[self.selected_suit_index] == self.drawn_card["suit"] and self.points_added == False:
                        print('You got the suit!')
                        self.player_total_points += 100
                        self.points_added = True
                    if self.ranks[self.selected_rank_index] == self.drawn_card["rank"] and self.points_added == False:
                        print('You got the rank!')
                        self.player_total_points += 500
                        self.points_added = True
                    if self.is_guess_correct:
                        other_image = self.other_images.get("win_outline", None)
                        if other_image:
                            image_rect = other_image.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
                            self.screen.blit(other_image, image_rect)

                    # Fix: Always display result text (even if empty)
                    result_text = 'Correct!' if self.is_guess_correct else ''
                    self.draw_text(result_text, self.screen_width // 5, self.screen_height - 50, self.BLACK)

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            clock.tick(60)

        pygame.quit()
        sys.exit()

class RemovedCardsWindow:
    def __init__(self, removed_cards, card_images):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Removed Cards")

        self.font = pygame.font.SysFont(None, 40)
        self.WHITE = (255, 255, 255)
        self.GREY = (178, 190, 181)
        self.BLACK = (0, 0, 0)
        self.RED = (210, 43, 43)
        self.BLUE = (76, 81, 247)
        
        # Define rank order
        rank_order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 
                    '10': 10, 'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}
        # Sort the list based on rank
        sorted_cards = sorted(removed_cards, key=lambda card: rank_order[card['rank']])
        
        self.removed_cards = sorted_cards
        self.card_images = card_images  # Pass card images to this class

    def draw_button(self, text, x, y, width, height, color):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        rect = pygame.Rect(x, y, width, height)

        pygame.draw.rect(self.screen, color, rect)
        self.draw_text(text, x + 10, y + 10, self.BLACK)

        if rect.collidepoint(mouse) and click[0] == 1:
            return True
        return False

    def draw_text(self, text, x, y, color):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def run(self):
        running = True
        card_width, card_height = 63, 99  # Set the desired size for the card images

        while running:
            self.screen.fill(self.GREY)

            # Display removed card images with resized dimensions
            max_cards_per_column = 5  # Number of cards to show per column
            x_offset = 40  # Horizontal offset for each column
            y_offset = 50   # Initial vertical offset for the first column
            column_count = 0  # Keeps track of how many columns we've used
            card_counter = 0  # Track number of cards in the current column
            for card in self.removed_cards[-52:]:  # Show last 52 removed cards
                card_name = f"{card['suit']}_{card['rank']}"
                if card_name in self.card_images:
                    card_image = self.card_images[card_name]
                    # Resize the image
                    resized_image = pygame.transform.scale(card_image, (card_width, card_height))
                    
                    # Position the image (new column after 5 cards)
                    image_rect = resized_image.get_rect(center=(x_offset, y_offset))
                    self.screen.blit(resized_image, image_rect)
                    
                    y_offset += 100  # Adjust space between images (increase to fit resized cards)
                    card_counter += 1
                    
                    # After 5 cards, move to the next column
                    if card_counter == max_cards_per_column:
                        column_count += 1
                        y_offset = 50  # Reset y_offset for the next column
                        x_offset += 72  # Move to the next column (horizontal space)
                        card_counter = 0  # Reset card counter for the new column

            # "Back to Game" button
            if self.draw_button("Back to Game", self.width // 3 + 50, self.height - 70, 200, 50, self.BLUE):
                running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.flip()

        self.screen = pygame.display.set_mode((800, 600))  # Reset back to original game window size

if __name__ == "__main__":
    game = GameWindow()
    game.main()
