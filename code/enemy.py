import pygame
from code.const import ENTITY_SPEED
from code.entity import Entity

class Enemy(Entity):
    """Meteor enemy class"""
    def __init__(self, position: tuple):
        super().__init__("meteor", position)
        self.damage = 1  # Damage dealt to player
        self.speed = ENTITY_SPEED['Meteor']
        self.surf = pygame.transform.scale(self.surf, (70, 50))  # Fixed size
        self.rect = self.surf.get_rect(center=position)

    def move(self):
        """Move left across screen"""
        self.rect.centerx -= self.speed
        if self.rect.right <= 0:  # Remove when off-screen
            self.kill()

    def kill(self):
        """Remove enemy from game"""
        if hasattr(self, 'group') and self.group:
            self.group.remove(self)