import os
import enum
import random
import tkinter as tk
from typing import Tuple, List

from PIL import ImageTk, Image


class Window(tk.Tk):

    BG_IMAGES = [
        os.path.join('assets', 'bg', file) for file in os.listdir(os.path.join('assets', 'bg'))
    ]

    def __init__(self, width: int, height: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Menu
        self.menu = Menu(self)
        self.config(menu=Menu(self))
        # Canvas
        self.canvas = Canvas(self, width=width, height=height)
        self.canvas.set_bg_image(random.choice(self.BG_IMAGES))
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        # Self
        self.title('Aquarium')
        self.resizable(0, 0)
        self.geometry(f'{width}x{height}')
        self.mainloop()


class Menu(tk.Menu):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._view_menu = tk.Menu(self._root(), tearoff=0)

        self._view_menu.add_cascade(label='Fish', menu=self._create_fish_menu())
        self._view_menu.add_cascade(label='Background', menu=self._create_bg_menu())

        self.add_cascade(label='View', menu=self._view_menu)

    def _create_fish_menu(self) -> tk.Menu:
        menu = tk.Menu(self, tearoff=0)
        var = tk.StringVar()
        for sprite_name in Fish.SPRITE_NAMES:
            menu.add_radiobutton(
                label=sprite_name.capitalize(),
                variable=var,
                value=sprite_name,
                command=lambda: self._root().canvas.fish.set_sprite_name(var.get())
            )
        return menu

    def _create_bg_menu(self) -> tk.Menu:
        menu = tk.Menu(self, tearoff=0)
        var = tk.StringVar()
        for image_path in self._root().BG_IMAGES:
            _, tail = os.path.split(image_path)
            menu.add_radiobutton(
                label=tail.capitalize()[:-4],
                variable=var,
                value=image_path,
                command=lambda: self._root().canvas.set_bg_image(var.get())
            )
        return menu


class Canvas(tk.Canvas):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Background Image
        self._bg_image = None
        self._bg_image_id = None
        # Fish
        self.fish = Fish(self, 'blue')
        self.fish.swim()

        self.bind('<Button-1>', self._handle_left_click)

    def set_bg_image(self, file_name: str):
        if self._bg_image_id:
            self.delete(self._bg_image_id)
        self._bg_image = Utils.load_image(file_name)
        self._bg_image_id = self.create_image(0, 0, image=self._bg_image, anchor=tk.NW)
        self.fish.repaint()

    def _handle_left_click(self, event):
        if self.fish.check_collision(event.x, event.y):
            self.fish.change_direction()


class Utils:

    @staticmethod
    def load_image(path: str) -> tk.PhotoImage:
        return ImageTk.PhotoImage(Image.open(path))

    @staticmethod
    def get_image_max_xy(canvas: tk.Canvas, image: tk.PhotoImage) -> Tuple[int, int]:
        return canvas.winfo_reqwidth() - image.width(), canvas.winfo_reqheight() - image.height()

    @staticmethod
    def get_random_xy(x_range: Tuple[int, int], y_range: Tuple[int, int]) -> Tuple[int, int]:
        return random.randint(*x_range), random.randint(*y_range)


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


@enum.unique
class Region(enum.Enum):
    """ Represents a region on the Canvas. """
    # X
    LEFT = enum.auto()
    CENTER = enum.auto()
    RIGHT = enum.auto()
    # Y
    TOP = enum.auto()
    MIDDLE = enum.auto()
    BOTTOM = enum.auto()

    def __str__(self):
        return self.name.lower()

    @classmethod
    def get(cls, x: int, x_max: int, y: int, y_max: int) -> Tuple['Region', 'Region']:
        """ """
        if 0 <= x <= x_max // 3:
            x_region = cls.LEFT
        elif x_max // 3 <= x <= x_max // 3 * 2:
            x_region = cls.CENTER
        else:
            x_region = cls.RIGHT

        if 0 <= y <= y_max // 3:
            y_region = cls.TOP
        elif y_max // 3 <= y <= y_max // 3 * 2:
            y_region = cls.MIDDLE
        else:
            y_region = cls.BOTTOM

        return x_region, y_region


class BorderCollisionError(Exception):
    """ Thrown when fish collides with a border. """


class Fish:

    SPRITE_NAMES = os.listdir(os.path.join('assets', 'fish'))

    def __init__(self, canvas: tk.Canvas, sprite_name: str):
        self._canvas = canvas
        self._sprite_name = sprite_name

        self._direction = Direction.get_random_horizontal()
        self._prev_direction = None

        self._image = Utils.load_image(self._get_image_path())
        self._x_max, self._y_max = Utils.get_image_max_xy(self._canvas, self._image)

        self._x, self._y = Utils.get_random_xy((0, self._x_max), (0, self._y_max))
        self._image_id = self._canvas.create_image(self._x, self._y, image=self._image, anchor=tk.NW)

        self._region = Region.get(self._x, self._x_max, self._y, self._y_max)

        self._velocity = 5
        self._update_time = 100

    def set_sprite_name(self, new_sprite_name: str):
        """ """
        self._sprite_name = new_sprite_name
        self.repaint()

    def change_direction(self):
        """ """
        self._prev_direction = self._direction
        exclude_directions: List[Direction] = [self._direction]
        if self._direction.is_horizontal():
            if self._region[1] is Region.TOP:
                exclude_directions.append(Direction.NORTH)
            elif self._region[1] is Region.BOTTOM:
                exclude_directions.append(Direction.SOUTH)
        else:
            if self._region[0] is Region.LEFT:
                exclude_directions.append(Direction.WEST)
            elif self._region[0] is Region.RIGHT:
                exclude_directions.append(Direction.EAST)
        print(f'exclude_directions: {exclude_directions}')
        self._direction = Direction.random(exclude=exclude_directions)
        print(f'direction is {self._direction}')
        self.repaint()

    def check_collision(self, x: int, y: int) -> bool:
        """ """
        return self._x <= x <= self._x + self._image.width() and self._y <= y <= self._y + self._image.height()

    def repaint(self):
        """ """
        self._canvas.delete(self._image_id)

        new_image = Utils.load_image(self._get_image_path())
        if self._prev_direction is Direction.EAST:
            self._x += self._image.width() - new_image.width()
        elif self._prev_direction is Direction.SOUTH:
            self._y += self._image.height() - new_image.height()
        self._image = new_image

        self._x_max, self._y_max = Utils.get_image_max_xy(self._canvas, self._image)
        self._image_id = self._canvas.create_image(self._x, self._y, image=self._image, anchor=tk.NW)

    def swim(self):
        """ """
        try:
            self._move_forward()
        except BorderCollisionError:
            self._handle_border_collision()
        finally:
            self._update_position()

        self._canvas.after(self._update_time, self.swim)

    def _move_forward(self):
        """ Move toward direction. """
        self._check_border_collision()

        if self._direction is Direction.WEST:
            x_move, y_move = -self._velocity, 0
        elif self._direction is Direction.EAST:
            x_move, y_move = self._velocity, 0
        elif self._direction is Direction.NORTH:
            x_move, y_move = 0, -self._velocity
        else:
            x_move, y_move = 0, self._velocity

        self._canvas.move(self._image_id, x_move, y_move)

    def _move_backward(self):
        """ Move toward opposite direction. """
        if self._direction is Direction.WEST:
            x_move, y_move = self._velocity, 0
        elif self._direction is Direction.EAST:
            x_move, y_move = -self._velocity, 0
        elif self._direction is Direction.NORTH:
            x_move, y_move = 0, self._velocity
        else:
            x_move, y_move = 0, -self._velocity

        self._canvas.move(self._image_id, x_move, y_move)

    def _update_position(self):
        """ Update self._x, self._y coordinates and regions. """
        self._x, self._y = self._canvas.coords(self._image_id)
        self._region = Region.get(self._x, self._x_max, self._y, self._y_max)

    def _handle_border_collision(self):
        self._move_backward()
        self.change_direction()

    def _check_border_collision(self):
        """ Raises BorderCollisionError if fish collides with a border. """
        if self._direction is Direction.WEST:
            collision_condition = self._x < 0
        elif self._direction is Direction.EAST:
            collision_condition = self._x > self._x_max
        elif self._direction is Direction.NORTH:
            collision_condition = self._y < 0
        else:
            collision_condition = self._y > self._y_max

        if collision_condition:
            raise BorderCollisionError(f'Border collision occurred in {self._direction} direction.')

    def _get_image_path(self) -> str:
        """ Returns the path to the image file depending on the current direction and x region. """
        if self._direction.is_horizontal():
            file = f"{self._direction}.png"
        elif self._region[0] is Region.CENTER:
            file = f"{self._direction}-{random.choice(['left', 'right'])}.png"
        else:
            file = f"{self._direction}-{self._region[0]}.png"
        return os.path.join('assets', 'fish', self._sprite_name, file)


if __name__ == '__main__':
    app = Window(800, 600)
