import random
import numpy as np


class Ship:
    def __init__(self, size, x, y, rotation, status='alive'):
        self.dots = []
        for i in range(size):
            if rotation == 'h':
                self.dots.append((x + i, y))
            else:
                self.dots.append((x, y + i))
        self.status = status


class Board:
    def __init__(self, player=None):
        self.user_field = np.array([['·'] * 6 for _ in range(6)])
        self.ai_field = np.array([['·'] * 6 for _ in range(6)])
        self.ai_field_game = np.array([['·'] * 6 for _ in range(6)])
        self.user_not_empty_cells = []
        self.ai_not_empty_cells = []
        self.user_ships = []
        self.ai_ships = []

    def random_board(self, player):
        sizes = [3, 2, 2, 1, 1, 1, 1]
        ships = []
        for size in sizes:
            counter = 0
            while True:
                rotation = random.choice(['v', 'h'])
                x, y = 5, 5
                if rotation == 'h':
                    x = 5 - size
                else:
                    y = 5 - size
                new_ship = Ship(size, random.randint(0, x), random.randint(0, y), rotation)
                for dot in new_ship.dots:
                    if player == 'user':
                        if dot in self.user_not_empty_cells:
                            break
                    else:
                        if dot in self.ai_not_empty_cells:
                            break
                else:
                    if player == 'user':
                        self.user_ships.append(new_ship.dots)
                    else:
                        self.ai_ships.append(new_ship.dots)
                    self.add_ship(new_ship, player)
                    ships.append(new_ship)
                    break
                counter += 1
                if counter > 50:
                    raise RecursionError

    def add_ship(self, ship, player):
        for x, y in ship.dots:
            if y in range(0, 6) and x in range(0, 6):
                if player == 'user':
                    self.user_field[y, x] = '■'
                    self.user_not_empty_cells.append((x, y))
                else:
                    self.ai_field[y, x] = '■'
                    self.ai_not_empty_cells.append((x, y))
            self.contour(x, y, player)

    def contour(self, x, y, player):
        for row in range(y - 1, y + 2):
            for col in range(x - 1, x + 2):
                if row in range(0, 6) and col in range(0, 6):
                    if player == 'user':
                        if self.user_field[row, col] == '·':
                            self.user_field[row, col] = '*'
                            self.user_not_empty_cells.append((col, row))
                    else:
                        if self.ai_field[row, col] == '·':
                            self.ai_field[row, col] = '*'
                            self.ai_not_empty_cells.append((col, row))


    def __str__(self):
        all_fields = ''
        abc = 'АБВГДЕ'
        for field in (self.user_field, self.ai_field):
            str_field = '  1 2 3 4 5 6\n'
            for i, row in enumerate(field, start=1):
                str_field += f'{abc[i-1]} ' + ' '.join(row) + '\n'
            all_fields += str_field
            all_fields += '\n'
        return all_fields


class Game:
    def __init__(self, board):
        self.board = board
        self.user_shoots = []
        self.ai_shoots = []
        self.destroyed_ai_ships = 0
        self.destroyed_user_ships = 0
        self.active_player = 'user'
        self.endgame = False

    def change_player(self):
        if self.active_player == 'user':
            self.active_player = 'user'
        else:
            self.active_player = 'user'

    def check_destroy(self, col, row):
        if self.active_player == 'user':
            ai_ships = self.board.ai_ships
            print(ai_ships)
            print(self.board.user_ships)
            for ship in ai_ships:
                if (row, col) in ship:
                    print(ship)
                    for item in ship:
                        if item not in self.user_shoots:
                            print('Ранил!')
                            return False
                    print(132)
                    print('Убил!')
                    self.destroyed_ai_ships += 1
                    return True
        else:
            user_ships = self.board.user_ships
            for ship in user_ships:
                if (row, col) in ship:
                    for item in ship:
                        if item not in self.ai_shoots:
                            print('Ранил!')
                            return False
                    print('Убил!')
                    self.destroyed_user_ships += 1
                    return True


    def check_endgame(self):
        if self.destroyed_user_ships == 4 or self.destroyed_ai_ships == 4:
            self.endgame = True

    def shoot(self, row, col):
        print(row, col)
        if self.active_player == 'user':
            if self.board.ai_field[row, col] in ('·', '*'):
                print(103)
                self.board.ai_field[row, col] = 'T'
                self.board.ai_field_game[row, col] = 'T'
                return False
            elif self.board.ai_field[row, col] == '■':
                print(108)
                self.board.ai_field[row, col] = 'X'
                self.board.ai_field_game[row, col] = 'X'
                return True
        else:
            if self.board.user_field[row, col] in ('·', '*'):
                print(114)
                self.board.user_field[row, col] = 'T'
                return False
            elif self.board.user_field[row, col] == '■':
                print(119)
                self.board.user_field[row, col] = 'X'
                return True

    def start_game(self):
        self.board.random_board('user')
        self.board.random_board('ai')
        while not self.endgame:
            print(self.board)
            if self.active_player == 'user':
                shoot_coords = input('Введите координаты клетки в формате А1: ')
                check = self.check_coords(shoot_coords)
                if check:
                    row, col = check
                    self.user_shoots.append((col, row))
                    if not self.shoot(row, col):
                        self.change_player()
                    else:
                        self.check_destroy(row, col)
            else:
                row, col = random.randint(0, 5), random.randint(0, 5)
                if (col, row) not in self.ai_shoots:
                    self.ai_shoots.append((col, row))
                    print(f'AI стреляет в row {row}, col {col}')
                    if not self.shoot(row, col):
                        self.change_player()
                    else:
                        self.check_destroy(row, col)
            self.check_endgame()
            print(self.destroyed_ai_ships, self.destroyed_user_ships)
        print('Игра завершена!')
        exit()

    def check_coords(self, shoot_coords):
        if len(shoot_coords) != 2:
            print('Проверьте корректность координат!')
            return False
        row, col = shoot_coords
        if not col.isdigit():
            print('Проверьте корректность координат!')
            return False
        col = int(col) - 1
        if row.upper() not in 'АБВГДЕ' or col not in range(6):
            print('Проверьте корректность координат!')
            return False
        row = 'АБВГДЕ'.index(row)
        if self.board.ai_field[row, col] not in ('T', 'X'):
            return row, col
        return False


board = Board()
game = Game(board)
game.start_game()
