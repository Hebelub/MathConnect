from Definitions import *


# Tile position in grid to screen position pixels
def tile_pos_to_screen_pos(x, y):
    screen_x = BOARD_DRAW_X + x * (TILE_SIZE + TILE_OFFSET)
    screen_y = BOARD_DRAW_Y + y * (TILE_SIZE + TILE_OFFSET)
    return screen_x, screen_y


# Offset from screen position to tile and center of tile
def tile_corner_center_offset(x, y):
    return x + TILE_SIZE / 2, y + TILE_SIZE / 2


# Tile position in grid to center of tile in screen position pixels
def centered_tile_pos_to_screen_pos(x, y):
    screen_x, screen_y = tile_pos_to_screen_pos(x, y)
    offset_x, offset_y = tile_corner_center_offset(x, y)
    return screen_x + offset_x, screen_y + offset_y


def add_to_color(color, amount):
    r = min(max(color[0] + amount, 0), 255)
    g = min(max(color[1] + amount, 0), 255)
    b = min(max(color[2] + amount, 0), 255)
    return r, g, b
