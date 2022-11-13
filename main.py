import pygame as pg
from entity import *
from scoreboard import *
from util import *
from typing import Tuple, List
from random import randint, choice

pg.init()

Vec = pg.Vector2

class Game:
    def __init__(self):
        self.clock = pg.time.Clock()

        # main game screen
        self.screen = pg.display.set_mode(Options.SIZE)
        self.sc_width, self.sc_height = self.screen.get_size()
        
        self.is_running = False

        self.group_kirbys = pg.sprite.LayeredUpdates()
        self.group_fuzzys = pg.sprite.LayeredUpdates()
        self.group_tomatoes = pg.sprite.LayeredUpdates()

        self.generation = 0

        self.scoreboard = Scoreboard(self.screen)

        self.generate_fuzzys(10)
        self.generate_tomatoes(2)
        self.generate_kirbys(8, initial=True)

        self.all_groups = [self.group_kirbys, self.group_fuzzys, self.group_tomatoes]

    def generate_tomatoes(self, n:int):
        for _ in range(n):
            Tomate(self.group_tomatoes, self, randint(Options.TOMATE_SIZE, self.sc_width - Options.TOMATE_SIZE), randint(Options.TOMATE_SIZE, self.sc_height - Options.TOMATE_SIZE))

    def generate_fuzzys(self, n:int):
        for _ in range(n):
            rx, ry = randint(Options.FUZZY_SIZE, self.sc_width - Options.FUZZY_SIZE), randint(Options.FUZZY_SIZE, self.sc_height) - Options.FUZZY_SIZE
            Fuzzy(self.group_fuzzys, self, rx, ry)

    def generate_kirbys(self, n:int, initial:bool):
        if initial:
            lives = randint(Options.MIN_KIRBY_START_HEALTH, Options.MAX_KIRBY_START_HEALTH)
            speed = randint(Options.MIN_KIRBY_START_SPEED, Options.MAX_KIRBY_START_SPEED) / 10
            size = randint(Options.MIN_KIRBY_START_SIZE, Options.MAX_KIRBY_START_SIZE)
            type = choice(["neutral", "tomato", "flee"])

        for _ in range(n):
            Kirby(self.group_kirbys, self, randint(40, self.sc_width - 40), randint(40, self.sc_height - 40), type, start_lives=lives, start_speed=speed, start_size=size)

    def is_everyone_dead(self):
        return len(self.group_kirbys) <= 0

    def events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.is_running = False

            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    self.is_running = False

    def clear_screen(self):
        self.screen.fill((12, 12, 12))

    def group_update(self):
        for group in self.all_groups:
            group.draw(self.screen)
            group.update()

    def draw(self):
        self.clear_screen()
        self.group_update()

        if self.is_everyone_dead():
            self.scoreboard.write_score()
        write(self.screen, f"generation {self.generation}", (10, 10)) # TODO : scoreboard

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

