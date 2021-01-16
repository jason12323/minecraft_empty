from __future__ import division

import sys
import math
import random
import pyglet
import time
import mods.modlist as modlist
from collections import deque
from typing import TextIO

from pyglet import image
from pyglet.gl import *
from pyglet.graphics import TextureGroup
from pyglet.window import key, mouse

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


class rw:
    def __init__(self, file):
        self.file = file

    def write(self, d=None):
        if d is None:
            d = {}
        c = ""
        global nt
        if not nt:
            ams = open(r"maps", "a+")
            ams.write("\n"+filename)
            ams.close()
            nt = True
        for am in d.items():
            c += str(am[0][0]) + "/" + str(am[0][1]) + "/" + str(am[0][2])
            c += "="
            c += bts[tuple(am[1])]
            c += ","
        c = c[:-1]
        ams = open(r"" + self.file, "w+")
        ams.write(c)
        ams.close()

    def read(self, addblocka):
        ams = open(r"" + self.file, "r+")
        c = ams.read()
        ams.close()
        c = c.split(",")
        for am in c:
            s = am.split("=")
            a1 = s[0].split("/")
            try:
                a2 = kabc[s[1]]
            except KeyError:
                continue
            a1 = [int(aip) for aip in a1]
            addblocka(tuple(a1), a2, immediate=False)

class rwb:
    def read(self, addblocka, a, b, file, rblock):
        ams = open(r"" + file, "r+")
        c = ams.read()
        ams.close()
        c = c.split(",")
        for am in c:
            s = am.split("=")
            a1 = s[0].split("/")
            a2 = kabc[s[1]]
            a1 = [int(aip) for aip in a1]
            a1[0] = a1[0] + a
            a1[2] = a1[2] + b
            if a2 != NSTON:
                addblocka(tuple(a1), a2, immediate=False)
            else:
                rblock(tuple(a1), immediate=False)


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


def tex_coord(x, y, n=4):
    """ Return the bounding vertices of the texture square.

    """
    m = 1.0 / n
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


