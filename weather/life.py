import time
from random import randint

from sense_hat import SenseHat
#from sense_emu import SenseHat

# Conway's game of life, on an 8x8 grid, with occasional random cells to break locked patterns
# and repopulation when empty. Nice little 8x8 color SenseHat demo. Slightly modified from the
# original to work with my Weather app.
#
# Simon Garton
# simon.garton@gmail.com
# November / December 2020


class Life():

    def __init__(self):
        self.sense = SenseHat()

    def setup_world(self, xdim, ydim):
        world = []
        for i in range(0, xdim):
            world.append([0] * ydim)
        return world

    def count_living(self, world):
        xdim = len(world)
        ydim = len(world[0])

        living = 0
        for x in range(0, xdim):
            for y in range(0, ydim):
                if (world[x][y] > 0):
                    living = living + 1
        return living

    def draw_world(self, world, rgb):
        xdim = len(world)
        ydim = len(world[0])

        self.sense.clear()
        for x in range(0, xdim):
            for y in range(0, ydim):
                w = world[x][y]
                if (w > 0):
                    w = w if w <= 5 else 5
                    w = 2 if w == 1 else 5
                    scaled = (rgb[0]*w, rgb[1]*w, rgb[2]*w)
                    self.sense.set_pixel(x, y, scaled)

    def random_world(self, world):
        xdim = len(world)
        ydim = len(world[0])

        for i in range(0, xdim * round(ydim / 3)):
            x = randint(0, xdim-1)
            y = randint(0, ydim-1)
            world[x][y] = randint(1, 5)

    def init_world(self, world):
        self.random_world(world)

    def glider(self, world):
        world[4][4] = 1
        world[5][5] = 1
        world[5][6] = 1
        world[4][6] = 1
        world[3][6] = 1

    def is_alive(self, world, xdim, ydim, x, y):
        x1 = (x + xdim) % xdim
        y1 = (y + ydim) % ydim
        return 1 if world[x1][y1] > 0 else 0

    def get_neighbor(self, world, xdim, ydim, x, y):
        x1 = (x + xdim) % xdim
        y1 = (y + ydim) % ydim
        alive = self.is_alive(world, xdim, ydim, x1, y1)
        return alive

    def get_neighbors(self, x, y, world):
        xdim = len(world)
        ydim = len(world[0])

        neighbors = 0
        neighbors = neighbors + \
            self.get_neighbor(world, xdim, ydim, x + 1, y + 1)
        neighbors = neighbors + \
            self.get_neighbor(world, xdim, ydim, x + 0, y + 1)
        neighbors = neighbors + \
            self.get_neighbor(world, xdim, ydim, x - 1, y + 1)
        neighbors = neighbors + \
            self.get_neighbor(world, xdim, ydim, x + 1, y + 0)
        neighbors = neighbors + \
            self.get_neighbor(world, xdim, ydim, x - 1, y + 0)
        neighbors = neighbors + \
            self.get_neighbor(world, xdim, ydim, x + 1, y - 1)
        neighbors = neighbors + \
            self.get_neighbor(world, xdim, ydim, x + 0, y - 1)
        neighbors = neighbors + \
            self.get_neighbor(world, xdim, ydim, x - 1, y - 1)
        return neighbors

    def update_world(self, world):
        xdim = len(world)
        ydim = len(world[0])

        new_world = []
        for i in range(0, xdim):
            new_world.append([0] * ydim)

        changed = False
        for x in range(0, xdim):
            for y in range(0, ydim):
                neighbors = self.get_neighbors(x, y, world)
                new = 0
                alive = self.is_alive(world, xdim, ydim, x, y)
                if (alive == 1):
                    new = alive + 1 if (neighbors ==
                                        2 or neighbors == 3) else 0
                else:
                    new = 1 if (neighbors == 3) else 0
                new_world[x][y] = new
                if new == 1:
                    changed = True

        for x in range(0, xdim):
            for y in range(0, ydim):
                world[x][y] = new_world[x][y]

        return changed

    def print_world(self, world):
        xdim = len(world)
        ydim = len(world[0])
        for y in range(0, ydim):
            line = ''
            for x in range(0, xdim):
                line = line + str(world[x][y])
            print(line)
        print(" " + str(self, self.count_living(world)))

    def run(self, xdim, ydim, seconds):
        start_time = time.time()
        world = self.setup_world(xdim, ydim)
        self.init_world(world)
        living = self.count_living(world)
        last = living
        iters = 0
        sleep_period = randint(1, 50)
        r = randint(0, 50)
        g = randint(0, 50)
        b = randint(0, 50)
        while(True):
            changed = self.update_world(world)
            self.draw_world(world, (r, g, b))
            sleep_period = sleep_period + randint(0, 6) - 3
            if (sleep_period < 10):
                sleep_period = 10
            if (sleep_period > 50):
                sleep_period = 50
            time.sleep(sleep_period / 100)
            living = self.count_living(world)
            if (living == last):
                iters = iters + 1
                if iters > 20:
                    self.random_world(world)
                    r = randint(0, 50)
                    g = randint(0, 50)
                    b = randint(0, 50)
                    sleep_period = randint(1, 50)
            else:
                iters = 0
            last = living
            if (randint(0, 100) == 0):
                self.random_world(world)
                r = randint(0, 50)
                g = randint(0, 50)
                b = randint(0, 50)
                sleep_period = randint(1, 50)
            if not seconds == None:
                if (time.time() - start_time) > seconds:
                    break
