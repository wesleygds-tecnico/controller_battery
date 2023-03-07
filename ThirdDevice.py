import socket
import json
import time

# --------------------------------------------------------------- #
# ----------- No BeagleBone para comunicar com a bateria -------- #
# --------------------------------------------------------------- #
"""
HOST_BBB = socket.gethostname()
print(HOST_BBB)
PORT_BBB = 50001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',PORT_BBB))

s.listen()
print("Waiting for client connection")

while True:
    conn, ender = s.accept()

"""

# --------------------------------------------------------------- #
# ----------- Na bateria para comunicar com o BeagleBone -------- #
# --------------------------------------------------------------- #

#HOST = '192.168.7.2'
HOST = socket.gethostname()
PORT = 50001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

print('Connected')
Message = 'Connected to devide 3'
    
while True:
    Answer = s.recv(2048)
    print('Das ist des Servers Nachricht: ', Answer)

    s.send(str.encode(Message))
    print('Hier ist ein Client Nachricht: ', Message)

    time.sleep(1)