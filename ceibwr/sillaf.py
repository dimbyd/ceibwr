# sillaf.py
"""
Diffiniad `Sillaf`

Mae tair rhan i bob sillaf: 
    * cyrch (onset), 
    * cnewyllyn (nucleus),
    * coda.

Sillaf = [cyrch, cnewyllyn, coda]
cyrch       `Cyfres` cytseiniaid
cnewyllyn   `Cyfres` llafariaid/deuseiniaid
cyrch       `Cyfres` cytseiniaid

Sillaf agored (open syllable): dim coda (e.e. pla, glo)
Sillaf gaeëdig (closed syllable): coda anwag (e.e. bwyd, siop)
"""

from ceibwr.base import TreeNode

from ceibwr.nod import Nod
from ceibwr.nod import Cytsain, Llafariad, Atalnod
from ceibwr.cysonion import (
    cytseiniaid,
    llafariaid,
    atalnodau,
    llafariaid_hirion,
    deuseiniaid,
    dosbarth_deusain,
    ipa_prifacen,
    hir2byr,
)

import logging
log = logging.getLogger(__name__)


class Cyfres(TreeNode):
    """
    Class `Cyfres`. Cyfres o wrthrychau `Nod`.

    Dosbarth haniaethol ar gyfer rhannau sillaf (cyrch, cnewyllyn, coda)
    Lefel 1:
    parent: `Sillaf`
    children: `list[Nod]`
    """

    def __init__(self, s="", parent=None):
        """
        Creu cyfres o nodau allan o `str` neu `list[Nod]`.

        Mae angen i'r mewnbwn gynnwys naill ai lafariaid yn unig 
        neu gytseiniaid yn unig (ac efallai atalnodau hefyd).
        TODO: Pam? Beth am chomp?
        """
        TreeNode.__init__(self, parent=parent)

        # Gwirio am linyn gwag.
        if not s:
            self.children = []

        # Creu cyfres allan o restr nodau.
        elif (
            type(s) in (list, tuple) and
            all([isinstance(x, Nod) for x in s])
        ):
            self.children = s

        # creu cyfres allan o gyfres arall
        elif type(s) is Cyfres:
            self.children = s.children

        # creu allan o `str`
        elif type(s) is str:
            self.children = []
            idx = 0
            while idx < len(s):

                # echdynnu'r nod nesaf (unicode)
                c = s[idx]

                # cytsain
                if c in cytseiniaid:

                    # cytseiniaid sydd o bosib yn rhan o ddeugraff
                    if (
                        idx < len(s) - 1 and
                        c.lower() in ["c", "d", "f", "l", "m", "n", "p", "r", "s", "t"]
                    ):
                        deugraff = c
                        c_nesaf = s[idx + 1]

                        # ch
                        if c.lower() == "c" and c_nesaf == "h":
                            deugraff = c + "h"
                            idx += 1
                        # dd
                        elif c.lower() == "d" and c_nesaf == "d":
                            deugraff = c + "d"
                            idx += 1
                        # ff
                        elif c.lower() == "f" and c_nesaf == "f":
                            deugraff = c + "f"
                            idx += 1
                        # ng/ngh
                        elif c.lower() == "n" and c_nesaf == "g":
                            if idx < len(s) - 2 and s[idx+2] == "h":
                                deugraff = c + "gh"
                                idx += 2
                            else:
                                deugraff = c + "g"
                                idx += 1
                        # mh
                        elif c.lower() == "m" and c_nesaf == "h":
                            deugraff = c + "h"
                            idx += 1
                        # nh
                        elif c.lower() == "n" and c_nesaf == "h":
                            deugraff = c + "h"
                            idx += 1
                        # ll
                        elif c.lower() == "l" and c_nesaf == "l":
                            deugraff = c + "l"
                            idx += 1
                        # ph
                        elif c.lower() == "p" and c_nesaf == "h":
                            deugraff = c + "h"
                            idx += 1
                        # rh
                        elif c.lower() == "r" and c_nesaf == "h":
                            deugraff = c + "h"
                            idx += 1
                        # th
                        elif c.lower() == "t" and c_nesaf == "h":
                            deugraff = c + "h"
                            idx += 1
                        # tsh
                        elif (
                            c.lower() == "t" and c_nesaf == "s" and
                            idx < len(s) - 2 and s[idx+2] == "h"
                        ):
                            deugraff = c + 'sh'
                            idx += 2
                    
                        # atodi
                        self.children.append(Cytsain(deugraff, parent=self))

                    # cytseiniaid eraill
                    else:
                        self.children.append(Cytsain(c, parent=self))

                # llafariaid
                elif c.lower() in llafariaid:
                    self.children.append(Llafariad(c, parent=self))

                # atalnodau
                elif c.lower() in atalnodau:
                    self.children.append(Atalnod(c, parent=self))

                # other (e.e. rhifolion, greek letters etc.)
                else:
                    self.children.append(Nod(c, parent=self))

                # ymlaen i'r nesaf
                idx += 1
        else:
            raise ValueError(
                "Wedi methu creu gwrthrych `Cyfres` o fewnbwn math {}".format(type(s))
            )
        # set parents
        for nod in self.children:
            nod.parent = self

    # Hafaledd: er mwyn gwirio os oes gan dau gyfres yr un sain
    def __eq__(self, other):
        return (
            isinstance(other, Cyfres)
            and len(self.children) == len(other.children)
            and all([a.sain == b.sain for a, b in zip(self.children, other.children)])
        )

    def __len__(self):
        return len(self.children)

    def __add__(self, other):
        if isinstance(other, Cyfres):
            return Cyfres(self.children + other.children)
        return ()

    def __setitem__(self, idx, nod):
        if not isinstance(nod, Nod):
            raise ValueError('Mae angen `Nod` fan hyn, nid{}'.format(type(nod)))
        nod.parent = self
        self.children[idx] = nod

    def __getitem__(self, idx):
        return self.children[idx]

    def __str__(self):
        return "".join([str(nod) for nod in (self.children)])

    def __repr__(self):
        return "".join([nod.text for nod in self.children])

    def sain(self):
        return ''.join([nod.sain for nod in self.children])

    def sain_fer(self):
        return "".join([nod.sain_fer() for nod in self.children])

    def nodau(self, atalnodau=True):
        if not atalnodau:
            return [nod for nod in self.children if not nod.is_atalnod()]
        return list(self.children)

    def cytseiniaid(self):
        return [nod for nod in self.children if nod.is_cytsain()]

    def pop(self, idx=-1):
        if not self.children:
            return None
        return self.children.pop(idx)

    def insert(self, idx, item):
        if not isinstance(item, Nod):
            return None
        if not self.children:
            return None
        return self.children.insert(idx, item)


