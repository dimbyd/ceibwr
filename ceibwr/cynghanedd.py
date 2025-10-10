# cynghanedd.py
'''
`Cynghanedd` type.

Class structure:
    `Rhaniad(TreeNode)`
    `Datrysiad(Rhaniad)`
    `Cynghanedd(Datrysiad)`

Mae `Cynghanedd` yn ddosbarth haniaethol (abstract class)
sydd yn uwch ddosbarth i'r cynganeddion sylfaenol (sef CRO, 
TRA, LLU, SAI) sydd yn eu tro yn uwch ddosbarthiadau i'r 
cynganeddion perthnasol.

Hefyd
    `Cwpled(Datrysiad)`
    `Mesur(Datrysiad)`
    `Amwys(Datrysiad)`

Mae gwrthrych `Cynghanedd' yn is-ddosbarth o
`Datrysiad`, sy'n is-ddosbarth `Rhaniad`,
    dwy ran: = CRO/TRA/LLU
    tair rhan: SAI/LLD ayb

Aceniad:
    Mae hyn yn dibynnu ar y gynghanedd benodol
    [x1, x2] - ACE[x1, x2] (heblaw LLU)
    [x1, x2, x3] 
        SAI: ACE(x2,x3]
    [x1, x2, x3, x4] 
        SGA: ACE(x2, x4)
        SDO: ACE(x3, x4)
        
Mae gan wrthrych Cynghanedd briodweddau penodol e.e.
    aceniad: CAC/CDI/ADY/ADI
Noder mai priodweddau'r rhaniad yw rhain,
h.y. nid y corfannau unigol.

DISP `Cynghanedd`
Caiff y nodau perthnasol eu cadw yn yr amryw restrau,
felly pan yn arddangos nod unigol

cy = Cynghanedd()
for nod in cy.nodau():
    if node in cy.cytseiniaid.gefelliaid:
        <span class=cytsain, dosbarth='gefell'>d</span>
    neu
        <cytsain dosbarth='gefell'>d</cytsain>.

`Sain`: rhaniad mewn i dri corfan
    self.odlau = [(g2, g3)] # linell, bell
        dwy gydran am odl SAI, CC7, TOB
        tair corfan am odl LLD, SAD, EMI
        pedair corfan am ENG (2+2, h.y. TOB a CC7)
        chwe chydrab am HAT (inc. odl gyrch)

Mae angen peidio cofnodi'r odlau yn y sillafau/geiriau
eu hunain fan hyn, gan bod odl ond yn gwneud synnwyr
mewn perthynas gair gyda geiriau eraill.

Priodwedd rhaniad yw odl, nid priodwedd y geiriau na'r
rhannau unigol: mae angen dau i odli ...

Yn enwedig o ystyried odlau cudd:  mae cofnodi'r odl
fel attribute y rhaniad cyfan yn rhoi modd cyrchu'r
gair dilynol, sy'n creu'r odl gudd.

[[g1, g2], [g3], [g4, g5, g6]]

Mae'r briodwedd `self.odl` yn restr o sillafau yn
y rhaniad sy'n odli gyda'i gilydd, yn cynnwys odlau
llusg ac odlau cyrch !!

`Cytseinedd`: rhaniad gyda nodau dethol
    self.cytseiniaid
        dau gorfan am CRO, TRA, SAI
        does dim cysteinedd dros tri corfan neu fwy!

Felly gall `Odl` berthyn i CNG, CWP a MES
ond `Cytseinedd` dim ond i CNG (dim llusg)
h.y. i raniad o'r rhestr geiriau gwreiddiol.

'''

from ceibwr.corfan import Corfan
from ceibwr.datrysiad import Datrysiad

from ceibwr.odlau import Odlau
from ceibwr.cytseinedd import Cytseinedd


class Cynghanedd(Datrysiad):
    '''
    Abstract class ar gyfer CRO, TRA, LLU, SAI
    Mewnbwn: rhestr corfannau
    CRO/TRA/LLU: dau gorfan [x1, x2]
    SAI/LLD: tri chorfan [x1, x2, x3] etc
    '''
    def __init__(self, rhaniad, parent=None):
        Datrysiad.__init__(self, rhaniad, parent=parent)

        # type check (rhaniadau syml yn unig)
        if not all([isinstance(elfen, Corfan) for elfen in rhaniad]):
            raise TypeError("Mae angen rhestr o wrthrychau `Corfan` fan hyn.")

    def __str__(self):
        return ''.join([str(corfan) for corfan in self.children])


