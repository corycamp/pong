import pygame
from .paddle import Paddle
from .ball import Ball

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('PONG')
        pygame.font.init()
        
        # Setup Variables
        self.screen = pygame.display.set_mode((1250, 720))
        self.my_font = pygame.font.SysFont('Arial', 80, True)
        self.clock = pygame.time.Clock()
        self.running = True
        self.frame_rate = self.clock.tick(60) / 1000
        
        # Game config
        self.border = 20
        self.player_one_score = 0
        self.player_two_score = 0
        self.last_collided = 0

        self.initialize_game(True)
        self.run()
        
    def initialize_game(self, initial=False):
         # Initialize players
        if initial:
            self.paddle_one = Paddle(100, self.screen.get_height()/2, self.frame_rate)
            self.paddle_two = Paddle(self.screen.get_width() - 30 - 100, self.screen.get_height()/2, self.frame_rate)
        
        #Initialize ball
        self.ball = Ball(self.screen.get_width()/2, self.screen.get_height()/2) 
        self.last_collided = 0
        
    def screen_refresh(self):
        self.screen.fill("black") 
        self.screen.blit(self.my_font.render(f'{self.player_one_score}', True, "white"),(self.screen.get_width()/2 - 200, 50))
        self.screen.blit(self.my_font.render(f'{self.player_two_score}', True, "white") ,(self.screen.get_width()/2 + 200, 50))
        
        # Border
        pygame.draw.rect(self.screen,"white",pygame.Rect(0,0,self.screen.get_width(),self.screen.get_height()), width=8)
        
        #Paddles
        paddle_one = pygame.draw.rect(self.screen,self.paddle_one.get_color(),pygame.Rect(self.paddle_one.get_x_pos(), self.paddle_one.get_y_pos(), self.paddle_one.get_width(), self.paddle_one.get_height()), width=0)
        paddle_two = pygame.draw.rect(self.screen,self.paddle_two.get_color(),pygame.Rect(self.paddle_two.get_x_pos(), self.paddle_two.get_y_pos(), self.paddle_two.get_width(), self.paddle_two.get_height()), width=0)
        
        #Ball
        ball = pygame.draw.circle(self.screen,self.ball.get_color(),(self.ball.get_x_pos(),self.ball.get_y_pos()), self.ball.get_width())

        collided = False
        if paddle_one.colliderect(ball):
            if self.last_collided != 1:
                collided = True
                self.last_collided = 1
            
        if paddle_two.colliderect(ball):
            if self.last_collided != 2:
                collided = True
                self.last_collided = 2

        self.handle_collision(collided)
        
    def handle_player_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if self.paddle_one.get_y_pos() - self.border > 0:
                self.paddle_one.move_up()
        if keys[pygame.K_s]:
            if self.paddle_one.get_y_pos() + self.paddle_one.get_height() + self.border < self.screen.get_height():
                self.paddle_one.move_down()  
                
    def cpu_movement(self): 
        if self.ball.horizontal_vel > 0:
            if self.ball.get_vertical_movement() < 0:
                if self.paddle_two.get_y_pos() - self.border > 0:
                    self.paddle_two.move_up()
            if self.ball.get_vertical_movement() > 0:
                if self.paddle_two.get_y_pos() + self.paddle_two.get_height() + self.border < self.screen.get_height():
                    self.paddle_two.move_down()  
    
    def handle_ball_movement(self):
        self.ball.move_ball(0)
        self.ball.move_ball(1)
                
    def handle_collision(self,collided):
        if collided:
            # print(f'Ball-Pos\nx:{self.ball.get_x_pos()}, y:{self.ball.get_y_pos()}')
            # print(f'Paddle-Pos\nx:{self.paddle_one.get_x_pos()}, y:{self.paddle_one.get_y_pos()}')
            self.ball.bounce_ball(0)
            self.ball.bounce_ball(1)
                
        # Touches top and bottom borders
        if self.ball.get_y_pos() - self.ball.get_width()/2 - 5 <=  self.border:
            self.ball.bounce_ball(1)
        if self.ball.get_y_pos() + self.ball.get_width()/2 + 5 >= self.screen.get_height():
            self.ball.bounce_ball(1)
            
    def reset_game(self):
        self.initialize_game()
    
    def handle_match_round(self):
        if self.ball.get_x_pos() - self.ball.get_width()/2 > self.screen.get_width():
            self.player_one_score += 1
            self.reset_game()
        if self.ball.get_x_pos() + self.ball.get_width()/2 < 0:
            self.player_two_score += 1
            self.reset_game()
        
        
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen_refresh()
            self.handle_player_movement()
            self.handle_ball_movement()
            self.handle_match_round()
            self.cpu_movement()
            pygame.display.flip()
            self.clock.tick(60) / 1000
        pygame.quit()
            