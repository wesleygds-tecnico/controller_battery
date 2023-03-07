###-------------------------------------------------------------------###
##------------------------ Importing libraries ------------------------##
###-------------------------------------------------------------------###

import socket
import json
import time
import math
from InverterCommands import Modbus

###-------------------------------------------------------------------###
##------------------------ Variables definition -----------------------##
###-------------------------------------------------------------------###

PGRq = 0
Pbat = 0

x_time = []
y_PCon = []
y_PPV = []
y_PbatRq = []
y_PGRq = []
y_SoC = []
y_SoCMin = []

BatteryCapacity = 5400*3600
SoC = 100
TimeStep = 1 #min

SoCMin = 40
PDMax = 10000
PCMax = -5000

PCon = []
PPV = []

###-------------------------------------------------------------------###
##-------------------- Begins to write the history --------------------##
###-------------------------------------------------------------------###

TimeToEnd = "Thu Jan 20 18:11:00 2024"
ReqtTime = time.ctime(time.time())

HistoryHeader = ['F',',','LP',',','PPS',',','id',',','Cap',',','PDMax',',',
                    'PCMax',',','RT',',','AT',',','PCon',',','PPV',',','Pbat',
                    ',','PG',',','SoC',',','SoCMin']

History = open("History.txt",'w')
History.writelines(HistoryHeader)
History.write("\n")

###-------------------------------------------------------------------###
##-------------- Access the data bases creating lists -----------------##
###-------------------------------------------------------------------###

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


###-------------------------------------------------------------------###
##------ Prepare data for control script with suitable resolution -----##
###-------------------------------------------------------------------###

for j in range(0,math.floor(len(PCon_total)/TimeStep)):
    PCon.append(float(PCon_total[j*TimeStep]))

for j in range(0,math.floor(len(PPV_total)/TimeStep)):
    PPV.append(float(PPV_total[j*TimeStep]))

Threshold = len(PCon)

###-------------------------------------------------------------------###
##------------------- Inversor Modbus Connection ----------------------##
###-------------------------------------------------------------------###

SMA1 = Modbus("169.254.12.3")
print('Connecta no inversor')


###-------------------------------------------------------------------###
##-------------------- TCP Real Time Connection -----------------------##
###-------------------------------------------------------------------###

'''

HOST = 'LAPTOP-675SSOQC'
PORT = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
'''

HOST = socket.gethostname()
print(HOST)
PORT = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',PORT))

s.listen()
print("Waiting for client connection")

conn, ender = s.accept()
print('Conexao aceita')

###-------------------------------------------------------------------###
##---------------------- Prepare history file -------------------------##
###-------------------------------------------------------------------###

history_header = ['F','LP','PPS','id','Cap','PDMax','PCMax','RT','AT','PCon','PPV','Pbat','PG','SoC','SoCMin']
file_name = "HistoryServer.csv"

f = open('History.txt','w')

###-------------------------------------------------------------------###
##------------------------ Control Loop -------------------------------##
###-------------------------------------------------------------------###

i = 0

SMA1.sendP(int(PPV[i]))
time.sleep(8)

while i < Threshold-1:
#while time.ctime(time.time()) < TimeToEnd: #breaking criteria follows time dependency

   #SMA1.sendP(int(PPV[i]))

    message = conn.recv(2048)

    SoC = (SoC*BatteryCapacity/100 - Pbat*60*TimeStep)*100/BatteryCapacity

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
    SMA1.initialRun()

    InvStatus = SMA1.return_dict()

    #print(time.ctime(time.time()), "%.1f  %.1f %.1f %.1f %.1f %.1f" % (PCon[i], PPV[i], PbatRq, PGRq, SoC, SoCMin))
    
    """
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
                        'PPV': PPV[i],
                        'Pbat': Pbat,
                        'PG': PGRq,
                        'SoC': SoC,
                        'SoCMin': SoCMin}
    """
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
                        'PPV': float(InvStatus['Power_Active']),
                        'Pbat': Pbat,
                        'PG': PGRq,
                        'SoC': SoC,
                        'SoCMin': SoCMin}

    Response = json.dumps(Response)

    conn.send(str.encode(Response))

    data = json.loads(Response)
    print('Erro entre comando e leitura: ', float(InvStatus['Power_Active'])-PPV[i])
    print('Valor da leitura: ', float(InvStatus['Power_Active']))
    print('Corrente em leitura: ', float(InvStatus['DC1_Current']))
    print('\n')

    HistoryData = [str(data["F"]), ',', str(data["LP"]), ',', str(data["PPS"]), ',', str(data["id"]), ',', str(data["Cap"]), ',', str(data["PDMax"]), ',', str(data["PCMax"]), ',', str(data["RT"]), ',', str(data["AT"]), ',', str(data["PCon"]), ',',  str(InvStatus['Power_Active']), ',',  str(data["Pbat"]), ',', str(data["PG"]), ',', str(data["SoC"]), ',', str(data["SoCMin"])]
    i = i + 1
    f.writelines(HistoryData)
    f.write("\n")
    SMA1.sendP(int(PPV[i]))
    time.sleep(3)
f.close()
