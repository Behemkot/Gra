import pygame as g
from pygame.math import Vector2
from physics import Body
from physics import Bbox
from player import Player


def chandler(collision):
    if isinstance(collision.a.body, Player):
        collision.a.body.on_ground = True
    elif isinstance(collision.b.body, Player):
        collision.b.body.on_ground = True

class Platform(Body):
    def __init__(self, game, pos):
        self.game = game
        self.position = pos

        shape = Bbox(self.position[0], self.position[1], self.game.platform_width, self.game.platform_height)
        shape.on_collide(chandler)
        super(Platform, self).__init__(self.position[0], self.position[1], shape)

        self.static = True

    def update(self, dt):
        pass

    def draw(self):
        self.game.camera.draw(g.draw.rect, (255, 0, 0), self.position, (self.game.platform_width, self.game.platform_height))
