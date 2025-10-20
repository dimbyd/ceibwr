# corfan.py
'''
`Corfan`: rhestr geiriau  # metrical foot
    [g1, g2, g3]


c1 = ["Wele", "rith"]
c2 = ["Fel", "ymyl", "rhod"]

'''
import os
from ceibwr.base import TreeNode
from ceibwr.nod import EOL
from ceibwr.gair import Gair


class Corfan(TreeNode):
    '''
    Rhestr geiriau.
    '''
    def __init__(self, geiriau=None, parent=None):
        TreeNode.__init__(self, parent=parent)

        if (
            type(geiriau) is not list or
            not all([type(child) is Gair for child in geiriau])
        ):
            raise ValueError('Mae angen rhestr o wrthrychau `Gair` fan hyn.')

        self.children = geiriau
        for child in self.children:
            child.parent = self

    def __str__(self):
        return ''.join([str(gair) + gair.terfyniad() for gair in self.children])

    def __repr__(self):
        return repr(self.children)

    def __len__(self):
        return len(self.children)

    def __add__(self, other):
        if isinstance(other, Corfan):
            return Corfan(self.children + other.children)
        return ()

    def __setitem__(self, idx, eitem):
        self.children[idx] = eitem

    def __getitem__(self, idx):
        return self.children[idx]

    def append(self, eitem):
        self.children.append(eitem)

    # sain
    def sain(self):
        return " ".join([gair.sain() for gair in self.children])

    def ipa(self):
        return " ".join([gair.ipa() for gair in self.children])

    # stats
    def nifer_geiriau(self):
        return len(self.children)

    def nifer_sillafau(self):
        return sum([child.nifer_sillafau() for child in self.children])

    # access methods
    def geiriau(self):
        return list(self.children)  # shallow copy

    def nodau(self, terfyniadau=True):
        nodau = []
        for gair in self.children:
            nodau.extend(gair.nodau())
            if terfyniadau:
                nodau.extend(gair.terfyn)
        return nodau

    def cytseiniaid(self):
        s = []
        for gair in self.children:
            s.extend(gair.cytseiniaid())
        return s

    def is_acennog(self):
        return self.children[-1].is_acennog()

    def gair_olaf(self):
        return self.children[-1]

    def sillaf_olaf(self):
        return self.children[-1].children[-1]

    # show
    def show_text(self, toriad='', bwlch=' ', eol=os.linesep):
        sep = toriad + bwlch if toriad else ''
        s = ''.join([gair.show_text(bwlch=bwlch, eol=eol) for gair in self.children])
        if any([type(nod) is EOL for nod in self.gair_olaf().terfyn]):
            return s
        return s + sep

    def show_acenion(self, toriad='', bwlch=' ', eol=os.linesep):
        sep = bwlch*(len(toriad) + 1) if toriad else ''
        s = ''.join([gair.show_acenion(bwlch=bwlch, eol=eol) for gair in self.children])
        if any([type(nod) is EOL for nod in self.gair_olaf().terfyn]):
            return s
        return s + sep

    def fancy(self):
        acenion = self.show_acenion(eol='*').split('*')
        geiriau = self.show_text(eol='*').split('*')
        return [x for y in zip(acenion, geiriau) for x in y]


# ------------------------------------------------
# test
def main():
    corfan = Corfan([Gair("o'n "), Gair("cwmpas\n"), Gair("campwaith ")])
    print(corfan)
    print()
    print(corfan.show_text())
    print(corfan.show_text(eol='*'))
    print(corfan.show_text(bwlch='~', eol='*'))
    print()
    print(corfan.show_acenion(eol='*'))
    print(corfan.show_text(eol='*'))
    print()
    # print(corfan.fancy())
    # print()
    acenion = corfan.show_acenion(eol='*').split('*')
    text = corfan.show_text(eol='*').split('*')
    # ac = acenion.split('*')
    # ge = geiriau.split('*')

    # interleave
    for line in [x for y in zip(acenion, text) for x in y]:
        print(line)


if __name__ == "__main__":
    main()
