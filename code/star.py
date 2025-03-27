import pygame

from code.const import ENTITY_SPEED, WIN_WIDTH
from code.entity import Entity


class Star(Entity):
    def __init__(self, position: tuple):
        super().__init__("star", position)
        self.speed = ENTITY_SPEED['Star']
        # Redimensiona para 30x30 (meteoros são 50x50)
        self.surf = pygame.transform.scale(self.surf, (30, 40))
        self.rect = self.surf.get_rect(center=position)

    def move(self):
        self.rect.centerx -= self.speed
        if self.rect.right < 0:
            self.remove()

    def remove(self):
        """Método para remover a estrela da entity_list"""
        if hasattr(self, 'game'):
            self.game.entity_list.remove(self)