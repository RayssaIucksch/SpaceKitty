import pygame
from code.const import ENTITY_SPEED, WIN_HEIGHT, WIN_WIDTH, CONTROLS
from code.entity import Entity

class Player(Entity):
    def __init__(self, name: str, position: tuple, new_size: None):
        super().__init__(name, position)
        if new_size:
            self.surf = pygame.transform.scale(self.surf, new_size)
            self.rect = self.surf.get_rect(left=position[0], top=position[1])

        # Player stats
        self.max_health = 3
        self.health = self.max_health
        self.score = 0
        self.invincible = False  # Damage immunity flag
        self.invincible_timer = 0  # Frames of remaining immunity

        # Load sound effects
        try:
            self.sound_hit = pygame.mixer.Sound('./asset/damage.wav')
            self.sound_collect = pygame.mixer.Sound('./asset/collectingstars.wav')
        except:
            print("Error loading sound files!")

    def move(self):
        # Handle player movement using configured controls
        pressed_key = pygame.key.get_pressed()
        if any(pressed_key[key] for key in CONTROLS['up']) and self.rect.top > 0:
            self.rect.centery -= ENTITY_SPEED[self.name]
        if any(pressed_key[key] for key in CONTROLS['down']) and self.rect.bottom < WIN_HEIGHT:
            self.rect.centery += ENTITY_SPEED[self.name]

        if any(pressed_key[key] for key in CONTROLS['left']) and self.rect.left > 0:
            self.rect.centerx -= ENTITY_SPEED[self.name]
        if any(pressed_key[key] for key in CONTROLS['right']) and self.rect.right < WIN_WIDTH:
            self.rect.centerx += ENTITY_SPEED[self.name]

    def take_damage(self):
        if self.invincible:
            return False

        self.health -= 1
        if self.sound_hit:
            self.sound_hit.play()

        # Activate temporary invincibility (1 second at 60fps)
        self.invincible = True
        self.invincible_timer = 60

        return self.health <= 0  # Return True if player died

    def update(self):
        # Count down invincibility frames
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

    def collect_star(self):
        self.score += 100
        if hasattr(self, 'sound_collect'):
            self.sound_collect.play()