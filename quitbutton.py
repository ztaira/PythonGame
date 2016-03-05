from tkinter import *


class quitButton(Button):
    def __init__(self, parent):
        Button.__init__(self, parent)
        self['text'] = 'Quit'
        # Command to close the window (the destroy method)
        self['command'] = parent.destroy
        self.pack(side=BOTTOM)
