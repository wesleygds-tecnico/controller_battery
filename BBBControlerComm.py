import socket
import json
import struct
from mqtt_SSOP import clientSubscriber
from InverterCommands import Modbus

###--------------------------------------------------###
##------------------- MQTT Connection ----------------##
###--------------------------------------------------###

f = open('CloudOders.txt','w')

def Initialize():
    Header = ['Function',',','Begin',',','Limit Power']
    f.writelines(Header)
    #f.writelines(str(CloudOrders))
    #clientSubscriber.subscribe('toAsset/123',CloudOrders,'0')
    f.write("\n")
    return f

Initialize()

CloudOrders = []

def ConnectCloud(CloudOrders,f):
    CloudOrders0 = CloudOrders
    #clientSubscriber.subscribe('toAsset/123',CloudOrders,'0')
    CloudOrders = {
        'Function': 'Self-Consumption',        
        'Begin': 'Thu Jan 20 18:11:00 2024'
    }
    print(CloudOrders)
    if CloudOrders0 != CloudOrders:
        CloudOrders_write = [CloudOrders["Function"], ",", CloudOrders["Begin"], ",", "", ",", ""]
        f.writelines(CloudOrders_write)
        #f.writelines(str(CloudOrders))
        f.write("\n")
        f.close()
    return CloudOrders

ConnectCloud(CloudOrders, f)

ReqTime = []
ReqService = []

def CloudObeyOrder():
    f = open('CloudOders.txt','r')
    lines = f.readlines()
    for x in lines:
        ReqService.append(x.split(',')[0][:])
    f.close()
    print(ReqService[:][1])
    Function = ReqService[:][1]
    for x in lines:
        ReqTime.append(x.split(',')[1][:])
    f.close()
    print(ReqTime[:][1])
    Begin = ReqTime[:][1]
    return Function, Begin

CloudObeyOrder()

###--------------------------------------------------###
##------------------ Modbus Connection ---------------##
###--------------------------------------------------###

def InitializeInv():
    SMA1 = Modbus("169.254.12.3")
    print('Connecta no inversor')    
    return SMA1

"""
SMA1 = Modbus("169.254.12.3")
print('Connecta no inversor')
"""
###--------------------------------------------------###
##------------- TCP Real Time Connection PC ----------##
###--------------------------------------------------###

def InitializePC():

    #Initialization Code

    HOST = socket.gethostname()
    print(HOST)
    PORT = 50000

    s0 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s0.bind(('',PORT))

    s0.listen()
    print("Waiting for client connection")

    ConnPC, ender = s0.accept()

    return ConnPC, ender, s0

'''
HOST = 'LAPTOP-675SSOQC'
PORT = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
'''

HOST = socket.gethostname()
print(HOST)
PORT = 50000

s0 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s0.bind(('',PORT))

s0.listen()
print("Waiting for client connection")

ConnPC, ender = s0.accept()

###--------------------------------------------------###
##-------------- TCP Real Time Connection Battery ------------##
###--------------------------------------------------###

def IntializeBat():

    HOST = '169.254.12.242'
    PORT = 2001

    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Conectando Bateria')
    s1.connect((HOST, PORT))
    print('Inicializando Bateria')

    data = s1.recv(1024) #Resposta
    data = list(data)
    value = struct.unpack("<hhh", bytearray(data))
    PDMax = value[2]
    PCMax = value[1]

    print('Bateria inicializada')
    
    PORT = 2000

    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.connect((HOST, PORT))
    print('Bateria pronta para serviço')

    PbatRq = 0

    f = open('History.txt','w')

    history_header = ['F','LP','PPS','id','Cap','PDMax','PCMax','RT','AT','PCon','PPV','Pbat','PG','SoC','SoCMin']
    file_name = "HistoryServer.csv"

    print('Conexao aceita')

    return s1, PDMax, PCMax, PbatRq

'''

HOST = 'LAPTOP-675SSOQC'
PORT = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
'''
"""
HOST = '169.254.12.242'
PORT = 2001

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.connect((HOST, PORT))
print('Connected')

data = s1.recv(1024) #Resposta
data = list(data)
value = struct.unpack("<hhh", bytearray(data))
PDMax = value[2]
PCMax = value[1]
"""
###--------------------------------------------------###
##-------------- TCP Real Time Connection Battery ------------##
###--------------------------------------------------###

'''

HOST = 'LAPTOP-675SSOQC'
PORT = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
'''
"""
PORT = 2000

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect((HOST, PORT))
print('Connected')

PbatRq = 0

f = open('History.txt','w')

history_header = ['F','LP','PPS','id','Cap','PDMax','PCMax','RT','AT','PCon','PPV','Pbat','PG','SoC','SoCMin']
file_name = "HistoryServer.csv"

print('Conexao aceita')
"""