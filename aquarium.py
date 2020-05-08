#!/usr/bin/python3

import os
import enum
import random
from typing import Tuple
import tkinter as tk


class Asset:

    DIRECTORY = 'assets'

    @classmethod
    def path(cls, file: str) -> str:
        return os.path.join(cls.DIRECTORY, file)


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

        fish = Fish(canvas)
        fish.swim()

        self.mainloop()


class CustomEnum(enum.Enum):

    def __str__(self):
        return self.name.lower()

    @classmethod
    def random(cls, exclude: 'CustomEnum' = None):
        choices = set(list(cls)) - set([exclude]) if exclude else list(cls)
        return random.choice(list(choices))


@enum.unique
class Region(CustomEnum):

    TOP_LEFT = enum.auto()
    TOP_CENTER = enum.auto()
    TOP_RIGHT = enum.auto()

    MIDDLE_LEFT = enum.auto()
    MIDDLE_CENTER = enum.auto()
    MIDDLE_RIGHT = enum.auto()

    BOTTOM_LEFT = enum.auto()
    BOTTOM_CENTER = enum.auto()
    BOTTOM_RIGHT = enum.auto()

    def x_part(self) -> str:
        ''' Returns LEFT, CENTER, or RIGHT. '''
        return self.name.split('_')[1]

    def y_part(self) -> str:
        ''' Return TOP, MIDDLE, or BOTTOM. '''
        return self.name.split('_')[0]

    def rand_coords(self, width, height) -> Tuple[int, int]:
        ''' Return random coordinates for this region. '''
        x_step = width // 3
        y_step = height // 3

        ranges = {
            'LEFT':   (0, x_step),
            'CENTER': (x_step, x_step * 2),
            'RIGHT':  (x_step * 2, x_step * 3),
            'TOP':    (0, y_step),
            'MIDDLE': (y_step, y_step * 2),
            'BOTTOM': (y_step * 2, y_step * 3),
        }

        x_range = ranges[self.x_part()]
        y_range = ranges[self.y_part()]

        return (random.randint(*x_range), random.randint(*y_range))


@enum.unique
class Direction(CustomEnum):

    WEST = enum.auto()
    EAST = enum.auto()
    NORTH = enum.auto()
    SOUTH = enum.auto()

    @classmethod
    def hrandom(cls) -> 'Direction':
        ''' h - horizontal. '''
        return random.choice([cls.WEST, cls.EAST])

    @classmethod
    def vrandom(cls) -> 'Direction':
        ''' v -vertical. '''
        return random.choice([cls.NORTH, cls.SOUTH])


class BorderCollisionError(Exception):
    pass


class Fish:

    def __init__(self, canvas):
        self._canvas = canvas
        self._region = Region.random()
        self._direction = Direction.random()
        self._velocity = 5
        self._update_time = 100
        file = Asset.path(f'fish-{self._direction}.png')
        self._image = tk.PhotoImage(file=file)
        self._x_max = self._canvas.winfo_reqwidth() - self._image.width()
        self._y_max = self._canvas.winfo_reqheight() - self._image.height()
        self._x, self._y = self._region.rand_coords(self._x_max, self._y_max)
        self._id = self._canvas.create_image(
            self._x, self._y, image=self._image, anchor=tk.NW
        )

    @property
    def image(self) -> tk.PhotoImage:
        return self._image

    @property
    def direction(self) -> 'Direction':
        return self._direction

    @property
    def region(self) -> 'Region':
        return self._region

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def update_time(self) -> int:
        return self._update_time

    @image.setter
    def image(self, file: str):
        ''' Change fish image on the canvas. '''
        self._image = tk.PhotoImage(file=file)
        self._canvas.itemconfig(self._id, image=self._image)

    @direction.setter
    def direction(self, direction: 'Direction'):
        ''' Change fish direction and it's image respectively. '''
        self._direction = direction
        self.image = Asset.path(f'fish-{self._direction}.png')

    def swim(self):
        '''  '''
        try:
            self.swim_forward()
        except BorderCollisionError:
            self.direction = Direction.random(exclude=self._direction)

        self._canvas.after(self._update_time, self.swim)

    def _update_position(self):
        self._x, self._y = self._canvas.coords(self._id)

    def swim_forward(self):
        '''  '''
        self._update_position()

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
