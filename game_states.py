import pygame

class GameStateHandler:
    def __init__(self, game):
        self.game = game
        self.previous_state = None  # Track where we came from when entering controls
    
    def handle_menu_events(self, event):
        #Handle menu button events and return False if should quit
        state = self.game.state
        menu_manager = self.game.menu_manager
        
        if state == "MENU":
            button_clicked = menu_manager.handle_events(event, 'main_menu')
            if button_clicked == 0:  # Play game
                self.game.state = "PLAYING"
                self.game.current_level = 1
                self.game.score = 0
                self.game.reset_level(preserve_health=False)
            elif button_clicked == 1:  # Level select
                self.game.state = "LEVEL_SELECT"
            elif button_clicked == 2:  # Controls
                self.previous_state = "MENU"  
                self.game.state = "CONTROLS"
            elif button_clicked == 3:  # Quit
                return False
        
        elif state == "LEVEL_SELECT":
            button_clicked = menu_manager.handle_events(event, 'level_select')
            if button_clicked is not None and button_clicked <= 7:
                self.game.current_level = button_clicked + 1
                self.game.score = 0
                self.game.state = "PLAYING"
                self.game.reset_level(preserve_health=False)
            elif button_clicked == 8:  
                self.game.state = "MENU"
        
        elif state == "CONTROLS":
            button_clicked = menu_manager.handle_events(event, 'controls')
            if button_clicked == 0:  # Back
                # Return to wherever we came from
                if self.previous_state == "PAUSED":
                    self.game.state = "PAUSED"
                else:
                    self.game.state = "MENU"
                self.previous_state = None  # Reset
        
        elif state == "PAUSED":
            button_clicked = menu_manager.handle_events(event, 'pause_menu')
            if button_clicked == 0:  # Resume
                self.game.state = "PLAYING"
            elif button_clicked == 1:  # Controls
                self.previous_state = "PAUSED"  
                self.game.state = "CONTROLS"
            elif button_clicked == 2:  # Main menu
                self.game.state = "MENU"
        
        elif state == "GAME_OVER":
            button_clicked = menu_manager.handle_events(event, 'game_over')
            if button_clicked == 0:  # Restart level
                self.game.state = "PLAYING"
                self.game.reset_level(preserve_health=False)
            elif button_clicked == 1:  # Play again
                self.game.current_level = 1
                self.game.score = 0
                self.game.state = "PLAYING"
                self.game.reset_level(preserve_health=False)
            elif button_clicked == 2:  # Main menu
                self.game.state = "MENU"
        
        elif state == "LEVEL_COMPLETE":
            button_clicked = menu_manager.handle_events(event, 'level_complete')
            if button_clicked == 0:  # Next level
                if self.game.current_level == 8:  
                    self.game.state = "GAME_COMPLETE"
                else:
                    self.game.current_level += 1
                    self.game.state = "PLAYING"
                    self.game.reset_level(preserve_health=True)
            elif button_clicked == 1:  # Main menu
                self.game.state = "MENU"
        
        elif state == "GAME_COMPLETE":
            button_clicked = menu_manager.handle_events(event, 'game_complete')
            if button_clicked == 0:  # Play again
                self.game.current_level = 1
                self.game.score = 0
                self.game.state = "PLAYING"
                self.game.reset_level(preserve_health=False)
            elif button_clicked == 1:  # Main menu
                self.game.state = "MENU"
            elif button_clicked == 2:  # Quit game
                return False
        
        return True
    
    def handle_keyboard_input(self, event):
        state = self.game.state
        
        if event.type != pygame.KEYDOWN:
            return True
        
        if state == "PLAYING":
            if event.key == pygame.K_w:
                self.game.player.jump()
            elif event.key == pygame.K_k: 
                self.game.player.shoot(self.game.player_bullets)
                for b in self.game.player_bullets:
                    if b not in self.game.all_sprites:
                        self.game.all_sprites.add(b)
            elif event.key == pygame.K_l:  
                self.game.player.dash()
            elif event.key == pygame.K_ESCAPE:
                self.game.state = "PAUSED"
        
        elif state == "MENU":
            if event.key == pygame.K_RETURN:
                self.game.state = "PLAYING"
                self.game.current_level = 1
                self.game.score = 0
                self.game.reset_level()
        
        elif state == "LEVEL_SELECT":
            if event.key == pygame.K_ESCAPE:
                self.game.state = "MENU"
            elif pygame.K_1 <= event.key <= pygame.K_8:  
                self.game.current_level = event.key - pygame.K_0
                self.game.score = 0
                self.game.state = "PLAYING"
                self.game.reset_level()
        
        elif state == "PAUSED":
            if event.key == pygame.K_ESCAPE:
                self.game.state = "PLAYING"
        
        elif state == "CONTROLS":
            if event.key == pygame.K_ESCAPE:
                # Return to wherever we came from
                if self.previous_state == "PAUSED":
                    self.game.state = "PAUSED"
                else:
                    self.game.state = "MENU"
                self.previous_state = None  # Reset
        
        elif state == "GAME_OVER":
            if event.key == pygame.K_1:
                self.game.state = "PLAYING"
                self.game.reset_level()
            elif event.key == pygame.K_r:
                self.game.current_level = 1
                self.game.score = 0
                self.game.state = "PLAYING"
                self.game.reset_level()
            elif event.key == pygame.K_ESCAPE:
                self.game.state = "MENU"
        
        elif state == "LEVEL_COMPLETE":
            if event.key == pygame.K_RETURN:
                if self.game.current_level == 8:  
                    self.game.state = "GAME_COMPLETE"
                else:
                    self.game.current_level += 1
                    self.game.state = "PLAYING"
                    self.game.reset_level(preserve_health=True)
            elif event.key == pygame.K_ESCAPE:
                self.game.state = "MENU"
        
        elif state == "GAME_COMPLETE":
            if event.key == pygame.K_r:
                self.game.current_level = 1
                self.game.score = 0
                self.game.state = "PLAYING"
                self.game.reset_level()
            elif event.key == pygame.K_ESCAPE:
                self.game.state = "MENU"
            elif event.key == pygame.K_q:
                return False
        
        return True