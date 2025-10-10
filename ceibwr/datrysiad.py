# datrysiad.py
'''
Class `Datrysiad`: rhaniad wedi ei ddatrys un ffordd neu'r llall.

"datrys" = "unravel"

Mae `Datrysiad` yn uwch-ddosbarth ar gyfer
`CNG`, `CWP`, `MES`, `AWD`

Mae rhain yn uwch-ddosbarthiadau ar gyfer
Lefel 1: `CNG`: `CRO`, `SAI`
Lefel 2: `CWP`: `CC7`, `TOB`
Lefel 3: `MES`: `CDH`, `EUU`
Lefel 4: `AWD`

a. Mae `SAI` yn subclass o `CNG` gyda 3-5 plentyn,
a phob plentyn o'r math `Corfan`

b1. Mae `CC7` yn subclass o `CWP` gyda dau blentyn,
y ddau o'r math `CNG`, ac odl rhyngddynt

b2. Mae `TOB` yn subclass o `CWP` gyda dau blentyn,
[`CNG`, `CNG`] lle gall yr ail CNG fod yn CBG/TBG/SBG/SAI.

c. Mae `ENG` yn subclass o `MES` gyda dau blentyn,
y cyntaf o'r math `TOB' a'r ail o'r math `CW7`,
ac odl rhyngddynt.

`Datrysiad`: rhaniad wedi ei ddosbarthu yn ôl cytseinedd ac odl
    rhaniad dau gorfan: CRO/TRA/LLU
    rhaniad tri chorfan: SAI/CBG/LLD ayb

'''
import os
import tabulate as tb
from copy import deepcopy

from ceibwr.nod import Llafariad, Cytsain
from ceibwr.corfan import Corfan
from ceibwr.rhaniad import Rhaniad
from ceibwr.cytseinedd import Cytseinedd
from ceibwr.beiro import Beiro

tb.PRESERVE_WHITESPACE = True


