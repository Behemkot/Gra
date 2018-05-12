import pygame as g


class Platform(object):
    def __init__(self, game, player):
        self.game = game
        self.player = player

        # pierwsza platforma
        self.position_x = 500
        self.position_y = self.player.position_y + 30

    def update(self):
        pass

    def draw(self):
        box = g.Rect(self.position_x, self.position_y, 10, 50)
        g.draw.rect(self.game.screen, (255, 0, 0), box)


