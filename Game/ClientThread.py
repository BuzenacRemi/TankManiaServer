import threading
from enum import Enum
import requests
from Game.protocol import handshake, config, queue
from Game.protocol.packet import Packet
from Game.protocol.queue import send_queue_position


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
        self.pos_x = 0
        self.pos_y = 0
        self.rotation = 0
        self.canon_rotation = 0

    def run(self):
        self.handle_client()
    def handle_client(self):
        print("New connection from", self.addr)
        with self.conn:
            while True:
                data = self.conn.recv(1024)
                if not data:
                    break
                #print("Received : ", data)
                packet = Packet.from_tcp_packet(data)
                match self.state:
                    case State.HANDSHAKE:
                        handshake.handle_handshake(self.conn)
                        self.state = State.CONFIG
                        print("Handshake successful")
                    case State.CONFIG:
                        self.uuid = str(config.handle_config_request(self.conn, packet.get_packet_data()))
                        print ("UUID : ", self.uuid)
                        threading.current_thread().name = self.uuid
                        self.state = State.QUEUE
                        print("Configuration successful")
                        pos_in_queue = -1
                        #send_queue_position(self.conn, [i for i in range(len(queue)) if queue[i] == self.uuid][0])
                        send_queue_position(self.conn, pos_in_queue)
                        #self.send_keep_alive()
                    case State.QUEUE:
                        match packet.get_packet_id():
                            case 0:
                                #handle_queue_request(self.conn)
                                print("Queue : Received", data)
                            case 153:
                                self.is_alive = True
                    case State.PLAY:
                        match packet.get_packet_id():
                            case 0:
                                pass
                                #print("Play : Received Player Position And Look")
                                print("Position : ", )
                            case 1:
                                pass
                                #print("Play : Received Canon Look")
                                #print("Rotation : ", packet.get_packet_data())
                            case 2:
                                pass
                                #print("Play : Received Player Movement")
                                #print("Bullet Shooted : ", packet.get_packet_data())
    def get_state(self):
        return self.state
    def send_keep_alive(self):
        if not self.is_alive:
            print("Connection lost")
            return
        print("Still alive")
        self.is_alive = False
        keep_alive_packet_id = b"\x99"
        self.conn.sendall(keep_alive_packet_id)
        threading.Timer(15, self.send_keep_alive).start()
