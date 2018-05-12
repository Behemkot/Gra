import pygame as g
import sys
from src.player import Player
from src.platform import Platform

class Game(object):
    def __init__(self):
        # CONFIG
        self.resolution = (600, 400)
        self.tps = 60.0
        self.speed = 4
        self.gravity = 1

        # Inicjowanie
        g.init()
        self.screen = g.display.set_mode(self.resolution, g.NOFRAME)

        self.tps_clock = g.time.Clock()
        self.tps_delta = 0.0

        self.player = Player(self)
        self.platform = Platform(self)

    def run(self):
        while True:
            # wydarzenia
            for event in g.event.get():
                if event.type == g.QUIT or (event.type == g.KEYDOWN and event.key == g.K_ESCAPE):
                    sys.exit(0)

            # tiki
            self.tps_delta += self.tps_clock.tick() / 1000.0
            while self.tps_delta > 1 / self.tps:
                self.tps_delta -= 1 / self.tps
                self.update()

            # rysowanie
            self.screen.fill((0, 0, 0))
            self.draw()
            g.display.update()

    def update(self):
        self.player.update()

    def draw(self):
        self.player.draw()
        self.platform.draw()


if __name__ == "__main__":
    game = Game()
    player = Player(game)
    platform = Platform(game)
    game.run()