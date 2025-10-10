# prawf_rhaniad.py
"""
Dulliau darganfod cynghanedd mewn rhaniad.

Lefel 0: `Gair`
Lefel 1: `Corfan` sef rhestr geiriau
Lefal 2: `Rhaniad` sef rhestr corfannau (e.e. CRO, LLU)
  - mae angen darganfod rhaniadau dilys

"""

from ceibwr.corfan import Corfan
from ceibwr.rhaniad import Rhaniad
from ceibwr.datrysiad import Datrysiad, Amwys

from ceibwr.datryswr_cytseinedd import prawf_cytseinedd
from ceibwr.datryswr_odl import prawf_odl

from ceibwr.cysonion import blaenoriaeth

from ceibwr.cynghanedd import (
    Croes, CroesGyswllt, CroesWreiddgoll,
    Traws, TrawsFantach, TrawsWreiddgoll,
    Llusg, LlusgLafarog, LlusgDeirodl,
    Sain, SainLafarog, SainDeirodl, SainGyswllt, SainGadwynog, SainDdwbl,
    CroesBengoll, TrawsBengoll, LlusgBengoll, SainBengoll,
    Llafarog,
)

import logging
log = logging.getLogger(__name__)


def prawf_cynghanedd(rhaniad, unigol=True, pengoll=False, TAY=False):
    '''
    Omnibus test: darganfod, hidlo a cyfuno
    '''

    if isinstance(rhaniad, Rhaniad):
        rhaniad = rhaniad.children

    dats = prawf_cynghanedd_sylfaenol(rhaniad)

    if pengoll:
        datsPG = prawf_cynghanedd_bengoll(rhaniad)
        if datsPG:
            dats.extend(datsPG)

    dats = chwynnu(dats)
    if not dats:
        dats = [Amwys([Corfan([x for corfan in rhaniad for x in corfan])])]

    if unigol:
        return best_guess(dats)

    return dats


def prawf_cynghanedd_bengoll(rhaniad, unigol=False):
    '''
    Prawf cynganeddion pengoll.
    '''
    # type check
    if not type(rhaniad) is list:
        raise TypeError('Mae angen `list` fan hyn.')

    # value check
    if not all([isinstance(rhan, Corfan) for rhan in rhaniad]):
        raise TypeError('Mae angen `list[Corfan]` fan hyn.')

    # cyfyngu ar hyd y gorfan bengoll
    if rhaniad and rhaniad[-1].nifer_sillafau() > 4:
        return None

    dats = prawf_cynghanedd_sylfaenol(rhaniad[:-1])

    dats_pengoll = []
    for dat in dats:
        if isinstance(dat, Croes):
            dats_pengoll.append(CroesBengoll(rhaniad, cytseinedd=dat.cytseinedd))
        elif isinstance(dat, Traws):
            dats_pengoll.append(TrawsBengoll(rhaniad, cytseinedd=dat.cytseinedd))
        elif isinstance(dat, Llusg):
            dats_pengoll.append(LlusgBengoll(rhaniad, odlau=dat.odlau))
        elif isinstance(dat, Sain):
            dats_pengoll.append(SainBengoll(rhaniad, odlau=dat.odlau, cytseinedd=dat.cytseinedd))

    if dats_pengoll and unigol:
        prif_dat = best_guess(dats_pengoll)
        return prif_dat

    return dats_pengoll


