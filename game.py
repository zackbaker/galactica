import sys

import pygame

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
        self.enemies = None
        self.lasers = None

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

            keys = pygame.key.get_pressed()
            self.check_player_movement(keys)

            self.write()

    def check_player_movement(self, keys):
        if keys[pygame.K_w] and 0 < (self.player.y + self.player.velocity):
            self.player.y -= self.player.velocity
        if keys[pygame.K_s] and self.height > ((self.player.y + self.player.get_height()) + self.player.velocity):
            self.player.y += self.player.velocity
        if keys[pygame.K_a] and 0 < (self.player.x + self.player.velocity):
            self.player.x -= self.player.velocity
        if keys[pygame.K_d] and self.width > ((self.player.x + self.player.get_width()) + self.player.velocity):
            self.player.x += self.player.velocity

    def write(self):
        self.window.blit(self.bg, (0, 0))
        self.player.write(self.window)

        pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.main_menu()
