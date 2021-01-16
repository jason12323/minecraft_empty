import random
x = ""


def add_block(p, t):
    global x
    x += str(p[0])+"/"+str(p[1])+"/"+str(p[2])+"="+t+","


def _initialize():
    n = 120  # 1/2 width and height of world
    s = 1  # step size
    y = 0  # initial y height
    for x in range(-n, n + 1, s):
        for z in range(-n, n + 1, s):
            # create a layer stone an grass everywhere.
            add_block((x, y - 2, z), "2")
            add_block((x, y - 3, z), "9")
            add_block((x, y - 4, z), "9")
            for immmb in range(5, 10):
                if random.randint(1, 5) == 2:
                    add_block((x, y - immmb, z), "5")
                else:
                    add_block((x, y - immmb, z), "4")
            add_block((x, y - 10, z), "6")


_initialize()
x = x[:-1]
z = open(r"ptw", "w+")
z.write(x)
z.close()
