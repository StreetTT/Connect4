import socket 
import threading

class Conn4:
    def __init__(self) -> None:
        self.board: list["Stack"] = []
        for _ in range(7):
            self.board.append(Stack(7))
        self.winner = None
        self.turn = "X"
        self.gameOver = False
    
    def getOpponent(self):
        if self.you == "X":
            return "O"
        return "X"

    def hostGame(self, host, port):
        self.you = "X"
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(1)

        client, addr = server.accept()

        threading.Thread(target=self.handleConnection, args=(client,)).start()

        server.close()
    
    def connectGame(self, host, port):
        self.you = "O"
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((host, port))
        
        threading.Thread(target=self.handleConnection, args=(client,)).start()
    
    def handleConnection(self, client: socket.socket):
        while not self.gameOver:
            if self.turn == self.you:
                move = input("Enter a Column: ")
                if self.moveValid(move):
                    client.send(move.encode('utf-8'))
                    self.applyMove(move, self.you)
                    self.turn = self.getOpponent()
                else:
                    print("Invalid Move")
            else:
                data = client.recv(1024)
                if  not data:
                    break
                self.applyMove(data.decode('utf-8'), self.getOpponent())
                self.turn = self.you
        client.close()
    
    def applyMove(self, move, player):
        if self.gameOver:
            return
        self.board[int(move)-1].push(player)
        self.printBoard()
        if self.gameIsWon():
            if self.winner == self.you:
                print("Congrats, you win")
            else:
                print("Sucks ass, do better")
            exit()
    
    def moveValid(self, move):
        return move in ("1","2","3","4","5","6","7") and not self.board[int(move)-1].full()
    
    def gameIsWon(self):
        directions = [(1, 0), (0, 1), (1, 1), (-1, 1)]  # Horizontal, Vertical, Diagonal (\), Diagonal (/)
    
        for direction in directions:
            for col in range(7):
                for row in range(6):
                    if self.board[col].stack[row] != " ":
                        player = self.board[col].stack[row]
                        count = 1
                        for i in range(1, 4):
                            new_col = col + direction[0] * i
                            new_row = row + direction[1] * i
                            if 0 <= new_col < 7 and 0 <= new_row < 6 and self.board[new_col].stack[new_row] == player:
                                count += 1
                            else:
                                break
                        if count == 4:
                            self.winner = player
                            self.gameOver = True
                            return True
        return False
    
    def printBoard(self):
        print("+---+---+---+---+---+---+---+")
        for i in range(7):  # Rows are printed from top to bottom
            for j in range(7):  # Columns are printed from left to right
                print("| " + self.board[j].stack[6-i] + " ", end="")
            print("|")
            print("+---+---+---+---+---+---+---+")
        print("  1   2   3   4   5   6   7  ")
    
class Stack:
    def __init__(self, size) -> None:
        self.stack = [" " for _ in range(size)]
        self.pointer = 0
        self.size = size

    def push(self, item):
        if not self.full():
            self.stack[self.pointer] = item
            self.pointer += 1
    
    def full(self):
        if self.pointer >= self.size:
            return True
        return False
