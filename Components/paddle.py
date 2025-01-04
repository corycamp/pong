from Components.ball import Ball
from typing import Type
class Paddle:
    def __init__(self, x_pos, y_pos, frame_rate):
        self.paddle_width = 30
        self.paddle_height = 200
        self.x = x_pos
        self.y = y_pos - (self.paddle_height / 2)
        self.paddle_speed = 300
        self.color = "white"
        self.frame_rate = frame_rate
        
    def move_up(self):
        self.y -= self.paddle_speed * self.frame_rate
        
    def move_down(self):
        self.y += self.paddle_speed * self.frame_rate
        
    def get_x_pos(self):
        return self.x
    
    def get_y_pos(self):
        return self.y
    
    def get_color(self):
        return self.color

    def get_width(self):
        return self.paddle_width
    
    def get_height(self):
        return self.paddle_height
    