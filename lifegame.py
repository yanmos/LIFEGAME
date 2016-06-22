#!/usr/bin/env python

import numpy as np
import curses as cs
import time

class lifegame:
    def __init__(self, ny, nx):
        self.field = np.zeros([ny, nx]).astype(np.int)
        self.ny = ny
        self.nx = nx

    def fill_random(self, duty=0.5):
        f = np.random.rand(self.ny, self.nx)
        self.field = np.floor(f + duty).astype(np.int)

    def update_generation(self):
        f = self.field
        next = np.zeros([self.ny, self.nx]).astype(np.int)
        f = np.r_[f[[self.ny - 1], :], f, f[[0], :]]
        f = np.c_[f[:, [self.nx - 1]], f, f[:, [0]]]
        for i in range(0, self.ny):
            for j in range(0, self.nx):
                area = f[i:i + 3, j:j + 3]
                life = np.sum(area) - area[1, 1]
                if area[1, 1] == 1:
                    if life == 2 or life == 3:
                        next[i, j] = 1
                else:
                    if life == 3:
                        next[i, j] = 1
        self.field = next

def display(win, buff, ny, nx):
    for i in range(0, ny):
        for j in range(0, nx):
            win.addch(i, j, buff[i, j])
    win.refresh()

def main(scr):
    mark = ord('*')
    blank = ord(' ')
    tc = 0.5
    scr.clear()
    ny, nx = scr.getmaxyx()
    win = scr.subwin(ny, nx, 0, 0)
    ny -= 1
    nx -= 1
    lg = lifegame(ny, nx)
    lg.fill_random(0.5)
    buff = lg.field * (mark - blank) + blank
    display(win, buff, ny, nx)
    scr.nodelay(1)
    time.sleep(0.5)
    tz1 = time.time()
    while(1):
        c = scr.getch()
        if c == -1:
            lg.update_generation()
            buff = lg.field * (mark - blank) + blank
            display(win, buff, ny, nx)
            tz0 = time.time()
            t = tz0 - tz1
            if t < tc:
                time.sleep(tc - t)
            tz1 = tz0
        elif 0 < c <= 255:
            c = chr(c)
            if c in 'Qq\n':
                break

if __name__ == '__main__':
    cs.wrapper(main)
