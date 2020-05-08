#!/usr/bin/python3

import os
import unittest

from aquarium import Asset, Region, Direction


class TestAssetMethods(unittest.TestCase):

    def test_path(self):
        correct = os.path.join('assets', 'sea.png')
        self.assertEqual(Asset.path('sea.png'), correct)


class TestRegionMethods(unittest.TestCase):

    def test_random(self):
        self.assertIn(Region.random(), list(Region))

    def test_x_part(self):
        self.assertEqual(Region.TOP_LEFT.x_part(), 'LEFT')

    def test_y_part(self):
        self.assertEqual(Region.TOP_LEFT.y_part(), 'TOP')

    def test_rand_coords(self):
        x1, y1 = Region.TOP_LEFT.rand_coords(300, 300)
        self.assertTrue(0 <= x1 <= 100 and 0 <= y1 <= 100)
        x2, y2 = Region.BOTTOM_RIGHT.rand_coords(600, 600)
        self.assertTrue(400 < x2 <= 600 and 400 < y2 <= 600)


class TestDirectionMethods(unittest.TestCase):

    def test_random(self):
        self.assertIn(Direction.random(), list(Direction))

    def test_random_exclude(self):
        exclude = Direction.WEST
        direction = Direction.random(exclude=exclude)
        self.assertNotEqual(direction, exclude)

    def test_hrandom(self):
        self.assertIn(Direction.hrandom(), [Direction.WEST, Direction.EAST])

    def test_vrandom(self):
        self.assertIn(Direction.vrandom(), [Direction.NORTH, Direction.SOUTH])


if __name__ == '__main__':
    unittest.main()
