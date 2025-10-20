# prawf_cwpled.py
'''
GPC: "cwpled" = dwy linell olynol o farddoniaeth
Mae'r term felly hefyd yn cynnwys toddeidiau

CWP -- CCA --- CCY
               --- CC4
               --- CC7
               --- CAG 
           --- TOD

CCA = Cwpled Caeth
CCY = Cwpled Cywydd (aceniad AD neu DA)
CC4/CC7 = odl
CAG: odl + odl gyrch (?)

HAT = [CCA10 CCA10, TOD]
Mae cwpled cywydd angen amrywio'r aceniad
ond nid felly am y cwpledi ddegsill mewn HAT

Cwpled Cywydd Bedairsill    CC4
Cwpled Cywydd Seithsill     CC7
Cwpled Awdl-Gywydd:         CAG

Cwpled Cyhydedd Hir:        CCH
Cwpled Rhupunt Byr:         CRB
Cwpled Rhupunt Hir:         CRH

TODO:
Llinell/Cwpled Cyhydedd Hir
LLCH: [CNG5, CNG5, CNG5, XX4]  # y tri rhan gyntaf yn odli

Mae bob amser angen dwy linell o gyhydedd hir
er mwyn ateb y brifodl (h.y. cwpled)

CCH = [LLCH, LLCH]

Felly hefyd am linellau unigol o RHB, RHH ...

Mae dwy linell o RHB/RHH yn ffurfio Cwpled.
    CRB: [LLRB, LLRB] = 2 x 12 = 2 x (4, 4, 4)
    CRH: [LLRH, LLRH] = 2 x 16 = 2 x (4, 4, 4, 4)

LLRB: [c1, c2, c3]
    - pob corfan yn bedairsill (cyfanswm o 12 sill)
    - ODL(c1, c2)
    - CRO(c2, c3) neu TRA(c2, c3)
    - equiv: SAI(c1, c2, c3)

LLRH: [c1, c2, c3, c4]
    - pob corfan yn bedairsill (cyfanswm o 16 sill)
    - ODL(c1, c2, c3)
    - CRO(c1, c2) neu TRA(c3, c4)
    - equiv SDO(c1, c2, c3, c4)

Cyhydedd Nawban: [c1, c2, c3, c4]
    - pedair llinell nawsill
    - CNG9(c1), CNG9(c2), CNG9(c3), CNG9(c4)
    - ODL(c1, c2, c3, c4)

LLCH: [c1, c2, c3, c4]
    - y tri rhan gyntaf yn bumsill, yr olaf yn bedairsill
    - ODL(c1, c2, c3)
    - CNG(c1), CNG(c2), CNG(c3)

TOB: [c1, c2]
    - c1: CNG7|CNG8|CNG9
    - c2: CBG9|CBG8|CBC7 neu SAI9|SAI8|SAI7
    - odl(c1, c2)

    TOD: [c1, c2]
    - c1: CBG7+3, CBG8+2, CBG9+1
    - c2: CNG9
    - ODL(c1[-1], c2[0])  # odl gyrch

TOH: [c1, c2]
    - c1: CBG7+3, CBG8+2, CBG9+1
    - c2: CNG10
    - ODL(c1[-1], c2[0])  # odl gyrch

Gwawdodyn Byr/Hir ??

TODO: Anghysondeb teiposod.

1. Caiff llinell o Gyhydedd Hir ei ysgrifennu mewn sawl ffordd:
a)
    c1 + c2 + c3 + c4 (dim yn aml gan fod 19 sillaf)
b)
    c1 + c2
    c3 + c4
c)
    c1
    c2
    c3 + c4

AYG t.143 : "Dwy linell o gyhydedd hir sy'n gwneud un pennill fel arfer"
Gallai yn feddwl 2, 4 neu 6 o linellau ar y sgrin

2. Felly hefyd am linell o Rupunt Byr (4 + 4 + 4):
a)
    c1 + c2 + c3
b)
    c1
    c2
    c3

Rhaniad heb gynghanedd: (None, [c1, c2, ...])
Rhaniad heb gwpled:
(None,
    (TRA7, [c1, c2]),
    (None, [c3, c4]),
)

Convention:
Mae'r ffwythiannau `datrys_xxx` yn delio gyda'r goeden text
Mae'r ffwythiannau `prawf_xxx` yn delio gyda'r goeden sain
'''

