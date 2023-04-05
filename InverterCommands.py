from pyModbusTCP.client import ModbusClient
from threading import Thread
import datetime
import time
class Modbus(Thread):
    def __init__(self,ip_address): #Stablish the connection via modbus among the ip_address of interest
        Thread.__init__(self)
        SERVER_HOST = ip_address
        SERVER_PORT = 502 #essa porta necessariamente -> pra comunicação em modbustcp
        self.c = ModbusClient(SERVER_HOST,SERVER_PORT,3)
        # define modbus server host, port
        print(self.c.host)
        #self.c.host(SERVER_HOST)
        #self.c.port(SERVER_PORT)
        #self.c.unit_id(3)
        self.smadict = {} #Cria-se um dicionário
        self.newPower = 0
        self.NewPowerFlag = False
        self.ControlledID = 0
        self.NewPowerFactorFlag = False
        self.newPowerFactor = 0
        self.NewLeadingFlag = False
        self.dummy = False
        self.ControlledID_time = datetime.datetime.now()
        if not self.c.is_open: #is_open --> get the state of the serial port, whether it's open
            if not self.c.open(): #open port
                print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))
                print(self.c.last_error())
                self.dummy = True
                self.smadict['status'] = "Not Connected"
        print("Connection Done")
        self.c.write_multiple_registers(40210,[0,1077]) #Altera o operating mode

    def __del__(self): #Destructor, close port when serial port instance is freed.
        print('ok')
        pass
        # create an axis
    def setID(self,id):
        self.ControlledID = id;
        self.ControlledID_time = datetime.datetime.now()
        return
    def getIDN(self):
        return self.ControlledID

    def getID_Time(self):
        return self.ControlledID_time

    def getCurrent_Time(self):
        return datetime.datetime.now()

    def isConnected(self):
        return (not self.dummy)

    def sendP(self,NewPower): #Send and set power
        self.c.write_multiple_registers(40212,[0,NewPower]) #Active Power Configuration, U32, FIX0, RW, W, 0W to 5050W, Active power limitation P active power configuration

    def sendPPer(self,NewPower): #Send and set power
        self.c.write_multiple_registers(41075,[0,NewPower/870]) #Active Power Configuration, U32, FIX0, RW, W, 0W to 5050W, Active power limitation P active power configuration        

    def setStopInverter(self):
        self.c.write_multiple_registers(40009,[0,381]) #Funcões usadas na escrita 381 -> menos significativo 0 -> mais significataivo (função STOP --> ver no mapa de registroos)
        #2, U32, TAGLIST, RW, 295: MPP (Mpp) | 381: Stop (Stop) | 443: Constant voltage (VolDCConst), 1, Operational Condition

    def setStartMPP(self):
        self.c.write_multiple_registers(40009,[0,295]) #Funcões usadas na escrita
        ##2, U32, TAGLIST, RW, 295: MPP (Mpp) | 381: Stop (Stop) | 443: Constant voltage (VolDCConst), 1, Operational Condition

    def setActivePowerGridManagement(self,Power):
        if Power > 100: #Está em %
            return -1
        if Power < 0:
            return 1
        self.c.write_single_register(40016,Power) #1, S16, FIX0, W, Normalized active power limitation by PV system ctrl
        return 0

    def setReactivePowerGridManagement(self,Power): 
        #print("working")
        if Power > 100:
            return -1
        if Power < 0:
            return -1
        self.c.write_single_register(40015,Power) #1, S16, FIX1, W, %, Normalized reactive power limitation by PV system ctrl
        return 0

    def setPowerFactorGridManagement(self,Power):
        if(Power < 0):
            self.c.write_multiple_registers(40025,[0,1041]) #Indutivo - 2, U32, TAGLIST, W, Excitation type that can be changed by PV system ctrl
        else:
            self.c.write_multiple_registers(40025,[0,1042]) #Capacitivo - 2, U32, TAGLIST, W, Excitation type that can be changed by PV system ctrl

        self.c.write_single_register(40024,int(abs(Power*10000))) #Define o valor do fator de potência - 1, U16, FIX4, W, Dis.pow.factor that can be changed via PV system ctrl
        return 0

    def getGridGuard(self):
        self.c.write_multiple_registers(43090,[40958,65347]) #Grid code, coloca-se nessa mesma ordem #It doesn't appear no the registers map

    def get_status(self):
        regs = self.c.read_holding_registers(30201, 2) #2, U32, TAGLIST, RO, 35: Fault (Alm) | 303: Off (Off) | 307: Ok (Ok) | 455: Warning (Wrn)
        if regs[1] == 35:
            self.smadict['status'] = "Error"

        if regs[1] == 303:
            self.smadict['status'] = "Off"

        if regs[1] == 307:
            self.smadict['status'] = "Ok"

        if regs[1] == 455:
            self.smadict['status'] = "Warning"


    def get_software_pack(self): #Me está confuso, não sei o que quer fazer

        regs = self.c.read_holding_registers(30059, 2) #2, U32, FW, RO, 40045, Vr, 1, 8, string8, RO, 0 to 4294967294
        Major = regs[0]>>8 & 0xFF # 0xFF is a hexadecimal constant which is 11111111 in binary. By using bitwise AND ( & ) with this constant, it leaves only the last 8 bits of the original (in this case, whatever cv2. waitKey(0) is).
        Minor = regs[0] &0xFF
        Build = regs[1]>>8 & 0xFF
        if (regs[1] & 0xFF) == 0:
            Rel = "N"
        if (regs[1] & 0xFF) == 1:
            Rel = "E"
        if (regs[1] & 0xFF) == 2:
            Rel = "A"
        if (regs[1] & 0xFF) == 3:
            Rel = "B"
        if (regs[1] & 0xFF) == 4:
            Rel = "R"
        if (regs[1] & 0xFF) == 5:
            Rel = "S"
        if (regs[1] & 0xFF) > 5:
            Rel = ""

        self.smadict['software_pack']= str(Major)+"."+str(Minor)+"."+str(Build)+"."+Rel

    def get_Premission_Status(self):
        self.smadict['grid_guard'] = self.c.read_holding_registers(43090, 2) #Register 

    def get_device_type(self): #Identifica o inversor
        regs = self.c.read_holding_registers(30053, 2)
        if regs[1] == 9074:
            self.smadict['type'] =  "SB 3000TL-21"
        if regs[1] == 9319:
            self.smadict['type'] =  "SB3.0-1AV-40" #O q interessa

    def get_dc1_status(self):
        I = self.c.read_holding_registers(30769, 2) #2, S32, FIX3, RO, 40641, DCA, 160, 1, uint16, 40624, RO, A
        V = self.c.read_holding_registers(30771, 2) #2, S32, FIX2, RO, 40642, DCV, 160, 1, uint16, 40625, RO, V
        P = self.c.read_holding_registers(30773, 2) #2, S32, FIX0, RO, 40643, DCW, 160, 1, uint16, 40626, RO, W
        if P != None:
            self.smadict['DC1_Power'] = P[1]
        if V != None:
            self.smadict['DC1_Voltage'] = V[1]/100 #Conversão, it only reads integer numbers, so divide by 100 to get the real quantity
        if I != None:
            self.smadict['DC1_Current'] = I[1]/1000 #Conversão de A para mA, the same

    def get_dc2_status(self):
        I = self.c.read_holding_registers(30957, 2) #2, S32, FIX3, RO, 40661, DCA, 160, 1, unit16, 40624, RO, A, DC current input  
        V = self.c.read_holding_registers(30959, 2) #2, S32, FIX2, RO, 40662, DCV, 160, 1, unit16, 40625, RO, V, DC voltage input
        P = self.c.read_holding_registers(30961, 2) #2, S32, FIX0, RO, 40663, DCW, 160, 1, unit16, 40626, RO, W, DC power input
        if P != None:
            self.smadict['DC2_Power'] = P[1]
        if V != None:
            self.smadict['DC2_Voltage'] = V[1]/100
        if I != None:
            self.smadict['DC2_Current'] = I[1]/1000


    def get_ac_status(self):
        regs = self.c.read_holding_registers(30803, 2) #2, U32, FIX2, RO, 40202, Hz, 101, 1, uint16, 40203, RO, Hz, Grid frequency
        if regs != None:
            frequency = regs[1]/100
        regs = self.c.read_holding_registers(30797, 2) #No results
        regs2 = self.c.read_holding_registers(30783, 2) #2, U32, FIX2, RO, 40196, PhVphA, 101, 1, uint16, 40199, RO, V, Grid voltage phase L!
        if regs != None and regs2 != None:
            V = regs2[1]/100
            if V == 655.35:
                V = 0
            I = regs[1]/1000
            self.smadict['AC_Frequency'] = frequency
            self.smadict['AC_Voltage'] = V
            self.smadict['AC_Current'] = I

    def get_powers(self):
        regs  = self.c.read_holding_registers(30775, 2) #2, S32, FIX, RO, 40200, W, 101, 1, int16, 40201, RO, W, Power
        regs2 = self.c.read_holding_registers(30805, 2) #2, S32, FIX0, RO, 40206, VAr, 101, 1, int16, 40207, RO, VAr, Reactive power
        regs3 = self.c.read_holding_registers(30813, 2) #2, S32, FIX0, RO, 40204, VA, 101, 1, int16, 40205, RO, VA, Apparent power 
        regs4 = self.c.read_holding_registers(30949, 2) #2, U32, FIX3, RO, Displacement power factor
        if regs != None and regs2 != None and regs3 != None and regs4 != None:
            iv = (regs2[0] << 16) + regs2[1]
            if(iv & 0x80000000):
                iv = -0x100000000 + iv
            Q = iv
            if Q == -2147483648:
                Q = 0
            P = regs[1]
            if P == 0xFFFF:
                P = 0
            S = regs3[1]
            if S == 0xFFFF:
                S = 0

            Phi = regs4[1]/1000
            if Phi == 65.535:
                Phi = 1
            self.smadict['Power_Active'] = P
            self.smadict['Power_Reactive'] = Q
            self.smadict['Power_Aparent'] = S
            self.smadict['Power_Factor'] = Phi

    def get_transferrate(self):
        regs = self.c.read_holding_registers(30925, 2) #2, U32, TAGLIST, RO, 40073, Spd, 11, 1, uint16, RO, 1720: 10 Mbit/s (ConnSpd10) | 1721: 100 Mbit/s (ConnSpd100) | 3581: No connection speed set (ConnSpdNone), 3, Connection speed of SMACOM A
        if regs == 1720:
            return 10
        if regs == 1721:
            return 100
        if regs == 1725:
            return -1

    def get_duplexmode(self):
        regs = self.c.read_holding_registers(30927, 2)
        if regs == 1725:
            return "Not Connected"
        if regs == 1726:
            return "Half-Duplex"
        if regs == 1727:
            return "Full-Duplex" #Identifica o tipo de comunicação -> enviar e receber em ambos sentidos

    def get_energy(self):
        regs = self.c.read_holding_registers(30529,2)
        if regs != None:
            iv = (regs[0]<<16) + regs[1]
            self.smadict['TotalYield'] = iv #Funcionou ok -- Há 
        regs = self.c.read_holding_registers(30535,2)
        if regs != None:
            iv = (regs[0]<<16) + regs[1]
            self.smadict['TotalYieldDay'] = iv #Lê energia total em um dia NÃO ESTAVA A FUNCIONAR  -- Há endereços a se testar

        return iv

    def initialRun(self):
        if self.dummy == False:
            self.get_status()
            self.get_device_type()
            self.get_Premission_Status()
            self.get_software_pack()
            self.get_dc1_status()
            self.get_dc2_status()
            self.get_ac_status()
            self.get_powers()
            self.get_energy()
            self.smadict['time'] = datetime.datetime.now()
        return self.smadict

    def newPowerSetPoint(self,Power):
        if (Power < 3000 and Power > 0):
            self.newPower = int((Power/3000)*100)
            self.NewPowerFlag = True
            return -1
        else:
            return 0

    def newPowerFactorSetPoint(self,Power_Factor):
        if (Power_Factor >= 0.8 and Power_Factor <= 1.0):
            self.newPowerFactor = Power_Factor
            self.NewPowerFactorFlag = True
        elif (Power_Factor>-1 and Power_Factor <= -0.8):
            self.newPowerFactor = Power_Factor
            self.NewPowerFactorFlag = True
        else:
            return -1
        return 0


    def run(self):
        while True:
            if self.dummy == False:
                self.get_status()
                self.get_dc1_status()
                self.get_dc2_status()
                self.get_ac_status()
                self.get_powers()
                self.get_energy()
                self.smadict['time'] = datetime.datetime.now()
                if self.NewPowerFlag == True:
                    self.NewPowerFlag = False
                    self.setActivePowerGridManagement(self.newPower)
                if self.NewPowerFactorFlag == True:
                    self.NewPowerFactorFlag = False
                    self.setPowerFactorGridManagement(self.newPowerFactor)
            time.sleep(1)

    def return_dict(self):
        return self.smadict