class UseCasesHuawei:
    def peak_shaving(Ppeak, Pgrid, Pbat_in, SoC, Cap, TimeStep, Pch_max, Pdh_max):
        # Determina a potência da bateria necessária
        Pdelta = Ppeak - Pgrid
        Pbat = Pbat_in + Pdelta
        Pbat = max(min(Pch_max, Pbat), Pdh_max)
        # Determina o SoC futuro
        SoC_next = (SoC[0] * Cap / 100 + Pbat * (TimeStep / 3600)) * 100 / Cap

        # Verifica se está dentro dos intervalos do SoC
        if SoC[1] > SoC_next or SoC_next > SoC[2] or (SoC_next > 50 and Pbat > 0):
            Pbat = 0
            SoC_next = SoC[0]

        return [Pbat, SoC_next]

    def self_consumption(Pgrid, Pbat_in, SoC, Cap, TimeStep, Pch_max, Pdh_max):
        # Determina a potência da bateria necessária
        Pdelta = Pgrid - Pbat_in
        Pbat = -Pdelta
        Pbat = max(min(Pch_max, Pbat), Pdh_max)
        # Determina o SoC futuro
        SoC_next = (SoC[0] * Cap / 100 + Pbat * (TimeStep / 3600)) * 100 / Cap

        # Verifica se está dentro dos intervalos do SoC
        if SoC[1] > SoC_next or SoC_next > SoC[2]:
            Pbat = 0
            SoC_next = SoC[0]

        return [Pbat, SoC_next]

    def tou_tariff(Pgrid, Pbat_in, SoC, Cap, TimeStep, Pch_max, Pdh_max, prices):
        # Determina a potência da bateria necessária
        Pdelta = Pgrid - Pbat_in
        # Faz as comparações dos códigos
        if prices[0] < prices[1]:
            Pbat = Pch_max
        elif prices[0] > prices[2]:
            Pbat = Pdh_max
        elif Pdelta <= 0:
            Pbat = -Pdelta
        else:
            Pbat = 0

        # Determina o SoC futuro
        SoC_next = (SoC[0] * Cap / 100 + Pbat * (TimeStep / 3600)) * 100 / Cap

        # Verifica se está dentro dos intervalos do SoC
        if SoC[1] > SoC_next or SoC_next > SoC[2]:
            Pbat = 0
            SoC_next = SoC[0]

        return [Pbat, SoC_next]
