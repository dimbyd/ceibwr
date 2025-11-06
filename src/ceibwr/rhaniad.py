# rhaniad.py
'''
`Rhaniad`: rhestr corfannau neu raniadau eraill

Mae `Rhaniad` yn is-ddosbarth uniongyrchol o `TreeNode`

Text: Gair -> Llinell -> Pennill
Sain: Nod -> Sillaf -> Gair -> Corfan -> Rhaniad

`Rhaniad` yw uwch-ddosbarth `Datrysiad`

`Datrysiad` yw base class
    `Cynghanedd`    # Lefel 1
    `Cwpled`        # Lefel 2
    `Mesur`         # Lefel 3
    `Awdl`          # Lefel 4
 
'''
import os

from ceibwr.base import TreeNode
from ceibwr.corfan import Corfan


class Rhaniad(TreeNode):
    '''
    Abstract class ar gyfer:
        `Cynghanedd`: CRO, TRA, LLU, SAI, ...
        `Cwpled`: CC7, TOB, ...
        `Mesur`: CYW, ENG, ...

    CRO/TRA/LLU: dau gorfan [c1, c2]
    SAI:         tri chorfan [c1, c2, c3]

    '''
    def __init__(self, rhaniad, parent=None):
        TreeNode.__init__(self, parent=parent)

        # type check
        if isinstance(rhaniad, Rhaniad):
            rhaniad = rhaniad.children

        if (
            type(rhaniad) is not list or
            not all([isinstance(elfen, (Corfan, Rhaniad)) for elfen in rhaniad])
        ):
            raise TypeError("Mae angen rhestr o wrthrychau `Corfan` neu `Rhaniad` fan hyn, nid {}.".format([type(rhan) for rhan in rhaniad]))

        self.children = rhaniad
        for child in self.children:
            child.parent = self

    def __str__(self):
        return ''.join([str(elfen) for elfen in self.children])

    def __repr__(self):
        return repr(self.children)

    # sain
    def sain(self):
        return " ".join([child.sain() for child in self.children])

    def ipa(self):
        return " ".join([child.ipa() for child in self.children])

    # properties
    def lefel(self):
        if all([type(child) is Corfan for child in self.children]):
            return 1
        else:
            lefel_max = max([child.lefel() for child in self.children])
            return lefel_max + 1

    def nifer_rhaniadau(self):
        return len(self.children)

    def nifer_sillafau(self):
        return sum([child.nifer_sillafau() for child in self.children])

    def nifer_geiriau(self):
        return sum([child.nifer_geiriau() for child in self.children])

    # access functions
    def nodau(self, terfyniadau=True):
        nodau = []
        for child in self.children:
            nodau.extend(child.nodau(terfyniadau=terfyniadau))
        return nodau

    def sillafau(self):
        sillafau = []
        for child in self.children:
            sillafau.extend(child.sillafau())
        return sillafau

    def geiriau(self):
        geiriau = []
        for child in self.children:
            geiriau.extend(child.geiriau())
        return geiriau

    def is_acennog(self):
        return self.children[-1].is_acennog()                

    def gair_olaf(self):
        return self.children[-1].gair_olaf()

    def sillaf_olaf(self):
        return self.children[-1].sillaf_olaf()

    # show
    def show_text(self, toriad='', bwlch=' ', eol=os.linesep):
        if self.lefel() == 1:
            return ''.join([corfan.show_text(toriad=toriad, bwlch=bwlch, eol=eol) for corfan in self.children])
        return ''.join([rhan.show_text(toriad=toriad, bwlch=bwlch, eol=eol) for rhan in self.children])

    def show_acenion(self, toriad='', bwlch=' ', eol=os.linesep):
        if self.lefel() == 1:
            return ''.join([corfan.show_acenion(toriad=toriad, bwlch=bwlch, eol=eol) for corfan in self.children])
        return ''.join([rhan.show_acenion(toriad=toriad, bwlch=bwlch, eol=eol) for rhan in self.children])

    def show_fancy(self, toriad=''):
        acenion = self.show_acenion(toriad=toriad, eol='*').split('*')
        rhannau = self.show_text(toriad=toriad, eol='*').split('*')
        return [x for y in zip(acenion, rhannau) for x in y]


class Trychwr():
    '''
    Creu rhaniadau allan o restr elfennau.

    Mae hwn wedi ei seilio ar yr algorithm y "stars and bars"
    '''
    def __init__(self):
        pass

    def rhaniadau(self, elfennau, min_rhannau=2, max_rhannau=5):
        '''
        Creu pob rhaniad posib.
        '''

        # type check
        if type(elfennau) is not list:
            raise TypeError("Mae angen rhestr o elfennau fan hyn.")

        rhestr_rhaniadau = []
        for nifer in range(min_rhannau, max_rhannau+1):
            for ymraniad in self.ymrannu(elfennau, nbars=nifer-1):
                rhaniad = Rhaniad([Corfan(rhan) for rhan in ymraniad])
                rhestr_rhaniadau.append(rhaniad)
        return rhestr_rhaniadau 

    def partitions(self, items, minparts=2, maxparts=None):

        # type check
        if type(items) is not list:
            raise TypeError("Mae angen rhestr o elfennau fan hyn.")
        
        if not maxparts:
            maxparts = len(items)

        partitions = []
        for numparts in range(minparts, maxparts+1):
            for partition in self.ymrannu(items, nbars=numparts-1):
                partitions.append(partition)
        return partitions

    def ymrannu(self, seq, nbars, min_size=1):
        # stars and bars
        if nbars == 0:
            yield [seq]
        else:
            for i in range(min_size, len(seq) - min_size * nbars + 1):
                for res in self.ymrannu(seq[i:], nbars-1, min_size):
                    yield [seq[:i]] + res


# ------------------------------------------------
# test
def main():
    tr = Trychwr()
    items = ['a', 'b', 'c', 'd', 'e']
    partitions = tr.partitions(items)
    print(partitions)
    print()
    partitions = tr.partitions(items, maxparts=3)
    print(partitions)


if __name__ == "__main__":
    main()
