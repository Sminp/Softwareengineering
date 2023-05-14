import socket
import pickle

class Client:
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.sock.connect((self.host, self.port))
            print("Connected to server")
            
            # 비밀번호를 서버에 전송합니다.
            self.sock.sendall(self.password.encode())
            response = self.sock.recv(1024).decode().strip()

            if response == "Wrong password":
                print("Wrong password")
                self.sock.close()
                return False

            print("Logged in")
            return True

        except ConnectionRefusedError:
            print("Connection refused")
            return False
