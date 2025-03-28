# Game constants and configurations
import pygame

COLOR_BLUE = (37, 51, 117)        # Primary blue color
COLOR_LIGHT_BLUE = (100, 120, 200) # Secondary blue
COLOR_WHITE = (255, 255, 255)      # White color
COLOR_YELLOW = (241, 192, 25)      # Yellow for highlights

# Key controls configuration (both arrows and WASD)
CONTROLS = {
    'up': (pygame.K_UP, pygame.K_w),
    'down': (pygame.K_DOWN, pygame.K_s),
    'left': (pygame.K_LEFT, pygame.K_a),
    'right': (pygame.K_RIGHT, pygame.K_d)
}

# Movement speeds for different entities
ENTITY_SPEED = {
    'BgLevel1': 0.6,  # Background layers
    'BgLevel2': 0.6,
    'BgLevel3': 2,
    'Player': 5,      # Player movement
    'Meteor': 4,      # Enemies
    'Star': 4         # Collectibles
}

# Menu options
MENU_OPTION = ('PLAY', 'SCORE', 'EXIT')

# Scroll speed for score screen
SCROLL_SPEED = 30

# Game window dimensions
WIN_WIDTH = 576
WIN_HEIGHT = 324