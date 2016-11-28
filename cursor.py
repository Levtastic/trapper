#!/usr/bin/env python
# coding: utf-8

import winfunctions as wf


class Clip:
    def __init__(self, bounds):
        self._bounds = bounds
        self._old_bounds = None

    def __del__(self):
        try:
            if self.clipped:
                self.release()
        except AttributeError:
            pass

    @staticmethod
    def clearClips():
        wf.ClipCursor(None)

    @property
    def bounds(self):
        return self._bounds

    def _getClipCursor(self):
        bounds = wf.Bounds()
        wf.GetClipCursor(bounds)

        return bounds

    @property
    def clipped(self):
        return (self._getClipCursor() == self._bounds)

    def clip(self):
        wf.ClipCursor(self._bounds)

    def release(self):
        wf.ClipCursor(None)

    def toggle(self):
        if self.clipped:
            self.release()
        else:
            self.clip()
