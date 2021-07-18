import pygame
from constants import *

class Paddle:

    def __init__(self, x):
        self.x = x
        self.HEIGHT = 100
        self.WIDTH = 15
        self.SPEED = 6
        self.y = (WINDOW_HEIGHT / 2) - (self.HEIGHT / 2)

    def get_pos(self):
        return (self.x, self.y)

    def get_rect(self):
        return pygame.Rect(self.get_pos(), (self.WIDTH, self.HEIGHT))

    def draw(self, win):
        pygame.draw.rect(win, WHITE, self.get_rect())

    def set_y(self):
        pass
    
    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and self.y >= 0:
            self.y -= self.SPEED

        if keys[pygame.K_DOWN] and (self.y + self.HEIGHT < WINDOW_HEIGHT):
            self.y += self.SPEED

        



