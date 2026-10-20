import pygame

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("IMG/Boss/Boss.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = 100
        self.max_health = 100
        self.speed = 2
        self.damage = 10
        self.attack_timer = 0
        self.hit_timer = 0  
        self.is_hit = False

    def update(self, player, projectiles, dt):
        # Boss movement 
        self.move_towards_player(player)

        # Handle attacks
        if self.attack_timer <= 0:
            self.attack(player)
            self.attack_timer = 2000  
        else:
            self.attack_timer -= dt

        # Check for collisions with player projectiles
        self.check_projectile_collisions(projectiles)

        # Handle hit feedback
        if self.is_hit:
            self.hit_timer -= dt
            if self.hit_timer <= 0:
                self.is_hit = False

    def move_towards_player(self, player):
        # Move the boss toward the player's position
        if self.rect.x < player.rect.x:
            self.rect.x += self.speed
        elif self.rect.x > player.rect.x:
            self.rect.x -= self.speed

        if self.rect.y < player.rect.y:
            self.rect.y += self.speed
        elif self.rect.y > player.rect.y:
            self.rect.y -= self.speed

    def attack(self, player):
        if self.rect.colliderect(player.rect):
            player.take_damage(self.damage)

    def check_projectile_collisions(self, projectiles):
        for projectile in projectiles:
            if self.rect.colliderect(projectile.rect):
                self.take_damage(projectile.damage)
                projectile.kill()  

    def take_damage(self, amount):
        self.health -= amount
        self.is_hit = True
        self.hit_timer = 200  
        if self.health <= 0:
            self.die()

    def die(self):
        # Handle boss death 
        print("Boss defeated!")

    def draw_health_bar(self, screen):
        # Draw the boss's health bar above its sprite
        bar_width = 100
        bar_height = 10
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 20, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 20, bar_width * health_ratio, bar_height))

    def draw(self, screen):
        # Draw the boss sprite and health bar
        screen.blit(self.image, self.rect)
        self.draw_health_bar(screen)
        if self.is_hit:
            # Flash effect when hit
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 3)