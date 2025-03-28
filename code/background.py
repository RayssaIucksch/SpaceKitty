from code.const import WIN_WIDTH, ENTITY_SPEED
from code.entity import Entity

class Background(Entity):
    """Scrolling background layer"""
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

    def move(self):
        """Continuous scrolling effect"""
        self.rect.centerx -= ENTITY_SPEED[self.name]
        if self.rect.right <= 0:  # Reset position when fully scrolled
            self.rect.left = WIN_WIDTH