# llinell.py

import os
import re

from ceibwr.base import TreeNode
from ceibwr.gair import Gair
from ceibwr.nod import Bwlch


class Llinell(TreeNode):
    """
    Llinell fel rhestr geiriau.

    Mae'r gair olaf yn amgodio yr EOL terfynnol.
    """

    def __init__(self, s, parent=None):
        TreeNode.__init__(self, parent=parent)

        # rhestr geiriau
        if type(s) is list and all([type(x) is Gair for x in s]):
            self.children = s

        # str
        elif type(s) is str:

            # value check (dim eols yn y canol)
            if os.linesep in s.strip():
                raise ValueError('EOL yn y canol.')

            # creu rhestr geiriau (hollti ar fylchau)
            t = re.split("(os.linesep| +)", s)
            svals = [c + d for c, d in list(zip(t[::2], t[1::2]+[os.linesep]))]
            for ss in svals:
                ss = ss.lstrip()
                if ss:
                    gair = Gair(ss.lstrip(), parent=self)
                    # print('G:', repr(gair), '>{}<'.format(ss.lstrip()))
                    self.children.append(gair)

        # bad input
        else:
            raise TypeError('Mae angen `str` fan hyn.')

    def __str__(self):
        return ''.join([str(gair) + gair.terfyniad() for gair in self.children])

    def __repr__(self):
        return ' '.join([repr(gair) + gair.terfyniad() for gair in self.children])

    def sain(self):
        return ''.join([gair.sain() + gair.terfyniad() for gair in self.children])

    def ipa(self):
        return ''.join([gair.ipa() + gair.terfyniad() for gair in self.children])

    def geiriau(self):
        return list(self.children)  # shallow copy

    def sillafau(self):
        return [sillaf for gair in self.children for sillaf in gair.sillafau()]

    def nodau(self, gofod=False):
        if not gofod:
            return [nod for gair in self.children for nod in gair.nodau()]
        else:
            nodau = []
            for idx, gair in enumerate(self.children):
                nodau = nodau + gair.nodau()
                if idx < len(self.children) - 1:
                    nodau.append(Bwlch())
            return nodau

    def prifodl(self):
        if self.children:
            return self.children[-1]
        return None

    # stats
    def nifer_geiriau(self):
        return len(self.children)

    def nifer_sillafau(self):
        return sum([g.nifer_sillafau() for g in self.children])


# ------------------------------------------------
# test
def main():

    s = 'O dad yn deulu dedwydd'
    s = "A’i cheraint a’i chwiorydd:"
    x = Llinell(s)
    print(x)
    print(repr(x))
    print(x.sain())
    print(x.ipa())


if __name__ == "__main__":
    main()
