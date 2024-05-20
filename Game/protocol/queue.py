def send_queue_position(conn, position):
    queue_response = b"\x00" + str(position).encode()
    conn.sendall(queue_response)
    print("Queue : Sent", queue_response)


def handle_queue_request(conn):
    position = -1
    print("Queue : Request received")
    send_queue_position(conn, position)

