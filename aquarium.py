#!/usr/bin/python3

import os
from enum import Enum
import random
import tkinter as tk


BG_IMAGE_FILENAME = os.path.join('assets', 'bg.png')
FISH_IMAGE_FILENAME = os.path.join('assets', 'fish_west.png')


class Window:

    TITLE = 'Aquarium'
    WIDTH, HEIGHT = 800, 600

    def __init__(self):
        self._master = self._create_master()
        self._canvas = self._create_canvas()

        self._bg = CanvasImage(self._canvas, 0, 0, BG_IMAGE_FILENAME)
        self._fish = Fish(self._canvas, 300, 250, FISH_IMAGE_FILENAME)

        self._fish.move()
        self._master.mainloop()

    def _create_master(self) -> tk.Tk:
        ''' Configure and return an instance of 'tk.Tk'. '''
        master = tk.Tk()
        master.title(self.TITLE)
        master.resizable(width=False, height=False)
        master.geometry(f'{self.WIDTH}x{self.HEIGHT}')
        return master

    def _create_canvas(self) -> tk.Canvas:
        ''' Configure and return an instance of 'tk.Canvas'. '''
        canvas = tk.Canvas(self._master, width=self.WIDTH, height=self.HEIGHT)
        canvas.pack(expand=tk.YES, fill=tk.BOTH)
        return canvas


class CanvasImage:

    def __init__(self, canvas, x, y, filename):
        self._canvas = canvas
        self._x = x
        self._y = y
        self._image = tk.PhotoImage(file=filename)
        self._x_max = self._canvas.winfo_reqwidth() - self._image.width()
        self._y_max = self._canvas.winfo_reqheight() - self._image.height()
        self._item_id = self._canvas.create_image(
            self._x, self._y, image=self._image, anchor=tk.NW
        )


class Direction(Enum):

    WEST = 0
    EAST = 1
    NORTH = 2
    SOUTH = 3
    NORTH_WEST = 4
    NORTH_EAST = 5
    SOUTH_WEST = 6
    SOUTH_EAST = 7

    @classmethod
    def list(cls) -> list:
        return [
            cls.WEST, cls.EAST, cls.NORTH, cls.SOUTH, cls.NORTH_WEST,
            cls.NORTH_EAST, cls.SOUTH_WEST, cls.SOUTH_EAST
        ]

    @classmethod
    def random(cls) -> int:
        return random.choice(cls.list())


class Fish(CanvasImage):

    DIRECTIONS = Direction.list()

    def __init__(self, canvas, x, y, filename):
        super().__init__(canvas, x, y, filename)

        self._velocity = 6
        self._update_time = 90

        self._direction = Direction.WEST
        self._prev_direction = None

    def set_image(self, filename):
        self._image = tk.PhotoImage(file=filename)
        self._canvas.itemconfig(self._item_id, image=self._image)

    def _can_move_forward(self):
        '''  '''
        if self._direction == Direction.NORTH:
            return self._y > 0

        elif self._direction == Direction.SOUTH:
            return self._y < self._y_max

        elif self._direction == Direction.EAST:
            return self._x < self._x_max

        elif self._direction == Direction.WEST:
            return self._x > 0

        elif self._direction == Direction.NORTH_WEST:
            return self._y > 0 and self._x > 0

        elif self._direction == Direction.NORTH_EAST:
            return self._y > 0 and self._x < self._x_max

        elif self._direction == Direction.SOUTH_WEST:
            return self._x > 0 and self._y < self._y_max

        elif self._direction == Direction.SOUTH_EAST:
            return self._x < self._x_max and self._y < self._y_max

    def _move_forward(self):
        '''  '''
        if self._direction == Direction.NORTH:
            self._canvas.move(self._item_id, 0, -self._velocity)

        elif self._direction == Direction.SOUTH:
            self._canvas.move(self._item_id, 0, self._velocity)

        elif self._direction == Direction.EAST:
            self._canvas.move(self._item_id, self._velocity, 0)

        elif self._direction == Direction.WEST:
            self._canvas.move(self._item_id, -self._velocity, 0)

        elif self._direction == Direction.NORTH_WEST:
            self._canvas.move(self._item_id, -self._velocity, -self._velocity)

        elif self._direction == Direction.NORTH_EAST:
            self._canvas.move(self._item_id, self._velocity, -self._velocity)

        elif self._direction == Direction.SOUTH_WEST:
            self._canvas.move(self._item_id, -self._velocity, self._velocity)

        elif self._direction == Direction.SOUTH_EAST:
            self._canvas.move(self._item_id, self._velocity, self._velocity)

        filename = f'fish_{self._direction.name.lower()}.png'
        self.set_image(os.path.join('assets', filename))

    def move(self):
        '''  '''
        self._x, self._y = self._canvas.coords(self._item_id)

        if self._can_move_forward():
            self._move_forward()
        else:
            self._direction = Direction.random()

        self._canvas.after(self._update_time, self.move)


if __name__ == '__main__':
    app = Window()
