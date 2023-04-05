# %% 

# some_file.py
import socket
import json
import time
import math
import struct
from InverterCommands import Modbus
"""
import DataBase.Biblioteca.clientSubscriber as subscriber
import threading
import gCentralComponentDB as DB
from datetime import datetime

#from mqtt_SSOP import clientSubscriber

# %% 

###--------------------------------------------------###
##------------------- MQTT Connection ----------------##
###--------------------------------------------------###

CloudOrders = {
    "lastMessage": "Not modified",
    "id": 0
}

ReqTime = []
ReqService = []
TimeStep = 1
SoCMin = 40

date = datetime.now().isoformat()

data = {
    'Type_Of_Service' : "date",
    'Type_Of_Activation' : date,
    'Price' : date,
    'Price_Min' : date,
    'Price_Max' : date,
}

data2 ={
    'meter_ID' : 1,
    'measure_ID' : 1,
    'timestamp' : date,
    'type' : 1,
    'n_Phases' : 1,
    'chanel' : 1,
    'unit' : 1,
    'multi_Factor' : 1,
    'measure_1' : 1,
    'measure_2' : 1,
    'measure_3' : 1,
}

def Initialize(CloudOrders, f):
    print("%--------------- Initialization ------------------%")
    #Header = ['Function',',','Begin',',','Limit Power']
    #f.writelines(Header)
    #f.write("\n")
    subThread = threading.Thread(target=lambda: subscriber.subscribe('toAsset/123',CloudOrders,'0'))
    subThread.start()
    print("Thread initiated")

    #print("Initialization of Orders DBCLC Concluded")
    time.sleep(5)
    print("CloudOrders: ", CloudOrders)

    print("%--------------- Initialization ------------------%")
    print("\n")

    print("%--------------- Writing on DataBase ------------------%")

    DB.newPayload(topic = "pVGeneratorData", iotDeviceID = "iotDeviceID", dataType = "dataType", data = data2) 
    
    #DataType identificação da tabela
    #Mensagem do MQTT
    #

    A = DB.listDataByID(1)
    B = DB.row2dict(A)
    print(B)

    A = DB.listDataByTopic("pVGeneratorData")
    B = DB.table2dict(A)
    print(B)

    print("%--------------- Writing on DataBase ------------------%")        
    return f, #ConnectCloud(CloudOrders, f)

def ConnectCloud(CloudOrders,f):
    print("%--------------- Connecting to Cloud ------------------%")

    CloudOrders0 = CloudOrders
    #clientSubscriber.subscribe('toAsset/123',CloudOrders,'0')
    print("Connected to Cloud")
    CloudOrders = {
        'Begin': 'Thu Jan 20 18:11:00 2023',
        'Function': 'Self-Consumption',
        'Limit Power': ' '
    }
    print(CloudOrders)
    if CloudOrders0 != CloudOrders:
        CloudOrders_write = [CloudOrders["Begin"], ",", CloudOrders["Function"], ",", CloudOrders["Limit Power"]]
        f.writelines(CloudOrders_write)
        #f.writelines(str(CloudOrders))
        f.writelines("\n")
        f.close()
        print("New Order Received")
    print("%--------------- Connecting to Cloud ------------------%")

    return CloudOrders, CloudGetOrder()



def CloudGetOrder():
    f = open('CloudOders.txt','r')
    lines = f.readlines()
    for x in lines:
        ReqService.append(x.split(',')[1][:])
    f.close()
    print("%------------%")
    print("ReqService: ", ReqService)
    print(ReqService[:][0])
    Function = ReqService[:][0]
    print('A Função é:', Function)
    for x in lines:
        ReqTime.append(x.split(',')[0][:])
    f.close()
    print("%------------%")                                                    
    print("ReqTime: ", ReqTime)
    print(ReqTime[:][0])
    Begin = ReqTime[:][0]
    print("Cloud Order was decoded")
    return Function, Begin, InitializeInv(Function, Begin)
"""
###--------------------------------------------------###
##------------------ Modbus Con§§§nection ---------------##
###--------------------------------------------------###

def InitializeInv(Function, TimeStep, SoCMin, Begin):
    print("Connecting to inversor")
    SMA1 = Modbus("169.254.12.3")
    print("Connected to the Inversor")
    
    return SMA1, InitializePC(Function, SMA1, TimeStep, SoCMin, Begin)

###--------------------------------------------------###
##------------- TCP Real Time Connection PC ----------##
###--------------------------------------------------###