class Datrysiad(Rhaniad):
    '''
    Abstract class ar gyfer CNG, CWP, MES
    Mewnbwn: `list[Corfan]` neu `list[Rhaniad]`]
    '''
    def __init__(self, rhaniad, parent=None):
        Rhaniad.__init__(self, rhaniad, parent=parent)

        # type check
        if not isinstance(rhaniad, list):
            raise TypeError("Mae angen `list` fan hyn.")
        
        # type check
        if not all([isinstance(rhan, (Corfan, Rhaniad)) for rhan in rhaniad]):
            raise TypeError("Mae angen `list[Corfan|Rhaniad]` fan hyn.")

        self.hysbys = []

    # output
    def dosb(self):
        dosb = 'XXX' if not self.dosbarth else str(self.dosbarth)
        if self.lefel() == 1:
            dosb += str(self.nifer_sillafau())
        return dosb

    def __str__(self):
        return ''.join([str(child) for child in self.children])

    def __repr__(self):
        return '(' + str(self.dosb()) + ', ' + repr(self.children) + ')'

    # properties (duplicate?)
    def nifer_rhaniadau(self):
        if self.lefel() == 1:
            return 1
        return sum([child.nifer_rhaniadau() for child in self.children])

    def nifer_geiriau(self):
        return sum([child.nifer_geiriau() for child in self.children])

    def nifer_sillafau(self):
        return sum([child.nifer_sillafau() for child in self.children])

    # show
    def aceniad_str(self):
        '''
        Aceniad rhaniad Lefel 1
        CAC, CDI, AAC, ADI

        TODO: eithriadau megis SAG a'r cynganeddion pengoll
        '''

        # check
        if self.lefel() > 1:
            return ''

        if len(self.children) < 2:
            return ''

        if self.dosbarth in ['LLU', 'LLL', 'LDO']:
            return ''
        
        # if self.dosbarth in ['CBG', 'TBG', 'SBG', 'LBG']:
        #     x = self.children[-3][-1]
        #     y = self.children[-2][-1]
        
        # elif self.dosbarth in ['SGA']:
        #     x = self.children[-3][-1]
        #     y = self.children[-1][-1]

        else:
            x = self.children[-2][-1]
            y = self.children[-1][-1]

        # cytbwys acennog
        if x.is_acennog() and y.is_acennog():
            return "CAC"

        # anghytbwys ddiacen/ddisgynegig
        elif x.is_acennog() and not y.is_acennog():
            return "ADI"

        # anghytbwys acennog/ddyrchafedig
        elif not x.is_acennog() and y.is_acennog():
            return "AAC"

        # cytbwys ddiacen
        else:
            return "CDI"

    def show_odlau(self, toriad='', bwlch=' ', eol=os.linesep, cmap=None):

        beiro = Beiro()
        sep = toriad + bwlch if toriad else ''

        if self.lefel() == 1:

            # init
            rhaniad_strs = []

            # iteru dros corfannau
            for corfan in self.children:
                corfan_strs = []

                # iteru dros geiriau
                for gair in corfan.children:
                    gair_strs = []

                    # iteru dros sillafau
                    for sillaf in gair.children:
                        
                        # edrych am nodau cudd yn y sillaf flaenorol ???
                        # print(gair, repr(sillaf), type(sillaf))
                        # sf = sillaf.blaenorol()
                        # if hasattr(sf, 'nodau_cudd'):
                        #     print('nodau cudd:', sf.nodau_cudd)

                        gair_strs.append(str(sillaf.cyrch()))

                        # lliwio
                        if cmap and (
                            self.parent and
                            hasattr(self.parent, 'odlau') and
                            sillaf.odl() in self.parent.odlau
                        ):
                            gair_strs.append(beiro.write(str(sillaf.odl()), lliw=cmap['odlau']))

                        elif cmap and (
                            self.parent and self.parent.parent and
                            hasattr(self.parent.parent, 'odlau') and
                            sillaf.odl() in self.parent.parent.odlau
                        ):
                            gair_strs.append(beiro.write(str(sillaf.odl()), lliw=cmap['odlau']))

                        elif cmap and (
                            hasattr(self, 'odlau') and
                            sillaf.odl() in self.odlau
                        ):
                            gair_strs.append(beiro.write(str(sillaf.odl()), lliw=cmap['odlau_mewnol']))

                        else:
                            gair_strs.append(str(sillaf.odl()))

                    gair_strs.append(gair.terfyniad(bwlch=bwlch, eol=eol))
                    corfan_strs.append(''.join(gair_strs))

                rhaniad_strs.append(''.join(corfan_strs))

            return sep.join(rhaniad_strs)

        # Lefel > 1
        else:
            rhaniad_strs = []
            for rhan in self.children:
                rhan_str = rhan.show_odlau(toriad=toriad, bwlch=bwlch, eol=eol, cmap=cmap)
                rhaniad_strs.append(rhan_str)

            return ''.join(rhaniad_strs)

    def show_cytseinedd(self, toriad='', bwlch=' ', eol=os.linesep, cmap=None):

        beiro = Beiro()

        sep = bwlch*(len(toriad) + 1)
        if hasattr(self, 'cytseinedd'):
            sep = toriad + bwlch if toriad else ''

        if self.lefel() == 1:

            # init
            rhaniad_strs = []

            # iteru dros corfannau
            for corfan in self.children:
                corfan_strs = []

                # iteru dros geiriau
                for gair in corfan.children:
                    gair_strs = []

                    acen_str = bwlch
                    if gair is corfan.gair_olaf():
                        acen_str = ':'

                    # iteru dros nodau
                    for nod in gair.nodau():  # + gair.terfyn:

                        if type(nod) is Llafariad:
                            if hasattr(self, 'cytseinedd') and nod in gair.prif_lafariaid()[-2:]:
                                gair_strs.append(acen_str)
                            else:
                                gair_strs.append(bwlch*len(str(nod)))

                        elif type(nod) is Cytsain:
                            if hasattr(self, 'cytseinedd') and nod in self.cytseinedd:
                                dosb = self.cytseinedd[nod]
                                if cmap and dosb in cmap:
                                    gair_strs.append(beiro.write(str(nod), lliw=cmap[dosb]))
                                else:
                                    gair_strs.append(str(nod))
                            else:
                                gair_strs.append(bwlch*len(str(nod)))

                        else:
                            gair_strs.append(bwlch)

                    # end iteru dros gair
                    gair_strs.append(gair.terfyniad(bwlch=bwlch, eol=eol))
                    corfan_strs.append(''.join(gair_strs))

                # end iteru dros corfan
                rhaniad_strs.append(''.join(corfan_strs))

            # end iteru
            return sep.join(rhaniad_strs)

        # Lefel > 1
        else:
            rhannau_strs = []
            for rhan in self.children:
                rhan_str = rhan.show_cytseinedd(toriad=toriad, bwlch=bwlch, eol=eol, cmap=cmap)
                rhannau_strs.append(rhan_str)

            return ''.join(rhannau_strs)

    def show_text(self, toriad='', bwlch=' ', eol=os.linesep):
        return super().show_text(toriad=toriad, bwlch=bwlch, eol=eol)

    def show_fancy(self, block=True, toriad='', bwlch=' ', eol=os.linesep, cmap=None):

        acenion_str = self.show_acenion(toriad=toriad, bwlch=bwlch, eol='*')
        odlau_str = self.show_odlau(toriad=toriad, bwlch=bwlch, eol='*', cmap=cmap)
        cytseinedd_str = self.show_cytseinedd(toriad=toriad, bwlch=bwlch, eol='*', cmap=cmap)

        if block:
            
            # split
            a = acenion_str.rstrip('*').split('*')
            b = odlau_str.rstrip('*').split('*')
            c = cytseinedd_str.rstrip('*').split('*')
            d = ['']*len(a)

            # interleave
            lists = [a, b, c, d]
            rows = [val for tup in zip(*lists) for val in tup]
            
            return eol.join(rows)

        else:

            return eol.join([acenion_str, odlau_str, cytseinedd_str])

    # tabulate
    def create_headers(self):

        headers = ["Llinell", "CNG", "NSI", "ACE", "CYT", "ODF"]
        
        if self.lefel() > 1:
            headers.extend(["CWP", "ODG"])

        if self.lefel() > 2:
            headers.extend(["MES", "ODL"])
        
        if self.lefel() > 3:
            headers.extend(["AWD"])
        
        return headers

    def _create_rows(self, fancy=False, toriad='|', bwlch=' ', eol=os.linesep, cmap=None):

        rows = []
        if self.lefel() == 1:
            if fancy:
                disp = self.show_fancy(toriad=toriad, bwlch=bwlch, eol=eol, cmap=cmap)
            else:
                disp = self.show_text(bwlch=bwlch, eol=eol)
            row = [disp,
                   self.dosbarth,
                   self.nifer_sillafau(),
                   self.aceniad_str(),
                   self.cytseinedd_str(),
                   self.odlau_str()
                   ]
            return [row]

        # hack Toddaid Byr (revert i'r llinellau gwreiddiol)
        elif self.dosbarth == 'TOB':

            x, y = self.children
            xnew = deepcopy(x)
            ynew = deepcopy(y)
            if not hasattr(xnew, 'cytseinedd'):
                xnew.cytseinedd = Cytseinedd()

            cyrch = ynew.children.pop(0)
            xnew.children.append(cyrch)
            if hasattr(ynew, 'cytseinedd'):
                for nod in cyrch.nodau():
                    if nod in ynew.cytseinedd:
                        xnew.cytseinedd[nod] = ynew.cytseinedd[nod]
            
            xnew_row = xnew.create_rows(fancy=fancy, toriad=toriad, bwlch=bwlch, eol=eol, cmap=cmap)
            ynew_row = ynew.create_rows(fancy=fancy, toriad=toriad, bwlch=bwlch, eol=eol, cmap=cmap)
            rows.extend(xnew_row)
            rows.extend(ynew_row)

        # recursive call
        else:
            for child in self.children:
                child_rows = child._create_rows(fancy=fancy, toriad=toriad, bwlch=bwlch, eol=eol, cmap=cmap)
                rows.extend(child_rows)

        # pad
        if self.lefel() == 2:
            for idx in range(len(rows)):
                rows[idx] = rows[idx] + [None]*2
            row = [None]*6 + [self.dosbarth, self.odlau_str()]

        elif self.lefel() == 3:
            for idx in range(len(rows)):
                rows[idx] = rows[idx] + [None]*2
            row = [None]*8 + [self.dosbarth, self.odlau_str()]

        else:
            for idx in range(len(rows)):
                rows[idx] = rows[idx] + [None]
            row = [None]*10 + [self.dosbarth]

        rows.append(row)
        return rows

    def create_rows(self, headers=False, fancy=False, toriad='|', bwlch=' ', eol=os.linesep, cmap=None):
        rows = self._create_rows(fancy=fancy, toriad=toriad, bwlch=bwlch, eol=eol, cmap=cmap)
        if headers:
            ncols = len(rows[0])
            head = self.create_headers()[:ncols]
            rows.insert(0, head)
        return rows

    def create_tabular(self, fancy=False, fmt='fancy_grid', toriad='', bwlch=' ', eol=os.linesep, cmap=None):
        rows = self.create_rows(headers=False, fancy=fancy, toriad=toriad, bwlch=bwlch, eol=eol, cmap=cmap)
        return tb.tabulate(
                rows,
                headers=self.create_headers(),
                tablefmt=fmt,
        )

    # create printables
    def odlau_str(self):

        odlau_str = ''
        if hasattr(self, 'odlau') and self.odlau:
            # print('odlau:', self.odlau)
            odlau_strs = []
            for od in self.odlau:
                odlau_strs.append(''.join([str(nod) for nod in od.nodau(atalnodau=False, h2b=True)]))
            odlau_str = min(odlau_strs, key=len)
            # print('odlau_str:', odlau_str)

        odlau_cyrch_str = ''
        if hasattr(self, 'odlau_cyrch') and self.odlau_cyrch:
            odlau_cyrch_strs = []
            for od in self.odlau_cyrch:
                odlau_cyrch_strs.append(''.join([str(nod) for nod in od.nodau(atalnodau=False, h2b=True)]))
            odlau_cyrch_str = min(odlau_cyrch_strs, key=len)
            if odlau_cyrch_str:
                odlau_str = ', '.join([odlau_str, odlau_cyrch_str])

        # print('odlau_str2:', odlau_str)
        return odlau_str 

    def cytseinedd_str(self, cudd=True):

        cytseinedd_str = ''
        if hasattr(self, 'cytseinedd'):
            cyts = list(set([str(c).lower() for c in self.cytseinedd.nodau('GEF')]))
            cyts.sort()
            cytseinedd_str = ' '.join(cyts)
        
        return cytseinedd_str 

    # lookup tables for templates
    def cyfuno_acenion(self):
        acenion = {}
        for child in self.children:
            if type(child) is Corfan:
                for gair in child.children:
                    for sillaf in gair.children:
                        for nod in sillaf.nodau():
                            if nod in gair.prif_lafariaid():
                                # print(nod, sillaf, type(sillaf), gair.prif_sillaf())
                                if sillaf is gair.prif_sillaf():
                                    acenion[nod] = 'PRA'
                                else:
                                    acenion[nod] = 'ISA'
            else:
                acenion = acenion | child.cyfuno_acenion()
        
        return acenion

    def cyfuno_cytseinedd(self):
        if self.lefel() == 1:
            if hasattr(self, 'cytseinedd'):
                return self.cytseinedd  # dict
            return {}
        else:
            cyts = {}
            for child in self.children:
                cyts = cyts | child.cyfuno_cytseinedd()
            return cyts

    def cyfuno_odlau(self):

        odlau = {}

        if self.lefel() == 1:
            if hasattr(self, 'odlau'):
                return {key: 'OFE' for key in self.odlau}
        else:
            if hasattr(self, 'odlau'):
                odlau = odlau | {key: 'ODL' for key in self.odlau}
            if hasattr(self, 'odlau_cyrch'):
                odlau = odlau | {key: 'OGY' for key in self.odlau_cyrch}

            for child in self.children:
                odlau = odlau | child.cyfuno_odlau()

        return odlau

    # stats (token: leave stats to jupyter/pandas)
    def stats(self):
        s = []
        s.append(f'Nifer geiriau:  {self.nifer_geiriau()}')
        s.append(f'Nifer sillafau: {self.nifer_sillafau()}')
        return '\n'.join(s)

    def freq(self):
        def _freq(self):
            if self.lefel() == 1:
                if self.dosbarth:
                    return [int(self.dosbarth[0] == z) for z in ('C', 'T', 'L', 'S')]
                else:
                    return [0, 0, 0, 0]
            else:
                freq = [0, 0, 0, 0]
                for child in self.children:
                    freq = [x+y for x, y in zip(freq, child._freq())]
                return freq
        freq = self._freq()
        return {
            'croes': freq[0],
            'traws': freq[1],
            'llusg': freq[2],
            'sain': freq[3],
        }

    # export to csv (needs work)
    def export_csv(self, filename):
        rows = self.create_rows(headers=True, fancy=False)
        csv = os.linesep.join([','.join([str(z) for z in x]) for x in rows])
        print(csv)


# -----------
# null object (synonym for `Datrysiad` with `dosbarth=None`)
class Amwys(Datrysiad):

    def __init__(self, rhaniad, parent=None):
        Datrysiad.__init__(self, rhaniad, parent=parent)

        self.dosbarth = None


# ------------------------------------------------
# test
def main():

    from ceibwr.cysonion import colormaps
    cmap = colormaps['default']

    # Test Llinell (CNG)
    from ceibwr.llinell import Llinell
    from ceibwr.datryswr_llinell import datryswr_llinell

    s = """Llewpart a dart yn ei din"""
    ll = Llinell(s)
    dat = datryswr_llinell(ll)
    tab = dat.create_tabular(fancy=True, cmap=cmap)
    print(tab)

    # Test Pennill (MES)
    from ceibwr.pennill import Pennill
    from ceibwr.datryswr_pennill import datryswr_pennill

    s = """Wele rith fel ymyl rhod - o'n cwmpas,
Campwaith dewin hynod;
Hen linell bell nad yw'n bod,
Hen derfyn nad yw'n darfod."""
    p = Pennill(s)
    dat = datryswr_pennill(p)
    tab = dat.create_tabular(fancy=True, cmap=cmap)
    print(tab)


if __name__ == "__main__":
    main()
