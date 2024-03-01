import pygame
import random
from typing import List

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
GRID_SIZE = (10, 20)
CELL_SIZE = 30
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 0, 0),      # Empty cell
    (0, 255, 255),  # Cyan
    (0, 0, 255),    # Blue
    (255, 128, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (255, 0, 0),    # Red
    (128, 0, 255)   # Purple
]

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

# Tetrimino shapes
# tetriminos = [
#     [[1, 1, 1, 1]],  # I
#     [[2, 2, 0], [0, 2, 2]],  # Z
#     [[0, 3, 3], [3, 3, 0]],  # S
#     [[4, 4], [4, 4]],  # O
#     [[0, 5, 0], [5, 5, 5]],  # T
#     [[6, 0, 0], [6, 6, 6]],  # J
#     [[0, 0, 7], [7, 7, 7]]   # L
# ]


def create_grid(locked_positions={}):
    grid = [[0 for _ in range(GRID_SIZE[0])] for _ in range(GRID_SIZE[1])]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid

# def convert_shape_format(shape):
#     positions = []
#     format = shape.shape[shape.rotation % len(shape.shape)]
#
#     for i, line in enumerate(format):
#         row = list(line)
#         for j, column in enumerate(row):
#             if column == '0':
#                 positions.append((shape.x + j, shape.y + i))
#
#     return positions

# def convert_shape_format(shape):
#     positions = []
#     format = shape.shape[shape.rotation % len(shape.shape)]
#
#     for i, line in enumerate(format):
#         for j, column in enumerate(line):
#             if column != 0:
#                 positions.append((shape.x + j, shape.y + i))
#
#     return positions

# def convert_shape_format(shape):
#     positions = []
#     format = shape.shape[shape.rotation % len(shape.shape)]
#
#     for i, line in enumerate(format):
#         for j, column in enumerate(line):
#             if column != 0:
#                 # Adjust position based on the shape's x and y coordinates
#                 positions.append((shape.x + j, shape.y + i))
#
#     return positions

# Tetrimino shapes


# tetriminos = [
#     [[1, 1, 1, 1]],  # I
#     [[2, 2, 0], [0, 2, 2]],  # Z
#     [[0, 3, 3], [3, 3, 0]],  # S
#     [[4, 4], [4, 4]],  # O
#     [[0, 5, 0], [5, 5, 5]],  # T
#     [[6, 0, 0], [6, 6, 6]],  # J
#     [[0, 0, 7], [7, 7, 7]]   # L
# ]

# def convert_shape_format(shape):
#     positions = []
#     format = shape.shape[shape.rotation % len(shape.shape)]
#
#     for i, line in enumerate(format):
#         for j, column in enumerate(line):
#             if column != 0:
#                 positions.append((shape.x + j, shape.y + i))
#
#     return positions
class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = COLORS[tetriminos.index(shape)]
        self.rotation = 0

tetriminos = [
    [[1, 1, 1, 1]],  # I
    [[2, 2, 0], [0, 2, 2]],  # Z
    [[0, 3, 3], [3, 3, 0]],  # S
    [[4, 4], [4, 4]],  # O
    [[0, 5, 0], [5, 5, 5]],  # T
    [[6, 0, 0], [6, 6, 6]],  # J
    [[0, 0, 7], [7, 7, 7]]   # L
]
def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, row in enumerate(format):  # Treat each element in 'format' as a row
        for j, cell in enumerate(row):  # Iterate over cells in the row
            if cell != 0:
                positions.append((shape.x + j, shape.y + i))

    return positions

def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(GRID_SIZE[0]) if grid[i][j] == 0] for i in range(GRID_SIZE[1])]
    accepted_pos = [j for sub in accepted_pos for j in sub]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    return Piece(5, 0, random.choice(tetriminos))

# class Piece(object):
#     rows = GRID_SIZE[1]
#     columns = GRID_SIZE[0]
#
#     def __init__(self, x, y, shape):
#         self.x = x
#         self.y = y
#         self.shape = shape
#         self.color = COLORS[tetriminos.index(shape)]
#         self.rotation = 0

def draw_grid(surface, grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, COLORS[grid[i][j]],
                             (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)

    # Draw grid lines
    for i in range(GRID_SIZE[1]):
        pygame.draw.line(surface, WHITE, (0, i * CELL_SIZE), (SCREEN_WIDTH, i * CELL_SIZE))
    for j in range(GRID_SIZE[0]):
        pygame.draw.line(surface, WHITE, (j * CELL_SIZE, 0), (j * CELL_SIZE, SCREEN_HEIGHT))

def draw_window(surface, grid):
    surface.fill(BLACK)
    draw_grid(surface, grid)
    pygame.display.update()

def main():
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1

                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                elif event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

        draw_window(screen, grid)

        if check_lost(locked_positions):
            run = False

    pygame.display.quit()

main()
