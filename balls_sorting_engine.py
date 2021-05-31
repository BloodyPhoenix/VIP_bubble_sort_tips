# -*- coding: utf-8 -*-


import random


class TestTube:

    def __init__(self, number: int, ball1, ball2, ball3, ball4):
        """

        :param number: number if a test tube starting from the upper-left side of the screen
        :param ball1: color of the upper ball
        :param ball2: color of the second ball
        :param ball3: color of the third ball
        :param ball4: color of the fourth ball
        For empty tube ball1-ball4 should be None
        """
        self.number = number
        self.ball1 = ball1
        self.ball2 = ball2
        self.ball3 = ball3
        self.ball4 = ball4
        self.balls = [ball1, ball2, ball3, ball4]
        self._update_state()

    def _update_balls_list(self):
        self.balls = [self.ball1, self.ball2, self.ball3, self.ball4]

    def _update_state(self):
        self._update_balls_list()
        self.check_if_completed()
        self.check_balls_amount()
        self.check_colours()

    def check_colours(self):
        self.colours = 0
        colours = set()
        for ball in self.balls:
            if ball:
                if ball not in colours:
                    colours.add(ball)
                    self.colours += 1

    def check_can_put_into(self):
        self.check_balls_amount()
        if 4 > self.balls_amount:
            return True
        else:
            return False

    def check_if_empty(self):
        for ball in self.balls:
            if ball:
                return False
        return True

    def check_balls_amount(self):
        self.balls_amount = 0
        for ball in self.balls:
            if ball is not None:
                self.balls_amount += 1

    def check_if_completed(self):
        self.check_colours()
        if 1 == self.colours:
            if not self.check_can_put_into():
                return True
        return False

    def put_new_ball(self, new_ball):
        if self.balls_amount == 4:
            raise ValueError("Too many balls")
        self.ball4 = self.ball3
        self.ball3 = self.ball2
        self.ball2 = self.ball1
        self.ball1 = new_ball
        self._update_state()


    def remove_ball(self):
        if self.balls_amount < 1:
            raise ValueError("There is no balls!")
        self.ball1 = self.ball2
        self.ball2 = self.ball3
        self.ball3 = self.ball4
        self.ball4 = None
        self._update_state()


class GameField:

    def __init__(self, test_tubes: list, empty_tubes_amount: int):
        self.test_tubes = test_tubes
        self.empty_tubes_start = empty_tubes_amount
        self.empty_tubes_current = []
        self.unsorted_tubes = []
        self.one_coloured_unfinished_tubes = []

    def find_one_coloured_unfinished_tubes(self):
        self._find_unsorted_tubes()
        self.one_coloured_unfinished_tubes = []
        for tube_number in self.unsorted_tubes:
            tube = self.test_tubes[tube_number-1]
            tube.check_colours()
            if 1 == tube.colours:
                self.one_coloured_unfinished_tubes.append(tube.number)

    def _find_unsorted_tubes(self):
        self.unsorted_tubes = []
        for test_tube in self.test_tubes:
            if not test_tube.check_if_empty():
                if not test_tube.check_if_completed():
                    self.unsorted_tubes.append(test_tube.number)

    def find_empty_tubes(self):
        self.empty_tubes_current = []
        for test_tube in self.test_tubes:
            if test_tube.check_if_empty():
                self.empty_tubes_current.append(test_tube.number)

    def check_if_finished(self):
        for test_tube in self.test_tubes:
            if not test_tube.check_if_empty():
                if not test_tube.check_if_completed():
                    return False
        return True


class GameSimulator:

    def __init__(self, game_field: GameField):
        self.log = []
        self.banned_moves = []
        self.game_field = game_field
        self.current_ball_colour = None
        self.first_test_tube_number = None
        self.second_test_tube_number = None

    def make_move(self):
        self.game_field.find_one_coloured_unfinished_tubes()
        tries = len(self.game_field.unsorted_tubes)
        checked_tubes = []
        for _ in range(tries):
            self._find_first_tube(checked_tubes)
            checked_tubes.append(self.first_test_tube_number)
            if self.second_test_tube_number:
                break
            self._find_second_tube()
        if self.second_test_tube_number:
            self.game_field.test_tubes[self.first_test_tube_number-1].remove_ball()
            self.game_field.test_tubes[self.second_test_tube_number-1].put_new_ball(self.current_ball_colour)
            self._update_banned_moves()
            self._write_log()
            return True
        return False

    def check_if_finished(self):
        return self.game_field.check_if_finished()

    def _find_first_tube(self, checked_tubes):
        for test_tube_number in self.game_field.one_coloured_unfinished_tubes:
            test_tube = self.game_field.test_tubes[test_tube_number-1]
            colour = test_tube.ball1
            number = test_tube.number
            for another_tube_number in self.game_field.one_coloured_unfinished_tubes:
                another_tube = self.game_field.test_tubes[another_tube_number-1]
                if another_tube.number == number:
                    continue
                if colour == another_tube.ball1:
                    self.current_ball_colour = colour
                    if test_tube.balls_amount == 4 - another_tube.balls_amount:
                        if test_tube.balls_amount <= another_tube.balls_amount:
                            self.first_test_tube_number = number
                            self.second_test_tube_number = another_tube.number
                        else:
                            self.first_test_tube_number = another_tube.number
                            self.second_test_tube_number = number
                        return
        while True:
            self.first_test_tube_number = random.choice(self.game_field.unsorted_tubes)
            if self.first_test_tube_number not in checked_tubes:
                self.current_ball_colour = self.game_field.test_tubes[self.first_test_tube_number-1].ball1
                return

    def _find_second_tube(self):
        possible_moves = []
        checked_moves = []
        for test_tube_number in self.game_field.unsorted_tubes:
            test_tube = self.game_field.test_tubes[test_tube_number-1]
            if test_tube.check_can_put_into():
                if test_tube.ball1 == self.current_ball_colour:
                    possible_moves.append(test_tube.number)
        self.game_field.find_empty_tubes()
        possible_moves += self.game_field.empty_tubes_current
        for _ in range(len(possible_moves)):
            while True:
                number = random.choice(possible_moves)
                if number not in checked_moves:
                    checked_moves.append(number)
                    break
            if (self.first_test_tube_number, number) in self.banned_moves:
                checked_moves.append(number)
                continue
            self.second_test_tube_number = number
            return
        self.second_test_tube_number = None

    def _write_log(self):
        move = f"{len(self.log)+1}: {self.current_ball_colour} из пробирки {self.first_test_tube_number} " \
               f"в пробирку {self.second_test_tube_number}"
        self.log.append(move)
        self.current_ball_colour = None
        self.first_test_tube_number = None
        self.second_test_tube_number = None

    def _update_banned_moves(self):
        for banned_move in self.banned_moves:
            if self.first_test_tube_number in banned_move:
                del banned_move
            elif self.second_test_tube_number in banned_move:
                del banned_move
        self.banned_moves.append((self.second_test_tube_number, self.first_test_tube_number))

