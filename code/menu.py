import pygame
from pygame.font import Font
from pygame.rect import Rect
from pygame.surface import Surface
from code.const import WIN_WIDTH, MENU_OPTION, COLOR_WHITE, COLOR_YELLOW


class Menu:
    """Main game menu system"""

    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./asset/MenuBG.png').convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)
        self.score_screen = None  # Reference to score screen

    def run(self):
        """Main menu loop"""
        menu_option = 0  # Currently selected option
        pygame.mixer_music.load('./asset/backgroundaudio.mp3')
        pygame.mixer_music.play(-1)  # Loop menu music

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "EXIT"

                if event.type == pygame.KEYDOWN:
                    # Menu navigation
                    if event.key == pygame.K_DOWN:
                        menu_option = (menu_option + 1) % len(MENU_OPTION)
                    elif event.key == pygame.K_UP:
                        menu_option = (menu_option - 1) % len(MENU_OPTION)
                    elif event.key == pygame.K_RETURN:
                        pygame.time.delay(200)  # Small delay for feedback

                        if MENU_OPTION[menu_option] == "SCORE":
                            # Lazy import to avoid circular dependencies
                            from code.score_screen import ScoreScreen
                            score_screen = ScoreScreen(self.window)
                            result = score_screen.run()

                            if result == "EXIT":
                                return "EXIT"

                            # Return to menu with music
                            pygame.mixer_music.play(-1)
                            continue

                        return MENU_OPTION[menu_option]  # Return selected option

            # Render menu
            self.window.blit(self.surf, self.rect)

            # Draw menu options
            for i, option in enumerate(MENU_OPTION):
                # Highlight selected option
                color = COLOR_YELLOW if i == menu_option else COLOR_WHITE
                self.menu_text(25, option, color, (WIN_WIDTH / 2, 220 + 30 * i))

            pygame.display.flip()

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        """Helper method for rendering menu text"""
        text_font: Font = pygame.font.SysFont('Open Sans', size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)