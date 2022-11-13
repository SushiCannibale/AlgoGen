import math
import pygame as pg
from random import randint
from abc import abstractproperty
from util import *
Vec2 = pg.Vector2





class Entity(pg.sprite.Sprite):
    def __init__(self, group, game, x:int, y:int):
        super().__init__(group)
        self.game = game
        self.screen:pg.Surface = game.screen
        self.sc_width = self.screen.get_width()
        self.sc_height = self.screen.get_height()

        self.group = group # le group propre à l'entité

        self.pos = Vec2(x, y)
        self.size = 0 # /!\ need to be redefined /!\


class LivingEntity(Entity):
    def __init__(self, group, game, x:int, y:int):
        super().__init__(group, game, x, y)
        self.speed = 0 # /!\ doit être redéfini /!\
        self.dir = Vec2(randint(-10, 10) / 10, randint(-10, 10) / 10).normalize()
        # peut throw une erreur en tentant de (0, 0).normalize()

    def move(self):
        self.pos += self.dir * self.speed

    def bounce_border(self):
        if self.pos.x + self.size//2 >= self.sc_width:
            self.pos.x = self.sc_width - self.size//2
            self.dir.x *= -1

        if self.pos.x - self.size//2 < 0:
            self.pos.x = 0 + self.size//2
            self.dir.x *= -1

        if self.pos.y + self.size//2 > self.sc_height:
            self.pos.y = self.sc_height - self.size//2
            self.dir.y *= -1

        if self.pos.y - self.size//2 < 0:
            self.pos.y = 0 + self.size//2
            self.dir.y *= -1

    def is_within_radius(self, radius:int, obj:Entity):
        return (self.pos.x - radius <= obj.pos.x <= self.pos.x + radius) and \
               (self.pos.y - radius <= obj.pos.y <= self.pos.y + radius)

    """
    Récupère l'objet du group <obj_group> le plus proche de self
    """
    def get_nearest(self, sprites_list:list[Entity]) -> Entity:
        objs = sprites_list
        nearest, min_dist = objs[0], math.sqrt((self.pos.x - objs[0].pos.x)**2 + (self.pos.y - objs[0].pos.y)**2)
        for obj in objs:
            sq_dist = math.sqrt((self.pos.x - obj.pos.x)**2 + (self.pos.y + obj.pos.y)**2)
            if sq_dist < min_dist:
                min_dist = sq_dist
                nearest = obj
        return nearest

    def flee_obj(self, obj:Entity):
        vec = Vec2(self.pos.x - obj.pos.x, self.pos.y - obj.pos.y)
        self.dir = vec.normalize()

    def approach_obj(self, obj:Entity):
        vec = Vec2(obj.pos.x - self.pos.x, obj.pos.y - self.pos.y)
        self.dir = vec.normalize()

    def try_pickup_obj(self, obj:Entity, on_pickup):
        if self.is_colliding(obj):
            on_pickup()



