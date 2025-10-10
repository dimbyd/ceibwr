# cwpled.py
'''
`Cwpled` type.

Cwpled                      CWP     [DIM, DIM]        ODL(1, 2)
Cwpled caeth                CCA     [CNG, CNG]        ODL(1, 2)
Cwpled cywydd               CCY     [CNG7, CNG7]      ODL(x1, x2)
Cwpled cywydd bedairsill    CC4     [CNG4, CNG4]      ODL(1, 2)   NAC(1, 2)
Cwpled cywydd seithsill     CC7     [CNG7, CNG7]      ODL(1, 2)   NAC(1, 2)
Cwpled awdl-gywydd          CAG     [CNG7, CNG7]      OGY(x1, x2)

B. Toddeidiau
Toddaid                 TOD     [CBG10, CN9]    ODL(x11, x22), ODL(x12, x21)
Toddaid byr             TOB     [CBG10, COR6]   ODL(x11, x22), CNG(x12, x21) neu SAI(x12, x21, x22)
Toddaid hir             TOH     [CBG10, CN10]   ODL(1.1, 2.2), ODL(1.2, 2.1)

Mae `Cwpled` yn uned seinegol. Ar y dudalen, dim ond rhestr o ddwy linell 
yw cwpled, yn y modd mai rhestr o linellau yw pennill.
Felly mae angen odl rhywle!

Text: Gair -> Llinell -> Pennill
Sain: Gair -> Corfan -> Cynghanedd -> Cwpled -> Mesur

Mae'n bosib cael Mesur heb gwpledi (e.e. EMI)

Mae prawf_cwpled yn prosesu dau wrthrych `Datrysiad`
    - CC4: CNG4, CNG4
    - CC7: CNG7, CNG7
    - TOB: CBGX, DIM6
    - TOD: CBGX, CNG9
    - TOH: CBGX, CNGX
- os llwyddiant, mae'n creu gwrthrych `Cwpled`

Felly mae angen prosesu pennill un linell ar y tro, ac atodi
datrysiadau `None`, `CNG` neu `CWP` i'r mesur wrth fynd ymlaen.

Os oes un o'r datrysiadau yn Amwys, yna mae'r pennill yn Amwys.

TOB:    x: CNG7|CNG8|CNG9
        y: CBG9|CBG8|CBG7|SAI9
TOD     x: CBG10 (7+3|8+2|9+1)
        y: CNG9
TOH     x: CBG10 (7+3|8+2|9+1)
        y: CNG10

'''

from ceibwr.rhaniad import Rhaniad
from ceibwr.datrysiad import Datrysiad
from ceibwr.cynghanedd import Cynghanedd

from ceibwr.cynghanedd import Llusg, Sain
from ceibwr.cynghanedd import CroesBengoll, TrawsBengoll, SainBengoll, LlusgBengoll

from ceibwr.odlau import Odlau


class Cwpled(Datrysiad):
    '''
    Base class ar gyfer cwpledi.
    Yr unig amod ar `Cwpled` yw bod dwy linell a
    rhyw fath o odl rhyngddynt, yn cynnwys odl gyrch
    rhwng y cyntaf a'r ail (e.e. cwpled awdl-gywydd)

    CDH: cyfres o CC7
    CDF: cyfres o CC4
    AWG: cyfres o CAG

    '''

    def __init__(self, x, y, odlau, parent=None):
        '''
        Mewnbwn: rhestr o ddwy raniad lefel 2
        h.y. y naill a'r llall yn raniad sylfaenol
        (sef rhaniad yn cynnwys corfannau yn unig)
        '''
        Datrysiad.__init__(self, [x, y], parent=parent)

        # type check
        if not isinstance(x, Rhaniad) or not isinstance(y, Rhaniad):
            raise TypeError("CWP: mae angen dau wrthrych `Rhaniad` fan hyn.")

        if not type(odlau) is Odlau:
            raise TypeError("CWP: mae angen gwrthrych `Odlau` fan hyn.")

        self.odlau = odlau
        self.dosbarth = 'CWP'

    def __str__(self):
        return ''.join([str(child) for child in self.children])

    def __repr__(self):
        return '(' + str(self.dosbarth) + ', ' + repr(self.children) + ')'


