# Note: This is class meant to handle the canvas and key binding things.

# =======================================================================


from tkinter import *
from shapely.geometry import LineString
from shapely.geometry import LinearRing
import quitbutton
import ControlledParticle
import SuperMissile
import ArrayMissile
import HomingMissile
import time
import DriftingParticle
import random
from threading import Thread
from threading import Lock


class CanvasWindow(Frame):
    """This is a class with a generic canvas meant to handle displays and
     popular key bindings, in order to play a game"""
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.canvas = Canvas(parent, width=800, height=650, bg='white')
        self.image = PhotoImage(file = 'background.gif')
        self.canvas.create_image(0, 0, image = self.image, anchor = NW)
        self.canvas.pack(expand=YES, fill=BOTH)

        # bindings for key presses, key releases, and mouse clicks
        self.initialize_key_bindings(parent)

        # variables to store the items
        self.initialize_item_variables()

        # variables needed to store button/mouse press data
        self.initialize_key_variables()

        # variables which do things on the canvas
        self.draw_environment()
        self.clock = time.time()
        self.my_lock = Lock()
        self.start_draw_thread()

    def start_draw_thread(self):
        """starts a thread that runs draw()"""
        t = Thread(target=self.draw(), args=())
        t.start()

    def draw(self):
        """updates the canvas"""
        self.my_lock.acquire()
        self.hitboxes = []
        self.update_clocks(0)
        # for each item in the list of items
        for item in range(len(self.items)):
            # get the new position and the old position
            new_pos = self.items[item].update_position(
                self.up_press,
                self.down_press,
                self.left_press,
                self.right_press,
                self.mouse_position[0],
                self.mouse_position[1])
            old_pos = self.canvas.coords(self.sprites[item])
            # store each hitbox and the movement path
            self.hitboxes.append([
                self.items[item].get_hitboxes(),
                [(old_pos[0], old_pos[1]), (new_pos[0], new_pos[1])]])
        self.update_clocks(1)
        # using the coordinates obtained in the previous for loop
        # replace these descriptions of geometric objects in shapely
        self.create_hitbox_geometry()
        self.update_clocks(2)
        self.check_collisions()
        self.update_clocks(3)
        for item in range(len(self.items)):
            # revise any positions that may have change b/c of collisions
            # want to display the item at point of impact b4 rebound/vanish
            # revise_position()... maybe takes in location?
            new_pos = self.items[item].revise_position()
            old_pos = self.canvas.coords(self.sprites[item])
            if new_pos == [-1, -1]:
                self.delete_list.append(item)
            else:
                self.canvas.move(
                    self.sprites[item],
                    new_pos[0]-old_pos[0],
                    new_pos[1]-old_pos[1])
        self.update_clocks(4)
        self.delete_things()
        self.update_clocks(5)
        self.collisions = []
        self.hitboxes = []
        self.update_clocks(6)
        self.iteration_number += 1
        self.my_lock.release()
        self.after(self.update_time, self.draw)

    def onKeyPress(self, event):
        """handles arrow key presses"""
        if event.char == ',' or event.char == '<':
            self.up_press = 1
        elif event.char == 'o' or event.char == 'O':
            self.down_press = 1
        elif event.char == 'a' or event.char == 'A':
            self.left_press = 1
        elif event.char == 'e' or event.char == 'E':
            self.right_press = 1
        else:
            self.misc_press(event)

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

    def onLeftClick(self, event):
        """handles left button mouse clicks"""
        origin = self.items[0].get_position()
        if len(self.items) < 3:
            if self.gun_mode == 0:
                self.items.append(
                    SuperMissile.SuperMissile(origin[0]+10, origin[1]+10,
                                              event.x, event.y, 800, 650,
                                              "player"))
                self.sprites.append(self.canvas.create_oval(origin[0]-5,
                                    origin[1]-5, origin[0]+5, origin[1]+5,
                                    fill='sky blue', outline='white'))
            elif self.gun_mode == 1:
                self.items.append(
                    ArrayMissile.ArrayMissile(origin[0]+10, origin[1]+10,
                                              event.x, event.y, 800, 650,
                                              "player"))
                self.sprites.append(self.canvas.create_oval(origin[0]-5,
                                    origin[1]-5, origin[0]+5, origin[1]+5,
                                    fill='red', outline='white'))
            elif self.gun_mode == 2:
                self.items.append(
                    HomingMissile.HomingMissile(origin[0]+10, origin[1]+10,
                                                event.x, event.y, 800, 650,
                                                "player"))
                self.sprites.append(self.canvas.create_oval(origin[0]-5,
                                    origin[1]-5, origin[0]+5, origin[1]+5,
                                    fill='green', outline='white'))
            elif self.gun_mode == 3:
                self.items.append(
                    DriftingParticle.DriftingParticle(random.randrange(50, 750),
                                                      random.randrange(50, 600),
                                                      0, 0, 800, 650, "enemy"))
                self.sprites.append(self.canvas.create_oval(0, 0, 30, 30,
                                                            fill='pink'))
        self.mouse_position = [event.x, event.y]

    def onMotion(self, event):
        """Keeps track of the mouse"""
        self.mouse_position = [event.x, event.y]

    def delete_things(self):
        """Deletes things that are no longer necessary"""
        if self.delete_list != []:
            for item in reversed(self.delete_list):
                self.canvas.delete(self.sprites[item])
                self.sprites.remove(self.sprites[item])
                self.items.remove(self.items[item])
                self.hitboxes.remove(self.hitboxes[item])
            self.delete_list = []

    def misc_press(self, event):
        """Handles miscellaneous key presses"""
        if event.char == '.':
            if self.gun_mode == 3:
                self.gun_mode = 0
            else:
                self.gun_mode += 1
        elif event.char == "'":
            if self.gun_mode == 0:
                self.gun_mode = 3
            else:
                self.gun_mode -= 1
        elif event.char == ' ':
            sys.exit()

    def initialize_key_variables(self):
        """creates variables for key presses and mouse position"""
        self.up_press = 0
        self.down_press = 0
        self.left_press = 0
        self.right_press = 0
        self.mouse_position = [0, 0]

    def initialize_item_variables(self):
        """creates variables for storing and manipulating items"""
        self.items = [0]  # stores created items
        self.sprites = [0]  # stores sprites relating to creative items
        self.update_time = 1  # draw handler delay
        # This is the starting particle and its related sprite
        self.items[0] = ControlledParticle.ControlledParticle(400, 325, 800,
                                                              650, "player")
        self.sprites[0] = self.canvas.create_oval(0, 0, 30, 30, fill='grey',
                                                  activefill='black')
        self.gun_mode = 0  # variable for switching between missile types
        self.delete_list = []  # variable for storing things-to-be-deleted
        self.hitboxes = []  # stores three hitboxes for each item.
        self.collisions = []
        # FOR PROFILING
        self.clock = time.time()
        # [0]: draw method total time
        # [1]: initial update_position calls
        # [2]: create_hitbox_geometry()
        # [3]: check_collisions()
        # [4]: revise_collision()
        # [5]: delete_things()
        # [6]: mystery
        self.clocks = [0, 0, 0, 0, 0, 0, 0]
        self.iteration_number = 1

    def initialize_key_bindings(self, parent):
        """binds events"""
        parent.bind('<KeyPress>', self.onKeyPress)
        parent.bind('<KeyRelease>', self.onKeyRelease)
        parent.bind('<Button-1>', self.onLeftClick)
        parent.bind('<Motion>', self.onMotion)

    def draw_environment(self):
        """draws the game environment"""
        self.canvas.create_line(0, 20, 800, 20, fill='white')  # horizontal line at 20y
        self.canvas.create_line(20, 0, 20, 650, fill='white')  # vertical line at 20x
        self.canvas.create_line(0, 640, 800, 640, fill='white')  # horizontal line at 630y
        self.canvas.create_line(790, 0, 790, 650, fill='white')  # vertical line at 780x
        self.canvas.create_line(400, 0, 400, 650, fill='white')  # vert midline
        self.canvas.create_line(0, 325, 800, 325, fill='white')

    def create_hitbox_geometry(self):
        """uses coordinate locations in self.hitboxes to implement shapely"""
        for item in range(len(self.hitboxes)):
            for number in range(2):
                if len(self.hitboxes[item][number]) == 2:
                    self.hitboxes[item][number] = LineString(self.hitboxes[item][number])
                elif len(self.hitboxes[item][number]) != 0:
                    self.hitboxes[item][number] = LinearRing(self.hitboxes[item][number])
                else:
                    pass

    def check_collisions(self):
        """checks whether or not a hitbox intersects another"""
        self.create_collision_list()
        self.check_collision_list()

    def create_collision_list(self):
        """creates a list with all the possible collisions"""
        for chris_brown in range(len(self.items)):
            for rihanna in range(len(self.items)):
                if self.items[chris_brown].get_hitbox_type() != self.items[rihanna].get_hitbox_type():
                    self.collisions.append((chris_brown, rihanna))
                    self.collisions.append((rihanna, chris_brown))

    def check_collision_list(self):
        """using self.collisions, calculates whether or not things collide"""
        for possible_collision in self.collisions:
            chris_brown = possible_collision[0]
            rihanna = possible_collision[1]
            for index1 in range(2):
                for index2 in range(2):
                    if self.hitboxes[chris_brown][index1] != [] and self.hitboxes[rihanna][index2] != []:
                        self.simulate_collision(chris_brown, rihanna, index1, index2)

    def simulate_collision(self, chris_brown, rihanna, index1, index2):
        """if things collide, calls on_collision method"""
        collision = self.hitboxes[chris_brown][index1].intersection(self.hitboxes[rihanna][index2])
        collision_location = self.get_collision_location(collision)
        if collision_location == 0:
            pass
        else:
            self.items[chris_brown].on_collision(self.items[rihanna].get_hitbox_type(),
                                                 collision_location)

    def get_collision_location(self, collision):
        """deciphers the location of the hitbox intersection"""
        if collision.wkt[:5] == 'POINT':
            return list(collision.coords)
        elif collision.wkt[:5] == 'MULTIPOINT':
            return [(collision.wkt[12], collision.wkt[14])]
        else:
            return 0

    def update_clocks(self, method_number):
        self.clocks[method_number] += (time.time()-self.clock)/self.iteration_number
        self.clock = time.time()

if __name__ == '__main__':
    window = Tk()
    quitter = quitbutton.quitButton(window)
    Canvas_Window = CanvasWindow(window)
    print('Woo!')
