# game.py
# Controls main Tetris game logic

import pygame, random
from board import Board, BLOCK_SIZE
from block import Block
from file_io import load_game_data, save_game_data
from board import COLS, BLOCK_SIZE


class Game:
    def __init__(self):
        self.board = Board()
        self.current = Block(3, 0)
        self.next_block = Block(3, 0)
        self.drop_speed = 500  # milliseconds per drop
        self.last_drop_time = pygame.time.get_ticks()
        self.score = 0
        self.data = load_game_data()
        self.high_score = self.data["high_score"]
        self.lines_cleared = 0
        self.level = 1

    def new_block(self):
        self.current = self.next_block
        self.next_block = Block(3, 0)
        if not self.board.valid_move(self.current.shape, self.current.x, self.current.y):
            return False  # Game over
        return True

    def move(self, dx, dy):
        if self.board.valid_move(self.current.shape, self.current.x + dx, self.current.y + dy):
            self.current.x += dx
            self.current.y += dy
            return True
        return False

    def rotate(self):
        old_shape = self.current.shape
        self.current.rotate()
        if not self.board.valid_move(self.current.shape, self.current.x, self.current.y):
            self.current.shape = old_shape

    def drop(self):
        """Control the logic of block falling, scoring and upgrading"""
        now = pygame.time.get_ticks()
        if now - self.last_drop_time > self.drop_speed:
            self.last_drop_time = now
            if not self.move(0, 1):
                # The cube landed.
                self.board.lock_shape(self.current.shape, self.current.color, self.current.x, self.current.y)
                cleared = self.board.clear_lines()

                if cleared > 0:
                    self.score += cleared * 100
                    old_level = self.level
                    self.lines_cleared += cleared

                    # Each time 10 lines are cleared, you will advance to the next level (and you can advance multiple times).
                    new_level = self.lines_cleared // 10 + 1
                    if new_level > old_level:
                        self.level = new_level
                        self.drop_speed = max(150, 500 - (self.level - 1) * 50)  # 最快不低于150ms

                    # Update the highest score
                    if self.score > self.high_score:
                        self.high_score = self.score
                        self.data["high_score"] = self.high_score
                        self.data["max_level"] = max(self.level, self.data["max_level"])
                        save_game_data(self.data)

                # Generate a new block
                if not self.new_block():
                    return False  # Game Over
        return True

    def draw(self, surface):
        self.board.draw(surface)
        shape = self.current.shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(surface, self.current.color,
                                     ((self.current.x + x) * BLOCK_SIZE,
                                      (self.current.y + y) * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE))

    def draw_next_block(self, surface):
        """Display next block preview on the right side"""
        import pygame
        font = pygame.font.SysFont("Arial", 20)
        text = font.render("Next:", True, (255, 255, 255))
        surface.blit(text, (COLS * BLOCK_SIZE + 10, 50))
        shape = self.next_block.shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(surface, self.next_block.color,
                                     (COLS * BLOCK_SIZE + 10 + x * 20,
                                      80 + y * 20, 20, 20))
                    # Operation Instruction Text
                    control_font = pygame.font.SysFont("Arial", 18)
                    controls_title = control_font.render("Controls:", True, (200, 200, 200))
                    surface.blit(controls_title, (COLS * BLOCK_SIZE + 10, 180))

                    # button instruction
                    controls = [
                        ("← → : Move", (COLS * BLOCK_SIZE + 10, 205)),
                        ("↑ : Rotate", (COLS * BLOCK_SIZE + 10, 225)),
                        ("↓ : Drop faster", (COLS * BLOCK_SIZE + 10, 245)),
                        ("P : Pause", (COLS * BLOCK_SIZE + 10, 265)),
                        ("R : Restart", (COLS * BLOCK_SIZE + 10, 285)),
                        ("ESC : Quit", (COLS * BLOCK_SIZE + 10, 305)),
                    ]

                    for text, pos in controls:
                        line = control_font.render(text, True, (180, 180, 180))
                        surface.blit(line, pos)