# --------------------
# Sylfaenol

class Croes(Cynghanedd):
    def __init__(self, rhaniad, cytseinedd, parent=None):
        Cynghanedd.__init__(self, rhaniad, parent=parent)

        # type check
        if type(cytseinedd) is not Cytseinedd:
            raise ValueError("Mae angen gwrthrych `Cytseinedd` fan hyn.")

        # value check
        if len(self.children) not in (2, 3):
            raise ValueError("Mae angen 2-3 corfan ar `Croes`.")

        self.dosbarth = 'CRO'
        self.cytseinedd = cytseinedd


class Traws(Cynghanedd):
    def __init__(self, rhaniad, cytseinedd, parent=None):
        Cynghanedd.__init__(self, rhaniad, parent=parent)

        # type check
        if type(cytseinedd) is not Cytseinedd:
            raise ValueError("Mae angen gwrthrych `Cytseinedd` fan hyn.")

        # value check
        if len(self.children) not in (2, 3):
            raise ValueError("Mae angen 2-3 corfan ar `Traws`.")

        self.dosbarth = 'TRA'
        self.cytseinedd = cytseinedd


class Llusg(Cynghanedd):
    def __init__(self, rhaniad, odlau, parent=None):
        Cynghanedd.__init__(self, rhaniad, parent=parent)

        # type check
        if type(odlau) is not Odlau:
            raise ValueError("Mae angen gwrthrych `Odlau` fan hyn.")

        # value check
        if len(self.children) not in (2, 3, 4):
            raise ValueError("Mae angen 2-4 corfan ar LLU.")

        # set parameters
        self.dosbarth = 'LLU'
        self.odlau = odlau


class Sain(Cynghanedd):
    def __init__(self, rhaniad, odlau, cytseinedd, parent=None):
        Cynghanedd.__init__(self, rhaniad, parent=parent)

        # value check
        if len(self.children) not in (3, 4, 5, 6):
            raise ValueError("Mae angen 3-6 corfan ar SAI.")

        self.dosbarth = 'SAI'
        self.cytseinedd = cytseinedd
        self.odlau = odlau


class Llafarog(Cynghanedd):
    def __init__(self, rhaniad, parent=None):
        Cynghanedd.__init__(self, rhaniad, parent=parent)

        self.dosbarth = 'LLA'


# --------------------
# Amrywolion Croes

class CroesGyswllt(Croes):
    def __init__(self, rhaniad, cytseinedd, parent=None):
        Croes.__init__(self, rhaniad, cytseinedd, parent=parent)

        # TODO check os oes cytsain gyswllt
        self.dosbarth = 'COG'


# --------------------
# Amrywolion Traws

class TrawsFantach(Traws):
    def __init__(self, rhaniad, cytseinedd, parent=None):
        Traws.__init__(self, rhaniad, cytseinedd, parent=parent)

        # TODO check nifer sillafau cyn yr orffwysfa
        self.dosbarth = 'TFA'


# --------------------
# Amrywolion Llusg

class LlusgDeirodl(Llusg):
    def __init__(self, rhaniad, odlau, parent=None):
        Llusg.__init__(self, rhaniad, odlau, parent=parent)

        # TODO check bod tair odl
        self.dosbarth = 'LLD'


class LlusgLafarog(Llusg):
    def __init__(self, rhaniad, odlau, parent=None):
        Llusg.__init__(self, rhaniad, odlau, parent=parent)

        # TODO check bod yr odlau yn llafarog
        self.dosbarth = 'LLL'


# --------------------
# Amrywolion Sain

class SainGyswllt(Sain):
    def __init__(self, rhaniad, odlau, cytseinedd, parent=None):
        Sain.__init__(self, rhaniad, odlau, cytseinedd, parent=parent)

        # TODO check bod cystsain gyswllt
        self.dosbarth = 'SOG'


