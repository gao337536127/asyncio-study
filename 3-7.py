import selectors
import socket
from selectors import SelectorKey
from typing import List, Tuple

selector = selectors.DefaultSelector()

server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ("127.0.0.1", 8000)
server_socket.setblocking(False)
server_socket.bind(server_address)
server_socket.listen()

selector.register(server_socket, selectors.EVENT_READ)

while True:
    events: List[Tuple[SelectorKey, int]] = selector.select(timeout=1)

    if len(events) == 0:
        print("No events, waiting a bit mode!")

    for event, _ in events:
        # 获取该事件的套接字，套接字存储在fileobj字段中
        event_socket = event.fileobj

        if event_socket == server_socket:
            # 这里表示有新连接进来
            connection, client_address = server_socket.accept()
            connection.setblocking(False)
            print(f"I got a connection from {client_address}")
            selector.register(connection, selectors.EVENT_READ)
        else:
            try:
                data = event_socket.recv(1024)
            except ConnectionResetError:
                data = b""

            if not data:
                print(f"Client disconnected: {event_socket.getpeername()}")
                selector.unregister(event_socket)
                event_socket.close()
                continue

            print(f"I got some data: {data}")
            event_socket.send(data)
