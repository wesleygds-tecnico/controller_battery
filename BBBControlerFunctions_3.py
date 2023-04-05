# %% 

# some_file.py
import socket
import json
import time
import math
import struct
from InverterCommands import Modbus
import BBBControlLoops
from SSOPInvertorDataBase.clientSubscriber import subscribe
import threading
from SSOPInvertorDataBase import gCentralComponentDB as DB
from datetime import datetime



#from mqtt_SSOP import clientSubscriber

# %% 

###--------------------------------------------------###
##------------------- MQTT Connection ----------------##
###--------------------------------------------------###

#ReqTime = []
#ReqService = []
#TimeStep = 1
#SoCMin = 40
#
#date = datetime.now().isoformat()

#data ={
#    "Service": "Self-Consumption",
#    "time":  date,
#    "Begin": date,
#    "PCon": 1,
#    "PPV": 1,
#    "PReqInv": 1,
#    "PMeaInv": 1,
#    "PReqBat": 1,
#    "PMeaBat": 1,
#    "SoC": 1,
#    "PDMax": 1,
#    "PCMax": 1,
#}

def Initialize(TimeStep, SoCMin, SoCMax):
    global subThread
    print("%--------------- Initialization ------------------%")
    #Header = ['Function',',','Begin',',','Limit Power']
    #f.writelines(Header)
    #f.write("\n")

    subThread = threading.Thread(target=lambda: subscribe(topic= 'toAsset/123', clientID = 'Client number 10'))    
    subThread.start()

    
    print("Thread initiated")

    #print("Initialization of Orders DBCLC Concluded")

    print("%--------------- Initialization ------------------%")
    print("\n")

    print("%--------------- Writing on DataBase ------------------%")

    #DB.newPayload(topic = "inverterData", iotDeviceID = "iotDeviceID", dataType = "inverterData", data = data) 
    
    #DataType identificação da tabela
    #Mensagem do MQTT
    #



    #print('Data', CloudOrder["data"]["Service"])
    #time.sleep(5)
    
    print("%--------------- Writing on DataBase ------------------%")     

#    while True:
#        DB.table2dict(DB.listData())
#        time.sleep(10)
    
    global subThread
    return GetNextOrder(subThread, TimeStep, SoCMin, SoCMax)

def GetNextOrder(subThread, TimeStep, SoCMin, SoCMax):
    data = DB.table2dict(DB.listDataByDataType("inverterData"))
    print('Database', data) #Em tese, it should return a dict with information to begin a new control loop
    CloudOrder = data["data"][-1]
    print("\n")
    print('Data', CloudOrder)
    print("\n")
    print('Data type', type(CloudOrder))
    print("\n")
    return CloudOrder, InitializeInv(subThread, CloudOrder, TimeStep, SoCMin, SoCMax)    


