import pygame as pg

class Options:
    pg.font.init()

    ### Game ###

    SIZE = WIDTH, HEIGHT = (1080, 720)
    FPS = 60

    FONT = pg.font.Font('assets/SMW-font.ttf', 16)

    ### Entities ###

    KIRBY = pg.image.load('assets/kirby.png')
    FUZZY = pg.image.load('assets/fuzzy.png')
    TOMATE = pg.image.load('assets/tomate.png')

    FUZZY_SIZE = 35
    FUZZY_SPEED = 3

    KIRBY_CHECK_RADIUS = 100

    TOMATE_SIZE = 40


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