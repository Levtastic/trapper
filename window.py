#!/usr/bin/env python
# coding: utf-8

import os
import winfunctions as wf


class Window:
    def __init__(self, hwnd):
        self._hwnd = hwnd

    def __str__(self):
        return self.title or self.process_name or 'Unnamed Window'

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.hwnd == other.hwnd

        return False

    @classmethod
    def getAllWindows(cls):
        windows = []
        def callback(hwnd, lParam):
            windows.append(cls(hwnd))
            return True

        wf.EnumWindows(wf.EnumWindowsProc(callback), 0)

        return windows

    @classmethod
    def getAllTaskbarWindows(cls):
        return [window for window in cls.getAllWindows() if window.taskbar]

    @classmethod
    def getForegroundWindow(cls):
        return cls(wf.GetForegroundWindow())

    @property
    def hwnd(self):
        return self._hwnd

    @property
    def exists(self):
        return wf.IsWindow(self.hwnd) != 0

    @property
    def visible(self):
        return wf.IsWindowVisible(self.hwnd) != 0

    @property
    def owner(self):
        try:
            return self.__class__(wf.GetWindow(self.hwnd, wf.GW_OWNER))
        except OSError:
            return None

    @property
    def root_owner(self):
        owner = self.owner
        if not owner:
            return self

        return self.owner.root_owner

    @property
    def taskbar(self):
        # https://stackoverflow.com/questions/2262726/determining-if-a-window-has-a-taskbar-button

        if not self.visible:
            return False

        try:
            STYLES = wf.GetWindowLongW(self.hwnd, wf.GWL_STYLE)
            EX_STYLES = wf.GetWindowLongW(self.hwnd, wf.GWL_EXSTYLE)
        except OSError:
            return False

        if EX_STYLES & wf.WS_EX_APPWINDOW:
            return True

        if self.owner:
            return False

        if (EX_STYLES & wf.WS_EX_NOACTIVATE) or (EX_STYLES & wf.WS_EX_TOOLWINDOW):
            return False

        if STYLES & wf.WS_CHILD:
            return False

        return True

    @property
    def title(self):
        length = wf.GetWindowTextLengthW(self.hwnd) + 1
        u_buffer = wf.create_unicode_buffer(length)
        wf.GetWindowTextW(self.hwnd, u_buffer, len(u_buffer))
        return u_buffer.value

    @property
    def process_path(self):
        process_id = wf.DWORD()
        wf.GetWindowThreadProcessId(self.hwnd, process_id)

        process = wf.OpenProcess(wf.PROCESS_QUERY_INFORMATION | wf.PROCESS_VM_READ, False, process_id)

        u_buffer = wf.create_unicode_buffer(1024)
        wf.GetModuleFileNameExW(process, None, u_buffer, len(u_buffer))

        wf.CloseHandle(process)

        return u_buffer.value

    @property
    def process_name(self):
        return os.path.basename(self.process_path)

    @property
    def bounds(self):
        bounds = wf.Bounds()
        wf.GetWindowRect(self.hwnd, bounds)
        return bounds

    @property
    def minimised(self):
        return wf.IsIconic(self.hwnd) != 0

    @property
    def foreground(self):
        return wf.GetForegroundWindow() == self.hwnd

    def activate(self):
        if self.minimised:
            wf.OpenIcon(self.hwnd)
        else:
            wf.SetForegroundWindow(self.hwnd)