def prawf_cynghanedd_sylfaenol(rhaniad, TAY=False):
    """
    Prawf cynghanedd

    Mewnbwn:    `Rhaniad` sylfaenol (h.y. o wrthrychau `Corfan`)
    Allbwn:     `Datrysiad`

    Mae'r union brawf yn dibynnu ar y nifer o gorfannau.

    ** Dau gorfan: x1, x2
    Croes/Traws:
        cytseinedd rhwng x1, x2
    Llusg:
        odl lusg rhwng x1, x2

    ** Tri chorfan: x1, x2, x3
    Sain:
        odl rhwng x1, x2
        cytseinedd rhwng x2, x3
    Llusg deirodl:
        odl rhwng x1, x2
        odl lusg rhwng x1/x2 a x3

    ** Pedwar corfan: x1, x2, x3, x4
    Sain gadwynog:
        odl rhwng x1, x3
        cytseinedd rhwng x2, x4
    Sain deirodl:
        odl rhwng x1, x2 a x3
        cytseinedd rhwng x3 a x4

    ** Pum corfan: x1, x2, x3, x4, x5
    Sain ddwbl
        sain rhwng x1, x2, x3
        sain rhwng x3, x4, x5
    """

    # type check
    if not all([type(elfen) is Corfan for elfen in rhaniad]):
        raise TypeError("Mae angen `Rhaniad` Lefel 1 fan hyn.")

    datrysiadau = []

    # alias
    nifer_corfannau = len(rhaniad)

    # ------------------------------
    # 2. dau gorfan: croes, traws a llusg
    if nifer_corfannau == 2:
        x1, x2 = rhaniad
        
        # dilysu
        if not x1 or not x2:
            raise ValueError("Mae angen dau gorfan anwag fan hyn.")

        # --------------------
        # 2.1 croes a thraws
        cyts12 = prawf_cytseinedd(x1, x2)

        # llwyddiant (mae angen cyfateb o leiaf un par o gytseiniaid)
        if cyts12 and cyts12.dosbarth and cyts12.dosbarth not in ['LLA']:
            if cyts12.dosbarth == 'CRO':
                dat = Croes(rhaniad, cyts12)
            elif cyts12.dosbarth == 'COG':
                dat = CroesGyswllt(rhaniad, cyts12)
            elif cyts12.dosbarth == 'CWG':
                dat = CroesWreiddgoll(rhaniad, cyts12)
            elif cyts12.dosbarth == 'TRA':
                dat = Traws(rhaniad, cyts12)
            elif cyts12.dosbarth == 'TFA':
                dat = TrawsFantach(rhaniad, cyts12)
            elif cyts12.dosbarth == 'TWG':
                dat = TrawsWreiddgoll(rhaniad, cyts12)
            else:
                dat = Llafarog(rhaniad, cyts12)

            # Hidlo cyfatebiaeth anghytbyws acennog (AAC)
            # Mae rhain yn iawn mewn cynghanedd sain.
            if not x1[-1].is_acennog() and x2[-1].is_acennog():
                pass
            else:
                datrysiadau.append(dat)  # cofnodi

        # --------------------
        # 2.2 Llusg
        odlau12 = prawf_odl(x1[-1], x2[-1], llusg=True, trwm_ac_ysgafn=TAY)

        if odlau12 and odlau12.dosbarth in ["ODL", "OLA", "OLU", "OLL"]:
            if odlau12.dosbarth in ["ODL", "OLU"]:
                dat = Llusg(rhaniad, odlau=odlau12)
            else:
                dat = LlusgLafarog(rhaniad, odlau=odlau12)
            datrysiadau.append(dat)

    # --------------------
    # 3. Tri chorfan: sain a llusg deirodl
    elif nifer_corfannau == 3:
        x1, x2, x3 = rhaniad

        # dilysu
        if not x1 or not x2 or not x3:
            return datrysiadau

        # 3a. Sain
        # profi am odl rhwng y cyntaf a'r ail
        odlau12 = prawf_odl(x1[-1], x2[-1])
        if odlau12 and odlau12.dosbarth in ["ODL", "OLA"]:

            # profi am gytseinedd rhwng yr ail a'r drydedd
            cyts23 = prawf_cytseinedd(x2, x3)

            if cyts23.dosbarth:

                if cyts23.gefelliaid:
                    if cyts23.dosbarth == "COG":
                        dat = SainGyswllt(rhaniad, odlau=odlau12, cytseinedd=cyts23)
                    else:
                        dat = Sain(rhaniad, odlau=odlau12, cytseinedd=cyts23)
                    datrysiadau.append(dat)

                else:
                    dat = SainLafarog(rhaniad, odlau=odlau12, cytseinedd=cyts23)
                    datrysiadau.append(dat)

            # 3b Llusg deirodl
            # profi am odl lusg rhwng yr ail a'r drydedd ran
            odlau23 = prawf_odl(x2[-1], x3[-1], llusg=True, trwm_ac_ysgafn=TAY)
            
            if odlau23 and odlau23.dosbarth in ["OLU", "OLL"]:
                odlau12.extend(odlau23)
                dat = LlusgDeirodl(rhaniad, odlau=odlau12)
                datrysiadau.append(dat)

    # --------------------
    # 4. Pedwar corfan: Sain gadwynog a Sain deirodl
    elif nifer_corfannau == 4:
        x1, x2, x3, x4 = rhaniad

        # dilysu
        if not x1 or not x2 or not x3 or not x4:
            return datrysiadau

        # --------------------
        # 4a Sain gadwynog
        # profi am odl rhwng x1 a x3
        # profi am gytseinedd rhwng x2 a x4

        odlau13 = prawf_odl(x1[-1], x3[-1])
        cyts24 = prawf_cytseinedd(x2, x4)
        if (
            odlau13 and odlau13.dosbarth in ["ODL", "OLA"] and
            cyts24 and cyts24.dosbarth
        ):
            if cyts24.gefelliaid:
                dat = SainGadwynog(rhaniad, odlau=odlau13, cytseinedd=cyts24)
                datrysiadau.append(dat)

        # --------------------
        # 4b sain deirodl
        # odl rhwng x1 a x2
        # odl rhwng x2 a x3
        # cytseinedd rhwng x3 a x4
        odlau12 = prawf_odl(x1[-1], x2[-1])
        odlau23 = prawf_odl(x2[-1], x3[-1])
        cyts34 = prawf_cytseinedd(x3, x4)

        if (
            odlau12 and odlau12.dosbarth in ["ODL", "OLA"] and
            odlau23 and odlau23.dosbarth in ["ODL", "OLA"] and
            cyts34 and cyts34.dosbarth
        ):
            dat = SainDeirodl(rhaniad, odlau=odlau12+odlau23, cytseinedd=cyts34)
            datrysiadau.append(dat)

    # --------------------
    # D. Pum corfan: Sain ddwbl
    elif nifer_corfannau == 5:
        x1, x2, x3, x4, x5 = rhaniad

        # dilysu
        if not x1 or not x2 or not x3 or not x4 or not x5:
            return datrysiadau

        # odl rhwng x1 a x2
        # cytseinedd rhwng x2 a x3
        # odl rhwng x3 a x4
        # cytseinedd rhwng x4 a x5
        odlau12 = prawf_odl(x1[-1], x2[-1])
        if odlau12 and odlau12.dosbarth in ["ODL", "OLA"]:
            cyts23 = prawf_cytseinedd(x2, x3)
            if cyts23 and cyts23.dosbarth:
                odlau34 = prawf_odl(x3[-1], x4[-1])
                if odlau34 and odlau34.dosbarth in ["ODL", "OLA"]:
                    cyts45 = prawf_cytseinedd(x4, x5)
                    if cyts45 and cyts45.dosbarth:
                        
                        # cyfuno
                        from ceibwr.cytseinedd import Cytseinedd
                        cyts = Cytseinedd()
                        cyts.dosbarth = 'DBL'
                        for nod in cyts23:
                            cyts[nod] = cyts23[nod]
                        for nod in cyts45:
                            cyts[nod] = cyts45[nod]

                        odlau = odlau12 + odlau34
                        dat = SainDdwbl(rhaniad, odlau=odlau, cytseinedd=cyts)
                        datrysiadau.append(dat)

    # dim byd: datrysiad `Amwys`
    if not datrysiadau:
        return [Amwys(rhaniad)]

    # diwedd
    return datrysiadau


