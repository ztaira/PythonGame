# Note: This is a standalone controlled particle class.
# It's just data, and was not meant to draw itself

# =======================================================================
import Object

class ControlledParticle(Object.Object):
    def __init__(self, x_origin, y_origin, canvas_size_x, canvas_size_y,
                 hitbox_type):
        # velocity and object variables
        self.acceleration = [0, 0]
        self.velocity = [0, 0]
        self.position = [x_origin, y_origin]
        self.bbox = [canvas_size_x-40, canvas_size_y-40]
        self.hitbox_type = hitbox_type
        self.has_collided = 0

    def update_position(self, up_press, down_press, left_press,
                        right_press, x_target, y_target):
        """updates position values according to kinematic equations"""
        # changes the acceleration based on which keys are pressed
        self.decide_acceleration(up_press, down_press, left_press, right_press)
        # update the velocity values using the acceleration values
        # Includes friction which subtracts 0.1% of velocity
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]
        self.velocity[0] *= 0.9
        self.velocity[1] *= 0.9
        # If it hits a wall, reverse the velocity so it bounces
        if self.position[0] < 20 and self.velocity[0] < 0:
            self.velocity[0] = -self.velocity[0]
        if self.position[0] > self.bbox[0] and self.velocity[0] > 0:
            self.velocity[0] = -self.velocity[0]
        if self.position[1] < 20 and self.velocity[1] < 0:
            self.velocity[1] = -self.velocity[1]
        if self.position[1] > self.bbox[1] and self.velocity[1] > 0:
            self.velocity[1] = -self.velocity[1]
        # update the position values using the velocity values
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        return self.position

    def decide_acceleration(self, up_press, down_press, left_press,
                            right_press):
        """Changes the acceleration based on which keys were pressed"""
        self.decide_y_acceleration(up_press, down_press)
        self.decide_x_acceleration(left_press, right_press)

    def decide_y_acceleration(self, up_press, down_press):
        """Changes the acceleration based on which keys were pressed"""
        # Up and down arrow keys, on the y axis. Handles acceleration
        if up_press == 1 and down_press == 1:
            self.acceleration[1] = 0
        elif up_press == 1:
            self.acceleration[1] = -1
        elif down_press == 1:
            self.acceleration[1] = 1
        else:
            self.acceleration[1] = 0

    def decide_x_acceleration(self, left_press, right_press):
        """Changes the acceleration based on which keys were pressed"""
        # left and right arrow keys, on the x axis. Handles acceleration.
        if left_press == 1 and right_press == 1:
            self.acceleration[0] = 0
        elif left_press == 1:
            self.acceleration[0] = -1
        elif right_press == 1:
            self.acceleration[0] = 1
        else:
            self.acceleration[0] = 0

    def get_hitboxes(self, x_position=-1, y_position=-1):
        """Returns an octagon with radius 15, centered on self.position
        Can also return octagon centered on given arguments"""
        if (x_position != -1) and (y_position != -1):
            a = x_position
            b = y_position
        else:
            a = self.position[0]
            b = self.position[1]
        x = 15
        y = 15
        x2 = x*((2)**0.5)/2
        y2 = y*((2)**0.5)/2
        return [(a, b+y), (a+x2, b+y2), (a+x, b), (a+x2, b-y2), (a, b-y),
                (a-x2, b-y2), (a-x, b), (a-x2, b+y2), (a, b+y)]

    def on_collision(self, hitbox_type, collision_location):
        """calculates what happens in the event of a collision"""
        # Can only hit 1 thing per frame
        if self.has_collided == 0:
            if hitbox_type == self.hitbox_type:
                pass
            else:
                # if it's an enemy bullet, give an impulse.
                # works like PK Thunder atm. Will implement actual impulse latr
                # collision_location is [(x, y)]
                dx = self.position[0] - collision_location[0][0]
                dy = self.position[1] - collision_location[0][1]
                self.velocity[0] += 100*dx/(dx**2+dy**2)
                self.velocity[1] += 100*dy/(dx**2+dy**2)
                self.has_collided = 1

    def revise_position(self):
        """revises the position of the object if it hits something"""
        self.has_collided = 0
        return self.position
