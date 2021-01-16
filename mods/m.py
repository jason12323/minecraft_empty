import mod
import pyglet.window.key as key
b = False
class red(mod.block):
    def __init__(self):
        global b
        super().__init__()
        self.texture = mod.tex_coords((2, 2), (2, 2), (2, 2))
        self.code = "13"
        self.key = key.F
        try:
            open("color.png", "rb")
        except IOError:
            b = True
        if not b:
            self.texturepath = "mods/color.png"

class main(mod.main):
    boll = (0, -1, 0)
    bp = 0
    rp = 0
    def __init__(self, world):
        super().__init__(world)
        self.world.rb = False
    def init(self):
        self._addblocks(-11, -1, -11, 11, 5, 11, mod.AIR)
        self._addblocks(-11, -2, -11, 11, -1, 11, mod.SNOW)
        self._addblocks(-10, -2, -10, 10, -1, 10, mod.GRASS)
        self._addblocks(-10, -2, 0, 10, -1, 1, mod.SNOW)
        self._addblock(0, -1, 0, mod.NSTON)
        self._addblocks(-5, 0, -10, 5, 1, -9, mod.WATER)
        self._addblocks(-5, 0, 10, 5, 1, 11, mod.MAGMA)
        self.world.position = (0, 0, -10)
    def mousepress(self, button):
        if button == mod.LMOUSE:
            vector = self.world.get_sight_vector()
            block, previous = self.world.model.hit_test(self.world.position, vector)
            if block is not None and block == self.boll:
                c = (block[0] - previous[0], block[1] - previous[1], block[2] - previous[2])
                self.world.model.remove_block(block)
                self.world.model.add_block((block[0] + c[0], block[1], block[2] + c[2]), mod.NSTON)
                self.boll = (block[0] + c[0], block[1], block[2] + c[2])
                if self.boll[0] >= 11 or self.boll[0] <= -11 or self.boll[2] >= 11 or self.boll[2] <= -11:
                    if -5 < self.boll[0] < 5:
                        if self.boll[2] >= 11:
                            self.bp += 1
                            self._print("Blue goal! blue "+str(self.bp)+",red "+str(self.rp))
                        if self.boll[2] <= -11:
                            self.rp += 1
                            self._print("Red goal! blue "+str(self.bp)+",red "+str(self.rp))
                    else:
                        self._print("Out! blue " + str(self.bp) + ",red " + str(self.rp))
                    self.world.model.remove_block(self.boll)
                    self.boll = (0, -1, 0)
                    self.world.model.add_block((0, -1, 0), mod.NSTON)
