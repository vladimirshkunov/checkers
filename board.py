import pygame

WHITE = 'white'
BLACK = 'black'
COLOR = WHITE


def color_opponent():
    if COLOR == BLACK:
        return WHITE
    return BLACK


def check_bqueen(board):  # проверка есть ли белые шашки расположенные на линии дамок
    sp = []
    for i in range(1, 8, 2):
        b = board[0][i]
        if b != None:
            if b.color == BLACK and b.__class__.__name__ == 'Usual':
                sp.append(i)
    return sp


def check_wqueen(board):
    sp = []
    for i in range(0, 7, 2):
        b = board[7][i]
        if b != None:
            if b.color == WHITE and b.__class__.__name__ == 'Usual':
                sp.append(i)
    return sp


class Shapes:
    def __init__(self, color):
        self.color = color


class Queen(Shapes):
    def can_move(self, board, x, y, pos_att):
        sp_kill = []
        for i, j in pos_att:
            sp_kill1 = []
            if abs(j - y) == abs(i - x) and board[j][i] == None:
                if (j > y) and (i > x):
                    v_step, h_step = 1, 1
                elif (j > y) and (i < x):
                    v_step, h_step = 1, -1
                elif (j < y) and (i < x):
                    v_step, h_step = -1, -1
                elif (j < y) and (i > x):
                    v_step, h_step = -1, 1

                for i1 in range(abs(j - y)):
                    iv = -i1 if v_step == -1 else i1
                    ih = -i1 if h_step == -1 else i1
                    if board[y + v_step + iv][x + h_step + ih] != None:
                        if board[y + v_step + iv][x + h_step + ih].color == COLOR:
                            return False
                        sp_kill1.append([x + h_step + ih, y + v_step + iv])
                if len(sp_kill1) > 1: return False
                sp_kill.extend(sp_kill1)
                x, y = i, j
            else:
                return False
        if sp_kill == []:
            return 1
        return sp_kill


