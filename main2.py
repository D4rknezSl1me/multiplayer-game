import socket
import threading

class TicTacToe:
    def __init__(self):
        self.board = [[" "]*3]*3
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
        print("Connected to",addr)
        self.you = "X"
        self.opponent = "O"
        threading.Thread(target=self.handle_connection, args=(client,)).start()
        server.close()

    def connect_to_game(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        print(f"Connected to {host} via port {port}")   
        self.you = "O"
        self.opponent = "X"
        threading.Thread(target=self.handle_connection, args=(client,)).start()

    def handle_connection(self, client):
        while not self.gameOver:
            if self.turn == self.you:
                move = eval(input("Enter a move (row,col): "))
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

    def check_valid_move(self, move):
        return self.board[move[0]][move[1]] == " "
    
    def apply_move(self, move, player):
        if self.gameOver:
            return
        self.counter +=1
        self.board[move[0]][move[1]] = player
        self.print_board()
        if self.check_won():
            if self.winner == self.you:
                print("You Win")
                exit()
            elif self.winner == self.opponent:
                print("You Lose")
                exit()
        elif self.counter == 9:
            print("It's a Tie!")
            exit()
    
    def check_won(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != " ":
                self.winner = self.board[row][0]
                self.gameOver = True
                return True
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != " ":
                self.winner = self.board[0][col]
                self.gameOver = True
                return True
        if (self.board[0][0] == self.board[1][1] == self.board[1][1] != " ") or (self.board[0][2] == self.board[1][1] == self.board[2][0] != " "):
            self.winner = self.board[1][1]
            self.gameOver
            return True
        return False
    
    def print_board(self):
        for row in range(3):
            print(f" {self.board[row][0]} | {self.board[row][1]} | {self.board[row][2]} ")

game = TicTacToe()
game.connect_to_game("localhost", 9999)