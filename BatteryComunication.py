import socket
import time
import struct

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
    message = conn.recv(2048)
    response = {"response": "ok"}
    response = json.dumps(response)
    response = str.encode(response)
    time.sleep(0.50)
    conn.sendall(response)
    data = json.loads(message)
    print(data)

"""

# --------------------------------------------------------------- #
# ----------- Inicialização -------- #
# --------------------------------------------------------------- #

HOST_BBB = '169.254.12.242'
#HOST_BBB = '192.168.7.2'
PORT = 2001

s_Bat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_Bat.connect((HOST_BBB, PORT))
print('Connected')

data = s_Bat.recv(1024) #Resposta
print(data)
data = list(data)
print(data)
value = struct.unpack("<hhh", bytearray(data))
print(value)



# --------------------------------------------------------------- #
# ----------- Na bateria para comunicar com o BeagleBone -------- #
# --------------------------------------------------------------- #

HOST_BBB = '169.254.12.242'
#HOST_BBB = '192.168.7.2'
PORT = 2000

s_Bat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_Bat.connect((HOST_BBB, PORT))
print('Connected')



"""
Message_1 = {'Who': 'Device 1'}
Message_1_json = json.dumps(Message_1)
Message_1_str = str.encode(Message_1_json)

#250000Ah
#+-48V
#

Message_2 = '-300'
#Message_2_json = json.dumps(Message_2)
Message_2_str = str.encode(Message_2)


Message_3 = 10
Message_3_bytes = bytes(str(Message_3), encoding="UTF-8")


Message_4 = 1
print(type(str(Message_4)))
Message_4_bytes = bytes(str(Message_4), encoding="UTF-8")
print(type(Message_4_bytes))

Message_5 = int('0101010101010101',2).to_bytes(2, byteorder='big')
"""

#Message_6 = 2000
#packer = struct.Struct('I')
#Message_6_data = packer.pack(*Message_6)
#Message_6_bytes = Message_6.to_bytes(4, 'big')
#Message_6_bytes = struct.pack("I", bytearray(int(Message_6)))
#Message_6_bytes = struct.pack("i", Message_6)

Message_6 = 100

while True:
    """
    s_Bat.send(Message_1_str) #ok
    data = s_Bat.recv(1024) #Resposta
    print(data)
    time.sleep(1)
    
    
    s_Bat.send(Message_2_str) #ok
    data = s_Bat.recv(1024)
    print(data)
    time.sleep(1)
    
    
    s_Bat.send(Message_3_bytes) #ok
    data = s_Bat.recv(1024)    
    print(data)
    time.sleep(1)

    s_Bat.send(Message_4_bytes) #ok
    data = s_Bat.recv(1024)    
    print(data)
    time.sleep(1)
"""
    
    Message_6_bytes = struct.pack("i", Message_6)
    print(Message_6)

    s_Bat.send(Message_6_bytes) #ok
    data = s_Bat.recv(1024) #Resposta
    #print(data)
    data = list(data)
    value = struct.unpack("<h", bytearray(data))[0]/100
    print(value)
    time.sleep(0.5)

    Message_6 = Message_6 + 50 #positivo a carregar
    #Negativo a descarregar


"""
    s_Bat.send(Message_5)
    data = s_Bat.recv(1024)
    print(data)
    time.sleep(1)
"""


"""
    Message = {'Cap': " ",
                'PDMax': " ",
                'PCMax': " ",
                'Pbat': " ",
                'PG': " ",
                'SoC': " ",
                'SoCMin': " "}
        
    Message = json.dumps(Message)

    s_Bat.sendall(str.encode(Message))
    data = s_Bat.recv(2048)
"""