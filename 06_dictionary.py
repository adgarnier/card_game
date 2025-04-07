import pygame
import sys

class GameWindow():
    def __init__(self):
        pygame.init()

        # Set up the game window dimensions
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Guess the Word")

        # Define colors
        self.WHITE = (255, 255, 255)
        self.GREY = (178, 190, 181)
        self.BLACK = (0, 0, 0)
        self.GREEN = (49, 146, 54)
        self.RED = (210, 43, 43)
        self.PURPLE = (157, 77, 187)
        self.GOLD = (243, 175, 25)

        # Initialize font
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 32)
        self.dt = 0

        self.reset_game()

    def draw_text(self, text, x, y, color, font=None):
        if font is None:
            font = self.font
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def reset_game(self):
        self.words = [
            {"definition": "A domesticated feline animal.", "word": "cat"},
            {"definition": "The opposite of cold.", "word": "hot"},
            {"definition": "A color between blue and yellow.", "word": "green"},
        ]
        self.current_index = 0
        self.input_text = ""
        self.message = ""
        self.player_total_points = 0
        self.gamestate = True

    def handle_input(self, event):
        if event.key == pygame.K_RETURN:
            guess = self.input_text.strip().lower()
            correct_word = self.words[self.current_index]["word"].lower()
            if guess == correct_word:
                self.message = "Correct!"
                self.player_total_points += 1
                self.current_index += 1
                if self.current_index >= len(self.words):
                    self.gamestate = False
            else:
                self.message = "Wrong! Try again."
            self.input_text = ""
        elif event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        else:
            if event.unicode.isalpha():
                self.input_text += event.unicode

    def main(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if self.gamestate:
                        self.handle_input(event)
                    else:
                        if event.key == pygame.K_r:
                            self.reset_game()

            self.screen.fill(self.GREY)

            if self.gamestate:
                definition = self.words[self.current_index]["definition"]
                self.draw_text("Definition:", 50, 50, self.BLACK)
                self.draw_text(definition, 50, 100, self.BLACK, self.small_font)
                self.draw_text("Your guess: " + self.input_text, 50, 200, self.BLACK, self.small_font)
                self.draw_text(self.message, 50, 250, self.GREEN if self.message == "Correct!" else self.RED, self.small_font)
                player_points_text = f'{int(self.player_total_points)}'
                self.draw_text(self.player_total_points, self.screen_height // 10, self.BLACK) 
            else:
                self.draw_text("All done!", 50, 100, self.PURPLE)
                self.draw_text(f"Final player_total_score: {self.player_total_points}", 50, 160, self.BLACK)
                self.draw_text("Press R to restart", 50, 220, self.GOLD)

            pygame.display.flip()
            self.dt = clock.tick(60) / 1000

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = GameWindow()
    game.main()
