import pygame as g
from pygame.math import Vector2
from physics import Body
from physics import Bbox


class Paper(Body):
    def __init__(self, x, y, game):
        self.game = game
        self.width = 40
        self.height = 50
        self.static = True

        shape = Bbox(x, y, self.width, self.height)
        super(Paper, self).__init__(x, y, shape, self.game.gravity, 0.8)

    def draw(self):
        self.game.camera.draw(g.draw.rect, (222, 222, 222), self.position, (self.width, self.height))
