# odliadur.py
'''
Dulliau regex am ddarganfod odlau.

TODO: mae angen newid regex am prawf_odl etc.
'''
import re
from ceibwr.settings import DATABASES

from ceibwr.cysonion import (
    str_llafariaid_byrion,
    cytseiniaid,
    eithriadau,
)

from ceibwr.gair import Gair

odliadur_file = DATABASES['default']['ODLIADUR']    # json
geirfa_file = DATABASES['default']['GEIRFA']  # txt

geiriau_lluosill_acennog = eithriadau['geiriau_lluosill_acennog']
# deuseiniaid["hiatus"] = eithriadau['hiatus']


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

    # defnyddio odliadur RS am odlau syml
    if not llusg:
        import json
        with open(odliadur_file, "r") as infile:
            odliadurRS = json.load(infile)
        if qstr in odliadurRS:
            odlog = odliadurRS[qstr]
            if acennog:
                odlog = [s for s in odlog if Gair(s).is_acennog()]
            return odlog if odlog else []

    # defnyddio geiriau JGJ am odlau llusg
    # Ar ol cymathu, gallwn ni just dorri'r sillaf olaf i ffwrddd
    llaf = '|'.join(str_llafariaid_byrion)
    cyts = '|'.join(cytseiniaid)
    if llusg:
        p = r'\b[a-z]*' + r'[' + cyts + r']+' + qstr + r'[' + llaf + r']+[' + cyts + ']*' + r'\b'
    else:
        p = r'\b[a-z]*' + qstr + r'\b'

    with open(geirfa_file) as f:
        s0 = f.read()

    odlog = re.findall(p, s0)
    # print('odlog:', odlog)

    # does dim odlau llusg mewn geiriau acennog!!
    if acennog:
        odlog = [s for s in odlog if Gair(s).is_acennog()]
    return odlog


def test_geiriadur(x):
    '''
    Creu odliadur newydd o eiriau JGJ. Mae hwn yn creu
    gwrthrychau `Gair` ac felly dylai gael yr acennu yn
    iawn o leiaf (sy'n bwysg am cleciau, pa fantais am
    odlau?)
    '''

    if not type(x) is Gair:
        raise TypeError("Mae angen `Gair` fan hyn.")

    qstr = str(x[-1].odl())

    # llaf = '|'.join(str_llafariaid_byrion)
    # cyts = '|'.join(cytseiniaid)
    p = r'\b[a-z]*' + qstr + r'\b'

    with open(geirfa_file) as f:
        s0 = f.read()

    import time
    
    # RS
    import json
    with open(odliadur_file, "r") as infile:
        odliadurRS = json.load(infile)

    start = time.time()
    if qstr in odliadurRS:
        odlog = odliadurRS[qstr]
    print('odlogRS:', odlog)
    print(len(odlog))
    end = time.time()
    print(end - start)

    # regexp (0.0003s)
    odlog = re.findall(p, s0)
    print('odlog:', odlog)
    print(len(odlog))
    end = time.time()
    print(end - start)

    from ceibwr.datryswr_odl import prawf_odl_sylfaenol

    # creu `Gair` objects (1.025s)
    start = time.time()
    geiriau = [Gair(s) for s in s0.split()]
    q = Gair(qstr)
    odlog2 = [gair for gair in geiriau if gair[-1].odl().sain() == qstr ]
    odlog2 = []
    for gair in geiriau:
        odlau = prawf_odl_sylfaenol(q, gair)
        if odlau and odlau.dosbarth in ('ODL', 'OLA'):
            odlog2.append(gair)

    print('odlog2:', [str(x) for x in odlog2])
    print(len(odlog2))
    end = time.time()
    print(end - start)


def main():
    # s = 'cariad'
    # s = 'nant'
    # s = 'ffenest'
    s = 'afon'
    # s = 'corrach'
    # s = 'afiach'
    # s = 'afal'
    # s = 'tro'

    query = Gair(s)

    odlau = test_geiriadur(query)

    return 0

    print('YMHOLIAD: {}'.format(s))


    odl = str(query.children[-1].odl())
    print('odl: ' + odl)

    # odlau cyffredin
    odlau = odl_search(odl)
    print('\nODLAU RS:\n' + '  '.join(odlau))

    print(Gair('llo').is_acennog())

    # odlau acennog yn unig
    odlau = odl_search(s, acennog=True)
    print('\nODLAU ACENNOG:\n' + ' '.join(odlau))

    # odlau llusg
    odlau = odl_search(s, llusg=True)
    print('\nODLAU LLUSG:\n' + ' '.join(odlau))


if __name__ == '__main__':
    main()
