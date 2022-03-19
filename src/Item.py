import Tile
from Audio import Audio
from Utility import centered_tile_pos_to_screen_pos
from dataclasses import dataclass


class CombineResult:
    def __init__(self, combine_text, x, y, recent=True):
        self.combine_text = combine_text
        self.recent = recent
        self.x = x
        self.y = y


@dataclass
class Item:
    operators = "+-*%&/=<>^"
    commands = "!|@"

    def __init__(self, text: str):
        self._text = ""
        self.set_text(text)

    def set_text(self, text: str):
        if len(text) >= 7:
            text = "∞"

        self._text = text

    def text(self):
        return self._text

    def get_visible_text(self):
        if self.text() == "*":
            return "×"
        elif self.text() == "/":
            return "÷"
        elif self.text() == "-":
            return "−"
        return self.text()

    def is_number(self):
        return (self.text().strip('-')).isnumeric() or self.text() == "∞"

    def is_operator(self):
        return self._text in Item.operators

    def is_command(self):
        return self._text in Item.commands

    def to_int(self):
        if self.text() == "∞":
            return 1000000
        return int(self._text)


def get_combine(left, operator, right):
    left_item = left.get_item()
    right_item = right.get_item()
    text = f"{left_item.text()} {operator} {right_item.text()}"
    x, y = centered_tile_pos_to_screen_pos(right.x, right.y)
    return CombineResult(text, x, y)


#  Recreate and move this prototype function to a class in the future
def combine_items(to_combine: list[Tile]):
    score = 0
    combines = []
    for i, tile in enumerate(to_combine):
        item = tile.get_item()
        if item is None:
            continue

        if i + 1 < len(to_combine) and True:
            next_tile = to_combine[i + 1]
            next_item = next_tile.get_item()
            if next_item is not None:
                if item.text() == "+" and next_item.text() == "+":
                    combines.append(get_combine(tile, '', next_tile))
                    # next_item.set_text("*")
                    tile.set_item(None)
                elif item.text() == "-" and next_item.text() == "-":
                    combines.append(get_combine(tile, '', next_tile))
                    # next_item.set_text("+")
                    tile.set_item(None)
                elif item.text() == "*" and next_item.text() == "*":
                    combines.append(get_combine(tile, '', next_tile))
                    # next_item.set_text("^")
                    tile.set_item(None)
                elif item.text() == "/" and next_item.text() == "/":
                    combines.append(get_combine(tile, '', next_tile))
                    # next_item.set_text("-")
                    tile.set_item(None)

        if item.is_operator() and 0 < i < (len(to_combine) - 1):
            left_tile = to_combine[i - 1]
            right_tile = to_combine[i + 1]
            left = left_tile.get_item()
            right = right_tile.get_item()
            if right is None or left is None:
                continue
            if left.is_number() and right.is_number():
                if item.text() == "&":
                    if right.text() != "∞" and left.text() != "∞" and right.is_number() and right.to_int() >= 0:
                        combines.append(get_combine(left_tile, '&', right_tile))
                        right.set_text(left.text() + right.text())
                        to_combine[i - 1].set_item(None)
                        to_combine[i].set_item(None)
                        score += 1
                elif item.text() == "+":
                    combines.append(get_combine(left_tile, '+', right_tile))
                    right.set_text(str(left.to_int() + right.to_int(), ))
                    to_combine[i - 1].set_item(None)
                    to_combine[i].set_item(None)
                    score += 1
                elif item.text() == "-" and left.to_int() >= right.to_int():
                    combines.append(get_combine(left_tile, '−', right_tile))
                    right.set_text(str(left.to_int() - right.to_int()))
                    to_combine[i - 1].set_item(None)
                    to_combine[i].set_item(None)
                    score += 1
                elif item.text() == "*":
                    combines.append(get_combine(left_tile, '×', right_tile))
                    right.set_text(str(left.to_int() * right.to_int()))
                    to_combine[i - 1].set_item(None)
                    to_combine[i].set_item(None)
                    score += 1
                elif item.text() == "%":
                    try:
                        text = str(left.to_int() % right.to_int())
                        combines.append(get_combine(left_tile, '%', right_tile))
                        right._text = text
                        to_combine[i - 1].set_item(None)
                        to_combine[i].set_item(None)
                        score += 2
                    except ZeroDivisionError:
                        pass
                elif item.text() == "^":
                    combines.append(get_combine(left_tile, '^', right_tile))
                    right.set_text(str(left.to_int() ** right.to_int()))
                    to_combine[i - 1].set_item(None)
                    to_combine[i].set_item(None)
                    score += 1
                elif item.text() == "/":
                    division = 0.5
                    try:
                        division = left.to_int() / right.to_int()
                    except ZeroDivisionError:
                        pass
                    if division.is_integer():
                        combines.append(get_combine(left_tile, '÷', right_tile))
                        right.set_text(str(int(division)))
                        to_combine[i - 1].set_item(None)
                        to_combine[i].set_item(None)
                        score += 5
                elif item.text() == "=":
                    if left.to_int() == right.to_int():
                        combines.append(get_combine(left_tile, '=', right_tile))
                        to_combine[i - 1].set_item(None)
                        to_combine[i].set_item(None)
                        to_combine[i + 1].set_item(None)
                        score += 10

            if right.is_number():
                if right.to_int() == 0:
                    to_combine[i + 1].set_item(None)

            if to_combine[i - 1].has_item() and to_combine[i].has_item():
                pass  # did not combine
            else:
                if item.text() == "=":
                    Audio.play_sound('explode')
                else:
                    Audio.play_sound('combine')

    return score, combines
