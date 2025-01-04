from mapa import window
from pygame import *

class ImageButton:
    def __init__(self, x, y, img, img_path):
        self.rect = img.get_rect(topleft=(x, y))
        self.img = img
        self.img_path = img_path

    def draw(self):
        window.blit(self.img, self.rect.topleft)

    def clicked(self, position):
        return self.rect.collidepoint(position)


class Button:
    def __init__(self, x, y, width, height, txt=None, size_txt=22, color_txt=(255, 255, 255),
                 color_rect=(196, 196, 196)):
        self.text = txt
        if txt:
            self.text = font.Font(None, size_txt).render(txt, True, color_txt)
        self.rect = Rect(x, y, width, height)
        self.color_r = color_rect
        self.color_txt = color_txt
        self.textx = self.rect.centerx - self.text.get_rect().width // 2
        self.texty = self.rect.centery - self.text.get_rect().height // 2

    def reset(self):
        draw.rect(window, self.color_r, self.rect, border_radius=10)
        if self.text:
            window.blit(self.text, (self.textx, self.texty))

    def clicked(self, position):
        return self.rect.collidepoint(position)