import itertools
from pygame.math import Vector2

class Bbox(object):
    def __init__(self, x, y, w, h, on_collide=None, on_uncollide=None):
        self.on_collide(on_collide, on_uncollide)
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

    def on_collide(self, cb_begin=None, cb_end=None):
        self.collision_begin = cb_begin
        self.collision_end = cb_end

class Body(object):
    def __init__(self, x, y, shape, gravity=0, friction=0):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.gravity = Vector2(0, gravity)
        self.friction = friction
        self.shape = shape
        self.static = False
        self.colliding = {}

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
        self.intersection = a.body.intersection(b.body)
        self.a = a
        self.b = b

    def do_begin(self):
        if self.a.collision_begin:
            self.a.collision_begin(self)

        if self.b.collision_begin:
            self.b.collision_begin(self)

    def do_end(self):
        if self.a.collision_end:
            self.a.collision_end(self)

        if self.b.collision_end:
            self.b.collision_end(self)

class World(object):
    def __init__(self, bodies=[]):
        self.bodies = bodies
        self.kill = []
        self.updating = False

    def add_body(self, body):
        self.bodies.append(body)

    def remove(self, body):
        if not self.updating:
            self.bodies.pop(body)
        else:
            self.kill.append(body)

    def update(self, dt):
        self.updating = True

        for (i, body) in enumerate(self.bodies):
            if not body.static:
                body.velocity += (body.acceleration + body.gravity) * dt

                colliding = {}
                for dim in [0, 1]:
                    body.position[dim] += body.velocity[dim] * dt
                    body.setpos()

                    bodies = iter(other for other in self.bodies if body != other)
                    collisions = iter(Collision(body.shape, other.shape) for other in bodies if body.collides(other))

                    for collision in collisions:
                        other = collision.b.body
                        colliding[other] = True

                        if other not in body.colliding:
                            body.colliding[other] = collision
                            other.colliding[body] = collision
                            collision.do_begin()
                        body.position[dim] -= collision.intersection[dim]
                        body.velocity[dim] = 0
                        body.setpos()

                remove = []
                for other, collision in body.colliding.items():
                    if other not in colliding:
                        collision.do_end()
                        remove.append(other)

                for other in remove:
                    del body.colliding[other]
                    del other.colliding[body]

                body.velocity[0] *= 1.0 - body.friction
                body.acceleration *= 0

                body.update(dt)

        for body in self.kill:
            self.bodies.remove(body)

        self.updating = False
