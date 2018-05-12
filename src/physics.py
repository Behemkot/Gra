import itertools
from pygame.math import Vector2

class Bbox(object):
    def __init__(self, x, y, w, h, on_collide=None):
        self.on_collide(on_collide)
        self.position = Vector2(x, y)
        self.w = w
        self.h = h

    def setpos(self, pos):
        self.position = pos

    def collides(self, other):
        if isinstance(other, Bbox):
            return self.position[0] < other.position[0] + other.w \
               and self.position[0] + self.w > other.position[0] \
               and self.position[1] < other.position[1] + other.h \
               and self.position[1] + self.h > other.position[1]
        else:
            return False

    def intersection(self, other):
        x = None
        y = None

        if self.position[0] < other.position[0] + other.w:
            x = self.position[0] - (other.position[0] + other.w)
        if self.position[0] + self.w > other.position[0]:
            x = self.position[0] + self.w - other.position[0]
        if self.position[1] < other.position[1] + other.h:
            y = self.position[1] - (other.position[1] + other.h)
        if self.position[1] + self.h > other.position[1]:
            y = self.position[1] + self.h - other.position[1]

        return (x, y)

    def on_collide(self, callback=None):
        self.collision_begin = callback

class Body(object):
    def __init__(self, x, y, shape, gravity=0, friction=0):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.gravity = Vector2(0, gravity)
        self.friction = friction
        self.shape = shape
        self.static = False

        shape.body = self

    def update(self, dt):
        pass

    def setpos(self, pos=None):
        if pos:
            self.position = pos

        self.shape.setpos(self.position)

    def apply_force(self, force):
        self.acceleration += force

    def collides(self, other):
        return self.shape.collides(other.shape)

    def intersection(self, other):
        return self.shape.intersection(other.shape)

class Collision(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def do(self):
        if self.a.collision_begin:
            self.a.collision_begin(self)

        if self.b.collision_begin:
            self.b.collision_begin(self)

class World(object):
    def __init__(self, bodies=[]):
        self.bodies = bodies

    def add_body(self, body):
        self.bodies.append(body)

    def update(self, dt):
        for body in self.bodies:
            if not body.static:
                body.velocity += (body.acceleration + body.gravity) * dt

                for dim in [0, 1]:
                    body.position[dim] += body.velocity[dim] * dt
                    body.setpos()

                    bodies = iter(other for other in self.bodies if body != other)
                    collisions = iter(Collision(body.shape, other.shape) for other in bodies if body.collides(other))

                    for collision in collisions:
                        collision.do()
                        body.position[dim] -= body.intersection(collision.b.body)[dim]
                        body.velocity[dim] = 0
                        body.setpos()

                body.velocity[0] *= 1.0 - body.friction
                body.acceleration *= 0

                body.update(dt)
