import socket
import traceback
from KasaSmartPowerStrip import SmartPowerStrip

power_strip = SmartPowerStrip('192.168.0.19')

HOST = '192.168.0.10'
PORT = 7557


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

    while True:
        try:
            indata = conn.recv(1024)
            #print("do sth")
            if len(indata) == 0: # connection closed    
                conn.close()
                print('client closed connection.')
                break
            print("rev:"+indata.decode())
            print(type(indata.decode()))
            print("repr:",repr(indata.decode('UTF-8').strip()))
            print("after remove",remove_upprintable_chars(indata.decode('UTF-8')))
            indata = remove_upprintable_chars(indata.decode('UTF-8'))
            if indata == "on" or indata == "off":
                print("switch",indata)
                power_strip.toggle_plug(indata, plug_num=1)
                power_strip.toggle_plug(indata, plug_num=2)
                power_strip.toggle_plug(indata, plug_num=3)
                power_strip.toggle_plug(indata, plug_num=4)
                power_strip.toggle_plug(indata, plug_num=5)
                power_strip.toggle_plug(indata, plug_num=6)

            outdata = 'echo ' + indata.decode()
            conn.send(outdata.encode())

        except:
            break
