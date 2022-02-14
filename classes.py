import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, size, text, *groups):
        super().__init__(*groups)
        self.font = pygame.font.Font(None, 50)
        self.image = pygame.Surface(size)
        self.rect = pygame.Rect(*pos, *size)
        self.change_text(text)

    def clicked(self, pos):
        return self.rect.collidepoint(*pos)

    def change_text(self, text):
        self.image.fill((230, 230, 230))
        text = self.font.render(text, False, (0, 0, 0))
        pos = (self.rect.width - text.get_width()) / 2, (self.rect.height - text.get_height()) / 2
        self.image.blit(text, pos)


class ImageButton(pygame.sprite.Sprite):
    def __init__(self, pos, size, image, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load(image), size)
        self.rect = pygame.Rect(*pos, *size)

    def clicked(self, pos):
        return self.rect.collidepoint(*pos)


class EditText(pygame.sprite.Sprite):
    def __init__(self, pos, size, font_size, *groups):
        super().__init__(*groups)
        self.font = pygame.font.Font(None, font_size)
        self.image = pygame.Surface(size)
        self.image.fill((230, 230, 230))
        self.rect = pygame.Rect(*pos, *size)
        self.text = ""

    def clicked(self, pos):
        return self.rect.collidepoint(*pos)

    def render(self):
        self.image.fill((230, 230, 230))
        text = self.font.render(self.text, False, (0, 0, 0))
        pos = (self.rect.width - text.get_width()) / 2, (self.rect.height - text.get_height()) / 2
        self.image.blit(text, pos)

    def update(self, event, *args):
        if event.type == pygame.TEXTINPUT:
            self.text += event.text
            self.render()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            if self.text:
                self.text = self.text[:-1]
                self.render()
