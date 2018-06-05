import pygame as g
import random
from pygame.math import Vector2
from physics import Body
from physics import Bbox


class Enemy(Body):
    def __init__(self, x, y, game):
        self.game = game
        self.width = 50
        self.height = 50

        self.on_ground = False

        dir = random.randint(0, 1)
        self.moving = dir

        shape = Bbox(x, y, self.width, self.height)
        super(Enemy, self).__init__(x, y, shape, self.game.gravity, 0.8)

    def move(self):
        self.apply_force(Vector2(self.moving * self.game.move_speed, 0))

    def bounds(self):
        if self.platform:
            return (self.platform.position[0],
                    self.platform.position[0] + self.platform.width - self.width)

    def update(self, dt):
        if abs(self.moving) < 1.0:
            if self.moving < 0:
                self.moving -= 1.5 * dt
            else:
                self.moving += 1.5 * dt

        if self.platform:
            (lo, hi) = self.bounds()
            if self.position[0] < lo and self.moving < 0:
                self.moving = 0.05
            if self.position[0] > hi and self.moving > 0:
                self.moving = -0.05
            self.move()

        if self.velocity[0] > self.game.max_speed:
            self.velocity[0] = self.game.max_speed
        if self.velocity[0] < -self.game.max_speed:
            self.velocity[0] = -self.game.max_speed

    def draw(self):
        self.game.camera.draw(g.draw.ellipse, (191, 0, 255), self.position, (self.width, self.height))
