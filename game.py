import sys
import random
from math import ceil

import pygame

from projectiles.laser import Laser
from ships.enemy import Enemy
from ships.player import Player


class Game:
    FRAME_RATE = 60
    COLORS = {'white': (255, 255, 255)}

    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.bg = pygame.transform.scale(pygame.image.load('assets/bg.png'), (self.width, self.height))
        self.window = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        pygame.font.init()
        self.font = 'comicsans'
        self.big_font = pygame.font.SysFont(self.font, 72)
        self.med_font = pygame.font.SysFont(self.font, 36)
        self.small_font = pygame.font.SysFont(self.font, 18)

        self.player = None
        self.enemies = []
        self.lasers = {'player': [], 'enemy': []}
        self.level = 0
        self.enemy_increment = 2
        # Full percentage, chance enemy will not shoot
        self.enemy_shoot_chance = 99

    def main_menu(self):
        menu_font = self.small_font.render('Press any key to start', True, self.COLORS['white'])
        instructions_font = self.med_font.render(
            'Use wasd keys to move and space bar to shoot',
            True,
            self.COLORS['white']
        )

        while True:
            self.window.blit(self.bg, (0, 0))
            self.window.blit(
                instructions_font,
                (
                    (self.width / 2) - (instructions_font.get_width() / 2),
                    (self.height / 2) - (instructions_font.get_height() / 2)
                )
            )
            self.window.blit(
                menu_font,
                ((self.width / 2) - (menu_font.get_width() / 2), (self.height / 2) + instructions_font.get_height())
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.game()

            pygame.display.update()

    def game(self):
        self.player = Player((self.width / 2 - 25), (self.height - 100))
        while True:
            self.clock.tick(self.FRAME_RATE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            if len(self.enemies) == 0:
                self.level += 1
                self.add_enemies()

            keys = pygame.key.get_pressed()
            self.check_player_inputs(keys)
            self.write()

    def add_enemies(self):
        num_of_enemies = self.enemy_increment * ceil(self.level / 2)
        for i in range(0, num_of_enemies):
            enemy = Enemy(-10000, -10000)
            enemy.x = random.randint(0, self.width - enemy.get_width())
            enemy.y = random.randint(-100 * num_of_enemies, -100)
            self.enemies.append(enemy)

    def check_player_inputs(self, keys):
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and 0 < (self.player.y + self.player.velocity):
            self.player.y -= self.player.velocity
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) \
                and self.height > ((self.player.y + self.player.get_height()) + self.player.velocity):
            self.player.y += self.player.velocity
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and 0 < (self.player.x + self.player.velocity):
            self.player.x -= self.player.velocity
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) \
                and self.width > ((self.player.x + self.player.get_width()) + self.player.velocity):
            self.player.x += self.player.velocity
        if keys[pygame.K_SPACE] and self.player.can_shoot():
            # TODO: Trim up images and get rid of the + 10
            # minus 10 is to get the laser to line up with the center of the ship
            self.lasers['player'].append(Laser(self.player.x + ((self.player.get_width() / 2) - 10), self.player.y))

    def write(self):
        self.window.blit(self.bg, (0, 0))
        level_font = self.small_font.render('Level: {level}'.format(level=self.level), True, self.COLORS['white'])
        self.window.blit(level_font, (self.width - (level_font.get_width() + 10), 10))

        for (laser_group, lasers) in self.lasers.items():
            for laser in lasers:
                if laser_group == 'player':
                    if (laser.y + laser.get_height()) < 0:
                        self.lasers['player'].remove(laser)

                    laser.move('up')
                elif laser_group == 'enemy':
                    if laser.y > self.height:
                        self.lasers['enemy'].remove(laser)

                    laser.move('down')
                laser.write(self.window)

        for enemy in self.enemies:
            if enemy.y > self.height:
                self.enemies.remove(enemy)
            else:
                if random.randint(0, 100) > self.enemy_shoot_chance and enemy.can_shoot():
                    # TODO get rid of the minus 10 by trimming enemy ships down
                    self.lasers['enemy'].append(Laser(enemy.x + (enemy.get_width() / 2 - 10), enemy.y))
                enemy.move()
                enemy.write(self.window)

        self.player.write(self.window)

        pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.main_menu()
