import socket
import json
import time
import math
import struct
from InverterCommands import Modbus
from mqtt_SSOP import clientSubscriber


###--------------------------------------------------###
##------------------- MQTT Connection ----------------##
###--------------------------------------------------###

CloudOrders = []

clientSubscriber.subscribe('toAsset/123',CloudOrders,'0')

###--------------------------------------------------###
##------------------ Modbus Connection ---------------##
###--------------------------------------------------###
"""
SMA1 = Modbus("169.254.12.3")
print('Connecta no inversor')
"""
###--------------------------------------------------###
##------------- TCP Real Time Connection PC ----------##
###--------------------------------------------------###

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

PGRq = 0
Pbat = 0

x_time = []
y_PCon = []
y_PPV = []
y_PbatRq = []
y_PGRq = []
y_SoC = []
y_SoCMin = []

ReqtTime = time.ctime(time.time())

HistoryHeader = ['F',',','LP',',','PPS',',','id',',','Cap',',','PDMax',',',
                    'PCMax',',','RT',',','AT',',','PCon',',','PPV',',','Pbat',
                    ',','PG',',','SoC',',','SoCMin']

History = open("History.txt",'w')
History.writelines(HistoryHeader)
History.write("\n")

BatteryCapacity = 5400*3600
SoC = 100
TimeStep = 1 #min

SoCMin = 40
PDMax = 10000
PCMax = -5000

f = open('Consume.txt','r')
lines = f.readlines()
PCon_total = []
for x in lines:
    PCon_total.append(x.split(',')[8])
f.close()

PCon_total.remove(PCon_total[0])
Threshold = len(PCon_total)

for i in range(0,1440):
    if float(PCon_total[i]) > 870:
        PCon_total[i] = float(PCon_total[i])/7
    if float(PCon_total[i]) > 870:
        print(PCon_total[i])

f = open('SolarProduction.txt','r')
lines = f.readlines()
PPV_total= []
for x in lines:
    PPV_total.append(x.split(',')[8])
f.close()

PPV_total.remove(PPV_total[0])

for i in range(0,1440):
    if float(PPV_total[i]) > 870:
        PPV_total[i] = float(PPV_total[i])/7
    if float(PPV_total[i]) > 870:
        print(PPV_total[i])

PCon = []
PPV = []

for j in range(0,math.floor(len(PCon_total)/TimeStep)):
    PCon.append(float(PCon_total[j*TimeStep]))

for j in range(0,math.floor(len(PPV_total)/TimeStep)):
    PPV.append(float(PPV_total[j*TimeStep]))



"""
SMA1.sendP(int(PPV[i]))
s2.send(struct.pack("i",PbatRq))
"""
i = 0
Threshold = len(PCon)
time.sleep(3)
f = open('History.txt','w')

while i < Threshold-1:
#while time.ctime(time.time()) < TimeToEnd:

   #SMA1.sendP(int(PPV[i]))

    message = ConnPC.recv(2048)
    #SoC = list(s2.recv(1024))

    #SoC = (SoC*BatteryCapacity/100 - Pbat*60*TimeStep)*100/BatteryCapacity

    if (SoC<=100 and (not PCon[i] >= PPV[i])) or (SoC>SoCMin and PCon[i] >= PPV[i]):
        PbatRq = PCon[i] - PPV[i]
        if PbatRq >= PDMax:
            PbatRq = PDMax
        if PbatRq <= PCMax:
            PbatRq = PCMax
    if SoC < SoCMin and PbatRq >= 0:
            PbatRq = 0
    if SoC > 100 and PbatRq < 0:
        PbatRq = 0

    if (SoC>SoCMin and (not PCon[i] >= PPV[i]) and (PPV[i] - PCon[i] > PCMax)) or (SoC> SoCMin and (not SoC < 100) and (not PCon[i] >= PPV[i])) or (PCon[i] >= PPV[i] and PCon[i] > PPV[i] + PDMax) or (PCon[i] >= PPV[i] and (not SoC > SoCMin)) or (SoC>SoCMin and (PCon[i] > PPV[i] + PDMax) and (not SoC < 100)):
        PGRq = PCon[i] - PbatRq

    if PbatRq == 0:
        PGRq = PCon[i] - PPV[i]

    if PbatRq < 0:
        PGRq = 0

    if PCon[i] <= PPV[i] + PbatRq and PbatRq > 0:
        PGRq = 0

    Pbat = PbatRq

    #time.sleep(8)
    #SMA1.initialRun()

    #InvStatus = SMA1.return_dict()

    #print(time.ctime(time.time()), "%.1f  %.1f %.1f %.1f %.1f %.1f" % (PCon[i], PPV[i], PbatRq, PGRq, SoC, SoCMin))
   
    Response = {'F': "Self Consumption",
                        'LP': " ",
                        'PPS': " ",
                        'id': " ",
                        'Cap': " ",
                        'PDMax': " ",
                        'PCMax': " ",
                        'RT': ReqtTime,
                        'AT': i*TimeStep,
                        'PCon': PCon[i],
                        'PPV': PPV[i], #float(InvStatus['Power_Active']),
                        'Pbat': Pbat,
                        'PG': PGRq,
                        'SoC': SoC,
                        'SoCMin': SoCMin}

    Response = json.dumps(Response)

    ConnPC.send(str.encode(Response))

    data = json.loads(Response)

    """
    print('Erro entre comando e leitura: ', float(InvStatus['Power_Active'])-PPV[i])
    print('Valor da leitura: ', float(InvStatus['Power_Active']))
    print('Corrente em leitura: ', float(InvStatus['DC1_Current']))
    print('\n')
    """
    
    HistoryData = [str(data["F"]), ',', str(data["LP"]), ',', str(data["PPS"]), ',', str(data["id"]), ',', str(data["Cap"]), ',', str(data["PDMax"]), ',', str(data["PCMax"]), ',', str(data["RT"]), ',', str(data["AT"]), ',', str(data["PCon"]), ',',  PPV[i], """str(InvStatus['Power_Active']),""" ',',  str(data["Pbat"]), ',', str(data["PG"]), ',', str(data["SoC"]), ',', str(data["SoCMin"])]

    i = i + 1
    f.writelines(HistoryData)
    f.write("\n")

    #SMA1.sendP(int(PPV[i]))
    #s2.send(struct.pack("i",PbatRq))
    time.sleep(3)
f.close()