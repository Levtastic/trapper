#!/usr/bin/env python
# coding: utf-8

from ctypes import *
from ctypes.wintypes import *


class Bounds(RECT):
    def __eq__(self, other):
        return (
            self.left == other.left and
            self.top == other.top and
            self.right == other.right and
            self.bottom == other.bottom
        )


def errorIfFalse(result, func, args):
    if not result:
        raise WinError()

    return result

IsWindow = windll.user32.IsWindow
IsWindow.argtypes = [HWND]
IsWindow.restype = BOOL

GetWindowLongW = windll.user32.GetWindowLongW
GetWindowLongW.argtypes = [HWND, c_int]
GetWindowLongW.restype = c_long
GetWindowLongW.errcheck = errorIfFalse

GWL_EXSTYLE = -20
GWL_STYLE = -16

WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080
WS_EX_NOACTIVATE = 0x08000000

WS_CHILD = 0x40000000

GetWindow = windll.user32.GetWindow
GetWindow.argtypes = [HWND, c_uint]
GetWindow.restype = HWND
GetWindow.errcheck = errorIfFalse

GW_OWNER = 4

IsWindowVisible = windll.user32.IsWindowVisible
IsWindowVisible.argtypes = [HWND]
IsWindowVisible.restype = BOOL

GetWindowTextLengthW = windll.user32.GetWindowTextLengthW
GetWindowTextLengthW.argtypes = [HWND]
GetWindowTextLengthW.restype = c_int

GetWindowTextW = windll.user32.GetWindowTextW
GetWindowTextW.argtypes = [HWND, LPWSTR, c_int]
GetWindowTextW.restype = c_int

GetWindowThreadProcessId = windll.user32.GetWindowThreadProcessId
GetWindowThreadProcessId.argtypes = [HWND, POINTER(DWORD)]
GetWindowThreadProcessId.restype = DWORD

OpenProcess = windll.kernel32.OpenProcess
OpenProcess.argtypes = [DWORD, BOOL, DWORD]
OpenProcess.restype = HANDLE

PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010

CloseHandle = windll.kernel32.CloseHandle
CloseHandle.argtypes = [HANDLE]
CloseHandle.restype = BOOL
CloseHandle.errcheck = errorIfFalse

GetModuleFileNameExW = windll.psapi.GetModuleFileNameExW
GetModuleFileNameExW.argtypes = [HANDLE, HMODULE, LPWSTR, DWORD]
GetModuleFileNameExW.restype = DWORD

GetWindowRect = windll.user32.GetWindowRect
GetWindowRect.argtypes = [HWND, LPRECT]
GetWindowRect.restype = BOOL
GetWindowRect.errcheck = errorIfFalse

IsIconic = windll.user32.IsIconic
IsIconic.argtypes = [HWND]
IsIconic.restype = BOOL

EnumWindowsProc = WINFUNCTYPE(BOOL, HWND, LPARAM)
EnumWindows = windll.user32.EnumWindows
EnumWindows.argtypes = [EnumWindowsProc, LPARAM]
EnumWindows.restype = BOOL
EnumWindows.errcheck = errorIfFalse

GetForegroundWindow = windll.user32.GetForegroundWindow
GetForegroundWindow.argtypes = []
GetForegroundWindow.restype = HWND

OpenIcon = windll.user32.OpenIcon
OpenIcon.argtypes = [HWND]
OpenIcon.restype = BOOL
OpenIcon.errcheck = errorIfFalse

SetForegroundWindow = windll.user32.SetForegroundWindow
SetForegroundWindow.argtypes = [HWND]
SetForegroundWindow.restype = BOOL
SetForegroundWindow.errcheck = errorIfFalse

ClipCursor = windll.user32.ClipCursor
ClipCursor.argtypes = [LPRECT] # null to unclip
ClipCursor.restype = BOOL
ClipCursor.errcheck = errorIfFalse

GetClipCursor = windll.user32.GetClipCursor
GetClipCursor.argtypes = [LPRECT]
GetClipCursor.restype = BOOL
GetClipCursor.errcheck = errorIfFalse
