import math
import pygame
import random
import os

class GameWindow():
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Duck Duck Goose")

        self.colors = {"WHITE": (255, 255, 255), "GREY": (178, 190, 181), "BLACK": (0, 0, 0)}
        self.font = pygame.font.SysFont(None, 55)
        self.dt = 0
        self.beer_images = self.load_beer_images()
        self.reset_game()

    def load_beer_images(self):
        image_list = [
            'alexanderkeiths', 'becks', 'budweiser', 'budlight', 'busch', 'carlsberg', 'chambly', 'coorslight',
            'corona', 'heineken', 'hoegaarden', 'hofbrau', 'iceberg', 'labattblue', 'michelobultra', 'millerlite',
            'modelo', 'molsoncanadian', 'moosehead', 'sapporo', 'stellaartois', 'tsingtao'
        ]
        images = {}
        for beer in image_list:
            path = os.path.join("beers", f"{beer}.png")
            images[beer] = pygame.image.load(path)
        return images

    def reset_game(self):
        self.birds = []
        self.explosions = []
        self.player_total_points = 0
        self.gamestate = True
        self.bird_size = 40  # Adjusted for beer images
        self.interval = 0.02
        self.point_multiplier = 0.05  

    def spawn_bird(self, direction):
        beer_type = random.choice(list(self.beer_images.keys()))
        x_pos = 0 if direction == "left" else self.screen_width
        y_pos = random.randint(50, self.screen_height - 200)
        speed_x = random.randint(100, 300) * (1 if direction == "left" else -1)
        wave_amplitude = random.randint(5, 250)
        wave_frequency = 2
        self.birds.append({
            "pos": pygame.Vector2(x_pos, y_pos),
            "speed_x": speed_x,
            "wave_amplitude": wave_amplitude,
            "wave_frequency": wave_frequency,
            "start_y": y_pos,
            "time_offset": random.uniform(0, math.pi * 2),
            "direction": direction,
            "beer_type": beer_type
        })

    def explode_bird(self, bird):
        self.explosions.append({"pos": bird["pos"].copy(), "radius": 5, "max_radius": 50})
        self.birds.remove(bird)

    def draw_text(self, text, x, y, color):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def main(self):
        running = True
        clock = pygame.time.Clock()
        time_elapsed = 0

        while running:
            self.screen.fill(self.colors["GREY"])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.reset_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    for bird in self.birds[:]:
                        if bird["pos"].distance_to((x, y)) < self.bird_size:
                            self.explode_bird(bird)

            if self.gamestate:
                if random.random() < self.interval:
                    self.spawn_bird("left")
                if random.random() < self.interval:
                    self.spawn_bird("right")

                time_elapsed += self.dt
                for bird in self.birds:
                    bird["pos"].x += bird["speed_x"] * self.dt
                    bird["pos"].y = bird["start_y"] + bird["wave_amplitude"] * math.sin(time_elapsed * bird["wave_frequency"] + bird["time_offset"])
                    beer_image = self.beer_images[bird["beer_type"]]
                    self.screen.blit(beer_image, (int(bird["pos"].x) - self.bird_size // 2, int(bird["pos"].y) - self.bird_size // 2))
                
                self.birds = [b for b in self.birds if 0 <= b["pos"].x <= self.screen_width]
                self.player_total_points += self.point_multiplier
                self.draw_text(f'{int(self.player_total_points)}', self.screen_width - 200, self.screen_height // 10, self.colors["BLACK"])
            
            for explosion in self.explosions[:]:
                explosion["radius"] += 5
                if explosion["radius"] >= explosion["max_radius"]:
                    self.explosions.remove(explosion)
                else:
                    pygame.draw.circle(self.screen, self.colors["WHITE"], (int(explosion["pos"].x), int(explosion["pos"].y)), explosion["radius"], 2)
            
            pygame.display.flip()
            self.dt = clock.tick(60) / 1000
        
        pygame.quit()

if __name__ == "__main__":
    game = GameWindow()
    game.main()
