import select
import socket
import machine
import sys
# import connect_jsi_main
from time import sleep


class Ser2TcpServer():
    """Telnet server"""

    def __init__(self, serial, log=False):
        self._log = log
        print("*** init: constructor ->")
        print("*** init: Server runs on 0.0.0.0:23")
        address = ('0.0.0.0', 23)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("*** init: Opts?")
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("*** init: Bind")
        self._socket.bind(address)
        print("*** init: Bind done.")
        self._socket.listen(1)
        print("*** init: Listening on ", address)
        self._connection = None
        self._serial = serial  # --- initialized in connect
        self._client_ip = None
        print("*** init: prepare connect.")
        self._client_connect()
        print("*** <- init: constructor ")
        print("*** init: done..\n")

    def __del__(self):
        self.close()

    def _serial_connect(self):
        """Serial stuff"""
        if self._serial:
            print("*** UART connected.")
            return True
        try:
            print("*** UART init.")
            self._serial = serial.init(115200, bits=8, parity=None, stop=1)
        except OSError as err:
            print("*** Serial %s is not connected %s",
                  "UART_1: 115200, bits=8, parity=None, stop=1", err)
            return False
        print("*** UART_1 connect success.")
        return True

    def _client_connect(self):
        """ establish tcp client connection"""
        print("*** waiting for client connect.")
        connection, client_ip = self._socket.accept()
        connection.setblocking(0) 
        self._connection = connection
        self._client_ip = client_ip
        # print("*** client connect." + client_ip)
        if not self._serial:
            if not self._serial_connect():
                print("Client connection canceled: %s:%d. Reason: Serial failed.", connection, client_ip)
                self._connection.close()
                return
        print("*** client accepted and serial ready.")

    def close(self):
        if self._connection is not None:
            self._connection = None
        if self._socket is not None:
            self._clients_disconnect()
        return

    def _clients_disconnect(self):
        """tcp client disconnect"""
        print("*** _clients_disconnect: close connection")
        self._connection.close()
        print("*** Exiting.. socket is None.")
        self._socket = None

    def on_tcp_received(self, data):
        """process received tcp data"""
        print('*** on_tcp_received: transfer to serial => %s' % data)
        # data = str(data) + chr(13) + chr(10)
        data = data.decode("utf-8") + chr(13) + chr(10)

        if data:
            self._serial.write(data)

    def send(self, data):
        """process received serial data, send serial data back to client"""
        print('*** send: sending data back to the client => %s' % data)
        done = False
        if data:
            b = bytearray()
            b.extend(data)
        try:
            # ---------------------
            self._connection.sendall(b)
            # ---------------------
            print("send: ok, after sendall.")
            done = True
        # except OSError as err:
        #    if err.args[0] not in [err.errno.EINPROGRESS, err.errno.ETIMEDOUT]:
        #        print('### send: Error sending', err)
        #    done = False
        except Exception as e:
            done = False
            print("*** Exception-Error in send: => {}  :-( ".format(e))
            return
        finally:
            if done:
                print("*** send ok: => {}  :-( ".format(data))
            else:
                print("*** Exception-Error in send: => {}  :-( ".format(e))

    def process(self):
        """process logic"""
        print("*** enter process ->")

        self._connection.settimeout(100)
        # self._socket.socket_setblocking(0)

        print("*** process: socket receive. Waiting for data...")
        data = self._connection.recv(1024)

        print("+++ process: socket received: {}".format(data))
        if not data:
            # print("*** no_data,  remove.")
            # self._clients_disconnect()
            return

        # if data == "b''":
        if not data: 
            '''ignore empty string'''
            sleep(2)
            return
        # --- send tcp-data to UART_1
        self.on_tcp_received(data)

        sleep(1)

        serial_data = None
        try:
            print("*** process: get serial data (readline!).")
            serial_data = self._serial.readline()  # --- expecting CR
            print("*** process: got serial data: %s." % serial_data)
        except Exception as e:
            print("*** process: Exception while get serial, disconnect clients %s" % e)
            self._clients_disconnect()
            serial_data = None

        if serial_data is not None:
            print("*** process: sock-send serial data (%s)" % serial_data)
            # self.send(bytes('%s\r\n' % serial_data, 'utf8'))
            self.send(serial_data)
            serial_data = ""
        else:
            print("*** process: no serial data available.")
        print("*** <- process done. ")

def main():
    """WLAN access and initiate process loop"""
    # --- serial access
    print("*** running in (%s)" % __name__)
    net2ser = Ser2TcpServer(serial=machine.UART(1, 115200), log=True )
    try:
        '''perform endlessly'''
        while True:
            net2ser.process()

    except OSError as err:
        print(" :-( OS-Error in MAIN: => {}".format(err))
        # if err.args[0] != errno.EINPROGRESS:
        #     raise
    except Exception as e:
        print("*** Exception-Error in MAIN: => {}  :-( ".format(e))

    finally:
        sys.exit(0)


if __name__ == '__main__':

    print("\n\n*** Register @WLAN before executing main.")
    # connect_jsi_main.main()
    print("\n\n*** WLAN connected sucessfully.")
    print("\n\n*** Execute main now.")
    main()