class Cyrch(Cyfres):
    def __init__(self, s="", parent=None):
        Cyfres.__init__(self, s, parent=parent)

        # type check (dim llafariaid)
        if any([child.is_llafariad() for child in self.children]):
            raise ValueError("Dim llafariaid fan hyn!")


class Cnewyllyn(Cyfres):
    def __init__(self, s="", parent=None):
        Cyfres.__init__(self, s, parent=parent)

        # type check (dim cytseiniaid)
        if any([child.is_cytsain() for child in self.children]):
            raise ValueError("Dim cytseiniaid fan hyn!")


class Coda(Cyfres):
    def __init__(self, s="", parent=None):
        Cyfres.__init__(self, s, parent=parent)

        # type check (dim llafariaid)
        if any([child.is_llafariad() for child in self.children]):
            raise ValueError("Dim llafariaid fan hyn.")


class Odl(TreeNode):
    def __init__(self, cnew_str="", coda_str="", cyrch_nesaf=None, parent=None):
        TreeNode.__init__(self, parent=parent)

        self.children = [
            Cnewyllyn(cnew_str, parent=self),
            Coda(coda_str, parent=self)
        ]
        self.nodau_cudd = None

    def __str__(self):
        return str(self.cnewyllyn()) + str(self.coda())

    def __repr__(self):
        return str(self.cnewyllyn()) + '.' + str(self.coda())

    def cnewyllyn(self):
        return self.children[0]

    def coda(self):
        return self.children[1]

    def sain(self):
        return ''.join([child.sain() for child in self.children])

    def nodau(self, atalnodau=True, h2b=False):
        a = self.cnewyllyn().nodau(atalnodau=atalnodau)
        if h2b:
            # print('H2B-BEF:', a)
            # print('H2B-XXX:', hir2byr['â'])
            # print('boo:', ('â' in hir2byr))
            a = [hir2byr[nod.text] if nod.text in hir2byr else nod.text for nod in a]
            # print('H2B-AFT:', a)
        b = self.coda().nodau(atalnodau=atalnodau)
        return a + b


