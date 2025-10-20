# gair.py
"""
Diffiniad  `Gair`.

Mae `Gair` yn is-ddosbarth unionyrchol i `TreeNode`
"""

import os
import re

from ceibwr.base import TreeNode
from ceibwr.nod import Cytsain, Llafariad
from ceibwr.nod import Bwlch, EOL
from ceibwr.sillaf import Sillaf
from ceibwr.cysonion import (
    llafariaid,
    llafariaid_hirion,
    hir2byr,
    cytseiniaid,
    atalnodau,
    deuseiniaid,
    eithriadau,
    ipa_prifacen,
    ipa_isacen,
)

import logging
log = logging.getLogger(__name__)


class Gair(TreeNode):
    """
    Dosbarth sy'n mynegi gair mewn rhestr o sillafau.

    Input: str

    Os mai bwlch/bylchau (inc. eol) yw'r nod olaf, caiff rhain
    eu recordio yn yr attribute `terfyn`.
    """

    def __init__(self, s, parent=None):
        '''Constructor method
        '''
        TreeNode.__init__(self, parent=parent)

        # type check
        if not type(s) is str:
            raise TypeError("Mae angen `str` fan hyn.")

        # value check
        if not s:
            raise TypeError("Mae angen `str` anwag fan hyn.")

        # cofnodi whitespace diweddol (yn cynnwys EOL)
        self.terfyn = []
        while s[-1].isspace():
            if s[-1] in os.linesep:
                self.terfyn.append(EOL())
            else:
                self.terfyn.append(Bwlch())
            s = s[:-1]

        # gwrthod bylchau yn y canol
        if re.search(r"\s", s):
            raise ValueError("Mae bwlch fan hyn: {}".format(s))

        # creu allwedd am lookups yn y rhestri eithriadau
        s_key = ''.join([x for x in s if x not in atalnodau]).lower()

        # trawsnewid str i restr sillafau
        idx = 0
        idx_sillaf = 0

        while idx < len(s):
            cyrch = ""
            while idx < len(s) and not s[idx] in llafariaid:
                cyrch = cyrch + s[idx]
                idx = idx + 1

            cnew = ""
            while idx < len(s) and not s[idx] in cytseiniaid:
                cnew = cnew + s[idx]
                idx = idx + 1

            coda = ""
            while idx < len(s) and not s[idx] in llafariaid:
                coda = coda + s[idx]
                idx = idx + 1

            # print(cyrch, cnew, coda)

            idx_sillaf += 1

            # echdynnu'r cwlwm llafariaid
            # TODO: delio gyda atalnodau unigol, espec. '-'
            
            key = cnew.lower()
            key = ''.join([c if c in llafariaid else '' for c in key])

            # Gwirio am ddeuseiniaid deusill (hiatus)
            # Mae angen gwneud hyn cyn fflatio ar gyfer lookups
            # e.e. dŵad, pŵer
            # Hefyd mae angen gwirio'r rhestri eithriadau
            # Noder: cnewyllyn "di-os" yw "i-o" ond yr allwedd yw "io"
            # h.y. gall len(cnewyllyn) fod yn fwy na dau
            # dyna pam mai cnew[1:] yn hytrach na cnew[1] sydd
            # yn yr ail sillaf
            if len(key) == 2 and (
                key in deuseiniaid["hiatus"] or
                s in eithriadau["hiatus"] or (
                    # priod, piod, diod, dianc, diadell, gwnio
                    cyrch.lower() in ["d", "p", "pr", "tr", "gwn"] and
                    key in ["io", "ia"]
                )
            ):
                self.children.append(Sillaf(cyrch, cnew[0], "", parent=self))
                self.children.append(Sillaf("", cnew[1:], coda, parent=self))
                continue

            elif len(key) == 3:
                xy = key[:2]
                yz = key[1:]
                
                if (
                    s_key in eithriadau['triawdau_deusill_x|yz'] or
                    xy in deuseiniaid["hiatus"]
                ):
                    self.children.append(Sillaf(cyrch, cnew[0], "", parent=self))
                    self.children.append(Sillaf("", cnew[1:], coda, parent=self))
                    continue

                elif (
                    s_key in eithriadau['triawdau_deusill_xy|z'] or
                    yz in deuseiniaid["hiatus"]
                ):
                    # print('XY|Z:', s)
                    self.children.append(Sillaf(cyrch, cnew[:2], "", parent=self))
                    self.children.append(Sillaf("", cnew[2], coda, parent=self))
                    continue

            # fflatio'r allwedd cyn hollti cnewyll trisain (er mwyn lookups)
            key = ''.join([hir2byr[char] if char in hir2byr else char for char in key])

            # creu deuseiniaid (hiatus wedi ei brosesu yn barod)
            if len(key) == 2:

                # deuseiniaid
                # TODO: creu gwrthrych `Deusain` fan hyn
                self.children.append(Sillaf(cyrch, cnew, coda, parent=self))
            
            elif len(key) == 3:
                # 1. hollti LL+T a LL+LL bob amser: xyz -> xy|z
                # mae'r acenion bob amser ar y cyntaf a'r olaf
                # gan bod y ddeuawd gyntaf yn lleddf ac felly 
                # mae'r llafariad ganol yn wan.
                #
                # awel (LL+T)     .aw.|.e.l
                # hoyw (LL+LL)    h.oy.|.w.
                # gloyw (LL+LL)     gl.oy.|.w.
                # deuwn (LL+LL)     d.eu.|.w.n
                # dywed (LL+T)      d.yw.|.e.d
                #
                # 2. hollti T+T os oes 'w' yn y canol
                # piwis (T+T)       p.iw.|.i.s
                #
                # Fel arall, creu un sillaf drisain .a.n|.i.f|.ei.l|.iai.d
                
                xy = key[:2]
                yz = key[1:]

                # TODO: ae angen creu gwrthrychau `Deusain` fan hyn
                # print('xy, yz:', (xy, yz))
                if (
                    yz in deuseiniaid["hiatus"] or
                    xy in deuseiniaid['lleddf'] or (
                        xy in deuseiniaid["talgron"] and
                        yz in deuseiniaid["talgron"] and
                        key[1] == "w" and
                        idx_sillaf == 1
                    )
                ):
                    # print(xy, yz)
                    self.children.append(Sillaf(cyrch, cnew[:2], "", parent=self))
                    self.children.append(Sillaf("", cnew[2], coda, parent=self))

                else:
                    # trisain - tair `Llafariad``, neu gwrthrych `Trisain`?
                    # does dim angen `Pedwarsain` gan eu bod yn hollti bob tro!
                    self.children.append(Sillaf(cyrch, cnew, coda, parent=self))

            elif len(key) == 4:
                # hollti bob tro: wxyz -> wx|yz
                # ieuanc (T+T)   .ie.|.ua.nc
                # rywiog (T+T)   r.yw.|.io.g
                self.children.append(Sillaf(cyrch, cnew[:2], "", parent=self))
                self.children.append(Sillaf("", cnew[2:], coda, parent=self))

            elif len(key) == 5:
                # hollti: vwxyz -> vw|xyz
                # lliwiau -> ll.iw.|.iau.
                # duwiau -> d.uw.|.iau.
                # gwywai -> g.wy.|.wai.
                # gwywion -> g.wiw.|.io.n dim g.wi.|.wio.n ?
                self.children.append(Sillaf(cyrch, cnew[:2], "", parent=self))
                self.children.append(Sillaf("", cnew[2:], coda, parent=self))

            elif len(key) == 6:
                # hollti: uvwxyz -> uvw|xyz
                # wiwiau -> .wiw.|.iau.
                self.children.append(Sillaf(cyrch, cnew[:3], "", parent=self))
                self.children.append(Sillaf("", cnew[3:], coda, parent=self))

            else:
                self.children.append(Sillaf(cyrch, cnew, coda, parent=self))

        # end while

    def terfyniad(self, bwlch=' ', eol=os.linesep):
        terfyniad = ''
        for nod in self.terfyn:
            if type(nod) is Bwlch:
                terfyniad += bwlch
            if type(nod) is EOL:
                terfyniad += eol
        return terfyniad

    def __str__(self):
        return "".join([str(sillaf) for sillaf in self.children])

    def __repr__(self):
        return "|".join([repr(sillaf) for sillaf in self.children])

    def sain(self):
        return "".join([sillaf.sain() for sillaf in self.children])

    def ipa(self, isacenion=True, cledrau=False):
        nodau_ipa = []
        for sillaf in self.children:
            if sillaf == self.prif_sillaf():
                nodau_ipa.append(ipa_prifacen)
            elif isacenion and sillaf.cnewyllyn():
                nodau_ipa.append(ipa_isacen)
            nodau_ipa += sillaf.ipa()
        if cledrau:
            nodau_ipa = '/' + ' '.join(nodau_ipa) + '/'
        
        return ''.join(nodau_ipa)

    def nodau(self):
        return [nod for sillaf in self.children for nod in sillaf.nodau()]

    def sillafau(self):
        return self.children

    def llafariaid(self):
        return [nod for nod in self.nodau() if nod.is_llafariad()]

    def cytseiniaid(self):
        return [nod for nod in self.nodau() if nod.is_cytsain()]

    def nifer_sillafau(self):
        return len([sillaf
                    for sillaf in self.children
                    if sillaf and sillaf.cnewyllyn()
                    ])

    def is_acennog(self):

        # Geiriau unsill
        if self.nifer_sillafau() == 1:
            return True

        # Gwirio am lafariad hir echblyg ar ddiwedd cnewyllyn y sill olaf
        if self.children and self.children[-1]:
            cn = self.children[-1].cnewyllyn()
            if cn.children and str(cn.children[-1]) in llafariaid_hirion:
                return True

        # Gwirio am h neu rh o flaen y llafariaid olaf
        # e.e. dyfalbarhau ...
        if self.children and len(self.children) > 1:
            if str(self.children[-2].coda()) in ["h", "rh"]:
                return True

        # Gwirio'r rhestr eithriadau
        s = "".join(
            [nod.text.lower() for nod in self.nodau() if nod.text not in atalnodau]
        )
        if s.lower() in eithriadau["geiriau_lluosill_acennog"]:
            return True

        # default: mae geiriau lluosill yn ddiacen fel arfer
        return False

    def prif_lafariaid(self):
        return tuple([sillaf.prif_lafariad() for sillaf in self.children])

    def prif_sillaf(self):
        if self.nifer_sillafau() > 0:
            if self.is_acennog():
                return self.children[-1]
            return self.children[-2]
        return None

    # show (mostly superseeded)
    def show_text(self, bwlch=' ', eol=os.linesep, terfyniad=True):
        if terfyniad:
            return str(self) + self.terfyniad(bwlch, eol)
        return str(self)

    def show_acenion(self, colon=False, bwlch=" ", eol=None):
        ss = list()
        for sillaf in self.children:
            for nod in sillaf.nodau():
                if nod in self.prif_lafariaid():
                    if sillaf is self.prif_sillaf():
                        ss.append("/" if not colon else ":")
                    else:
                        ss.append("v" if not colon else ":")
                else:
                    ss.append(bwlch * len(nod.text))

        return ''.join(ss) + self.terfyniad(bwlch, eol)

    def show_llafariaid(self, bwlch=" ", eol=None):
        ss = []
        for sillaf in self.children:
            for nod in sillaf.nodau():
                if type(nod) is Llafariad:
                    ss.append(nod.text)
                else:
                    ss.append(bwlch * len(nod.text))

        return ''.join(ss) + self.terfyniad(bwlch, eol)

    def show_cytseiniaid(self, bwlch=" ", eol=None):
        ss = []
        for sillaf in self.children:
            for nod in sillaf.nodau():
                if type(nod) is Cytsain:
                    ss.append(nod.text)
                else:
                    ss.append(bwlch * len(nod.text))

        return ''.join(ss) + self.terfyniad(bwlch, eol)


