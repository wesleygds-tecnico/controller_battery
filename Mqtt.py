from mqtt_SSOP import clientSubscriber
import time

###--------------------------------------------------###
##------------------- MQTT Connection ----------------##
###--------------------------------------------------###

CloudOrders = []

clientSubscriber.subscribe('toAsset/123',CloudOrders,'0')

print(CloudOrders)

f = open('CloudOders.txt','w')

while True:
    lines = f.readlines(CloudOrders)
    time.sleep(1)
