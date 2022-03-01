from random import randint


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"


a = Dot(1, 2)
b = Dot(1, 2)


# print(a)


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


class BoardWrongShipException(BoardException):
    pass


class Ships:
    def __init__(self, bow, num_deck, orientation):
        self.bow = bow
        self.orientation = orientation
        self.num_deck = num_deck
        self.lives = num_deck

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.num_deck):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.orientation == 0:
                cur_x += i

            elif self.orientation == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


ship1 = Ships(Dot(5, 1), 3, 0)

print(ship1.dots, ship1.num_deck)


class Boards:
    def __init__(self, hid=False, size=10):
        self.hid = hid
        self.size = size
        self.count = 0

        self.busy = []
        self.ships = []
        self.field = [[" "] * size for _ in range(size)]
        
    def __str__(self):
        res = ""
        res += "   | а | б | в | г | д | е | ж | з | и | к |"
        res += "   \n   | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10|"

        for i, row in enumerate(self.field):
            if i == 9:
                res += f"\n {i + 1}| " + " | ".join(row) + " |"
            else:
                res += f"\n {i + 1} | " + " | ".join(row) + " |"

            if self.hid:
                res = res.replace("■", " ")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur) and cur not in self.busy):
                    if verb:
                        self.field[cur.x][cur.y] = '#'
                    self.busy.append(cur)

    def add_ship(self, ship):
        for i in ship.dots:
            if self.out(i) or i in self.busy:
                raise BoardWrongShipException()
        for i in ship.dots:
            self.field[i.x][i.y] = "■"
            self.busy.append(i)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.field[d.x][d.y] = "."
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []
        board = Boards()


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 9), randint(0, 9))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=10):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = False

        self.comp = AI(co, pl)
        self.user = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def try_board(self):
        lens_ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        board = Boards(size=self.size)
        attempts = 0
        for lens in lens_ships:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ships(Dot(randint(0, self.size), randint(0, self.size)), lens, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.user.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.comp.board)
            print("-" * 20)
            if num % 2 == 0:
                print("Ходит пользователь!")
                repeat = self.user.move()
            else:
                print("Ходит компьютер!")
                repeat = self.comp.move()
            if repeat:
                num -= 1

            if self.comp.board.count == 10:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.user.board.count == 10:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()