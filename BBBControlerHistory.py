def InitizalizeHistory():

    HistoryHeader = ['F',',','LP',',','PPS',',','id',',','Cap',',','PDMax',',',
                    'PCMax',',','RT',',','AT',',','PCon',',','PPV',',','Pbat',
                    ',','PG',',','SoC',',','SoCMin']

    History = open("History.txt",'w')
    History.writelines(HistoryHeader)
    History.write("\n")

    return History