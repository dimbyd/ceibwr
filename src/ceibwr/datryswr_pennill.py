# datryswr_pennill.py
'''
Dulliau ar gyfer darganfod pennill ar un o'r mesurau traddodiadol.

Cywydd deuair hirion:   CDH = [CW7, CW7, ...]
Cywydd deuair fyrion:   CDF = [CW4, CW4, ...]

Englyn unodl union:     EUU = [TOB, CW7]
Englyn crwca:           ECR = [CW7, TOB]
Englyn milwr:           EMI = [CY7, CY7, CY7]
Englyn penfyr:          EPF = [TOB, CY7]

Cyhydedd nawban:        CH9 = [CY9, CY9, CY9, CY9]   # pob llinell yn nawsill ac yn odli
Cyhydedd fer:           CHF = [CY8, CY8, CY8, CY8]   # pob llinell yn wythsill ac yn odli
Cyhydedd hir:           CHH = [CY5, CY5, CY5, XX4]   # 1,2,3 yn odli

Gwawdodyn byr:          GWB = [CY9, CY9, TOD]       # pob llinell yn odli
Gwawdodyn hir:          GWH = [CY9, CY9, CY9, CY9, TOD]         # pob llinell yn odli, dim cynghanedd lusg yn y llinell olaf
Hir a thoddaid:         HAT = [CWX, CWX[,CWX],TOH]   # pob llinell yn odli
'''
from ceibwr.llinell import Llinell
from ceibwr.pennill import Pennill

from ceibwr.cynghanedd import CroesBengoll, TrawsBengoll
from ceibwr.cwpled import CwpledCywyddBedairsill, CwpledCywyddSeithsill

from ceibwr.corfan import Corfan

from ceibwr.odlau import Odlau
from ceibwr.datrysiad import Amwys

from ceibwr.cwpled import Cwpled, CwpledCaeth
from ceibwr.cwpled import Toddaid, ToddaidByr, ToddaidHir

from ceibwr.datryswr_llinell import datryswr_llinell

from ceibwr.datryswr_cwpled import prawf_cwpled
from ceibwr.datryswr_triawd import prawf_triawd
from ceibwr.datryswr_cwatrain import prawf_cwatrain

from ceibwr.seinyddwr import Seinyddwr


