# cytseinedd.py
'''
Gwrthrych `Cytseinedd` sef `dict` o cytsain:dosbarth

Gall berthyn i wrthrychau `Cynghanedd` yn unig.
'''


from ceibwr.cysonion import llythrenwau
enwau = llythrenwau['cytsain']


class Cytseinedd(dict):
    '''
    Cofnod cytseinedd.
    Gall hyn berthyn i raniad `Cynghanedd` yn unig,

    CRO     cyfatebol
    TRA     cyfatebol + canolgoll
    GWG     cyfatebol + gwreiddgoll
    COG     cyfatebol + cyswllt
    PGO     corfan bengoll
    LLA     cyfateb dan yr acen yn unig

    '''
    def __init__(self):
        pass
        self.dosbarth = None
        self.hysbys = []

    def __str__(self):
        dosb_str = llythrenwau['cynghanedd'][self.dosbarth]
        s = [dosb_str]
        for dosb in llythrenwau['cytsain']:
            nodau = self.nodau(dosb)
            if nodau:
                s.append(llythrenwau['cytsain'][dosb] + ': ' + str(nodau))
        return '\n'.join(s)

    def nodau(self, val):
        return [k for k, v in self.items() if v == val]

    def dosbarth_cytseinedd(self):
        x_blaen = [k for k, v in self.items() if v == 'GWG']
        y_blaen = [k for k, v in self.items() if v == 'TRA']
        clecs = [k for k, v in self.items() if v == 'GEF']

        # 0. dim cyfatebiaeth
        if not clecs:
            dosbarth = 'LLA'

        # 1. croes (cyfatebiaeth union)
        elif not x_blaen and not y_blaen:
            dosbarth = "CRO"

        # 2. croes wreiddgoll
        elif x_blaen and not y_blaen:

            # croes n-wreidgoll
            if len(x_blaen) == 1 and x_blaen[0].text.lower() == "n":
                dosbarth = "CRO"

            elif len(x_blaen) > 0:
                dosbarth = 'CWG'

        # 3. traws
        elif not x_blaen and y_blaen:

            # croes n-ganolgoll
            if len(y_blaen) == 1 and y_blaen[0].text.lower() == "n":
                dosbarth = "CRO"
            
            # traws
            else:
                dosbarth = "TRA"

        # 4. traws wreiddgoll
        elif x_blaen and y_blaen:
            if len(x_blaen) == 1 and x_blaen[0].text.lower() == "n":
                dosbarth = "TRA"
            else:
                dosbarth = "TWG"

        return dosbarth


def main():
    cytseinedd = Cytseinedd()
    cytseinedd.dosbarth = 'CRO'
    
    from ceibwr.nod import Nod
    nod1 = Nod('d')
    cytseinedd[nod1] = 'GEF'
    nod2 = Nod('ch')
    cytseinedd[nod2] = 'CYS'
    nod3 = Nod('s')
    cytseinedd[nod3] = 'PEG'

    print(cytseinedd)
    print(cytseinedd.dosbarth)

    # print(cytseinedd.gefelliaid)
    print(cytseinedd.nodau('GEF'))


if __name__ == "__main__":
    main()
