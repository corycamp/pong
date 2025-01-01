import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption('PONG')
    pygame.font.init()
    my_font = pygame.font.SysFont('Arial', 80, True)
    clock = pygame.time.Clock()
    running = True
    
    # Game config
    border = 25
    player_one_score = 0
    player_two_score = 0
    passes = 0
    
    # Paddle config
    paddle_height = 200
    paddle_width = 30
    paddle_speed = 300
    paddle_color = "white"
    
    # Ball config
    ball_color = "white"  
    ball_width = 30
    ball_vel = -10
    
    # Initial positions
    player_x_pos = 100
    player_y_pos = screen.get_height() / 2
    cpu_x_pos =screen.get_width() - border - paddle_width
    cpu_y_pos = screen.get_height() / 2
    ball_x_pos = screen.get_width() / 2
    ball_y_pos = screen.get_height() / 2
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill("black") 
        player_one_score_display = my_font.render(f'{player_one_score}', True, "white")
        player_two_score_display = my_font.render(f'{player_two_score}', True, "white") 
        screen.blit(player_one_score_display,(screen.get_width()/2 - 200, 50))
        screen.blit(player_two_score_display,(screen.get_width()/2 + 200, 50))

        # border
        pygame.draw.rect(screen,"white",pygame.Rect(0,0,screen.get_width(),screen.get_height()), width=8)
        
        # Paddle one
        pygame.draw.rect(screen,paddle_color,pygame.Rect(player_x_pos, player_y_pos, paddle_width, paddle_height), width=0, border_radius=20)
        
        # Paddle two
        pygame.draw.rect(screen,paddle_color,pygame.Rect(cpu_x_pos, cpu_y_pos, paddle_width, paddle_height), width=0, border_radius=20)
        
        # ball
        pygame.draw.circle(screen,ball_color,(ball_x_pos,ball_y_pos), ball_width)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if player_y_pos - border > 0:
                player_y_pos -= paddle_speed * dt
        if keys[pygame.K_s]:
            if player_y_pos + paddle_height + border < screen.get_height():
                player_y_pos += paddle_speed * dt  
                
        ball_x_pos += ball_vel
        
        # # Hamdle collision with paddle
        # if ball_x_pos < player_x_pos + ball_width + paddle_width and ball_x_pos > player_x_pos - ball_width:
        if ball_x_pos > player_x_pos:
            if ball_y_pos + ball_width >= player_y_pos and ball_y_pos - ball_width <= player_y_pos + paddle_height:
                ball_vel *= -1
                passes += 1
        
        if ball_x_pos >= cpu_x_pos - ball_width:
            if ball_y_pos + ball_width >= cpu_y_pos and ball_y_pos - ball_width <= cpu_y_pos + paddle_height:
                ball_vel *= -1
                passes += 1
                
        # Speed up
        # if passes == 10:
        #     ball_vel *= 2
        #     passes += 1

        # Round Win
        if ball_x_pos > screen.get_width() - border:
            player_one_score += 1
            ball_vel = -10
            ball_x_pos = screen.get_width() / 2
            ball_y_pos = screen.get_height() / 2
        elif ball_x_pos < border:
            player_two_score += 1
            ball_vel = -10
            ball_x_pos = screen.get_width() / 2
            ball_y_pos = screen.get_height() / 2
                
        pygame.display.flip()
        dt = clock.tick(60) / 1000
    
    pygame.quit()
    
if __name__ == '__main__':
    main()