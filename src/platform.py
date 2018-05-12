import pygame as g


class Platform(object):
    def __init__(self, game):
        self.game = game

        # pierwsza platforma
        self.position_x = 500
        self.position_y = self.game.player.position_y - 60

    def update(self):
        pass

    def draw(self):
        box = g.Rect(self.position_x, self.position_y, 100, 50)
        g.draw.rect(self.game.screen, (255, 0, 0), box)


