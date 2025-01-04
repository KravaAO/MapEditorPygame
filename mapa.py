from pygame import *

WIDTH = 1280
HEIGHT = 800
window = display.set_mode((WIDTH, HEIGHT))
display.set_caption('Map Editor')
BLOCK_SIZE = 50

def draw_grid():
    for y in range(0, HEIGHT, BLOCK_SIZE):
        for x in range(0, int(WIDTH / 1.3), BLOCK_SIZE):
            draw.rect(window, (255, 0, 0), [x, y, BLOCK_SIZE, BLOCK_SIZE], 2)
