import pygame
import sys
import os
from ShipClass import Ship
from BulletClass import Bullet


# Definir otras constantes relacionadas con el juego
PLAYER_IMAGE = pygame.image.load(os.path.join('img', 'player_image.png'))
BULLET_IMAGE = pygame.image.load(os.path.join('img', 'bullet_image.png'))

WIDTH, HEIGHT = 800, 600

class Player(Ship):
    def __init__(self, x, y, x_speed, y_speed, health = 100):
        super().__init__(x, y, health)
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.ship_img = PLAYER_IMAGE
        self.bullet_img = BULLET_IMAGE
        self.bullet_speed = -10
        self.max_health = health
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.creation_cooldown_counter = 0
        self.max_amount_bullets = 3
        self.bullets = []
        self.bullet_cooldown_counter = 0
    # Movement
    def move(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and (self.y > 0):
            self.y -= self.y_speed
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and (self.y < HEIGHT - self.ship_img.get_height() - 60):
            self.y += self.y_speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (self.x < WIDTH - self.ship_img.get_width()):
            self.x += self.x_speed
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (self.x > 0):
            self.x -= self.x_speed

    def increase_speed(self):
        if self.x_speed < 10:
            self.x_speed += 1.25
            self.y_speed += 1.25
        elif self.x_speed >= 10:
            self.x_speed = 10
            self.y_speed = 8
        if self.cool_down > 25:
            self.cool_down *= 0.9

    def create_bullets(self):
        if (len(self.bullets) < self.max_amount_bullets) and (self.creation_cooldown_counter == 0):
            bullet = Bullet(self.x, self.y, self.bullet_img)
            self.bullets.append(bullet)
            self.creation_cooldown_counter = 1
        for bullet in self.fired_bullets:
            if bullet.y <= -40:
                self.fired_bullets.pop(0) 

    
    def cooldown(self):
        if self.bullet_cooldown_counter >= 20:
            self.bullet_cooldown_counter = 0
        elif self.bullet_cooldown_counter > 0:
            self.bullet_cooldown_counter += 1

        if self.creation_cooldown_counter >= self.cool_down :
            self.creation_cooldown_counter = 0
        elif self.creation_cooldown_counter > 0:
            self.creation_cooldown_counter += 1
            
    # Fire
    def fire(self, window):
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_SPACE]) and (len(self.bullets) > 0) and (self.bullet_cooldown_counter == 0):
            self.bullets[-1].x = self.x + (self.ship_img.get_width() - self.bullet_img.get_width())/2
            self.bullets[-1].y = self.y + 10
            self.fired_bullets.append(self.bullets.pop())
            self.bullet_cooldown_counter = 1
            self.creation_cooldown_counter = 1

        for i in range(len(self.fired_bullets)):
            self.fired_bullets[i].move(self.bullet_speed)
            self.fired_bullets[i].draw(window)
    
    def hit(self, enemy):
        for i in range(len(self.fired_bullets)):
            self.creation_cooldown_counter = self.cool_down *0.8
            return self.fired_bullets[i].collision(enemy)
         