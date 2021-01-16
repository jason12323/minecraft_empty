import mod
import pyglet.window.key as key

class red(mod.block):
    def __init__(self):
        super().__init__()
        self.texture = mod.tex_coords((2, 2), (2, 2), (2, 2))
        self.code = "13"
        self.key = key.F
        self.texturepath = "mods/color.png"
class orange(mod.block):
    def __init__(self):
        super().__init__()
        t = (0, 2)
        self.texture = mod.tex_coords(t, t, t)
        self.code = "14"
        self.key = key.G
        self.texturepath = "mods/color.png"
class yellow(mod.block):
    def __init__(self):
        super().__init__()
        t = (3, 2)
        self.texture = mod.tex_coords(t, t, t)
        self.code = "15"
        self.key = key.H
        self.texturepath = "mods/color.png"
class green(mod.block):
    def __init__(self):
        super().__init__()
        t = (0, 3)
        self.texture = mod.tex_coords(t, t, t)
        self.code = "16"
        self.key = key.J
        self.texturepath = "mods/color.png"
class qi(mod.block):
    def __init__(self):
        super().__init__()
        t = (1, 3)
        self.texture = mod.tex_coords(t, t, t)
        self.code = "17"
        self.key = key.K
        self.texturepath = "mods/color.png"
class blue(mod.block):
    def __init__(self):
        super().__init__()
        t = (2, 3)
        self.texture = mod.tex_coords(t, t, t)
        self.code = "18"
        self.key = key.L
        self.texturepath = "mods/color.png"
class pink(mod.block):
    def __init__(self):
        super().__init__()
        t = (3, 3)
        self.texture = mod.tex_coords(t, t, t)
        self.code = "19"
        self.key = key.Z
        self.texturepath = "mods/color.png"
class brown(mod.block):
    def __init__(self):
        super().__init__()
        t = (1, 2)
        self.texture = mod.tex_coords(t, t, t)
        self.code = "20"
        self.key = key.X
        self.texturepath = "mods/color.png"
class main(mod.main):
    def __init__(self, world):
        global kabc
        super().__init__(world)
        self.block = [red(), orange(), yellow(), green(), blue(), qi(), pink(), brown()]

