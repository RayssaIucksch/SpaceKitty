import pygame

# C
COLOR_YELLOW = (241, 192, 25)
COLOR_WHITE = (255, 255, 255)

CONTROLS = {
    'up': (pygame.K_UP, pygame.K_w),
    'down': (pygame.K_DOWN, pygame.K_s),
    'left': (pygame.K_LEFT, pygame.K_a),
    'right': (pygame.K_RIGHT, pygame.K_d)
}

# M
MENU_OPTION = ('PLAY',
               'SCORE',
               'EXIT')

# E
ENTITY_SPEED = {
    'BgLevel1': 0.6,
    'BgLevel2': 0.6,
    'BgLevel3': 2,
    'Player': 5,
    'Meteor': 4,
    'Star' : 4
}

# W
WIN_WIDTH = 576
WIN_HEIGHT = 324
