import pygame
import subprocess
import sys

class LauncherWindow():
    def __init__(self):
        pygame.init()
        # Constants
        self.screen_width = 800
        self.screen_height = 600
        self.WHITE = (255, 255, 255)
        self.GREY = (178, 190, 181)
        self.GREY4 = (158, 170, 161)
        self.BLACK = (0, 0, 0)
        self.GOLD = (243, 175, 25)
        self.FONT = pygame.font.SysFont(None, 48)

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Game Launcher")

        # Define games
        self.games = [
            {"title": "Card Guessing Game", "file": "01_card_guessing_game.py", "desc": "A game of chance, memory, and patience.", "bg": "images/screenshots/01.png"},
            {"title": "Dodge Ball", "file": "02_dodge_ball.py", "desc": "Dodge the ball(s).", "bg": "images/screenshots/02.png"},
            {"title": "Drinking Game", "file": "03_drinking_game.py", "desc": "Cheers.", "bg": "images/screenshots/03.png"},
            {"title": "Duck Duck Goose", "file": "04_duck_duck_goose.py", "desc": "Non-vegan first person shooter.", "bg": "images/screenshots/04.png"},
            {"title": "Maze v2", "file": "05_maze_v2.py", "desc": "The only way out is in.", "bg": "images/screenshots/05.png"},
            {"title": "Match the Meaning", "file": "06_match_the_meaning.py", "desc": "Game (Noun): A form of play or sport.", "bg": "images/screenshots/06.png"},
            {"title": "Duck Hunt", "file": "07_duck_hunt.py", "desc": "Find the duck-like object.", "bg": "images/screenshots/07.png"},
            {"title": "CEO Simulator", "file": "08_ceo_simulator.py", "desc": "All the responsibility, with all the hassle.", "bg": "images/screenshots/08.png"},
        ]

        self.selected_index = 0
        self.game_rects = []

    def draw_background(self):
        self.screen.fill(self.GREY)
        
        # Load and scale the background image
        bg_path = self.games[self.selected_index]["bg"]
        bg_image = pygame.image.load(bg_path).convert()  # .convert() for performance
        bg_image = pygame.transform.scale(
            bg_image,
            (self.screen.get_width(), self.screen.get_height())
        )

        self.screen.blit(bg_image, (0, 0))

    def draw_menu(self):
        self.draw_background()
        self.game_rects.clear()

        box_surface = pygame.Surface((460, 500), pygame.SRCALPHA)
        box_surface.fill((255, 255, 255, 230))
        self.screen.blit(box_surface, (0, 55))

        for i, game in enumerate(self.games):
            color = (76, 81, 247) if i == self.selected_index else self.GREY4
            text_surface = self.FONT.render(game["title"], True, color)
            text_rect = text_surface.get_rect(topleft=(70, 70 + i * 60))
            # Create transparent box behind text
            box_padding = 10
            box_rect = pygame.Rect(
                text_rect.x - box_padding,
                text_rect.y - box_padding,
                text_rect.width + box_padding * 2,
                text_rect.height + box_padding * 2
            )

            # Draw the text
            self.screen.blit(text_surface, text_rect)

            # Store rect for mouse hover
            self.game_rects.append((text_rect, i))

        desc = self.games[self.selected_index].get("desc", "")
        desc_surface = pygame.font.SysFont(None, 32).render(desc, True, self.BLACK)
        # self.screen.blit(desc_surface, (100, 600 - 50))  # Bottom margin

        pygame.display.flip()

    def update_hover_selection(self):
        mouse_pos = pygame.mouse.get_pos()
        for rect, idx in self.game_rects:
            if rect.collidepoint(mouse_pos):
                self.selected_index = idx
                break

    def launch_game(self, filepath):
        pygame.quit()
        subprocess.run([sys.executable, filepath])
        pygame.init()
        self.__init__()

    def main(self):
        running = True
        while running:
            self.update_hover_selection()
            self.draw_menu()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.games)
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.games)
                    elif event.key == pygame.K_RETURN:
                        self.launch_game(self.games[self.selected_index]["file"])

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for rect, idx in self.game_rects:
                        if rect.collidepoint(event.pos):
                            self.selected_index = idx
                            self.launch_game(self.games[idx]["file"])

if __name__ == "__main__":
    launcher = LauncherWindow()
    launcher.main()