field = [[" "] * 3 for i in range(3)]


def show_field(*args):
    print(f"    | 0 | 1 | 2 |")
    print(f"  ---------------")
    field[x][y] = symbol_user
    for i in range(3):
        row_info = f"  {i} | {' | '.join(field[i])} | "
        print(row_info)
        print(f" ----------------")


def input_user():
    while True:
        coords = input("   Ваш ход:  ").split()
        if len(coords) != 2:
            print("Введите две координаты через пробел!")
            continue

        a, b = coords

        if not (a.isdigit()) or not (b.isdigit()):
            print("Введите числа!")
            continue

        a, b = int(a), int(b)

        if 0 <= a <= 2 and 0 <= b <= 2:
            if field[a][b] == " ":
                return a, b
            else:
                print("Занято")
                continue
        return print("Клетка вне диапазона")
    
    def check_win():
    win_cord = [((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
                ((0, 2), (1, 1), (2, 0)), ((0, 0), (1, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
                ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2))]
    for cord in win_cord:
        symbols = []

        for c in cord:
            symbols.append(field[c[0]][c[1]])
        if symbols == ["X", "X", "X"]:
            print("Выиграл X!!!")
            return True
        if symbols == ["O", "O", "O"]:
            print("Выиграл O!!!")
            return True
        return False




num = 0

while True:
    num += 1
    if num % 2 == 0:
        symbol_user = "X"
        print("Ходит крестик")
    else:
        symbol_user = "O"
        print("Ходит нолик")

    x, y = input_user()
    show_field(symbol_user, x, y)

    if check_win():
        break

    if num == 9:
        print("Ничья")
        break


