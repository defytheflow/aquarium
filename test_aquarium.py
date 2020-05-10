#!/usr/bin/python3

import unittest

from aquarium import Direction


class TestDirectionMethods(unittest.TestCase):

    def test_random(self):
        self.assertIn(Direction.random(), list(Direction))

    def test_random_exclude(self):
        exclude = Direction.WEST
        direction = Direction.random(exclude=exclude)
        self.assertNotEqual(direction, exclude)

    def test_random_horizontal(self):
        self.assertIn(Direction.random_horizontal(), [Direction.WEST, Direction.EAST])

    def test_random_vertical(self):
        self.assertIn(Direction.random_vertical(), [Direction.NORTH, Direction.SOUTH])


if __name__ == '__main__':
    unittest.main()