# --------------------
# Cwpledi Caeth

class CwpledCaeth(Cwpled):
    def __init__(self, x, y, odlau, parent=None):
        Cwpled.__init__(self, x, y, odlau, parent=parent)

        # type check
        if not isinstance(x, Cynghanedd) or not isinstance(y, Cynghanedd):
            raise TypeError("CCA: mae angen dau wrthrych `Cynghanedd` fan hyn.")
        
        # check nad oes Llusg yn yr ail ran
        # TODO: check os yw hyn yn ofynnol ar gyfer Hir-a-Thoddaid ac eraill?
        # if isinstance(y, Llusg):
        #     raise ValueError("CCA: dim `Llusg` fan hyn.")

        self.dosbarth = 'CCA'


# --------------------
# Cwpledi Cywydd

class CwpledCywydd(CwpledCaeth):
    def __init__(self, x, y, odlau, parent=None):
        Cwpled.__init__(self, x, y, odlau, parent=parent)

        # type check
        CP = (CroesBengoll, TrawsBengoll, SainBengoll, LlusgBengoll)
        if isinstance(x, CP):
            raise TypeError("CCA: dim cyngahnedd bengoll yn y llinell gyntaf.")
        if isinstance(y, CP):
            raise TypeError("CCA: dim cyngahnedd bengoll yn yr ail linell.")

        # check aceniad
        if (
            (x.is_acennog() and y.is_acennog()) or
            (not x.is_acennog() and not y.is_acennog())
        ):
            raise ValueError("Mae angen gwahanol aceniad fan hyn.")

        # llwyddiant
        self.dosbarth = 'CCY'


class CwpledCywyddSeithsill(CwpledCywydd):
    '''
    Cwpled Cywydd Seithsill.

    Os nad yw pob amod wedi ei foddhau, dylen ni ddim
    creu CC7 ddiffygiol, e.e. os nad oes odl rhwng y
    ddwy ran, dim CC7 yw e! Felly mae angen gwneud pob 
    check yn __init__()

    Beth felly yw swyddogaeth prawf_cwpled? Bydd hwn yn
    cymryd dwy raniad a checko'r pethau yma anyway, ac ond
    yn creu e.e CC7 os yw'r amodau wedi eu boddhau.
    Felly "failsafe" yw'r checks yn CC7.__init__ ond 
    mae'n bwysig gwneud hyn. 

    Ond beth am "dosbarth = None" am "Amwys" neu "Rhydd"
    e.e falle bydd y ddwy gynghanedd yn gywir (seithsill ayb) ond 
    bod y ddau yn acennog, neu'r ddau yn ddiacen?

    Yr hyn sydd angen yw
        (None, [CNG7, CNG7])
    sef datrysiad cwpled rydd.

    Felly "double check" sydd fan hyn,
    er mwyn osgoi creu gwrthrychau diffygiol.
    '''
    def __init__(self, x, y, odlau, parent=None):
        CwpledCywydd.__init__(self, x, y, odlau, parent=parent)

        # check nifer sillafau
        if x.nifer_sillafau() != 7 or y.nifer_sillafau() != 7:
            raise ValueError("Mae angen [CNG7, CNG7] fan hyn.")

        # llwyddiant
        self.dosbarth = 'CC7'


class CwpledCywyddBedairsill(CwpledCywydd):
    def __init__(self, x, y, odlau, parent=None):
        CwpledCywydd.__init__(self, x, y, odlau, parent=parent)

        # check nifer sillafau
        if x.nifer_sillafau() != 4 or y.nifer_sillafau() != 4:
            raise ValueError("Mae angen [CNG4, CNG4] fan hyn.")

        # llwyddiant
        self.dosbarth = 'CC4'


class CwpledAwdlGywydd(Cwpled):
    def __init__(self, x, y, odlau, parent=None):
        Cwpled.__init__(self, x, y, odlau, parent=parent)

        # check nifer sillafau
        if x.nifer_sillafau() != 7 or y.nifer_sillafau() != 7:
            raise ValueError("Mae angen dwy raniad seithsill fan hyn.")

        # odlau/odlau cyrch?

        # llwyddiant
        self.dosbarth = 'CAG'


# --------------------
# Toddeidiau

