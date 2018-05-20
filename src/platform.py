import pygame as g
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
    def __init__(self, game):
        self.game = game

        # pierwsza platforma
        position_x = 100
        position_y = 350
        self.width = 300
        self.height = 50

        shape = Bbox(position_x, position_y, self.width, self.height)
        shape.on_collide(chandler)
        super(Platform, self).__init__(position_x, position_y, shape)

        self.static = True

    def update(self, dt):
        pass

    def draw(self):
        self.game.camera.draw(g.draw.rect, (255, 0, 0), self.position, (self.width, self.height))
