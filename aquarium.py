#!/usr/bin/python3

import os
import enum
import random
from typing import Tuple
import tkinter as tk

from PIL import ImageTk, Image


class ImageLoader:

    @staticmethod
    def load(path: str) -> tk.PhotoImage:
        return ImageTk.PhotoImage(Image.open(path))


class Window(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._width = 800
        self._height = 600

        self._canvas = tk.Canvas(self, width=self._width, height=self._height)
        self._canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self._fish = Fish(self._canvas, 'blue')
        self._fish.swim()

        self._bg = None
        self._bg_id = None
        self._bg_images = os.listdir(os.path.join('assets', 'bg'))
        self.set_bg(random.choice(self._bg_images))

        self.title('Aquarium')
        self.resizable(0, 0)
        self.geometry(f'{self._width}x{self._height}')

        self.menu = tk.Menu(self)
        self.menu.add_cascade(label='Fish', menu=self._create_fish_menu())
        self.menu.add_cascade(label='Background', menu=self._create_bg_menu())
        self.config(menu=self.menu)

        self.mainloop()

    def set_bg(self, file: str):
        if self._bg:
            self._canvas.delete(self._bg_id)
        self._bg = ImageLoader.load(os.path.join('assets', 'bg', file))
        self._bg_id = self._canvas.create_image(0, 0, image=self._bg, anchor=tk.NW)
        self._fish.repaint()

    def _create_bg_menu(self) -> tk.Menu:
        menu = tk.Menu(self.menu, tearoff=0)
        menu.add_radiobutton(label='First', command=lambda: self.set_bg('1.png'))
        menu.add_radiobutton(label='Second', command=lambda: self.set_bg('2.jpg'))
        menu.add_radiobutton(label='Third', command=lambda: self.set_bg('3.jpg'))
        return menu

    def _create_fish_menu(self) -> tk.Menu:
        menu = tk.Menu(self.menu, tearoff=0)
        menu.add_radiobutton(label='Blue', command=lambda: self._fish.set_sprite('blue'))
        menu.add_radiobutton(label='Yellow', command=lambda: self._fish.set_sprite('yellow'))
        return menu


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
    def get_random_horizontal(cls):
        return random.choice([cls.WEST, cls.EAST])

    @classmethod
    def random(cls, exclude: list = None):
        choices = set(list(cls)) - set(exclude) if exclude else list(cls)
        return random.choice(list(choices))


class BorderCollisionError(Exception):
    """ Thrown when fish stumbles open a border. """
    pass


@enum.unique
class XRegion(enum.Enum):
    LEFT = enum.auto()
    CENTER = enum.auto()
    RIGHT = enum.auto()

    def __str__(self):
        return self.name.lower()

    @classmethod
    def get(cls, x, x_bound):
        if 0 <= x <= x_bound // 3:
            return cls.LEFT
        elif x_bound // 3 <= x <= x_bound // 3 * 2:
            return cls.CENTER
        else:
            return cls.RIGHT


@enum.unique
class YRegion(enum.Enum):
    TOP = enum.auto()
    MIDDLE = enum.auto()
    BOTTOM = enum.auto()

    def __str__(self):
        return self.name.lower()

    @classmethod
    def get(cls, y, y_bound):
        if 0 <= y <= y_bound // 3:
            return cls.TOP
        elif y_bound // 3 <= y <= y_bound // 3 * 2:
            return cls.MIDDLE
        else:
            return cls.BOTTOM


class Fish:

    def __init__(self, canvas: tk.Canvas, sprite: str):
        self._canvas = canvas
        self._sprite = sprite

        self._direction = Direction.get_random_horizontal()
        self._prev_direction = None

        self._image = ImageLoader.load(self._get_image_path())
        self._x_max, self._y_max = self.get_max_xy(self._canvas, self._image)

        self._x, self._y = self.get_random_xy((0, self._x_max), (0, self._y_max))
        self._image_id = self._canvas.create_image(self._x, self._y, image=self._image, anchor=tk.NW)

        self._velocity = 5
        self._update_time = 100

    def set_sprite(self, new_sprite: str):
        """ Change this fish sprite. """
        self._sprite = new_sprite
        self.repaint()

    def repaint(self):
        """ Called by Window to repaint fish above the changed background. """
        self._canvas.delete(self._image_id)
        self._image = ImageLoader.load(self._get_image_path())
        self._image_id = self._canvas.create_image(self._x, self._y, image=self._image, anchor=tk.NW)

    def swim(self):
        """ """
        try:
            self._swim_forward()
        except BorderCollisionError:
            self._bounce_back()
            self._change_direction()

        self._canvas.after(self._update_time, self.swim)

    def _change_image(self):
        """ Change fish image on the canvas. """
        self._canvas.delete(self._image_id)
        self._image = tk.PhotoImage(file=self._get_image_path())
        self._x_max, self._y_max = self.get_max_xy(self._canvas, self._image)
        if self._prev_direction is Direction.WEST:
            self._x = 0
        elif self._prev_direction is Direction.EAST:
            self._x = self._x_max
        elif self._prev_direction is Direction.NORTH:
            self._y = 0
        else:
            self._y = self._y_max
        self._image_id = self._canvas.create_image(self._x, self._y, image=self._image, anchor=tk.NW)

    def _change_direction(self):
        """ Change fish direction and it's image accordingly. """
        self._prev_direction = self._direction
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
        self._change_image()

    def _swim_forward(self):
        """ Swim towards current direction. """
        self._update_position()

        if self._collides_with_border():
            raise BorderCollisionError()

        if self._direction is Direction.WEST:
            self._canvas.move(self._image_id, -self._velocity, 0)
        elif self._direction is Direction.EAST:
            self._canvas.move(self._image_id, self._velocity, 0)
        elif self._direction is Direction.NORTH:
            self._canvas.move(self._image_id, 0, -self._velocity)
        elif self._direction is Direction.SOUTH:
            self._canvas.move(self._image_id, 0, self._velocity)

    def _update_position(self):
        """ Update current x, y coordinates and regions. """
        self._x, self._y = self._canvas.coords(self._image_id)
        self._x_region = XRegion.get(self._x, self._x_max)
        self._y_region = YRegion.get(self._y, self._y_max)

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
            self._canvas.move(self._image_id, self._velocity, 0)
        elif self._direction is Direction.EAST:
            self._canvas.move(self._image_id, -self._velocity, 0)
        elif self._direction is Direction.NORTH:
            self._canvas.move(self._image_id, 0, self._velocity)
        elif self._direction is Direction.SOUTH:
            self._canvas.move(self._image_id, 0, -self._velocity)
        self._update_position()

    def _get_image_path(self) -> str:
        """ Returns the path to the image file depending on the current direction and x region. """
        if self._direction.is_horizontal():
            file = f'{self._direction}.png'
        else:
            file = f'{self._direction}-{self._x_region}.png'
        return os.path.join('assets', 'fish', self._sprite, file)

    @staticmethod
    def get_max_xy(canvas: tk.Canvas, image: tk.PhotoImage):  # TODO: bad name
        return canvas.winfo_reqwidth() - image.width(), canvas.winfo_reqheight() - image.height()

    @staticmethod
    def get_random_xy(x_range: Tuple[int, int], y_range: Tuple[int, int]) -> Tuple[int, int]:
        return random.randint(*x_range), random.randint(*y_range)


if __name__ == '__main__':
    app = Window()
