# Serial_to_TCP-Bridge to serve Maple-Signalduino as WLAN-gateway to FHEM
# Author: JUERGS @ 2020.05.05
# Thanks to: RALF9 & SIDEY in respect to their great work, developing the radio receiver device firmware Signalduino.
# Also very thanks to Roberthh @ https://forum.micropython.org/memberlist.php?mode=viewprofile&u=601
# for providing the solution for the blocking socket!
# 20200505_juergs: Version 0.0.1 (pre-release)

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
        # print("~~~ Timer5.Tick: ->"),
        read_serial(),
        # print("~~~ Timer5.Tick: <-")
    )
                )
    print("*** <- init timer")


def init_serial():
    """Additional keyword - only parameters that may  be
        https://docs.micropython.org/en/latest/library/machine.UART.html
    """
    print("*** init serial ->")
    serial.init(115200, bits=8, parity=None, stop=1)
    time.sleep(1)
    serial.write('Hello world' + chr(10) + chr(13))
    print("*** <- init serial ")


def read_serial():
    # print("*** read_serial ->")
    global data
    data = None
    data = serial.readline()
    if not data:
        # print("+++ read_serial: no_data")
        pass
    else:
        global buffer
        buffer.append(data)
        print("+++ read_serial: appended %s" % data)
    # print("*** read_serial <-")


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
    print("*** init RTC")
    rtc.init((2019, 9, 12, 3, 13, 0, 0, 0))

    print("*** init serial ")
    init_serial()

    # ===============================================
    print("*** init socket: will run local socket-server  on 0.0.0.0:23")
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

    print("*** forever outer loop")
    # --- main loop
    while True:
        print("*** socket accept client")
        res = s.accept()
        client_s = res[0]
        client_addr = res[1]
        client_s.setblocking(False)

        '''' --- now we could start to serve serial data'''
        print("*** init Timer")
        init_timer()

        while True:
            ''' --- prepare to receive data'''
            try:
                ''' --- try to receive data from client'''
                req = client_s.recv(1024)
                if req:
                    ''' --- yes, we have tcp data, send it directly to serial device'''
                    got_serial_data = False
                    output_msg = ""
                    global serial
                    msg = '+++ received tcp data {!r}'.format(req)
                    print(msg)
                    # msg = msg.decode('ascii')
                    if req == bytearray("b''"):
                        pass
                    elif "V" in str(req):
                        buffer.append("V 3.3.1 SIGNALduino cc1101 (chip CC1101) - compiled at Dec 3 2019 19:40:46 " + chr(10) + chr(13))
                        got_serial_data = True
                    elif "P" in str(req):
                        buffer.append("OK" + chr(10) + chr(13))
                        got_serial_data = True
                    else:
                        ''' --- we got real tcp data, writeln to serial'''
                        print("+++ got tcp data: %s" % req)
                        output_msg = str(req) + chr(10) + chr(13)
                        got_serial_data = True

                    if got_serial_data:
                        serial.write(output_msg)
                        print("+++ wrote serial data {}".format(output_msg))
                        time.sleep(0.5)
                        got_serial_data = False

                else:
                    print('No data: connection closed by the client?')
                    if client_s:
                        client_s.close()
                    global timer5
                    ''' --- stop timer -> serial data aquisition'''
                    timer5.deinit()
                    #raise ClientDisconnected
                    break
            except Exception as ex:
                '''--- only catch no tcp data'''
                # print("*** tcp-exception: {} ".format(ex, client_addr))
                # print("*** no tcp data")
                pass

            # --- we have a connection, get serial data and send towards client
            # --- let timers execute to gain serial data
            time.sleep(1)
            done = False
            # --- serial data should be collected in timer tick
            if buffer:
                ''' --- we have serial data, send to client'''
                if len(buffer) > 0:
                    print("buffer-len: %d" % len(buffer))
                    for i in range(len(buffer)):
                        print(buffer[i])
                        if client_s:
                            ba = bytearray()
                            ba.extend(buffer[i])
                            client_s.sendall(ba)
                            print("==> sending serial content to client: %s" % buffer[i])
                            done = True
                        i += 1
            else:
                # print("*** no serial data.")
                pass

            # --- when sent to client, reset buffer
            if done:
                buffer.clear()

            # print("............................")


if __name__ == '__main__':
    # try:
    main()
    # except Exception as e:
    #    print ("!!! Main: exception caught: {} ".format(e))
    # finally:
    #    '''clean up'''
    #    if timer5:
    #        timer5 = None

'''exit to console or blink error-led?'''
sys.exit(0)