#%%
"""
def ConnectCloud(CloudOrders,f):
    print("%--------------- Connecting to Cloud ------------------%")

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

def InitializeInv(subThread, CloudOrder, TimeStep, SoCMin, SoCMax):
    print("Connecting to inversor")
    SMA1 = Modbus("169.254.12.172")
    print("Connected to the Inversor")
    
    return InitializePC(subThread, CloudOrder, SMA1, TimeStep, SoCMin, SoCMax)

###--------------------------------------------------###
##------------- TCP Real Time Connection PC ----------##
###--------------------------------------------------###

def InitializePC(subThread, CloudOrder, SMA1, TimeStep, SoCMin, SoCMax):

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

    return ConnPC, ender, s0, InitializeBat(subThread, CloudOrder, SMA1, ConnPC, TimeStep, SoCMin, SoCMax)

###--------------------------------------------------###
##------------ TCP Real Time Connection Battery ------------##
###--------------------------------------------------###

def InitializeBat(subThread, CloudOrder, SMA1, ConnPC, TimeStep, SoCMin, SoCMax):

    HOST = '169.254.12.176'
    PORT = 2001

    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Conectando à Bateria')
    s1.connect((HOST, PORT))
    print('Inicializando Bateria')

    data = s1.recv(1024) #Resposta
    data = list(data)
    value = struct.unpack("<hhh", bytearray(data))
    Cap = value[0]
    PDMax = value[2]
    PCMax = value[1]

    print('Bateria inicializada')

    PORT = 2000

    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.connect((HOST, PORT))
    print('Bateria pronta para serviço')

    PbatRq = 0

    print('Conexao aceita')    

    return s2, PDMax, PCMax, InitializeData(subThread, CloudOrder, ConnPC, SMA1, s2, Cap, PDMax, PCMax, PbatRq, TimeStep, SoCMin, SoCMax)


###--------------------------------------------------###
##------------- Get data from time series ------------##
###--------------------------------------------------###

def InitializeData(subThread, CloudOrder, ConnPC, SMA1, s2, Cap, PDMax, PCMax, PbatRq, TimeStep, SoCMin, SoCMax):
    Period = 30
    print("Obtaining data from time series databases")
    f = open('Consume.txt','r')
    lines = f.readlines()
    Timetable = []
    PCon_total = []
    for x in lines:
        Timetable.append(x.split(",")[0])
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

    # Determina o periodo de ação
    TimeIndex = Timetable.index("2022-02-20T15:00:00.000Z")
    PCon = PCon_total[TimeIndex: TimeIndex + Period]
    PCon = list(map(float, PCon))
    print(PCon)
    PPV = PPV_total[TimeIndex: TimeIndex + Period]
    PPV = list(map(float, PPV))
    print(PPV)
    print("Data ready to use")    
    return PCon, PPV, Timetable, Period, Threshold, InitizalizeHistory(subThread, CloudOrder, ConnPC, SMA1, s2, PPV, PCon, Cap, PDMax, PCMax, PbatRq, TimeStep, Timetable, Period, SoCMin, SoCMax)

###--------------------------------------------------###
##------------- Begin BBB history ------------##
###--------------------------------------------------###

def InitizalizeHistory(subThread, CloudOrder, ConnPC, SMA1, s2, PPV, PCon, Cap, PDMax, PCMax, PbatRq, TimeStep, Timetable, Period, SoCMin, SoCMax):

    print("Preparing Control History")

    HistoryHeader = ['F',',','LP',',','PPS',',','id',',','Cap',',','PDMax',',',
                    'PCMax',',','RT',',','AT',',','PCon',',','PPV',',','PInv',',','Pbat',
                    ',','PG',',','SoC',',','SoCMin']

    History = open("History.txt",'w')
    History.writelines(HistoryHeader)
    History.write("\n")

    print("History ready to use")
    
    return History, SelectService(subThread, CloudOrder, ConnPC, SMA1, s2, PPV, PCon, Cap, PDMax, PCMax, PbatRq, TimeStep, Timetable, Period, SoCMin, SoCMax)


#def SelectService(Function, ConnPC, SMA1, s2, PPV, PCon, PDMax, PCMax, SoCMin, TimeStep, Begin):
def SelectService(subThread, CloudOrder, ConnPC, SMA1, s2, PPV, PCon, Cap, PDMax, PCMax, PbatRq, TimeStep, Timetable, Period, SoCMin, SoCMax):
    while True:
        Function = CloudOrder["Service"]
        Begin = CloudOrder["Begin"]
        print(Function)
        print("Selecting Service out of Cloud order")

        if Function == 'Self-Consumption' and Begin <= datetime.now().isoformat():
            #SelfConsumption(ConnPC, SMA1, s2, PPV, PCon, PDMax, PCMax, SoCMin, TimeStep, Begin)
            print("Service Self-Consumption has begun")
            SelfConsumption(subThread, Function, ConnPC, SMA1, s2, PPV, PCon, Cap, PDMax, PCMax, PbatRq, TimeStep, Timetable, Period, SoCMin, SoCMax, Begin)

        if Function == 'Peak-Shaving' and Begin <= datetime.now().isoformat():
            print("Service Peak-Shaving has begun")
            PeakShaving(subThread, Function, ConnPC, SMA1, s2, PPV, PCon, PDMax, PCMax, PbatRq, TimeStep, Timetable, Period, SoCMin, Begin)

        time.sleep(5)

        data = DB.table2dict(DB.listDataByDataType("inverterData"))
        print('Database', data) #Em tese, it should return a dict with information to begin a new control loop
        CloudOrder = data["data"][-1]
        print("\n")
        print('Data', CloudOrder)
        print("\n")
        print('Data type', type(CloudOrder))
        print("\n")
        #if Function == 'Self-Consumption':

        #if Function == 'Self-Consumption':

###--------------------------------------------------###
##------------- Self-Consumption Controler loop ------------##
###--------------------------------------------------###

#def SelfConsumption(ConnPC, SMA1, s2, PPV, PCon, PDMax, PCMax, SoCMin, TimeStep, Begin):

def SelfConsumption(subThread, Function, ConnPC, SMA1, s2, PPV, PCon, Cap, PDMax, PCMax, PbatRq, TimeStep, Timetable, Period, SoCMin, SoCMax, Begin):
    Pbat = 0
    EP_Type = False
    i = 0
    f = open('History.txt','w')

    #while time.ctime(time.time()) > Begin:
    while i < Period:
        Function0 = Function
        Begin0 = Begin

        Pdiff = PCon[i] - PPV[i]
        # Simula a leitura da potência da rede
        PGRq = Pdiff + Pbat
        # Determina trânsito de potência de acordo com o tipo de quadro
        if EP_Type:
            PGRq = PCon[i] - PPV[i] + Pbat
        else:
            PGRq = PGRq

        [Pbat, SoC] = BBBControlLoops.self_consumption(PGRq, Pbat, [SoC, SoCMin, SoCMax], Cap, TimeStep, PCMax, PDMax)

        """
        match choice:
            case 1:  # Ativa a função Peak Shaving
                [Pbat_in, SoC] = BBBControlLoops.peak_shaving(Ppeak, Pgrid, Pbat_in, [SoC, SoCMin, SoCMax], Cap, TimeStep, PCMax, PDMax)
            case 2:  # Ativa a função Self_Consumption
                [Pbat_in, SoC] = BBBControlLoops.self_consumption(Pgrid, Pbat_in, [SoC, SoCMin, SoCMax], Cap, TimeStep, PCMax, PDMax)
            case 3:  # Ativa a função ToU
                [Pbat_in, SoC] = BBBControlLoops.tou_tariff(Pgrid, Pbat_in, [SoC, SoCMin, SoCMax], Cap, TimeStep, PCMax, PDMax, [pcurr, pmin, pmax])
        """

        if PGRq <= 0:
            PInv = PGRq

        print(Pbat)
        print(SoC)

        SMA1.sendP(int(PInv))
        print("request de potência enviado ao inv")
        print("Potencia enviada a bateria: ", -PbatRq)
        s2.send(struct.pack("<i", -int(PbatRq)))

        time.sleep(4)        

        SMA1.initialRun()
        print("Get inversor data")

        InvStatus = SMA1.return_dict()

        #print(time.ctime(time.time()), "%.1f  %.1f %.1f %.1f %.1f %.1f" % (PCon[i], PPV[i], PbatRq, PGRq, SoC, SoCMin))
    
        Response = {'F': Function0,
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
                            'PInv': float(InvStatus['Power_Active']),
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
        
        HistoryData = [str(data["F"]), ',', str(data["LP"]), ',', str(data["PPS"]), ',', str(data["id"]), ',', str(data["Cap"]), ',', str(data["PDMax"]), ',', str(data["PCMax"]), ',', str(data["RT"]), ',', str(data["AT"]), ',', str(data["PCon"]), ',',  str(PPV[i]), ',', str(InvStatus['Power_Active']), ',',  str(-data["Pbat"]), ',', str(data["PG"]), ',', str(data["SoC"]), ',', str(data["SoCMin"])]

        f.writelines(HistoryData)
        f.write("\n")

        data = {
            'id' : 'BBB',
            'Service' : Function,
            'time' : datetime.now().isoformat(),
            'Begin' : Begin,
            'PCon' : PCon[i],
            'PPV' : PPV[i],
            'PReqInv' : int(PPV[i]),
            'PMeaInv' : float(InvStatus['Power_Active']),
            'PReqBat' : -int(PbatRq),
            'PMeaBat' : -int(PbatRq),
            'SoC' : SoC,
            'PCMax' : PCMax,
            'PDMax' : PDMax
        }

        DB.newPayload('ControlHistory','Beaglebone','inverterData', data)

        AccessOrder(subThread, Function, Function0, ConnPC, SMA1, s2, PPV, PCon, PDMax, PCMax, PbatRq, TimeStep, SoCMin, SoCMax, Begin, Begin0)
        i = i + 1

    f.close()

def PeakShaving(subThread, ConnPC, SMA1, s2, PPV, PCon, PDMax, PCMax, PbatRq, TimeStep, SoCMin, Begin):
    print("In Construction")

def AccessOrder(subThread, Function,Function0, ConnPC, SMA1, s2, PPV, PCon, PDMax, PCMax, PbatRq, TimeStep, SoCMin, SoCMax, Begin, Begin0):
    CloudOrder = GetNextOrder(subThread, TimeStep, SoCMin, SoCMax)
    Function = CloudOrder["Service"]
    Begin = CloudOrder["Begin"]
    if (Function != Function0) and (Begin != Begin0):
        SelectService(subThread, Function, ConnPC, SMA1, s2, PPV, PCon, PDMax, PCMax, PbatRq, TimeStep, SoCMin, Begin)


## %%
