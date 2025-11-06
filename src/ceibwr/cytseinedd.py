# cytseinedd.py
'''
Gwrthrych `Cytseinedd` sef `dict` o cytsain:dosbarth

Gall berthyn i wrthrychau `Cynghanedd` yn unig.
'''


from ceibwr.cysonion import llythrenwau
enwau = llythrenwau['cytsain']


class Cytseinedd():
    '''
    Cofnod cytseinedd.
    Gall hyn berthyn i raniad `Cynghanedd` yn unig,

    Dosbarthiadau cytseinedd
    CRO     gefyll
    TRA     gefyll + canolgoll
    GWG     gefyll + gwreiddgoll
    COG     gefyll + cyswllt
    PGO     corfan bengoll
    LLA     dim cyfatebiaeth o flaen yr acen (dan yr acen yn unig)

    '''
    def __init__(self):

        self.dosbarth = None

        self.gefyll = []
        self.gwreiddgoll = []
        self.canolgoll = []
        self.pengoll = []

        self.special = {}
        self.hysbys = []

    def __str__(self):
        s = [self.dosbarth]
        s.append('GEF: ' + str(self.gefyll))
        s.append('GWG: ' + str(self.gwreiddgoll))
        s.append('CAG: ' + str(self.canolgoll))
        s.append('PEG: ' + str(self.pengoll))
        for key, val in self.special.items():
            s.append(val + ': ' + str(key))
        return '\n'.join(s)

    def dosbarth_cytsain(self, nod):
        if nod in self.special:
            return self.special[nod]
        elif nod in [x for tup in self.gefyll for x in tup]:
            return 'GEF'
        elif nod in self.gwreiddgoll:
            return 'GWG'
        elif nod in self.canolgoll:
            return 'CAG'
        elif nod in self.pengoll:
            return 'PEG'
        else:
            return None

    def nodau(self):
        nodau = [nod for tup in self.gefyll for nod in tup]
        return nodau + self.gwreiddgoll + self.canolgoll + self.pengoll

    def lookup(self):
        return {nod: self.dosbarth_cytsain(nod) for nod in self.nodau()}
        # lookup = {}
        # for tup in self.gefyll:
        #     for nod in tup:
        #         lookup[nod] = 'GEF'
        # for nod in self.gwreiddgoll:
        #     lookup[nod] = 'GWG'
        # for nod in self.canolgoll:
        #     lookup[nod] = 'TRA'
        # return lookup | self.special

    def dosbarth_cytseinedd(self):
        """
        TODO: duplicate: self.dosbarth is set
        by datryswr_cytseinedd()
        """

        # 0. dim cyfatebiaeth
        if not self.gefyll:
            dosbarth = 'LLA'

        # 1. croes (cyfatebiaeth union)
        elif not self.gwreiddgoll and not self.canolgoll:
            dosbarth = "CRO"

        # 2. croes wreiddgoll
        elif self.gwreiddgoll and not self.canolgoll:

            # croes n-wreidgoll
            if len(self.gwreiddgoll) == 1 and self.gwreiddgoll[0].text.lower() == "n":
                dosbarth = "CRO"

            elif len(self.gwreiddgoll) > 0:
                dosbarth = 'CWG'

        # 3. traws
        elif not self.gwreiddgoll and self.canolgoll:

            # croes n-ganolgoll
            if len(self.canolgoll) == 1 and self.canolgoll[0].text.lower() == "n":
                dosbarth = "CRO"
            
            # traws
            else:
                dosbarth = "TRA"

        # 4. traws wreiddgoll
        elif self.gwreiddgoll and self.canolgoll:
            if len(self.gwreiddgoll) == 1 and self.gwreiddgoll[0].text.lower() == "n":
                dosbarth = "TRA"
            else:
                dosbarth = "TWG"

        return dosbarth


def main():
    cyts = Cytseinedd()
    cyts.dosbarth = 'CRO'
    
    from ceibwr.nod import Nod
    nod1 = Nod('d')
    nod2 = Nod('ch')
    cyts.gefyll.append((nod1, nod2))
    nod3 = Nod('s')
    cyts.canolgoll.append(nod3)

    print(cyts)

    print('----------')
    print(cyts.lookup())


if __name__ == "__main__":
    main()
