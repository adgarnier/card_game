# Example file showing balls randomly falling from the top of the window
import pygame
import random

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

        # List to store balls
        self.balls = []
        self.ball_size = 20

        self.player_total_points = 0

    # Method to spawn a new ball at a random horizontal position at the top
    def spawn_ball(self):
        x_pos = random.randint(0, self.screen_width)
        y_pos = 0
        speed = random.randint(100, 300)
        self.balls.append({"pos": pygame.Vector2(x_pos, y_pos), "speed": speed})

    def draw_text(self, text, x, y, color):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    # Main game loop
    def main(self):
        running = True
        clock = pygame.time.Clock()
        gamestate = True

        while running:
            # Poll for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        print('Restarting...')
                        self.balls = []
                        self.player_total_points = 0  # Reset player points if necessary
                        self.new_points_calc = self.player_total_points  # Reset round points if necessary
                        self.gamestate = True

            # Fill the screen with a color to wipe away anything from last frame
            self.screen.fill(self.GREY)

            for ball in self.balls:
                if self.player_pos.distance_to(ball["pos"]) < self.ball_size * 2:
                    gamestate = False
                    self.balls = []

            if gamestate == True:
                # Draw the player circle
                pygame.draw.circle(self.screen, self.GOLD, self.player_pos, self.ball_size)

                keys = pygame.key.get_pressed()
                if keys[pygame.K_w] and self.player_pos.y > 0 + self.ball_size:
                    self.player_pos.y -= 650 * self.dt
                if keys[pygame.K_s] and self.player_pos.y < self.screen_height - self.ball_size:
                    self.player_pos.y += 650 * self.dt
                if keys[pygame.K_a] and self.player_pos.x > 0 + self.ball_size:
                    self.player_pos.x -= 650 * self.dt
                if keys[pygame.K_d] and self.player_pos.x < self.screen_width - self.ball_size:
                    self.player_pos.x += 650 * self.dt

                # Spawn a new ball at random intervals
                if random.random() < 0.02:  # Adjust the probability as needed
                    self.spawn_ball()

                # Update and draw balls
                for ball in self.balls:
                    ball["pos"].y += ball["speed"] * self.dt
                    pygame.draw.circle(self.screen, self.RED, (int(ball["pos"].x), int(ball["pos"].y)), self.ball_size)

                # Display points
                player_points_text = f'{int(self.player_total_points)}'
                self.draw_text(player_points_text, self.screen_width - 200, self.screen_height // 10, self.BLACK) 

                # Remove balls that have fallen off the screen
                self.balls = [ball for ball in self.balls if ball["pos"].y < self.screen_height + self.ball_size]

            else:
                player_points_text = f'FINAL SCORE: {int(self.player_total_points)}'
                self.draw_text(player_points_text, self.screen_width // 5, self.screen_height // 2, self.BLACK)

            # Flip the display to put your work on screen
            pygame.display.flip()

            # Limits FPS to 60
            self.dt = clock.tick(60) / 1000

        pygame.quit()

if __name__ == "__main__":
    game = GameWindow()
    game.main()