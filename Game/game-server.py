import socket
import time

from Game.ClientThread import ClientThread
from Game.MatchmakingThread import MatchmakingThread

HOST = "127.0.0.1"
PORT = 65432

matchmaking_thread = MatchmakingThread()
matchmaking_thread.start()


def accept_connections(s):
    while True:
        conn, addr = s.accept()
        client_thread = ClientThread(conn, addr)
        client_thread.start()

        # Attendre que l'UUID soit défini
        while client_thread.uuid is None:
            time.sleep(0.1)

        matchmaking_thread.add_to_queue(client_thread)

        matchmaking_thread.update_rank(client_thread.uuid)



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    accept_connections(s)

