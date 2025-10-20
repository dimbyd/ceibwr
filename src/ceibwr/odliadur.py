# odliadur.py
'''
Dulliau regex am ddarganfod odlau.

TODO: mae angen newid regex am prawf_odl etc.
'''
import os
import re
import json

from ceibwr.settings import GEIRIADURON

from ceibwr.cysonion import (
    str_llafariaid_byrion,
    cytseiniaid,
    eithriadau,
)

from ceibwr.gair import Gair

geirfa = GEIRIADURON['default']['GEIRFA']       # txt
odliadur = GEIRIADURON['default']['ODLIADUR']   # json

geiriau_lluosill_acennog = eithriadau['geiriau_lluosill_acennog']


class Geirfa():
    def __init__(self, s):

        # type check
        if type(s) is str:
            s = s.split(os.linesep)
        elif not type(s) is list and all([type(x) is str for x in s]):
            raise TypeError("Mae angen `str` neu `list[str]` fan hyn.")

        self.geiriau = [Gair(x) for x in s if len(x) > 0 and not x.isspace()]

        # write


class Odliadur():
    def __init__(self, geirfa, llusg=False):

        # type check
        if type(geirfa) is not Geirfa:
            raise TypeError("Mae angen `Geirfa` fan hyn.")

        self.geirfa = geirfa
        self.odlau = {}
        for idx, gair in enumerate(self.geirfa.geiriau):
            if idx % 1000 == 0:
                print('.', end='')
            odl = gair.children[-1].odl()
            qstr = str(odl)
            self.odlau[gair] = odl_search(qstr)

    def odlau(self, qstr):
        q = Gair(qstr)
        return self.odlau[q]

    def as_dict(self):
        od = {}
        for key, val in self.odlau.items():
            od[str(key)] = [str(x) for x in val]
        return od

    # write
    def export(self, fname):
        # convert to str

        s = json.dumps(self.as_dict(), indent=4, ensure_ascii=False)
        with open(fname, 'w') as f:
            f.write(s)


def odl_search(qstr, llusg=False, acennog=False):
    '''
    TODO: mae angen cysefeillio deuseiniaid tra'n
    chwilio drwy geiriadur JGJ

    TODO: derbyn `Gair` fel input. Bydd eisioes wedi ei
    hollti mewn i sillafau a gyda ffwythiant i adrodd
    ei aceniad. Hefyd mae angen cymharu yn ol sain, yn
    hytrach na text. 

    Bydd hyn yn araf, fel y cleciadur, felly mae
    angen creu "geiriadur" o wrthrychau `Gair`, ac ar
    sail hyn creu `dict` mawr, un entry ar gyfer pob
    `Gair` (key), wedi mapio yn erbyn rhestr geiriau 
    sy'n odli gydag ef. Bydd mao wahanol am odlau llusg, 
    ac un arall am eiriau sy'n cynganeddu. 
    
    Beth am e.e.
    lookup = {
        "afal": {
            odlog: [],
            llusg_odlog: [],
            cynganeddog: [],
            proest_gynganeddog: [],
        }
    }

    O ran odlau, mae pob query drwy `prawf_odl` yn cymryd
    tua 1s, mae just angen iteru dros yr holl endings posib
    easy peasy!

    'Run peth gyda cleciau, ond bydd angen mynd drwy pob 
    gair (~26,000) yn hytrach na phob ending (~200)
    '''
    # type check
    if type(qstr) is not str:
        raise TypeError("Mae angen `str` fan hyn.")

    # safoni
    qstr = qstr.lower()

    # defnyddio odliadur RS am odlau syml
    if not llusg:
        # import json
        # with open(odliadur_file, "r") as infile:
        #     odliadurRS = json.load(infile)
        if qstr in odliadur:
            odlau = odliadur[qstr]
            if acennog:
                odlau = [s for s in odlau if Gair(s).is_acennog()]
            return odlau if odlau else []

    # defnyddio geiriau JGJ am odlau llusg
    # Ar ol cymathu, gallwn ni just dorri'r sillaf olaf i ffwrddd
    llaf = '|'.join(str_llafariaid_byrion)
    cyts = '|'.join(cytseiniaid)
    if llusg:
        p = r'\b[a-z]*' + r'[' + cyts + r']+' + qstr + r'[' + llaf + r']+[' + cyts + ']*' + r'\b'
    else:
        p = r'\b[a-z]*' + qstr + r'\b'

    # with open(geirfa_file) as f:
    #     s0 = f.read()
    # odlau = re.findall(p, s0)
    odlau = re.findall(p, ' '.join(geirfa))

    # does dim odlau llusg mewn geiriau acennog!!
    if acennog:
        odlau = [s for s in odlau if Gair(s).is_acennog()]
    return odlau


