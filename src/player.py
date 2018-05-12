import pygame as g
from pygame.math import Vector2
from src.physics import Body


class Player(Body):
    def __init__(self, game):
        self.game = game
        self.position_x = self.game.resolution[0]/2 - 25
        self.position_y = 350 - 50

        self.on_ground = False

        super(Player, self).__init__(self.position_x, self.position_y, [], self.game.gravity, 0.8)

    def jump(self):
        if self.on_ground:
            self.apply_force(Vector2(0, -self.game.jump_force))
            self.on_ground = False

    def move_left(self):
        self.apply_force(Vector2(-self.game.jump_force, 0))

    def move_right(self):
        self.apply_force(Vector2(self.game.jump_force, 0))

    def update(self, dt):
        # Input
        pressed = g.key.get_pressed()
        if pressed[g.K_w]:
            self.jump()
        if pressed[g.K_a]:
            self.move_left()
        if pressed[g.K_d]:
            self.move_right()

        super(Player, self).update(1)

    def draw(self):
        box = g.Rect(self.position[0], self.position[1], 50, 50)
        g.draw.ellipse(self.game.screen, (0, 255, 0), box)
