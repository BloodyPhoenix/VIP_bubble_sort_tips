# -*- coding: utf-8 -*-


import balls_sorting_engine
import unittest


class TestGameSimulator(unittest.TestCase):

    def setUp(self):
        tube_1 = balls_sorting_engine.TestTube(1, "blue", "red", None, None)
        tube_2 = balls_sorting_engine.TestTube(2, "blue", "blue", "red", "red")
        tube_3 = balls_sorting_engine.TestTube(3, "red", "blue", None, None)
        tube_4 = balls_sorting_engine.TestTube(4, "yellow", "yellow", "yellow", None)
        tube_5 = balls_sorting_engine.TestTube(5, "yellow", None, None, None)
        game_field = balls_sorting_engine.GameField([tube_1, tube_2, tube_3, tube_4, tube_5], 2)
        self.game_simulator = balls_sorting_engine.GameSimulator(game_field)
        self.game_simulator.game_field.find_one_coloured_unfinished_tubes()

    def test_find_first_tube_colour_added(self):
        """Tests that _find_first_tube adds correct current_colour param to GameSimulator object"""
        self.game_simulator._find_first_tube([])
        test_tube_index = self.game_simulator.first_test_tube_number-1
        colour = self.game_simulator.game_field.test_tubes[test_tube_index].ball1
        assert self.game_simulator.current_ball_colour
        self.assertEqual(colour, self.game_simulator.current_ball_colour)

    def test_complete_tube(self):
        """Tests if program is trying to complete tubes that are already almost done first"""
        self.game_simulator._find_first_tube([])
        self.assertEqual(5, self.game_simulator.first_test_tube_number)
        self.assertEqual("yellow", self.game_simulator.current_ball_colour)

    def test_banned_move(self):
        self.game_simulator.make_move()
        self.assertEqual([(4, 5)], self.game_simulator.banned_moves)

    def test_make_move(self):
        assert self.game_simulator.make_move()


if __name__ == "__main__":
    TestGameSimulator()
