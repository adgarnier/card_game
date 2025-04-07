import pygame
import random
import json
import os
import Levenshtein  # You may need to install the `python-Levenshtein` package

class GameWindow:
    def __init__(self):
        # pygame setup
        pygame.init()

        # Set up the game window dimensions
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Set the title of the window
        pygame.display.set_caption("Word Guessing Game")

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
        self.font = pygame.font.SysFont(None, 50)
        self.small_font = pygame.font.SysFont(None, 30)

        # Load dictionary
        self.load_dictionary()

        # Reset game state
        self.reset_game()

    def load_dictionary(self):
        # Load the dictionary from the file
        with open(os.path.join("dictionary", "filtered.json"), "r") as file:
            self.dictionary = json.load(file)

    def reset_game(self):
        # Reset the game state
        self.score = 0
        self.guessed_word = ""
        
        # Keep picking a word until we find one with meanings
        while True:
            self.word = random.choice(list(self.dictionary.keys()))  # Random word from the dictionary
            if self.dictionary[self.word]["MEANINGS"]:  # Check if there are meanings available
                break

        self.length = len(self.dictionary[self.word])
        self.type = self.dictionary[self.word]["MEANINGS"][0][0]  # Get the first meaning only
        self.definition = self.dictionary[self.word]["MEANINGS"][0][1]  # Get the first meaning only
        self.synonyms = self.dictionary[self.word]["SYNONYMS"][:]
        word = str(self.word).capitalize()
        print(word)
        self.synonyms = str(self.synonyms).replace("[", "").replace("]", "").replace("\'", "").replace(word, "")
        self.game_over = False
        self.feedback = ""

    def draw_text(self, text, x, y, font, color):
        # Break the text into lines if it exceeds the screen width
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            # If the word doesn't fit on the current line, move it to the next line
            if font.size(current_line + word)[0] <= self.screen_width - 500:  # 40px padding from the edge
                current_line += word + " "
            else:
                lines.append(current_line)
                current_line = word + " "
        
        lines.append(current_line)  # Add the last line

        # Draw each line of text
        line_height = font.get_height() + 5  # Add some space between lines
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, color)
            self.screen.blit(text_surface, (x, y + i * line_height))

    def get_feedback(self):
        # Calculate Levenshtein distance between guessed word and the correct word
        if self.guessed_word:
            distance = Levenshtein.distance(self.guessed_word.lower(), self.word.lower())
            if distance == 0:
                return "Correct!"
            elif distance <= 2:  # If the word is close, within a 2-character difference
                return "<=2 letters away"
            elif distance <= 5:  # If the word is close, within a 2-character difference
                return "<=5 letters away"
            elif distance <= 10:  # If the word is close, within a 2-character difference
                return "<=10 letters away"
            else:
                return "Try again!"
        return ""

    def main(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            # Poll for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and not self.game_over:
                        if self.guessed_word.lower() == self.word.lower():  # Check if the guess is correct
                            self.score += 1
                            self.reset_game()
                            self.feedback = ""  # Clear feedback after resetting the word
                        else:
                            self.feedback = self.get_feedback()  # Give feedback if the guess is close
                            self.guessed_word = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.guessed_word = self.guessed_word[:-1]  # Remove last character
                    elif event.key >= 97 and event.key <= 122:  # Check for alphabetic keys a-z
                        self.guessed_word += chr(event.key)
                    elif event.key == pygame.K_ESCAPE:  # If the player presses the 'ESC' key, skip the definition
                        self.feedback = f"The word was: {self.word}"  # Show the correct word
                        self.reset_game()
                        self.guessed_word = ""  # Clear any previous guess
                        self.feedback = ""  # Clear feedback after skipping

            # Fill the screen with white
            self.screen.fill(self.GREY)

            if not self.game_over:
                # Draw the definition as the hint
                self.draw_text(f"TYPE: {self.type}", 400, 120, self.small_font, self.BLACK)
                self.draw_text(f"LENGTH: {len(self.word)}", 80, 120, self.small_font, self.BLACK)
                self.draw_text(f"DEFINITION: {self.definition}", 80, 150, self.small_font, self.BLACK)
                self.draw_text(f"SYNONYMS: {self.synonyms}", 400, 150, self.small_font, self.BLACK)

                # Draw the current guessed word
                self.draw_text(f"Guess the word: {self.guessed_word}", self.screen_width // 10, self.screen_height - 100, self.font, self.BLACK)

                # Draw the score
                self.draw_text(f"{self.score}", self.screen_width - 200, self.screen_height // 10, self.font, self.BLACK)

                # Draw feedback if available
                if self.feedback:
                    self.draw_text(self.feedback, self.screen_width // 10, self.screen_height - 200, self.font, self.GREEN if "close" in self.feedback.lower() else self.RED)
            else:
                # Display game over message
                self.draw_text(f"Final Score: {self.score}", self.screen_width // 4, self.screen_height // 2, self.font, self.RED)

            # Flip the display to put your work on screen
            pygame.display.flip()

            # Limits FPS to 60
            clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = GameWindow()
    game.main()
