from enum import Enum


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

    @staticmethod
    def to_offset(direction):
        if direction == Direction.UP:
            return 0, -1
        elif direction == Direction.RIGHT:
            return 1, 0
        elif direction == Direction.DOWN:
            return 0, 1
        elif direction == Direction.LEFT:
            return -1, 0

    @staticmethod
    def opposite(direction):
        if direction == Direction.UP:
            return Direction.DOWN
        elif direction == Direction.RIGHT:
            return Direction.LEFT
        elif direction == Direction.DOWN:
            return Direction.UP
        elif direction == Direction.LEFT:
            return Direction.RIGHT

    @staticmethod
    def rotate(direction):
        if direction == Direction.UP:
            return Direction.RIGHT
        elif direction == Direction.RIGHT:
            return Direction.DOWN
        elif direction == Direction.DOWN:
            return Direction.LEFT
        elif direction == Direction.LEFT:
            return Direction.UP

    @staticmethod
    def is_horizontal(direction):
        return direction == Direction.LEFT or direction == Direction.RIGHT

    @staticmethod
    def is_vertical(direction):
        return direction == Direction.UP or direction == Direction.DOWN
