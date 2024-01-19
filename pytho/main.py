import pygame
from copy import deepcopy
from random import choice, randrange

W, H = 10, 20
TILE = 45
GAME_RES = W * TILE, H * TILE
RES = 750, 940

pygame.init()
game_sc = pygame.display.set_mode(GAME_RES)
clock = pygame.time.Clock()

grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)] #сетка поля

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]] #фигуры

figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos] #берем фигуры из списка
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2) #отрисовывает части фигуры
field = [[0 for i in range(W)] for j in range(H)]#карта поля с положением фигур

anim_count, anim_speed, anim_limit = 0, 60, 2000 #плавность падения

get_color = lambda: (randrange(30, 256), randrange(30, 256), randrange(30, 256)) #получение цвета фигур

figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures)) #выбор системой случайной фигуры
color, next_color = get_color(), get_color() #выбор системой случайного цвета фигуры

#границы
def check_borders():
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True


while True:
    dx, rotate = 0, False
    game_sc.fill(pygame.Color('white'))
    #управление
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:
                anim_limit = 100
            elif event.key == pygame.K_UP:
                rotate = True
    # копия фигуры и граница
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_borders():
            figure = deepcopy(figure_old)
            break
    # счетчик
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_borders():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = color
                figure, color = next_figure, next_color
                next_figure, next_color = deepcopy(choice(figures)), get_color()
                anim_limit = 1000
                break
    # переворотка фигур
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders():
                figure = deepcopy(figure_old)
                break
    # проверка гориз линий
    line = H - 1
    for row in range(H - 1, -1, -1):
        count = 0
        for i in range(W):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < W:
            line -= 1
    #зачисление очков
    score += scores[lines]
    [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid] #рисует поле
    for i in range(4):
        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE
        pygame.draw.rect(game_sc, color, figure_rect) #рисует фигуры
    # отрисовываем фигуры на карте поля
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pygame.draw.rect(game_sc, col, figure_rect)
    # отрисовывем следующую фигуру
    for i in range(4):
        figure_rect.x = next_figure[i].x * TILE + 380
        figure_rect.y = next_figure[i].y * TILE + 180
        pygame.draw.rect(sc, next_color, figure_rect)
    # конец игры
    for i in range(W):
        if field[0][i]:
            field = [[0 for i in range(W)] for i in range(H)]
            anim_count, anim_speed, anim_limit = 0, 60, 2000
            score = 0

    pygame.display.flip()
