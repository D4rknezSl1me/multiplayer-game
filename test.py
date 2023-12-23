board = [["X"]*3]*3
for row in range(3):
    print(f" {board[row][0]} | {board[row][1]} | {board[row][2]}")
    print("----------") if row != 2 else None