class Kirby(LivingEntity):
    """
    Il existe 4 types de comportements (simplifiées)
        - Classique : Cherche à **aller vers la tomate la plus proche** mais **fuis les fuzzys s'ils sont dans son rayon de check**
        - Fuyard : Cherche toujours à **fuire les ennemis** (ne fais pas attention aux tomates)
        - Téméraire : Cherche à **récupérer la tomate la plus prohce de lui** (sans s'occuper des fuzzys)

        - Déviant : Se déplace aléatoirement

    Quand un kirby meurt, il est ajouté à une liste de morts, qui sera **triée par ordre décroissant de temps de survie**
    puis affichée lorsque tous les kirbys seront morts
    """
    def __init__(self, group, game, sx, sy, behaviour, start_lives, start_speed, start_size):
        super().__init__(group, game, sx, sy)

        self.lives = start_lives
        self.speed = start_speed
        self.size = start_size
        self.time_lived = pg.time.get_ticks() # time when created

        self.tint = pg.Color(randint(100, 255), randint(100, 255), randint(100, 255))

        # rendu
        self.image = pg.transform.scale(Options.KIRBY, (self.size, self.size))
        self.image.fill(self.tint, special_flags=pg.BLEND_RGBA_MULT)

        self.rect = self.image.get_rect()

        # Group refs
        self.fuzzys = self.game.group_fuzzys
        self.tomatoes = self.game.group_tomatoes

        self.check_radius = Options.KIRBY_CHECK_RADIUS
        # rayon d'un cercle à partir duquel le kirby fa faire des checks (fuzzy ou tomate)

        # TODO : Invincibilité quand hit
        self.curr_invincible = Options.KIRBY_INVINCIBLE_TIME

        self.behaviour = self.flee if behaviour == "flee" else self.target_tomatoes if behaviour == "tomato" else self.neutral

    def set_time_lived(self):
        self.time_lived = pg.time.get_ticks() - self.time_lived

    def display_lives(self):
        write(self.screen, f"{self.lives}", (self.pos.x - 20, self.pos.y - self.size))
        self.screen.blit(Options.TOMATE_ICON, (self.pos.x, self.pos.y - self.size))

    def update(self):
        self.decr_invincibility()
        self.bounce_border()
        self.display_lives()
        self.check_collisions()
        draw_radius(self.screen, self.pos.x, self.pos.y, self.check_radius, False)
        self.behaviour()
        self.rect.center = self.pos

    def check_collisions(self):
        self.check_collision_tomato()
        self.check_collision_fuzzys()  # TODO : collsions & invincibility tick

    def check_collision_tomato(self):
        for tomato in self.tomatoes:
            if self.rect.colliderect(tomato.rect):
                tomato.on_pickup()
                self.lives += 1

    def check_collision_fuzzys(self):
        hit = False
        for fuzzy in self.fuzzys:
            if self.rect.colliderect(fuzzy.rect):
                hit = True

        if hit and self.curr_invincible <= 0:
            self.hit()
            self.set_invincible()

    def hit(self):
        if self.lives <= 1: # ??? wtf mais ça marche... okk
            self.game.scoreboard.add(self)
            print(self.time_lived)
            self.kill()
        else:
            self.lives -= 1

    def set_invincible(self):
        self.curr_invincible = Options.KIRBY_INVINCIBLE_TIME

    def decr_invincibility(self):
        if self.curr_invincible > 0:
            self.blink()
            self.curr_invincible -= 1

    # TODO : Blinking when hit
    def blink(self):
        pass

    ### Comportements ###

    """
    Fuis les fuzzys sans rechercher les tomates
    """
    def flee(self):
        for fuzzy in self.fuzzys.sprites():
            if self.is_within_radius(self.check_radius, fuzzy):
                self.flee_obj(fuzzy)
        self.move()

    """
    Recherche la tomate la plus proche sans s'occuper des fuzzys
    """
    def target_tomatoes(self):
        nearest_tomato = self.get_nearest(self.tomatoes.sprites())
        self.approach_obj(nearest_tomato)
        self.move()

    """
    Cherche à récupérer la maxi-tomate la plus proche, mais fuis les fuzzys dès qu'ils sont dans le rayon de check
    """
    def neutral(self):
        nearest_tomato = self.get_nearest(self.tomatoes.sprites())
        no_fuzzy = True

        for fuzzy in self.fuzzys.sprites():
            if self.is_within_radius(self.check_radius, fuzzy):
                self.flee_obj(fuzzy)
                no_fuzzy = False
                break

        if no_fuzzy:
            self.approach_obj(nearest_tomato)

        self.move()





class Fuzzy(LivingEntity):
    """
    Les ennemis des kirbys. Leur point de départ et direction initiale est aléatoire. Ils se baladent selon cette même direction
    pendant toute la partie, rebondissant sur les murs.
    """
    def __init__(self, group, game, sx, sy):
        super().__init__(group, game, sx, sy)
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




class Tomate(Entity):
    def __init__(self, group, game, x, y):
        super().__init__(group, game, x, y)

        self.size = Options.TOMATE_SIZE
        self.image = pg.transform.scale(Options.TOMATE, (self.size, self.size))
        self.rect = self.image.get_rect()

        self.rect.center = self.pos

    def on_pickup(self):
        print("pickup")
        Tomate(self.group, self.game, randint(Options.TOMATE_SIZE, self.sc_width - Options.TOMATE_SIZE), randint(Options.TOMATE_SIZE, self.sc_height - Options.TOMATE_SIZE))
        self.kill()

