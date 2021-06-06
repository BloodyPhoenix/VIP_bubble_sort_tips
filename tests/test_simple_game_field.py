# -*- coding: utf-8 -*-


import bubble_sort_engine
import unittest


class TestGameField(unittest.TestCase):

    def setUp(self):
        tube_1 = bubble_sort_engine.TestTube(1, "yellow", "blue", "yellow", "red")
        tube_2 = bubble_sort_engine.TestTube(2, "blue", "blue", "red", "red")
        tube_3 = bubble_sort_engine.TestTube(3, "yellow", "yellow", "red", "blue")
        tube_4 = bubble_sort_engine.TestTube(4, None, None, None, None)
        tube_5 = bubble_sort_engine.TestTube(5, None, None, None, None)
        self.game_field = bubble_sort_engine.GameField([tube_1, tube_2, tube_3, tube_4, tube_5], 2)
        self.game_field.test_tubes[0].remove_bubble()
        self.game_field.test_tubes[3].put_new_bubble("yellow")

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
        self.game_field = bubble_sort_engine.GameField(
            [bubble_sort_engine.TestTube(1, "yellow", "yellow", "yellow", "yellow"),
             bubble_sort_engine.TestTube(2, "red", "red", "red", "red"),
             bubble_sort_engine.TestTube(3, None, None, None, None),
             bubble_sort_engine.TestTube(4, "blue", "blue", "blue", "blue"),
             bubble_sort_engine.TestTube(5, None, None, None, None)], 2)
        self.assertEqual(True, self.game_field.check_if_finished())


if __name__ == "__main__":
    TestGameField()