# main.py
# Entry point for Tetris Project

import pygame, sys
from game import Game
from board import BLOCK_SIZE, ROWS, COLS

WINDOW_WIDTH = COLS * BLOCK_SIZE + 150
WINDOW_HEIGHT = ROWS * BLOCK_SIZE

def show_start_screen(screen, font, high_score):
    """Display the start menu before the game begins."""
    import pygame, sys
    title_font = pygame.font.SysFont("Arial", 40, bold=True)
    small_font = pygame.font.SysFont("Arial", 24)

    while True:
        screen.fill((0, 0, 0))
        title = title_font.render("TETRIS", True, (255, 255, 0))
        subtitle = small_font.render("COMP9001 Final Project", True, (255, 255, 255))
        info1 = small_font.render("Press ENTER to Start", True, (0, 255, 0))
        info2 = small_font.render("Press ESC to Quit", True, (255, 0, 0))
        highscore_text = small_font.render(f"High Score: {high_score}", True, (255, 255, 255))

        # 居中显示
        screen.blit(title, (80, 180))
        screen.blit(subtitle, (60, 230))
        screen.blit(highscore_text, (60, 280))
        screen.blit(info1, (60, 330))
        screen.blit(info2, (60, 370))

        pygame.display.update()

        # 检测按键事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter 启动游戏
                    return
                elif event.key == pygame.K_ESCAPE:  # Esc 退出
                    pygame.quit()
                    sys.exit()

def main():
    pygame.init()
    pygame.display.set_caption("Tetris - COMP9001 Final Project")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 22)
    game = Game()
    running = True

    paused = False
    # 显示开始菜单（传入最高分）
    show_start_screen(screen, font, game.high_score)

    while running:
        screen.fill((0, 0, 0))
        # ✅ 绘制右侧“Next Block”区域背景（与主区域颜色区分）
        next_area_x = COLS * BLOCK_SIZE
        pygame.draw.rect(screen, (20, 20, 20), (next_area_x, 0, 150, WINDOW_HEIGHT))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    game.move(0, 1)
                elif event.key == pygame.K_UP:
                    game.rotate()
                elif event.key == pygame.K_p:  # 新增暂停功能
                    paused = not paused

                elif event.key == pygame.K_r:  # 新增重启功能
                    game = Game()
                    paused = False

        if paused:
            pause_text = font.render("PAUSED - Press P to Resume", True, (255, 255, 0))
            screen.blit(pause_text, (20, WINDOW_HEIGHT // 2))
        else:
            if not game.drop():
                text = font.render("GAME OVER! Press ESC to exit", True, (255, 0, 0))
                screen.blit(text, (20, WINDOW_HEIGHT // 2))
            else:
                game.draw(screen)
                game.draw_next_block(screen)
                score_text = font.render(f"Score: {game.score} | High: {game.high_score}", True, (255, 255, 255))
                screen.blit(score_text, (10, 10))
                # ✅ 新增：显示等级
                level_text = font.render(f"Level: {game.level}", True, (255, 255, 255))
                screen.blit(level_text, (10, 40))

        pygame.display.update()
        clock.tick(30)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