class Model(object):

    def __init__(self):

        # A Batch is a collection of vertex lists for batched rendering.
        self.batch = pyglet.graphics.Batch()

        # A TextureGroup manages an OpenGL texture.
        self.group = TextureGroup(image.load(TEXTURE_PATH).get_texture())

        # A mapping from position to the texture of the block at that position.
        # This defines all the blocks that are currently in the world.
        self.world = {}
        self.hsworld = {}

        # Same mapping as `world` but only contains blocks that are shown.
        self.shown = {}

        self._shown = {}

        self.rwk = rw("map/" + filename)
        self.rwb = rwb()

        # Mapping from sector to a list of positions inside that sector.
        self.sectors = {}

        # Simple function queue implementation. The queue is populated with
        # _show_block() and _hide_block() calls
        self.queue = deque()

        self._initialize()

    def _initialize(self):
        if filename is not None and nt:
            self.rwk.read(self.add_block)
            return
        n = 120  # 1/2 width and height of world
        s = 1  # step size
        y = 0  # initial y height
        for x in xrange(-n, n + 1, s):
            for z in xrange(-n, n + 1, s):
                # create a layer stone an grass everywhere.
                self.add_block((x, y - 2, z), GRASS, immediate=False)
                self.add_block((x, y - 3, z), DIRT, immediate=False)
                self.add_block((x, y - 4, z), DIRT, immediate=False)
                for immmb in range(5, 10):
                    if random.randint(1, 5) == 2:
                        self.add_block((x, y - immmb, z), MAGMA, immediate=False)
                    else:
                        self.add_block((x, y - immmb, z), STONE, immediate=False)
                self.add_block((x, y - 10, z), NSTON, immediate=False)

        # generate the hills randomly
        o = n - 30
        for _ in xrange(30):
            a = random.randint(-o, o)  # x position of the hill
            b = random.randint(-o, o)  # z position of the hill
            c = -1  # base of the hill
            h = random.randint(10, 30)  # height of the hill
            s = random.randint(10, h)  # 2 * s is the side length of the hill
            t = random.choice([GRASS, SAND, STONE, SNOW, BRICK, NSTON])
            if t == GRASS or t == BRICK:
                for y in xrange(c, c + h):
                    for x in xrange(a - s, a + s + 1):
                        for z in xrange(b - s, b + s + 1):
                            if (x - a) ** 2 + (z - b) ** 2 > (s + 1) ** 2:
                                continue
                            if (x - 0) ** 2 + (z - 0) ** 2 < 5 ** 2:
                                continue
                            if y > 15:
                                self.add_block((x, y, z), SNOW, immediate=False)
                            elif y > 11:
                                self.add_block((x, y, z), random.choice([STONE, SNOW]), immediate=False)
                            elif y > 4:
                                self.add_block((x, y, z), random.choice([STONE, GRASS]), immediate=False)
                            else:
                                self.add_block((x, y, z), GRASS, immediate=False)
                    if y < 15:
                        s -= random.choice([1, 1, 2])  # decrement side lenth so hills taper off
                    else:
                        s -= 1
            elif t == SNOW:
                s = random.randint(20, 40)
                for x in range(a - s, a + s):
                    for z in range(b - s, b + s):
                        for y in range(-2, -2 - random.randint(2, 4), -1):
                            if (x - a) ** 2 + (z - b) ** 2 > (s + 1) ** 2:
                                continue
                            if (x, y, z) in self.world.keys():
                                self.remove_block((x, y, z))
                            self.add_block((x, y, z), random.choice(
                                [SNOW, SNOW, SNOW, SNOW, SNOW, SNOW, SNOW, SNOW, SNOW, SNOW, SNOW, SNOW, WATER]),
                                           immediate=False)
            elif t == NSTON:
                h = 7
                for y in xrange(c, c - h, -1):
                    for x in xrange(a - s, a + s + 1):
                        for z in xrange(b - s, b + s + 1):
                            if (x - a) ** 2 + (z - b) ** 2 > (s + 1) ** 2:
                                continue
                            if (x - 0) ** 2 + (z - 0) ** 2 < 5 ** 2:
                                continue
                            if (x, y, z) in self.world.keys():
                                self.remove_block((x, y, z))
                        s -= 2
            elif t == SAND:
                s = random.randint(20, 40)
                for x in range(a - s, a + s):
                    for z in range(b - s, b + s):
                        for y in range(-2, -2 - random.randint(2, 4), -1):
                            if (x - a) ** 2 + (z - b) ** 2 > (s + 1) ** 2:
                                continue
                            if (x, y, z) in self.world.keys():
                                self.remove_block((x, y, z))
                            self.add_block((x, y, z), SAND, immediate=False)
            elif t == STONE:
                se = random.randint(1, 6)
                if se < 3:
                    self.rwb.read(self.add_block, a, b, "op/b", self.remove_block)
                elif se > 3:
                    self.rwb.read(self.add_block, a, b, "op/t", self.remove_block)

    def hit_test(self, position, vector, max_distance=20):
        m = 20
        x, y, z = position
        dx, dy, dz = vector
        previous = None
        for _ in xrange(max_distance * m):
            key = normalize((x, y, z))
            if key != previous and key in self.world:
                return key, previous
            previous = key
            x, y, z = x + dx / m, y + dy / m, z + dz / m
        return None, None

    def exposed(self, position):
        x, y, z = position
        for dx, dy, dz in FACES:
            if (x + dx, y + dy, z + dz) not in self.world:
                return True
        return False

    def add_block(self, position, texture, immediate=True):
        if position in self.world:
            self.remove_block(position, immediate)
        self.world[position] = texture
        self.sectors.setdefault(sectorize(position), []).append(position)
        if immediate:
            if self.exposed(position):
                self.show_block(position)
            self.check_neighbors(position)

    def remove_block(self, position, immediate=True):
        try:
            del self.world[position]
            self.sectors[sectorize(position)].remove(position)
            if immediate:
                if position in self.shown:
                    self.hide_block(position)
                self.check_neighbors(position)
        except KeyError:
            pass

    def check_neighbors(self, position):
        x, y, z = position
        for dx, dy, dz in FACES:
            key = (x + dx, y + dy, z + dz)
            if key not in self.world:
                continue
            if self.exposed(key):
                if key not in self.shown:
                    self.show_block(key)
            else:
                if key in self.shown:
                    self.hide_block(key)

    def show_block(self, position, immediate=True):
        texture = self.world[position]
        self.shown[position] = texture
        if immediate:
            self._show_block(position, texture)
        else:
            self._enqueue(self._show_block, position, texture)

    def _show_block(self, position, texture):
        x, y, z = position
        vertex_data = cube_vertices(x, y, z, 0.5)
        texture_data = list(texture)
        # create vertex list
        # FIXME Maybe `add_indexed()` should be used instead
        self._shown[position] = self.batch.add(24, GL_QUADS, self.group,
                                               ('v3f/static', vertex_data),
                                               ('t2f/static', texture_data))

    def hide_block(self, position, immediate=True):
        self.shown.pop(position)
        if immediate:
            self._hide_block(position)
        else:
            self._enqueue(self._hide_block, position)

    def _hide_block(self, position):
        self._shown.pop(position).delete()

    def show_sector(self, sector):
        for position in self.sectors.get(sector, []):
            if position not in self.shown and self.exposed(position):
                self.show_block(position, False)

    def hide_sector(self, sector):
        for position in self.sectors.get(sector, []):
            if position in self.shown:
                self.hide_block(position, False)

    def change_sectors(self, before, after):
        before_set = set()
        after_set = set()
        pad = 4
        for dx in xrange(-pad, pad + 1):
            for dy in [0]:  # xrange(-pad, pad + 1):
                for dz in xrange(-pad, pad + 1):
                    if dx ** 2 + dy ** 2 + dz ** 2 > (pad + 1) ** 2:
                        continue
                    if before:
                        x, y, z = before
                        before_set.add((x + dx, y + dy, z + dz))
                    if after:
                        x, y, z = after
                        after_set.add((x + dx, y + dy, z + dz))
        show = after_set - before_set
        hide = before_set - after_set
        for sector in show:
            self.show_sector(sector)
        for sector in hide:
            self.hide_sector(sector)

    def _enqueue(self, func, *args):
        self.queue.append((func, args))

    def _dequeue(self):
        func, args = self.queue.popleft()
        func(*args)

    def process_queue(self):
        start = time.time()
        while self.queue and time.time() - start < 1.0 / TICKS_PER_SEC:
            self._dequeue()

    def process_entire_queue(self):
        while self.queue:
            self._dequeue()


