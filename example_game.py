# Example file showing a circle moving on screen
import pygame

class GameWindow():
    def __init__(self):
        # pygame setup
        pygame.init()

        # Set up the game window dimensions
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Set the title of the window
        pygame.display.set_caption("Ball Mover")

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
        self.font = pygame.font.SysFont(None, 55)
        
        self.dt = 0

        self.player_pos = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)

    # Main game loop
    def main(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill(self.GREY)

            pygame.draw.circle(self.screen, self.GOLD, self.player_pos, 20)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.player_pos.y -= 400 * self.dt
            if keys[pygame.K_s]:
                self.player_pos.y += 400 * self.dt
            if keys[pygame.K_a]:
                self.player_pos.x -= 400 * self.dt
            if keys[pygame.K_d]:
                self.player_pos.x += 400 * self.dt

            # flip() the display to put your work on screen
            pygame.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            self.dt = clock.tick(60) / 1000

        pygame.quit()

if __name__ == "__main__":
    game = GameWindow()
    game.main()