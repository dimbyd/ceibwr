# mesur.py
'''
`Mesur` type

1. Englynion (7)
Enlyn unodl union       EUU     [TOB, CC7]                ODL(x1,x2)
Englyn milwr            EMI     [CNG7, CNG7, CNG7]        ODL(x1,x2,x3)
Englyn penfyr           EPF     [TOB, CNG7]               ODL(x1,x2)
Englyn crwca            ECR     [CC7, TOB]                ODL(x1,x2)
Englyn cyrch            ECY     [CC7, CNG7, CNG7]         ODL(x1,x2,x3)
Englyn cyfnewidiog      ECF     [CNG7, CNG7, CNG7, CNG7]  ODL(x1,x2,x3,x4)
Englyn cadwynog         ECA     [CNG7, CNG7, CNG7, CNG7]  ODL(x1,x3), ODL(x3,x4), PRO(x1,x2)

2. Cywyddau (4)
Cywydd deuair hirion    CDH     [CC7, CC7, ...]
Cywydd deuair fyrion    CDF     [CC4, CC4, ...]
Awdl-gywydd             AWG     [CAG, CAG, ...]
Cywydd llosgyrnog       CLL

TODO: Mae angen quatrains ar AWG:
QSS: prifodl "abab" (cwatrain soned Shakesperaidd)
QAG: prifodl "abcb" (cwatrain awdl-gywydd)

AWG     [CNG7, CNG7, CNG7, CN7]      OGY(1, 2), OGY(3, 4), ODL(2, 4)
AWG     [CAG, CAG]                   ODL(1, 2)

3. Eraill (13)
Hir-a-thoddaid          HAT     [CNGX, CNGX, CNGX, CNGX, TOD]
Byr-a-thoddaid          BAT

Gwawdodyn byr           GWB     [CNG9, CNG9, TOD]
Gwawdodyn hir           GWH     [CNG9, CNG9, CNG9, CNG9, TOD]

Rhupunt byr             RHB     [CO4, CO4, CO4]         ODL(1, 2),      CNG(2, 3)
Rhupunt hir             RHH     [CO4, CO4, CO4, CO4]    ODL(1, 2, 3)    CNG(3, 4)

Cyhydedd nawban         CYN     [CN9, CN9, CN9, CN9]    ODL(1, 2, 3, 4)
Cyhydedd fer            CYF     [CN8, CN8, CN8, CN8]    ODL(1, 2, 3, 4)
Cyhydedd hir            CYH     [CN5, CN5, CO5, CO4]    ODL(1, 2, 3), CNG(3, 4)

TODO:
Clogyrnach
Cyrch-a-chwta
Tawddgyrch cadwynog
Cadwynfyr

'''

from ceibwr.gair import Gair
from ceibwr.corfan import Corfan
from ceibwr.datrysiad import Datrysiad

from ceibwr.cynghanedd import Cynghanedd, Llusg
from ceibwr.cwpled import ToddaidByr, CwpledCywyddBedairsill, CwpledCywyddSeithsill, CwpledAwdlGywydd

from ceibwr.datryswr_odl import prawf_odl


class Mesur(Datrysiad):
    '''
    Abstract class ar gyfer EUU, EMI, CDH, CDF, HAT, ...

    Mae creu gwrthrych `Mesur` yn "constructive process"
    e.e. am EUU mae angen creu TOB a CC7 yn gyntaf,
     wedyn eu cyfuno fel mewnbwn i'r "constructor".

    Mae hyn hefyd yn wir am CWP a TOD
        mae angen creu [CNG, CNG] yn gyntaf

    Mae'r checks mewnol er mwyn sicrhau nad ein
    bod yn creu gwrthrychau diffygiol.

    '''

    def __init__(self, rhaniad, parent=None):
        Datrysiad.__init__(self, rhaniad, parent=parent)

    def __str__(self):
        return ''.join([str(elfen) for elfen in self.children])

    def nifer_sillafau(self):
        return sum([child.nifer_sillafau() for child in self.children])


# -------------------------------
# CYWYDDAU
# -------------------------------
class CywyddDeuairHirion(Mesur):
    '''
    Mewnbwn: rhestr o datrysiadau: [CC7, CC7, ...]
    '''
    def __init__(self, rhaniad, odlau=None, parent=None):
        Mesur.__init__(self, rhaniad, parent=parent)

        # type check
        if not all([type(x) is CwpledCywyddSeithsill for x in rhaniad]):
            raise TypeError("Mae angen `list[CC7]` fan hyn.")

        # TODO: check odlau (er mwyn peidio creu gwrthrychau diffygiol)
        self.odlau = odlau

        # llwyddiant
        self.dosbarth = 'CDH'


