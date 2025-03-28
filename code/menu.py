import pygame
import pygame.image
from pygame.font import Font
from pygame.rect import Rect
from pygame.surface import Surface
from code.const import WIN_WIDTH, MENU_OPTION, COLOR_WHITE, COLOR_YELLOW


class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./asset/MenuBG.png').convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)
        self.score_screen = None

    def run(self):
        menu_option = 0
        pygame.mixer_music.load('./asset/backgroundaudio.mp3')
        pygame.mixer_music.play(-1)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "EXIT"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        menu_option = (menu_option + 1) % len(MENU_OPTION)
                    elif event.key == pygame.K_UP:
                        menu_option = (menu_option - 1) % len(MENU_OPTION)
                    elif event.key == pygame.K_RETURN:
                        pygame.time.delay(200)

                        if MENU_OPTION[menu_option] == "SCORE":
                            from code.score_screen import ScoreScreen
                            score_screen = ScoreScreen(self.window)
                            result = score_screen.run()

                            if result == "EXIT":
                                return "EXIT"

                            pygame.mixer_music.play(-1)
                            continue

                        return MENU_OPTION[menu_option]

            self.window.blit(self.surf, self.rect)

            for i, option in enumerate(MENU_OPTION):
                color = COLOR_YELLOW if i == menu_option else COLOR_WHITE
                self.menu_text(25, option, color, (WIN_WIDTH / 2, 220 + 30 * i))

            pygame.display.flip()

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont('Open Sans', size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)