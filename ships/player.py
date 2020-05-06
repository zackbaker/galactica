import os

import pygame

from ships.base import Base


class Player(Base):
    def __init__(self, x, y):
        super().__init__(x, y)
        # TODO: Figure this mess out. See if there is a better way
        dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.img = pygame.image.load(os.path.join(dirname, 'assets', 'player_ship.png'))
