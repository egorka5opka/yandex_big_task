import pygame


class Button(pygame.sprite.Sprite):

    def __init__(self, pos, text, *groups):
        super().__init__(*groups)
        font = pygame.font.Font(None, 50)
        self.image = font.render(text, False, (0, 0, 0), (230, 230, 230))
        self.rect = self.image.get_rect().move(*pos)

    def clicked(self, pos):
        return self.rect.collidepoint(*pos)

    def change_text(self, text):
        font = pygame.font.Font(None, 50)
        self.image = font.render(text, False, (0, 0, 0), (230, 230, 230))
        self.rect.width = self.image.get_width()