class Toddaid(CwpledCaeth):
    '''
    Dwy raniad yn cyfateb i'r llinellau.
    Llinell gyntaf yn bengoll
    Odl gyrch rhwng diwedd y cyntaf a dechre'r ail
    Mae'r ail linell yn gynghanedd gyflawn (nawsill)

    Toddaid:
    Input: rhaniadau x ac y(lefel 2):
    x = (TBG10, [[A'u, gweld], [yn, eu, dillad, gwaith], [-, trwy'r, oriau]])
    y = (CBG9, [[Yn, rhwygo, o, greigiau], [eu, goreugwaith]])
    ODL(x[-2], y[-1])
    ODL(x[-1], y[0])

    Toddaid Byr:
    Input: rhaniadau x ac y (lefel 2):
    x = ('TRA', [[wele, rith], [fel, ymyl. rhod)]])
    y = ('CBG', [[o'n, cwmpas], [campwaith], [dewin hynod]])

    OGY(x[-1], y[-1])  # prif odl
    ODL(y[0], y[-1])   # odl gyrch!
    CNG9(y)

    TODO: os mai SAI9 sy'n olaf, mae'n bosib i'r odl
    gyrch fod rhwng naill ai'r rhagodl neu'r orodl:
        ODL(y[0]], y[1]) neu ODL(y[0], y[2])
    TODO: Hefyd y drydedd odl mewn SainDeirodl !!
    '''

    def __init__(self, x, y, odlau, odlau_cyrch, parent=None):
        Cwpled.__init__(self, x, y, odlau, parent=parent)

        # check nifer sillafau
        if x.nifer_sillafau() != 10 or y.nifer_sillafau() != 9:
            raise ValueError("Mae angen 10+9 sillaf.")

        # check odlau?

        # llwyddiant
        # print('HWRE')
        self.odlau_cyrch = odlau_cyrch
        self.dosbarth = 'TOD'


class ToddaidHir(CwpledCaeth):
    '''
    Cwpled 10 + 10
    Yn union fel Toddaid ond gyda deg sill yn y rhan olaf.
    '''
    def __init__(self, x, y, odlau, odlau_cyrch, parent=None):
        Cwpled.__init__(self, x, y, odlau, parent=parent)

        # check nifer sillafau
        if x.nifer_sillafau() != 10 or y.nifer_sillafau() != 10:
            raise ValueError("Mae angen 10+10 sillaf.")

        # llwyddiant
        self.odlau_cyrch = odlau_cyrch
        self.dosbarth = 'TOH'


class ToddaidByr(CwpledCaeth):
    '''
    Cwpled 10 + 6

    Mae dau fersiwn o'r toddaid byr mewn englyn [x1, x2, x3]
    0. Rhaniad x1 bob amser yn cynghaneddu
        e.e. CRO[x11, x12] neu SAI[x11, x12, x13]
    Fersiwn 1.
        [x21, x22] yn cynganeddu
        [x3] yn bengoll
    Fersiwn 2 (sain)
        [x21, x22] yn odli
        [x22, x3] yn cynganeddu

    Mae'r ail fath *yn union* fel cynghanedd sain, sef
    odl rhwng y ddwy gorfan gyntaf, a chytseinedd
    rhwng yr ail a'r trydydd.
    
    Mae diwedd y linell gyntaf felly yn BWYSIG, mae'n
    wastraff amser chwilio am raniadau sy'n goferu
    dros ddiwedd y gyntaf ymlaen i ddechrau'r ail. 
    Mae gorffwysfa ar ddiwedd llinell bob amser
    
    '''
    def __init__(self, x, y, odlau, parent=None):
        Cwpled.__init__(self, x, y, odlau, parent=parent)
    
        # print('x:', repr(x), type(x), isinstance(x, Cynghanedd), isinstance(x, Datrysiad))
        
        # type check
        # if not isinstance(x, Cynghanedd):
        #     raise ValueError("Mae angen `Cynghanedd` yn y rhan gyntaf, nid {}.".format(str(type(x))))

        # # type check
        # if not isinstance(r, CynghaneddBengoll):
        #     raise ValueError("Mae angen `CynghaneddBengoll` yn yr ail ran.")

        # check nifer sillafau
        if (
            x.nifer_sillafau() not in (7, 8, 9) or
            y.nifer_sillafau() not in (9, 8, 7) or
            x.nifer_sillafau() + y.nifer_sillafau() != 16
        ):
            raise ValueError("Mae angen 7+3+6 | 8+2+6 | 9+1+6 sillaf.")

        # check cynghanedd sain yn rhan 1
        # AYG: dylai'r orodl ddisgyn ar y bumed sillaf
        if isinstance(x, Sain):
            lleoliad = x[0].nifer_sillafau() + x[1].nifer_sillafau()
            if lleoliad != 5:
                # print("TOB: Dylai gorodl `SAIN` ddisgyn ar y bumed sillaf fan hyn.")
                pass

        # check cynghanedd sain yn rhan 2
        # Fel arfer mae'n rhaid rhedeg at y ddiwedd (AYG)
        # TODO: check am SainAlun
        if isinstance(y, Sain):
            if y.dosbarth == 'SBG':
                # print("TOB: Rhaid i'r gynghanedd sain redeg at ddiwedd y linell fan hyn.")
                pass
            
        # llwyddiant
        self.dosbarth = 'TOB'


