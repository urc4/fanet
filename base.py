import pygame
from utils import BLACK


class Base:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def draw(self, screen):
        """Draw the base as a square on the screen."""
        top_left_x = self.x - self.size // 2
        top_left_y = self.y - self.size // 2
        pygame.draw.rect(screen, BLACK, (top_left_x, top_left_y, self.size, self.size))
