import pygame

# C
COLOR_BLUE = (37, 51, 117)
COLOR_LIGHT_BLUE = (100, 120, 200)
COLOR_WHITE = (255, 255, 255)
COLOR_YELLOW = (241, 192, 25)

CONTROLS = {
    'up': (pygame.K_UP, pygame.K_w),
    'down': (pygame.K_DOWN, pygame.K_s),
    'left': (pygame.K_LEFT, pygame.K_a),
    'right': (pygame.K_RIGHT, pygame.K_d)
}

# E
ENTITY_SPEED = {
    'BgLevel1': 0.6,
    'BgLevel2': 0.6,
    'BgLevel3': 2,
    'Player': 5,
    'Meteor': 4,
    'Star' : 4
}

# M
MENU_OPTION = ('PLAY',
               'SCORE',
               'EXIT')

#S
SCROLL_SPEED = 30  # Velocidade do scroll

# W
WIN_WIDTH = 576
WIN_HEIGHT = 324
