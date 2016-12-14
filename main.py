#!/usr/bin/env python
# coding: utf-8

import sys, os

from datetime import datetime

from window import Window
from cursor import Clip
from ui import UI


class App:
    refresh_delay = 500 # half a second

    def __init__(self):
        self.windows = {}
        self.selected_window = None
        self.current_clip = None

        self.ui = ui = UI('Trapper', self.resourcePath, self.refresh_delay)
        ui.add_callback('getListOfWindows', self.getListOfWindows)
        ui.add_callback('changeSelectedWindow', self.changeSelectedWindow)
        ui.add_callback('clipCursor', self.clipCursor)
        ui.add_callback('refreshClip', self.refreshClip)
        ui.add_callback('isClipped', self.isClipped)

    def __del__(self):
        Clip.clearClips()

    @staticmethod
    def resourcePath(relative):
        basedir = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
        return os.path.join(basedir, relative)

    def run(self):
        self.ui.mainloop()

    def getListOfWindows(self):
        self.windows = {str(window): window for window in Window.getAllTaskbarWindows()}
        windows = [(name, window == self.selected_window) for name, window in self.windows.items()]
        return sorted(windows, key=lambda w: w[0])

    def changeSelectedWindow(self, selection):
        self.selected_window = self.windows.get(selection, None)

    def clipCursor(self, selection):
        self.selected_window = self.windows.get(selection, None)

        if self.isClipped():
            if self.current_clip:
                self.current_clip.release()
                self.current_clip = None

            return False

        elif self.selected_window:
            self.current_clip = Clip(self.selected_window.bounds)
            self.current_clip.clip()
            self.ui.root.after(self.refresh_delay, lambda: self.refreshClipLoop(self.current_clip))

            return True

        return False

    def refreshClipLoop(self, previous_clip):
        if (not self.current_clip) or self.current_clip != previous_clip:
            return

        if self.refreshClip():
            self.ui.root.after(self.refresh_delay, lambda: self.refreshClipLoop(self.current_clip))

    def refreshClip(self):
        if (not self.current_clip):
            return

        if (not self.selected_window) or (not self.selected_window.exists):
            self.current_clip.release()
            self.current_clip = None
            return

        window_bounds = self.selected_window.bounds
        if self.current_clip.bounds != window_bounds:
            # window has moved, so get a new clip for the new coords
            self.current_clip.release()
            self.current_clip = Clip(window_bounds)

        self.current_clip.clip()
        
    def isClipped(self):
        return (self.selected_window and self.selected_window.exists
                and self.current_clip and self.current_clip.clipped)


if __name__ == '__main__':
    app = App()
    app.run()
