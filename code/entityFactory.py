import pygame
from code.background import Background
from code.const import WIN_WIDTH
from code.enemy import Enemy
from code.player import Player
from code.star import Star


class EntityFactory:
    """Factory pattern for creating game entities"""

    @staticmethod
    def get_entity(entity_name: str, position=(0, 0), new_size=None):
        """Create entity instances by type"""
        match entity_name:
            case 'BgLevel':
                # Create parallax background layers
                list_bg = []
                for i in range(1, 4):
                    list_bg.append(Background(f'BgLevel{i}', (0, 0)))
                    list_bg.append(Background(f'BgLevel{i}', (WIN_WIDTH, 0)))

                    if new_size:  # Handle custom sizing
                        for bg in list_bg[-2:]:
                            bg.surf = pygame.transform.scale(bg.surf, new_size)
                            bg.rect = bg.surf.get_rect(left=bg.rect.left, top=0)
                return list_bg

            case 'Player':
                return [Player("Player", position, new_size)]

            case 'Enemy':
                enemy = Enemy(position)
                if new_size:  # Allow custom enemy sizes
                    enemy.surf = pygame.transform.scale(enemy.surf, new_size)
                    enemy.rect = enemy.surf.get_rect(center=position)
                return [enemy]

            case 'Star':
                return [Star(position)]