def chwynnu(datrysiadau,
            dileu_gwreiddgoll=True,
            dileu_pengoll=False,
            dileu_nones=True):
    '''
    Weithiau bydd rhestr datrysiadau `prawf_cynghanedd` yn
    cynnwys mwy nag un datrysiad, ac mae angen blaenoriaethu
    a chyfuno rhain yn `best_guess`. Mae `chwynnu` yn helpu
    cael gwared ar ddatrysiadau nas dymunir.

    Hefyd mae `datryswr_llinell` yn cyfrifo datrysiadau ar
    gyfer pob rhaniad posib o'r linell, a dosbarth rhan
    fwyaf ohonynt fydd `None`.

    Os yw pob datrysiad yn `None`, mae creu datrysiad newydd 
    `Amwys` ar sail rhaniad Lefel 0 (sef corfan sengl), sydd
    eto a'r dosbarth `None`.
    '''
    # type check
    if not type(datrysiadau) is list:
        raise ValueError("Mae angen `list` fan hyn.")

    if not datrysiadau:
        return []

    if not all([isinstance(dat, Datrysiad) for dat in datrysiadau]):
        raise ValueError("Mae angen rhestr o wrthrychau `Datrysiad` fan hyn.")

    # dileu datrysiadau pengoll
    if datrysiadau and dileu_pengoll:
        datrysiadau = [dat for dat in datrysiadau
                       if dat.dosbarth not in ['CBG', 'TBG', 'LBG', 'SBG']]

    # dileu datrysiadau gwreiddgoll
    if datrysiadau and dileu_gwreiddgoll:
        datrysiadau = [dat for dat in datrysiadau
                       if dat.dosbarth not in ['CWG', 'TWG']]

    # dlieu datrysiadau llafarog (dodgy)
    # Mae cyfatebiaeth llafarog yn iawn fel rhan o SAI
    # ond caiff hynny ei amgodio yn y dosbarth SAL
    datrysiadau = [dat for dat in datrysiadau
                   if dat.dosbarth not in ['LLA']]

    # os yw dosbarth pob datrysiad yn `None`,
    # dychwelyd un datrysiad `Amwys`
    if datrysiadau and all([dat.dosbarth is None for dat in datrysiadau]):
        dat = datrysiadau[0]
        corfan_sengl = [x for corfan in dat for x in corfan]
        return [Amwys([Corfan(corfan_sengl)])]
    
    # fel arall, dileu pob dosbarth `None`
    # h.y. os oes datrysiad cadarnhaol
    if datrysiadau and dileu_nones:
        datrysiadau = [dat for dat in datrysiadau
                       if dat.dosbarth is not None]

    return datrysiadau