def InitializePC(Function, SMA1, TimeStep, SoCMin, Begin):

    #Initialization Code
    print("Connecting to the PC")
    HOST = socket.gethostname()
    print(HOST)
    PORT = 50000

    s0 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s0.bind(('',PORT))

    s0.listen()
    print("Waiting for PC connection")

    ConnPC, ender = s0.accept()
    print("PC connection stablished")

    return ConnPC, ender, s0, InitializeBat(Function, SMA1, ConnPC, TimeStep, SoCMin, Begin)

###--------------------------------------------------###
##------------ TCP Real Time Connection Battery ------------##
###--------------------------------------------------###

def InitializeBat(Function, SMA1, ConnPC, TimeStep, SoCMin, Begin):

    HOST = '169.254.12.242'
    PORT = 2001

    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Conectando à Bateria')
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

    print('Conexao aceita')    

    return s2, PDMax, PCMax, InitializeData(Function, ConnPC, SMA1, s2, PDMax, PCMax, PbatRq, TimeStep, SoCMin, Begin)


###--------------------------------------------------###
##------------- Get data from time series ------------##
###--------------------------------------------------###

def InitializeData(Function, ConnPC, SMA1, s2, PDMax, PCMax, PbatRq, TimeStep, SoCMin, Begin):
    print("Obtaining data from time series databases")
    f = open('Consume.txt','r')
    lines = f.readlines()
    PCon_total = []
    for x in lines:
        PCon_total.append(x.split(',')[8])
    f.close()

    PCon_total.remove(PCon_total[0])

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
    print("TimeStep is: ", TimeStep)
    for j in range(0,math.floor(len(PCon_total)/TimeStep)):
        PCon.append(float(PCon_total[j*TimeStep]))

    for j in range(0,math.floor(len(PPV_total)/TimeStep)):
        PPV.append(float(PPV_total[j*TimeStep]))    

    Threshold = len(PCon_total)

    print("Data ready to use")    
    return PCon, PPV, Threshold, InitizalizeHistory(Function, ConnPC, SMA1, s2, PPV, PCon, PDMax, PCMax, PbatRq, TimeStep, SoCMin, Begin)

###--------------------------------------------------###
##------------- Begin BBB history ------------##
###--------------------------------------------------###

def InitizalizeHistory(Function, ConnPC, SMA1, s2, PPV, PCon, PDMax, PCMax, PbatRq, TimeStep, SoCMin, Begin):

    print("Preparing Control History")

    HistoryHeader = ['F',',','LP',',','PPS',',','id',',','Cap',',','PDMax',',',
                    'PCMax',',','RT',',','AT',',','PCon',',','PPV',',','Pbat',
                    ',','PG',',','SoC',',','SoCMin']

    History = open("History.txt",'w')
    History.writelines(HistoryHeader)
    History.write("\n")

    print("History ready to use")
    
    return History, SelectService(Function, ConnPC, SMA1, s2, PPV, PCon, PDMax, PCMax, PbatRq, TimeStep, SoCMin, Begin)


#def SelectService(Function, ConnPC, SMA1, s2, PPV, PCon, PDMax, PCMax, SoCMin, TimeStep, Begin):
def SelectService(Function, ConnPC, SMA1, s2, PPV, PCon, PDMax, PCMax, PbatRq, TimeStep, SoCMin, Begin):
    print(Function)
    print("Selecting Service out of Cloud order")
    if Function == 'Self-Consumption':
        #SelfConsumption(ConnPC, SMA1, s2, PPV, PCon, PDMax, PCMax, SoCMin, TimeStep, Begin)
        print("Service Self-Consumption has begun")
        SelfConsumption(Function, ConnPC, SMA1, s2, PPV, PCon, PDMax, PCMax, PbatRq, TimeStep, SoCMin, Begin)

    if Function == 'Peak-Shaving':
        print("Service Peak-Shaving has begun")
        PeakShaving(Function, ConnPC, SMA1, s2, PPV, PCon, PDMax, PCMax, PbatRq, TimeStep, SoCMin, Begin)

    #if Function == 'Self-Consumption':

    #if Function == 'Self-Consumption':

###--------------------------------------------------###
##------------- Self-Consumption Controler loop ------------##
###--------------------------------------------------###

#def SelfConsumption(ConnPC, SMA1, s2, PPV, PCon, PDMax, PCMax, SoCMin, TimeStep, Begin):

