import pygame
from .paddle import Paddle
from .ball import Ball
from .text import game_text
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('PONG')
        pygame.font.init()
        
        # Setup Variables
        self.screen = pygame.display.set_mode((1250, 720))
        self.font_size = 80
        self.text_color = 'white'
        self.main_color = 'black'
        self.my_font = pygame.font.SysFont('Arial', self.font_size, True)
        self.clock = pygame.time.Clock()
        self.running = True
        self.frame_rate = self.clock.tick(60) / 1000
        self.mouse_pos = ''
        self.start = False
        
        # Game config
        self.border = 20
        self.player_one_score = 0
        self.player_two_score = 0
        self.last_collided = 0
        self.control_scheme = 0
        self.passes = 0
        self.page = 'menu'
        self.last_page = self.page
        
        self.initialize_game(True)
        self.run()
        
    def initialize_game(self, initial=False):
        #Initialize players
        if initial:
            self.paddle_one = Paddle(100, self.screen.get_height()/2, self.frame_rate)
            self.paddle_two = Paddle(self.screen.get_width() - 30 - 100, self.screen.get_height()/2, self.frame_rate)
        
        #Initialize ball
        self.ball = Ball(self.screen.get_width()/2, self.screen.get_height()/2, self.text_color) 
        self.last_collided = 0
        self.passes = 0
        
    def screen_refresh(self, mouse):
        self.screen.fill(self.main_color) 
        self.screen.blit(self.my_font.render(f'{self.player_one_score}', True, self.text_color),(self.screen.get_width()/2 - 200, 30))
        self.screen.blit(self.my_font.render(f'{self.player_two_score}', True, self.text_color) ,(self.screen.get_width()/2 + 193, 30))
        
        pause_button = pygame.draw.rect(self.screen,self.main_color,pygame.Rect(self.screen.get_width() / 2 - 7, 50, 50,50), width=1)
        pygame.draw.rect(self.screen,self.text_color,pygame.Rect(self.screen.get_width() / 2 - 6, 50, 15,50), width=0)
        pygame.draw.rect(self.screen,self.text_color,pygame.Rect(self.screen.get_width() / 2 + 27, 50, 15,50), width=0)
        
        # Border
        pygame.draw.rect(self.screen,self.text_color,pygame.Rect(0,0,self.screen.get_width(),self.screen.get_height()), width=8)
        top_border = pygame.draw.rect(self.screen,self.main_color,pygame.Rect(0,0,self.screen.get_width(),self.border), width=0)
        bottom_border = pygame.draw.rect(self.screen,self.main_color,pygame.Rect(0,self.screen.get_height()-self.border,self.screen.get_width(),20), width=0)
        
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
        
        if top_border.colliderect(ball):
            print(self.last_collided)
            if self.last_collided != 3:
                self.last_collided = 3
        
        if bottom_border.colliderect(ball):
            if self.last_collided != 4:
                self.last_collided = 4      
            
        self.handle_collision(collided)
        
        if mouse != '':
            if pause_button.collidepoint(mouse[0],mouse[1]):
                self.pause_game()
        
    def pause_game(self):
        self.last_page = self.page
        self.page = 'pause'
        self.start = False
        
    def handle_player_movement(self):
        keys = pygame.key.get_pressed()
        if self.control_scheme == 0 and keys[pygame.K_w] or self.control_scheme == 1 and keys[pygame.K_UP]:
            if self.paddle_one.get_y_pos() - self.border > 0:
                self.paddle_one.move_up()
        if self.control_scheme == 0 and keys[pygame.K_s] or self.control_scheme == 1 and keys[pygame.K_DOWN]:
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
        #Validates if the ball collided with a paddle and should be bounced back
        if collided:
            self.get_collision_angle()
            self.passes += 1
            self.ball.bounce_ball(0)
            self.ball.bounce_ball(1)
        
        #Triggers bonus mode after consecutive passes
        if (self.passes / 10) % 2 == 1 and self.passes != 0:
            self.update_colors('black','white')
        elif (self.passes / 10) % 2 == 0 :
            self.update_colors('white', 'black')
                
        #Checks if the ball touches top and bottom border
        if self.last_collided == 3 or self.last_collided == 4:
            self.ball.bounce_ball(1)
            self.last_collided = 0

    
    def get_collision_angle(self):
        paddle = ''
        if self.last_collided == 1:
            paddle = self.paddle_one
        elif self.last_collided == 2:
            paddle = self.paddle_two
        #Top
        if self.ball.get_y_pos() <= paddle.get_y_pos() + 115 and  self.ball.get_y_pos() >= paddle.get_y_pos() + 85:
            self.ball.set_angle(0)
        elif self.ball.get_y_pos() < paddle.get_y_pos() + 85 and self.ball.get_y_pos() >= paddle.get_y_pos() + 50:
            self.ball.set_angle(-1.5)
        elif self.ball.get_y_pos() < paddle.get_y_pos() + 50:
            self.ball.set_angle(-2.5)
            
        #Bottom
        if self.ball.get_y_pos() > paddle.get_y_pos() + 115 and self.ball.get_y_pos() <= paddle.get_y_pos() + 150:
            self.ball.set_angle(1.5)
        elif self.ball.get_y_pos() >= paddle.get_y_pos() + 150:
            self.ball.set_angle(2.5)
                
        
    def reset_game(self):
        self.initialize_game()
    
    def update_colors(self, primary, secondary):
        #Update the colors of the components
        self.text_color = primary
        self.main_color = secondary
        self.paddle_one.set_color(primary)
        self.paddle_two.set_color(primary)
        self.ball.set_color(primary)
            
    def handle_match_round(self):
        #Checks if the ball went pass a paddle to give a point
        if self.ball.get_x_pos() - self.ball.get_width()/2 > self.screen.get_width():
            self.player_one_score += 1
            self.reset_game()
        if self.ball.get_x_pos() + self.ball.get_width()/2 < 0:
            self.player_two_score += 1
            self.reset_game()

    def run_game(self, mouse):
        self.screen_refresh(mouse)
        self.handle_player_movement()
        self.handle_ball_movement()
        self.handle_match_round()
        self.cpu_movement()
        
    def main_menu(self, mouse):
        if self.page == 'menu' or self.page == 'pause':
            self.screen.fill(self.main_color)
            spacing = 100
            start_button_text = 'Start'
            #Changes start to resume button for paused game
            if self.page == 'pause':
                start_button_text = 'Resume'
                
            # Start Menu
            start = self.screen.blit(self.my_font.render(start_button_text, True, self.text_color),(self.screen.get_width()/2 - self.font_size / 2, self.screen.get_height()/2 - spacing - self.font_size / 2))
            options = self.screen.blit(self.my_font.render('Options', True, self.text_color) ,(self.screen.get_width()/2 - self.font_size / 2,  self.screen.get_height()/2 - self.font_size / 2))
            quit = self.screen.blit(self.my_font.render('Quit', True, self.text_color) ,(self.screen.get_width()/2 - self.font_size / 2, self.screen.get_height()/2 + spacing - self.font_size / 2))
            
            #Controls menu item selection
            if mouse != '':
                if start.collidepoint(mouse[0],mouse[1]):
                    self.start = True
                if options.collidepoint(mouse[0], mouse[1]):
                    self.last_page = self.page
                    self.page = 'options'
                if quit.collidepoint(mouse[0], mouse[1]):
                    self.running = False
        elif self.page == 'options':
            self.options_screen(mouse)
                
    def options_screen(self, mouse):
        self.screen.fill(self.main_color)
        textObj = game_text['options_page']
        options_font = pygame.font.SysFont('Arial', 40, True)
        
        #Options page text and back button
        back = self.screen.blit(options_font.render('Back', True, self.text_color) ,(15, self.screen.get_height() - 50))
        self.screen.blit(self.my_font.render('Options', True, self.text_color) ,(self.screen.get_width()/2 - 150, 10))
        self.screen.blit(options_font.render(f'{textObj['intro']}', True, self.text_color), (self.screen.get_width() / 2 - 500, 150))
        
        #First control scheme option
        option_one = pygame.draw.rect(self.screen,self.text_color,pygame.Rect(self.screen.get_width() / 2 - 200, self.screen.get_height() / 2 - 100, 50, 50), width=0 if self.control_scheme == 0 else 1)
        self.screen.blit(options_font.render(f'{textObj['control_scheme_one_up']}', True, self.text_color),(self.screen.get_width()/2 - 100, self.screen.get_height()/2 - 125))
        self.screen.blit(options_font.render(f'{textObj['control_scheme_one_down']}', True, self.text_color),(self.screen.get_width()/2 - 100, self.screen.get_height()/2 - 80))
        
        #Second control scheme option
        option_two = pygame.draw.rect(self.screen,self.text_color,pygame.Rect(self.screen.get_width() / 2 - 200, self.screen.get_height() / 2 + 10, 50, 50), width=1 if self.control_scheme == 0 else 0)
        self.screen.blit(options_font.render(f'{textObj['control_scheme_two_up']}', True, self.text_color),(self.screen.get_width()/2 - 100, self.screen.get_height()/2 - 5))
        self.screen.blit(options_font.render(f'{textObj['control_scheme_two_down']}', True, self.text_color),(self.screen.get_width()/2 - 100, self.screen.get_height()/2 + 40))
        
        #Mouse controls for control selection and navigating back to the menu
        if mouse != '':
            if back.collidepoint(mouse[0],mouse[1]):
                if self.last_page == 'menu':
                    self.last_page = self.page
                    self.page = 'menu'
                elif self.last_page == 'pause':
                    self.last_page = self.page
                    self.page = 'pause'
            if option_one.collidepoint(mouse[0], mouse[1]):
                self.control_scheme = 0
            if option_two.collidepoint(mouse[0], mouse[1]):
                self.control_scheme = 1
                
    def run(self):
        while self.running:
            mouse = ''
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    self.running = False
            if self.start:
                self.run_game(mouse)
            else :
                self.main_menu(mouse)
            pygame.display.flip()
            self.clock.tick(60) / 1000  
        pygame.quit()
            