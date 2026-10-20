import pygame
from bullet import *
from settings import *
from items import PowerUpManager

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path=None):
        super().__init__()
        
        # Load and scale original image
        self.original_image = pygame.image.load('IMG/X/X.PNG').convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (80, 80))
        
        # Set current image 
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(topleft=(x, y))  

        # movement 
        self.vel_x = 0  
        self.vel_y = 0  
        self.speed = 5  
        self.jump_strength = 15
        self.gravity = 0.8  
        self.on_ground = False  
        self.facing = 1  

        # health
        self.health = 5 
        self.max_health = 5  
        
        # invincibility frames 
        self.invulnerable = False
        self.invulnerable_time = 0
        self.invulnerable_duration = 500  
        
        # shooting cooldown
        self.last_shot_time = 0
        self.shoot_cooldown = 500
        self.normal_cooldown = 500
        self.rapid_fire_cooldown = 100  
        
        # Dash ability
        self.dash_speed = 15
        self.dash_duration = 200  # milliseconds
        self.dash_cooldown = 1000  # 1 second cooldown
        self.is_dashing = False
        self.dash_start_time = 0
        self.last_dash_time = 0
        self.dash_direction = 0
        
        # Dash invulnerability
        self.dash_invulnerable = True
        
        # Power-up manager
        self.powerup_manager = PowerUpManager()

    def update_sprite_direction(self):
        if self.facing == 1:
            self.image = self.original_image.copy()
        else:  
            self.image = pygame.transform.flip(self.original_image, True, False)
        
        # Visual feedback for dashing
        if self.is_dashing:
            self.image.set_alpha(150)  # Make player semi-transparent during dash
        else:
            self.image.set_alpha(255)

    def update(self, platforms, keys): 
        current_time = pygame.time.get_ticks()
        
        self.update_invulnerability()
        
        # Update shooting cooldown based on rapid fire status
        if self.powerup_manager.is_active("rapid_fire"):
            self.shoot_cooldown = self.rapid_fire_cooldown
        else:
            self.shoot_cooldown = self.normal_cooldown
        
        # Handle dash
        if self.is_dashing:
            dash_elapsed = current_time - self.dash_start_time
            if dash_elapsed >= self.dash_duration:
                self.is_dashing = False
                self.update_sprite_direction()
            else:
                # Store old position for collision checking
                old_x = self.rect.x
                
                # Move at dash speed
                self.rect.x += self.dash_speed * self.dash_direction
                
                # Check for wall collisions during dash
                self._collide_horizontal(platforms)
                
                # If we hit a wall, stop dashing
                if self.rect.x == old_x:
                    self.is_dashing = False
                    self.update_sprite_direction()
                
                self.vel_y += self.gravity * 0.3
                if self.vel_y > 15:
                    self.vel_y = 15
                self.rect.y += self.vel_y
                self._collide_vertical(platforms)
                return  
        
        # horizontal movement  
        self.vel_x = 0  
        
        if keys[pygame.K_a]:  
            self.vel_x = -self.speed
            self.facing = -1  
        if keys[pygame.K_d]:  
            self.vel_x = self.speed
            self.facing = 1   

        # update sprite direction
        self.update_sprite_direction()

        # gravity 
        self.vel_y += self.gravity
        if self.vel_y > 15:  
            self.vel_y = 15

        # horizontal collision 
        self.rect.x += self.vel_x
        self._collide_horizontal(platforms)

        # vertical collision 
        self.rect.y += self.vel_y
        self._collide_vertical(platforms)

    def dash(self):
        #Perform a dash in the direction player is facing
        current_time = pygame.time.get_ticks()
        
        # Check if dash is off cooldown
        if not self.is_dashing and current_time - self.last_dash_time >= self.dash_cooldown:
            self.is_dashing = True
            self.dash_start_time = current_time
            self.last_dash_time = current_time
            self.dash_direction = self.facing
            
            # Optional: make player invulnerable during dash
            if self.dash_invulnerable:
                self.invulnerable = True
                self.invulnerable_time = current_time
            
            return True
        return False

    def jump(self):
        #only jump if on ground
        if self.on_ground:
            self.vel_y = -self.jump_strength  
            self.on_ground = False

    def _collide_horizontal(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_x > 0 or (self.is_dashing and self.dash_direction > 0):  
                    self.rect.right = platform.rect.left
                elif self.vel_x < 0 or (self.is_dashing and self.dash_direction < 0):  
                    self.rect.left = platform.rect.right

    def _collide_vertical(self, platforms):
        self.on_ground = False  
        
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0  
                    self.on_ground = True 
                elif self.vel_y < 0:  
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0  
    
    def shoot(self, bullet_group):
        #Shoot bullets with power-up support
        current_time = pygame.time.get_ticks()
        
        # Only shoot if cooldown has passed
        if current_time - self.last_shot_time >= self.shoot_cooldown:
            bullet_x = self.rect.centerx + (self.facing * 20) 
            bullet_y = self.rect.centery
            
            # Triple shot power-up
            if self.powerup_manager.is_active("triple_shot"):
                # Center bullet
                b1 = Bullet(bullet_x, bullet_y, self.facing)
                bullet_group.add(b1)
                
                # Upper bullet
                b2 = Bullet(bullet_x, bullet_y - 15, self.facing)
                bullet_group.add(b2)
                
                # Lower bullet
                b3 = Bullet(bullet_x, bullet_y + 15, self.facing)
                bullet_group.add(b3)
            else:
                # Normal single bullet
                b = Bullet(bullet_x, bullet_y, self.facing)
                bullet_group.add(b)
            
            self.last_shot_time = current_time

    def update_invulnerability(self):
        #Update invincibility frames
        if self.invulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.invulnerable_time > self.invulnerable_duration:
                self.invulnerable = False
    
    def take_damage(self, amount=1):
        #damage with invincibility frames
        if not self.invulnerable:
            self.health -= amount
            self.invulnerable = True
            self.invulnerable_time = pygame.time.get_ticks()
        return self.health <= 0
    
    def heal(self, amount=1):
        #Heal the player#
        if self.health < self.max_health:
            self.health = min(self.health + amount, self.max_health)
            return True
        return False
    
    def collect_item(self, item):
        #Handle item collection
        if item.item_type == "rapid_fire":
            self.powerup_manager.activate_powerup("rapid_fire", item.duration)
            return True
        elif item.item_type == "triple_shot":
            self.powerup_manager.activate_powerup("triple_shot", item.duration)
            return True
        elif item.item_type == "med_kit":
            return self.heal(item.heal_amount)
        return False
    
    def get_dash_cooldown_percent(self):
        #Returns dash cooldown for UI display
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.last_dash_time
        if elapsed >= self.dash_cooldown:
            return 1.0
        return elapsed / self.dash_cooldown