# def test_geiriadur(x):
#     '''
#     Creu odliadur newydd o eiriau JGJ. Mae hwn yn creu
#     gwrthrychau `Gair` ac felly dylai gael yr acennu yn
#     iawn o leiaf (sy'n bwysg am cleciau, pa fantais am
#     odlau?)
#     '''

#     if not type(x) is Gair:
#         raise TypeError("Mae angen `Gair` fan hyn.")

#     qstr = str(x[-1].odl())

#     # llaf = '|'.join(str_llafariaid_byrion)
#     # cyts = '|'.join(cytseiniaid)
#     p = r'\b[a-z]*' + qstr + r'\b'

#     with open(geirfa_file) as f:
#         s0 = f.read()

#     import time
    
#     # RS
#     import json
#     with open(odliadur_file, "r") as infile:
#         odliadurRS = json.load(infile)

#     start = time.time()
#     if qstr in odliadurRS:
#         odlog = odliadurRS[qstr]
#     print('odlogRS:', odlog)
#     print(len(odlog))
#     end = time.time()
#     print(end - start)

#     # regexp (0.0003s)
#     odlog = re.findall(p, s0)
#     print('odlog:', odlog)
#     print(len(odlog))
#     end = time.time()
#     print(end - start)

#     from ceibwr.datryswr_odl import prawf_odl_sylfaenol

#     # creu `Gair` objects (1.025s)
#     start = time.time()
#     geiriau = [Gair(s) for s in s0.split()]
#     q = Gair(qstr)
#     odlog2 = [gair for gair in geiriau if gair[-1].odl().sain() == qstr ]
#     odlog2 = []
#     for gair in geiriau:
#         odlau = prawf_odl_sylfaenol(q, gair)
#         if odlau and odlau.dosbarth in ('ODL', 'OLA'):
#             odlog2.append(gair)

#     print('odlog2:', [str(x) for x in odlog2])
#     print(len(odlog2))
#     end = time.time()
#     print(end - start)


def main():

    # create
    geirfa_file = "/Users/scmde/ceibwr/src/ceibwr/data/geirfaJGJ.txt"
    with open(geirfa_file) as f:
        s = f.read()

    # print("==============================================")
    # print(s)

    print("==============================================")
    ge = Geirfa(s)
    print(ge)

    print("==============================================")
    od = Odliadur(ge)
    print(od)

    qstr = 'ydd'
    print('qstr:', qstr)

    outname = "/Users/scmde/ceibwr/src/ceibwr/data/odliadurJGJ.json"
    od.export(outname)

    # check
    od2 = json.load(outname)
    print((od2))
    return

    # s = 'cariad'
    # s = 'nant'
    # s = 'ffenest'
    s = 'afon'
    # s = 'corrach'
    # s = 'afiach'
    # s = 'afal'
    # s = 'tro'

    query = Gair(s)

    # odlau = test_geiriadur(query)

    # return 0

    print('YMHOLIAD: {}'.format(s))

    odl = str(query.children[-1].odl())
    print('odl: ' + odl)

    # odlau cyffredin
    odlau = odl_search(odl)
    print('\nODLAU:\n' + '  '.join(odlau))

    # print(Gair('llo').is_acennog())

    # # odlau acennog yn unig
    # odlau = odl_search(s, acennog=True)
    # print('\nODLAU ACENNOG:\n' + ' '.join(odlau))

    # # odlau llusg
    # odlau = odl_search(s, llusg=True)
    # print('\nODLAU LLUSG:\n' + ' '.join(odlau))


if __name__ == '__main__':
    main()
