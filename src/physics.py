import itertools
from pygame.math import Vector2

class Shape(object):
    def __init__(self, on_collide=None):
        self.on_collide(on_collide)

    def collides(other):
        return False

    def setpos(pos):
        pass

    def on_collide(self, callback=None):
        self.collision_begin = callback

    def add_collision(self, other):
        self.colliding.append(other)

class Rectangle(Shape):
    def __init__(self, x, y, w, h, on_collide=None):
        super(Rectangle, self).__init__(on_collide)
        self.position = Vector2(x, y)
        self.w = w
        self.h = h

    def setpos(self, pos):
        self.position = pos

    def collides(self, other):
        if isinstance(other, Rectangle):
            return self.position[0] < other.position[0] + other.w \
               and self.position[0] + self.w > other.position[0] \
               and self.position[1] < other.position[1] + other.h \
               and self.position[1] + self.w > other.position[1]
        else:
            return False

class Body(object):
    def __init__(self, x, y, shapes, gravity=0, friction=0):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.gravity = Vector2(0, gravity)
        self.friction = friction
        self.shapes = shapes
        self.static = False

        for shape in shapes:
            shape.body = self

    def update(self, dt):
        pass

    def setpos(self, pos=None):
        if pos:
            self.position = pos

        for shape in self.shapes:
            shape.setpos(self.position)

    def apply_force(self, force):
        self.acceleration += force

    def collisions(self, other):
        if isinstance(other, Body):
            pairs = itertools.product(self.shapes, other.shapes)
            return iter(Collision(a, b) for (a, b) in pairs if a.collides(b))
        else:
            return iter()

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
            body.velocity += (body.acceleration + body.gravity) * dt

            for dim in [0, 1]:
                body.position[dim] += body.velocity[dim] * dt
                body.setpos()

                collisions = iter(body.collisions(other) for other in self.bodies if body != other)
                collides = False

                for cs in collisions:
                    for collision in cs:
                        collision.do()
                        collides = True

                if collides:
                    body.position[dim] -= body.velocity[dim] * dt
                    body.setpos()

            body.velocity[0] *= 1.0 - body.friction
            body.acceleration *= 0

            body.update(dt)
