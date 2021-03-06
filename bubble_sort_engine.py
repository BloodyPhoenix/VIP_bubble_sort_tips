# -*- coding: utf-8 -*-


import random


class TestTube:

    def __init__(self, number: int, bubble1, bubble2, bubble3, bubble4):
        """

        :param number: number if a test tube starting from the upper-left side of the screen
        :param bubble1: color of the upper bubble
        :param bubble2: color of the second bubble
        :param bubble3: color of the third bubble
        :param bubble4: color of the fourth bubble
        For empty tube bubble1-bubble4 should be None
        """
        self.number = number
        self.bubble1 = bubble1
        self.bubble2 = bubble2
        self.bubble3 = bubble3
        self.bubble4 = bubble4
        self.bubbles = [bubble1, bubble2, bubble3, bubble4]
        self.bubbles_amount = 0
        self.colours = 0
        self.can_put_into = False
        self.empty = False
        self.completed = False
        self._update_state()

    def _update_bubbles_list(self):
        self.bubbles = [self.bubble1, self.bubble2, self.bubble3, self.bubble4]

    def _update_state(self):
        self._update_bubbles_list()
        self._check_if_empty()
        self._check_can_put_into()
        self._check_if_completed()
        self._check_can_put_into()

    def _check_colours(self):
        self.colours = 0
        colours = set()
        for bubble in self.bubbles:
            if bubble:
                if bubble not in colours:
                    colours.add(bubble)
                    self.colours += 1

    def _check_can_put_into(self):
        self._check_bubbles_amount()
        if 4 > self.bubbles_amount:
            self.can_put_into = True
        else:
            self.can_put_into = False

    def _check_if_empty(self):
        for bubble in self.bubbles:
            if bubble is not None:
                self.empty = False
                return
        self.empty = True

    def _check_bubbles_amount(self):
        self.bubbles_amount = 0
        for bubble in self.bubbles:
            if bubble is not None:
                self.bubbles_amount += 1

    def _check_if_completed(self):
        self._check_colours()
        if 1 == self.colours:
            if not self.can_put_into:
                self.completed = True
                return
        self.completed = False

    def put_new_bubble(self, new_bubble):
        if self.bubbles_amount == 4:
            raise ValueError("Too many bubbles")
        self.bubble4 = self.bubble3
        self.bubble3 = self.bubble2
        self.bubble2 = self.bubble1
        self.bubble1 = new_bubble
        self._update_state()

    def remove_bubble(self):
        if self.bubbles_amount < 1:
            raise ValueError("There is no bubbles!")
        self.bubble1 = self.bubble2
        self.bubble2 = self.bubble3
        self.bubble3 = self.bubble4
        self.bubble4 = None
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
            if 1 == tube.colours:
                self.one_coloured_unfinished_tubes.append(tube.number)

    def _find_unsorted_tubes(self):
        self.unsorted_tubes = []
        for test_tube in self.test_tubes:
            if not test_tube.empty:
                if not test_tube.completed:
                    self.unsorted_tubes.append(test_tube.number)

    def find_empty_tubes(self):
        self.empty_tubes_current = []
        for test_tube in self.test_tubes:
            if test_tube.empty:
                self.empty_tubes_current.append(test_tube.number)

    def check_if_finished(self):
        for test_tube in self.test_tubes:
            if not test_tube.empty:
                if not test_tube.completed:
                    return False
        return True


class GameSimulator:

    def __init__(self, game_field: GameField):
        self.log = []
        self.banned_moves = []
        self.game_field = game_field
        self.current_bubble_colour = None
        self.first_test_tube_number = None
        self.second_test_tube_number = None

    def make_move(self):
        self.game_field.find_one_coloured_unfinished_tubes()
        tries = len(self.game_field.unsorted_tubes)
        checked_tubes = []
        for _ in range(tries):
            self._find_first_tube(checked_tubes)
            checked_tubes.append(self.first_test_tube_number)
            if self.second_test_tube_number is None:
                self._find_second_tube()
            if self.second_test_tube_number is not None:
                self.game_field.test_tubes[self.first_test_tube_number-1].remove_bubble()
                self.game_field.test_tubes[self.second_test_tube_number-1].put_new_bubble(self.current_bubble_colour)
                self._update_banned_moves()
                self._write_log()
                return True
        return False

    def check_if_finished(self):
        return self.game_field.check_if_finished()

    def _find_first_tube(self, checked_tubes):
        for test_tube_number in self.game_field.one_coloured_unfinished_tubes:
            test_tube = self.game_field.test_tubes[test_tube_number-1]
            colour = test_tube.bubble1
            number = test_tube.number
            for another_tube_number in self.game_field.one_coloured_unfinished_tubes:
                another_tube = self.game_field.test_tubes[another_tube_number-1]
                if another_tube.number == number:
                    continue
                if colour == another_tube.bubble1:
                    self.current_bubble_colour = colour
                    if test_tube.bubbles_amount == 4 - another_tube.bubbles_amount:
                        if test_tube.bubbles_amount <= another_tube.bubbles_amount:
                            self.first_test_tube_number = number
                            self.second_test_tube_number = another_tube.number
                        else:
                            self.first_test_tube_number = another_tube.number
                            self.second_test_tube_number = number
                        return
        while True:
            self.first_test_tube_number = random.choice(self.game_field.unsorted_tubes)
            if self.first_test_tube_number not in checked_tubes:
                self.current_bubble_colour = self.game_field.test_tubes[self.first_test_tube_number-1].bubble1
                return

    def _find_second_tube(self):
        possible_moves = []
        for test_tube_number in self.game_field.unsorted_tubes:
            if test_tube_number == self.first_test_tube_number:
                continue
            test_tube = self.game_field.test_tubes[test_tube_number-1]
            if test_tube.can_put_into:
                if test_tube.bubble1 == self.current_bubble_colour:
                    possible_moves.append(test_tube.number)
        if 1 != self.game_field.test_tubes[self.first_test_tube_number-1].colours:
            self.game_field.find_empty_tubes()
            possible_moves += self.game_field.empty_tubes_current
        while len(possible_moves) > 0:
            number = random.choice(possible_moves)
            possible_moves.remove(number)
            test_tube = self.game_field.test_tubes[number-1]
            if (self.first_test_tube_number, number) in self.banned_moves:
                continue
            if not test_tube.empty:
                if test_tube.bubble1 == self.current_bubble_colour:
                    self.second_test_tube_number = number
                    return
            else:
                self.second_test_tube_number = number
                return
        self.second_test_tube_number = None

    def _write_log(self):
        move = f"{len(self.log)+1}: {self.current_bubble_colour} ???? ???????????????? {self.first_test_tube_number} " \
               f"?? ???????????????? {self.second_test_tube_number}"
        self.log.append(move)
        self.current_bubble_colour = None
        self.first_test_tube_number = None
        self.second_test_tube_number = None

    def _update_banned_moves(self):
        for banned_move in self.banned_moves:
            if self.first_test_tube_number in banned_move:
                del banned_move
            elif self.second_test_tube_number in banned_move:
                del banned_move
        self.banned_moves.append((self.second_test_tube_number, self.first_test_tube_number))

