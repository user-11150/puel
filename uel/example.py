import socket
sock = socket.socket();
sock.bind(("127.0.0.1",2500))
sock.listen(128)
while True:
    conn, addr = sock.accept()
    user_send = conn.recv(1024)
    print(user-send)