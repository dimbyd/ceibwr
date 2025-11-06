# datryswr_cytseinedd.py
"""
Darganfod a dosbarthu cytseinedd rhwng dau gorfan.

Dosbarthiadau:
GEF: 'gefell'
GWG: 'gwreiddgoll'
TRA: 'canolgoll'
PEG: 'pengoll'
TRB: 'trychben'
CYB: 'cysylltben'
CYS: 'cyswllt'

"""

from ceibwr.gair import Gair
from ceibwr.corfan import Corfan
from ceibwr.rhaniad import Rhaniad

from ceibwr.cytseinedd import Cytseinedd

from ceibwr.cysonion import cyfuniadau_trychben

from ceibwr.seinyddwr import cyfatebiaeth


def gefeillio(x, y):
    """
    Chwilio am gyfatebiaeth cytseiniol rhwng dwy restr nodau.

    Mae'r broses cysefeillio yn mynd o'r dde i'r chwith.
    Mewnbwn: dau wrthrych `list[Cytsain]`
    Allbwn: tri `list[Cytsain]`
        gefelliaid:   rhestr gefelliaid (o'r dde i'r chwith)
        x_blaen: gweddill y rhan gyntaf
        y_blaen: gweddill yr ail ran
    """

    # gwrthod rhestr wag
    if not x or not y:
        return ([], x, y)

    # init
    gefyll = []
    hysbys = []  # not used

    # creu copiau er mwyn peidio dinistrio'r gwreiddiol
    x_nodau = list(x)
    y_nodau = list(y)

    while x_nodau and y_nodau:
        x_nod = x_nodau.pop()
        y_nod = y_nodau.pop()

        if not x_nod.sain:  # e.e. wedi dileu tran'n seinegoli
            y_nodau.append(y_nod)  # trio eto!
            continue
        if not y_nod.sain:
            x_nodau.append(x_nod)  # trio eto!
            continue

        # profi am gyfatebiaeth
        if cyfatebiaeth(x_nod, y_nod):
            gefyll.append((x_nod, y_nod))

            # profi nad oes cyfatebiaeth yn y par nesaf
            if x_nodau and y_nodau and cyfatebiaeth(x_nodau[-1], y_nodau[-1]):
                pass

            # check: dau yn ateb un (rhan gyntaf)
            elif x_nodau and cyfatebiaeth(x_nod, x_nodau[-1]):
                x_nod = x_nodau.pop()
                gefyll.append((x_nod, y_nod))
                hysbys.append('dau-yn-ateb-un')

            # check: dau yn ateb un (ail ran)
            elif y_nodau and cyfatebiaeth(y_nod, y_nodau[-1]):
                y_nod = y_nodau.pop()
                gefyll.append((x_nod, y_nod))
                hysbys.append('dau-yn-ateb-un')

        #  h heb ei hateb
        elif x_nod.text in ["h", "H"]:
            y_nodau.append(y_nod)  # trio eto!
            hysbys.append("h-heb-ei-hateb")

        elif y_nod.text in ["h", "H"]:
            x_nodau.append(x_nod)
            hysbys.append("h-heb-ei-hateb")

        # dim cyfatebiaeth
        else:
            x_nodau.append(x_nod)  # ailosod
            y_nodau.append(y_nod)
            break

    gefyll.reverse()
    return (gefyll, x_nodau, y_nodau)


def aceniad(x, y):
    """
    Dosbarthu dau gorfan yn ol aceniad.
    Mewnbwn: dau wrthrych `Corfan`
    Allwbwn: dosbarth aceniad
    """
    # type check
    if type(x) is not Corfan or type(y) is not Corfan:
        raise TypeError('Mae angen dwy wrthrych `Corfan` fan hyn.')

    if x[-1].is_acennog() and y[-1].is_acennog():
        return "CAC"  # cytbwys acennog

    elif x[-1].is_acennog() and not y[-1].is_acennog():
        return "ADI"  # anghytbwys ddiacen (ddisgynedig)

    elif not x[-1].is_acennog() and y[-1].is_acennog():
        return "AAC"  # anghytbwys acennog (ddyrchafedig)

    else:
        return "CDI"  # cytbwys ddiacen


