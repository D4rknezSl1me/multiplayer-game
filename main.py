import socket
import threading

class TicTacToe:
    def __init__(self):
        self.board = [[""]*3]*3
        self.turn = "X"
        self.you = "X"
        self.opponent = "O"
        self.winner = None
        self.gameOver = False
        self.counter = 0

    def host_game(self, host, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # set tpc connection
        server.bind((host,port))
        server.listen(1)    # listen for 1 connection

        client, addr = server.accept()
        self.you = "X"
        self.opponent = "O"
        threading.Thread(target=self.handle_connection, args=(client,)).start()
        server.close()

    def connect_to_game(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(host, port)
        self.you = "O"
        self.opponent = "X"
        threading.Thread(target=self.handle_connection, args=(client,)).start()

    def handle_connection(self, client):
        while not self.gameOver:
            if self.turn == self.you:
                move = eval(input("Enter a move (row, col): "))
                if self.check_valid_move(move):
                    self.apply_move(move, self.you)
                    self.turn = self.opponent
                    client.send(move.encode('utf-8'))
                else: 
                    print("Invalid move!")
            else:
                data = client.recv(1024)
                if not data:
                    break
                else:
                    self.apply_move(data.decode('uft-8'), self.opponent)
                    self.turn = self.you
        client.close()



