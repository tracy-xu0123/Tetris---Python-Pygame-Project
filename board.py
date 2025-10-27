# board.py
# Manages the Tetris game board and collision logic

import pygame

ROWS = 20
COLS = 10
BLOCK_SIZE = 30

class Board:
    def __init__(self):
        self.grid = [[(0, 0, 0) for _ in range(COLS)] for _ in range(ROWS)]

    def draw(self, surface):
        for y in range(ROWS):
            for x in range(COLS):
                pygame.draw.rect(surface, self.grid[y][x],
                                 (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                pygame.draw.rect(surface, (40, 40, 40),
                                 (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def valid_move(self, shape, offset_x, offset_y):
        """Check if shape is valid at new position"""
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = offset_x + x
                    new_y = offset_y + y
                    if new_x < 0 or new_x >= COLS or new_y >= ROWS:
                        return False
                    if new_y >= 0 and self.grid[new_y][new_x] != (0, 0, 0):
                        return False
        return True

    def lock_shape(self, shape, color, pos_x, pos_y):
        """Lock shape into grid"""
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[pos_y + y][pos_x + x] = color

    def clear_lines(self):
        """Remove completed rows and return number cleared"""
        new_grid = [row for row in self.grid if (0, 0, 0) in row]
        cleared = ROWS - len(new_grid)
        while len(new_grid) < ROWS:
            new_grid.insert(0, [(0, 0, 0) for _ in range(COLS)])
        self.grid = new_grid
        return cleared
