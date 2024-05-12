def handle_handshake(conn):
    handshake_response = b"\x00"
    conn.sendall(handshake_response)
    print("Handshake : Sent", handshake_response)
