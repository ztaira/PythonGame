# This class is meant to represent the overall Object Class

#  =========================================================


class Object():
    """This class represents the most basic object class"""
    def __init__(self, x_origin, y_origin, canvas_size_x, canvas_size_y,
                 hitbox_type):
        self.position = [x_origin, y_origin]
        self.velocity = [0, 0]
        self.bbox = [canvas_size_x-20, canvas_size_y-20]
        self.to_delete = 0
        self.hitbox_type = hitbox_type
        self.has_collided = 0

    def update_position(self):
        """Update position of the object and return it"""
        return self.position

    def get_hitboxes(self, points):
        """Creates the hitboxes for each class"""
        return [(self.position[0], self.position[1])]

    def is_bounded(self):
        """if it's out of the bbox, display it impacting and then delete it"""
        # Note: can use math to more accurately display impact.
        # Needs previous position though
        if self.position[0] < 20:
            self.position[0] = 20
            self.velocity = [0, 0]
            self.to_delete = 1
        elif self.position[0] > self.bbox[0]:
            self.position[0] = self.bbox[0]
            self.velocity = [0, 0]
            self.to_delete = 1
        if self.position[1] < 20:
            self.position[1] = 20
            self.velocity = [0, 0]
            self.to_delete = 1
        elif self.position[1] > self.bbox[1]:
            self.position[1] = self.bbox[1]
            self.velocity = [0, 0]
            self.to_delete = 1

    def get_position(self):
        """returns the position of this Object"""
        return self.position

    def get_velocity(self):
        """returns the velocity of this object"""
        return self.velocity

    def on_collision(self):
        """does something that happens on collision"""
        pass

    def revise_position(self):
        """if a collision happened, return the adjusted location"""
        return self.position

    def get_hitbox_type(self):
        """returns the hitbox type"""
        return self.hitbox_type
