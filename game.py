import pygame
from ball import Ball
from paddle import Paddle
from constants import *



class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("PONG!")
        self.WIN = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.run = True
        self.players = []
        self.ball = None
        self.players.append(Paddle(10))
        self.players.append(Paddle(WINDOW_WIDTH-30))
        self.ball = Ball(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                break

    def update(self):

        for player in self.players:
            player.move()
            player.draw(self.WIN)

        self.ball.move()
        self.ball.draw(self.WIN)
        self.ball.check_collision(self.players)

    def main_loop(self):
        while self.run:
            self.WIN.fill(BLACK)
            self.update()
            self.check_events()
            pygame.display.update()
            self.clock.tick(self.FPS)


def main():
    Game().main_loop()
    pygame.quit()
    quit()



if __name__ == "__main__":
    main()



    



