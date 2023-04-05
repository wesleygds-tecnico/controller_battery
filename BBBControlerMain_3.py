import BBBControlerFunctions_3

f = open('CloudOders.txt','w')

CloudOrders = {
    "lastMessage": "Not modified",
    "id": 0
}

ReqTime = []
ReqService = []
TimeStep = 1
SoCMin = 40
SoCMax = 40
Period = 30
Function = "Self-Consumption"
Begin = "A"

try:
    #BBBControlerFunctions.Initialize(CloudOrders, f)
    BBBControlerFunctions_3.Initialize(TimeStep, SoCMin, SoCMax)
except:
    #BBBControlerFunctions.Initialize(CloudOrders, f)
    BBBControlerFunctions_3.Initialize(TimeStep, SoCMin, SoCMax)