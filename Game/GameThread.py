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

    def run(self):
        while 1:
            pass