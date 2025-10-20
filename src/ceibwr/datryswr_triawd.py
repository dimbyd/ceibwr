# datryswr_triawd.py
'''
Datrys triawd o linellau.

EMI     Englyn Milwr
EPF     Englyn Penfyr
'''

from ceibwr import mesur
from ceibwr.cynghanedd import Cynghanedd, Llusg

from ceibwr.datrysiad import Datrysiad, Amwys
from ceibwr.cwpled import ToddaidByr

from ceibwr.datryswr_odl import prawf_odl
from ceibwr.datryswr_cwpled import prawf_cwpled


def prawf_triawd(x1, x2, x3):
    '''
    Profi triawd o linellau
    input:   [`Datrysiad`, `Datrysiad`, `Datrysiad`]
    output:  `Datrysiad`
    '''

    # type check
    if not all([isinstance(x, Datrysiad) for x in (x1, x2, x3)]):
        raise TypeError("Mae angen [`Datrysiad`, `Datrysiad`, `Datrysiad`] fan hyn.")

    # Englyn Milwr (EMI)
    odlau12 = prawf_odl(x1.gair_olaf(), x2.gair_olaf())
    odlau23 = prawf_odl(x2.gair_olaf(), x3.gair_olaf())
    
    if odlau12 and odlau23:

        if (
            isinstance(x1, Cynghanedd) and
            isinstance(x2, Cynghanedd) and
            isinstance(x3, Cynghanedd) and
            not isinstance(x3, Llusg)
        ):
            return mesur.EnglynMilwr([x1, x2, x3])

    # Englyn Penfyr (EPF)
    x12 = prawf_cwpled(x1, x2)
    odlau123 = prawf_odl(x12.gair_olaf(), x3.gair_olaf())

    if x12 and odlau123:

        if (
            type(x12) is ToddaidByr and
            isinstance(x3, Cynghanedd) and
            not isinstance(x3, Llusg)
        ):
            return mesur.EnglynPenfyr([x12, x3])

    return Amwys([x1, x2, x3])


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
        'englyn_milwr',
        'englyn_penfyr',
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

            se.seinyddio(a)
            se.seinyddio(b)
            se.seinyddio(c)

            x1 = datryswr_llinell(a, pengoll=True)
            x2 = datryswr_llinell(b)
            x3 = datryswr_llinell(c, pengoll=True)

            # print('x1:', repr(x1), type(x1))
            # print('x2:', repr(x2), type(x2))
            # print('x3:', repr(x3), type(x3))

            dat = prawf_triawd(x1, x2, x3)

            print()
            print(dat)
            print(dat.show_fancy(toriad='|', cmap=cmap))
            print(beiro.cyan(dat.dosbarth) if dat.dosbarth else beiro.coch('XXX'))
            print()


if __name__ == '__main__':
    main()
