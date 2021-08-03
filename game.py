import pygame
from ball import Ball
from paddle import Paddle
from client import Client
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
        self.player = None
        self.ball = None
        self.client = None
        self.current_id = 0
        self.data = ""

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                break

    def update(self):

        for player in self.players:
            #player.move()
            player.draw(self.WIN)

        #self.ball.move()
        self.ball.draw(self.WIN)
        #self.ball.check_collision(self.players)
        self.player.move()
        self.data = f"move {self.player.y}" 

    def connect_client(self):
        self.client = Client()
        self.current_id = self.client.connect()
        self.ball, self.players = self.client.send("get")
        self.player = self.players[self.current_id-1]

    def main_loop(self):

        while self.run:
            self.WIN.fill(BLACK)
            self.update()
            self.ball, self.players = self.client.send(self.data) 
            self.check_events()
            pygame.display.update()
            self.clock.tick(self.FPS)
        self.client.disconnect()
        


def main():
    game = Game()
    game.connect_client()
    game.main_loop()
    pygame.quit()
    quit()



if __name__ == "__main__":
    main()



    



