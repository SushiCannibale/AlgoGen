import pygame as pg

class Options:
    pg.font.init()

    ### Game ###

    SIZE = WIDTH, HEIGHT = (1080, 720)
    FPS = 120

    FONT = pg.font.Font('assets/SMW-font.ttf', 16)

    ### Entities ###

    KIRBY = pg.image.load('assets/kirby.png')
    FUZZY = pg.image.load('assets/fuzzy.png')
    TOMATE = pg.image.load('assets/tomate.png')
    TOMATE_ICON = pg.transform.scale(TOMATE, (20, 20))

    FUZZY_SIZE = 35
    FUZZY_SPEED = 3

    KIRBY_CHECK_RADIUS = 100

    TOMATE_SIZE = 40

    MIN_KIRBY_START_SIZE = 40
    MAX_KIRBY_START_SIZE = 60

    MIN_KIRBY_START_SPEED = 2  # div by 10
    MAX_KIRBY_START_SPEED = 7  # div by 10

    MIN_KIRBY_START_HEALTH = 1
    MAX_KIRBY_START_HEALTH = 2

    KIRBY_INVINCIBLE_TIME = 200  # in millis

    KIRBY_INVINC_BLINK_DELAY = 10  # every 4 frames

    ### Scoreboard ###

    SCOREBOARD_INTERLINE = 10


def tint(surf, tint_color):
    """ adds tint_color onto surf.
    """
    surf = surf.copy()
    surf.fill((0, 0, 0, 255), None, pg.BLEND_RGBA_MULT)
    surf.fill(tint_color[0:3] + (0,), None, pg.BLEND_RGBA_ADD)
    return surf

def write(surface:pg.Surface, text:str, pos:tuple[int, int]):
    render = Options.FONT.render(text, False, (255, 255, 255, 120))
    surface.blit(render, pos)

def draw_radius(screen:pg.surface.Surface, x:float, y:float, radius:int, filled:bool):
    pg.draw.rect(screen, (255, 0, 0), pg.Rect(x - radius, y - radius, 2*radius, 2*radius), width=(0 if filled else 1))