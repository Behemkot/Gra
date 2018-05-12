import pygame as g
import sys
from player import Player
from physics import World


class Game(object):
    def __init__(self):
        # CONFIG
        self.resolution = (600, 400)
        self.tps = 60.0
        self.jump_force = 1
        self.move_speed = 1
        self.max_speed = 1
        self.gravity = 1

        # Inicjowanie
        g.init()
        self.screen = g.display.set_mode(self.resolution, g.NOFRAME)

        self.tps_clock = g.time.Clock()
        self.tps_delta = 0.0

        self.player = Player(self)

        self.world = World()
        self.world.add_body(self.player)

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
        self.world.update(1)

    def draw(self):
        self.player.draw()


if __name__ == "__main__":
    game = Game()
    game.run()
