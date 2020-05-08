#!/usr/bin/python3

import os
import enum
import random
import tkinter as tk


class Window(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._bg = tk.PhotoImage(file=Asset.path('bg.png'))
        self._width = 800
        self._height = 600

        self.title('Aquarium')
        self.resizable(0, 0)
        self.geometry(f'{self._width}x{self._height}')

        canvas = tk.Canvas(self, width=self._width, height=self._height)
        canvas.create_image(0, 0, image=self._bg, anchor=tk.NW)
        canvas.pack(expand=tk.YES, fill=tk.BOTH)

        fish = Fish(canvas, 0, 0)
        fish.swim()

        self.mainloop()


@enum.unique
class Direction(enum.Enum):

    WEST = enum.auto()
    EAST = enum.auto()
    NORTH = enum.auto()
    SOUTH = enum.auto()

    def __str__(self):
        return self.name.lower()

    @classmethod
    def hrandom(cls) -> 'Direction':
        ''' h - horizontal. '''
        return random.choice([cls.WEST, cls.EAST])

    @classmethod
    def vrandom(cls) -> 'Direction':
        ''' v -vertical. '''
        return random.choice([cls.NORTH, cls.SOUTH])

    @classmethod
    def random(cls) -> 'Direction':
        return random.choice(list(cls))


class Asset:

    DIRECTORY = 'assets'

    @classmethod
    def path(cls, file: str) -> str:
        return os.path.join(cls.DIRECTORY, file)


class BorderCollisionError(Exception):
    pass


class Fish:

    def __init__(self, canvas, x=0, y=0, direction=Direction.hrandom()):
        self._canvas = canvas
        self._direction = direction
        self._image = tk.PhotoImage(file=Asset.path(f'fish-{direction}.png'))
        self._id = canvas.create_image(x, y, image=self._image, anchor=tk.NW)
        self._x = x
        self._y = y
        self._x_max = self._canvas.winfo_reqwidth() - self._image.width()
        self._y_max = self._canvas.winfo_reqheight() - self._image.height()
        self._velocity = 5
        self._update_time = 100

    @property
    def image(self) -> tk.PhotoImage:
        return self._image

    @image.setter
    def image(self, file: str):
        self._image = tk.PhotoImage(file=Asset.path(file))
        self._canvas.itemconfig(self._id, image=self._image)

    @property
    def direction(self) -> 'Direction':
        return self._direction

    @direction.setter
    def direction(self, direction: 'Direction'):
        '''  '''
        self._direction = direction
        self.image = f'fish-{self._direction}.png'

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def update_time(self) -> int:
        return self._update_time

    def swim(self):
        '''  '''
        try:
            self.swim_forward()
        except BorderCollisionError:
            self.direction = Direction.random()

        self._canvas.after(self._update_time, self.swim)

    def swim_forward(self):
        '''  '''
        self._x, self._y = self._canvas.coords(self._id)

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


if __name__ == '__main__':
    app = Window()
