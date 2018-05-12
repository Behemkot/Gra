import pygame as g
from pygame.math import Vector2

class Camera(object):
    def __init__(self, screen, x, y, w=1, h=1):
        self.position = Vector2(x, y)
        self.screen = screen

    def translate(self, x, y):
        self.position += Vector2(x, y)

    def draw(self, func, color, pos, size):
        box = g.Rect(pos[0] - self.position[0], pos[1] - self.position[1],
                     size[0], size[1])
        func(self.screen, color, box)
