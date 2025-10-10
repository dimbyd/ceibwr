# cleciadur.py
'''
Chwillio am eiriau sy'n cynganeddu.
'''

from ceibwr.settings import DATABASES
from ceibwr.cysonion import eithriadau

from ceibwr.gair import Gair

from ceibwr.datryswr_cytseinedd import prawf_cytseinedd

odlau_file = DATABASES['default']['ODLIADUR']    # json
geirfa_file = DATABASES['default']['GEIRFA']  # txt

geiriau_lluosill_acennog = eithriadau['geiriau_lluosill_acennog']


def clec_search(s):
    """
    Darganfod geiriau sy'n cynganeddu.

    :param s: query string
    :type s: str
    :return: matches
    :rtype: list[str]

    """
    x = Gair(s)

    # geirfa
    with open(geirfa_file, encoding='utf-8-sig') as f:
        s0 = f.read()
        geirfa = s0.strip().split('\n')

    clecs = {
        'CAC': [],
        'CDI': [],
        'AAC': [],
        'ADI': [],
    }

    for s2 in geirfa:
        y = Gair(s2)
        
        # anwybyddu AAC
        if not x.is_acennog() and y.is_acennog():
            pass
        
        # reject odl dan yr acen
        # odlau = prawf_odl_sylfaenol(x.prif_sillaf(), y.prif_sillaf())
        # if odlau and odlau.dosbarth in ('ODL', 'OLA'):
        #     continue
        
        # reject yr un llafariaid dan yr acen
        if x.prif_sillaf().cnewyllyn().sain() == y.prif_sillaf().cnewyllyn().sain():
            continue

        # TODO: mwy o brofion?
        
        # x ar yr orffwysfa
        cyts = prawf_cytseinedd(x, y)
        if cyts.dosbarth and cyts.dosbarth == 'CRO':
            if x.is_acennog() and y.is_acennog():
                clecs['CAC'].append(str(y))
            elif x.is_acennog() and not y.is_acennog():
                clecs['ADI'].append(str(y))
            elif not x.is_acennog() and y.is_acennog():
                clecs['AAC'].append(str(y))
            else:
                clecs['CDI'].append(str(y))
        
        # x ar y diwedd
        cyts2 = prawf_cytseinedd(y, x)
        if cyts2.dosbarth and cyts2.dosbarth == 'CRO':
            if x.is_acennog() and not y.is_acennog():
                clecs['AAC'].append(str(y))
            elif not x.is_acennog() and y.is_acennog():
                clecs['ADI'].append(str(y))

    return clecs


def main():
    s = 'cariad'
    s = 'cor'
    # s = 'ffenest'
    # s = 'afon'
    # s = 'corrach'

    print('YMHOLIAD: {}'.format(s))
    print()
    clecs = clec_search(s)
    for key, val in clecs.items():
        print(f'{key}:, {val}')


if __name__ == '__main__':
    main()
