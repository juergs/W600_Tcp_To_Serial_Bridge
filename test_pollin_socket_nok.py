import machine
import select
import socket

try:
    serial = machine.UART(1, 115200)
    serial.init(115200, bits=8, parity=None, stop=1)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 23))
    server.listen(5)  # max client
    server.setblocking(0)

    poll = select.poll()
    poll.register(server, select.POLLIN)
    sockets = {server.fileno(): server}
    print('server ', server.fileno())

    while True:
        for fd, event in poll.poll():
            print('socket ', fd.fileno(), ' event ', event)
            if event == select.POLLIN:
                if fd.fileno() == server.fileno():
                    client, addr = server.accept()
                    poll.register(client, select.POLLIN)
                    sockets[client.fileno()] = client
                    print('accept ', client, addr)
                    client.send(b"hello!")
                else:
                    client = sockets[fd.fileno()]
                    print('repond data ', client)
                    data = client.recv(64)  # max recv limit
                    print(data)
                    # disconnect, if you receive an empty packet or a specified string(such as data == b'disconnect').
                    if len(data) == 0 or data == b'disconnect':
                        poll.modify(client, select.POLLOUT)  # it modify to POLLOUT
            elif event == select.POLLOUT:
                client = sockets[fd.fileno()]
                sockets.pop(fd.fileno())
                client.send(b"goodbye!")
                poll.unregister(client)
                client.close()

finally:
    # it will throw error OSError: [Errno 12] ENOMEM if your dont exec the code.
    server.close()