class Usual(Shapes):
    def can_move(self, board, x, y, pos_att):
        if (pos_att[0][0] == x + 1 or pos_att[0][0] == x - 1) and pos_att[0][1] == y + 1 and len(
                pos_att) == 1 and self.color == WHITE:
            if board[pos_att[0][1]][pos_att[0][0]] == None: return 1

        elif (pos_att[0][0] == x + 1 or pos_att[0][0] == x - 1) and pos_att[0][1] == y - 1\
                and len(pos_att) == 1 and self.color == BLACK:
            if board[pos_att[0][1]][pos_att[0][0]] == None: return 1

        else:
            sp_kill = []
            print('can_move: ', pos_att)
            for i, j in pos_att:
                print('wbrk')
                if (i == x + 2 or i == x - 2) and (j == y + 2 or j == y - 2) and board[j][i] == None:
                    kill = board[(j + y) // 2][(i + x) // 2]
                    print('kill: ', (j + y) // 2, (i + x) // 2)
                    if kill == None: return False

                    if kill.color == COLOR: return False

                    sp_kill.append([(i + x) // 2, (j + y) // 2])
                    x, y = i, j
            return sp_kill


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.field = [[None] * 8 for _ in range(8)]
        self.field[0][1] = Usual(WHITE)
        self.field[0][3] = Usual(WHITE)
        self.field[0][5] = Usual(WHITE)
        self.field[0][7] = Usual(WHITE)
        self.field[1][0] = Usual(WHITE)
        self.field[1][2] = Usual(WHITE)
        self.field[1][4] = Usual(WHITE)
        self.field[1][6] = Usual(WHITE)
        self.field[2][1] = Usual(WHITE)
        self.field[2][3] = Usual(WHITE)
        self.field[2][5] = Usual(WHITE)
        self.field[2][7] = Usual(WHITE)
        self.field[5][0] = Usual(BLACK)
        self.field[5][2] = Usual(BLACK)
        self.field[5][4] = Usual(BLACK)
        self.field[5][6] = Usual(BLACK)
        self.field[6][1] = Usual(BLACK)
        self.field[6][3] = Usual(BLACK)
        self.field[6][5] = Usual(BLACK)
        self.field[6][7] = Usual(BLACK)
        self.field[7][0] = Usual(BLACK)
        self.field[7][2] = Usual(BLACK)
        self.field[7][4] = Usual(BLACK)
        self.field[7][6] = Usual(BLACK)
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 50
        self.mouse_coords = []

    # настройка внешнего вида  (пока не тестировалось)
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        screen.fill('#ac9362', (
        self.left - 10, self.top - 10, self.cell_size * self.width + 20, self.cell_size * self.height + 20))
        font = pygame.font.Font(None, 35)
        text = font.render(f"Ходит {'белый ' if COLOR == WHITE else 'чёрный'} игрок", True, (255, 255, 255))
        screen.blit(text, (130, 10))
        font = pygame.font.Font(None, 17)
        text = font.render(
            f"A{''.join(' ' for i in range(13))}B              C              D              E              F              G              H",
            True, (0, 0, 0))
        screen.blit(text, (self.left + self.cell_size / 2, 40))
        for i in range(1, 9):
            text = font.render(str(i), True, (0, 0, 0))
            screen.blit(text, (self.left - 8, self.top + self.cell_size * (i - 0.5)))

        for i in range(self.height):
            for j in range(self.width):
                if i % 2:
                    color = '#f5f5dc' if j % 2 else '#964b00'
                else:
                    color = '#f5f5dc' if j % 2 == 0 else '#964b00'
                screen.fill(pygame.Color(color),
                            (self.left + self.cell_size * j, self.top + self.cell_size * i, self.cell_size,
                             self.cell_size), 0)
                if self.field[i][j]:
                    pygame.draw.circle(screen, self.field[i][j].color,
                                       (self.left + self.cell_size * (j + 0.5), self.top + self.cell_size * (i + 0.5)),
                                       self.cell_size // 2 - 2)
                    if self.field[i][j].__class__.__name__ == 'Queen':
                        pygame.draw.circle(screen, WHITE if self.field[i][j].color == BLACK else BLACK, (
                            self.left + self.cell_size * (j + 0.5), self.top + self.cell_size * (i + 0.5)),
                                           self.cell_size // 4, 4)
        if self.mouse_coords:
            x, y = self.mouse_coords[0]
            if self.field[y][x]:
                if self.field[y][x].color == COLOR:
                    screen.fill('blue', (
                    self.left + self.cell_size * x, self.top + self.cell_size * y, self.cell_size, self.cell_size))
                    pygame.draw.circle(screen, COLOR,
                                       (self.left + self.cell_size * (x + 0.5), self.top + self.cell_size * (y + 0.5)),
                                       self.cell_size // 2 - 2)
                    for i in range(self.height):
                        for j in range(self.width):
                            if self.field[y][x].can_move(self.field, x, y, ([j, i],)):
                                screen.fill('green',
                                            (self.left + self.cell_size * j, self.top + self.cell_size * i,
                                             self.cell_size, self.cell_size))

    def move(self, x, y, pos_att):
        if len(pos_att) < 1: return False
        for i, j in pos_att:
            if i > 7 or i < 0 or j < 0 or j > 7: return False

        s = self.field[y][x]
        if s == None: return False

        if s.color != COLOR: return False

        rez = s.can_move(self.field, x, y, pos_att)
        print(rez)
        if not rez: return False
        if rez == 1:
            self.field[pos_att[0][1]][pos_att[0][0]], self.field[y][x] = self.field[y][x], None
        elif len(rez) == len(pos_att):  # при атаке должно совпадать кол-во убранных шашек с кол-вом позиций атак
            self.field[pos_att[-1][1]][pos_att[-1][0]], self.field[y][x] = self.field[y][x], None
            for i, j in rez:
                self.field[j][i] = None
        else:
            return False
        sp_bq = check_bqueen(self.field)
        sp_wq = check_wqueen(self.field)
        for i in sp_wq:
            self.field[7][i] = Queen(WHITE)
        for i in sp_bq:
            self.field[0][i] = Queen(BLACK)
            print(2)
        return True

    def get_cell(self, mouse_pos):
        x, y = mouse_pos[0], mouse_pos[1]
        if self.left <= x <= self.left + self.width * self.cell_size and\
                self.top <= y <= self.top + self.height * self.cell_size:
            for i in range(self.height):
                for j in range(self.width):
                    if self.left + self.cell_size * j <= x <= self.left + self.cell_size * (j + 1) and\
                            self.top + self.cell_size * i <= y <= self.top + self.cell_size * (i + 1):
                        return j, i
        else:
            return None

    def on_click(self, cell_coords):
        global COLOR
        if cell_coords is not None:
            if len(self.mouse_coords) >= 1:
                # если второй раз нажимаешь на одну и ту же клетку
                if len(self.mouse_coords) == 1 and self.mouse_coords[-1] == cell_coords:
                    self.mouse_coords = []
                    return
                self.mouse_coords.append(cell_coords)
                if board.move(self.mouse_coords[0][0], self.mouse_coords[0][1], self.mouse_coords[1:]):
                    COLOR = color_opponent()
                self.mouse_coords = []
            if self.mouse_coords == []:
                self.mouse_coords = [cell_coords]

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


pygame.init()
size = 500, 500
# screen — холст, на котором нужно рисовать:
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Шашки')

board = Board(8, 8)
board.set_view(50, 50, 50)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                board.get_click(event.pos)
            if event.button == 3:  # возникает ошибка в том, что несколько раз записываются координаты при одном нажатии
                board.mouse_coords.append(board.get_cell(event.pos))
            print(board.mouse_coords)

    screen.fill((0, 0, 0))
    board.render(screen)
    pygame.display.flip()
