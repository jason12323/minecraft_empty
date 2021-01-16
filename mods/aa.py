import mod
from main import *
class brown(mod.block):
    def __init__(self):
        super().__init__()
        t = (0,1)
        self.texture = tex_coords(t, t, t)
        self.code = "20"
        self.texturepath = "mods/Sprite 6.png"
class main(mod.main):
    world: Window
    def __init__(self, world):
        global kabc
        super().__init__(world)
        self.block = [brown()]
    @staticmethod
    def texturenum():
        return 2