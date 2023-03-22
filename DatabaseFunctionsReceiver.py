# %% 

# some_file.py
import socket
import json
import time
import math
import struct
from InverterCommands import Modbus
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
    'Type_Of_Service' : "Self-Consumption",
    'Activation' : date,
    'Price' : 'NA',
    'Price_Min' : 'NA',
    'Price_Max' : 'NA',
}

Data ={
    'meter_ID' : 1,
    'measure_ID' : 1,
    'timestamp' : date,
}

DataInversor = {
    'id': 'Inversor',
    'time': date,
    'PowerRequested': 'PowerRequested',
    'PowerMeasured': 'PowerMeasured',
}

DataBattery = {
    'id': 'Battery',
    'time': date,
    'PCMax': 'PCMax',
    'PDMax': 'PDMax',
    'SoC': 'SoC',
    'PowerRequested': 'PowerRequested',
    'PowerMeasured': 'PowerMeasured',
}

DataCloud = {
    'id': 'Cloud',
    'time': date,
    'Service': 'Self-Consumption',
    'Begin': 'Begin'
}

data = {
    'Service': 'Self-Consumption',
    'time': 'date',
    'Begin': 'Begin',
    'PCon': 'PCon',
    'PPV': 'PPV',
    'PReqInv': 'PReqInv',
    'PMeaInv': 'PMeaInv',
    'PReqBat': 'PReqBat',
    'PMeaBat': 'PMeaBat',
    'SoC': 'SoC',
    'PCMax': 'PCMax',
    'PDMax': 'PDMax',
}

print("%--------------- Initialization ------------------%")

subThread = threading.Thread(target=lambda: subscriber.subscribe('toAsset/123',CloudOrders,'0'))
subThread.start()
print("Thread initiated")

#print("Initialization of Orders DBCLC Concluded")

time.sleep(5)
print("CloudOrders: ", CloudOrders)

print("%--------------- Initialization ------------------%")
print("\n")

print("%--------------- Writing on DataBase ------------------%")

DB.newPayload(topic = "InversorHistory", iotDeviceID = 1, dataType = "dataType", data = DataInversor) 
DB.newPayload(topic = "BatteryHistory", iotDeviceID = 2, dataType = "dataType", data = DataBattery) 
DB.newPayload(topic = "CloudHistory", iotDeviceID = 3, dataType = "dataType", data = DataCloud) 
    
#DataType identificação da tabela
#Mensagem do MQTT
#

A = DB.listDataByID(1)
print(A)
B = DB.row2dict(A)
print(B)

A = DB.listDataByID(2)
print(A)
B = DB.row2dict(A)
print(B)

A = DB.listDataByID(3)
print(A)
B = DB.row2dict(A)
print(B)

print("%--------------- Writing on DataBase ------------------%")        