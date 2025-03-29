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
        pygame.display.set_caption("Duck Duck Bird")

        self.colors = {"WHITE": (255, 255, 255), "GREY": (178, 190, 181), "BLACK": (0, 0, 0), 
                       "RED": (210, 43, 43), "GREEN": (49, 146, 54), "BLUE": (76, 81, 247),
                       "PURPLE": (157, 77, 187)}
        # Define colors
        self.GOLD = (243, 175, 25)
        self.GREY2 = (100, 100, 100)
        self.BROWN = (137, 81, 41)
        
        self.font = pygame.font.SysFont(None, 55)
        self.dt = 0
        self.bird_images = self.load_bird_images()
        self.reset_game()

    def load_bird_images(self):
        image_list = [
            'Albatross', 'Crow', 'Duck', 'Eagle', 'Falcon', 'Flamingo', 'Goose', 'Heron', 'Hummingbird', 'Owl', 'Pidgeon'
        ]
        images = {}
        for bird in image_list:
            path = os.path.join("birds", f"{bird}.png")
            try:
                image = pygame.image.load(path)
                images[bird] = image 
            except pygame.error as e:
                print(f"Error loading {bird}.png: {e}")
                images[bird] = None  # Placeholder for missing images
        return images

    def draw_hitbox(self, bird):
        # for lower bird
        if bird["image"]:
            # Define top or bottom birds
            upper_birds = ['Albatross', 'Flamingo', 'Heron', 'Hummingbird', 'Owl']
            if bird["bird_type"] in upper_birds:
                top_or_bottom = bird["size"] // 2
            elif bird["bird_type"] == 'Falcon':
                top_or_bottom = bird["size"] // 3
            else:
                top_or_bottom = 0
            bird_rect = pygame.Rect(
                int(bird["pos"].x) - bird["size"] // 2, 
                int(bird["pos"].y) - top_or_bottom, 
                bird["size"], 
                bird["size"] // 2
            )
            pygame.draw.rect(self.screen, self.colors["RED"], bird_rect, 2)  # Red rectangle around birds

    def next_round(self):
        self.wave_height = self.wave_height * 1.1
        self.spawn_rate = self.spawn_rate * 1.1
        self.speed = self.speed * 1.1
        self.interval = self.interval * 1.1
        self.point_multiplier = self.point_multiplier * 1.1
        # Generate a new sequence of three target birds (can repeat)
        self.target_sequence = [random.choice(list(self.bird_images.keys())) for _ in range(1)]
        self.current_target_index = 0  # Track progress through the sequence

    def reset_game(self):
        self.birds = []
        self.explosions = []
        self.player_total_points = 0
        self.gamestate = True
        self.wave_height = 1
        self.spawn_rate = 1
        self.speed = 1
        self.interval = 0.005
        self.point_multiplier = 1
        
        # Generate a new sequence of three target birds (can repeat)
        self.target_sequence = [random.choice(list(self.bird_images.keys())) for _ in range(1)]
        self.current_target_index = 0  # Track progress through the sequence

    def spawn_bird(self, direction):
        bird_type = random.choice(list(self.bird_images.keys()))
        x_pos = 0 if direction == "left" else self.screen_width
        y_pos = random.randint(50, self.screen_height - 200)
        speed_x = random.randint(100, 300) * (1 if direction == "left" else -1) * self.speed
        wave_amplitude = random.randint(5, 100) * self.wave_height
        wave_frequency = 2
        size = random.randint(50, 150)  # Random size per bird spawn
        
        if self.bird_images[bird_type]:
            original_image = self.bird_images[bird_type]
            aspect_ratio = original_image.get_height() / original_image.get_width()
            new_width = size
            new_height = int(new_width * aspect_ratio)
            resized_image = pygame.transform.scale(original_image, (new_width, new_height))
        else:
            resized_image = None
        
        self.birds.append({
            "pos": pygame.Vector2(x_pos, y_pos),
            "speed_x": speed_x,
            "wave_amplitude": wave_amplitude,
            "wave_frequency": wave_frequency,
            "start_y": y_pos,
            "time_offset": random.uniform(0, math.pi * 2),
            "direction": direction,
            "bird_type": bird_type,
            "image": resized_image,
            "size": size
        })

    def explode_bird(self, bird):
        if bird["bird_type"] == self.target_sequence[self.current_target_index]:
            self.explosions.append({"pos": bird["pos"].copy(), "radius": 5, "max_radius": 50})
            self.birds.remove(bird)
            self.current_target_index += 1  # Move to the next target in the sequence
            self.player_total_points += 10 * self.point_multiplier  # Reward points for correct click

            if self.current_target_index == len(self.target_sequence):
                self.next_round()  # Generate a new sequence of 3 birds after winning
        else:
            self.gamestate = False  # Lose if you click the wrong bird

    def draw_text(self, text, x, y, color):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_sequence(self):
        """Display the target sequence at the top of the screen."""
        x_offset = 50
        for i, bird in enumerate(self.target_sequence):
            color = self.colors["GREEN"] if i < self.current_target_index else self.colors["WHITE"]
            self.draw_text(bird, x_offset, self.screen_height - 50, color)
            x_offset += 200

    def draw_crosshair(self, mouse_x, mouse_y):
        # Draw horizontal line
        pygame.draw.line(self.screen, self.colors["RED"], (mouse_x - 15, mouse_y), (mouse_x + 15, mouse_y), 2)
        # Draw vertical line
        pygame.draw.line(self.screen, self.colors["RED"], (mouse_x, mouse_y - 15), (mouse_x, mouse_y + 15), 2)

    def main(self):
        running = True
        clock = pygame.time.Clock()
        time_elapsed = 0
        
        pygame.mouse.set_visible(False)

        while running:
            self.screen.fill(self.colors["GREY"])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.reset_game()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.gamestate:
                    x, y = pygame.mouse.get_pos()
                    for bird in self.birds[:]:
                        # Create the hitbox using the same logic as `draw_hitbox`
                        upper_birds = ['Albatross', 'Flamingo', 'Heron', 'Hummingbird', 'Owl']
                        if bird["bird_type"] in upper_birds:
                            top_or_bottom = bird["size"] // 2
                        elif bird["bird_type"] == 'Falcon':
                            top_or_bottom = bird["size"] // 3
                        else:
                            top_or_bottom = 0

                        bird_rect = pygame.Rect(
                            int(bird["pos"].x) - bird["size"] // 2, 
                            int(bird["pos"].y) - top_or_bottom, 
                            bird["size"], 
                            bird["size"] // 2
                        )

                        # Check if mouse click is inside the hitbox
                        if bird_rect.collidepoint(x, y):
                            self.explode_bird(bird)

            if self.gamestate:
                
                if len(self.birds) == 0:
                    self.spawn_bird(random.choice(["left", "right"]))
                
                if random.random() < self.interval:
                    self.spawn_bird("left")
                if random.random() < self.interval:
                    self.spawn_bird("right")

                time_elapsed += self.dt
                for bird in self.birds:
                    bird["pos"].x += bird["speed_x"] * self.dt
                    bird["pos"].y = bird["start_y"] + bird["wave_amplitude"] * math.sin(pygame.time.get_ticks() * 0.002 * bird["wave_frequency"] + bird["time_offset"])
                    
                    if bird["image"]:
                        image = pygame.transform.flip(bird["image"], bird["direction"] == "right", False)
                        self.screen.blit(image, (int(bird["pos"].x) - bird["size"] // 2, int(bird["pos"].y) - bird["size"] // 2))
                        self.draw_hitbox(bird)
                
                self.birds = [b for b in self.birds if -50 <= b["pos"].x <= self.screen_width + 50]
            
                self.draw_text(f'{int(self.player_total_points)}', self.screen_width - 200, self.screen_height // 10, self.colors["BLACK"])
                self.draw_sequence()  # Draw the sequence at the top

            else:
                if self.current_target_index == len(self.target_sequence):
                    self.draw_text("YOU WIN! Press R to restart", self.screen_width // 4, self.screen_height // 2, self.colors["GREEN"])
                else:
                    self.draw_text(f"FINAL SCORE: {self.player_total_points}", self.screen_width // 5, self.screen_height // 2, self.colors["BLACK"])

            # Get mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Draw crosshair at the mouse position
            self.draw_crosshair(mouse_x, mouse_y)

            for explosion in self.explosions[:]:
                explosion["radius"] += 5
                if explosion["radius"] >= explosion["max_radius"]:
                    self.explosions.remove(explosion)
                else:
                    pygame.draw.circle(self.screen, self.colors["RED"], (int(explosion["pos"].x), int(explosion["pos"].y)), explosion["radius"], 3)

            pygame.display.flip()
            self.dt = clock.tick(60) / 1000
        
        pygame.quit()

if __name__ == "__main__":
    game = GameWindow()
    game.main()
