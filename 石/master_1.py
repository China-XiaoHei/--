import pygame
import random

# --- 全局常量 ---
# 屏幕尺寸
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
PLAY_WIDTH = 300  # 游戏区域宽度 (10 * 30)
PLAY_HEIGHT = 600 # 游戏区域高度 (20 * 30)
BLOCK_SIZE = 30    # 每个方块的大小

# 游戏区域左上角的坐标
TOP_LEFT_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = SCREEN_HEIGHT - PLAY_HEIGHT - 50

# --- 方块形状定义 ---
# S, Z, I, O, J, L, T
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

SHAPES = [S, Z, I, O, J, L, T]
SHAPE_COLORS = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# 颜色: 绿, 红, 青, 黄, 橙, 蓝, 紫

# --- 颜色定义 ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
YELLOW = (255, 255, 0)

# --- 类定义 ---

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0

# --- 游戏核心函数 ---

def create_grid(locked_positions={}):
    """创建游戏网格"""
    grid = [[BLACK for _ in range(10)] for _ in range(20)]

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in locked_positions:
                c = locked_positions[(x, y)]
                grid[y][x] = c
    return grid

def convert_shape_format(piece):
    """将方块的格式转换为坐标列表"""
    positions = []
    shape_format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))

    # 移除偏移
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

def valid_space(piece, grid):
    """检查方块是否在有效空间内"""
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == BLACK] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(piece)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    """检查游戏是否结束"""
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    """随机获取一个新方块"""
    return Piece(5, 0, random.choice(SHAPES))

def draw_text_middle(surface, text, size, color):
    """在屏幕中央绘制文本"""
    # *** 修改点 1: 使用 Pygame 默认字体 ***
    font = pygame.font.Font(None, size)
    label = font.render(text, 1, color)
    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH / 2 - (label.get_width() / 2),
                         TOP_LEFT_Y + PLAY_HEIGHT / 2 - label.get_height() / 2))

def draw_grid(surface, grid):
    """绘制网格线"""
    for i in range(len(grid)):
        pygame.draw.line(surface, GRAY, (TOP_LEFT_X, TOP_LEFT_Y + i * BLOCK_SIZE),
                         (TOP_LEFT_X + PLAY_WIDTH, TOP_LEFT_Y + i * BLOCK_SIZE))
    for j in range(len(grid[0])):
        pygame.draw.line(surface, GRAY, (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y),
                         (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + PLAY_HEIGHT))

def clear_rows(grid, locked):
    """清除满行并返回清除的行数"""
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if BLACK not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                new_key = (x, y + inc)
                locked[new_key] = locked.pop(key)
    return inc

def draw_next_shape(shape, surface):
    """在侧边栏绘制下一个方块"""
    # *** 修改点 2: 使用 Pygame 默认字体 ***
    font = pygame.font.Font(None, 30)
    label = font.render('Next Shape', 1, WHITE)

    sx = TOP_LEFT_X + PLAY_WIDTH + 50
    sy = TOP_LEFT_Y + PLAY_HEIGHT / 2 - 100
    shape_format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j * BLOCK_SIZE, sy + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    surface.blit(label, (sx + 10, sy - 30))

def draw_window(surface, grid, score=0, last_score=0):
    """绘制主游戏窗口"""
    surface.fill(BLACK)

    pygame.font.init()
    # *** 修改点 3: 使用 Pygame 默认字体 ***
    font = pygame.font.Font(None, 60)
    label = font.render('TETRIS', 1, WHITE)
    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH / 2 - (label.get_width() / 2), 30))

    # 显示当前分数
    # *** 修改点 4: 使用 Pygame 默认字体 ***
    font = pygame.font.Font(None, 30)
    label = font.render('Score: ' + str(score), 1, WHITE)
    sx = TOP_LEFT_X + PLAY_WIDTH + 50
    sy = TOP_LEFT_Y + PLAY_HEIGHT / 2 - 100
    surface.blit(label, (sx + 20, sy + 160))

    # 显示最高分
    label = font.render('High Score: ' + str(last_score), 1, WHITE)
    surface.blit(label, (sx + 20, sy + 200))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    pygame.draw.rect(surface, (255, 0, 0), (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)
    draw_grid(surface, grid)

def update_score(nscore):
    """更新最高分文件"""
    score = max_score()

    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))

def max_score():
    """读取最高分"""
    try:
        with open('scores.txt', 'r') as f:
            lines = f.readlines()
            score = lines[0].strip()
    except:
        score = "0"
    return score

def main(win):
    """主游戏循环"""
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        # 随着时间推移增加下落速度
        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        # 方块自动下落
        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

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
                        change_piece = True
                elif event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -= 1
                elif event.key == pygame.K_SPACE:
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                    change_piece = True

        shape_pos = convert_shape_format(current_piece)

        # 将当前方块的坐标和颜色添加到网格中
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # 如果方块已经落地
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            cleared_rows = clear_rows(grid, locked_positions)
            # 根据清除的行数更新分数
            if cleared_rows == 1:
                score += 40
            elif cleared_rows == 2:
                score += 100
            elif cleared_rows == 3:
                score += 300
            elif cleared_rows == 4: # TETRIS!
                score += 1200

        draw_window(win, grid, score, last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(win, "YOU LOST!", 80, WHITE)
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)

def main_menu(win):
    """主菜单"""
    run = True
    while run:
        win.fill(BLACK)
        # *** 修改点 5: 使用 Pygame 默认字体 ***
        draw_text_middle(win, 'Press Any Key To Play', 60, WHITE)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)
    pygame.quit()

if __name__ == "__main__":
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')
    main_menu(win)
