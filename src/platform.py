import pygame as g
from physics import Body
from physics import Bbox
from player import Player


def chandler(collision):
    if isinstance(collision.a.body, Player):
        collision.a.body.on_ground = True
    elif isinstance(collision.b.body, Player):
        collision.b.body.on_ground = True

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
        box = g.Rect(self.position[0], self.position[1], self.width, self.height)
        g.draw.rect(self.game.screen, (255, 0, 0), box)


