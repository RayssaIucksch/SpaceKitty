import pygame
from pygame.font import Font
from code.const import WIN_WIDTH, WIN_HEIGHT, COLOR_WHITE, SCROLL_SPEED, COLOR_BLUE, COLOR_LIGHT_BLUE, CONTROLS
from code.database import get_top_scores


class ScoreScreen:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./asset/scoreBG.png').convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)
        self.scroll_offset = 0
        self.max_offset = 0

        self.up_keys = CONTROLS['up']
        self.down_keys = CONTROLS['down']

        self.table_area = pygame.Rect(
            WIN_WIDTH // 6,
            150,
            WIN_WIDTH * 2 // 3,
            95
        )

    def score_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple, bold=False):
        text_font = pygame.font.SysFont('Open Sans', size=text_size, bold=bold)
        text_surf = text_font.render(text, True, text_color).convert_alpha()
        text_rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(text_surf, text_rect)

    def format_date(self, date_str):
        if isinstance(date_str, str):
            try:
                if '-' in date_str:
                    year, month, day = date_str.split()[0].split('-')
                else:
                    day, month, year = date_str.split()[0].split('/')
                return f"{day.zfill(2)}/{month.zfill(2)}/{year[-2:]}"
            except:
                return date_str[:8]
        return date_str

    def run(self):
        pygame.mixer_music.stop()
        scores = get_top_scores()

        if not scores:
            self.window.blit(self.surf, self.rect)
            self.score_text(24, "Nenhuma partida registrada ainda", COLOR_WHITE,
                            (WIN_WIDTH // 4, WIN_HEIGHT // 2))
            self.score_text(18, "Pressione ESC ou ENTER para voltar", COLOR_WHITE,
                            (WIN_WIDTH // 2 - 150, WIN_HEIGHT - 50))
            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return "EXIT"
                    if event.type == pygame.KEYDOWN:
                        if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                            return "MENU"
            return "MENU"

        col_widths = [40, 140, 60, 100]
        col_spacing = 15
        row_height = 35

        visible_rows = self.table_area.height // row_height
        self.max_offset = max(0, len(scores) * row_height - self.table_area.height)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "EXIT"
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                        return "MENU"
                    if event.key in self.down_keys:
                        self.scroll_offset = min(self.scroll_offset + SCROLL_SPEED, self.max_offset)
                    if event.key in self.up_keys:
                        self.scroll_offset = max(self.scroll_offset - SCROLL_SPEED, 0)

            self.window.blit(self.surf, self.rect)

            headers = ["POS", "PLAYER", "SCORE", "DATE"]
            x_pos = self.table_area.x

            for header, width in zip(headers, col_widths):
                if header == "SCORE":
                    self.score_text(26, header, COLOR_LIGHT_BLUE, (x_pos - 10, 120), bold=True)
                else:
                    self.score_text(26, header, COLOR_LIGHT_BLUE, (x_pos, 120), bold=True)
                x_pos += width + col_spacing

            self.window.set_clip(self.table_area)

            for i, (name, stars, date) in enumerate(scores, 1):
                entry_y = self.table_area.y + (i - 1) * row_height - self.scroll_offset

                if self.table_area.y <= entry_y <= self.table_area.y + self.table_area.height:
                    items = [
                        f"{i}.",
                        name[:12].ljust(12),
                        str(stars).rjust(3),
                        self.format_date(date)
                    ]

                    x_pos = self.table_area.x
                    for item, width in zip(items, col_widths):
                        self.score_text(22, item, COLOR_WHITE, (x_pos, entry_y))
                        x_pos += width + col_spacing

            self.window.set_clip(None)

            instruction = "Pressione ESC ou ENTER para voltar"
            instr_width = pygame.font.SysFont('Open Sans', 20).size(instruction)[0]
            self.score_text(20, instruction, COLOR_WHITE, (WIN_WIDTH // 2 - instr_width // 2, WIN_HEIGHT - 50))

            pygame.display.flip()

        return "MENU"