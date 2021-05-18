# -*- coding: utf-8 -*-


from collections import defaultdict
import copy
import random


class TestTube:

    def __init__(self, number, ball1, ball2, ball3, ball4):
        self.number = number
        self.ball1 = ball1
        self.ball2 = ball2
        self.ball3 = ball3
        self.ball4 = ball4
        self.balls = [ball1, ball2, ball3, ball4]

    def check_can_put_into(self):
        if None in self.balls:
            return True
        else:
            return False

    def check_if_empty(self):
        for ball in self.balls:
            if not None == ball:
                return False
        return True

    def check_if_completed(self):
        if not self.check_can_put_into():
            if all(self.balls[index] == self.balls[index-1] for index in range(4)):
                return True
        return False


class GameField:

    def __init__(self, test_tubes: list, empty_tubes_amount: int):
        self.test_tubes = test_tubes
        self.empty_tubes_start = empty_tubes_amount
        self.empty_tubes_current = empty_tubes_amount

    def check_if_finished(self):
        for test_tube in self.test_tubes:
            if not test_tube.check_if_empty() or test_tube.check_if_completed():
                return False
        return True