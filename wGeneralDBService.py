
# * Implement REST API to access, manipulate IoT publish information in database
# * and implement additional operations

## Errors
# 0 → No error
# 1 → Arguments to create a new gate are not in the correct format
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from flask import Flask, request, abort
from gCentralComponentDB import listData, newPayload, listDataByID, listDataByTopic, row2dict

GATEDATASERVICE = "http://localhost:8000"

app = Flask(__name__)

def raise_error(errorNumber, errorDescription):
    return {"error": errorNumber, "errorDescription":errorDescription}

# GET   /API/gates -> Register new gate
# POST  /API/gates -> List registered gates
@app.route("/API/data", methods=['GET', 'POST'])
def data():
    if request.method == 'POST': #With the Post come one json like {"topic":"9999", "type":"something"}
        #parse body
        body = request.json
        try:
            topic = body['topic']
            iotDeviceID = body['iotDeviceID']
            dataType = body['dataType']
        except:
            abort(400)

        # Register Gate
        if (error := newPayload( topic,iotDeviceID, dataType )) == 0:
            return { 
                "error": 0
            }
        elif error == -1:
            return raise_error(1,"Arguments to create a new gate are not in the correct format.")
        else:
            return raise_error(100, "Something went wrong")
    elif request.method == 'GET':
        list = listData()
        dataList = []
        for i in list:
            dataList.append({"id":i.id, "topic":i.topic, "iotDeviceID":i.iotDeviceID, "dataType":i.dataType})

        return {
            "gatesList": dataList,
            "error": 0
        }

@app.route("/API/data/ID/<path:dataID>", methods=['GET', 'POST'])
def getDataByID(dataID):
    
    return row2dict(listDataByID(dataID))
    
@app.route("/API/data/topic/<path:topic>", methods=['GET', 'POST'])
def getDataByTopic(topic):

    return row2dict(listDataByTopic(topic))    


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)


