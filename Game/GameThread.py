import threading

from Game.ClientThread import ClientThread


class Player:
    def __init__(self, thread: ClientThread):
        self.thread = thread
        self.remaining_lives = 3
        self.bullets = []
        self.position = (0, 0)


class GameThread(threading.Thread):
    def __init__(self, player1: ClientThread, player2: ClientThread):
        super().__init__()
        self.player1 = player1
        self.player2 = player2
        self.pos_player1 = bytes
        self.pos_player2 = bytes

    def run(self):
        while 1:
            if self.pos_player1 != self.player1.pos:
                print("player1 moved")
                self.pos_player1 = self.player1.pos
                packet_content = b'0'
                for byte in self.pos_player1:
                    packet_content += bytes([byte])
                self.player2.conn.sendall(packet_content)
            if self.pos_player2 != self.player2.pos:
                print("player2 moved")
                self.pos_player2 = self.player2.pos
                packet_content = b'0'
                for byte in self.pos_player2:
                    packet_content += bytes([byte])
                self.player1.conn.sendall(packet_content)
