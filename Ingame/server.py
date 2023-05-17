import pygame
import socket
import threading
from _thread import *
import pickle
# from game_functions import *
import game_functions

class Server:
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.bind((self.host, self.port))
        except socket.error as e:
            print(str(e))
        self.sock.listen(2) # 최대 플레이어 수 
        self.clients = []
        self.player_name = []

    def threaded_client(self, conn, player):
        self.clients.append(conn)
        conn.send(pickle.dumps(player))
        reply = {}
        
        while True:
            try:
                    
                data = pickle.loads(conn.recv(2048))

                data_key = list(data.keys())[0]
                data_val = list(data.values())[0]
                
                if data_key == 'password':
                    reply['password'] = self.password
                elif data_key == 'add_players':
                    self.player_name.append(data_val)
                    reply['players'] = self.player_name
                elif data_key == 'get_players':
                    reply['players'] = self.player_name
                elif data_key == 'change_name':
                    self.player_name[int(data_val.split(',')[1])] = data_val.split(',')[0]
                    reply['players'] = self.player_name
                elif data_key == 'disconnect':
                    del reply['players'][data_val]
                elif data_key == 'kick':
                    self.clients[data_val].close()
                    del self.clients[data_val]
                    del self.player_name[data_val]
                elif data_key == 'full':
                    reply['full'] = data_val
                                     
                conn.sendall(pickle.dumps(reply))

            except Exception as e:
                print(str(e))
                break

        if conn in self.clients:
            self.clients.remove(conn)
            conn.close()

    def run(self):
        print(f"Server started on {self.host}:{self.port}")
        print(f"Password is {self.password}")
        print("Waiting for connections...")
        current_player = 0

        while True:
            conn, addr = self.sock.accept()
            print("Connected to:", addr)

            start_new_thread(self.threaded_client, (conn, current_player))
            current_player += 1

