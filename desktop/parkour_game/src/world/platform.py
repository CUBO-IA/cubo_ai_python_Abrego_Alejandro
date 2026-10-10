import pygame


class Platform:

    def __init__(self, x, y, width, height):

        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

    def draw(self, screen, camera):

        position = camera.apply(self.rect)

        pygame.draw.rect(
            screen,
            (80, 85, 95),
            position
        )
