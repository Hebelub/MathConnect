import Board
from typing import Optional
from Item import Item
from Direction import Direction


class Tile:
    def __init__(self, board: Board, x, y):
        self.x = x
        self.y = y
        self.board = board
        self.item: Optional[Item] = None

    def __eq__(self, other: "Tile"):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return self.x + self.y * 100000

    def set_item(self, item: Optional[Item]):
        self.item = item

    def is_empty(self):
        return self.item is None

    def has_item(self):
        return self.item is not None

    def get_item(self):
        return self.item

    def move_item_to(self, tile):
        tile.set_item(self.item)
        self.set_item(None)

    def get_tile_in_direction(self, d: Direction):
        offset = Direction.to_offset(d)
        return self.get_tile_with_offset(offset[0], offset[1])

    def get_line_in_direction(self, d: Direction):
        line = [self]
        next_tile = self.get_tile_in_direction(d)
        if next_tile is not None:
            line.extend(next_tile.get_line_in_direction(d))
        return line

    def get_tile_with_offset(self, x, y):
        return self.board.get_tile(self.x + x, self.y + y)

    def count_items_in_direction(self, d: Direction):
        adj_tile = self.get_tile_in_direction(d)
        if adj_tile is None:
            return 0
        return adj_tile.count_items_in_direction(d) + (not adj_tile.is_empty())

    def count_horizontal_items(self):
        return self.count_items_in_direction(Direction.LEFT) \
             + self.count_items_in_direction(Direction.RIGHT) \
             + self.has_item()

    def count_vertical_items(self):
        return self.count_items_in_direction(Direction.UP) \
             + self.count_items_in_direction(Direction.DOWN) \
             + self.has_item()

    def count_empty_in_direction(self, direction: Direction):
        adj_tile = self.get_tile_in_direction(direction)
        if adj_tile is None:
            return 0
        return adj_tile.count_items_in_direction(direction) + adj_tile.is_empty()
