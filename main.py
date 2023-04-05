import socket
import json
import time
import math
from use_cases import UseCases as use_cases
import numpy as np

# Potências Máxima de carregamento e descarregamento em W
Pch_max = 2500
Pdh_max = -2500
# Capacidade da bateria em Wh
Cap = 5000
# SoC atual e SoC min em percentagem
SoC = 70
SoC_min = 20
SoC_max = 80
# Tipo de quadro eléctrico (false= lê Pgrid; true= lê Pcon)
EP_Type = False
# Potência Pico em W
Ppeak = 1000
# Intervalos de Preços
pmin = 140
pmax = 200
pcurr = 150
# Identifica o intervalo de tempo de ação em segundos e o período de tempo em minutos
TimeStep = 60
Period = 30
choice = 1

# Variáveis auxiliares
i = 0
Pbat = 0
Pbat_in = 0

PCon = []
PPV = []
Pdiff = []

f = open("Databases/Consume.txt", "r")
lines = f.readlines()
Timetable = []
PCon_total = []
for x in lines:
    Timetable.append(x.split(",")[0])
    PCon_total.append(x.split(",")[8])
f.close()

f = open("Databases/SolarProduction.txt", "r")
lines = f.readlines()
PPV_total = []
for x in lines:
    PPV_total.append(x.split(",")[8])
f.close()

# Determina o periodo de ação
TimeIndex = Timetable.index("2022-02-20T15:00:00.000Z")
PCon = PCon_total[TimeIndex: TimeIndex + Period]
PCon = list(map(float, PCon))
print(PCon)
PPV = PPV_total[TimeIndex: TimeIndex + Period]
PPV = list(map(float, PPV))
print(PPV)

Pdiff = np.array(PCon) - np.array(PPV)
Pgrid_in = Pdiff[i]

while i < Period:
    # Simula a leitura da potência da rede
    Pgrid_in = Pdiff[i] + Pbat_in
    # Determina trânsito de potência de acordo com o tipo de quadro
    if EP_Type:
        Pgrid = PCon[i] - PPV[i] + Pbat_in
    else:
        Pgrid = Pgrid_in

    match choice:
        case 1:  # Ativa a função Peak Shaving
            [Pbat_in, SoC] = use_cases.peak_shaving(Ppeak, Pgrid, Pbat_in, [SoC, SoC_min, SoC_max], Cap, TimeStep, Pch_max, Pdh_max)
        case 2:  # Ativa a função Self_Consumption
            [Pbat_in, SoC] = use_cases.self_consumption(Pgrid, Pbat_in, [SoC, SoC_min, SoC_max], Cap, TimeStep, Pch_max, Pdh_max)
        case 3:  # Ativa a função ToU
            [Pbat_in, SoC] = use_cases.tou_tariff(Pgrid, Pbat_in, [SoC, SoC_min, SoC_max], Cap, TimeStep, Pch_max, Pdh_max, [pcurr, pmin, pmax])

    print(Pbat_in)
    print(SoC)
    i = i + 1
