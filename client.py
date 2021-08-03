import socket
import pickle

class Client:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET)
        self.host = "0.0.0.0" # The server ip
        self.port = 5555
        self.address = (self.host, self.port)

    def connect(self):
        self.client.connect(self.address)
        reply = self.client.recv(8)
        return int(reply.decode("utf-8"))

    def disconnect(self):
        self.client.close()

    def send(self, data, pick=False):
        try:
            if pick:
                self.client.send(pickle.dumps(data))
            else:
                self.client.send(bytes(data, 'utf-8'))
                
            reply = self.client.recv(1024)

            try:
                reply = pickle.loads(reply)
            except Exception as e:
                print(e)
            
            return reply
        
        except socket.error as e:
            print(e)