def SelfConsumption(Function, ConnPC, SMA1, s2, PPV, PCon, PDMax, PCMax, PbatRq, TimeStep, SoCMin, Begin):

    #SMA1.sendP(int(PPV[i]))
    #print("request de potência enviado ao inv")
    s2.send(struct.pack("i",PbatRq))

    i = 0
    #time.sleep(3)
    f = open('History.txt','w')

    #while time.ctime(time.time()) > Begin:
    while True:
        Function0 = Function
        Begin0 = Begin

        #SMA1.sendP(int(PPV[i]))
        #SMA1.newPowerSetPoint(int(PPV[i]))
        
        message = ConnPC.recv(2048)

        SoC = s2.recv(1024)
        SoC = list(SoC)
        SoC = struct.unpack("<h", bytearray(SoC))[0]/100

        print("Battery Answer: ", SoC)

        #SoC = (SoC*BatteryCapacity/100 - Pbat*60*TimeStep)*100/BatteryCapacity

        if (SoC<=100 and (not PCon[i] >= PPV[i])) or (SoC>SoCMin and PCon[i] >= PPV[i]):
            PbatRq = PCon[i] - PPV[i]
            if PbatRq >= -PDMax:
                PbatRq = -PDMax
            if PbatRq <= -PCMax:
                PbatRq = -PCMax
        if SoC < SoCMin and PbatRq >= 0:
                PbatRq = 0
        if SoC > 100 and PbatRq < 0:
            PbatRq = 0

        if (SoC>SoCMin and (not PCon[i] >= PPV[i]) and (PPV[i] - PCon[i] > -PCMax)) or (SoC> SoCMin and (not SoC < 100) and (not PCon[i] >= PPV[i])) or (PCon[i] >= PPV[i] and PCon[i] > PPV[i] - PDMax) or (PCon[i] >= PPV[i] and (not SoC > SoCMin)) or (SoC>SoCMin and (PCon[i] > PPV[i] - PDMax) and (not SoC < 100)):
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
        print("Get inversor data")

        InvStatus = SMA1.return_dict()

        #print(time.ctime(time.time()), "%.1f  %.1f %.1f %.1f %.1f %.1f" % (PCon[i], PPV[i], PbatRq, PGRq, SoC, SoCMin))
    
        Response = {'F': "Self Consumption",
                            'LP': " ",
                            'PPS': " ",
                            'id': " ",
                            'Cap': " ",
                            'PDMax': " ",
                            'PCMax': " ",
                            'RT': Begin,
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

        print('Erro entre comando e leitura: ', float(InvStatus['Power_Active'])-PPV[i])
        print('Valor da leitura: ', float(InvStatus['Power_Active']))
        print('Corrente em leitura: ', float(InvStatus['DC1_Current']))
        print('\n')
        
        HistoryData = [str(data["F"]), ',', str(data["LP"]), ',', str(data["PPS"]), ',', str(data["id"]), ',', str(data["Cap"]), ',', str(data["PDMax"]), ',', str(data["PCMax"]), ',', str(data["RT"]), ',', str(data["AT"]), ',', str(data["PCon"]), ',',  str(PPV[i]), str(InvStatus['Power_Active']), ',',  str(-data["Pbat"]), ',', str(data["PG"]), ',', str(data["SoC"]), ',', str(data["SoCMin"])]

        i = i + 1
        f.writelines(HistoryData)
        f.write("\n")

        SMA1.sendP(int(PPV[i]))
        #SMA1.newPowerSetPoint(int(PPV[i]))
        print("request de potência enviado ao inv")
        print("Potencia enviada a bateria: ", -PbatRq)
        s2.send(struct.pack("i", -int(PbatRq)))

        time.sleep(5)
        print("Adding zero value")
        s2.send(struct.pack("<i", int(0)))

        #AccessOrder(Function, Function0, ConnPC, SMA1, s2, PPV, PCon, PDMax, PCMax, PbatRq, TimeStep, SoCMin, Begin, Begin0)
        time.sleep(5)
    f.close()

def PeakShaving(ConnPC, SMA1, s2, PPV, PCon, PDMax, PCMax, PbatRq, TimeStep, SoCMin, Begin):
    print("In Construction")

def AccessOrder(Function,Function0, ConnPC, SMA1, s2, PPV, PCon, PDMax, PCMax, PbatRq, TimeStep, SoCMin, Begin, Begin0):
    if Function != Function0 and (Begin <= time.ctime(time.time())):
        SelectService(Function, ConnPC, SMA1, s2, PPV, PCon, PDMax, PCMax, PbatRq, TimeStep, SoCMin, Begin)


## %%