def traeannu(x):
    """
    Mewnbwn: `Gair` neu `Corfan` (`Gair` am yr odliadur/cleciadur)
    Allbwn:  Tri rhestr cytseiniaid: blaen, canol, diwedd
    Noder:   y canol yw "dan yr acen"
    """

    # type check
    if type(x) is Gair:
        x = Corfan([x])
    elif type(x) is not Corfan:
        raise TypeError('Mae angen `Gair` neu `Corfan` fan hyn.')

    # creu rhestr sillafau
    sillafau = [sillaf for gair in x for sillaf in gair.children]

    # value check
    if not sillafau:
        raise ValueError("Mae angen o leiaf un `Sillaf` fan hyn.")

    # init
    blaen = []
    dan_yr_acen = []
    diwedd = []

    # edrych ar y sill olaf
    sill_olaf = sillafau.pop()
 
    # 1. diwedd acennog (unsill neu lluosill acennog)
    if x and x[-1].is_acennog():

        blaen = sill_olaf.cyrch().cytseiniaid()
        dan_yr_acen = sill_olaf.coda().cytseiniaid()
        # blaen = cyrch_olaf
        # dan_yr_acen = coda_olaf
        diwedd = []

    # 2. diwedd ddiacen (lluosill bob tro)
    elif x and sillafau:

        # edrych ar y goben
        sill_olaf_ond_un = sillafau.pop()

        blaen = sill_olaf_ond_un.cyrch().cytseiniaid()
        dan_yr_acen = sill_olaf_ond_un.coda().cytseiniaid()
        dan_yr_acen += sill_olaf.cyrch().cytseiniaid()
        diwedd = sill_olaf.coda().cytseiniaid()

    # echdynnu gweddill cytseiniaid y rhan flaen
    while sillafau:
        sillaf = sillafau.pop()
        blaen = sillaf.coda().cytseiniaid() + blaen
        blaen = sillaf.cyrch().cytseiniaid() + blaen

    # the end
    return blaen, dan_yr_acen, diwedd