class SainGadwynog(Sain):
    def __init__(self, rhaniad, odlau, cytseinedd, parent=None):
        Sain.__init__(self, rhaniad, odlau, cytseinedd, parent=parent)

        # TODO check bod pedwar corfan
        self.dosbarth = 'SAG'


class SainDeirodl(Sain):
    def __init__(self, rhaniad, odlau, cytseinedd, parent=None):
        Sain.__init__(self, rhaniad, odlau, cytseinedd, parent=parent)

        # TODO check bod pedwar corfan a thair odl
        self.dosbarth = 'SAD'


class SainDdwbl(Sain):
    def __init__(self, rhaniad, odlau, cytseinedd, parent=None):
        Sain.__init__(self, rhaniad, odlau, cytseinedd, parent=parent)

        # TODO check bod pum corfan
        self.dosbarth = 'SDD'


class SainLafarog(Sain):
    def __init__(self, rhaniad, odlau, cytseinedd, parent=None):
        Sain.__init__(self, rhaniad, odlau, cytseinedd, parent=parent)

        # TODO check bod yr odlau yn llafarog
        self.dosbarth = 'SAL'


# --------------------
# Pengoll

class CroesBengoll(Croes):
    def __init__(self, rhaniad, cytseinedd, parent=None):
        Croes.__init__(self, rhaniad[:-1], cytseinedd, parent=parent)

        self.children.append(rhaniad[-1])
        self.dosbarth = 'CBG'


class TrawsBengoll(Traws):
    def __init__(self, rhaniad, cytseinedd, parent=None):
        Traws.__init__(self, rhaniad[:-1], cytseinedd, parent=parent)

        self.children.append(rhaniad[-1])
        self.dosbarth = 'TBG'


class LlusgBengoll(Llusg):
    def __init__(self, rhaniad, odlau, parent=None):
        Llusg.__init__(self, rhaniad[:-1], odlau, parent=parent)

        self.children.append(rhaniad[-1])
        self.dosbarth = 'LBG'


class SainBengoll(Sain):
    def __init__(self, rhaniad, odlau, cytseinedd, parent=None):
        Sain.__init__(self, rhaniad[:-1], odlau, cytseinedd, parent=parent)

        self.children.append(rhaniad[-1])
        self.dosbarth = 'SBG'


# --------------------
# Gwreiddgoll

class CroesWreiddgoll(Croes):
    def __init__(self, rhaniad, cytseinedd, parent=None):
        Croes.__init__(self, rhaniad, cytseinedd, parent=parent)

        self.dosbarth = 'CWG'


class TrawsWreiddgoll(Traws):
    def __init__(self, rhaniad, cytseinedd, parent=None):
        Traws.__init__(self, rhaniad, cytseinedd, parent=parent)

        self.dosbarth = 'TWG'


# ------------------------------------------------
# test
def main():

    from ceibwr.gair import Gair
    from ceibwr.datrysiad import Amwys

    # manual test (poenus!)
    x111 = Corfan([Gair("Wele"), Gair("rith")])
    x112 = Corfan([Gair("fel"), Gair("ymyl"), Gair("rhod")])
    x113 = Corfan([Gair("o'n"), Gair("cwmpas")])

    x121 = Corfan([Gair("campwaith")])
    x122 = Corfan([Gair("dewin"), Gair("hynod")])

    x211 = Corfan([Gair("Hen "), Gair("linell ")])
    x212 = Corfan([Gair("bell ")])
    x213 = Corfan([Gair("nad "), Gair("yw'n "), Gair("bod\n")])

    x221 = Corfan([Gair("Hen "), Gair("derfyn ")])
    x222 = Corfan([Gair("nad "), Gair("yw'n "), Gair("darfod\n")])

    cnull = Cytseinedd()
    onull = Odlau()

    x11 = TrawsBengoll([x111, x112, x113], cytseinedd=cnull)
    x12 = Amwys([x121, x122])
    x21 = Sain([x211, x212, x213], cytseinedd=cnull, odlau=onull)
    x22 = Croes([x221, x222], cytseinedd=cnull)

    print('x11:', repr(x11))
    print('x12:', repr(x12))
    print('x21:', repr(x21))
    print('x22:', repr(x22))

    print(x21.create_tabular(toriad='|'))


if __name__ == "__main__":
    main()
