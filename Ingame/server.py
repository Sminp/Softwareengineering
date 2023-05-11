import pygame
import socket
import threading

class Server:
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        self.clients = []
        self.p = 0

    def handle_client(self, conn, addr):
        # 클라이언트가 접속하면 이 함수가 호출됩니다.
        print(f"{addr} connected")
        self.clients.append(conn)
         
        # 비밀번호를 검사합니다.
        conn.sendall("Enter password: ".encode())
        password = conn.recv(1024).decode().strip()
        if password != self.password:
            print(f"{addr} disconnected (wrong password)")
            conn.sendall("Wrong password".encode())
            self.clients.remove(conn)
            self.p -= 1
            conn.close()
            return

        # 비밀번호가 일치할 경우 접속을 허용합니다.
        print(f"{addr} logged in")
        conn.sendall("Welcome to the server".encode())
        conn.send(str.encode(str(self.p)))
        self.p += 1

        while True:
            data = conn.recv(1024)
            if not data:
                break
            # 클라이언트로부터 받은 데이터를 처리합니다.
            # ...

        print(f"{addr} disconnected")
        self.clients.remove(conn)
        self.p -= 1
        conn.close()

    def run(self):
        print(f"Server started on {self.host}:{self.port}")
        print(f"Password is {self.password}")
        print("Waiting for connections...")

        while True:
            conn, addr = self.sock.accept()

            # 클라이언트가 접속하면 새로운 스레드를 생성하여 클라이언트와 통신합니다.
            t = threading.Thread(target=self.handle_client, args=(conn, addr))
            t.start()