from ceibwr.datrysiad import Datrysiad, Amwys

from ceibwr.cynghanedd import Cynghanedd, Llusg, Sain
from ceibwr.cynghanedd import CroesBengoll, TrawsBengoll, LlusgBengoll, SainBengoll

import ceibwr.cwpled as cwpled

from ceibwr.datryswr_odl import prawf_odl
from ceibwr.datryswr_cynghanedd import prawf_cynghanedd, best_guess

from ceibwr.rhaniad import Trychwr  # am TOB


def prawf_cwpled(x1, x2):
    '''
    Omnibus test
    input:   [`Rhaniad`, `Rhaniad`]
    output:  `Datrysiad`

    CC7: (TRA7, SAI7)
    TOB: (TBG10, None6) + odl_check
    TOD: (TBG10, CNG9) + odl_check
    TOH: (TBG10, CNG10) + odl_check
    '''

    if not isinstance(x1, Datrysiad) or not isinstance(x2, Datrysiad):
        raise TypeError("Mae angen dau `Datrysiad` fan hyn.")

    # --------------------
    # 1. Cwpled Cywydd neu Awdl-Gywydd
    CPG = (CroesBengoll, TrawsBengoll, LlusgBengoll, SainBengoll)
    if (
        not isinstance(x1, CPG) and
        not isinstance(x2, CPG) and
        isinstance(x1, Cynghanedd) and
        isinstance(x2, Cynghanedd) and
        not isinstance(x2, Llusg)
     ):

        # check odl gyrch (CAG)
        odlau_cyrch = prawf_odl(x1.gair_olaf(), x2[0].gair_olaf())
        if odlau_cyrch and x1.nifer_sillafau() == 7 and x2.nifer_sillafau() == 7:
            return cwpled.CwpledAwdlGywydd(x1, x2, odlau=odlau_cyrch)

        # check odl diweddol (CC7, CC4)
        odlau = prawf_odl(x1.gair_olaf(), x2.gair_olaf())
        if odlau:
            if (
                (x1.is_acennog() and not x2.is_acennog()) or
                (not x1.is_acennog() and x2.is_acennog())
            ):
                if x1.nifer_sillafau() == 7 and x2.nifer_sillafau() == 7:
                    return cwpled.CwpledCywyddSeithsill(x1, x2, odlau=odlau)

                elif x1.nifer_sillafau() == 4 and x2.nifer_sillafau() == 4:
                    return cwpled.CwpledCywyddBedairsill(x1, x2, odlau=odlau)

    # --------------------
    # 2. Prawf Toddaid (TOB/TOD/TOH)

    if (
        isinstance(x1, Cynghanedd) and
        x1.dosbarth in ('CBG', 'TBG', 'LBG', 'SBG')
     ):
        # check nifer sillafau
        nifer_cyrch = x1[-1].nifer_sillafau()
        nifer_blaen = x1.nifer_sillafau() - nifer_cyrch
        nifer_nesaf = x2.nifer_sillafau()

        if (
            nifer_blaen in (7, 8, 9) and
            nifer_cyrch in (1, 2, 3) and
            nifer_blaen + nifer_cyrch == 10 and
            nifer_nesaf in (6, 9, 10)
        ):
            # check cynghanedd rhan gyntaf y linell gyntaf
            x11 = prawf_cynghanedd(x1[:-1])

            # check prif odlau (x11, x2)
            odlau = prawf_odl(x11[-1].gair_olaf(), x2[-1].gair_olaf())

            # Toddaid, Toddaid Hir
            if nifer_nesaf in (9, 10):

                # check odl gyrch
                odlau_cyrch = prawf_odl(x1.gair_olaf(), x2[0].gair_olaf())

                if odlau and odlau_cyrch and (
                    isinstance(x11, Cynghanedd) and
                    isinstance(x2, Cynghanedd) and
                    not isinstance(x2, Llusg)
                ):
                    if nifer_nesaf == 9:
                        return cwpled.Toddaid(x1, x2, odlau, odlau_cyrch)
                    else:
                        return cwpled.ToddaidHir(x1, x2, odlau, odlau_cyrch)

            # Toddaid Byr
            else:

                # cyfuno'r cyrch a'r ail linell
                geiriau = x1[-1].geiriau() + x2.geiriau()

                # creu rhaniadau
                tr = Trychwr()
                rhaniadau = tr.rhaniadau(geiriau, min_rhannau=3, max_rhannau=3)
                
                # CBG/TBG/SAI yn OK
                # TODO: Sain Alun: mae pedwar corfan!
                dats = []
                for rhaniad in rhaniadau:

                    # check am SAI neu CBG/TBG/SBG
                    dat = prawf_cynghanedd(rhaniad, pengoll=True)
                    
                    # print('dat:', repr(dat))
                    if isinstance(dat, Sain):
                        dats.append(dat)
                    
                    elif type(dat) in [CroesBengoll, TrawsBengoll]:
                        dats.append(dat)
                
                # print('dats:', dats)
                    
                dat3 = None
                if len(dats) > 0:
                    dat3 = best_guess(dats, cyfuno=False)
                
                if x1 and dat3:
                    return cwpled.ToddaidByr(x11, dat3, odlau)

    # end: cwpled syml
    odlau = prawf_odl(x1.gair_olaf(), x2.gair_olaf())
    if odlau:
        if (
            isinstance(x1, Cynghanedd) and
            isinstance(x2, Cynghanedd)
        ):
            return cwpled.CwpledCaeth(x1, x2, odlau)

        return cwpled.Cwpled(x1, x2, odlau)

    return Amwys([x1, x2])


