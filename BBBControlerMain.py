import BBBControlerFunctions

f = open('CloudOders.txt','w')

CloudOrders = []
ReqTime = []
ReqService = []
TimeStep = 1
SoCMin = 40

try:
    BBBControlerFunctions.Initialize(CloudOrders, f)
except:
    BBBControlerFunctions.Initialize(CloudOrders, f)