# -*- coding: utf-8 -*-


import balls_sorting_setup
from balls_sorting_engine import GameField
import unittest
from unittest.mock import Mock


class TestSetup(unittest.TestCase):

    def test_setup(self):
        balls_sorting_setup.get_test_tubes_amount = Mock(return_value=5)
        balls_sorting_setup.get_empty_tubes_amount = Mock(return_value=2)
        balls_sorting_setup.empty_tubes_position = Mock(return_value=[4, 5])
        balls_sorting_setup.fill_tubes_with_balls = Mock(return_value=[None, None, None, None])
        game_field = balls_sorting_setup.setup_game_field()
        expected_field = GameField([
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]],
            2)
        self.assertEqual(expected_field, game_field)


if __name__ == "__main__":
    TestSetup()
