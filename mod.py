from __future__ import division

import sys
import math

from pyglet.gl import *
from pyglet.window import mouse

TICKS_PER_SEC = 60

mode = True
filename = "minecraft"

# Size of sectors used to e
# ase block loading.
SECTOR_SIZE = 16
heart = 10
hunger = 10

sky_color = (0.5, 0.69, 1.0)

WALKING_SPEED = 4
FLYING_SPEED = 13

LMOUSE = pyglet.window.mouse.LEFT
RMOUSE = pyglet.window.mouse.RIGHT

GRAVITY = 20.0
MAX_JUMP_HEIGHT = 1.5  # About the height of a block.
# To derive the formula for calculating jump speed, first solve
#    v_t = v_0 + a * t
# for the time at which you achieve maximum height, where a is the acceleration
# due to gravity and v_t = 0. This gives:
#    t = - v_0 / a
# Use t and the desired MAX_JUMP_HEIGHT to solve for v_0 (jump speed) in
#    s = s_0 + v_0 * t + (a * t^2) / 2
JUMP_SPEED = math.sqrt(2 * GRAVITY * MAX_JUMP_HEIGHT)
TERMINAL_VELOCITY = 50

nt = False
try:
    sudfsfa = open(r"map/" + filename, "r+")
    ka = sudfsfa.read()
    sudfsfa.close()
    if len(ka.split(",")) <= 1:
        nt = False
    else:
        nt = True
except IOError:
    nt = False

sasd = open(r"maps", "r+")
na = sasd.read()
sasd.close()
maps = na.split("\n")


PLAYER_HEIGHT = 2

if sys.version_info[0] >= 3:
    xrange = range
ten = 4

def cube_vertices(x, y, z, n):
    """ Return the vertices of the cube at position x, y, z with size 2*n.

    """
    return [
        x - n, y + n, z - n, x - n, y + n, z + n, x + n, y + n, z + n, x + n, y + n, z - n,  # top
        x - n, y - n, z - n, x + n, y - n, z - n, x + n, y - n, z + n, x - n, y - n, z + n,  # bottom
        x - n, y - n, z - n, x - n, y - n, z + n, x - n, y + n, z + n, x - n, y + n, z - n,  # left
        x + n, y - n, z + n, x + n, y - n, z - n, x + n, y + n, z - n, x + n, y + n, z + n,  # right
        x - n, y - n, z + n, x + n, y - n, z + n, x + n, y + n, z + n, x - n, y + n, z + n,  # front
        x + n, y - n, z - n, x - n, y - n, z - n, x - n, y + n, z - n, x + n, y + n, z - n,  # back
    ]


def tex_coord(x, y):
    """ Return the bounding vertices of the texture square.

    """
    m = 1.0 / ten
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m


def tex_coords(top, bottom, side):
    """ Return a list of the texture squares for the top, bottom and side.

    """
    top = tex_coord(*top)
    bottom = tex_coord(*bottom)
    side = tex_coord(*side)
    result = []
    result.extend(top)
    result.extend(bottom)
    result.extend(side * 4)
    return result


TEXTURE_PATH = 'texture.png'

GRASS = tex_coords((1, 0), (0, 1), (0, 0))
SAND = tex_coords((1, 1), (1, 1), (1, 1))
BRICK = tex_coords((2, 0), (2, 0), (2, 0))
STONE = tex_coords((2, 1), (2, 1), (2, 1))
MAGMA = tex_coords((2, 2), (2, 2), (2, 2))
NSTON = tex_coords((3, 1), (3, 1), (3, 1))
TDHS = tex_coords((0, 1), (2, 1), (2, 1))
SNOW = tex_coords((3, 0), (3, 0), (3, 0))
WATER = tex_coords((1, 2), (1, 2), (1, 2))
DIRT = tex_coords((0, 1), (0, 1), (0, 1))
YLB = tex_coords((0, 1), (0, 1), (3, 0))
AIR = "AIR"
COMMAND_BLOCK = tex_coords((3, 2), (3, 2), (3, 2))
kabc = {"1": BRICK, "2": GRASS, "3": SAND, "4": STONE, "6": NSTON, "5": MAGMA, "7": SNOW, "8": WATER, "9": DIRT,
        "10": TDHS, "11": YLB, "12": COMMAND_BLOCK}
bts = {}
for i in kabc.items():
    bts[tuple(i[1])] = i[0]
backpack = []

FACES = [
    (0, 1, 0),
    (0, -1, 0),
    (-1, 0, 0),
    (1, 0, 0),
    (0, 0, 1),
    (0, 0, -1),
]


def normalize(position):
    x, y, z = position
    x, y, z = (int(round(x)), int(round(y)), int(round(z)))
    return (x, y, z)


def sectorize(position):
    x, y, z = normalize(position)
    x, y, z = x // SECTOR_SIZE, y // SECTOR_SIZE, z // SECTOR_SIZE
    return (x, 0, z)


class block:
    def __init__(self):
        self.texture = ()
        self.code = ""
        self.key = None
        self.texturepath = None
    def update(self):
        pass
class main:
    def __init__(self, world):
        self.world = world
        self.block = []
    def update(self):
        for i in self.block:
            i.update()
    def init(self):
        pass
    def keypress(self, symbol):
        for i in self.block:
            if i.key is not None:
                if symbol == i.key:
                    self.world.block = i.texture
    def mousepress(self, button):
        pass
    def _print(self, text):
        self.world.l.text = text
    def _addblock(self, x, y, z, texture):
        if texture != "AIR":
            self.world.model.add_block((x, y, z), texture)
        else:
            self.world.model.remove_block((x, y, z))
    def _addblocks(self, x, y, z, x2, y2, z2, texture):
        for x3 in range(x, x2):
            for y3 in range(y, y2):
                for z3 in range(z, z2):
                    if texture != "AIR":
                        self.world.model.add_block((x3, y3, z3), texture)
                    else:
                        self.world.model.remove_block((x3, y3, z3))