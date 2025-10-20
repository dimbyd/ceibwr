# pennill.py

import os
from ceibwr.base import TreeNode
from ceibwr.llinell import Llinell


class Pennill(TreeNode):
    '''
    Pennill fel rhestr o wrthrychau `Llinell`
 
    OND pan yn datrys pennill, mae dal yn gwneud synnwyr i
    edrych ar pob llinell yn olynol, ac edrych ar y linell
    nesaf (ac efallai'r un ganlynol) er mwyn datrys cwpledi 
    ayb. 
    Felly mae pennill yn restr llinellau ond mae
      ENG = [TOB, CC7]
      EMI = [CNG7, CNG7, CNG7]
    yn ddatrysiadau penillion.

    Mae englyn wedi ei ysgrifennu ar bapur yn
    bennill, ond mae gwrthrych ENG yn ddatrysiad
    o'r pennill yma.

    Caiff gwrthrychau `Pennill` gael eu creu o
    `str` yn unig, nid o restr gwrthrychau `Llinell`.
    Mae'r constructor yn creu'r gwrthrychau `Llinell`
    sydd angen.

    Yn wahanol i hyn, mae'r goeden sain wedi creu allan o
    wrthrychau `Rhaniad`, sy ddim o angenrheidrwydd
    cyfateb gyda llinellau (gw. TOB).
    '''

    def __init__(self, s, parent=None):
        TreeNode.__init__(self, parent=parent)

        # type check input
        if not type(s) is str:
            raise TypeError('Mae angen `str` fan hyn.')

        # print('pe:>', s, '<:pe')
        s = s.strip()
        # print('pe:>', s, '<:pe')

        # value check (dim "\n\n")
        if os.linesep + os.linesep in s:
            raise ValueError("Llinell wag fan hyn.")

        for ss in s.split(os.linesep):
            ss = ss.strip()
            llinell = Llinell(ss, parent=self)
            self.children.append(llinell)

    def __str__(self):
        return ''.join([str(llinell) for llinell in self.children])

    def __repr__(self):
        return ''.join([repr(llinell) for llinell in self.children])

    def sain(self):
        return ''.join([llinell.sain() for llinell in self.children])

    def ipa(self):
        return ''.join([llinell.ipa() for llinell in self.children])

    # stats
    def nifer_llinellau(self):
        return len(self.children)

    def nifer_sillafau(self):
        return sum([child.nifer_sillafau() for child in self.children])

    def nifer_geiriau(self):
        return sum([child.nifer_geiriau() for child in self.children])

    # useful
    def nodau(self):
        s = []
        for child in self.children:
            s.extend(child.nodau())
        return s

    def geiriau(self):
        s = []
        for child in self.children:
            s.extend(child.geiriau())
        return s


# ------------------------------------------------
# test
def main():
    s = '''Wele rith fel ymyl rhod - o'n cwmpas
Campwaith dewin hynod
Hen linell bell nad yw'n bod
Hen derfyn nad yw'n darfod.'''

    p = Pennill(s)

    from ceibwr.seinyddwr import Seinyddwr
    se = Seinyddwr()
    for llinell in p.children:
        se.seinyddio_llinell(llinell)

    print('--------------------')
    print(p)
    print('--------------------')
    for llinell in p.children:
        print(llinell.nifer_sillafau(), str(llinell).replace('\n', '*'))
    print('SAIN ---------------')
    print(p.sain())
    print('IPA ----------------')
    print(p.ipa())
    print('--------------------')


if __name__ == "__main__":
    main()
