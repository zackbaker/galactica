import os

import pygame

from ships.base import Base


class Player(Base):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.velocity = 5
        self.laser_img = 'player_laser.png'
        # TODO: Figure this mess out. See if there is a better way
        dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.img = pygame.image.load(os.path.join(dirname, 'assets', 'player_ship.png'))
        self.mask = pygame.mask.from_surface(self.img)
