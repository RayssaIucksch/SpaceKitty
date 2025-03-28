import pygame
from code.const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION
from code.menu import Menu
from code.level import Level


class Game:
    """Main game controller"""

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Space Kitty")

    def run(self):
        """Main game loop"""
        while True:
            menu = Menu(self.window)
            menu_return = menu.run()

            # Handle menu selection
            if menu_return == "EXIT" or menu_return == MENU_OPTION[2]:
                pygame.quit()
                return

            elif menu_return == MENU_OPTION[0]:  # PLAY
                pygame.mixer_music.stop()  # Stop menu music

                # Create and run level
                level = Level(self.window, 'Level', menu_return)
                level_status = level.run()

                # Return to menu after game over
                if level_status == "GAME_OVER":
                    pygame.mixer_music.load('./asset/backgroundaudio.mp3')
                    pygame.mixer_music.play(-1)  # Restart menu music
                    continue