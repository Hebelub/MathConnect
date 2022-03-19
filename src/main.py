from Game import Game
from Direction import Direction
from Display import draw_board, draw_particles, BACKGROUND_COLOR
import pygame


def main():

    game = Game()

    pygame.init()
    surface = pygame.display.set_mode((800, 750))

    # Variable to keep the main loop running
    running = True
    clock = pygame.time.Clock()

    # Main loop
    while running:
        clock.tick(60)

        game.game_state.particle_system.update_particles(surface.get_width(), surface.get_height())

        # Look at every event in the queue
        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == pygame.KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_UP:
                    game.receive_move_input(Direction.UP)
                elif event.key == pygame.K_DOWN:
                    game.receive_move_input(Direction.DOWN)
                elif event.key == pygame.K_LEFT:
                    game.receive_move_input(Direction.LEFT)
                elif event.key == pygame.K_RIGHT:
                    game.receive_move_input(Direction.RIGHT)
                elif event.key == pygame.K_p:
                    game.paused = not game.paused
                elif event.key == pygame.K_r:
                    game = Game()

            # Did the user click the window close button? If so, stop the loop.
            elif event.type == pygame.QUIT:
                running = False

        surface.fill(BACKGROUND_COLOR)
        draw_board(surface, game.game_state)
        draw_particles(surface, game.game_state)
        pygame.display.flip()


if __name__ == '__main__':
    main()
