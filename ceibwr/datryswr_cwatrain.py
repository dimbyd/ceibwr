# datryswr_cwatrain.py
'''
Datrys pedair llinell.

EUU     Englyn Unodl Union
ECR     Englyn Crwca
ECY     Englyn Cyrch
'''

from ceibwr import mesur
from ceibwr.cynghanedd import Cynghanedd, Llusg

from ceibwr.datrysiad import Datrysiad, Amwys
from ceibwr.cwpled import CwpledCywyddSeithsill, ToddaidByr

from ceibwr.datryswr_odl import prawf_odl
from ceibwr.datryswr_cwpled import prawf_cwpled


def prawf_cwatrain(x1, x2, x3, x4):
    '''
    Profi cwatrain o linellau
    input:   [`Datrysiad`, `Datrysiad`, `Datrysiad`, `Datrysiad`]
    output:  `Datrysiad`
    '''

    # type check
    if not all([isinstance(x, Datrysiad) for x in (x1, x2, x3, x4)]):
        raise TypeError("Mae angen [`Datrysiad`, `Datrysiad`, `Datrysiad`] fan hyn.")

    x12 = prawf_cwpled(x1, x2)
    x34 = prawf_cwpled(x3, x4)

    odlau24 = prawf_odl(x2.gair_olaf(), x4.gair_olaf())

    # EUU
    if x12 and x34 and odlau24 and (
        type(x12) is ToddaidByr and
        type(x34) is CwpledCywyddSeithsill
    ):
        if odlau24:
            return mesur.EnglynUnodlUnion([x12, x34])

    # ECR
    if x12 and x34 and odlau24 and (
        type(x12) is CwpledCywyddSeithsill and
        type(x34) is ToddaidByr
    ):
        if odlau24:
            return mesur.EnglynCrwca([x12, x34])

    # ECY
    if type(x12) is CwpledCywyddSeithsill and (
        isinstance(x3, Cynghanedd) and
        isinstance(x4, Cynghanedd) and
        not isinstance(x4, Llusg)
    ):

        odlau_cyrch34 = prawf_odl(x3.gair_olaf(), x4[0].gair_olaf())
        if odlau24 and odlau_cyrch34:
            return mesur.EnglynCyrch([x12, x3, x4])

    return Amwys([x1, x2, x3, x4])


# ------------------------------------------------
# test
def main():
    '''
    Mae seinyddio ar draws llinellau yn dodgy.
    Mae hyn siwr o fod yn wir am seinyddio ar draws brawddegau.
    h.y. mae atalnod llawn yn ddigon o "pause" i'w stopio.
    '''

    from ceibwr.profion_pennill import profion
    from ceibwr.beiro import Beiro
    from ceibwr.seinyddwr import Seinyddwr

    from ceibwr.pennill import Pennill
    from ceibwr.datryswr_llinell import datryswr_llinell
    from ceibwr.cysonion import colormaps

    se = Seinyddwr()
    beiro = Beiro()
    cmap = colormaps['default']

    for key in [
        'englyn_unodl_union',
        'englyn_crwca',
        # 'englyn_cyrch',
    ]:
        print()
        print('========================================')
        print(beiro.magenta(key.upper()))
        print('========================================')
        for s in profion[key]:

            pennill = Pennill(s)  # parse
            
            a = pennill.children[0]  # type `Llinell`
            b = pennill.children[1]
            c = pennill.children[2]
            d = pennill.children[3]

            se.seinyddio(a)
            se.seinyddio(b)
            se.seinyddio(c)
            se.seinyddio(d)

            x1 = datryswr_llinell(a, pengoll=True)
            x2 = datryswr_llinell(b)
            x3 = datryswr_llinell(c, pengoll=True)
            x4 = datryswr_llinell(d)

            dat = prawf_cwatrain(x1, x2, x3, x4)

            print()
            print(dat)
            print(dat.show_fancy(toriad='|', cmap=cmap))
            print(beiro.cyan(dat.dosbarth) if dat.dosbarth else beiro.coch('XXX'))
            print()


if __name__ == '__main__':
    main()
