import pygame
from code.const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION
from code.menu import Menu
from code.level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Space Kitty")

    def run(self):
        while True:
            menu = Menu(self.window)
            menu_return = menu.run()

            # Verifica a opção selecionada
            if menu_return == "EXIT" or menu_return == MENU_OPTION[2]:
                pygame.quit()
                return

            elif menu_return == MENU_OPTION[0]:  # PLAY
                # Para a música do menu
                pygame.mixer_music.stop()

                # Cria e roda o nível
                level = Level(self.window, 'Level', menu_return)
                level_status = level.run()

                # Se o nível terminou (game over), volta ao menu
                if level_status == "GAME_OVER":
                    # Reinicia a música do menu
                    pygame.mixer_music.load('./asset/backgroundaudio.mp3')
                    pygame.mixer_music.play(-1)
                    continue
