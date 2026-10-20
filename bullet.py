import pygame
from settings import * 

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed=10, color=None, size=(10,5)):
        super().__init__()
        
        # Create bullet appearance
        self.image = pygame.Surface(size)  
        self.image.fill(color if color is not None else colors["yellow"]) 
        
        # Position and collision box
        self.rect = self.image.get_rect(center=(x, y))
        
        # Movement - velocity depends on direction and speed
        # direction: 1 = right, -1 = left
        self.vx = speed * direction
        
        # Add lifetime tracking for better cleanup
        self.spawn_x = x
        self.max_distance = 1000  # Remove bullet after traveling 1000 pixels

    def update(self, *args):
        # Move horizontally
        self.rect.x += self.vx
        
        # Remove bullet based on distance traveled OR screen bounds
        distance_traveled = abs(self.rect.x - self.spawn_x)
        if distance_traveled > self.max_distance:
            self.kill()
        # Also remove if way off screen
        elif self.rect.right < -200 or self.rect.left > 4000:
            self.kill()

class EnemyBullet(Bullet):
    def __init__(self, x, y, direction, speed=6):
        # IMPORTANT: direction should be 1 for right, -1 for left
        super().__init__(x, y, direction, speed, 
                        color=colors["red"],  
                        size=(8,4))
        
        # Shorter max distance for enemy bullets
        self.max_distance = 800
        
    def update(self, *args):
        # Move horizontally
        self.rect.x += self.vx
        
        # Better cleanup - remove based on distance or bounds
        distance_traveled = abs(self.rect.x - self.spawn_x)
        if distance_traveled > self.max_distance:
            self.kill()
        elif self.rect.right < -200 or self.rect.left > 4000 or self.rect.top > 800 or self.rect.bottom < -100:
            self.kill()

class AngledEnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed=6, angle=0):
        super().__init__()
        
        # Create bullet appearance
        self.image = pygame.Surface((8, 4))
        self.image.fill(colors["red"])
        
        # Position and collision box
        self.rect = self.image.get_rect(center=(x, y))
        
        # Movement with angle 
        import math
        # direction: 1 = right, -1 = left
        self.vx = speed * direction * math.cos(angle)
        self.vy = speed * math.sin(angle)
        
        # Track spawn position for distance-based cleanup
        self.spawn_x = x
        self.spawn_y = y
        self.max_distance = 800
        
        self.lifetime = 0
        self.max_lifetime = 200

    def update(self, *args):
        # Move with both horizontal and vertical velocity
        self.rect.x += self.vx
        self.rect.y += self.vy
      
        self.lifetime += 1
     
        dx = self.rect.x - self.spawn_x
        dy = self.rect.y - self.spawn_y
        distance_traveled = (dx * dx + dy * dy) ** 0.5
        
        # Remove bullet if it goes too far OR lives too long OR off screen
        if (distance_traveled > self.max_distance or
            self.lifetime > self.max_lifetime or
            self.rect.right < -200 or self.rect.left > 4000 or 
            self.rect.top > 800 or self.rect.bottom < -100):
            self.kill()