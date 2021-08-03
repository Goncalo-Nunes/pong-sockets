import pygame
from random import randint
from constants import *

class Ball:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.RADIUS = 14
        self.SPEED = 3
        self.x_velocity = self.SPEED
        self.y_velocity = randint(-self.SPEED, self.SPEED)

    def get_pos(self):
        return (self.x, self.y)

    def get_rect(self):
        return pygame.Rect(self.x - self.RADIUS/2, self.y- self.RADIUS/2, self.RADIUS, self.RADIUS)

    def reset(self):
        self.x = WINDOW_WIDTH / 2
        self.y = WINDOW_HEIGHT / 2
        self.x_velocity = self.SPEED
        self.y_velocity = randint(-self.SPEED, self.SPEED)



    def draw(self, win):
        pygame.draw.circle(win, WHITE, self.get_pos(), self.RADIUS)

    def check_collision(self, paddles: list):
        for paddle in paddles:
            if self.get_rect().colliderect(paddle.get_rect()):
                delta_y = (paddle.y + paddle.HEIGHT/2) - self.y
                self.y_velocity = delta_y * -0.15
                self.x_velocity *= -1
                return True

        return False

    def move(self):
            
        if (self.x <= 0) or (self.x + self.RADIUS >= WINDOW_WIDTH):
            self.reset()

        if (self.y - self.RADIUS <= 0) or (self.y + self.RADIUS >= WINDOW_HEIGHT):
            self.y_velocity *= -1

        self.y += self.y_velocity
        self.x += self.x_velocity
       
