from GameState import GameState
from Game import Game
import pygame
from Definitions import *
from Utility import add_to_color, tile_corner_center_offset

pygame.font.init()
game_font = pygame.font.Font('assets/Satoshi.ttf', 72)
game_font_medium = pygame.font.Font('assets/Satoshi.ttf', 55)
game_font_small = pygame.font.Font('assets/Satoshi.ttf', 40)
game_font_mini = pygame.font.Font('assets/Satoshi.ttf', 28)


def draw_text(text, center_position, surface, alpha=1.0, color=BLACK, font=game_font):
    text_surface = font.render(text, True, color)
    text_surface.set_alpha(alpha * 255)
    x = center_position[0] - (text_surface.get_width() / 2)
    y = center_position[1] - (text_surface.get_height() / 2)
    surface.blit(text_surface, (x, y))


def draw_board(surface: pygame.Surface, game: GameState):
    for i, item in enumerate(game.sequence):
        x = SEQUENCE_DRAW_X + i * (TILE_SIZE + TILE_OFFSET)
        y = SEQUENCE_DRAW_Y
        color = add_to_color(SEQUENCE_COLOR, i * - 25)
        pygame.draw.rect(surface, color, pygame.Rect(x, y, TILE_SIZE, TILE_SIZE), border_radius=10)
        draw_text(item.get_visible_text(), tile_corner_center_offset(x, y), surface)

    for tile in game.board.get_tiles():
        x = BOARD_DRAW_X + tile.x * (TILE_SIZE + TILE_OFFSET)
        y = BOARD_DRAW_Y + tile.y * (TILE_SIZE + TILE_OFFSET)
        pygame.draw.rect(surface, TILE_COLOR, pygame.Rect(x, y, TILE_SIZE, TILE_SIZE), border_radius=10)
        if tile in game.next_tiles:
            pygame.draw.rect(surface, NEXT_TILE_COLOR, pygame.Rect(x, y, TILE_SIZE, TILE_SIZE), 4, border_radius=10)

            ox, oy = tile_corner_center_offset(x, y)
            draw_text(game.sequence[0].get_visible_text(),
                      (ox - TILE_SIZE / 3.5, oy - TILE_SIZE / 3.5),
                      surface, alpha=1, color=SEQUENCE_COLOR,
                      font=game_font_mini)

        if tile.has_item():
            if len(tile.item.get_visible_text()) >= 6:
                font = game_font_mini
            elif len(tile.item.get_visible_text()) >= 4:
                font = game_font_small
            elif len(tile.item.get_visible_text()) >= 3:
                font = game_font_medium
            else:
                font = game_font

            color = BLACK if tile.item.is_number() else OPERATOR

            draw_text(tile.get_item().get_visible_text(),
                      tile_corner_center_offset(x, y),
                      surface, font=font, color=color)

    draw_text("Score", (685, BOARD_DRAW_Y), surface, font=game_font_small, color=WHITE)
    font = game_font_mini if len(str(game.score)) >= 8 else game_font_small
    draw_text(str(game.score), (685, BOARD_DRAW_Y + 50), surface, font=font, color=WHITE)

    draw_text("Combos", (685, BOARD_DRAW_Y + 120), surface, font=game_font_small, color=WHITE)
    for i, combine in enumerate(reversed(game.combine_list[-8:])):
        text = combine.combine_text
        font = game_font_small if combine.recent else game_font_mini
        draw_text(text, (685, BOARD_DRAW_Y + 170 + 50 * i), surface, font=font, color=WHITE)


def draw_particles(surface, game: GameState):
    particles = game.particle_system.get_particles()

    for p in particles:
        pygame.draw.circle(surface, p.color, (p.x, p.y), p.radius)
