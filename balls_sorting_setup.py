# -*- coding: utf-8 -*-


from collections import defaultdict
import balls_sorting_engine


class TooManyColours(ValueError):
    pass


def setup_game_field():
    test_tubes_amount = get_test_tubes_amount()
    empty_tubes_amount = get_empty_tubes_amount()
    empty_tubes_position = get_empty_tubes_position(empty_tubes_amount, test_tubes_amount)
    test_tubes = []
    while True:
        try:
            test_tubes = fill_tubes_with_balls(
                tubes_amount=test_tubes_amount, empty_tubes_position=empty_tubes_position
            )
            break
        except TooManyColours:
            continue
    for index, test_tube in enumerate(test_tubes):
        test_tubes[index] = balls_sorting_engine.TestTube(
            index+1, test_tube[0], test_tube[1], test_tube[2], test_tube[3])
    return balls_sorting_engine.GameField(test_tubes, empty_tubes_amount)


def get_test_tubes_amount():
    while True:
        test_tubes_amount = input("Введите количество пробирок: ")
        if not test_tubes_amount.isdigit():
            print()
            print("Вы ввели не целое число. Пожалуйста, повторите ввод")
            continue
        return int(test_tubes_amount)


def get_empty_tubes_amount():
    while True:
        empty_test_tubes_amount = input("Введите количество пустых пробирок: ")
        if not empty_test_tubes_amount.isdigit():
            print()
            print("Вы ввели не целое число. Пожалуйста, повторите ввод")
            continue
        return int(empty_test_tubes_amount)


def get_empty_tubes_position(empty_tubes_amount, test_tubes_amount):
    empty_tubes = []
    while len(empty_tubes) < empty_tubes_amount:
        empty_tube_position = input("Введите позицию пустой пробирки: ")
        if not empty_tube_position.isdigit():
            print("Вы ввели не целое число. Пожалуйста, повторите ввод")
            continue
        empty_tube_position = int(empty_tube_position)
        if empty_tube_position > test_tubes_amount:
            print("Слишком большое значение. Пробирки с таким номером на поле нет.")
            continue
        if empty_tube_position in empty_tubes:
            print("Вы ввели одно и то же число дважды. Повторите ввод.")
            continue
        empty_tubes.append(empty_tube_position)
    return empty_tubes


def fill_tubes_with_balls(tubes_amount, empty_tubes_position):
    colour_counter = defaultdict(int)
    test_tubes = []
    for _ in range(tubes_amount):
        test_tubes.append(["", "", "", ""])
    for tube_index in range(tubes_amount):
        if tube_index+1 in empty_tubes_position:
            test_tubes[tube_index] = [None, None, None, None]
            continue
        for ball_index in range(4):
            print(f"Введите цвет {ball_index+1} шарика в {tube_index+1} пробирке.")
            colour = input()
            test_tubes[tube_index][ball_index] = colour
            colour_counter[colour] += 1
            if colour_counter[colour] > 4:
                print("Ошибка ввода. Больше четырёх шариков одного цвета.")
                raise TooManyColours()
    while True:
        for colour in colour_counter:
            if colour_counter[colour] == 1:
                for tube_index, test_tube in enumerate(test_tubes):
                    for ball_index, ball_colour in test_tube:
                        if ball_colour == colour:
                            print(f"Опечатка: цвет шарика номер {ball_colour} {colour} в пробирке номер {tube_index+1}")
                            print("Введите корректный цвет шарика")
                            new_colour = input()
                            test_tubes[tube_index][ball_index] = new_colour
        return test_tubes

