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
