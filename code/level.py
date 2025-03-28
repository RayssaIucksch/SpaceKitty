import sys
import random
import pygame
from code.const import COLOR_WHITE, WIN_HEIGHT, WIN_WIDTH
from code.enemy import Enemy
from code.entity import Entity
from code.entityFactory import EntityFactory
from code.player import Player
from code.star import Star
from code.database import salvar_score


class Level:
    """Main game level logic"""

    def __init__(self, window, name, game_mode):
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []

        # Initialize background and player
        self.entity_list.extend(EntityFactory.get_entity('BgLevel'))
        self.entity_list.extend(EntityFactory.get_entity('Player', position=(10, WIN_HEIGHT / 2), new_size=(110, 60)))

        # Load UI elements
        self.star_icon = pygame.image.load('./asset/star.png').convert_alpha()
        self.life_icon = pygame.image.load('./asset/life.png').convert_alpha()
        self.star_icon = pygame.transform.scale(self.star_icon, (30, 40))
        self.life_icon = pygame.transform.scale(self.life_icon, (30, 30))

        # Game state
        self.star_count = 0
        self.player_name = "Player"

        # Sound effects
        self.sounds = {
            'hit': pygame.mixer.Sound('./asset/damage.wav'),
            'collect': pygame.mixer.Sound('./asset/collectingstars.wav'),
        }
        self.sounds['hit'].set_volume(0.5)
        self.sounds['collect'].set_volume(0.7)

        self._spawn_wave()  # Initial enemy wave

    def run(self):
        """Main game loop"""
        pygame.mixer_music.load('./asset/backgroundaudio.mp3')
        pygame.mixer_music.play(-1)  # Play level music

        clock = pygame.time.Clock()
        spawn_timer = 0  # Timer for enemy spawning

        # Get player instance
        player_instance = next((e for e in self.entity_list if isinstance(e, Player)), None)
        if player_instance is None:
            print("ERROR: Player not found!")
            pygame.quit()
            sys.exit()

        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Spawn new wave periodically
            spawn_timer += 1
            if spawn_timer >= 80:  # Every ~1.3 seconds at 60fps
                self._spawn_wave()
                spawn_timer = 0

            # Update all entities
            for ent in self.entity_list:
                ent.move()
            player_instance.update()

            # Collision detection
            for entity in self.entity_list[:]:  # Copy for safe removal
                if entity.rect.colliderect(player_instance.rect):
                    if isinstance(entity, Enemy) and not player_instance.invincible:
                        if player_instance.take_damage():
                            try:
                                salvar_score(self.player_name, self.star_count)
                            except Exception as e:
                                print(f"Error saving score: {e}")
                            return "GAME_OVER"
                        entity.kill()
                    elif isinstance(entity, Star):
                        self.star_count += 1
                        if player_instance.sound_collect:
                            player_instance.sound_collect.play()
                        self.entity_list.remove(entity)

            # Rendering
            self.window.fill((0, 0, 0))  # Clear screen
            for ent in self.entity_list:
                # Flash effect when invincible
                if ent == player_instance and player_instance.invincible:
                    if pygame.time.get_ticks() % 200 < 100:  # Blink every 200ms
                        self.window.blit(ent.surf, ent.rect)
                else:
                    self.window.blit(ent.surf, ent.rect)

            # Draw HUD
            self.show_star_count(self.star_count)
            self.window.blit(self.life_icon, (10, 10))
            self.level_text(24, f"{player_instance.health}", COLOR_WHITE, (50, 10))
            self.level_text(14, f'fps: {clock.get_fps():.0f}', COLOR_WHITE, (10, WIN_HEIGHT - 35))

            pygame.display.flip()
            clock.tick(60)  # Cap at 60 FPS

        return "GAME_OVER"

    def _spawn_wave(self):
        """Create new wave of enemies and stars"""
        slots = [i * (WIN_HEIGHT // 4) + 50 for i in range(4)]  # Vertical positions
        random.shuffle(slots)

        # Spawn 3 enemies and 1 star
        enemy_positions = slots[:3]
        for y in enemy_positions:
            self.entity_list.append(EntityFactory.get_entity('Enemy', (WIN_WIDTH + 100, y))[0])

        # Place star in remaining slot
        possible_star_positions = [pos for pos in slots if pos not in enemy_positions]
        star_pos = random.choice(possible_star_positions) if possible_star_positions else slots[3]
        self.entity_list.append(EntityFactory.get_entity('Star', (WIN_WIDTH + 100, star_pos))[0])

    def show_star_count(self, star_count: int):
        """Display star counter in HUD"""
        self.window.blit(self.star_icon, (10, 40))
        self.level_text(24, f"{star_count}", COLOR_WHITE, (50, 40))

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        """Helper method for rendering text"""
        text_font = pygame.font.SysFont('Comic Sans MS', size=text_size)
        text_surf = text_font.render(text, True, text_color).convert_alpha()
        text_rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)