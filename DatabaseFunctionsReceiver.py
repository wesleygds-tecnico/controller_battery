# %% 

# some_file.py
import requests
from datetime import datetime
from gCentralComponentDB import newPayload
from InverterDB

#URL_BASE = "http://127.0.0.1:8000/"

URL_BASE = "http://www.google.com"

URL_Requets_pvge2 = "API/data"
URL_Requets_pvge = "API/data/dataType/pVGeneratorData"

#x = requests.get( URL_BASE + URL_Requets_pvge  )
x = requests.get( URL_BASE )
#y = requests.get( URL_BASE + URL_Requets_pvge2  )

print(x.status_code)
print(x.text)
#print(y.status_code)
#print(y.text)

data = {
    'Service': "Self_Consumption",
    'time': datetime.now().isoformat(),
    'Begin': datetime.now().isoformat(),
    'PCon': 1,
    'PPV': 1,
    'PReqInv': 1,
    'PMeaInv': 1,
    'PReqBat': 1,
    'PMeaBat': 1,
    'SoC': 1,
    'PCMax': 1,
    'PDMax': 1,
}


newPayload("toAsset/123", "123", "inverterData", data)



# %% 
"""
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
"""