def best_guess(datrysiadau, cyfuno=True):
    '''
    Cyfuno cynganeddion (ar ol hidlo)
    SAI + CRO = SEG
    TRA + LLU = TRL etc.
    '''

    # type check
    if not type(datrysiadau) is list:
        raise ValueError("Mae angen `list` fan hyn.")

    if not datrysiadau:
        raise ValueError("Mae angen o leiaf un `Datrysiad` fan hyn.")
        
    if not all([isinstance(dat, Datrysiad) for dat in datrysiadau]):
        raise ValueError("Mae angen `list[Datrysiad]` fan hyn.")

    # dim datrysiadau
    if len(datrysiadau) == 0:
        raise ValueError("Mae angen o leiaf un datrysiad fan hyn.")

    # datrysiad unigol
    if len(datrysiadau) == 1:
        # print('UNIGOL:', type(datrysiadau))
        return datrysiadau[0]

    # didoli yn ôl y drefn flaenoriaeth
    trefn = {x: i for i, x in enumerate(blaenoriaeth)}

    datrysiadau.sort(key=lambda x: trefn[x.dosbarth])

    if not cyfuno:
        return datrysiadau[0]

    datrysiadau = datrysiadau[:2]

    # erbyn hyn dylen ni gael dau ddatrysiad o'r un
    # dosbarth sylfaenol, a rheiny wedi eu trefnu yn
    # ol y drefn flaenoriaeth.

    # sanity check
    # if len(datrysiadau) > 2:
    #     raise ValueError("Dylen ni ddim cyrraedd fan hyn!")

    # Noder: datrysiad x1 yw'r gorau yn ol y drefn flaenoriaeth
    x1, x2 = datrysiadau

    # check bod y ddau yn wahanol
    if x1.dosbarth == x2.dosbarth:
        return x1

    # dosbarthiadau sylfaenol
    # dim cyfuno cynganeddion pengoll!
    croes = ["COG", "CRO", "CWG"]
    traws = ["TRA", "TFA", "TWG"]
    llusg = ["LLD", "LLU", "LLL"]
    sain = ["SOG", "SDD", "SAD", "SAG", "SAI", "SAL"]
    pengoll = ["CBG", "SBG", "LBG", "TBG"]

    # cyfuno dwy gynnghanedd o'r un dosbarth sylfaenol
    for sylfaen in [croes, traws, llusg, sain]:
        if x1.dosbarth in sylfaen and x2.dosbarth in sylfaen:
            return x1

    # anwybyddu cyghanedd bengoll os oes un cadarnhaol
    if x2.dosbarth in pengoll:
        return x1
    if x1.dosbarth in pengoll:
        return x2

    # seingroes
    if (
        (x1.dosbarth in sain and x2.dosbarth in croes) or
        (x1.dosbarth in croes and x2.dosbarth in sain)
    ):
        x1.dosbarth = 'SEG'

    # seindraws
    elif (
        (x1.dosbarth in sain and x2.dosbarth in traws) or
        (x1.dosbarth in traws and x2.dosbarth in sain)
    ):
        x1.dosbarth = 'SED'

    # seinlusg
    elif (
        (x1.dosbarth in sain and x2.dosbarth in llusg) or
        (x1.dosbarth in llusg and x2.dosbarth in sain)
    ):
        x1.dosbarth = 'SEL'

    # trawsgroes
    elif (
        (x1.dosbarth in traws and x2.dosbarth in croes) or
        (x1.dosbarth in croes and x2.dosbarth in traws)
    ):
        x1.dosbarth = 'TRG'

    # trawslusg
    elif (
        (x1.dosbarth in traws and x2.dosbarth in llusg) or
        (x1.dosbarth in llusg and x2.dosbarth in traws)
    ):
        x1.dosbarth = 'TRL'

    # croeslusg
    elif (
        (x1.dosbarth in croes and x2.dosbarth in llusg) or
        (x1.dosbarth in llusg and x2.dosbarth in croes)
    ):
        x1.dosbarth = 'CRL'
    
    # dyna bopeth ...
    else:
        raise ValueError('Dylen ni ddim cyrraedd fan hyn!')

    return x1


