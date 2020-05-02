# W600_Tcp_To_Serial_Bridge
See: [Wiki](https://github.com/juergs/W600_Tcp_To_Serial_Bridge/wiki) for more informations.


Unresolved: blocking connection.recv(255) doesn't allow asynchronous serial send/ tcp receive.

See: [select with socket](https://steelkiwi.com/blog/working-tcp-sockets/) and [nonblocking socket](https://forum.micropython.org/viewtopic.php?t=4211)
