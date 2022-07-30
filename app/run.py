from multiprocessing.connection import wait
import os
import socket
import threading
from IoTAppBackEnd.database import account

def django_server():
    os.system("python manage.py runserver 0.0.0.0:8701")


def signupServer():
    HOST = '0.0.0.0'
    PORT = 7557


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)

    print('server start at: %s:%s' % (HOST, PORT))
    print('wait for connection...')

    while True:
        conn, addr = s.accept()
        print('connected by ' + str(addr))
        t = 0
        user = []
        while True:
            try:
                print(t)
                indata = conn.recv(4096)
                user.append(indata.decode('utf-8'))
                if len(indata) == 0: # connection closed
                    conn.close()
                    print('client closed connection.')
                    account.update_password(user[0], user[1])
                    break
                else :
                    t+=1
                    print(user)
            except:
                break
def loginServer():
    HOST = '0.0.0.0'
    PORT = 7558


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)

    print('server start at: %s:%s' % (HOST, PORT))
    print('wait for connection...')
    while True:
        conn, addr = s.accept()
        print('connected by ' + str(addr))
        t = 0
        user = []
        while True:
            try:
                print(t)
                if t == 2: # connection closed
                    if (account.login(user[0], user[1]) == True):
                        print('login success')
                        conn.send(b't')
                    else:
                        print('login failed')
                        conn.send(b'f')
                    conn.close()
                    print('client closed connection.')
                    break
                    
                else :
                    indata = conn.recv(4096)
                    user.append(indata.decode('utf-8'))
                    t+=1
                    print(user)
            except:
                break
#put thread in here
threading.Thread(target=signupServer).start()
threading.Thread(target=loginServer).start()
#----------------------------------------------------------------------------------------------------------------------
threading.Thread(target=django_server).start()



