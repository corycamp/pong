import random

class Ball:
    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos
        self.width = 20
        self.vertical_vel = 10 * random.choice([-1,1])
        self.horizontal_vel = 10  * random.choice([-1,1])
        self.color = "white"
        
    def get_color(self):
        return self.color
    
    def get_x_pos(self):
        return self.x
    
    def get_y_pos(self):
        return self.y
    
    def get_width(self):
        return self.width
    
    def bounce_ball(self, orientation=0):
        if orientation == 0:
            self.horizontal_vel *= -1
        elif orientation == 1:
            self.vertical_vel *= -1
        
    def move_ball(self, orientation=0):
        if orientation == 0:
            self.x += self.horizontal_vel
        elif orientation == 1:
            self.y += self.vertical_vel