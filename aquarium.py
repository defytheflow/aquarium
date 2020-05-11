#!/usr/bin/python3

import os
import enum
import random
import typing
import tkinter as tk


class Window(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._bg = tk.PhotoImage(file=os.path.join('assets', 'bg.png'))
        self._width = 800
        self._height = 600
        self.title('Aquarium')
        self.resizable(0, 0)
        self.geometry(f'{self._width}x{self._height}')

        canvas = tk.Canvas(self, width=self._width, height=self._height)
        canvas.create_image(0, 0, image=self._bg, anchor=tk.NW)
        canvas.pack(expand=tk.YES, fill=tk.BOTH)

        fish = Fish(canvas)
        fish.swim()

        self.mainloop()


@enum.unique
class Direction(enum.Enum):
    """ Represents fish direction. """
    WEST = enum.auto()
    EAST = enum.auto()
    NORTH = enum.auto()
    SOUTH = enum.auto()

    def __str__(self):
        return self.name.lower()

    def is_horizontal(self):
        return self in [self.WEST, self.EAST]

    def is_vertical(self):
        return self in [self.NORTH, self.SOUTH]

    @classmethod
    def random(cls, exclude: list = None):
        choices = set(list(cls)) - set(exclude) if exclude else list(cls)
        return random.choice(list(choices))


class BorderCollisionError(Exception):
    """ Thrown when fish stumbles open a border. """
    pass


@enum.unique
class YRegion(enum.Enum):
    TOP = enum.auto()
    MIDDLE = enum.auto()
    BOTTOM = enum.auto()

    def __str__(self):
        return self.name.lower()


@enum.unique
class XRegion(enum.Enum):
    LEFT = enum.auto()
    CENTER = enum.auto()
    RIGHT = enum.auto()

    def __str__(self):
        return self.name.lower()


class Fish:

    def __init__(self, canvas: tk.Canvas):
        self._canvas = canvas
        self._direction = Direction.random()
        self._image = tk.PhotoImage(file=os.path.join('assets', f'fish-{self._direction}.png'))
        self._x_max = self._canvas.winfo_reqwidth() - self._image.width()
        self._y_max = self._canvas.winfo_reqheight() - self._image.height()
        self._x, self._y = self.get_random_coordinates(self._x_max, self._y_max)
        self._id = self._canvas.create_image(self._x, self._y, image=self._image, anchor=tk.NW)
        self._x_region = self._get_x_region()
        self._y_region = self._get_y_region()
        self._velocity = 5
        self._update_time = 100

    def _change_image(self, file: str):
        """ Change fish image on the canvas. """
        self._image = tk.PhotoImage(file=file)
        self._canvas.itemconfig(self._id, image=self._image)

    def _change_direction(self):
        """ Change fish direction and it's image accordingly. """
        if self._direction.is_horizontal():
            if self._y_region is YRegion.TOP:
                self._direction = Direction.random(exclude=[self._direction, Direction.NORTH])
            elif self._y_region is YRegion.MIDDLE:
                self._direction = Direction.random(exclude=[self._direction])
            else:
                self._direction = Direction.random(exclude=[self._direction, Direction.SOUTH])
        else:
            if self._x_region is XRegion.LEFT:
                self._direction = Direction.random(exclude=[self._direction, Direction.WEST])
            elif self._x_region is XRegion.CENTER:
                self._direction = Direction.random(exclude=[self._direction])
            else:
                self._direction = Direction.random(exclude=[self._direction, Direction.EAST])
        self._change_image(os.path.join('assets', f'fish-{self._direction}.png'))

    def swim(self):
        """ """
        try:
            self._swim_forward()
        except BorderCollisionError:
            self._bounce_back()
            self._change_direction()

        self._canvas.after(self._update_time, self.swim)

    def _swim_forward(self):
        """ Swim towards current direction. """
        self._update_position()

        if self._collides_with_border():
            raise BorderCollisionError()

        if self._direction is Direction.WEST:
            self._canvas.move(self._id, -self._velocity, 0)
        elif self._direction is Direction.EAST:
            self._canvas.move(self._id, self._velocity, 0)
        elif self._direction is Direction.NORTH:
            self._canvas.move(self._id, 0, -self._velocity)
        elif self._direction is Direction.SOUTH:
            self._canvas.move(self._id, 0, self._velocity)

    def _update_position(self):
        """ Update current x, y coordinates and regions. """
        self._x, self._y = self._canvas.coords(self._id)
        self._x_region, self._y_region = self._get_x_region(), self._get_y_region()

    def _collides_with_border(self) -> bool:
        """ Check if fish collides with a border in current direction. """
        if self._direction is Direction.WEST:
            return self._x < 0
        if self._direction is Direction.EAST:
            return self._x > self._x_max
        if self._direction is Direction.NORTH:
            return self._y < 0
        if self._direction is Direction.SOUTH:
            return self._y > self._y_max

    def _bounce_back(self):
        """ Bounce back after colliding with a border. """
        if self._direction is Direction.WEST:
            self._canvas.move(self._id, self._velocity, 0)
        elif self._direction is Direction.EAST:
            self._canvas.move(self._id, -self._velocity, 0)
        elif self._direction is Direction.NORTH:
            self._canvas.move(self._id, 0, self._velocity)
        elif self._direction is Direction.SOUTH:
            self._canvas.move(self._id, 0, -self._velocity)

    def _get_x_region(self) -> XRegion:
        if 0 <= self._x <= self._x_max // 3:
            return XRegion.LEFT
        if self._x_max // 3 <= self._x <= self._x_max // 3 * 2:
            return XRegion.CENTER
        if self._x_max // 3 * 2 <= self._x <= self._x_max:
            return XRegion.RIGHT

    def _get_y_region(self) -> YRegion:
        if 0 <= self._y <= self._y_max // 3:
            return YRegion.TOP
        if self._y_max // 3 <= self._y <= self._y_max // 3 * 2:
            return YRegion.MIDDLE
        if self._y_max // 3 * 2 <= self._y <= self._y_max:
            return YRegion.BOTTOM

    @staticmethod
    def get_random_coordinates(width: int, height: int) -> typing.Tuple[int, int]:
        return random.randint(0, width), random.randint(0, height)


if __name__ == '__main__':
    app = Window()
