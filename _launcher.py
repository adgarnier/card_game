import pygame
import subprocess
import sys

class LauncherWindow():
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.WHITE = (255, 255, 255)
        self.GREY = (178, 190, 181)
        self.GREY4 = (158, 170, 161)
        self.BLACK = (0, 0, 0)
        self.GOLD = (243, 175, 25)
        self.TITLE = (76, 81, 247)
        self.FONT = pygame.font.SysFont(None, 48)

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Game Launcher")

        self.games = [
            {"title": "Card Guessing Game", "file": "01_card_guessing_game.py", "desc": "A game of chance, memory, and patience.",
             "bg": "images/screenshots/01.png", "ctrls": "WASD or Arrow keys to select | SPACE to guess"},
            {"title": "Dodge Ball", "file": "02_dodge_ball.py", "desc": "Dodge the ball(s).",
             "bg": "images/screenshots/02.png", "ctrls": "WASD or Arrow keys to move | Q/E to switch modes"},
            {"title": "Drinking Game", "file": "03_drinking_game.py", "desc": "Cheers.",
             "bg": "images/screenshots/03.png", "ctrls": "Mouse click to match sequence"},
            {"title": "Duck Duck Goose", "file": "04_duck_duck_goose.py", "desc": "Non-vegan first person shooter.",
             "bg": "images/screenshots/04.png", "ctrls": "Mouse click to shoot | Press 1-9 for difficulty"},
            {"title": "Maze v2", "file": "05_maze_v2.py", "desc": "The only way out is in.",
             "bg": "images/screenshots/05.png", "ctrls": "Click or Arrow keys to navigate"},
            {"title": "Match the Meaning", "file": "06_match_the_meaning.py", "desc": "Game (Noun): A form of play or sport.",
             "bg": "images/screenshots/06.png", "ctrls": "Click or press 1-6 to choose a word"},
            {"title": "Duck Hunt", "file": "07_duck_hunt.py", "desc": "Find the duck-like object.",
             "bg": "images/screenshots/07.png", "ctrls": "Mouse click on bird"},
            {"title": "CEO Simulator", "file": "08_ceo_simulator.py", "desc": "All the responsibility, with all the hassle.",
             "bg": "images/screenshots/08.png", "ctrls": "Click to select persona and responses"},
            {"title": "S p a c e", "file": "09_space.py", "desc": "It's out of this world.",
             "bg": "images/screenshots/09.png", "ctrls": "Click to add planets"},
            {"title": "Color Correct", "file": "10_color_correct.py", "desc": "Distinguish between blue and other blue.",
             "bg": "images/screenshots/10.png", "ctrls": "Click to pick color"},
            ]

        self.selected_index = 0
        self.visible_start_index = 0
        self.max_visible = 7
        self.game_rects = []

    def draw_background(self):
        bg_path = self.games[self.selected_index]["bg"]
        bg_image = pygame.image.load(bg_path).convert()
        bg_image = pygame.transform.scale(bg_image, (self.screen_width, self.screen_height))
        self.screen.blit(bg_image, (0, 0))

    def draw_menu(self):
        self.draw_background()
        self.game_rects.clear()

        visible_games = self.games[self.visible_start_index:self.visible_start_index + self.max_visible]

        for i, game in enumerate(visible_games):
            actual_index = self.visible_start_index + i
            color = self.TITLE if actual_index == self.selected_index else self.GREY4
            text_surface = self.FONT.render(game["title"], True, color)
            text_rect = text_surface.get_rect(topleft=(70, 60 + i * 60))

            box_padding = 10
            box_rect = pygame.Rect(
                0,
                text_rect.y - box_padding,
                text_rect.width + 70 + box_padding * 2,
                text_rect.height + box_padding * 2
            )

            if actual_index == self.selected_index:
                highlight_box = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
                highlight_box.fill((255, 255, 255, 255))
                self.screen.blit(highlight_box, (box_rect.x, box_rect.y))

            self.screen.blit(text_surface, text_rect)
            self.game_rects.append((text_rect, actual_index))

        desc = self.games[self.selected_index].get("desc", "")
        ctrls = self.games[self.selected_index].get("ctrls", "")
        all_ctrls1 = "R to restart | ESC to return"

        desc_surface = pygame.font.SysFont(None, 32).render(f"{desc}", True, self.TITLE)
        ctrls_surface = pygame.font.SysFont(None, 24).render(f"{ctrls}", True, self.TITLE)
        all_surface1 = pygame.font.SysFont(None, 24).render(f"{all_ctrls1}", True, self.TITLE)

        desc_y = 510
        info_box = pygame.Surface((700, 80), pygame.SRCALPHA)
        info_box.fill((255, 255, 255, 255))
        self.screen.blit(info_box, (290, desc_y))
        self.screen.blit(desc_surface, (300, desc_y + 5))
        self.screen.blit(ctrls_surface, (300, desc_y + 35))
        self.screen.blit(all_surface1, (300, desc_y + 60))
        info_box.fill((255, 255, 255, 100))
        self.screen.blit(info_box, (290, desc_y))

        self.add_scroll_indicators()

        pygame.display.flip()

    def add_scroll_indicators(self):
        arrow_color = (255, 255, 255)
        arrow_size = 20
        center_x = 200

        if self.visible_start_index > 0:
            pygame.draw.polygon(self.screen, arrow_color, [
                (center_x, 5),
                (center_x - arrow_size, 25),
                (center_x + arrow_size, 25)
            ])

        if self.visible_start_index + self.max_visible < len(self.games):
            pygame.draw.polygon(self.screen, arrow_color, [
                (center_x, 570),
                (center_x - arrow_size, 550),
                (center_x + arrow_size, 550)
            ])

    def update_hover_selection(self):
        mouse_pos = pygame.mouse.get_pos()
        for rect, idx in self.game_rects:
            if rect.collidepoint(mouse_pos):
                self.selected_index = idx
                self.ensure_selected_visible()
                break

    def ensure_selected_visible(self):
        if self.selected_index < self.visible_start_index:
            self.visible_start_index = self.selected_index
        elif self.selected_index >= self.visible_start_index + self.max_visible:
            self.visible_start_index = self.selected_index - self.max_visible + 1

    def launch_game(self, filepath):
        pygame.quit()
        subprocess.run([sys.executable, filepath])

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
                        self.ensure_selected_visible()
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.games)
                        self.ensure_selected_visible()
                    elif event.key == pygame.K_RETURN:
                        self.launch_game(self.games[self.selected_index]["file"])

                elif event.type == pygame.MOUSEWHEEL:
                    if event.y > 0:  # Scroll up
                        self.selected_index = max(0, self.selected_index - 1)
                        self.ensure_selected_visible()
                    elif event.y < 0:  # Scroll down
                        self.selected_index = min(len(self.games) - 1, self.selected_index + 1)
                        self.ensure_selected_visible()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for rect, idx in self.game_rects:
                        if rect.collidepoint(event.pos):
                            self.selected_index = idx
                            self.ensure_selected_visible()
                            self.launch_game(self.games[idx]["file"])

if __name__ == "__main__":
    launcher = LauncherWindow()
    launcher.main()