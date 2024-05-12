class Packet:
    packet_id: int
    packet_data: bytes

    def __init__(self, packet_id: int, packet_data: bytes):
        self.packet_id = packet_id
        self.packet_data = packet_data

    def __eq__(self, other):
        return self.packet_id == other.packet_id and self.packet_data == other.packet_data

    def __str__(self):
        return f"Packet({self.packet_id}, {self.packet_data})"

    def from_tcp_packet(data):
        return Packet(data[0], data[1:])

    def get_packet_id(self):
        return self.packet_id

    def get_packet_data(self):
        return self.packet_data
