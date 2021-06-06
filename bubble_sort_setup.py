# -*- coding: utf-8 -*-


from collections import defaultdict
import bubble_sort_engine


def setup_game_field():
    test_tubes_amount = get_test_tubes_amount()
    empty_tubes_amount = get_empty_tubes_amount()
    empty_tubes_position = get_empty_tubes_position(empty_tubes_amount, test_tubes_amount)
    tubes_filler = BubblesColoursFiller(test_tubes_amount, empty_tubes_position)
    test_tubes = None
    while not test_tubes:
        try:
            test_tubes = tubes_filler.fill_tubes_with_bubbles()
        except ValueError:
            continue
    for index, test_tube in enumerate(test_tubes):
        test_tubes[index] = bubble_sort_engine.TestTube(
            index+1, test_tube[0], test_tube[1], test_tube[2], test_tube[3])
    return bubble_sort_engine.GameField(test_tubes, empty_tubes_amount)


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


class BubblesColoursFiller:

    def __init__(self, test_tubes_amount: int, empty_tubes_postition: list):
        self.test_tubes_amount = test_tubes_amount
        self.empty_tubes_position = empty_tubes_postition
        self.colour_counter = defaultdict(int)
        self.test_tubes = []

    def _create_tubes(self):
        for _ in range(self.test_tubes_amount):
            self.test_tubes.append(["", "", "", ""])

    def fill_tubes_with_bubbles(self):
        self._create_tubes()
        for tube_index in range(self.test_tubes_amount):
            if tube_index+1 in self.empty_tubes_position:
                self.test_tubes[tube_index] = [None, None, None, None]
                continue
            for bubble_index in range(4):
                print(f"Введите цвет {bubble_index+1} шарика в {tube_index+1} пробирке.")
                colour = input()
                self.test_tubes[tube_index][bubble_index] = colour
                self.colour_counter[colour] += 1
                if self.colour_counter[colour] > 4:
                    print("Ошибка ввода. Больше четырёх шариков одного цвета.")
                    raise ValueError
        correct_input = False
        while not correct_input:
            correct_input = self._check_single_colour()
        correct_input = False
        while not correct_input:
            correct_input = self._check_one_coloured_bubbles_amount()
            if not correct_input:
                self.correct_input()
        return self.test_tubes

    def _check_single_colour(self):
        """Checks if there a typo in colours"""
        for colour in self.colour_counter:
            if 1 == self.colour_counter[colour]:
                for index, test_tube in enumerate(self.test_tubes):
                    if colour in test_tube:
                        bubble_index = test_tube.index(colour)
                        print(f"Опечатка в пробирке номер {index} с шариком {bubble_index}. Введите корректный цвет")
                        new_colour = input()
                        self.test_tubes[index][bubble_index] = new_colour
                        return False
        return True

    def _check_one_coloured_bubbles_amount(self):
        for colour in self.colour_counter:
            if 4 > self.colour_counter[colour]:
                print(f"Слишком мало шариков цвета {colour}. Скорректируйте ваш ввод")
                return False
        return True

    def correct_input(self):
        """Allows user to correct his input"""
        while True:
            test_tube_index = input("Введите номер пробирки (нормеа считаютс слеванаправо и сверху вниз): ")
            if not test_tube_index.isdigit():
                print("Вы ввели не число! Повторите ввод.")
            test_tube_index = int(test_tube_index)
            if test_tube_index > self.test_tubes_amount:
                print("Слишком большой номер. Пробирки с таким номером нет! Повторите ввод")
            else:
                test_tube_index = test_tube_index-1
                break
        while True:
            bubble_index = input("Введите номер шарика (номера шариков считаются сверху-вниз): ")
            if not bubble_index.isdigit():
                print("Вы ввели не число! Повторите ввод.")
            bubble_index = int(bubble_index)
            if bubble_index > 4:
                print("Неверный номер шарика. В пробирке не может быть больше четырёх шариков. Повторите ввод")
            else:
                bubble_index = bubble_index-1
                break
        print(f"Введите новый цвет {bubble_index+1} шарика в {test_tube_index+1} пробирке")
        new_colour = input()
        self.test_tubes[test_tube_index][bubble_index] = new_colour


