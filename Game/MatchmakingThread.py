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
                player1: ClientThread.ClientThread = self.queue.pop(0)
                player2: ClientThread.ClientThread = self.queue.pop(0)
                print("Match found")
                if player1.state == State.QUEUE:
                    Game.GameThread.GameThread(player1, player2).start()
                else :
                    print("One of the player is not ready")
            time.sleep(1)

    def add_to_queue(self, player: ClientThread):
        self.queue.append(player)