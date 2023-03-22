#%%
# Implement database that will store every  information
# This file is the central point of all the database
# Coordinates the flow of information, the type of information that comes in and out. Stores
# all of the information in the database


#ERRORS
# -1 -> Could not connect to the central database
# -2 -> Type of argument not correct
# -3 -> Entry/Table does not exist (or the object that is being search for doesn't exist)
# -4 -> Being implemented ( it is in topics available but it is yet to be implemented)
# -5 -> Something unexpected
# -6 -> Could not create entry on the database
# -7 ->
# -8 ->

#System imports
import sys
sys.path.append('./')

# gBaseDB imports
from gBaseDB import Base, session
from gBaseDB import Column,String,Integer, createTable
from datetime import datetime
# Other tables imports
# There are three functions for every table:
# Create new entry on the table, list things on the table and look for a specific ID on the table

from sBessMeasurementDataDB     import newBessMeasurementData, listBessMeasurementData, listBessMeasurementDataID 
from sBessSetPointDataDB        import newBessSetPointData, listBessSetPointData, listBessSetPointDataByID
from sMeasureDB                 import newMeasurement, listMeasurementsData, listMeasurementByID
from sPVGeneratorData           import newPVGeneratorData, listPVGeneratorData, listPVGeneratorDataByID
from sPVGeneratorSetPoint       import newPVGeneratorSetPoint, listPVGeneratorSetPoint, listPVGeneratorSetPointByID 
from sServiceArbitrage          import newServiceArbitrage, listServiceArbitrage, listServiceArbitrageByID
from sServicePeakShaving        import newServicePeakShaving, listServicePeakShaving, listServicePeakShavingByID
from sServiceSelfConsumption    import newServiceSelfConsumption, listServiceSelfConsumption, listServiceSelfConsumptionforID

#For the user, we need someone to fix bugs so it prints on the terminal a issue solver
EMERGENCY_CONTACT = "Instituto Superior Técnico"


# Tables and topic implemented or yet to be implemented
# #
topicsAvailable = ["bessMeasurementData",
                   "bessSetPointDataDB",
                   "measurementData",
                   "pVGeneratorData",
                   "pVGeneratorSetPoint",
                   "serviceArbitrage",
                   "ServicePeakShaving",
                   "serviceSelfConsumption"
                   ]


#Test to run and examples of data to be sent into the functions 
#
"""
#%%
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
"""

# Declaration of Central Table:
# This table has all the flow of information that comes in and out
#%%

class allPayLoads(Base):
    
    __tablename__ = 'All Payloads'
    # This should be uncommented if the tables changes
    #__table_args__ = {'extend_existing': True} 
    id = Column(Integer, primary_key=True)
    topic = Column(String)
    iotDeviceID = Column(String)
    dataType = Column(String)


    def __repr__(self):
        return "All Payloads : {{ sid : %d, topic : %s, IoT Device ID : %s, dataType : %s)}}" % (
            self.id, self.topic,
            self.iotDeviceID, self.dataType)


#Create a table in the database with the allPayLoads
#Functions from the gBaseDB
createTable()



#
#List Functions: All the funtions that retrieve information from databases
#

#%% 
# Retrieve all the data from the central table
def listData():
    
    
    try:
        return session.query(allPayLoads).all()
    except:
        print("Couldn't return info from database! Contact library owner!")
        return -1

# Retrieve all the data from the topic table passed as argument  
def listDataByTopic(topic):
    
    # Verify if the type of the arguments is correct
    if not isinstance(topic,str): 
        return -2
        
    else: 
        #Checks the topics availale array to check if the user is searching for a existing topic
        if not checkTopic(topic):
            return -3

        #tries to go to every table searching for the right topic
        try:
            if topic == "bessMeasurementData":
                return listBessMeasurementData()
            elif topic == "bessSetPointDataDB":
                return listBessSetPointData()
            elif topic == "measurementData":
                return listMeasurementsData()
            elif topic == "pVGeneratorData":
                return listPVGeneratorData()
            elif topic == "pVGeneratorSetPoint":
                return listPVGeneratorSetPoint()
            elif topic == "serviceArbitrage":
                return listServiceArbitrage()
            elif topic == "ServicePeakShaving":
                return listServicePeakShaving()
            elif topic == "serviceSelfConsumption":
                return listServiceSelfConsumption()
        
            else:
                print("Topic not valid because function doesn't exist!!! However it is in the topicsAvailable")
                return -4

        except:
            print("Couldn't access data on the database")
            return -1


