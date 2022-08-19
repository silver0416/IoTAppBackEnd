import socket
import traceback
from KasaSmartPowerStrip import SmartPowerStrip
import time
from datetime import datetime


HOST = '192.168.0.15'
PORT = 7560


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)

print('server start at: %s:%s' % (HOST, PORT))
print('wait for connection...')

def remove_upprintable_chars(s):
    #移除所有不可见字符
    return ''.join(x for x in s if x.isprintable())

while True:
    conn, addr = s.accept()
    print('connected by ' + str(addr))
    now = datetime.now()
    print(now.strftime("%d/%m/%Y %H:%M:%S"))

    while True:
        try:
            print(0)
            indata = conn.recv(1024)
            print(1)
            power_strip = SmartPowerStrip('192.168.0.11')
            info = ""
            for i in range(6):
                print(power_strip.get_plug_info(i+1)[0].get("state"))
                info += str(power_strip.get_plug_info(i+1)[0].get("state"))

            #indata = conn.recv(1024)
            print(2)
            print("indeta:",type(indata))
            if len(indata) == 0: # connection closed    
                conn.close()
                print('client closed connection.')
                break
            outdata = info
            print(3)
            outdata = bytes(outdata, 'UTF-8')
            conn.send(outdata)
            print(4)
            conn.close()
            print('client closed connection.')
            time.sleep(1)

        except:
            break
