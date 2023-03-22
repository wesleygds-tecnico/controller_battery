import BBBControlerFunctions

f = open('CloudOders.txt','w')

CloudOrders = {
    "lastMessage": "Not modified",
    "id": 0
}

ReqTime = []
ReqService = []
TimeStep = 1
SoCMin = 40

Function = "Self-Consumption"
Begin = "A"

try:
    #BBBControlerFunctions.Initialize(CloudOrders, f)
    BBBControlerFunctions.InitializeInv(Function, TimeStep, SoCMin, Begin)
except:
    #BBBControlerFunctions.Initialize(CloudOrders, f)
    BBBControlerFunctions.InitializeInv(Function, TimeStep, SoCMin, Begin)