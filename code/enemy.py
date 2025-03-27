#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from code.const import ENTITY_SPEED
from code.entity import Entity


class Enemy(Entity):
        def __init__(self, position: tuple):
            super().__init__("meteor", position)
            self.damage = 1
            self.speed = ENTITY_SPEED['Meteor']

            self.surf = pygame.transform.scale(self.surf, (50, 50))  # Tamanho fixo
            self.rect = self.surf.get_rect(center=position)


        def move(self, ):
            self.rect.centerx -= self.speed
            if self.rect.right <= 0:
                self.kill()

        def kill(self):
            if hasattr(self, 'group') and self.group:
                self.group.remove(self)
                pass