class Sillaf(TreeNode):
    """
    Class `Sillaf`. [`Cyrch`, `Odl`]

    parent: `Gair`
    children: `[Cyrch, Odl]`
    """

    def __init__(self, cyrch="", cnewyllyn="", coda="", parent=None):
        TreeNode.__init__(self, parent=parent)

        self.children.append(Cyrch(cyrch, parent=self))
        self.children.append(Odl(cnewyllyn, coda, parent=self))

    def sain(self):
        return "".join([child.sain() for child in self.children])

    def ipa(self, prifacen=False):
        nodau_ipa = []
        if prifacen:
            nodau_ipa.append(ipa_prifacen)
        for nod in self.nodau():
            nodau_ipa.append(nod.ipa())
        return ''.join(nodau_ipa)

    def __str__(self):
        return "".join([
            str(self.cyrch()),
            str(self.cnewyllyn()),
            str(self.coda())
        ])

    def __repr__(self):
        return ".".join([
            str(self.cyrch()),
            str(self.cnewyllyn()),
            str(self.coda())
        ])

    def cyrch(self):
        return self.children[0]

    def odl(self):
        return self.children[1]

    def cnewyllyn(self):
        return self.children[1].children[0]

    def coda(self):
        return self.children[1].children[1]

    def nodau(self):
        return self.cyrch().children + self.cnewyllyn().children + self.coda().children

    def prif_lafariad(self):
        '''
        Canfod y nod sy'n cario'r acen.
        '''

        # anwybyddu atalnodau e.e. a'i, o'u, "nesa'", ayb)
        nodau = self.cnewyllyn().nodau(atalnodau=False)

        # cnewyll unsain
        if len(nodau) == 1:
            return nodau[0]

        # cnewyll ddeusain
        elif len(nodau) == 2:
            ds = nodau[0].sain_fer().lower() + nodau[1].sain_fer().lower()
            # print('ds:', ds)
            if ds in dosbarth_deusain:
                if ds in deuseiniaid["lleddf"]:
                    #   lleddf: acen ar y llarariad cyntaf
                    #   'aw', 'ew', 'ai', 'eu', ...
                    return nodau[0]
                else:
                    #   talgron: acen ar yr ail lafariad
                    #   'ia', 'ie', 'we', 'wi', ...
                    return nodau[1]
            else:
                # raise ValueError("Heb adnabod y ddeusain `{}`".format(ds))
                return nodau[0]

        # cnewyll drisain (acen bob amser ar y llafariad ganol)
        elif len(nodau) == 3:
            return nodau[1]

        # Caiff clymau bedwarsain eu hollti yn `Gair`
        # felly ni ddylem gyrraedd fan hyn ...
        return None

    def is_ysgafn(self):
        """Gwirio os yw'r sillaf yn ysgafn (prif lafariad hir)."""
        if self.prif_lafariad().text.lower() in llafariaid_hirion:
            return True
        return False

    def is_trwm(self):
        """Gwirio os yw'r sillaf yn drwm (prif llafariad fer)."""
        return not self.is_ysgafn()


# ------------------------------------------------
# test
def main():
    profion = (
        # unigol
        ('c', 'a', 'r'),
        ('c', 'i', 'st'),
        ('b', 'a', 'rdd'),
        ('d', 'au', ''),
        ('', 'ia', 'dd'),
        ('', 'ae', 'l'),
        ('', 'yw', ''),
    )

    for cy, cn, co in profion:
        print([cy, cn, co])
        sillaf = Sillaf(cy, cn, co)
        print("-------------------")
        print(sillaf)
        print(repr(sillaf))
        print('prif_lafariad: ', sillaf.prif_lafariad())
        print(sillaf.ipa())
        print(sillaf.ipa(prifacen=True))
        print()
        print(sillaf.xml_str())
        print("-------------------")

    x = Sillaf('d', 'a', 'rt')
    y = Sillaf('d', 'a', 'rt')
    print(x == y)
    print(x.children == y.children)

    x = Cyrch('d')
    y = Cyrch('d')
    print(x == y)


if __name__ == "__main__":
    main()
