# This is a particle that drifts aimlessly through space
# It's meant to be a target

# ========================================================================
import Object
import random


class DriftingParticle(Object.Object):
    def __init__(self, x_origin, y_origin, x_target, y_target,
                 canvas_size_x, canvas_size_y, hitbox_type):
        self.acceleration = [0, 0]
        self.velocity = [random.randrange(5), random.randrange(5)]
        self.position = [x_origin, y_origin]
        self.bbox = [canvas_size_x-40, canvas_size_y-40]
        self.hitbox_type = hitbox_type
        self.has_collided = 0
        self.to_delete = 0

    def update_position(self, up_press, down_press, left_press,
                        right_press, x_target, y_target):
        """drifts w/ random speed and constant velocity. rebounds off walls"""
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
                self.has_collided = 1

    def revise_position(self):
        """revises the position of the object if it hits something"""
        if self.has_collided == 0:
            return self.position
        elif self.has_collided == 1:
            return [-1, -1]
