from gBaseDB import Base, Column, DateTime  
from datetime import datetime
from gBaseDB import Integer, Float 
from gBaseDB import session, createTable

# Declaration of Table

class bessMeasurementData(Base):
    
    __tablename__ = 'Bess Measurement Data'
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)

    meter_ID = Column(Integer)
    measure_ID = Column(Integer)
    timestamp = Column(DateTime)
    type = Column(Integer)
    n_Phases = Column(Integer)
    chanel = Column(Integer)
    unit = Column(Integer)
    multi_Factor = Column(Integer)
    measure_1 = Column(Float)
    measure_2 = Column(Float)
    measure_3 = Column(Float)
    
    def __repr__(self):
        return "<Bess Measured Data(id = %d, name = %d)>" % (self.id,
                                                self.meter_ID)
    

createTable

#returns the list of the data
def listBessMeasurementData():
    return session.query(bessMeasurementData).all()

def listBessMeasurementDataID(id):
    return session.query(bessMeasurementData).filter(bessMeasurementData.id==id).first()

#Creates a new action (history) of an existent user
def newBessMeasurementData(data):
    # Verify if the type of the arguments is correct

    meter_ID = int(data['meter_ID'])
    measure_ID = int(data['measure_ID'])
    timestamp = datetime.fromisoformat(data['timestamp'])
    type = int(data['type'])
    n_Phases = int(data['n_Phases'])
    chanel = int(data['chanel'])
    unit = int(data['unit'])
    multi_Factor = int(data['multi_Factor'])
    measure_1 = float(data['measure_1'])
    measure_2 = float(data['measure_2'])
    measure_3 = float(data['measure_3'])


    
    try:
        bess = bessMeasurementData(meter_ID = meter_ID,
                                    measure_ID = measure_ID,
                                    timestamp = timestamp,
                                    type = type,
                                    n_Phases = n_Phases,
                                    chanel = chanel,
                                    unit = unit,
                                    multi_Factor = multi_Factor,
                                    measure_1 = measure_1,
                                    measure_2 = measure_2,
                                    measure_3 = measure_3
        )
        
        session.add(bess)
        try:
            session.commit()
        except:
            session.rollback()
            return -4

        

    except:
        return -1

    return 0


