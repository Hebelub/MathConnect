from Board import Board
from Item import Item, CombineResult
import random
from Audio import Audio
from ParticleSystem import ParticleSystem
from Direction import Direction


class GameState:
    def __init__(self):
        self.score = 0
        self.game_over = False

        self.particle_system = ParticleSystem()

        self.board = Board(4, 4)

        self.sequence = []
        self.sequence = [self.generate_random_item() for _ in range(5)]

        self.next_tiles = [random.choice(self.board.get_tiles())]
        self.combine_list = []
        self.add_next_in_sequence()

    def empty_next_tiles(self):
        empty_tiles = []
        for tile in self.next_tiles:
            if tile.is_empty():
                empty_tiles.append(tile)
        return empty_tiles

    def add_next_in_sequence(self):
        random.choice(self.empty_next_tiles()).set_item(self.sequence[0])
        self.sequence.pop(0)
        self.sequence.append(self.generate_random_item())
        self.next_tiles = self.board.get_next_tiles()

    def execute_move(self, direction):
        if self.game_over:
            return

        if self.board.can_swipe(direction):
            score, combines = self.board.swipe(direction)

            # update score
            self.score += score

            # did the move do any combining?
            if len(combines) > 0:
                # set our current combines to not be recent
                # will be drawn smaller in GUI
                for combine in self.combine_list:
                    combine.recent = False

                # add the recent combines
                self.combine_list.extend(combines)

                # add particles to where the combines happened
                for combine in combines:
                    for i in range(25):
                        self.particle_system.add_particle(combine.x, combine.y)

            self.add_next_in_sequence()
        else:
            print(f"Couldn't swipe {direction.name}")
            Audio.play_sound('error')

        if self.is_game_over():
            print("Game over! Total Score: " + str(self.score))
            self.game_over = True
            Audio.play_sound('gameover')

    def is_game_over(self):
        for d in Direction:
            if self.board.can_swipe(d):
                return False
        return True

    def generate_random_item(self):
        numbers = "2468"  # "123456789"
        operators = "+-/*"  
        # operators = "&/*^+-=%"

        num_numbers = 0
        num_operators = 0
        for item in self.board.get_items() + self.sequence:
            if item.is_number():
                num_numbers += 1
            else:
                num_operators += 1

        if num_operators == num_numbers:
            item = random.choice(numbers + operators)
        elif num_operators > num_numbers:
            item = random.choice(numbers)
        else:
            item = random.choice(operators)
        return Item(item)
