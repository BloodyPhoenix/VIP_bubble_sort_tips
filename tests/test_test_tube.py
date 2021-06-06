# -*- coding: utf-8 -*-


import bubble_sort_engine
import unittest


class TestTube(unittest.TestCase):

    def setUp(self):
        self.tube = bubble_sort_engine.TestTube(1, "red", "blue", "blue", "yellow")

    def test_check_colours(self):
        self.assertEqual(3, self.tube.colours)

    def test_bubbles_amount(self):
        self.tube.remove_bubble()
        self.tube.remove_bubble()
        self.tube.put_new_bubble("yellow")
        self.assertEqual(3, self.tube.bubbles_amount)

    def test_check_bubbles_amount(self):
        self.tube.bubble4 = None
        self.tube._update_state()
        self.assertEqual(3, self.tube.bubbles_amount)

    def test_can_put_bubble_False(self):
        self.assertEqual(False, self.tube.can_put_into)

    def test_if_completed_False(self):
        self.assertEqual(False, self.tube.completed)

    def test_put_new_bubble(self):
        self.tube.bubble4 = None
        self.tube.bubble3 = None
        self.tube._update_state()
        self.tube.put_new_bubble("red")
        self.assertEqual(2, self.tube.colours)
        self.assertEqual(3, self.tube.bubbles_amount)
        self.assertEqual(True, self.tube.can_put_into)
        self.assertEqual(False, self.tube.empty)
        self.assertEqual(False, self.tube.completed)

    def test_remove_bubble(self):
        self.tube.remove_bubble()
        self.assertEqual(self.tube.colours, 2)
        self.assertEqual(self.tube.bubbles_amount, 3)
        self.assertEqual(self.tube.can_put_into, True)
        self.assertEqual(self.tube.empty, False)
        self.assertEqual(self.tube.completed, False)
        self.assertEqual(self.tube.bubble4, None)

    def test_can_put_bubble_True(self):
        self.tube.remove_bubble()
        self.assertEqual(self.tube.can_put_into, True)

    def test_completed_True(self):
        self.tube.bubble1 = "blue"
        self.tube.bubble4 = "blue"
        self.tube._update_state()
        self.assertEqual(self.tube.completed, True)

    def test_if_empty_True(self):
        self.tube = bubble_sort_engine.TestTube(1, None, None, None, None)
        self.tube._update_state()
        self.assertEqual(self.tube.empty, True)
        self.assertEqual(self.tube.can_put_into, True)
        self.assertEqual(self.tube.completed, False)
        self.assertEqual(self.tube.colours, 0)
        self.assertEqual(self.tube.bubbles_amount, 0)

    def test_check_if_empty_False(self):
        self.assertEqual(False, self.tube.empty)


if __name__ == "__main__":
    TestTube()


