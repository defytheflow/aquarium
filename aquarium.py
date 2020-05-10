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

    @classmethod
    def random(cls, exclude: 'Direction' = None):
        choices = set(list(cls)) - {exclude} if exclude else list(cls)
        return random.choice(list(choices))

    @classmethod
    def random_horizontal(cls) -> 'Direction':
        return random.choice([cls.WEST, cls.EAST])

    @classmethod
    def random_vertical(cls) -> 'Direction':
        return random.choice([cls.NORTH, cls.SOUTH])


class BorderCollisionError(Exception):
    """ Thrown when fish stumbles open a border. """
    pass


class Fish:

    def __init__(self, canvas):
        self._canvas = canvas
        self._direction = Direction.random()
        self._image = tk.PhotoImage(file=os.path.join('assets', f'fish-{self._direction}.png'))
        self._x_max = self._canvas.winfo_reqwidth() - self._image.width()
        self._y_max = self._canvas.winfo_reqheight() - self._image.height()
        self._x, self._y = self.get_random_coordinates(self._x_max, self._y_max)
        self._velocity = 5
        self._update_time = 100
        self._id = self._canvas.create_image(self._x, self._y, image=self._image, anchor=tk.NW)

    @property
    def image(self) -> tk.PhotoImage:
        return self._image

    @property
    def direction(self) -> Direction:
        return self._direction

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def update_time(self) -> int:
        return self._update_time

    def set_image(self, file: str):
        """ Change fish image on the canvas. """
        self._image = tk.PhotoImage(file=file)
        self._canvas.itemconfig(self._id, image=self._image)

    def set_direction(self, direction: Direction):
        """ Change fish direction and it's image accordingly. """
        self._direction = direction
        self.set_image(os.path.join('assets', f'fish-{self._direction}.png'))

    def swim(self):
        """ """
        try:
            self.swim_forward()
        except BorderCollisionError:
            self.set_direction(Direction.random(exclude=self._direction))

        self._canvas.after(self._update_time, self.swim)

    def swim_forward(self):
        self._update_coordinates()

        border_collision = {
            Direction.WEST:  self._x < 0,
            Direction.EAST:  self._x > self._x_max,
            Direction.NORTH: self._y < 0,
            Direction.SOUTH: self._y > self._y_max,
        }

        if border_collision[self._direction]:
            raise BorderCollisionError()

        offset = {
            Direction.WEST:  (-self._velocity, 0),
            Direction.EAST:  (self._velocity,  0),
            Direction.NORTH: (0, -self._velocity),
            Direction.SOUTH: (0,  self._velocity),
        }

        off_x, off_y = offset[self._direction]
        self._canvas.move(self._id, off_x, off_y)

    def _update_coordinates(self):
        self._x, self._y = self._canvas.coords(self._id)

    @staticmethod
    def get_random_coordinates(width: int, height: int) -> typing.Tuple[int, int]:
        return random.randint(0, width), random.randint(0, height)


if __name__ == '__main__':
    app = Window()
