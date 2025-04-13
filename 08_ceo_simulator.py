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

        self.money_high = 1000
        self.reputation_high = 1000
        self.morale_high = 1000

        self.reset()

    def startup_screen(self):
        selecting = True
        while selecting:
            self.screen.fill(self.GREY)
            self.draw_text("Choose Your CEO Type", 200, 100, self.font, self.BLACK)

            types = ["Capitalist", "Narcissist", "Socialist", "Idealist"]
            buttons = []

            for i, ceo_type in enumerate(types):
                rect = pygame.Rect(250, 180 + i * 80, 300, 50)
                pygame.draw.rect(self.screen, self.BLUE, rect)
                self.draw_text(ceo_type, rect.x + 20, rect.y + 10, self.small_font, self.WHITE)
                buttons.append((rect, ceo_type))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for rect, ceo_type in buttons:
                        if rect.collidepoint(event.pos):
                            self.reset()
                            self.game_type(ceo_type)
                            selecting = False

            pygame.display.flip()

    def load_scenarios(self):
        with open(os.path.join("jsons", "ceo_scenarios.json"), "r") as file:
            self.scenarios = json.load(file)

    def reset(self):
        self.click = True
        self.type = ""
        self.penalty_message = ""
        self.load_scenarios()
        self.money = 50
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
        self.penalty_message = ""
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

        # Set limits
        if self.type == "Capitalist":
            if self.reputation > self.reputation_high and self.morale > self.morale_high:
                self.money -= 10
                self.penalty_message = "The goal is money (-10 Money)"
            elif self.reputation > self.reputation_high:
                self.money -= 5
                self.penalty_message = "Too much reputation, not enough money (-5 Money)"
            elif self.morale > self.morale_high:
                self.money -= 5
                self.penalty_message = "Employee are not your priority, focus up (-5 Money)"
        if self.type == "Narcissist":
            if self.money > self.money_high and self.morale > self.morale_high:
                self.reputation -= 10
                self.penalty_message = "Think more about yourself (-10 Reputation)"
            elif self.money > self.money_high:
                self.reputation -= 5
                self.penalty_message = "You are punished for your greed (-5 Reputation)"    
            elif self.morale > self.morale_high:
                self.reputation -= 5
                self.penalty_message = "Employees have it too good (-5 Reputation)"
        if self.type == "Socialist":
            if self.money > self.money_high and self.reputation > self.reputation_high:
                self.morale -= 10
                self.penalty_message = "Employees are your top priority (-10 Morale)"
            elif self.money > self.money_high:
                self.morale -= 5
                self.penalty_message = "Greed is the enemy (-5 Morale)"
            elif self.reputation > self.reputation_high:
                self.morale -= 5
                self.penalty_message = "Unnecessary reputation holds you back (-5 Morale)"
        if self.type == "Idealist":
            if not (abs(self.money - self.reputation) <= 20 and 
                    abs(self.reputation - self.morale) <= 20 and 
                    abs(self.money - self.morale) <= 20):
                self.money -= 5
                self.reputation -= 5
                self.morale -= 5
                self.penalty_message = "All should be equal (-5 all)"

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
        color_money = self.BLACK
        color_reputation = self.BLACK
        color_morale = self.BLACK
        if self.money >= self.money_high:
            color_money = self.RED
        if self.reputation >= self.reputation_high:
            color_reputation = self.RED
        if self.morale >= self.morale_high:
            color_morale = self.RED
            
        self.draw_text(f"Money: {self.money}", 20, 20, self.small_font, color_money)
        self.draw_text(f"Reputation: {self.reputation}", 20, 50, self.small_font, color_reputation)
        self.draw_text(f"Morale: {self.morale}", 20, 80, self.small_font, color_morale)

    def check_game_over(self):
        if self.money <= 0 or self.reputation <= 0 or self.morale <= 0:
            self.game_over("You have lost the game!")
        elif (self.type == "Capitalist" and self.money >= 150)\
        or (self.type == "Narcissist" and self.reputation >= 150)\
        or (self.type == "Socialist" and self.morale >= 150)\
        or (self.type == "Idealist" and self.money >= 150 and self.reputation >= 150 and self.morale >= 150)\
        or (self.type == "" and self.money >= 100):
            self.game_over("Congratulations, you've won!")

    def game_over(self, message):
        self.screen.fill(self.GREY)
        self.draw_text(message, self.screen_width // 5, self.screen_height // 2, self.font, self.RED) 
        pygame.display.flip()

    def game_type(self, type):
        self.type = type
        if self.type == "Capitalist":
            self.reputation_high = 70
            self.morale_high = 55
        elif self.type == "Narcissist":
            self.money_high = 60
            self.morale_high = 60
        elif self.type == "Socialist":
            self.money_high = 55
            self.reputation_high = 70
        elif self.type == "Idealist":
            return

    def main(self):
        self.startup_screen()
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
                        self.startup_screen()   

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
                feedback_color = self.GREEN
                pygame.draw.rect(self.screen, self.GREY, (50, 480, self.screen_width - 100, 100))
                self.draw_text(self.feedback, 50, 500, self.font, feedback_color)
                self.draw_text(self.penalty_message, 50, 550, self.font, self.RED)
                if pygame.time.get_ticks() - self.feedback_timer > 2000:
                    self.next_scenario()

            self.draw_text(self.type, self.screen_width - 200, self.screen_height // 10, self.small_font, self.BLACK) 

            self.check_game_over()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = CEOSimulator()
    game.main()