# First looks for the entry in the central table
# If success, looks for the entry in the right table (the topic found).
# If success, retrieves information
def listDataByID(ID):
    
    # Verify if the type of the arguments is correct
    if not isinstance(ID,int): 
        print("Id is not a in the correct format!")
        return -2
        
    else: 

        try:
            entry = session.query(allPayLoads).get(ID)
        except:
            print("Couldn't access to that id! Error in database")
            return -1
        
        if entry == None:
            print("There is no entry with this ID!")
            return -3

        try:
            if entry.topic == "bessMeasurementData":
                return listBessMeasurementDataID(ID)
            elif entry.topic == "bessSetPointDataDB":
                return listBessSetPointDataByID(ID)
            elif entry.topic == "measurementData":
                return  listMeasurementByID(ID)
            elif entry.topic == "pVGeneratorData":
                return  listPVGeneratorDataByID(ID)
            elif entry.topic == "pVGeneratorSetPoint":
                return listPVGeneratorSetPointByID(ID)
            elif entry.topic == "serviceArbitrage":
                return listServiceArbitrageByID(ID)
            elif entry.topic == "ServicePeakShaving":
                return  listServicePeakShavingByID(ID)
            elif entry.topic == "serviceSelfConsumption":
                return listServiceSelfConsumptionforID(ID)
                    
            else:
                print("Something happen when tried to write that ID in the correct table! Not valid!")
                return -5

        except:

            print("Couldn't access data on the database of specific table!")
            return -1











# %% 
# #
# 
# Simple Functions: 
# -> Delete one row 
# -> Check all the rows in one topic
# -> Tranform into dict form 
#
# #

def deleteEntryByID(id):
    
    session.query(allPayLoads).filter_by(id=id).delete()
    session.commit()

def checkTopic(topic):

    for a in topicsAvailable:

        if a == topic:
            return 1

    return 0

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d



#%% New data
# #
# 
# Add Rows o the right places in the database
# 
# 


#To add a new payload, first creates an attemp of access data in the main table,
# Then, if the informatio is correct, it creates the entry in the right table with the topic given 



def newPayload(topic, iotDeviceID, dataType, data):
    
    # Verify if the type of the arguments is correct
    if not (isinstance(topic,str) and isinstance(iotDeviceID,str) and isinstance(dataType,str) and isinstance(data,dict)): 
        print("Type of argument/arguments is not correct!")
        return -2
        
    else:     
        if not checkTopic(topic):
            print("Topic argument does not exist! Try an existing topic!")
            return -2

        newPayload = allPayLoads(topic = topic, iotDeviceID = iotDeviceID, dataType = dataType )
        session.add(newPayload)

        try:
            session.commit()
        except:
            session.rollback()
            print("Could not create that entry on main database do to database error! Contact {}.".format(EMERGENCY_CONTACT))
            return -6
        
        data['id'] = newPayload.id

        try:
            if topic == "bessMeasurementData":
                result = newBessMeasurementData(data)
                if 0 >  result:
                    deleteEntryByID(data['id'])
            elif topic == "bessSetPointDataDB":
                result = newBessSetPointData(data)
                if 0 >  result:
                    deleteEntryByID(data['id'])
            elif topic == "measurementData":
                result =  newMeasurement(data)
                if 0 >  result:
                    deleteEntryByID(data['id'])
            elif topic == "pVGeneratorData":
                result =  newPVGeneratorData(data)
                if 0 >  result:
                    deleteEntryByID(data['id'])
            elif topic == "pVGeneratorSetPoint":
                result = newPVGeneratorSetPoint(data)
                if 0 >  result:
                    deleteEntryByID(data['id'])
            elif topic == "serviceArbitrage":
                result = newServiceArbitrage(data)
                if 0 >  result:
                    deleteEntryByID(data['id'])
            elif topic == "ServicePeakShaving":
                result =  newServicePeakShaving(data)
                if 0 >  result:
                    deleteEntryByID(data['id'])
            elif topic == "serviceSelfConsumption":
                result = newServiceSelfConsumption(data)
                if 0 >  result:
                    deleteEntryByID(data['id'])
                    
            else:
                print("Topic not valid because functions not implemented!!! However it is in the available topics. Contact {%s}".format(EMERGENCY_CONTACT) )
                return -4

        except:
            deleteEntryByID(data['id'])
            print("Couldn't write data on the database. Database error!")
            return -1
        
    
    return result









"""
#%%
# #
# 
# Test Functions
# 
# #

#%% Test Funtions
newPayload(topic = "pVGeneratorData", iotDeviceID = "iotDeviceID", dataType = "dataType", data = data2 )





# %%
#listDataByTopic("measurementData")
listDataByTopic("pVGeneratorData")







#%%
#listDataByID(20)
listDataByID(2)


"""