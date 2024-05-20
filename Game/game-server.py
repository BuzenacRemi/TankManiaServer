import socket

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

        matchmaking_thread.add_to_queue(client_thread)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    accept_connections(s)