# ------------------------------------------------
def main():

    import re

    from ceibwr.beiro import Beiro
    from ceibwr.seinyddwr import Seinyddwr
    from ceibwr.gair import Gair

    from ceibwr.profion_cynghanedd import profion

    beiro = Beiro()
    se = Seinyddwr()

    from cysonion import colormaps
    cmap = colormaps['default']

    profion['pengoll'] = (
        ("Wele rith", "fel ymyl rhod", "o'n cwmpas"),
        ("Rhwydd gamwr", "hawdd ei gymell", "- i'r bryniau"),
        ("Oriau", "ei dyddiau",  "diddig", "- a dreuliodd"),
        ("Ac yn nyfnder", "y weryd", "- gwn y caf"),
        ("cwmpas", "campwaith", "dewin hynod"),
    )

    profion['problem'] = (
        ("Ymysg y bedw", "yn ddedwydd"),
        # ("Eilio'r iaith", "fal Iolo'r oedd"),
        # ("I wlad nef", "eled, yn iach!"),
        ("Anedd o hedd", "yw'r bedd", "bach"),
        ("Yn rhwygo o greigiau", "eu goreugwaith"),  # COG ??
        ("I Frân ap Dyfnwal", "a'r wyneb diofnog."),  # COG ??
        ("Trown i'r acer", "lawn cerrig"),  # mae angen odli 'er' a 'err'
        ("cwmpas", "campwaith"),
        ("- o'n cwmpas", "campwaith"),
        # ("car", "coch"),
        # ("cariad", "coryn"),
        # ("carsad", "corsyn"),
        # ("campaith", "compyn"),
        # ("cwmpan", "campwaith"),
        # ("cwmpas", "campwaith"),
    )

    for key in [
            # 'croes',
            # 'traws',
            # 'llusg',
            # 'sain',
            # 'croes_o_gyswllt',
            # 'sain_o_gyswllt',
            # 'sain_gadwynog',
            # 'trychben',
            # 'cysylltben',
            # 'traws_fantach',
            # 'llusg_lafarog',
            # 'llusg_ewinog',
            # 'sain_ewinog',
            # 'llusg_gudd',
            # 'sain_gudd',
            # 'sain_lafarog',
            # 'llusg_deirodl',
            # 'sain_deirodl',
            # 'sain_ddwbl',
            'pengoll',
            # 'problem',
    ]:

        print()
        print('==============================')
        print('***', key.upper(), '***')
        print('==============================')
        for tup in profion[key]:

            # creu rhaniad
            corfannau = []
            for s in tup:
                t = re.split("(os.linesep| +)", s)
                tt = [c + d for c, d in list(zip(t[::2], t[1::2]+[' ']))]
                corfannau.append(Corfan([Gair(s) for s in tt]))
            rhaniad = Rhaniad(corfannau)

            se.seinyddio(rhaniad)

            # datrys
            if key == 'pengoll':
                dat = prawf_cynghanedd(rhaniad, pengoll=True)
            else:
                dat = prawf_cynghanedd(rhaniad)

            if not dat.dosbarth:
                print(repr(dat))
                print(beiro.coch('XXX'))
            else:
                print(repr(dat))
                print()
                print(dat.show_fancy(toriad='|', eol='\n', cmap=cmap))

            print('--------------------------------------------')

    return None


if __name__ == '__main__':

    main()
