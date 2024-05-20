import threading
import time

import Game.GameThread
from Game import ClientThread
from Game.ClientThread import State


class MatchmakingThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.queue = []
        self.is_alive = True

    def run(self):
        while self.is_alive:
            if len(self.queue) >= 2:
                tmpP1: ClientThread.ClientThread = self.queue[0]
                tmpP2: ClientThread.ClientThread = self.queue[1]
                if tmpP1.state == State.QUEUE and tmpP2.state == State.QUEUE:
                    player1: ClientThread.ClientThread = self.queue.pop(0)
                    player2: ClientThread.ClientThread = self.queue.pop(0)
                    player1.state = State.PLAY
                    player2.state = State.PLAY
                    Game.GameThread.GameThread(player1, player2).start()
                time.sleep(1)

    def add_to_queue(self, player: ClientThread):
        self.queue.append(player)

#Ceci est un commentaire pour push bordel