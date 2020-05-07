#!/usr/bin/python3

import os
import random
import tkinter as tk


class Window:

    TITLE = 'Aquarium'
    WIDTH, HEIGHT = 800, 600
    BG_IMAGE_FILENAME = os.path.join('assets', 'sea.png')

    def __init__(self):
        self._master = self._create_master()
        self._canvas = self._create_canvas()

        bg_image = tk.PhotoImage(file=self.BG_IMAGE_FILENAME)
        self._bg = self._canvas.create_image(0, 0, image=bg_image, anchor=tk.NW)

        self._fish = Fish(self._canvas)
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


class Fish:

    FISH_IMAGE_FILENAME = os.path.join('assets', 'fish.png')
    NORTH, SOUTH, WEST, EAST = range(4)

    def __init__(self, canvas):
        self._canvas = canvas
        self._image = tk.PhotoImage(file=self.FISH_IMAGE_FILENAME)

        self._x = 300
        self._y = 250
        self._vel = 7
        self._update_time = 100  # milliseconds
        self._dir = self.EAST

        self._item_id = self._canvas.create_image(
            self._x, self._y, image=self._image, anchor=tk.NW
        )

    def move(self):
        '''  '''
        width = self._canvas.winfo_reqwidth()
        height = self._canvas.winfo_reqheight()
        self._x, self._y = self._canvas.coords(self._item_id)

        if self._dir == self.EAST:
            if self._x < width - self._image.width():
                self._canvas.move(self._item_id, self._vel, 0)
            else:
                self._dir = random.choice([self.NORTH, self.SOUTH, self.WEST])
        elif self._dir == self.WEST:
            if self._x > 0:
                self._canvas.move(self._item_id, -self._vel, 0)
            else:
                self._dir = random.choice([self.NORTH, self.SOUTH, self.EAST])
        elif self._dir == self.SOUTH:
            if self._y < height - self._image.height():
                self._canvas.move(self._item_id, 0, self._vel)
            else:
                self._dir = random.choice([self.NORTH, self.WEST, self.EAST])
        elif self._dir == self.NORTH:
            if self._y > 0:
                self._canvas.move(self._item_id, 0, -self._vel)
            else:
                self._dir = random.choice([self.WEST, self.SOUTH, self.EAST])

        self._canvas.after(self._update_time, self.move)


if __name__ == '__main__':
    app = Window()