# ------------------------------------------------
# main
def demo():
    '''
    Mae seinyddio ar draws llinellau yn dodgy.
    Mae hyn siwr o fod yn wir am seinyddio ar draws brawddegau.
    h.y. mae atalnod llawn yn ddigon o "pause" i'w stopio.
    '''

    from ceibwr.profion_cwpled import profion

    from ceibwr.llinell import Llinell
    from ceibwr.datryswr_llinell import datryswr_llinell

    from ceibwr.beiro import Beiro
    from ceibwr.seinyddwr import Seinyddwr
    from ceibwr.cysonion import colormaps

    se = Seinyddwr()
    beiro = Beiro()
    cmap = colormaps['default']

    profion['problem'] = (

        (
            "Daeth i'r lofa dalog swyddogion,",
            "A mud weithwyr lle bu cymdeithion.",
        ),
    )

    for key in [
        # 'cwpled',
        # 'cwpled_cywydd_seithsill',
        # 'cwpled_cywydd_bedairsill',
        # 'cwpled_awdl_gywydd',
        # 'toddaid_byr',
        # 'toddaid',
        # 'toddaid_hir',
        'problem',
    ]:
        print()
        print('========================================')
        print(beiro.magenta(key.upper()))
        print('========================================')
        # print(profion[key])

        for z1, z2 in profion[key]:

            # creu llinellau
            z1 = Llinell(z1)
            z2 = Llinell(z2)
            se.seinyddio_llinell(z1)
            se.seinyddio_llinell(z2)

            # datrys fesul llinell
            x1 = datryswr_llinell(z1, pengoll=True)
            x2 = datryswr_llinell(z2)

            x = prawf_cwpled(x1, x2)

            # print('x1:', repr(x1))
            # print('x2:', repr(x2))
            # print('x:', repr(x))

            print()
            print(x)
            print()
            print(repr(x))
            print()
            print(x.show_fancy(toriad='|', cmap=cmap))
            print(beiro.cyan(x.dosbarth) if x.dosbarth else beiro.coch('XXX'))
            print()
            print('--------------------')


if __name__ == '__main__':
    demo()
