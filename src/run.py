import pygame as g
import sys
import random
from pygame.math import Vector2
from player import Player
from enemy import Enemy
from platform import Platform
from physics import World
from camera import Camera

class Game(object):
    def __init__(self):
        # CONFIG
        self.resolution = (1366, 768)
        self.tps = 60.0
        self.jump_force = 45000
        self.move_speed = 12000
        self.max_speed = 20000
        self.gravity = 1800

        self.platform_width = 300
        self.platform_height = 50
        self.platform_space = 130
        platform_max = (self.resolution[1] % self.platform_space) + 80
        self.platform_range = [self.resolution[1] - self.platform_height, platform_max]

        platform_position = Vector2(100, self.platform_range[0])
        self.last_platform = platform_position

        # Inicjowanie
        g.init()
        self.screen = g.display.set_mode(self.resolution)
        self.camera = Camera(self.screen, 0, 0,
                self.resolution[0], self.resolution[1])

        self.tps_clock = g.time.Clock()
        self.tps_delta = 0.0

        self.player = Player(self)

        self.world = World()
        self.world.add_body(self.player)
        self.world.add_body(Platform(self, self.last_platform))


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
        # generowanie platform
        if self.camera.position[0] + self.resolution[0] > self.last_platform[0] - self.platform_width:
            self.last_platform[0] += 400
            if self.last_platform[1] > self.platform_range[1] and self.last_platform[1] < self.platform_range[0]:
                pos = random.randint(-1, 1)
                if pos == 0:
                    self.last_platform[0] += 100
                else:
                    self.last_platform[1] += pos*self.platform_space
            elif self.last_platform[1] == self.platform_range[0]:
                #pos = random.randint(0, 1)
                self.last_platform[1] -= self.platform_space
            else:
                pos = random.randint(0, 1)
                self.last_platform[1] += self.platform_space
            self.world.add_body(Platform(self, self.last_platform))
            self.world.add_body(Enemy(self.last_platform[0] + 20, self.last_platform[1] - 50, self))

        self.world.update(dt)

    def draw(self):
        for obj in self.world.bodies:
            obj.draw()


if __name__ == "__main__":
    game = Game()
    game.run()
