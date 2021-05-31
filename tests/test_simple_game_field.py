# -*- coding: utf-8 -*-


import balls_sorting_engine
import unittest


class TestGameField(unittest.TestCase):

    def setUp(self):
        tube_1 = balls_sorting_engine.TestTube(1, "yellow", "blue", "yellow", "red")
        tube_2 = balls_sorting_engine.TestTube(2, "blue", "blue", "red", "red")
        tube_3 = balls_sorting_engine.TestTube(3, "yellow", "yellow", "red", "blue")
        tube_4 = balls_sorting_engine.TestTube(4, None, None, None, None)
        tube_5 = balls_sorting_engine.TestTube(5, None, None, None, None)
        self.game_field = balls_sorting_engine.GameField([tube_1, tube_2, tube_3, tube_4, tube_5], 2)
        self.game_field.test_tubes[0].remove_ball()
        self.game_field.test_tubes[3].put_new_ball("yellow")

    def test_check_if_finished_False(self):
        self.assertEqual(False, self.game_field.check_if_finished())

    def test_find_empty_tubes(self):
        self.game_field.find_empty_tubes()
        self.assertEqual([5], self.game_field.empty_tubes_current)

    def test_find_one_coloured_unfinished(self):
        self.game_field.find_one_coloured_unfinished_tubes()
        self.assertEqual([4], self.game_field.one_coloured_unfinished_tubes)

    def test_find_unsorted_tubes(self):
        self.game_field._find_unsorted_tubes()
        self.assertEqual([1, 2, 3, 4], self.game_field.unsorted_tubes)

    def test_check_if_finished_True(self):
        self.game_field = balls_sorting_engine.GameField(
            [balls_sorting_engine.TestTube(1, "yellow", "yellow", "yellow", "yellow"),
             balls_sorting_engine.TestTube(2, "red", "red", "red", "red"),
             balls_sorting_engine.TestTube(3, None, None, None, None),
             balls_sorting_engine.TestTube(4, "blue", "blue", "blue", "blue"),
             balls_sorting_engine.TestTube(5, None, None, None, None)], 2)
        self.assertEqual(True, self.game_field.check_if_finished())


if __name__ == "__main__":
    TestGameField()