def prawf_cytseinedd(x, y, proest=False):
    """
    Gwirio am gytseinedd rhwng dau air neu gorfan.

    :param x: y gair neu'r corfan cyntaf
    :type x: `Gair` neu `Corfan`
    :param y: yr ail air neu gorfan
    :type y: `Gair` neu `Corfan`
    :return: Manylion cytseinedd
    :rtype: `Cytseinedd` neu `None`
    """

    # type check
    if type(x) is Gair:
        x = Corfan([x])
    if type(y) is Gair:
        y = Corfan([y])

    if type(x) is not Corfan or type(y) is not Corfan:
        raise TypeError('Mae angen dau wrthrych `Corfan` fan hyn.')

    # init record
    cyts = Cytseinedd()  # default: dosbarth = None

    # mae'r symbol `x` yn caei ei trasho rhywle ar hyd y ffordd
    # ond mae angen y gorfan wreiddiol (neu o leiaf y ddau air
    # cyntaf) ar gyfer datrys TFA. Dylen ni fynd trwyddo a ffeinio
    # llefydd mae'r symbol yn cael ei newid ond ... hac amdani!
    from copy import copy
    xorig = copy(x)

    # dadelfeniad mewn i restri cytseiniaid
    x_blaen, x_dan_yr_acen, x_diwedd = traeannu(x)
    y_blaen, y_dan_yr_acen, y_diwedd = traeannu(y)

    # init
    nod_trychben = None
    nodau_cysylltben = []

    # --------------------
    # A. Profi'r cytseiniaid dan yr acen

    # 1. Cytbwys acennog (CAC)
    # Gwahaniaeth dan yr acen.
    # Eithriad: mae proest yn dderbyniol mewn toddaid byr
    # Fan hyn mae angen defnyddio'r opsiwn "proest=True" (?)
    if x[-1].is_acennog() and y[-1].is_acennog():
        if (
            not proest and x_dan_yr_acen and y_dan_yr_acen and
            str(x_dan_yr_acen) == str(y_dan_yr_acen)
        ):
            msg = f'Proest: {x[-1]}, {y[-1]}'
            cyts.hysbys.append(msg)
            return cyts

        gefyll_dan_yr_acen = []

    # 2. Cytbwys ddiacen (CDI)
    # Cyfatebiaeth dan yr acen
    # Gwahaniaeth ar y diwedd
    elif not x[-1].is_acennog() and not y[-1].is_acennog():

        # CDI: check cytseiniaid terfynnol
        if x_diwedd and y_diwedd and x_diwedd == y_diwedd:
            msg = f'CDI: Proest: {x[-1]}, {y[-1]}'
            cyts.hysbys.append(msg)
            return cyts

        # CDI: check cytseiniaid dan yr acen
        gefyll_dan_yr_acen, xb, yb = gefeillio(x_dan_yr_acen, y_dan_yr_acen)

        if xb or yb:
            msg = f"CDI: Dim cyfatebiaeth dan yr acen: {x[-1]}, {y[-1]}"
            cyts.hysbys.append(msg)
            return cyts

    # 3. Anghytbwys ddiacen (ADI)
    # Cyfatebiaeth dan yr acen (yn cynnwys sillafau llafarog)
    # Gwahaniaeth ar y diwedd.
    #
    # ADI yw'r unig ddosbarth aceniad lle mae'n bosib
    # cael cynganeddion trychben a chysylltben.
    elif x[-1].is_acennog() and not y[-1].is_acennog():

        # 3.1 Prawf cyfatebiaeth union
        gefyll_dan_yr_acen, xb, yb = gefeillio(x_dan_yr_acen, y_dan_yr_acen)

        # 3.2 Prawf cyfatebiaeth gysylltben
        if xb or yb:
            # Mae angen benthyg cytsain gyntaf yr ail ran
            # a'i atodi at ddiwedd y rhan gyntaf.
            #
            # Rhaid mynd nol i'r gwreiddiol er mwyn profi rhain, gan
            # ad oes modd benthyg ar draws llafariad decrhreuol, h.y.
            # mae angen cyrch anwag ar sillaf gyntaf yr ail ran.
            
            cyrch_nesaf = y.children[0].children[0].cyrch()
            nodau_cys = []

            if cyrch_nesaf.children:
                for idx, nod in enumerate(cyrch_nesaf.children):
                    # benthyg nod o'r ail ran
                    nodau_cys.append(nod)
                    x_dan_yr_acen.append(nod)
                    gefyll_dan_yr_acen, xb, yb = gefeillio(x_dan_yr_acen, y_dan_yr_acen)
                    if not xb and not yb:
                        nodau_cysylltben = nodau_cys
                        break

                # reset
                x_dan_yr_acen = x_dan_yr_acen[:-len(nodau_cys)]

        # 3.3 Prawf cyfatebiaeth drychben
        if (xb or yb) and len(x_dan_yr_acen) > 1:

            key = str(x_dan_yr_acen[-2]) + str(x_dan_yr_acen[-1])
            
            if key.lower() in cyfuniadau_trychben:
                nod = x_dan_yr_acen.pop()
                y_blaen.insert(0, nod)
                gefyll_dan_yr_acen, xb, yb = gefeillio(x_dan_yr_acen, y_dan_yr_acen)
                
                if not xb and not yb:
                    nod_trychben = nod

        if xb or yb:
            msg = f"ADI: Dim cyfatebiaeth dan yr acen: {x[-1]}, {y[-1]}"
            cyts.hysbys.append(msg)
            return cyts  # null

    # 4. Anghytbwys acennog (AAC)
    # (Nid oes rhaid ateb y cytseinaid dan yr acen)
    else:
        gefyll_dan_yr_acen = []

    # 3. Profi cytseiniaid blaen
    gefyll_blaen, x_blaen, y_blaen = gefeillio(x_blaen, y_blaen)

    # cyfuno'r gefyll blaen a'r gefyll canol
    gefyll = gefyll_blaen + gefyll_dan_yr_acen

    # print('x here:', x)

    # ------------
    # 1. prawf croes-o-gyswllt
    # rhaid hepgor y gytsain gyntaf
    # fel arall, mae'n cysefeillio gyda'i hun!
    nodau_cyswllt = []

    if x_blaen and not y_blaen:

        # Rhaid i'r nodau blaen sydd dros ben gyfateb a
        # nodau sydd ar ddiwedd y rhan gyntaf, yn yr un drefn.
        # Mae angen stopio cyn cyrraedd y nodau dros ben
        # neu maent yn cyfateb a'u hunain.
        x_blaen_cwta = x.cytseiniaid()[len(x_blaen):]
        gefyll2, xb2, zb2 = gefeillio(x_blaen, x_blaen_cwta)
        # print('abc:', gefyll2, xb2, zb2)
        if not xb2 or (len(xb2) == 1 and xb2[0].text.lower() == "n"):
            # print('Croes-o-Gyswllt!!')
            gefyll.extend(gefyll2)
            nodau_cyswllt = x_blaen
            x_blaen = xb2  # empty

    # --------------------
    # cofnodi
    cyts.gefyll = gefyll
    cyts.gwreiddgoll = x_blaen
    cyts.canolgoll = y_blaen
    cyts.pengoll = x_diwedd + y_diwedd

    for nod in nodau_cyswllt:
        cyts.special[nod] = 'CYS'
    if nod_trychben is not None:
        cyts.special[nod_trychben] = 'TRB'
    for nod in nodau_cysylltben:
        cyts.special[nod] = 'CYB'

    #  TODO: problem fan hyn. Mae angen creu copi o'r
    # datrysiad cyn gosod `neighbours`
    #
    # for x, y in gefyll:
    #     x.add_neighbour(y)
    #     y.add_neighbour(x)

    # # create lookup
    # for par in gefyll:
    #     for nod in par:
    #         cyts[nod] = 'GEF'

    # for nod in x_blaen:
    #     cyts[nod] = 'GWG'

    # for nod in y_blaen:
    #     cyts[nod] = 'TRA'

    # for nod in nodau_cyswllt:
    #     cyts[nod] = 'CYS'

    # if nod_trychben is not None:
    #     cyts[nod_trychben] = 'TRB'

    # for nod in nodau_cysylltben:
    #     cyts[nod] = 'CYB'


    # --------------------
    # dosbarthu: oes angen hwn fan hyn? 
    # Pam na diffinio ffwythiant `dosbarth()` wedi seilio ar 
    # y rhestri nodau, yn y dosbarth `Cytseinedd`.

    # croes/traws wreiddgoll
    # Mae'n bosib cael sawl cytsain gwreiddgoll
    # rhwng ail a thrydedd rhan cynghanedd sain.
    # Ond mae hefyd angen upper limit er mwyn
    # osgoi cyfateb dim cytseiniaid o flaen yr
    # acenion. Felly mae angen checko bod |gefyll_blaen| > 0 ?

    # 1. croes (cyfatebiaeth union)
    if not x_blaen and not y_blaen:
        if gefyll:
            if nodau_cyswllt:
                cyts.dosbarth = 'COG'
            else:
                cyts.dosbarth = "CRO"
        else:
            cyts.dosbarth = "LLA"

    # 2. croes wreiddgoll
    elif x_blaen and not y_blaen:

        # croes n-wreidgoll
        if len(x_blaen) == 1:
            if x_blaen[0].text.lower() == "n":
                if gefyll:
                    cyts.dosbarth = "CRO"
                else:
                    cyts.dosbarth = "LLA"
                cyts.hysbys.append("n-wreiddgoll")
        else:
            cyts.dosbarth = 'CWG'

    # 3. traws
    elif not x_blaen and y_blaen:

        if gefyll:

            # croes n-ganolgoll
            if len(y_blaen) == 1 and y_blaen[0].text.lower() == "n":

                cyts.dosbarth = "CRO"
                cyts.hysbys.append("n-ganolgoll")

            else:

                cyts.dosbarth = "TRA"

                # traws fantach?
                if len(xorig) == 1 and xorig[0].nifer_sillafau() == 1 or (
                    len(xorig) == 2 and xorig[0].nifer_sillafau() == 1 and
                    xorig[1].nifer_sillafau() == 1 and
                    not any(nod.is_cytsain() for nod in xorig[0].nodau())
                ):
                    cyts.dosbarth = 'TFA'

        # else:
        #     cyts.dosbarth = "LLA"

    # 4. traws wreiddgoll
    elif x_blaen and y_blaen:
        if len(x_blaen) == 1:
            if x_blaen[0].text.lower() == "n":
                if gefyll:
                    cyts.dosbarth = "TRA"
                    cyts.hysbys.append("n-wreiddgoll")
                else:
                    cyts.dosbarth = "LLA"
        else:
            cyts.dosbarth = "TWG"

    # dim
    else:
        cyts.dosbarth = None

    return cyts


