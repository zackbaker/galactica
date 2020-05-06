import os

import pygame

from ships.base import Base


class Enemy(Base):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.velocity = 1
        dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.img = pygame.image.load(os.path.join(dirname, 'assets', 'enemy_ship.png'))

    def move(self):
        self.y += self.velocity
