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
        self.still_img = pygame.image.load(os.path.join(dirname, 'assets', 'player_ship.png'))
        self.move_img = pygame.image.load(os.path.join(dirname, 'assets', 'player_ship_moving.png'))
        self.img = self.still_img
        self.mask = pygame.mask.from_surface(self.img)
        self.full_health = 100
        self.health = 100
        self.is_moving = False

    def draw(self, window):
        super(Player, self).draw(window)
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.get_height(), self.get_width(), 2))
        pygame.draw.rect(
            window,
            (0, 255, 0),
            (self.x, self.y + self.get_height(), self.get_width() * (self.health / self.full_health), 2)
        )

    def hit(self):
        self.health -= 10
