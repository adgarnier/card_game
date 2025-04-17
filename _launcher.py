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
        self.TITLE = (76, 81, 247)
        self.FONT = pygame.font.SysFont(None, 48)

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Game Launcher")

        # Define games
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
        ]

        self.selected_index = 0
        self.game_rects = []
        
        self.max_visible = 8  # Number of titles to show at once
        self.visible_start_index = 0


    def draw_background(self):
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

        for i, game in enumerate(self.games):
            color = self.TITLE if i == self.selected_index else self.GREY4
            text_surface = self.FONT.render(game["title"], True, color)
            text_rect = text_surface.get_rect(topleft=(70, 30 + i * 60))

            # Create box behind text
            box_padding = 10
            box_rect = pygame.Rect(
                0,
                text_rect.y - box_padding,
                text_rect.width + 70 + box_padding * 2,
                text_rect.height + box_padding * 2
            )

            if i == self.selected_index:
                # Draw semi-transparent highlight box
                highlight_box = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
                highlight_box.fill((255, 255, 255, 255))  # Gold-ish semi-transparent
                self.screen.blit(highlight_box, (box_rect.x, box_rect.y))

            # Draw the text
            self.screen.blit(text_surface, text_rect)

            # Store rect for mouse hover
            self.game_rects.append((text_rect, i))
            
            # Show description and controls below the menu list
            desc = self.games[self.selected_index].get("desc", "")
            ctrls = self.games[self.selected_index].get("ctrls", "")
            all_ctrls1 = "R to restart | ESC to return"

            desc_surface = pygame.font.SysFont(None, 32).render(f"{desc}", True, self.TITLE)
            ctrls_surface = pygame.font.SysFont(None, 24).render(f"{ctrls}", True, self.TITLE)
            all_surface1 = pygame.font.SysFont(None, 24).render(f"{all_ctrls1}", True, self.TITLE)
            
            desc_y = 510
            
            info_box = pygame.Surface((700, 80), pygame.SRCALPHA)
            info_box.fill((255, 255, 255, 100))
            self.screen.blit(info_box, (290, desc_y))
            
            self.screen.blit(desc_surface, (300, desc_y))
            self.screen.blit(ctrls_surface, (300, desc_y + 30))
            self.screen.blit(all_surface1, (300, desc_y + 55))
            self.screen.blit(info_box, (290, desc_y - 10))
            
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