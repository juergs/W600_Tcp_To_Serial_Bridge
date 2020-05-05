import binascii
import network
import time
import w600

def main():
	print("*** Connecting to WLAN-AP and establih a FTP-server on port 21 user=root password=root")
	print("*** Returning the sta_if object for disconnect() of WLAN")
	sta_if = network.WLAN(network.STA_IF)
	sta_if.active(True)
	sta_if.connect("<Your SSID>", "<Your WLAN-password>")
	time.sleep(5)
	sta_if.isconnected()
	print("***connected, ip is " + sta_if.ifconfig()[0])

	'''if FTP server isn't needed, comment this '''	
	w600.run_ftpserver(port=21, username="root", password="root")
	print("***FTP-server on port 21 user=root password=root IP=" + sta_if.ifconfig()[0])
	return sta_if
	
def disconnect():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.disconnect()	

if __name__ == "__main__":
    main()
