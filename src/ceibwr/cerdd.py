# pennill.py
import os
from ceibwr.base import TreeNode
from ceibwr.pennill import Pennill


class Cerdd(TreeNode):
    '''
    Cerdd fel rhestr o wrthrychau `Pennill`
    '''

    def __init__(self, s, parent=None):
        TreeNode.__init__(self, parent=parent)

        # input: str
        if type(s) is str:

            for ss in s.split(os.linesep + os.linesep):
                ss = ss.rstrip()
                pennill = Pennill(ss, parent=self)
                self.children.append(pennill)

        # bad input
        else:
            raise TypeError('Mae angen `str` fan hyn.')

    def __str__(self):
        return os.linesep.join([str(pennill) for pennill in self.children])

    def __repr__(self):
        return (os.linesep+os.linesep).join([repr(pennill) for pennill in self.children])

    def sain(self):
        return os.linesep.join([pennill.sain() for pennill in self.children])

    def ipa(self):
        return os.linesep.join([pennill.ipa() for pennill in self.children])

    # stats
    def nifer_penillion(self):
        return len(self.children)

    def nifer_llinellau(self):
        return sum([pennill.nifer_llinellau() for pennill in self.children])

    def acenion_str(self, blanksymbol=' '):
        return "\n\n".join([
            child.acenion_str(blanksymbol=blanksymbol)
            for child in self.children
            ])

    def geiriau(self):
        s = []
        for child in self.children:
            s.extend(child.geiriau())
        return s


def main():
    s = '''
Gwelwn echrysa golwg,
Gwael iawn ddrych y galon ddrwg:
Calon afradlon o fryd,
Annuwiol heb ei newid:
Calon yw mam pob cilwg,
An-noeth drefn, a nyth y drwg;
Drwg ddi-obaith, draig ddiball,
Pwy edwyn ei gwŷn a'i gwall?

Effaith y cwymp, a'i ffrwyth cas,
A luniodd pob galanas;
Grym pechod yn ymgodi,
A'i chwantau fel llynnau lli;
Glennydd afonydd y fall,
Dengys bob nwydau anghall;
Dîg-ofid yn dygyfor,
Tân a mŵg, fel tonnau môr:
Uffern yw hon, o'i ffwrn hi
Mae bariaeth yma'n berwi:
Ysbyty, llety pob llid,
Gwe gyfan gwae a gofid;
Trigfa pob natur wagfost,
Bwystfilaidd 'nifeilaidd fost:
Treigle a chartref-le trais,
Rhyfeloedd, a phob rhyw falais;
Rhial pob an-wadal wŷn,
Ty ac aelwyd y gelyn.
Meirch, a chwn, a moch annwn,
Sy'n tewhau yn y ty hwn,
Seirff hedegog mewn ogo,
A heigiau dreigiau blin dro.
Pob lleisiau, arw foesau'r fall,
Sy'n dwad i swn deall;

Swn t'ranau, sain trueni,
Swn gofalon greulon gri:
Melin wynt, yn malu'n wâg,
Rhod o agwedd rhedeg-wag;
A'i chocys afaelus fôn,
Yn troi'u gilydd trwy'n galon;
Drylliad, ag ebilliad bach,
Y maen isaf, mae'n hawsach,
Na dryllio, gwir bwyllo i'r bon,
Ceulaidd, drygioni calon,
C'letach a thrawsach ei thrin,
Mewn malais, na maen melin.

Llais hen Saul, a llys hwn sydd,
Fan chwerw, o fewn ei chaerydd.
Ni all telyn a dyn doeth,
Clywn, ennill calon annoeth.

Och! ni byth, achwyn y bo'n,
Wrth goelio, fod fath galon:
Gweddiwn, llefwn rhag llid,
Yn Nuw, am gael ei newid.
Nid oes neb a'i hadnebydd,
Ond gain y Tad, a'i rad rydd;
A'n gair os daw, gwiw-ras dôn,
A dry'r golwg drwy'r galon:
A drwg calon draw cilio,
Amen fyth, mai hynny fo.'''

    c = Cerdd(s)

    print('--------------------')
    print(c)
    print('--------------------')
    print(repr(c))
    print('--------------------')
    # print(str(c).replace('\n', '*'))
    # print('--------------------')
    # for pennill in c.children:
    #     print(pennill.nifer_llinellau(), str(pennill).replace('\n', '*'))
    # print('SAIN ---------------')
    # print(c.sain())
    print('IPA ----------------')
    print(c.ipa())
    print('--------------------')


if __name__ == "__main__":
    main()
