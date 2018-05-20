import pygame as g
import sys
from player import Player
from enemy import Enemy
from platform import Platform
from physics import World
from camera import Camera

class Game(object):
    def __init__(self):
        # CONFIG
        self.resolution = (600, 400)
        self.tps = 60.0
        self.jump_force = 45000
        self.move_speed = 12000
        self.max_speed = 20000
        self.gravity = 1800

        # Inicjowanie
        g.init()
        self.screen = g.display.set_mode(self.resolution, g.NOFRAME)
        self.camera = Camera(self.screen, 0, 0,
                self.resolution[0], self.resolution[1])

        self.tps_clock = g.time.Clock()
        self.tps_delta = 0.0

        self.player = Player(self)

        self.world = World()
        self.world.add_body(self.player)
        self.world.add_body(Platform(self))
        self.world.add_body(Enemy(120, 300, self))

    def run(self):
        while True:
            # wydarzenia
            for event in g.event.get():
                if event.type == g.QUIT or (event.type == g.KEYDOWN and event.key == g.K_ESCAPE):
                    sys.exit(0)

            # tiki
            self.tps_delta += self.tps_clock.tick() / 1000.0
            while self.tps_delta > 1 / self.tps:
                self.update(self.tps_delta)
                self.tps_delta -= 1 / self.tps

            # rysowanie
            self.screen.fill((0, 0, 0))
            self.draw()
            g.display.update()

    def update(self, dt):
        self.world.update(dt)

    def draw(self):
        for obj in self.world.bodies:
            obj.draw()


if __name__ == "__main__":
    game = Game()
    game.run()
