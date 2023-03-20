import struct
import time
import json

def SelfConsumption(ConnPC, SMA1, s2, PPV, PCon, PDMax, PCMax, SoCMin, TimeStep, Begin):

    SMA1.sendP(int(PPV[i]))
    s2.send(struct.pack("i",PbatRq))

    i = 0
    Threshold = len(PCon)
    time.sleep(3)
    f = open('History.txt','w')

    while i < Threshold-1:
    #while time.ctime(time.time()) < TimeToEnd:

        SMA1.sendP(int(PPV[i]))

        message = ConnPC.recv(2048)
        SoC = list(s2.recv(1024))

        #SoC = (SoC*BatteryCapacity/100 - Pbat*60*TimeStep)*100/BatteryCapacity

        if (SoC<=100 and (not PCon[i] >= PPV[i])) or (SoC>SoCMin and PCon[i] >= PPV[i]):
            PbatRq = PCon[i] - PPV[i]
            if PbatRq >= PDMax:
                PbatRq = PDMax
            if PbatRq <= PCMax:
                PbatRq = PCMax
        if SoC < SoCMin and PbatRq >= 0:
                PbatRq = 0
        if SoC > 100 and PbatRq < 0:
            PbatRq = 0

        if (SoC>SoCMin and (not PCon[i] >= PPV[i]) and (PPV[i] - PCon[i] > PCMax)) or (SoC> SoCMin and (not SoC < 100) and (not PCon[i] >= PPV[i])) or (PCon[i] >= PPV[i] and PCon[i] > PPV[i] + PDMax) or (PCon[i] >= PPV[i] and (not SoC > SoCMin)) or (SoC>SoCMin and (PCon[i] > PPV[i] + PDMax) and (not SoC < 100)):
            PGRq = PCon[i] - PbatRq

        if PbatRq == 0:
            PGRq = PCon[i] - PPV[i]

        if PbatRq < 0:
            PGRq = 0

        if PCon[i] <= PPV[i] + PbatRq and PbatRq > 0:
            PGRq = 0

        Pbat = PbatRq

        #time.sleep(8)
        #SMA1.initialRun()

        #InvStatus = SMA1.return_dict()

        #print(time.ctime(time.time()), "%.1f  %.1f %.1f %.1f %.1f %.1f" % (PCon[i], PPV[i], PbatRq, PGRq, SoC, SoCMin))
    
        Response = {'F': "Self Consumption",
                            'LP': " ",
                            'PPS': " ",
                            'id': " ",
                            'Cap': " ",
                            'PDMax': " ",
                            'PCMax': " ",
                            'RT': Begin,
                            'AT': i*TimeStep,
                            'PCon': PCon[i],
                            'PPV': PPV[i], #float(InvStatus['Power_Active']),
                            'Pbat': Pbat,
                            'PG': PGRq,
                            'SoC': SoC,
                            'SoCMin': SoCMin}

        Response = json.dumps(Response)

        ConnPC.send(str.encode(Response))

        data = json.loads(Response)

        """
        print('Erro entre comando e leitura: ', float(InvStatus['Power_Active'])-PPV[i])
        print('Valor da leitura: ', float(InvStatus['Power_Active']))
        print('Corrente em leitura: ', float(InvStatus['DC1_Current']))
        print('\n')
        """
        
        HistoryData = [str(data["F"]), ',', str(data["LP"]), ',', str(data["PPS"]), ',', str(data["id"]), ',', str(data["Cap"]), ',', str(data["PDMax"]), ',', str(data["PCMax"]), ',', str(data["RT"]), ',', str(data["AT"]), ',', str(data["PCon"]), ',',  PPV[i], """str(InvStatus['Power_Active']),""" ',',  str(data["Pbat"]), ',', str(data["PG"]), ',', str(data["SoC"]), ',', str(data["SoCMin"])]

        i = i + 1
        f.writelines(HistoryData)
        f.write("\n")

        #SMA1.sendP(int(PPV[i]))
        #s2.send(struct.pack("i",PbatRq))
        time.sleep(3)
    f.close()
    return