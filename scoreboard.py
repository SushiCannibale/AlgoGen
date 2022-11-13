import pygame as pg
from util import *

class Scoreboard:
    """
    Tableau de scores quand tous les kirbys sont morts.
    Affiche en haut le meilleur de na génération, et en bas le moins bon.
    """
    def __init__(self, main_screen:pg.surface.Surface):
        self.main_screen = main_screen

        self.screen = pg.Surface(main_screen.get_size(), pg.SRCALPHA) # not linked to the main game's screen
        self.screen.fill((12, 12, 12, 220))

        self.individuals: list[pg.sprite.Sprite] = []
        self.sorted = False

    def clear(self):
        self.individuals = []

    def add(self, obj: pg.sprite.Sprite):
        self.individuals.append(obj)

    def draw(self):
        self.main_screen.blit(self.screen, (0, 0))

    """
    Le meilleur kirby prend la position <0> et le moins bon <length-1>
    """
    def sort_by_time_lived(self):
        self.individuals.sort(key=lambda kirby: kirby.time_lived, reverse=True)
        self.sorted = True

    # TODO : writing scores
    def write_score(self):
        if not self.sorted:
            self.sort_by_time_lived()

        for i in range(len(self.individuals)):
            kirby = self.individuals[i]

            self.screen.blit(kirby.image, (20, 50 + kirby.size*i))
            write(self.screen, f"fitness {kirby.time_lived}", (20 + kirby.size + 10, 50 + kirby.size*i + kirby.size//2))
        self.draw()




