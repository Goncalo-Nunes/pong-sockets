import pygame
import socket
import time
import pickle
from thread import start_new_thread
from ball import Ball
from paddle import Paddle
from constants import WINDOW_HEIGHT, WINDOW_WIDTH


class Server:

    def __init__(self):
        self.S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.S.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.PORT = 5555
        self.HOST_NAME = socket.gethostname()
        self.SERVER_IP = "0.0.0.0"
        self.connections = 0
        self._id = 0
        self.players = {}
        self.ball = Ball(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        self.start_game = False


    def pickle_game_objects(self):
        return pickle.dumps((self.ball, list(self.players.values())))

    def start(self):
        try:
            self.S.bind((self.SERVER_IP, self.PORT))
        except socket.error as e:
            print(str(e))
            print("[SERVER] Server could not start")
            quit()

        self.S.listen()
        print(f"[SERVER] Server running on {self.SERVER_IP}")

    def handle_ball(self):
        if self.start_game:
            self.ball.move()
            self.ball.check_collision(self.players.values())

    def threaded_client(self, conn, current_id):
     
        print("[LOG] Player connected")

        if self.players == {}:
            x = 10
        else:
            x = WINDOW_WIDTH - self.players[1].WIDTH - 10

        self.players[current_id] = Paddle(x)
        conn.send(bytes(str(current_id), 'utf-8'))

        while True:
            try:
                data = conn.recv(32)
                if not data:
                    break

                data = data.decode("utf-8")
                split_data = data.split()
                #print(f"[DATA] Recieved {data} from client {current_id}")

                if split_data[0] == "move":
                    y = float(split_data[1])
                    self.players[current_id].y = y



                    send_data = self.pickle_game_objects()

                elif split_data[0] == "id":
                    send_data = bytes(str(current_id), 'utf-8')

                else:
                    send_data = self.pickle_game_objects()
                
                conn.send(send_data)

            except Exception as e:
                print(e)
                break


        print(f"[DISCONNECT] Client {current_id} disconnected")
        self.connections -= 1
        self._id -= 1

        del self.players[current_id]
        self.ball.reset()
        time.sleep(1)
        self.start_game = False
        conn.close()
            
    
    def main_loop(self):
        
        while True:

            if self.connections < 2:
                connection, adress = self.S.accept()
                print(f"[CONNECTION] Connected to {adress}")
                self.connections += 1
                self._id += 1
                start_new_thread(self.threaded_client, (connection, self._id))

            # adress[0] == self.SERVER_IP
            if self.connections == 2 and not self.start_game:
                self.start_game = True
                time.sleep(5)
                print("[GAME] Game started")
            

            self.handle_ball()
            pygame.time.Clock().tick(150)
        
        print("[SERVER] Server offline")



if __name__ == "__main__":
    server = Server()
    server.start()
    server.main_loop()

