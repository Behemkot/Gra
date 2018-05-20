import pygame as g
from pygame.math import Vector2
from physics import Body
from physics import Bbox
from player import Player
from enemy import Enemy


def chandler(collision):
    if isinstance(collision.a.body, Player):
        collision.a.body.on_ground = True
    elif isinstance(collision.b.body, Player):
        collision.b.body.on_ground = True

    if isinstance(collision.a.body, Enemy):
        collision.a.body.platform = collision.b.body
    elif isinstance(collision.b.body, Enemy):
        collision.b.body.platform = collision.a.body

class Platform(Body):
    def __init__(self, game, pos):
        self.game = game
        self.position = pos
        self.width = game.platform_width
        self.heigth = game.platform_height

        shape = Bbox(self.position[0], self.position[1], self.width, self.height)
        shape.on_collide(chandler)
        super(Platform, self).__init__(self.position[0], self.position[1], shape)

        self.static = True

    def update(self, dt):
        pass

    def draw(self):
        self.game.camera.draw(g.draw.rect, (255, 0, 0), self.position, (self.width, self.height))