# ------------------------------------------------
# test
def main():

    from ceibwr.profion_cytseinedd import profion
    from ceibwr.seinyddwr import Seinyddwr
    from ceibwr.beiro import Beiro
    from ceibwr.cysonion import llythrenwau

    se = Seinyddwr()
    beiro = Beiro()

    profion["problem"] = [
        ("bedw", "dedwydd"),
        ("heb na chledr,", "na chlwyd"),  # CFG da
        ("ieuanc", "ei awen"),  # LL
        ("Wrth goelio", "fod fath galon"),  # r-wreiddgoll
        ("I wlad nef", "eled, yn iach!"),
        ("Y mae", "Morfudd"),
        ("Dewi gâr,", "lle dug urael,"),
        ("ac i gymuned", "o gamau unig."),
        ("Y miniog", "ei ymennydd"),
        ("cwmpas", "campwaith"),
        ("Ar wely’r ferch;", "alar fu."),
        ("a gwin", "a gawn"),
        ("mewn llan", "a llys"),
    ]

    for key in [
        "croes",
        # "traws",
        # "traws_fantach",
        # "croes_o_gyswllt",
        # "croes_o_gyswllt_gymhleth",
        # "trychben",
        # "cysylltben",
        # "caledu",
        # "meddalu",
        # "dau-yn-ateb-un",
        # "croes_o_gyswllt_ewinog",
        # "misc",
        # "problem",
    ]:
        print("\n------------------------------")
        print(key.upper())

        prawf = profion[key]
        for s1, s2 in prawf:
            x = Corfan([Gair(s) for s in s1.split(" ")])
            y = Corfan([Gair(s) for s in s2.split(" ")])
            
            # from ceibwr.llinell import Llinell
            # Seinyddwr().seinyddio(Llinell(x1+x2))
            
            rhaniad = Rhaniad([x, y])
            se.seinyddio(rhaniad)

            print("------------------------------")
            # print(s_acenion)
            print(" | ".join([corfan.show_acenion() for corfan in rhaniad]))
            print("{} | {}".format(s1, s2))
            print(" | ".join([corfan.sain() for corfan in rhaniad]))
            print()
            cyts = prawf_cytseinedd(x, y)
            # print('dosb2:', cyts.dosbarth)
            if cyts.dosbarth:
                if cyts.dosbarth in ('CWG, TWG'):
                    print(beiro.melyn(cyts.dosbarth))
                else:
                    dosb = llythrenwau['cynghanedd'][cyts.dosbarth]
                    print(beiro.gwyrdd(dosb))
                print('---------------')
                print(cyts)
                print('---------------')

            else:
                print(beiro.coch('DIM'))

        print("------------------------------")


if __name__ == "__main__":
    main()
