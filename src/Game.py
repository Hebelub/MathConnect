from Board import Board
from Item import Item, CombineResult
import random
from Audio import Audio
from ParticleSystem import ParticleSystem
from Direction import Direction
from GameState import GameState


class Game:
    def __init__(self):
        # self.seed = 3
        # random.seed(self.seed)
        self.game_state = GameState()
        self.paused = False

        # self.particle_system = ParticleSystem()

    def receive_move_input(self, direction: Direction):
        if self.paused:
            return

        # Should check for if animation is done

        # Throw a data object inn as a parameter
        # it should be filled with:
        # sounds to create
        # animations like:
        # combines
        # slides
        # The game passes it to Animation, Audio etc

        # Another choice could be:
        # GameState and everything under knows about latest events
        # Game could then utilize that info other places
        self.game_state.execute_move(direction)
