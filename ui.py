#!/usr/bin/env python
# coding: utf-8

from tkinter import *
from tkinter.ttk import *


class UI:
    width = 550
    height = 350
    minwidth = 120
    minheight = 90

    def __init__(self, app_name, resource_path_func, list_refresh_delay):
        self.list_refresh_delay = list_refresh_delay

        self.windows = {}
        self.callbacks = {}

        self.root = root = Tk()
        root.title(app_name)
        root.geometry('{}x{}'.format(self.width, self.height))
        root.minsize(self.minwidth, self.minheight)
        root.iconbitmap(resource_path_func('icon.ico'))
        root.columnconfigure(0, weight=1)

        self.buttons = Buttons(root)

        self.list = WindowsList(root)
        root.rowconfigure(1, weight=1)

        self.buttons.clip_button.configure(command=self.clip_button_clicked)
        self.list.results_listbox.bind('<<ListboxSelect>>', self.selection_changed)
        self.root.after(1, self.refreshWindowListLoop)

    @property
    def mainloop(self):
        return self.root.mainloop

    def add_callback(self, key, callback):
        self.callbacks[key] = callback

    def remove_callback(self, key):
        del self.callbacks[key]

    def run_callback(self, key, *args):
        return self.callbacks[key](*args)

    def clip_button_clicked(self):
        listbox = self.list.results_listbox

        selection = listbox.curselection()
        if not selection:
            return

        index = int(selection[0])
        value = listbox.get(index)
        clipping = self.run_callback('clipCursor', value)

        self.refreshIfClipped(clipping)

    def refreshIfClipped(self, is_clipped = None):
        if is_clipped is None:
            self.run_callback('refreshClip')
            is_clipped = self.run_callback('isClipped')

        button = self.buttons.clip_button
        listbox = self.list.results_listbox
        label = self.list.results_label

        button_text = 'Unclip' if is_clipped else 'Clip'
        button.configure(text=button_text)

        listbox_state = DISABLED if is_clipped else NORMAL
        listbox.configure(state=listbox_state)

        if is_clipped:
            label.grid()
        else:
            label.grid_remove()

    def selection_changed(self, event):
        listbox = event.widget
        label = self.list.results_label

        selection = listbox.curselection()
        if not selection:
            return

        index = int(selection[0])
        value = listbox.get(index)

        label.config(text=value)

        clipping = self.run_callback('changeSelectedWindow', value)

    def refreshWindowListLoop(self):
        self.refreshWindowList()
        self.root.after(self.list_refresh_delay, self.refreshWindowListLoop)

    def refreshWindowList(self):
        listbox = self.list.results_listbox
        label = self.list.results_label
        disabled = listbox.cget('state') == DISABLED

        if disabled:
            listbox.config(state=NORMAL)

        listbox.delete(0, END)

        for title, selected in self.run_callback('getListOfWindows'):
            listbox.insert(END, title)
            if selected:
                label.config(text=title)
                index = listbox.size() - 1
                listbox.selection_set(index)
                listbox.activate(index)

        if disabled:
            listbox.config(state=DISABLED)

        self.refreshIfClipped()


class Section(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid(sticky=N+E+W+S, padx=1, pady=1)
        self.createWidgets()


class Buttons(Section):
    def createWidgets(self):
        button = Button(self, text='Clip', style='TButton')
        button.grid(sticky=N+E+W+S, padx=5, pady=5)

        self.columnconfigure(0, weight=1)

        self.clip_button = button


class WindowsList(Section):
    def createWidgets(self):
        label = Label(self)
        scrollbar = AutoScrollbar(self, orient=VERTICAL)
        listbox = Listbox(self, yscrollcommand=scrollbar.set, exportselection=0)
        scrollbar.config(command=listbox.yview)

        label.grid(row=0, columnspan=2)
        label.grid_remove()
        listbox.grid(row=1, column=0, sticky=N+E+W+S)
        scrollbar.grid(row=1, column=1, sticky=N+S)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.results_label = label
        self.results_listbox = listbox


class AutoScrollbar(Scrollbar):
    def set(self, low, high):
        if float(low) <= 0.0 and float(high) >= 1.0:
            self.grid_remove()
        else:
            self.grid()

        Scrollbar.set(self, low, high)
