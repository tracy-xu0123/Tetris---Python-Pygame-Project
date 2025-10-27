# block.py
# Defines all Tetris block shapes and behavior

import random

# 7 standard Tetris shapes
SHAPES = [
    [[1, 1, 1, 1]],                      # I
    [[1, 1], [1, 1]],                    # O
    [[0, 1, 0], [1, 1, 1]],              # T
    [[1, 0, 0], [1, 1, 1]],              # J
    [[0, 0, 1], [1, 1, 1]],              # L
    [[1, 1, 0], [0, 1, 1]],              # S
    [[0, 1, 1], [1, 1, 0]]               # Z
]

COLORS = [
    (0, 255, 255),  # I - Cyan
    (255, 255, 0),  # O - Yellow
    (128, 0, 128),  # T - Purple
    (0, 0, 255),    # J - Blue
    (255, 165, 0),  # L - Orange
    (0, 255, 0),    # S - Green
    (255, 0, 0)     # Z - Red
]

class Block:
    def __init__(self, x, y):
        idx = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[idx]
        self.color = COLORS[idx]
        self.x = x
        self.y = y

    def rotate(self):
        """Rotate the shape clockwise"""
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
