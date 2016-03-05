# Note: This is a moving particle, contained in a window.
# This is NOT a standalone moving particle class.


# =======================================================================

from tkinter import *
import fuckthis


class ControlledParticle(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.canvas = Canvas(parent, width=800, height=650)
        self.canvas.pack(expand=YES, fill=BOTH)
        parent.bind('<KeyPress>', self.onKeyPress)
        parent.bind('<KeyRelease>', self.onKeyRelease)
        # velocity and object variables
        self.acceleration = [0, 0]
        self.velocity = [0, 0]
        self.position = [400, 325]
        self.items = [0]
        self.radius = 15
        # key press variables variables
        self.up_press = 0
        self.right_press = 0
        self.down_press = 0
        self.left_press = 0
        # to things on the canvas
        self.update_time = 1
        self.draw_circle(self.position[0], self.position[1], self.radius)
        self.draw()

    def draw(self):
        """updates the canvas"""
        self.update_position()
        self.after(self.update_time, self.draw)

    def onKeyPress(self, event):
        """handles key presses"""
        if event.char == ',' or event.char == '<':
            self.up_press = 1
        elif event.char == 'o' or event.char == 'O':
            self.down_press = 1
        elif event.char == 'a' or event.char == 'A':
            self.left_press = 1
        elif event.char == 'e' or event.char == 'E':
            self.right_press = 1

    def onKeyRelease(self, event):
        """handles key releases"""
        if event.char == ',' or event.char == '<':
            self.up_press = 0
        elif event.char == 'o' or event.char == 'O':
            self.down_press = 0
        elif event.char == 'a' or event.char == 'A':
            self.left_press = 0
        elif event.char == 'e' or event.char == 'E':
            self.right_press = 0

    def update_position(self):
        """updates position values according to kinematic equations"""
        # Up and down arrow keys, on the y axis. Handles acceleration
        if self.up_press == 1 and self.down_press == 1:
            self.acceleration[1] = 0
        elif self.up_press == 1:
            self.acceleration[1] = -2
        elif self.down_press == 1:
            self.acceleration[1] = 2
        else:
            self.acceleration[1] = 0
        # left and right arrow keys, on the x axis. Handles acceleration.
        if self.left_press == 1 and self.right_press == 1:
            self.acceleration[0] = 0
        elif self.left_press == 1:
            self.acceleration[0] = -2
        elif self.right_press == 1:
            self.acceleration[0] = 2
        else:
            self.acceleration[0] = 0
        # update the velocity values using the acceleration values. Includes damper
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]
        self.velocity[0] *= 0.9
        self.velocity[1] *= 0.9
        if self.position[0] < 10 and self.velocity[0] < 0:
            self.velocity[0] = -self.velocity[0]
        if self.position[0] > 750 and self.velocity[0] > 0:
            self.velocity[0] = -self.velocity[0]
        if self.position[1] < 10 and self.velocity[1] < 0:
            self.velocity[1] = -self.velocity[1]
        if self.position[1] > 600 and self.velocity[1] > 0:
            self.velocity[1] = -self.velocity[1]
        # update the position values using the velocity values
        self.canvas.move(self.items[0], self.velocity[0], self.velocity[1])
        self.position = self.canvas.coords(self.items[0])

    def draw_circle(self, x_origin, y_origin, radius):
        """draws a circle with radius radius at (x_origin, y_origin)"""
        self.items[0] = self.canvas.create_oval((x_origin-radius, y_origin-radius, x_origin+radius, y_origin+radius), fill='grey', activefill='black')

if __name__ == '__main__':
    window = Tk()
    quitter = fuckthis.quitButton(window)
    snake = ControlledParticle(window)
