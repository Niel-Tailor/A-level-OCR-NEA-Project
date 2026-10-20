import pygame
from settings import *

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color           
        self.hover_color = hover_color  
        self.text = text             
        self.text_color = text_color 
        self.font = FONT            

    def handle_event(self, event):
        #Handle button click events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
            if self.rect.collidepoint(event.pos):  
                return True
        return False

    def draw(self, screen):
        #Draw the button
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        
        pygame.draw.rect(screen, current_color, self.rect)
        pygame.draw.rect(screen, colors["white"], self.rect, 2)
        
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

def draw_menu(screen):
    #Draw main menu background
    main_bg = pygame.image.load('IMG/MainMenu/MainMenu.png').convert()
    main_bg = pygame.transform.scale(main_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(main_bg, (0, 0))
  
    title = pygame.font.Font(None, 48).render("Project X", True, colors["white"])
    title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 200))
    screen.blit(title, title_rect)

def draw_level_selector(screen):
    #Draw level selection screen
    level_bg = pygame.image.load('IMG/MainMenu/MainMenu.png').convert()
    level_bg = pygame.transform.scale(level_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(level_bg, (0, 0))
  
    title = pygame.font.Font(None, 36).render("SELECT LEVEL", True, colors["white"])
    title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 50))
    screen.blit(title, title_rect)
    
    level_descriptions = [
        "Tutorial",
        "Getting Harder", 
        "The Canyon Crossing",
        "Vertical Challenge",
        "The Pendulum",
        "The Spiral",
        "The Maze",
        "The Final Battle"
    ]
    
    # Two rows: 1-4 and 5-8
    level_button_width = 140
    level_spacing = 30
    row_width = (level_button_width * 4) + (level_spacing * 3)
    row_start_x = (SCREEN_WIDTH - row_width) // 2
    
    # First row: Levels 1-4
    description_y1 = 200
    for i in range(4):
        color = colors["yellow"]
        text = FONT.render(f"Level {i+1}:", True, color)
        desc_text = pygame.font.Font(None, 18).render(level_descriptions[i], True, colors["white"])
        
        button_center_x = row_start_x + (level_button_width // 2) + (i * (level_button_width + level_spacing))
        
        text_rect = text.get_rect(center=(button_center_x, description_y1))
        screen.blit(text, text_rect)
        
        desc_rect = desc_text.get_rect(center=(button_center_x, description_y1 + 25))
        screen.blit(desc_text, desc_rect)
    
    # Second row: Levels 5-8
    description_y2 = 350
    for i in range(4):
        color = colors["red"] if i == 3 else colors["yellow"]  
        text = FONT.render(f"Level {i+5}:", True, color)
        desc_text = pygame.font.Font(None, 18).render(level_descriptions[i+4], True, colors["white"])
        
        button_center_x = row_start_x + (level_button_width // 2) + (i * (level_button_width + level_spacing))
        
        text_rect = text.get_rect(center=(button_center_x, description_y2))
        screen.blit(text, text_rect)
        
        desc_rect = desc_text.get_rect(center=(button_center_x, description_y2 + 25))
        screen.blit(desc_text, desc_rect)

def draw_controls_screen(screen):
    #Draw controls screen
    controls_bg = pygame.image.load('IMG/MainMenu/MainMenu.png').convert()
    controls_bg = pygame.transform.scale(controls_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(controls_bg, (0, 0))

    title = pygame.font.Font(None, 36).render("CONTROLS", True, colors["white"])
    title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
    screen.blit(title, title_rect)
    
    controls = [
        "Game:",                    
        "  A - Move Left",         
        "  D - Move Right",
        "  W - Jump", 
        "  K - Shoot",
        "  L - Dash",  
        "",                       
        "Menu:",                   
        "  ESC - Pause Game / Return to Menu"
    ]
    
    y_offset = 180
    for i in range(len(controls)):
        color = colors["yellow"] if controls[i].endswith(":") else colors["white"]
        if "NEW!" in controls[i]:
            color = (0, 255, 255)  
        text = FONT.render(controls[i], True, color)
        screen.blit(text, (SCREEN_WIDTH//2 - 150, y_offset + i*25))

def draw_pause_overlay(screen):
    #Draw pause screen overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)  
    overlay.fill(colors["black"])
    screen.blit(overlay, (0, 0))
    
    pause_text = pygame.font.Font(None, 48).render("PAUSED", True, colors["white"])
    pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, 150))
    screen.blit(pause_text, pause_rect)

def draw_game_over(screen, score):
    #Draw game over screen
    screen.fill(colors["black"])
    
    game_over_text = pygame.font.Font(None, 48).render("GAME OVER", True, colors["red"])
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, 150))
    screen.blit(game_over_text, game_over_rect)
    
    score_text = FONT.render(f"Final Score: {score}", True, colors["white"])
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 200))
    screen.blit(score_text, score_rect)
    
    shortcut_y = 500
    shortcuts = [
        "Keyboard Shortcuts:",      
        "1 - Restart Current Level",
        "R - Play Again (from Level 1)", 
        "ESC - Main Menu"          
    ]
    
    for i in range(len(shortcuts)):
        color = colors["yellow"] if i == 0 else colors["white"]
        text = pygame.font.Font(None, 20).render(shortcuts[i], True, color)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, shortcut_y + i*25))
        screen.blit(text, text_rect)

