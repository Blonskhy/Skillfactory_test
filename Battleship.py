import random

class BoardOutException(Exception):
    pass

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"

class Ship:
    def __init__(self, length, bow, direction):
        self.length = length
        self.bow = bow
        self.direction = direction
        self.lives = length

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            cur_x = self.bow.x
            cur_y = self.bow.y
            if self.direction == 0:
                cur_x += i
            elif self.direction == 1:
                cur_y += i
            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots

class Board:
    def __init__(self, hid=False):
        self.field = [["О"] * 6 for _ in range(6)]
        self.ships = []
        self.hid = hid
        self.live_ships = 0

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or self.field[d.x][d.y] != "О":
                raise BoardOutException("Невозможно разместить корабль")
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
        self.ships.append(ship)
        self.live_ships += 1
        self.contour(ship)

    def contour(self, ship):
        around = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1), (0, 0), (0, 1),
                  (1, -1), (1, 0), (1, 1)]
        for d in ship.dots:
            for dx, dy in around:
                cur = Dot(d.x + dx, d.y + dy)
                if not self.out(cur) and self.field[cur.x][cur.y] == "О":
                    self.field[cur.x][cur.y] = "."

    def __str__(self):
        res = "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"
        if self.hid:
            res = res.replace("■", "О")
        return res

    def out(self, d):
        return not (0 <= d.x < 6 and 0 <= d.y < 6)

    def shot(self, d):
        if self.out(d):
            raise BoardOutException("Выстрел за пределы поля")
        if self.field[d.x][d.y] == "T" or self.field[d.x][d.y] == "X":
            raise BoardOutException("Уже стреляли в эту клетку")
        if self.field[d.x][d.y] == "■":
            self.field[d.x][d.y] = "X"
            for ship in self.ships:
                if d in ship.dots:
                    ship.lives -= 1
                    if ship.lives == 0:
                        self.live_ships -= 1
                        print("Корабль уничтожен!")
                    else:
                        print("Корабль ранен!")
                    return True
        else:
            self.field[d.x][d.y] = "T"
            print("Мимо!")
            return False

class Player:
    def __init__(self, board, enemy_board):
        self.board = board
        self.enemy_board = enemy_board

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy_board.shot(target)
                return repeat
            except BoardOutException as e:
                print(e)

class AI(Player):
    def ask(self):
        d = Dot(random.randint(0, 5), random.randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d

class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()
            if len(cords) != 2:
                print("Введите 2 координаты (1-6)")
                continue
            x, y = cords
            if not (x.isdigit()) or not (y.isdigit()):
                print("Введите числа (1-6)")
                continue
            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)

class Game:
    def __init__(self):
        self.user_board = self.random_board()
        self.ai_board = self.random_board(hid=True)
        self.ai = AI(self.ai_board, self.user_board)
        self.user = User(self.user_board, self.ai_board)

    def random_board(self, hid=False):
        board = None
        while board is None:
            board = self.try_board(hid)
        return board

    def try_board(self, hid):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(hid)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(l, Dot(random.randint(0, 6), random.randint(0, 6)), random.randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardOutException:
                    pass
        board.field = [["О" if cell == "." else cell for cell in row] for row in board.field]
        return board

    def greet(self):
        print("""
        Приветствую вас в игре Морской бой
          Формат ввода: x y
            Где
         x - номер строки
         y - номер столбца 
          Адмирал, желаю вам удачи!""")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска игрока:")
            print(self.user_board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai_board)
            if num % 2 == 0:
                print("-" * 20)
                print("Ходит Игрок!")
                repeat = self.user.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1
            if self.ai_board.live_ships == 0:
                print("-" * 20)
                print("Игрок выиграл!")
                break
            if self.user_board.live_ships == 0:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()

game = Game()
game.start()