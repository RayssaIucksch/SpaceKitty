import pygame
from code.const import ENTITY_SPEED, WIN_WIDTH
from code.entity import Entity

class Star(Entity):
    """Collectible star item"""
    def __init__(self, position: tuple):
        super().__init__("star", position)
        self.speed = ENTITY_SPEED['Star']
        self.surf = pygame.transform.scale(self.surf, (30, 40))  # Slightly smaller than meteors
        self.rect = self.surf.get_rect(center=position)

    def move(self):
        """Move left like enemies"""
        self.rect.centerx -= self.speed
        if self.rect.right < 0:  # Remove when off-screen
            self.remove()

    def remove(self):
        """Clean up when collected or off-screen"""
        if hasattr(self, 'game'):
            self.game.entity_list.remove(self)