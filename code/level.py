import sys
import random
import pygame
from code.const import COLOR_WHITE, WIN_HEIGHT, WIN_WIDTH
from code.enemy import Enemy
from code.entity import Entity
from code.entityFactory import EntityFactory
from code.player import Player
from code.star import Star


class Level:
    def __init__(self, window, name, game_mode):
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity('BgLevel'))
        self.entity_list.extend(EntityFactory.get_entity('Player', position=(10, WIN_HEIGHT / 2), new_size=(110, 60)))

        self.sounds = {
            'hit': pygame.mixer.Sound('./asset/damage.wav'),
            'collect': pygame.mixer.Sound('./asset/collectingstars.wav'),
        }
        self.sounds['hit'].set_volume(0.5)
        self.sounds['collect'].set_volume(0.7)

        self._spawn_wave()

    def run(self):
        pygame.mixer_music.load('./asset/backgroundaudio.mp3')  # Ou carregue uma música diferente para o nível
        pygame.mixer_music.play(-1)

        clock = pygame.time.Clock()
        spawn_timer = 0
        star_count = 0

        player_instance = next((e for e in self.entity_list if isinstance(e, Player)), None)
        if player_instance is None:
            print("ERRO: Player não encontrado!")
            pygame.quit()
            sys.exit()

        running = True
        while running:
            # Processamento de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Atualização do jogo
            spawn_timer += 1
            if spawn_timer >= 85:  # 3 segundos
                self._spawn_wave()
                spawn_timer = 0

            # Movimento e colisões
            for ent in self.entity_list:
                ent.move()

            player_instance.update()

            # Verifica colisões
            for entity in self.entity_list[:]:
                if entity.rect.colliderect(player_instance.rect):
                    if isinstance(entity, Enemy) and not player_instance.invincible:
                        if player_instance.take_damage():
                            # Só termina o jogo na 3ª colisão
                            print("Game Over!")
                            return "GAME_OVER"
                        entity.kill()

                    elif isinstance(entity, Star):
                        star_count += 1
                        if player_instance.sound_collect:
                            player_instance.sound_collect.play()
                        self.entity_list.remove(entity)

            # Renderização
            self.window.fill((0, 0, 0))  # Limpa a tela
            for ent in self.entity_list:
                if ent == player_instance and player_instance.invincible:
                    # Piscar quando invencível
                    if pygame.time.get_ticks() % 200 < 100:  # Pisca a cada 100ms
                        self.window.blit(ent.surf, ent.rect)
                else:
                    self.window.blit(ent.surf, ent.rect)

            for ent in self.entity_list:
                if hasattr(ent, 'surf') and hasattr(ent, 'rect'):
                    self.window.blit(ent.surf, ent.rect)

            # Mostra HUD
            self.show_star_count(star_count)
            self.level_text(24, f"Vidas: {player_instance.health}", COLOR_WHITE, (10, 10))
            self.level_text(24, f"Vidas: {player_instance.health}/{player_instance.max_health}", COLOR_WHITE, (10, 10))
            pygame.display.flip()
            clock.tick(60)

        return "GAME_OVER"

        # Spawn de inimigos e estrelas
        spawn_timer += 1
        if spawn_timer >= spawn_interval:
            self._spawn_wave()
            spawn_timer = 0

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def _spawn_wave(self):
        # Divide a tela em 4 slots verticais
        slots = [i * (WIN_HEIGHT // 4) + 50 for i in range(4)]
        random.shuffle(slots)

        # 3 inimigos
        enemy_positions = slots[:3]
        for y in enemy_positions:
            self.entity_list.append(EntityFactory.get_entity('Enemy', (WIN_WIDTH + 100, y))[0])

        # 1 estrela garantida em posição diferente
        possible_star_positions = [pos for pos in slots if pos not in enemy_positions]
        star_pos = random.choice(possible_star_positions) if possible_star_positions else slots[3]
        self.entity_list.append(EntityFactory.get_entity('Star', (WIN_WIDTH + 100, star_pos))[0])

    def show_star_count(self, star_count: int):
        self.level_text(24, f"Estrelas: {star_count}", COLOR_WHITE, (WIN_WIDTH - 150, 20))

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font = pygame.font.SysFont('Comic Sans MS', size=text_size)
        text_surf = text_font.render(text, True, text_color).convert_alpha()
        text_rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)