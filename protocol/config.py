
def handle_config_request(conn, data):
    config_response = b"\x00"+data
    conn.sendall(config_response)
    print("Config : Sent", config_response)
    return str(data)



