import pygame as g
import sys
import os
import random
from pygame.math import Vector2
from player import Player
from enemy import Enemy
from platform import Platform
from paper import Paper
from physics import World
from camera import Camera

class Game(object):
    def __init__(self):
        # CONFIG
        # OGÓLNY
        self.resolution = (1366, 768)
        self.tps = 60.0
        self.jump_force = 45000
        self.move_speed = 12000
        self.max_speed = 20000
        self.gravity = 1800
        self.time = 120
        self.text_color = (119, 136, 153)  # szary

        # PLATFORMY
        self.platform_width = 300
        self.platform_height = 50
        self.platform_space = 130
        platform_max = (self.resolution[1] % self.platform_space) + 80
        self.platform_range = [self.resolution[1] - self.platform_height, platform_max]

        platform_position = Vector2(100, self.platform_range[0])
        self.last_platform = platform_position

        # WROGOWIE
        self.enemy_chance = 0.5
        self.last_platform_enemy = False

        # NOTATKI
        self.notes_chance = 0.1
        self.last_platform_notes = False

        # Inicjowanie
        g.init()
        self.text_font = g.font.Font(g.font.get_default_font(), 40)
        #self.background = g.image.load(os.path.join('models', 'bground.png'))

        self.screen = g.display.set_mode(self.resolution)
        self.camera = Camera(self.screen, 250 - self.resolution[0] / 2, 0,
                self.resolution[0], self.resolution[1])

        self.tps_clock = g.time.Clock()
        self.tps_delta = 0.0
        self.sec = 0.0

        self.player = Player(self)

        self.world = World()
        self.world.add_body(self.player)
        self.world.add_body(Platform(self, self.last_platform))


    def run(self):
        while True:
            # wydarzenia
            for event in g.event.get():
                if event.type == g.QUIT or (event.type == g.KEYDOWN and event.key == g.K_ESCAPE):
                    sys.exit(0)

            # tiki
            self.tps_delta += self.tps_clock.tick() / 1000.0
            while self.tps_delta > 1 / self.tps:
                self.update(self.tps_delta)
                self.tps_delta -= 1 / self.tps


            # Tło
            #self.screen.blit(self.background, (0, 0))
            self.screen.fill((0, 0, 0))

            # wyswietlane wyniku
            score_text = self.text_font.render("SCORE: " + str(self.player.papers), True, self.text_color)
            self.screen.blit(score_text, (20, 20))

            # wyświetlanie czasu
            time_text = self.text_font.render('TIME: ' + str(self.time), True, self.text_color)
            self.screen.blit(time_text, (self.resolution[0] - 220, 20))

            # wyświetlanie życia
            health_text = self.text_font.render('HP: ' + str(self.player.health), True, self.text_color)
            self.screen.blit(health_text, (self.resolution[0] / 2 - 50, 20))

            self.draw()
            g.display.update()


    def update(self, dt):
        # TIMER
        self.sec += dt
        if self.sec >= 1.0:
            self.time -= 1
            self.sec = 0.0

        # generowanie platform
        if self.camera.position[0] + self.resolution[0] > self.last_platform[0] - self.platform_width:
            self.last_platform[0] += 400
            if self.last_platform[1] > self.platform_range[1] and self.last_platform[1] < self.platform_range[0]:
                pos = random.randint(-1, 1)
                if pos == 0:
                    self.last_platform[0] += 100
                else:
                    self.last_platform[1] += pos*self.platform_space
            elif self.last_platform[1] == self.platform_range[0]:
                #pos = random.randint(0, 1)
                self.last_platform[1] -= self.platform_space
            else:
                #pos = random.randint(0, 1)
                self.last_platform[1] += self.platform_space
            self.world.add_body(Platform(self, self.last_platform))



            # generowanie wrogow
            is_enemy = random.random()
            if self.last_platform_enemy:
                self.enemy_chance = 0.3
            else:
                self.enemy_chance += 0.2

            if is_enemy < self.enemy_chance:
                self.world.add_body(Enemy(self.last_platform[0] + random.randint(20,
                                          self.platform_width - 70),
                                          self.last_platform[1] - 50,
                                          self))
                self.last_platform_enemy = True
            else:
                self.last_platform_enemy = False

            # generowanie notatek
            if self.last_platform_enemy:
                self.notes_chance = 0.3
            elif not self.last_platform_notes:
                self.notes_chance += 0.1

            is_note = random.random()
            if is_note < self.notes_chance:
                self.world.add_body(Paper(self.last_platform[0] + random.randint(20, self.platform_width - 70),
                                          self.last_platform[1] - 50,
                                          self))
                self.notes_chance = 0.0

        self.world.update(dt)

    def draw(self):
        for obj in self.world.bodies:
            obj.draw()


if __name__ == "__main__":
    game = Game()
    game.run()