class Window(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        global kabc, bts, TEXTURE_PATH
        super(Window, self).__init__(*args, **kwargs)

        # Whether or not the window exclusively captures the mouse.
        self.exclusive = False

        # When flying gravity has no effect and speed is increased.
        self.flying = False

        self.mode = True

        # Strafing is moving lateral to the direction you are facing,
        # e.g. moving to the left or right while continuing to face forward.
        #
        # First element is -1 when moving forward, 1 when moving back, and 0
        # otherwise. The second element is -1 when moving left, 1 when moving
        # right, and 0 otherwise.
        self.strafe = [0, 0]

        # Current (x, y, z) position in the world, specified with floats. Note
        # that, perhaps unlike in math class, the y-axis is the vertical axis.
        self.position = (0, 0, 0)

        # First element is rotation of the player in the x-z plane (ground
        # plane) measured from the z-axis down. The second is the rotation
        # angle from the ground plane up. Rotation is in degrees.
        #
        # The vertical plane rotation ranges from -90 (looking straight down) to
        # 90 (looking straight up). The horizontal rotation range is unbounded.
        self.rotation = (0, 0)

        self.lpos = (1000, 1000, 1000)

        # Which sector the player is currently in.
        self.sector = None

        # The crosshairs at the center of the screen.
        self.reticle = None

        # Velocity in the y (upward) direction.
        self.dy = 0
        self.pfile = filename

        # A list of blocks the player can place. Hit num keys to cycle.
        self.inventory = [BRICK, GRASS, SAND, STONE, MAGMA, SNOW, WATER, DIRT, TDHS, YLB]

        # The current block the user can place. Hit num keys to cycle.
        self.block = self.inventory[1]
        self.fal = False
        self.fd = 0
        self.t_code = {}
        # Convenience list of num keys.
        self.num_keys = [
            key._1, key._2, key._3, key._4, key._5,
            key._6, key._7, key._8, key._9, key._0]

        self.e_keys = {}
        self.value = []
        self.rb = True
        self.b = None

        # Instance of the model that handles the world.
        self.mod = []
        for iii in modlist.mod:
            self.mod.append(iii(self))
        for ii in self.mod:
            for j in ii.block:
                kabc[j.code] = j.texture
                if j.texturepath is not None:
                    TEXTURE_PATH = j.texturepath
        for iii in kabc.items():
            bts[tuple(iii[1])] = iii[0]
        self.model = Model()
        for im in self.mod:
            im.init()
        # The label that is displayed in the top left of the canvas.
        self.hglabel = pyglet.text.Label('', font_name=u'微软雅黑'.encode('gbk'), font_size=18,
                                         x=10, y=self.height - 10, anchor_x='left', anchor_y='top',
                                         color=(255, 0, 0, 255))
        self.hghlabel = pyglet.text.Label('', font_name=u'微软雅黑'.encode('gbk'), font_size=18,
                                          x=self.width - 100, y=self.height - 10, anchor_x='right', anchor_y='top',
                                          color=(128, 64, 1, 255))
        self.label = pyglet.text.Label('', font_name='Arial', font_size=18,
                                       x=10, y=self.height - 30, anchor_x='left', anchor_y='top',
                                       color=(0, 0, 0, 255))
        self.l = pyglet.text.Label('', font_name='Arial', font_size=18,
                                       x=10, y=100, anchor_x='left', anchor_y='top',
                                       color=(0, 0, 0, 255))
        self.inte = pyglet.text.Label('hello', font_name='Arial', font_size=18,
                                      x=10, y=self.height - 50, anchor_x='left', anchor_y='top',
                                      color=(0, 0, 0, 255))

        # This call schedules the `update()` method to be called
        # TICKS_PER_SEC. This is the main game event loop.
        self.runm()
        pyglet.clock.schedule_interval(self.update, 1.0 / TICKS_PER_SEC)

    def set_exclusive_mouse(self, exclusive):
        super(Window, self).set_exclusive_mouse(exclusive)
        self.exclusive = exclusive

    def get_sight_vector(self):
        x, y = self.rotation
        # y ranges from -90 to 90, or -pi/2 to pi/2, so m ranges from 0 to 1 and
        # is 1 when looking ahead parallel to the ground and 0 when looking
        # straight up or down.
        m = math.cos(math.radians(y))
        # dy ranges from -1 to 1 and is -1 when looking straight down and 1 when
        # looking straight up.
        dy = math.sin(math.radians(y))
        dx = math.cos(math.radians(x - 90)) * m
        dz = math.sin(math.radians(x - 90)) * m
        return (dx, dy, dz)

    def get_motion_vector(self):
        if any(self.strafe):
            x, y = self.rotation
            strafe = math.degrees(math.atan2(*self.strafe))
            y_angle = math.radians(y)
            x_angle = math.radians(x + strafe)
            if self.flying:
                m = math.cos(y_angle)
                dy = math.sin(y_angle)
                if self.strafe[1]:
                    # Moving left or right.
                    dy = 0.0
                    m = 1
                if self.strafe[0] > 0:
                    # Moving backwards.
                    dy *= -1
                # When you are flying up or down, you have less left and right
                # motion.
                dx = math.cos(x_angle) * m
                dz = math.sin(x_angle) * m
            else:
                dy = 0.0
                dx = math.cos(x_angle)
                dz = math.sin(x_angle)
        else:
            dy = 0.0
            dx = 0.0
            dz = 0.0
        return (dx, dy, dz)

    def update(self, dt):
        if int(time.time() * 60) / 60 % 1 == 0:
            self.runn()
        for im in self.mod:
            im.update()
        for im in self.t_code.keys():
            if "==" in im:
                f1 = str(im.split("==")[0])
                f2 = str(im.split("==")[1])
                if f1 == "getx":
                    f1 = self.position[0]
                elif f1 == "gety":
                    f1 = self.position[1]
                elif f1 == "getz":
                    f1 = self.position[2]
                elif f1 == "getmapname":
                    f1 = filename
                elif f1 == "getpblock":
                    if (
                    int(self.position[0]), int(self.position[1] - 2), int(self.position[2])) in self.model.world.keys():
                        f1 = bts[tuple(self.model.world[
                                           (int(self.position[0]), int(self.position[1] - 2), int(self.position[2]))])]
                    else:
                        f1 = 0
                if f2 == "getx":
                    f2 = self.position[0]
                elif f2 == "gety":
                    f2 = self.position[1]
                elif f2 == "getz":
                    f2 = self.position[2]
                elif f2 == "getmapname":
                    f2 = filename
                elif f2 == "getpblock":
                    if (
                    int(self.position[0]), int(self.position[1] - 2), int(self.position[2])) in self.model.world.keys():
                        f2 = bts[tuple(self.model.world[
                                           (int(self.position[0]), int(self.position[1] - 2), int(self.position[2]))])]
                    else:
                        f2 = 0
                if f1 == f2:
                    self._run(self.t_code[im])
            elif "~=" in im:
                f1 = str(im.split("~=")[0])
                f2 = str(im.split("~=")[1])
                if f1 == "getx":
                    f1 = self.position[0]
                elif f1 == "gety":
                    f1 = self.position[1]
                elif f1 == "getz":
                    f1 = self.position[2]
                elif f1 == "getmapname":
                    f1 = filename
                elif f1 == "getpblock":
                    if (
                            int(self.position[0]), int(self.position[1] - 2),
                            int(self.position[2])) in self.model.world.keys():
                        f1 = bts[tuple(self.model.world[
                                           (int(self.position[0]), int(self.position[1] - 2), int(self.position[2]))])]
                    else:
                        f1 = 0
                if f2 == "getx":
                    f2 = self.position[0]
                elif f2 == "gety":
                    f2 = self.position[1]
                elif f2 == "getz":
                    f2 = self.position[2]
                elif f2 == "getmapname":
                    f2 = filename
                elif f2 == "getpblock":
                    if (
                            int(self.position[0]), int(self.position[1] - 2),
                            int(self.position[2])) in self.model.world.keys():
                        f2 = bts[tuple(self.model.world[
                                           (int(self.position[0]), int(self.position[1] - 2), int(self.position[2]))])]
                    else:
                        f2 = 0
                if 1 >= int(f1) - int(f2) >= -1:
                    self._run(self.t_code[im])
        global heart, hunger
        if int(time.time() * 60) / 60 % 10 == 0 and heart < 10:
            heart += 1
        if heart <= 0:
            heart = 10
            hunger = 10
            self.position = (0, 0, 0)
        try:
            if self.model.world[(int(self.position[0]), int(self.position[1] - 2), int(self.position[2]))] == YLB or \
                    self.model.world[
                        (int(self.position[0]), int(self.position[1] - 1), int(self.position[2]))] == YLB or \
                    self.model.world[(int(self.position[0]), int(self.position[1]), int(self.position[2]))] == YLB:
                ps = [self.position[0], self.position[1] - 2, self.position[2]]
                zw = [(0, 0, 1), (1, 0, 0), (0, 1, 0), (-1, 0, 0), (0, -1, 0), (0, 0, -1), (0, 1, 1), (1, 0, 1),
                      (0, 1, -1), (1, 0, -1), (0, -1, -1), (-1, 0, -1), (1, -1, 0), (1, 1, 0), (-1, 1, 0), (-1, -1, 0),
                      (1, 1, 1), (1, -1, 1), (-1, -1, 1), (-1, 1, 1), (1, -1, -1), (-1, -1, -1), (0, 0, 2)]
                for i in zw:
                    dx = int(i[0] + ps[0])
                    dy = int(i[1] + ps[1])
                    dz = int(i[2] + ps[2])
                    if (dx, dy, dz) in self.model.world.keys() and (dx, dy, dz + 1) in self.model.world.keys():
                        if self.model.world[(dx, dy, dz)] == TDHS:
                            self.lpos = (dx, dy, dz)
                            self.moveb((dx, dy, dz + 1), (0, 0, 1))
        except KeyError:
            pass
        self.model.process_queue()
        sector = sectorize(self.position)
        if sector != self.sector:
            self.model.change_sectors(self.sector, sector)
            if self.sector is None:
                self.model.process_entire_queue()
            self.sector = sector
        m = 8
        dt = min(dt, 0.2)
        for _ in xrange(m):
            self._update(dt / m)

    def _update(self, dt):
        # walking
        speed = FLYING_SPEED if self.flying else WALKING_SPEED
        d = dt * speed  # distance covered this tick.
        dx, dy, dz = self.get_motion_vector()
        # New position in space, before accounting for gravity.
        dx, dy, dz = dx * d, dy * d, dz * d
        # gravity
        if not self.flying:
            # Update your vertical speed: if you are falling, speed up until you
            # hit terminal velocity; if you are jumping, slow down until you
            # start falling.
            global JUMP_SPEED
            if self.block != MAGMA:
                self.dy -= dt * GRAVITY
                JUMP_SPEED = math.sqrt(2 * GRAVITY * MAX_JUMP_HEIGHT)
            else:
                self.dy -= dt * 0.2
                JUMP_SPEED = math.sqrt(2 * 0.2 * MAX_JUMP_HEIGHT)
            self.fal = True
            self.dy = max(self.dy, -TERMINAL_VELOCITY)
            dy += self.dy * dt
        # collisions
        x, y, z = self.position
        x, y, z = self.collide((x + dx, y + dy, z + dz), PLAYER_HEIGHT)
        if self.fal and dy <= 0:
            self.fd -= dy
        self.position = (x, y, z)

    def runm(self):
        try:
            xg = open(r"package/" + self.pfile, "r+")
            cmg = xg.read()
            xg.close()
        except IOError:
            xg = open(r"package/" + self.pfile, "w+")
            xg.write("setup:\nmain:")
            xg.close()
            cmg = "setup:\nmain:"
        cmg = cmg.split("\n")
        c = ""
        for im in cmg:
            c += im
        c = c.split("setup:")[1]
        seu = c.split("main:")[0]
        se = c.split("main:")[1].split("when:")[1:]
        for im in se:
            if " press:" in im:
                sw = im.split(" press:")[0]
                self.e_keys[sw] = im.split(" press:")[1]
            else:
                sw = im.split(":")[0]
                self.t_code[sw] = im.split(":")[1]

        self._run(seu)

    def _run(self, seu):
        global filename
        for cod in seu.split(";"):
            if cod == "":
                continue
            f = cod.split("(")[1][:-1]
            m = cod.split("(")[0]
            if len(f) >= 6:
                lf = len(f)
                for im in range(5, lf):
                    if "value" == f[im - 5:im]:
                        f = f[:im - 5] + str(self.value[int(f[im])]) + f[im + 1:]
            if f == "getx":
                f = self.position[0]
            elif f == "gety":
                f = self.position[1]
            elif f == "getz":
                f = self.position[2]
            elif f == "getpblock":
                if (int(self.position[0]), int(self.position[1] - 2), int(self.position[2])) in self.model.world.keys():
                    f = bts[tuple(
                        self.model.world[(int(self.position[0]), int(self.position[1] - 2), int(self.position[2]))])]
                else:
                    f = 0
            elif f == "getmp":
                vector = self.get_sight_vector()
                block = self.model.hit_test(self.position, vector)[1]
                f = ""
                if block is not None:
                    for amsd in block:
                        f += str(amsd) + ","
                f = f[:-1]
            elif f == "getmb":
                vector = self.get_sight_vector()
                block = self.model.hit_test(self.position, vector)[0]
                f = ""
                if block is not None:
                    for amsd in block:
                        f += str(amsd) + ","
                f = f[:-1]
            elif f == "getmapname":
                f = filename
            elif "++" in f:
                f = str(int(f.split("+")[0]) + int(f.split("+")[1]))
            elif "--" in f:
                f = str(int(f.split("-")[0]) - int(f.split("-")[1]))
            elif "**" in f:
                f = str(int(f.split("*")[0]) * int(f.split("*")[1]))
            elif "//" in f:
                f = str(int(f.split("/")[0]) // int(f.split("/")[1]))

            if m == "setmode":
                if f == "1":
                    self.mode = True
                else:
                    self.mode = False
            elif m == "newvalue":
                self.value.append(f)
            elif m == "changemap":
                filename = f
                self.model = Model()
                self.flying = False
                self.mode = True
                self.strafe = [0, 0]
                self.position = (0, 0, 0)
                self.rotation = (0, 0)
                self.lpos = (1000, 1000, 1000)
                self.sector = None
                self.reticle = None
                self.dy = 0
                self.pfile = filename
                self.fal = False
                self.fd = 0
                self.t_code = {}
                self.e_keys = {}
                self.value = []
                self.rb = True
                x, y = self.width // 2, self.height // 2
                n = 10
                self.reticle = pyglet.graphics.vertex_list(4, ('v2i', (x - n, y, x + n, y, x, y - n, x, y + n)))
            elif m[:8] == "setvalue":
                self.value[int(m[8])] = f
            elif m == "canchangeblock":
                self.rb = (f == "1")
            elif m == "setblock":
                f = f.split(",")
                if len(f) >= 4:
                    if f[3] != "n":
                        self.model.add_block(tuple([int(imt) for imt in f[:3]]), kabc[f[3]])
                    else:
                        self.model.remove_block(tuple([int(imt) for imt in f[:3]]))
            elif m == "save":
                self.model.rwk.write(self.model.world)
            elif m == "sleep":
                time.sleep(float(f))
            elif m == "give":
                self.block = kabc[f]
                backpack.append(kabc[f])
            elif m == "move":
                f = f.split(",")
                self.position = [int(imt) for imt in f[:3]]
            elif m == "setflymode":
                self.flying = (f == "1")
            elif m == "setrotation":
                f = f.split(",")
                self.rotation = tuple([int(imt) for imt in f[:2]])
            elif m == "setwalkspeed":
                global WALKING_SPEED
                WALKING_SPEED = int(f)
            elif m == "setflyspeed":
                global FLYING_SPEED
                FLYING_SPEED = int(f)
            elif m == "setjumpspeed":
                global JUMP_SPEED
                JUMP_SPEED = int(f)
            elif m == "say":
                self.inte.text = f

    def runn(self):
        xg = open(r"package/" + self.pfile, "r+")
        cmg = xg.read()
        xg.close()
        cmg = cmg.split("\n")
        c = ""
        for im in cmg:
            c += im
        c = c.split("setup:")[1]
        seu = c.split("main:")[1]
        seu = seu.split("when:")[0]
        self._run(seu)

    def collide(self, position, height):
        pad = 0.25
        p = list(position)
        np = normalize(position)
        for face in FACES:  # check all surrounding blocks
            for i in xrange(3):  # check each dimension independently
                if not face[i]:
                    continue
                # How much overlap you have with this dimension.
                d = (p[i] - np[i]) * face[i]
                if d < pad:
                    continue
                for dy in xrange(height):  # check each height
                    op = list(np)
                    op[1] -= dy
                    op[i] += face[i]
                    if tuple(op) not in self.model.world:
                        continue
                    p[i] -= (d - pad) * face[i]
                    if face == (0, -1, 0) or face == (0, 1, 0):
                        # You are colliding with the ground or ceiling, so stop
                        # falling / rising.
                        self.fal = False
                        if self.fd > 8 and self.mode and self.block != MAGMA:
                            global heart
                            heart -= int(self.fd / 5 + 1)
                        self.fd = 0
                        self.dy = 0
                    break
        return tuple(p)

    def moveb(self, position, dir):
        x, y, z = position
        dx = x + dir[0]
        dy = y + dir[1]
        dz = z + dir[2]
        if position in self.model.world.keys():
            if (dx, dy, dz) in self.model.world.keys():
                self.moveb((dx, dy, dz), dir)
            self.model.add_block((dx, dy, dz), self.model.world[position], immediate=False)
            self.model.remove_block(position)

    def on_mouse_press(self, x, y, button, modifiers):
        for im in self.mod:
            im.mousepress(button)
        if self.exclusive:
            if self.rb:
                vector = self.get_sight_vector()
                block, previous = self.model.hit_test(self.position, vector)
                if button == mouse.RIGHT:
                    if previous:
                        if (not self.mode) or (self.block in backpack):
                            self.model.add_block(previous, self.block)
                            if self.mode:
                                backpack.remove(self.block)
                elif button == pyglet.window.mouse.LEFT and block:
                    texture = self.model.world[block]
                    if texture != NSTON:
                        self.model.remove_block(block)
                        if self.mode:
                            backpack.append(texture)
        else:
            self.set_exclusive_mouse(True)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.exclusive:
            m = 0.15
            x, y = self.rotation
            x, y = x + dx * m, y + dy * m
            y = max(-90, min(90, y))
            self.rotation = (x, y)

    def on_key_press(self, symbol, modifiers):
        for im in self.mod:
            im.keypress(symbol)
        if symbol == key.W:
            self.strafe[0] -= 1
        elif symbol == key.S:
            self.strafe[0] += 1
        elif symbol == key.A:
            self.strafe[1] -= 1
        elif symbol == key.D:
            self.strafe[1] += 1
        elif symbol == key.M:
            self.mode = not self.mode
        elif symbol == key.B:
            self.on_mouse_press(-10000000, 0, mouse.RIGHT, 0)
        elif symbol == key.SPACE:
            if self.dy == 0:
                self.dy = JUMP_SPEED
        elif symbol == key.ESCAPE:
            self.set_exclusive_mouse(False)
        elif symbol == key.TAB and (not self.mode):
            self.flying = not self.flying
        elif symbol in self.num_keys:
            index = (symbol - self.num_keys[0]) % len(self.inventory)
            self.block = self.inventory[index]
        elif symbol == key.C:
            self.model.rwk.write(self.model.world)
        elif symbol == key.Z:
            block, previous = self.model.hit_test(self.position, self.get_sight_vector())
            if self.model.world[block] == TDHS:
                self.moveb((block[0], block[1], block[2] + 1), (0, 0, 1))
            elif self.model.world[block] == COMMAND_BLOCK:
                pass
        elif symbol in {key.Q: "Q", key.T: "T", key.E: "E", key.R: "R", key.Y: "Y", key.U: "U", key.I: "I", key.O: "O",
                        key.P: "P", key.F: "F", key.G: "G", key.H: "H", key.N: "N"}.keys():
            if \
            {key.Q: "Q", key.T: "T", key.E: "E", key.R: "R", key.Y: "Y", key.U: "U", key.I: "I", key.O: "O", key.P: "P",
             key.F: "F", key.G: "G", key.H: "H", key.N: "N"}[symbol] in self.e_keys.keys():
                self._run(self.e_keys[
                              {key.Q: "Q", key.T: "T", key.E: "E", key.R: "R", key.Y: "Y", key.U: "U", key.I: "I",
                               key.O: "O", key.P: "P", key.F: "F", key.G: "G", key.H: "H", key.N: "N"}[
                                  symbol]])

    def on_key_release(self, symbol, modifiers):
        if symbol == key.W:
            self.strafe[0] += 1
        elif symbol == key.S:
            self.strafe[0] -= 1
        elif symbol == key.A:
            self.strafe[1] += 1
        elif symbol == key.D:
            self.strafe[1] -= 1
        elif symbol == key.Z:
            block, previous = self.model.hit_test(self.position, self.get_sight_vector())
            if self.model.world[block] == TDHS:
                self.moveb((block[0], block[1], block[2] + 2), (0, 0, -1))

    def on_resize(self, width, height):
        self.label.y = height - 30
        self.hglabel.y = height - 10
        self.inte.y = height - 50
        if self.reticle:
            self.reticle.delete()
        x, y = self.width // 2, self.height // 2
        n = 10
        self.reticle = pyglet.graphics.vertex_list(4,
                                                   ('v2i', (x - n, y, x + n, y, x, y - n, x, y + n))
                                                   )

    def set_2d(self):
        width, height = self.get_size()
        glDisable(GL_DEPTH_TEST)
        viewport = self.get_viewport_size()
        glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, max(1, width), 0, max(1, height), -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set_3d(self):
        width, height = self.get_size()
        glEnable(GL_DEPTH_TEST)
        viewport = self.get_viewport_size()
        glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(65.0, width / float(height), 0.1, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        x, y = self.rotation
        glRotatef(x, 0, 1, 0)
        glRotatef(-y, math.cos(math.radians(x)), 0, math.sin(math.radians(x)))
        x, y, z = self.position
        glTranslatef(-x, -y, -z)

    def on_draw(self):
        self.clear()
        self.set_3d()
        glColor3d(1, 1, 1)
        self.model.batch.draw()
        self.draw_focused_block()
        self.set_2d()
        self.draw_label()
        self.draw_reticle()

    def draw_focused_block(self):
        vector = self.get_sight_vector()
        block = self.model.hit_test(self.position, vector)[0]
        if block:
            x, y, z = block
            vertex_data = cube_vertices(x, y, z, 0.51)
            glColor3d(0, 0, 0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            pyglet.graphics.draw(24, GL_QUADS, ('v3f/static', vertex_data))
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def draw_label(self):
        x, y, z = self.position
        self.label.text = ' (%.2f, %.2f, %.2f), mode=%s' % (x, y, z, {True: "生存", False: "创造"}[self.mode])
        self.label.draw()
        self.hglabel.text = "❤" * heart
        self.hghlabel.text = "🍗" * hunger
        if self.mode:
            self.hglabel.draw()
            self.hghlabel.draw()
        self.l.draw()
        self.inte.draw()

    def draw_reticle(self):
        glColor3d(0, 0, 0)
        self.reticle.draw(GL_LINES)


def setup_fog():
    # Enable fog. Fog "blends a fog color with each rasterized pixel fragment's
    # post-texturing color."
    glEnable(GL_FOG)
    # Set the fog color.

    rr, gg, bb = sky_color
    glFogfv(GL_FOG_COLOR, (GLfloat * 4)(rr, gg, bb, 1))

    # Say we have no preference between rendering speed and quality.
    glHint(GL_FOG_HINT, GL_DONT_CARE)
    # Specify the equation used to compute the blending factor.
    glFogi(GL_FOG_MODE, GL_LINEAR)
    # How close and far away fog starts and ends. The closer the start and end,
    # the denser the fog in the fog range.
    glFogf(GL_FOG_START, 20.0)
    glFogf(GL_FOG_END, 60.0)


def setup():
    # Set the color of "clear", i.e. the sky, in rgba.
    rr, gg, bb = sky_color
    glClearColor(rr, gg, bb, 1)

    # Enable culling (not rendering) of back-facing facets -- facets that aren't
    # visible to you.
    glEnable(GL_CULL_FACE)
    # Set the texture minification/magnification function to GL_NEAREST (nearest
    # in Manhattan distance) to the specified texture coordinates. GL_NEAREST
    # "is generally faster than GL_LINEAR, but it can produce textured images
    # with sharper edges because the transition between texture elements is not
    # as smooth."
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    setup_fog()


def main():
    window = Window(width=800, height=600, caption="Minecraft-Jason.Chen   我的世界 模组更新" + filename, resizable=True)
    # Hide the mouse cursor and prevent the mouse from leaving the window.
    setup()
    pyglet.app.run()

def maii():
    global filename, nt
    print("Minecraft-Jason.Chen:\n\n")
    print("我的世界 模组更新")
    if mode:
        for i in range(len(maps)):
            print(str(i+1)+":"+maps[i])
        print(str(len(maps) + 1) + ":新地图")
        print(str(len(maps) + 2) + ":退出")
        bh = int(input("?"))
        if bh <= len(maps):
            filename = maps[bh-1]
            nt = True
            main()
        elif bh == len(maps)+1:
            filename = input("地图名?")
            nt = False
            main()
        elif bh == len(maps)+2:
            exit()
    else:
        main()


if __name__ == '__main__':
    print("Minecraft-Jason.Chen:\n\n")
    print("我的世界 模组更新")
    if mode:
        for i in range(len(maps)):
            print(str(i+1)+":"+maps[i])
        print(str(len(maps) + 1) + ":新地图")
        print(str(len(maps) + 2) + ":退出")
        bh = int(input("?"))
        if bh <= len(maps):
            filename = maps[bh-1]
            nt = True
            main()
        elif bh == len(maps)+1:
            filename = input("地图名?")
            nt = False
            main()
        elif bh == len(maps)+2:
            pass
    else:
        main()