def datryswr_pennill(pennill, fesul_llinell=False):
    '''
    Ceisio adnabod ffurf penodol ar bennill.

    Yn union fel trio adnabod ffurf penodol ar linell.
    '''

    # check
    if type(pennill) is not Pennill:
        raise TypeError("Mae angen `Pennill` fan hyn")

    # double check
    if not all([type(x) is Llinell for x in pennill.children]):
        raise TypeError("Mae angen `list[Llinell]` fan hyn")

    # seinyddio
    se = Seinyddwr()
    for llinell in pennill.children:
        se.seinyddio_llinell(llinell)

    # datrys pob llinell yn unigol
    dats = []
    for llinell in pennill.children:
        dat = datryswr_llinell(llinell, pengoll=True)
        dats.append(dat)

    # debug
    if fesul_llinell:
        return Amwys(dats)  # rhestr o ddatrysiadau llinell yn unig

    # -----------------------------------
    # Prawf mesur

    # ------------------------------
    # 0. dim byd
    # ------------------------------
    if not dats:
        return []

    # ------------------------------
    # 1. llinell unigol
    # ------------------------------
    elif len(dats) == 1:
        return dats[0]

    # ------------------------------
    # 2. dwy linell: cwpled unigol (inc toddeidiau)
    # ------------------------------
    if len(dats) == 2:
        x1, x2 = dats
        return prawf_cwpled(x1, x2)

    # ------------------------------
    # 3. tair llinell
    # ------------------------------
    elif len(dats) == 3:
        x1, x2, x3 = dats

        return prawf_triawd(x1, x2, x3)
    # ------------------------------
    # 4. pedair
    # ------------------------------
    else:
        if len(dats) == 4:
            x1, x2, x3, x4 = dats
            dat = prawf_cwatrain(x1, x2, x3, x4)
            if dat.dosbarth:
                return dat
    
    # ------------------------------
    # 5. TODO: chwech/wyth/deg am HAT etc
    # ------------------------------

    # ------------------------------
    # X. chwilio am gwpledi
    # ------------------------------

    # canfod cwpledi
    dat_seq = []
    seq = list(reversed(dats))
    x = seq.pop()
    while seq:
        y = seq.pop()
        dat_cwpled = prawf_cwpled(x, y)
        if dat_cwpled.dosbarth:
            dat_seq.append(dat_cwpled)
            x = seq.pop() if seq else None
        else:
            dat_seq.append(x)
            x = y
    if x is not None:
        dat_seq.append(x)

    # hac: kill CBG/TBG
    for idx, dat in enumerate(dat_seq):
        if isinstance(dat, CwpledCaeth) and not isinstance(dat, (Toddaid, ToddaidByr, ToddaidHir)):
            pengoll_found = False
            if type(dat[0]) in [CroesBengoll, TrawsBengoll]:
                corfan_sengl = [x for corfan in dat[0] for x in corfan]
                dat[0] = Amwys([Corfan(corfan_sengl)])
                pengoll_found = True
            if type(dat[1]) in [CroesBengoll, TrawsBengoll]:
                corfan_sengl = [x for corfan in dat[1] for x in corfan]
                dat[1] = Amwys([Corfan(corfan_sengl)])
                pengoll_found = True
            if pengoll_found:
                dat_seq[idx] = Cwpled(dat[0], dat[1], dat.odlau)
        elif type(dat) in [CroesBengoll, TrawsBengoll]:
            corfan_sengl = [x for corfan in dat for x in corfan]
            dat_seq[idx] = Amwys([Corfan(corfan_sengl)])


    # Syniad gwael. Gwell gadael yr odlau yn y cwpledi and/or
    # yn y mesurau tair llinell neu bedair llinell. 
    # concat odlau
    # odlau = Odlau()
    # for dat in dat_seq:
    #     if hasattr(dat, 'odlau'):
    #         odlau.extend(dat.odlau)

    # Cywydd Deuair Hirion (CDH)
    if all([type(dat) is CwpledCywyddSeithsill for dat in dat_seq]):

        # TODO: check os yw'r odlau yn newid am yn ail
        from ceibwr.mesur import CywyddDeuairHirion
        return CywyddDeuairHirion(dat_seq)

    # Cywydd Deuair Fyrion (CDF)
    if all([type(dat) is CwpledCywyddBedairsill for dat in dat_seq]):

        from ceibwr.mesur import CywyddDeuairFyrion
        return CywyddDeuairFyrion(dat_seq)

    # dim mesur
    return Amwys(dat_seq)


# ------------------------------------------------
# test
def main():

    from ceibwr.cysonion import colormaps
    from ceibwr.beiro import Beiro
    cmap = colormaps['default']
    beiro = Beiro()

    from ceibwr.profion_pennill import profion

    profion['problem'] = (

        """Dan oer hin yn dwyn y rhaw - mewn trymwaith
        Bu ganwaith heb giniaw.""",

        """dwyglust feinion aflonydd
        dail saets wrth ei dâl y sydd
        trwsio fal golewo glain
        y bu wydrwr ei bedrain""",
    )

    for key in [
        # 'cywydd_deuair_hirion',
        # 'cywydd_deuair_fyrion',
        # 'englyn_milwr',
        # 'englyn_penfyr',
        'englyn_unodl_union',
        # 'englyn_crwca',
        # 'englyn_cyrch',
        # 'cyhydedd_nawban',
        # 'hir_a_thoddaid',
        # 'problem',
        # 'cywydd',
    ]:

        print('========================================')
        print(key.upper())
        print('========================================')
        for s in profion[key]:

            pennill = Pennill(s)
            print(pennill)

            dat = datryswr_pennill(pennill)

            print(repr(dat))
            print()
            print(dat.show_fancy(toriad='|', cmap=cmap))
            print(beiro.cyan(dat.dosbarth) if dat.dosbarth else beiro.coch('XXX'))
            print()
            print('--------------------------------------------')
            print()

            # dat.export_csv('dat.csv')


if __name__ == '__main__':

    main()
