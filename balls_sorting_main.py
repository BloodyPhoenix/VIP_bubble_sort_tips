# -*- coding: utf-8 -*-
import copy

import balls_sorting_engine
import balls_sorting_setup


def balls_sort():
    print("""Добро пожаловать в приложение, помогающее проходить игру Bubble Sort и ей подобные!
    
Для того, чтобы начать, нажмите Enter""")
    input()
    print("""Сейчас вам нужно будет задать начальные условия уровня: количество пробирок, их расположение и цвета шариков.
Программа не чувствительна к языку и регистру. Вы можете вводить цвета шаирков любым удобным для вас способом,
в том числе - используя сокращения. Главное - чтобы вы сами понимали, какое обозначение какому цвету соответствует, 
и везде обозначали один цвет одинаково. Если будут попадаться цвета "Жёлтый" и "жёлтый", программа будет считать их
разными цветами и не сможет корректно начать работу.
    
Нумерация пробирок идёт от верхнего левого угла поля, шариков - от верхнего к нижнему.""")
    base_game_field = balls_sorting_setup.setup_game_field()
    tries = 0
    completed = False
    while not completed:
        tries += 1
        print("Попытка номер", tries)
        game_field = copy.deepcopy(base_game_field)
        simulator = balls_sorting_engine.GameSimulator(game_field)
        has_moves = True
        while has_moves:
            if simulator.make_move():
                if simulator.check_if_finished():
                    print_log(simulator)
                    completed = True
                    has_moves = False
            else:
                has_moves = False
    input()


def print_log(simulator: balls_sorting_engine.GameSimulator):
    for line in simulator.log:
        print(line)


if __name__ == "__main__":
    balls_sort()