def draw_level_complete(screen, score, level):
    #Draw level complete screen
    screen.fill(colors["black"])
    
    complete_text = pygame.font.Font(None, 48).render("LEVEL COMPLETE!", True, colors["green"])
    complete_rect = complete_text.get_rect(center=(SCREEN_WIDTH//2, 150))
    screen.blit(complete_text, complete_rect)
    
    level_text = FONT.render(f"Level {level} Complete!", True, colors["yellow"])
    level_rect = level_text.get_rect(center=(SCREEN_WIDTH//2, 190))
    screen.blit(level_text, level_rect)
    
    score_text = FONT.render(f"Score: {score}", True, colors["white"])
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 220))
    screen.blit(score_text, score_rect)

def draw_game_complete(screen, final_score):
    #Draw game complete screen
    level_bg = pygame.image.load('IMG/MainMenu/MainMenu.png').convert()
    level_bg = pygame.transform.scale(level_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(level_bg, (0, 0))
    
    congrats_text = pygame.font.Font(None, 48).render("CONGRATULATIONS!", True, colors["green"])
    congrats_rect = congrats_text.get_rect(center=(SCREEN_WIDTH//2, 80))
    screen.blit(congrats_text, congrats_rect)
    
    complete_text = pygame.font.Font(None, 36).render("You have completed Project X!", True, colors["yellow"])
    complete_rect = complete_text.get_rect(center=(SCREEN_WIDTH//2, 120))
    screen.blit(complete_text, complete_rect)
    
    final_score_text = pygame.font.Font(None, 32).render(f"Final Score: {final_score}", True, colors["white"])
    final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH//2, 160))
    screen.blit(final_score_text, final_score_rect)
    
def draw_health_bar(screen, x, y, current_health, max_health, width=100, height=15):
    #Draw a health bar
    background_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, colors["red"], background_rect)
    pygame.draw.rect(screen, colors["white"], background_rect, 2)  
    
    if current_health > 0:
        health_percentage = current_health / max_health
        current_width = int(width * health_percentage)
        
        if health_percentage > 0.6:
            health_color = colors["green"]
        elif health_percentage > 0.3:
            health_color = colors["yellow"]
        else:
            health_color = (255, 165, 0)  
            
        current_rect = pygame.Rect(x, y, current_width, height)
        pygame.draw.rect(screen, health_color, current_rect)

def draw_hearts(screen, x, y, current_health, max_health, heart_size=20):
    #Draw hearts for health display
    heart_spacing = heart_size + 5
    
    for i in range(max_health):
        heart_x = x + (i * heart_spacing)
        heart_y = y
        
        if i < current_health:
            heart_color = colors["red"]
        else:
            heart_color = (100, 100, 100)  
        
        pygame.draw.circle(screen, heart_color, (heart_x + 6, heart_y + 6), 6)
        pygame.draw.circle(screen, heart_color, (heart_x + 14, heart_y + 6), 6)
        
        points = [
            (heart_x + 10, heart_y + 18),  
            (heart_x + 2, heart_y + 10),   
            (heart_x + 18, heart_y + 10)   
        ]
        pygame.draw.polygon(screen, heart_color, points)
        
        pygame.draw.circle(screen, colors["white"], (heart_x + 6, heart_y + 6), 6, 1)
        pygame.draw.circle(screen, colors["white"], (heart_x + 14, heart_y + 6), 6, 1)
        pygame.draw.polygon(screen, colors["white"], points, 1)

def draw_dash_indicator(screen, player):
    x = 15
    y = 85  # Position below hearts
    
    cooldown_percent = player.get_dash_cooldown_percent()
    
    # Simple text indicator
    font = pygame.font.Font(None, 20)
    if cooldown_percent >= 1.0:
        # Ready - show in bright cyan
        text = font.render("Dash: READY", True, (0, 255, 255))
    else:
        # On cooldown - show timer
        remaining = 1.0 - cooldown_percent
        text = font.render(f"Dash: {remaining:.1f}s", True, (150, 150, 150))
    
    screen.blit(text, (x, y))

def draw_hud(screen, player, score, level, health_style="hearts"):
    #Draw the heads-up display
    hud_surface = pygame.Surface((240, 160))
    hud_surface.set_alpha(150) 
    hud_surface.fill(colors["black"])
    screen.blit(hud_surface, (10, 10))  
    
    if health_style == "hearts":
        health_label = FONT.render("Health:", True, colors["white"])
        screen.blit(health_label, (15, 15))
        draw_hearts(screen, 15, 45, player.health, player.max_health)
        
        # Draw dash indicator
        draw_dash_indicator(screen, player)
        
        score_y = 110
        level_y = 135
        
    elif health_style == "bar":
        health_label = FONT.render("Health:", True, colors["white"])
        screen.blit(health_label, (15, 15))
        draw_health_bar(screen, 15, 45, player.health, player.max_health, width=120, height=15)
        
        # Draw simple dash indicator
        draw_dash_indicator(screen, player)
        
        score_y = 110
        level_y = 135

    else: 
        health_color = colors["green"] if player.health > 2 else colors["yellow"] if player.health > 1 else colors["red"]
        health_text = FONT.render(f"Health: {player.health}/{player.max_health}", True, health_color)
        screen.blit(health_text, (15, 15))
        
        # Draw simple dash indicator
        draw_dash_indicator(screen, player)
        
        score_y = 110
        level_y = 135
    
    score_text = FONT.render(f"Score: {score}", True, colors["white"])
    screen.blit(score_text, (15, score_y))
    
    level_color = colors["red"] if level == 8 else colors["white"] 
    level_text = FONT.render(f"Level: {level}", True, level_color)
    screen.blit(level_text, (15, level_y))

class Menu:
    def __init__(self):
        self.buttons = {}  
        self.create_buttons() 
    
    def create_buttons(self):
        #Create all menu buttons
        button_width = 200
        button_height = 50
        button_spacing = 70  
        start_y = 280       
        center_x = SCREEN_WIDTH // 2 - button_width // 2  
        
        # Main menu buttons 
        self.buttons['main_menu'] = [
            Button("PLAY GAME", center_x, start_y, button_width, button_height, 
                  colors["darkblue"], colors["blue"]),
            Button("LEVEL SELECT", center_x, start_y + button_spacing, button_width, button_height, 
                  colors["darkblue"], colors["green"]),
            Button("CONTROLS", center_x, start_y + button_spacing * 2, button_width, button_height, 
                  colors["darkblue"], colors["blue"]),
            Button("QUIT", center_x, start_y + button_spacing * 3, button_width, button_height, 
                  colors["darkblue"], colors["red"])
        ]
        
        # Level selector buttons
        level_button_width = 140
        level_button_height = 50
        level_spacing = 30  
        
        # Two rows: 1-4, 5-8
        row_width = (level_button_width * 4) + (level_spacing * 3)
        row_start_x = (SCREEN_WIDTH - row_width) // 2
        
        # Row Y positions
        first_row_y = 240
        second_row_y = 390
        
        self.buttons['level_select'] = [
            # First row: Levels 1-4
            Button("LEVEL 1", row_start_x, first_row_y, level_button_width, level_button_height, 
                  colors["darkblue"], colors["green"]),
            Button("LEVEL 2", row_start_x + (level_button_width + level_spacing), first_row_y, level_button_width, level_button_height, 
                  colors["darkblue"], colors["green"]),
            Button("LEVEL 3", row_start_x + (level_button_width + level_spacing) * 2, first_row_y, level_button_width, level_button_height, 
                  colors["darkblue"], colors["green"]),
            Button("LEVEL 4", row_start_x + (level_button_width + level_spacing) * 3, first_row_y, level_button_width, level_button_height, 
                  colors["darkblue"], colors["green"]),
            
            # Second row: Levels 5-8
            Button("LEVEL 5", row_start_x, second_row_y, level_button_width, level_button_height, 
                  colors["darkblue"], colors["green"]),
            Button("LEVEL 6", row_start_x + (level_button_width + level_spacing), second_row_y, level_button_width, level_button_height, 
                  colors["darkblue"], colors["green"]),
            Button("LEVEL 7", row_start_x + (level_button_width + level_spacing) * 2, second_row_y, level_button_width, level_button_height, 
                  colors["darkblue"], colors["green"]),
            Button("LEVEL 8", row_start_x + (level_button_width + level_spacing) * 3, second_row_y, level_button_width, level_button_height, 
                  colors["darkblue"], colors["red"]), 
            
            # Back button
            Button("BACK", center_x, second_row_y + 80, button_width, button_height, 
                  colors["darkblue"], colors["yellow"])
        ]
        
        # Pause menu buttons 
        self.buttons['pause_menu'] = [
            Button("RESUME", center_x, start_y, button_width, button_height, 
                  colors["darkblue"], colors["green"]),
            Button("CONTROLS", center_x, start_y + button_spacing, button_width, button_height, 
                  colors["darkblue"], colors["blue"]),
            Button("MAIN MENU", center_x, start_y + button_spacing * 2, button_width, button_height, 
                  colors["darkblue"], colors["yellow"])
        ]
        
        # Control screen buttons 
        self.buttons['controls'] = [
            Button("BACK", center_x, 450, button_width, button_height, 
                  colors["darkblue"], colors["green"])
        ]
        
        # Game over buttons
        self.buttons['game_over'] = [
            Button("RESTART LEVEL", center_x, start_y, button_width, button_height, 
                  colors["darkblue"], colors["blue"]),
            Button("PLAY AGAIN", center_x, start_y + button_spacing, button_width, button_height, 
                  colors["darkblue"], colors["green"]),
            Button("MAIN MENU", center_x, start_y + button_spacing * 2, button_width, button_height, 
                  colors["darkblue"], colors["yellow"])
        ]
        
        # Level complete buttons
        self.buttons['level_complete'] = [
            Button("NEXT LEVEL", center_x, start_y + 50, button_width, button_height, 
                  colors["darkblue"], colors["green"]),
            Button("MAIN MENU", center_x, start_y + button_spacing + 50, button_width, button_height, 
                  colors["darkblue"], colors["yellow"])
        ]
        
        # Game complete buttons
        self.buttons['game_complete'] = [
            Button("PLAY AGAIN", center_x, 450, button_width, button_height, 
                  colors["darkblue"], colors["green"]),
            Button("MAIN MENU", center_x, 450 + button_spacing, button_width, button_height, 
                  colors["darkblue"], colors["yellow"]),
            Button("QUIT GAME", center_x, 450 + button_spacing * 2, button_width, button_height, 
                  colors["darkblue"], colors["red"])
        ]
    
    def handle_events(self, event, menu_type):
        #Handle button events for a menu
        buttons = self.buttons.get(menu_type, [])  
        for i in range(len(buttons)):
            if buttons[i].handle_event(event):  
                return i  
        return None 
    
    def draw_buttons(self, screen, menu_type):
        #Draw all buttons for a menu
        buttons = self.buttons.get(menu_type, [])
        for button in buttons:
            button.draw(screen)