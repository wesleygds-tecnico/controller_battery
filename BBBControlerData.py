import math



def InitializeData(TimeStep):
    f = open('Consume.txt','r')
    lines = f.readlines()
    PCon_total = []
    for x in lines:
        PCon_total.append(x.split(',')[8])
    f.close()

    PCon_total.remove(PCon_total[0])

    for i in range(0,1440):
        if float(PCon_total[i]) > 870:
            PCon_total[i] = float(PCon_total[i])/7
        if float(PCon_total[i]) > 870:
            print(PCon_total[i])

    f = open('SolarProduction.txt','r')
    lines = f.readlines()
    PPV_total= []
    for x in lines:
        PPV_total.append(x.split(',')[8])
    f.close()

    PPV_total.remove(PPV_total[0])

    for i in range(0,1440):
        if float(PPV_total[i]) > 870:
            PPV_total[i] = float(PPV_total[i])/7
        if float(PPV_total[i]) > 870:
            print(PPV_total[i])

    PCon = []
    PPV = []

    for j in range(0,math.floor(len(PCon_total)/TimeStep)):
        PCon.append(float(PCon_total[j*TimeStep]))

    for j in range(0,math.floor(len(PPV_total)/TimeStep)):
        PPV.append(float(PPV_total[j*TimeStep]))    

    Threshold = len(PCon_total)
    return PCon, PPV, Threshold