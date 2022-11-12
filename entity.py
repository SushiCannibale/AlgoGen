import pygame as pg
from random import randint
from abc import abstractproperty
from util import *
Vec2 = pg.Vector2


class EnumBehaviours:
    SHY = "shy"
    BOLD = "bold"
    NEUTRAL = "neutral"

class Entity(pg.sprite.Sprite):
    def __init__(self, group, screen:pg.Surface, x:int, y:int):
        super().__init__(group)
        self.screen = screen
        self.group = group

        self.pos = Vec2(x, y)
        self.size = 0 # /!\ need to be redefined /!\


class LivingEntity(Entity):
    def __init__(self, group, screen:pg.Surface, x:int, y:int):
        super().__init__(group, screen, x, y)
        self.dir = Vec2(randint(-10, 10) / 10, randint(-10, 10) / 10).normalize()
        # peut throw une erreur en tentant de (0, 0).normalize()

    def bounce_border(self):
        if self.pos.x + self.size//2 > self.screen.get_width() or self.pos.x - self.size//2 < 0:
            self.dir.x *= -1
        if self.pos.y + self.size//2 > self.screen.get_height() or self.pos.y - self.size//2 < 0:
            self.dir.y *= -1

    def is_colliding(self, obj):
        return self.image.get_rect().colliderect(obj.get_rect)


class Kirby(LivingEntity):
    """
    Il existe 4 types de comportements (simplifiées)
        - Classique : Cherche à **aller vers la tomate la plus proche** mais **fuis les fuzzys s'ils sont dans son rayon de check**
        - Fuyard : Cherche toujours à **fuire les ennemis** (ne fais pas attention aux tomates)
        - Téméraire : Cherche à **récupérer la tomate la plus prohce de lui** (sans s'occuper des fuzzys)

        - Déviant : Se déplace aléatoirement
    """
    def __init__(self, group, game, sx, sy):
        super().__init__(group, game.screen, sx, sy)

        self.lives = 1
        self.speed = 0.5
        self.size = 40
        self.color = pg.Color(randint(0, 255), randint(0, 255), randint(0, 255))

        self.image = pg.transform.scale(Options.KIRBY, (self.size, self.size))
        self.rect = self.image.get_rect()

        self.fuzzys = game.group_fuzzys.sprites()
        self.tomatoes = game.group_tomatoes.sprites()

        self.check_radius = Options.KIRBY_CHECK_RADIUS
        # rayon d'un cercle à partir duquel le kirby fa faire des checks (fuzzy ou tomate)

    def on_hit(self):
        if self.lives > 0:
            self.lives -= 1
        else:
            self.lives = 0
            self.kill()

    def is_within_radius(self, obj):
        return (self.pos.x - self.check_radius <= obj.pos.x <= self.pos.x + self.check_radius) and \
               (self.pos.y - self.check_radius <= obj.pos.y <= self.pos.y + self.check_radius)

    def draw_radius(self):
        pg.draw.rect(self.screen, (255, 0, 0), pg.Rect(self.pos.x - self.check_radius, self.pos.y - self.check_radius, 2*self.check_radius, 2*self.check_radius), width=1)

    def move(self):
        self.pos += self.dir * self.speed

    def update(self):
        self.draw_radius()
        self.flee()
        self.rect.center = self.pos

    #####################
    ### Conportements ###
    #####################

    def flee_obj(self, obj):
        vec = Vec2(self.pos.x - obj.pos.x, self.pos.y - obj.pos.y)
        self.dir = vec.normalize()

    def target_obj(self, obj):
        vec = Vec2(obj.pos.x - self.pos.x, obj.pos.y - self.pos.y)
        self.dir = vec.normalize()

    def flee(self):
        for fuzzy in self.fuzzys:
            if self.is_within_radius(fuzzy):
                self.flee_obj(fuzzy)

        self.move()

    def target_tomatoes(self):
        for tomato in self.tomatoes:
            if self.is_within_radius(tomato):
                self.target_obj(tomato)
        self.move()


class Fuzzy(LivingEntity):
    """
    Les ennemis des kirbys. Leur point de départ et direction initiale est aléatoire. Ils se baladent selon cette même direction
    pendant toute la partie, rebondissant sur les murs.
    """
    def __init__(self, group, game, sx, sy):
        super().__init__(group, game.screen, sx, sy)
        self.size = Options.FUZZY_SIZE
        self.speed = Options.FUZZY_SPEED

        self.image = pg.transform.scale(Options.FUZZY, (Options.FUZZY_SIZE, Options.FUZZY_SIZE))
        self.rect = self.image.get_rect()

    def move(self):
        self.bounce_border()
        self.pos += self.dir * self.speed

    def update(self):
        self.move()
        self.rect.center = self.pos


"""
Ecris sur le screen les caractéristiques du kirby étudié (speed, lives, size, et fitness)
"""
# TODO
def write_data(kirby:Kirby, screen:pg.surface):
    pass


# TODO
class Tomate(Entity):
    def __init__(self, group, screen, x, y):
        super().__init__(group, screen, x, y)

        self.size = Options.TOMATE_SIZE
        self.image = pg.transform.scale(Options.TOMATE, (self.size, self.size))
        self.rect = self.image.get_rect()

    def on_pickup(self):
        self.kill()

    def update(self):
        if len(self.group) == 0:
            Tomate(self.group, self.screen, randint(Options.TOMATE_SIZE, self.screen.get_width() - Options.TOMATE_SIZE), randint(Options.TOMATE_SIZE, self.screen.get_height() - Options.TOMATE_SIZE))
        self.rect.center = self.pos



