def send_queue_position(conn, position):
    queue_response = b"\x00" + position.to_bytes(1, byteorder='big')
    conn.sendall(queue_response)
    print("Queue : Sent", queue_response)


def handle_queue_request(conn):
    position = 0
    print("Queue : Request received")
    send_queue_position(conn, position)
