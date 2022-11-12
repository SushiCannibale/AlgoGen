import pygame as pg
from entity import *
from util import *
from typing import Tuple, List

pg.init()

Vec = pg.Vector2

class Game:
    def __init__(self):
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(Options.SIZE)
        self.is_running = False

        self.group_kirbys = pg.sprite.LayeredUpdates()
        self.group_fuzzys = pg.sprite.LayeredUpdates()
        self.group_tomatoes = pg.sprite.LayeredUpdates()

        self.generation = 0

        for i in range(0, 10):
            uid, rx, ry = i, randint(Options.FUZZY_SIZE, self.screen.get_width() - Options.FUZZY_SIZE), randint(Options.FUZZY_SIZE, self.screen.get_height()) - Options.FUZZY_SIZE
            self.fuzzy = Fuzzy(self.group_fuzzys, self, rx, ry)
            print(rx, " - ", ry)

        self.kirby = Kirby(self.group_kirbys, self, self.screen.get_width()//2, self.screen.get_height()//2)
        Tomate(self.group_tomatoes, self.screen, self.screen.get_width()//2 - 50, self.screen.get_height()//2)

        self.all_groups = [self.group_kirbys, self.group_fuzzys, self.group_tomatoes]

    def events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.is_running = False

    def draw(self):
        self.screen.fill((12, 12, 12))

        for group in self.all_groups:
            group.draw(self.screen)
            group.update()

        write(self.screen, f"generation {self.generation}", (10, 10))

    def loop(self):
        self.is_running = True
        while self.is_running:
            self.events()

            self.draw()

            pg.display.flip()

            self.clock.tick(Options.FPS)

game = Game()
game.loop()

pg.quit()

