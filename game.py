import sys
import random
from math import ceil

import pygame

from projectiles.laser import Laser
from ships.enemy import Enemy
from ships.player import Player


class Game:
    FRAME_RATE = 60
    COLORS = {'white': (255, 255, 255), 'red': (255, 0, 0)}

    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Space Invaders')

        self.bg = pygame.transform.scale(pygame.image.load('assets/bg.png'), (self.width, self.height))
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
        self.score = 0
        self.enemy_increment = 2
        # Full percentage, chance enemy will not shoot
        self.enemy_shoot_chance = .04

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
                    break

            pygame.display.update()

    def game_over(self):
        score_font = self.big_font.render('Score: {score}'.format(score=self.score), True, self.COLORS['white'])
        score_font_y = (self.height / 2) - (score_font.get_height() / 2)
        game_over_font = self.big_font.render('GAME OVER', True, self.COLORS['red'])
        instructions_font = self.small_font.render('Press enter to replay', True, self.COLORS['white'])

        while True:
            self.window.blit(self.bg, (0, 0))
            self.window.blit(game_over_font, ((self.width / 2) - (game_over_font.get_width() / 2), 10))
            self.window.blit(
                score_font,
                ((self.width / 2) - (score_font.get_width() / 2), score_font_y)
            )
            self.window.blit(
                instructions_font,
                ((self.width / 2) - (instructions_font.get_width() / 2), score_font_y + score_font.get_height() + 10)
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.score = 0
                    self.level = 0
                    self.game()
                    break

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

            for laser in self.lasers['player']:
                for enemy in self.enemies:
                    if self.check_collision(laser, enemy):
                        self.lasers['player'].remove(laser)
                        self.enemies.remove(enemy)
                        self.score += 1

            for laser in self.lasers['enemy']:
                if self.check_collision(self.player, laser):
                    self.lasers['enemy'].remove(laser)
                    self.player.hit()

            for enemy in self.enemies:
                if self.check_collision(self.player, enemy):
                    self.enemies.remove(enemy)
                    self.player.hit()
                    self.score += 1

            if self.player.health <= 0:
                self.game_over()
                break

            self.move_lasers()
            self.move_enemies()
            self.enemy_shoot()

            keys = pygame.key.get_pressed()
            self.check_player_inputs(keys)
            self.draw()

    def add_enemies(self):
        num_of_enemies = self.enemy_increment * ceil(self.level / 2)
        for i in range(0, num_of_enemies):
            enemy = Enemy(-10000, -10000)
            enemy.x = random.randint(0, self.width - enemy.get_width())
            enemy.y = random.randint(-100 * num_of_enemies, -100)
            self.enemies.append(enemy)

    def move_lasers(self):
        for (laser_group, lasers) in self.lasers.items():
            for laser in lasers:
                if (laser.y + laser.get_height()) < 0 or laser.y > self.height:
                    self.lasers[laser_group].remove(laser)

                if laser_group == 'player':
                    laser.move('up')
                elif laser_group == 'enemy':
                    laser.move('down')

    def check_collision(self, obj1, obj2):
        offset_x = round(obj2.x - obj1.x)
        offset_y = round(obj2.y - obj1.y)
        intersect = obj1.mask.overlap(obj2.mask, (offset_x, offset_y))
        if intersect is None:
            return False
        else:
            return True

    def move_enemies(self):
        for enemy in self.enemies:
            if enemy.y > self.height:
                self.enemies.remove(enemy)
            else:
                enemy.move()

    def enemy_shoot(self):
        for enemy in self.enemies:
            if (random.random() + random.random()) / 2 < self.enemy_shoot_chance and enemy.can_shoot():
                self.lasers['enemy'].append(Laser(
                    enemy.x + (enemy.get_width() / 2) - 10,
                    enemy.y + enemy.get_height(),
                    enemy.laser_img
                ))

    def check_player_inputs(self, keys):
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and 0 < (self.player.y + self.player.velocity):
            self.player.y -= self.player.velocity
            self.player.img = self.player.move_img
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) \
                and self.height > ((self.player.y + self.player.get_height()) + self.player.velocity):
            self.player.y += self.player.velocity
            self.player.img = self.player.move_img
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and 0 < (self.player.x + self.player.velocity):
            self.player.x -= self.player.velocity
            self.player.img = self.player.move_img
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) \
                and self.width > ((self.player.x + self.player.get_width()) + self.player.velocity):
            self.player.x += self.player.velocity
            self.player.img = self.player.move_img
        if keys[pygame.K_SPACE] and self.player.can_shoot():
            # TODO: Trim up images and get rid of the + 10
            # minus 10 is to get the laser to line up with the center of the ship
            self.lasers['player'].append(
                Laser(self.player.x + ((self.player.get_width() / 2) - 10), self.player.y, self.player.laser_img)
            )

        if not keys[pygame.K_w] and not keys[pygame.K_UP]:
            self.player.img = self.player.still_img

    def draw(self):
        self.window.blit(self.bg, (0, 0))

        level_font = self.small_font.render('Level: {level}'.format(level=self.level), True, self.COLORS['white'])
        self.window.blit(level_font, (self.width - (level_font.get_width() + 10), 10))

        score_font = self.small_font.render('Score: {score}'.format(score=self.score), True, self.COLORS['white'])
        self.window.blit(score_font, (10, 10))

        for (laser_group, lasers) in self.lasers.items():
            for laser in lasers:
                laser.draw(self.window)

        for enemy in self.enemies:
            enemy.draw(self.window)

        self.player.draw(self.window)

        pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.main_menu()