# ------------------------------------------------
# test
def demo():

    from ceibwr.gair import Gair
    from ceibwr.corfan import Corfan

    c111 = Corfan([Gair("Wele "), Gair("rith ")])
    c112 = Corfan([Gair("fel "), Gair("ymyl "), Gair("rhod ")])
    c113 = Corfan([Gair("o'n "), Gair("cwmpas\n")])
    
    c121 = Corfan([Gair("campwaith ")])
    c122 = Corfan([Gair("dewin "), Gair("hynod\n")])

    c211 = Corfan([Gair("Hen "), Gair("linell ")])
    c212 = Corfan([Gair("bell ")])
    c213 = Corfan([Gair("nad "), Gair("yw'n "), Gair("bod\n")])

    c221 = Corfan([Gair("Hen "), Gair("derfyn ")])
    c222 = Corfan([Gair("nad "), Gair("yw'n "), Gair("darfod.\n")])

    # dummies
    from ceibwr.odlau import Odlau
    from ceibwr.cytseinedd import Cytseinedd
    off = Odlau()
    cff = Cytseinedd()

    from ceibwr.cynghanedd import Croes, Traws, Llusg, Sain
    from ceibwr.cynghanedd import CroesBengoll

    # ---------------
    # Check TOB
    c11 = Traws([c111, c112], cytseinedd=cff)
    c12 = CroesBengoll([c113, c121, c122], cytseinedd=cff)
    tob = ToddaidByr(c11, c12, odlau=off)

    # ---------------
    # Check CC7
    c21 = Sain([c211, c212, c213], odlau=off, cytseinedd=cff)
    c22 = Traws([c221, c222], cytseinedd=cff)
    cc7 = CwpledCywyddSeithsill(c21, c22, odlau=off)

    print('--------------------')
    print(tob)
    print(repr(tob))
    print(tob.ipa())
    print(type(tob))
    print('----------')
    print(cc7)
    print(repr(cc7))
    print(cc7.ipa())
    print(type(cc7))
    print('--------------------')

    print(isinstance(cc7, CwpledCywyddSeithsill))


def demo2():
    
    from ceibwr.gair import Gair
    from ceibwr.corfan import Corfan
    from ceibwr.datryswr_cynghanedd import prawf_cynghanedd
    from ceibwr.datryswr_odl import prawf_odl

    x11 = Corfan([Gair("Dwyglust "), Gair("feinion ")])
    x12 = Corfan([Gair("aflonydd\n")])
    x21 = Corfan([Gair("Dail "), Gair("saets ")])
    x22 = Corfan([Gair("wrth "), Gair("ei "), Gair("dâl "), Gair("y "), Gair("sydd.\n")])
    
    dat1 = prawf_cynghanedd([x11, x12])
    print(repr(dat1))
    
    dat2 = prawf_cynghanedd([x21, x22])
    print(repr(dat2))

    odlau = prawf_odl(x12.gair_olaf(), x22.gair_olaf())
    cwp = CwpledCywyddSeithsill(dat1, dat2, odlau)
    print(repr(cwp))

if __name__ == "__main__":
    demo2()
