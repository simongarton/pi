from sense_emu import SenseHat

sense = SenseHat()
sense.clear()


def init():
    pixels = [
        [0, 1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 0, 1],
        [1, 1, 0, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 0, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 0]]
    return pixels


def draw(bright, pixels):
    for row in range(0, 8):
        for col in range(0, 8):
            if pixels[col][row] == 1:
                sense.set_pixel(row, col, (bright, bright, 0))


def face():
    pixels = init()
    draw(200, pixels)


face()
