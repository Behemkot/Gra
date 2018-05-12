import pygame as g
from pygame.math import Vector2


class Player(object):
    def __init__(self, game):
        self.game = game
        self.position_x = self.game.resolution[0]/2 - 25
        self.position_y = 350 - 50
        self.position = Vector2(self.position_x, self.position_y)

        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)

    def jump(self):

        self.acceleration += Vector2(0, -self.game.speed)

    def move_left(self):
        self.game.platform.position_x += 2*self.game.speed

    def move_right(self):
        self.game.platform.position_x -= 2*self.game.speed

    def update(self):

        # Input
        pressed = g.key.get_pressed()
        if pressed[g.K_w]:
            self.jump()
        if pressed[g.K_a]:
            self.move_left()
        if pressed[g.K_d]:
            self.move_right()


        # Fizyka
        self.velocity *= 0.8
        if self.position[1] < self.position_y:
            self.velocity += Vector2(0, self.game.gravity)
        self.velocity += self.acceleration
        self.position += self.velocity
        self.acceleration *= 0

    def draw(self):
        box = g.Rect(self.position[0], self.position[1], 50, 50)
        g.draw.ellipse(self.game.screen, (0, 255, 0), box)