class CywyddDeuairFyrion(Mesur):
    '''
    Mewnbwn: rhestr o datrysiadau: [CC4, CC4, ...]
    '''
    def __init__(self, rhaniad, parent=None):
        Mesur.__init__(self, rhaniad, parent=parent)

        # type check
        if not all([type(x) is CwpledCywyddBedairsill for x in rhaniad]):
            raise TypeError("Mae angen rhestr o CC4 fan hyn.")

        # llwyddiant
        self.dosbarth = 'CDF'


class AwdlGywydd(Mesur):
    '''
    Mewnbwn: rhestr o datrysiadau: [CAG, CAG, ...]
    '''
    def __init__(self, rhaniad, parent=None):
        Mesur.__init__(self, rhaniad, parent=parent)

        # type check
        if not all([type(x) is CwpledAwdlGywydd for x in rhaniad]):
            raise TypeError("Mae angen rhestr o CC4 fan hyn.")

        # llwyddiant
        self.dosbarth = 'CAG'


# -------------------------------
# ENGLYNION
# -------------------------------

class EnglynUnodlUnion(Mesur):
    '''
    Mewnbwn: [TOB, CC7]
    '''
    def __init__(self, rhaniad, parent=None):
        Mesur.__init__(self, rhaniad, parent=parent)

        # type check
        if not type(rhaniad) is list or len(rhaniad) != 2 or (
            not isinstance(rhaniad[0], ToddaidByr) or
            not isinstance(rhaniad[1], CwpledCywyddSeithsill)
        ):
            raise TypeError("EUU: mae angen `[TOB, CC7]` fan hyn.")

        x1, x2 = rhaniad

        # check odl
        odlau = prawf_odl(x1.gair_olaf(), x2.gair_olaf())
        if not odlau:
            raise ValueError('EUU: mae angen odlau fan hyn.')

        # llwyddiant
        self.odlau = x1.odlau + x2.odlau
        self.dosbarth = 'EUU'


class EnglynCrwca(Mesur):
    '''
    Mewnbwn: [CC7, TOB]
    '''
    def __init__(self, rhaniad, parent=None):
        Mesur.__init__(self, rhaniad, parent=parent)

        # type check
        if not type(rhaniad) is list or len(rhaniad) != 2 or (
            not isinstance(rhaniad[0], CwpledCywyddSeithsill) or
            not isinstance(rhaniad[1], ToddaidByr)
        ):
            raise TypeError("ECR: mae angen `[CC7, TOB]` fan hyn.")

        x1, x2 = rhaniad

        # check odl
        odlau = prawf_odl(x1.gair_olaf(), x2.gair_olaf())
        if not odlau:
            raise ValueError('ECR: mae angen odlau fan hyn.')

        # llwyddiant
        self.odlau = x1.odlau + x2.odlau
        self.dosbarth = 'ECR'


class EnglynMilwr(Mesur):
    '''
    Mewnbwn: [CNG7, CNG7, CNG7])
    '''
    def __init__(self, rhaniad, parent=None):
        Mesur.__init__(self, rhaniad, parent=parent)

        # type check
        if len(rhaniad) != 3 or (
            not all([isinstance(rhan, Cynghanedd) for rhan in rhaniad])
        ):
            raise ValueError("EMI: mae angen [CNG7, CNG7, CNG7] fan hyn.")

        x1, x2, x3 = rhaniad

        # check odlau
        odlau12 = prawf_odl(x1.gair_olaf(), x2.gair_olaf())
        odlau13 = prawf_odl(x1.gair_olaf(), x3.gair_olaf())
        if not odlau12 or not odlau13:
            raise ValueError('EMI: mae angen odlau fan hyn.')

        # llwyddiant
        self.dosbarth = 'EMI'
        self.odlau = odlau12 + odlau13


