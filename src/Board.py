from Tile import Tile
from Direction import Direction
from Item import combine_items
import random
from Audio import Audio
import copy
import itertools


def remove_empty_in_line(line: list[Tile]):
    to_remove = []
    for tile in line:
        if tile.is_empty():
            to_remove.append(tile)
    for tile in to_remove:
        line.remove(tile)


class Board:

    def __init__(self, width, height):
        self.tiles = [[Tile(self, x, y) for x in range(width)] for y in range(height)]

        self.width = width
        self.height = height

    def __eq__(self, other: "Board"):
        tiles = self.get_tiles()
        other_tiles = other.get_tiles()
        for i in range(len(tiles)):
            tile = tiles[i]
            o_tile = other_tiles[i]
            if tile.get_item() != o_tile.get_item():
                return False
        return True

    def get_tile(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        else:
            return None

    def can_swipe(self, d: Direction):
        if self == self.state_after_move(d):
            return False
        else:
            return True

    def copy(self):
        return copy.deepcopy(self)

    def state_after_move(self, d: Direction):
        new = self.copy()
        new.swipe(d)
        return new

    def possible_states_after_swipe(self):
        states = []
        for d in Direction:
            if self.can_swipe(d):
                states.append(self.state_after_move(d))
        return states

    def get_next_tiles(self):
        states = []

        for state in self.possible_states_after_swipe():
            states.append(state.get_empty_tiles())

        best_combos = []
        least_spikes_used = 1000000
        for combo in itertools.product(*states):
            spikes = len(set(combo))
            if spikes < least_spikes_used:
                least_spikes_used = spikes
                best_combos.clear()
            if spikes == least_spikes_used:
                best_combos.append(set(combo))

        if len(best_combos) > 0:
            chosen_combo = list(random.choice(list(best_combos)))
            real_combo = []

            tiles = self.get_tiles()

            for tile in chosen_combo:
                for real_tile in tiles:
                    if tile == real_tile:
                        real_combo.append(real_tile)

            return real_combo
        else:
            return []

    def get_non_empty_tiles(self):
        non_empty_tiles = []
        for row in self.tiles:
            for tile in row:
                if tile.has_item():
                    non_empty_tiles.append(tile)
        return non_empty_tiles

    def get_empty_tiles(self):
        empty_tiles = []
        for tile in self.get_tiles():
            if tile.is_empty():
                empty_tiles.append(tile)
        return empty_tiles

    def get_tiles(self):
        tiles = []
        for row in self.tiles:
            for tile in row:
                tiles.append(tile)
        return tiles

    def get_edge_tiles_in_direction(self, d: Direction):
        corner = Tile
        if d == Direction.UP:
            corner = self.get_tile(0, 0)
        elif d == Direction.RIGHT:
            corner = self.get_tile(self.width-1, 0)
        elif d == Direction.DOWN:
            corner = self.get_tile(self.width-1, self.height-1)
        elif d == Direction.LEFT:
            corner = self.get_tile(0, self.height-1)

        rot_d = Direction.rotate(d)
        return corner.get_line_in_direction(rot_d)

    def get_lines(self, d: Direction):
        edge = self.get_edge_tiles_in_direction(Direction.opposite(d))
        lines = []
        for tile in edge:
            lines.append(tile.get_line_in_direction(d))
        return lines

    def get_items(self):
        items = []
        for tile in self.get_non_empty_tiles():
            items.append(tile.item)
        return items

    def swipe(self, d: Direction):
        Audio.play_sound('swipe')

        score = 0
        combines = []

        state_changed = True
        lines = self.get_lines(d)

        for line in lines:
            remove_empty_in_line(line)
            line_score, line_combines = combine_items(line)
            score += line_score
            combines.extend(line_combines)

    #    while state_changed:
    #        for

        while state_changed:
            state_changed = False
            for tile in self.get_tiles():
                if tile is None:
                    continue
                if tile.is_empty():
                    continue
                adj_tile = tile.get_tile_in_direction(d)
                if adj_tile is None:
                    continue
                if adj_tile.is_empty():
                    tile.move_item_to(adj_tile)
                    state_changed = True

        return score, combines
