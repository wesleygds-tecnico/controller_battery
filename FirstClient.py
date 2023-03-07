import socket
import time

## --------------------------------------------------------------------------------------- ##
## ----------------------------- First Connection ---------------------------------------- ##
## --------------------------------------------------------------------------------------- ##

HOST = socket.gethostname()
print(HOST)
PORT_0 = 50000

s_0 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_0.bind(('',PORT_0))

s_0.listen()
print("Waiting for client 1")

conn_0, ender_0 = s_0.accept()
print('Conexao aceita')

Message_0 = 'Who'
Message_0_str = str.encode(Message_0)

## --------------------------------------------------------------------------------------- ##
## ---------------------------- Second Connection ---------------------------------------- ##
## --------------------------------------------------------------------------------------- ##

PORT_1 = 50001

s_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_1.bind(('',PORT_1))

s_1.listen() 
print("Waiting for client 2")

conn_1, ender_1 = s_1.accept()
print('Conexao aceita')

Message_1 = 'Who'
Message_1_str = str.encode(Message_1)

## --------------------------------------------------------------------------------------- ##
## ---------------------------- Second Connection ---------------------------------------- ##
## --------------------------------------------------------------------------------------- ##

while True:
    conn_0.send(Message_0_str)
    Answer_0 = conn_0.recv(1024)
    print(Answer_0)

    time.sleep(1)

    conn_1.send(Message_1_str)
    Answer_1 = conn_1.recv(1024)
    print(Answer_1)

    time.sleep(1)