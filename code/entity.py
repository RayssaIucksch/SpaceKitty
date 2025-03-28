from abc import ABC, abstractmethod
import pygame

class Entity(ABC):
    """Abstract base class for all game entities"""
    def __init__(self, name: str, position: tuple):
        self.name = name
        self.surf = pygame.image.load(f'./asset/{name}.png').convert_alpha()
        self.rect = self.surf.get_rect(left=position[0], top=position[1])
        self.speed = 0  # To be overridden by subclasses

    @abstractmethod
    def move(self):
        """Movement logic to be implemented by subclasses"""
        pass