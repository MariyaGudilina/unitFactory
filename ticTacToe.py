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
