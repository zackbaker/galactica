import os

import pygame


class Laser:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 2
        dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.img = pygame.image.load(os.path.join(dirname, 'assets', 'player_laser.png'))

    def move(self, direction):
        if direction == 'up':
            self.y -= self.velocity
        elif direction == 'down':
            self.y += self.velocity

    def write(self, window):
        window.blit(self.img, (self.x, self.y))
