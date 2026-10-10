import pygame

from src.core.settings import WIDTH, HEIGHT


class Camera:

    def __init__(self):

        self.x = 0
        self.y = 0

    def update(self, player):

        target_x = player.rect.centerx - WIDTH // 2
        target_y = player.rect.centery - HEIGHT // 2

        self.x += (target_x - self.x) * 0.10
        self.y += (target_y - self.y) * 0.10

    def apply(self, rect):

        return pygame.Rect(
            rect.x - int(self.x),
            rect.y - int(self.y),
            rect.width,
            rect.height
        )
