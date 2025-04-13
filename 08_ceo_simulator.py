import pygame
import random
import json
import os

class CEOSimulator:
    def __init__(self):
        pygame.init()

        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("CEO Simulator")

        self.WHITE = (255, 255, 255)
        self.GREY = (230, 230, 230)
        self.BLACK = (0, 0, 0)
        self.RED = (200, 50, 50)
        self.GREEN = (50, 160, 50)
        self.BLUE = (50, 80, 200)
        self.GOLD = (200, 180, 50)

        self.font = pygame.font.SysFont(None, 40)
        self.small_font = pygame.font.SysFont(None, 30)

        self.reset()

    def load_scenarios(self):
        with open(os.path.join("jsons", "ceo_scenarios.json"), "r") as file:
            self.scenarios = json.load(file)

    def reset(self):
        self.click = True
        self.load_scenarios()
        self.money = 100
        self.reputation = 50
        self.morale = 50
        self.feedback = ""
        self.feedback_timer = 0
        self.option_rects = []
        self.scenarios_seen = set()
        self.next_scenario()

    def next_scenario(self):
        if len(self.scenarios_seen) == len(self.scenarios):
            self.scenarios_seen.clear()  # Reset when all have been shown

        available_indexes = [i for i in range(len(self.scenarios)) if i not in self.scenarios_seen]
        chosen_index = random.choice(available_indexes)

        self.scenarios_seen.add(chosen_index)
        self.current = self.scenarios[chosen_index]

        self.feedback = ""
        self.feedback_timer = 0
        self.option_rects = []
        self.click = True

    def draw_text(self, text, x, y, font, color):
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            if font.size(current_line + word)[0] <= self.screen_width - 100:
                current_line += word + " "
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)

        line_height = font.get_height() + 5
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, color)
            self.screen.blit(text_surface, (x, y + i * line_height))

    def apply_effects(self, effects):
        self.money += effects.get("money", 0)
        self.reputation += effects.get("reputation", 0)
        self.morale += effects.get("morale", 0)

        # Clamp values
        self.money = max(0, self.money)
        self.reputation = max(0, min(100, self.reputation))
        self.morale = max(0, min(100, self.morale))

    def check_click(self, pos):
        for rect, choice in self.option_rects:
            if rect.collidepoint(pos):
                self.apply_effects(choice["effects"])
                self.feedback = choice["feedback"]
                self.feedback_timer = pygame.time.get_ticks()
                return

    def draw_stats(self):
        self.draw_text(f"Money: {self.money}", 20, 20, self.small_font, self.BLACK)
        self.draw_text(f"Reputation: {self.reputation}", 20, 50, self.small_font, self.BLACK)
        self.draw_text(f"Morale: {self.morale}", 20, 80, self.small_font, self.BLACK)

    def check_game_over(self):
        if self.money <= 0 or self.reputation <= 0 or self.morale <= 0:
            self.game_over("You have lost the game!")
        elif self.money >= 1000:  # Or any victory condition
            self.game_over("Congratulations, you've won!")

    def game_over(self, message):
        self.screen.fill(self.GREY)
        self.draw_text(message, self.screen_width // 5, self.screen_height // 2, self.font, self.RED) 
        pygame.display.flip()

    def game_type(self, type):
        self.types = type
        if type == "Narcissist":
            print("N")
        if type == "Capitalist":
            print("capitalism rules")
        if type == "Socialist":
            
        
    narcissist
    capitalist
    socialist

    def main(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_click(event.pos)
                elif event.type ==pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()
                    if event.key == pygame.K_1:
                        self.game_type("Capitalist")
                    if event.key == pygame.K_2:
                        self.game_type("Narcissist")
                    if event.key == pygame.K_3:
                        self.game_type("Socialist")
                    if event.key == pygame.K_4:
                        self.game_type("Idealist")

            self.screen.fill(self.GREY)
            self.draw_stats()

            self.draw_text(self.current["scenario"], 50, 140, self.font, self.BLACK)

            self.option_rects = []
            for i, choice in enumerate(self.current["choices"]):
                rect = pygame.Rect(70, 260 + i * 70, 660, 50)
                pygame.draw.rect(self.screen, self.BLUE, rect)
                self.draw_text(choice["text"], rect.x + 10, rect.y + 10, self.small_font, self.WHITE)
                if self.click:
                    self.option_rects.append((rect, choice))

            if self.feedback:
                self.click = False
                feedback_color = self.GREEN if "bold" not in self.feedback else self.RED
                pygame.draw.rect(self.screen, self.GREY, (50, 480, self.screen_width - 100, 100))
                self.draw_text(self.feedback, 50, 500, self.font, feedback_color)
                if pygame.time.get_ticks() - self.feedback_timer > 1000:
                    self.next_scenario()

            self.check_game_over()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = CEOSimulator()
    game.main()