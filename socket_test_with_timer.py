# Do not use this code in real projects! Read
# http_server_simplistic_commented.py for details.
try:
    import usocket as socket
except:
    import socket
import sys

import ntptime
from machine import RTC
from machine import Timer
from machine import UART

buffer = []
rtc = RTC()
serial = UART(1, 115200)
data = None
timer5 = Timer(5)


def init_timer():
    print("*** init timer ->")
    global timer5
    timer5.init(period=2000, mode=Timer.PERIODIC, callback=lambda y: (
                                                                    print("~~~ Timer5.Tick: ->"),
                                                                    read_serial(),
                                                                    print("~~~ Timer5.Tick: <-")
                                                                     )
               )
    print("*** <- init timer")


def init_serial():
    print("*** init serial ->")
    serial.init(115200, bits=8, parity=None, stop=1)
    time.sleep(1)
    serial.write('Hello world' + chr(10) + chr(13))
    print("*** <- init serial ")


def read_serial():
    print("*** read_serial ->")
    global data
    data = None
    data = serial.readline()
    if not data:
        print("+++ read_serial: no_data")
        pass
    else:
        global buffer
        buffer.append(data)
        print("+++ read_serial: appended %s" % data)
    print("*** read_serial <-")


def get_timestamp():
    ts = rtc.now()
    return str(ts)


def main():
    print("*** Main ->")

    global rtc
    global buffer
    global data
    global timer4

    # ntptime.settime()
    print("%s *** Init RTC")
    rtc.init((2019, 9, 12, 3, 13, 0, 0, 0))

    print("*** Init serial ")
    init_serial()

    print("*** Init socket")

    # ===============================================
    print("*** init socket: running on 0.0.0.0:23")
    address = ('0.0.0.0', 23)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("*** init: Opts?")
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("*** init: Bind")
    s.bind(address)
    print("*** init: Bind done.")
    s.listen(1)
    print("*** init: Listening on ", address)
    # ===============================================

    print("*** Init TIMER")
    init_timer()

    print("*** Forever outer loop")
    # --- main loop
    while True:
        res = s.accept()
        client_s = res[0]
        client_addr = res[1]

        while True:
            print("*** Forever inner loop")

            req = client_s.recv(4096)
            if not req:
                print("*** no_data,  client disconnected?")
                client_s.close()
                sys.exit(0)
            else:
                if req == bytearray("b''"):
                    pass
                else:
                    print("+++ Request: %s" % req)

            # let timers execute, gain serial data
            time.sleep(10)

            if buffer:
                if len(buffer) > 0:
                    for line in buffer:
                        if client_s:
                            ba = bytearray()
                            ba.extend(line)
                            client_s.sendall(ba)
                            print("==> sending serial content: %s" % line)
                            buffer.clear()
                # client_s.close()
            else:
                print("*** no serial data.")

            # print("............................")


if __name__ == '__main__':
    main()