# ------------------------------------------------
# test
def main():

    from ceibwr.profion_gair import profion

    profion['anodd'] = (
        "Gwnïo",
        "dŵad",
        "pïau",
        "achosion",
        "on",  # sef odl `afon`
        "chwiorydd",
        "di-os",
    )

    # for key in profion:
    for key in [
        'cyffredin',
        'deuseiniaid',
        'deuawd ddeusill',
        'triawd ddeusill',
        'lluosill acennog',
        'w-gytsain',
        'gwr, gwl',
        'triawd talgron-talgron (T-T)',
        'triawd talgron-lleddf (T-LL)',
        'triawd lleddf-talgron (LL-T)',
        'triawd lleddf-lleddf (LL-LL)',
        'pedwarawd',
        'trychben',
        'hollti-ia',
        'y-olau',
        'wy-bondigrybwyll',
        'anodd',
    ]:
        # call(["clear"])
        print("==============================")
        print(key.upper())
        print("==============================")
        for s in profion[key]:
            x = Gair(s)
            print(x.show_acenion())
            print(x)
            print(x.sain())
            print(repr(x))
            print(x.ipa())
            print("Nifer sillafau: {}".format(x.nifer_sillafau()))
            print(x[-1].odl().sain())
            print('--------------------')


if __name__ == "__main__":
    main()
