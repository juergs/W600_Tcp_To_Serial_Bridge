# W600_Tcp_To_Serial_Bridge
See: [Wiki](https://github.com/juergs/W600_Tcp_To_Serial_Bridge/wiki) for more informations.


<s>Unresolved</s> Solved: blocking connection.recv(255) doesn't allow asynchronous serial send/ tcp receive. 

>socket.accept() returns a tuple, consisting of the a socket and an address. So in your script, the variable connection is of 
>type "socket". Which can set to non-blocking mode by connection.setblocking(False). 
  
The Script 	connect_jsi_main.py serves as initializer on setup (main.py) to establish a WLAN-connection before opening a socket server 
by executing of script Serial_Bridge_ok.py.

See: [select with socket](https://steelkiwi.com/blog/working-tcp-sockets/) and [how can non-blocking socket instances be implemented](https://forum.micropython.org/viewtopic.php?t=4211)


<img src="https://github.com/juergs/W600_Tcp_To_Serial_Bridge/blob/master/pictures/MapleSDuino-Serial_Bridge_W600.png" width="800"/>

<img src="https://github.com/juergs/W600_Tcp_To_Serial_Bridge/blob/master/pictures/W600_Tcp_To_Serial_Bridge.png" width="800"/>
