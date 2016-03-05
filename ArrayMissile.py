# This class is meant to be a missile which deploys before targeting

# =======================================================================
import math
import random
import Object


class ArrayMissile(Object.Object):
    """This class represents a missile which deploys before targeting"""
    def __init__(self, x_origin, y_origin, x_target, y_target,
                 canvas_size_x, canvas_size_y, hitbox_type):
        # For final targeting
        self.acceleration = 3
        self.velocity = [0, 0]
        self.position = [x_origin, y_origin]
        self.ratio = 0
        self.target = [x_target, y_target]
        # Bounding box size
        self.bbox = [canvas_size_x-20, canvas_size_y-20]
        # Angle and duration of launch
        self.deploy_time = random.randrange(25, 50)
        self.random_angle = random.randrange(360)
        self.counter = 0
        self.to_delete = 0
        self.hitbox_type = hitbox_type
        self.has_collided = 0

    def update_position(self, up_press, down_press, left_press, right_press,
                        x_target, y_target):
        if self.to_delete == 2:
            return self.position
        if self.counter < self.deploy_time:
            self.counter += 1
            self.position[0] += math.cos(self.random_angle)*2
            self.position[1] += math.sin(self.random_angle)*2
            self.stay_bounded()
            return self.position
        elif self.counter == self.deploy_time:
            self.ratio = [self.target[0]-self.position[0],
                          self.target[1]-self.position[1]]
            self.ratio[0] /= ((self.target[0]-self.position[0])**2 +
                              (self.target[1]-self.position[1])**2)**0.5
            self.ratio[1] /= ((self.target[0]-self.position[0])**2 +
                              (self.target[1]-self.position[1])**2)**0.5
            self.counter += 1
            return self.position
        elif self.counter > self.deploy_time:
            self.velocity[0] += self.ratio[0]*self.acceleration
            self.velocity[1] += self.ratio[1]*self.acceleration
            self.position[0] += self.velocity[0]
            self.position[1] += self.velocity[1]
            # Calls parent bounding method
            self.is_bounded()
            return self.position

    def stay_bounded(self):
        """Makes sure the position returned is within the bounding box"""
        if self.position[0] < 20:
            self.position[0] = 20
            self.velocity[0] = 0
        elif self.position[0] > self.bbox[0]:
            self.position[0] = self.bbox[0]
            self.velocity[0] = 0
        if self.position[1] < 20:
            self.position[1] = 20
            self.velocity[1] = 0
        elif self.position[1] > self.bbox[1]:
            self.position[1] = self.bbox[1]
            self.velocity[1] = 0

    def get_hitboxes(self, x_position=-1, y_position=-1):
        """Returns 0. To save time, projectiles are simulated as lines."""
        return []

    def on_collision(self, hitbox_type, collision_location):
        """calculates what happens in the event of a collision"""
        # hitbox_type is string, collision_location is [(x, y)]
        # this ArrayMissile can only hit one thing per frame
        if self.has_collided == 0:
            if hitbox_type == self.hitbox_type:
                pass
            elif hitbox_type != self.hitbox_type:
                self.position = [collision_location[0][0],
                                 collision_location[0][1]]
                self.to_delete = 1
                self.has_collided = 1
        elif self.has_collided == 1:
            pass

    def revise_position(self):
        """revises the position of the object if it hits something"""
        if self.to_delete == 0:
            return self.position
        elif self.to_delete == 1:
            self.to_delete += 1
            return self.position
        elif self.to_delete == 2:
            return [-1, -1]
