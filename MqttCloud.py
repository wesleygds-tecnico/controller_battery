#%%
import mqtt_SSOP.clientPublisher as Pub
from datetime import datetime
import json

date = datetime.now()

date = str(date)

data = {

    "credentials" : {
        "username" : "pedro"
    },
    "data" : 
        {       
            'Service': 'Self_Consumption',
            'time': str(datetime.now()),
            'Begin': date,
            'PCon': "1",
            'PPV': "1",
            'PReqInv': "1",
            'PMeaInv': "1",
            'PReqBat': "1",
            'PMeaBat': "1",
            'SoC': "1",
            'PCMax': "1",
            'PDMax': "1",
    },
}

#%%
Pub.publish("toAsset/123",data, "Client number 10")