class EnglynPenfyr(Mesur):
    '''
    Mewnbwn: [TOB, LL7]
    '''
    def __init__(self, rhaniad, parent=None):
        Mesur.__init__(self, rhaniad, parent=parent)

        # print('++++++++++++')
        # print(type(rhaniad) is list)
        # print(type(rhaniad[0]) is ToddaidByr)
        # print(isinstance(rhaniad[0], ToddaidByr))
        # print('++++++++++++')

        if not type(rhaniad) is list or len(rhaniad) != 2 or (
            type(rhaniad[0]) is not ToddaidByr or
            not isinstance(rhaniad[1], Cynghanedd) or
            isinstance(rhaniad[1], Llusg)
        ):
            raise TypeError("EPF: Mae angen `[CC7, CNG7]` fan hyn.")

        x1, x2 = rhaniad
        
        # check nifer sillafau
        if x2.nifer_sillafau() != 7:
            raise ValueError("EPF: mae angen CNG7 fan hyn.")
        
        # check odl
        odlau12 = prawf_odl(x1.gair_olaf(), x2.gair_olaf())
        if not odlau12:
            raise ValueError('EPF: mae angen odlau fan hyn.')

        # llwyddiant
        self.odlau = x1.odlau + odlau12
        self.dosbarth = 'EPF'


class EnglynCyrch(Mesur):
    '''
    Mewnbwn: Rhaniad([CC7, CNG7, CNG7])
    '''
    def __init__(self, rhaniad, parent=None):
        Mesur.__init__(self, rhaniad, parent=parent)

        if not type(rhaniad) is list or len(rhaniad) != 3 or (
            type(rhaniad[0]) is not CwpledCywyddSeithsill or
            not isinstance(rhaniad[1], Cynghanedd) or
            not isinstance(rhaniad[2], Cynghanedd) or
            isinstance(rhaniad[2], Llusg)
        ):
            raise TypeError("ECY: Mae angen `[CC7, CNG7, CNG7]` fan hyn.")
 
        x1, x2, x3 = rhaniad
        
        odlau13 = prawf_odl(x1.gair_olaf(), x3.gair_olaf())
        odlau_cyrch23 = prawf_odl(x2.gair_olaf(), x3[0].gair_olaf())
        if not (odlau13 and odlau_cyrch23):
            raise ValueError('ECY: mae angen odlau fan hyn.')

        # llwyddiant
        self.odlau = x1.odlau + odlau13 + odlau_cyrch23
        self.dosbarth = 'ECY'


# ------------------------------------------------
# test
def main():

    # manual test
    x111 = Corfan([Gair("Wele "), Gair("rith ")])
    x112 = Corfan([Gair("fel "), Gair("ymyl "), Gair("rhod ")])
    x113 = Corfan([Gair("o'n "), Gair("cwmpas\n")])

    x121 = Corfan([Gair("campwaith ")])
    x122 = Corfan([Gair("dewin "), Gair("hynod.\n")])

    x211 = Corfan([Gair("Hen "), Gair("linell ")])
    x212 = Corfan([Gair("bell ")])
    x213 = Corfan([Gair("nad "), Gair("yw'n "), Gair("bod,\n")])

    x221 = Corfan([Gair("Hen "), Gair("derfyn ")])
    x222 = Corfan([Gair("nad "), Gair("yw'n "), Gair("darfod.\n")])

    from ceibwr.odlau import Odlau
    from ceibwr.cytseinedd import Cytseinedd
    from ceibwr.cynghanedd import Traws, CroesBengoll, Sain

    # null objects
    cff = Cytseinedd()
    off = Odlau()

    # paladr
    x11 = Traws([x111, x112], cytseinedd=cff)
    x12 = CroesBengoll([x113, x121, x122], cytseinedd=cff)
    odlau1 = prawf_odl(x11.gair_olaf(), x12.gair_olaf())
    tob = ToddaidByr(x11, x12, odlau1)

    # esgyll
    x21 = Sain([x211, x212, x213], odlau=off, cytseinedd=cff)
    x22 = Traws([x221, x222], cytseinedd=cff)
    odlau2 = prawf_odl(x21.gair_olaf(), x22.gair_olaf())
    cc7 = CwpledCywyddSeithsill(x21, x22, odlau2)

    odlau = prawf_odl(x11.gair_olaf(), x21.gair_olaf())
    if odlau:
        eng = EnglynUnodlUnion([tob, cc7])

        print('ENGLYN')
        print(eng)
        print(repr(eng))
        print('---------------------')
        print(eng.create_tabular(fancy=True))

    else:
        print('Dim odlau??')


if __name__ == "__main__":
    main()
