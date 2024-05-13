import socket
import threading
from enum import Enum
import protocol.handshake
import protocol.config
import protocol.queue
import protocol.packet
import protocol.keepAlive

HOST = "127.0.0.1"
PORT = 65432

queue = []


class State(Enum):
    HANDSHAKE = 0
    CONFIG = 1
    QUEUE = 2
    PLAY = 3


class ClientThread(threading.Thread):
    def __init__(self, conn, addr):
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.state = State.HANDSHAKE
        self.uuid = None
        self.is_alive = True

    def run(self):
        self.handle_client()

    def handle_client(self):
        print("New connection from", self.addr)
        with self.conn:
            while True:
                data = self.conn.recv(1024)
                if not data:
                    break
                print("Received : ", data)
                packet = protocol.packet.Packet.from_tcp_packet(data)
                match self.state:
                    case State.HANDSHAKE:
                        protocol.handshake.handle_handshake(self.conn)
                        self.state = State.CONFIG
                        print("Handshake successful")
                    case State.CONFIG:
                        self.uuid = protocol.config.handle_config_request(self.conn, packet.get_packet_data())
                        self.state = State.QUEUE
                        queue.append(self.uuid)
                        self.send_keep_alive()
                        print("Configuration successful")
                        protocol.queue.send_queue_position(self.conn, [i for i in range(len(queue)) if queue[i] == self.uuid][0])
                    case State.QUEUE:
                        match packet.get_packet_id():
                            case 0:
                                protocol.queue.handle_queue_request(self.conn)
                                print("Queue : Received", data)
                            case 153:
                                self.is_alive = True
                    case State.PLAY:
                        match packet.get_packet_id():
                            case 0:
                                print("Play : Received Player Position And Look")
                                print("Position : ", packet.get_packet_data())
                            case 1:
                                print("Play : Received Canon Look")
                                print("Rotation : ", packet.get_packet_data())


    def get_state(self):
        return self.state

    def kill_connection(self):
        queue.remove(self.uuid)
        threading.current_thread()

    def send_keep_alive(self):
        if not self.is_alive:
            self.kill_connection()
        print("Still alive")
        self.is_alive = False
        keep_alive_packet_id = b"\x99"
        self.conn.sendall(keep_alive_packet_id)
        threading.Timer(15, self.send_keep_alive).start()


def accept_connections(s):
    print("Server started on ", HOST, ":", PORT)
    while True:
        conn, addr = s.accept()

        client_thread = ClientThread(conn, addr)
        client_thread.start()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    accept_connections(s)
