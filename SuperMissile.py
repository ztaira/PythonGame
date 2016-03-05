# This class is meant to be a missile which accelerates in a straight line.

# =======================================================================
import Object


class SuperMissile(Object.Object):
    """This is a class that represents a missile which accelerates in a
       straight line"""
    def __init__(self, x_origin, y_origin, x_target, y_target, canvas_size_x,
                 canvas_size_y, hitbox_type):
        # Variables for kinematic equation along a line
        self.acceleration = 1.5
        self.velocity = [0, 0]
        self.position = [x_origin, y_origin]
        self.ratio = [x_target-x_origin, y_target-y_origin]
        self.ratio[0] /= ((x_target-x_origin)**2+(y_target-y_origin)**2)**0.5
        self.ratio[1] /= ((x_target-x_origin)**2+(y_target-y_origin)**2)**0.5
        # Variable to describe the bounding box of said missiles
        self.bbox = [canvas_size_x-20, canvas_size_y-20]
        self.to_delete = 0
        self.hitbox_type = hitbox_type
        self.has_collided = 0

    def update_position(self, up_press, down_press, left_press, right_press,
                        x_target, y_target):
        """Updates position with a kinematic equation"""
        if self.to_delete == 2:
            return self.position
        # Note: Never goes beyond the bounding box. Returns new position
        self.velocity[0] += self.ratio[0]*self.acceleration
        self.velocity[1] += self.ratio[1]*self.acceleration
        # Calls parent bounding method
        self.is_bounded()
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        # Calls parent bounding method
        self.is_bounded()
        return self.position

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
            else:
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
