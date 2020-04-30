# W600_Tcp_To_Serial_Bridge
TCP-Server for serial bridging over WLAN for WEMOS W600
Some infos to W600-Processor and AirW602-Board:
https://github.com/SeeedDocument/W600_Module/tree/master/res

Module Air602: https://www.seeedstudio.com/Air602-WiFi-Module.html
Development-Board: https://www.seeedstudio.com/Air602-WiFi-Development-Board.html
Specs and documents: http://www.winnermicro.com/en/html/1/156/158/536.html

Other Boards (to be done):

How-To:
The Module Air602 will be delivered with a AT-command firmware, which in my opinion is completly waste of time using it. ;-(

Micropython image from Winner:
http://www.winnermicro.com/en/upload/1/editor/1573450100756.zip

Image sources:
http://www.winnermicro.com/en/upload/1/editor/1573450104930.zip

Manual "Micropython-User Guide":
http://www.winnermicro.com/en/upload/1/editor/1573450100546.pdf

Micropython_Lib:
https://github.com/micropython/micropython-lib

Get started with Wemos W600:
https://docs.wemos.cc/en/latest/tutorials/w600/get_started_with_micropython_w600.html

Bootloader+AT-Firmware: https://download.w600.fun/?dir=firmware

Tutorials: https://yoursunny.com/t/2018/Air602-blink/
           https://yoursunny.com/t/2018/Air602-weather/


There would be two modes on programming Micropython to the board:
So, first action is to reprogram the board's firmware using this pyton-upload-script from here:
https://github.com/vshymanskyy/w600tool

Usage: 
python3 "D:\Air602\_software\w600tool-0.1\w600tool.py" -p COM15 --upload-baud 115200 --upload "D:\Air602\_firmware\W60x_MicroPython_1.10_B1.5_img\W60X_MicroPython_1.10_B1.5_img\1M_Flash\wm_w600_gz.img"

This will erase the AT-Firmware install the Micropython not persistent on the board.
Bootloader is not touched.. After Reset there will be only SECBOOT-Boatloader present and printints via connected 
serial adapter "

This Sample shows upload from an Arduino build inside Arduino-IDE via "Upload"-process:
See https://forum.seeedstudio.com/t/arduino-integration-via-boardmanager-fails-installing-board-type-w600/251387
and https://github.com/juergs/w600-arduino_upload-workaround

C:\Users\js\AppData\Local\Temp\arduino_build_131628>python3 “D:\Air602_software\w600tool-0.1\w600tool.py” -p COM15 --upload C:\Users\js\AppData\Local\Temp\arduino_build_131628/sketch_apr16a.ino.gz.img --upload-baud 115200
Opening device: COM15
Uploading C:\Users\js\AppData\Local\Temp\arduino_build_131628/sketch_apr16a.ino.gz.img
0% [##############################] 100% | ETA: 00:00:00
Total time elapsed: 00:00:27
Reset board to run user code…

If Arduino is your preferred programming tool:
if you want to download and install the board definition of W600.

    add W600 board manager URL from File -> Preference
    copy and paste the link https://raw.githubusercontent.com/salmanfarisvp/snippet/master/package_wmcom_index.json
    open Board Manager Tools -> Board -> Board Manager
    search for W600 and click install.
    
    




