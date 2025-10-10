# nod.py
"""
Unedau orgraffyddol/seiniol sylfaenol (basic orthographic/phonic units).

Mae'r modiwl hwn yn diffinio unedau sylfaenol sydd yn cyfuno elfennau
orgraffyddol a seinyddol.

Caiff yr unedau eu dosbarthu fel a ganlyn:
- Llafariaid
- Cytseiniaid (yn cynnwys deugraffau)
- Deuseiniaid
- Atalnodau
- Bylchau

Mae gan bob gwrthrych `Nod` y priodweddau canlynol.
- text (orgraffyddol): ffurf safonol (llythrennau, atalnodau, bylchau)
- sain (seinyddol):    ffurf ffonetig (llythrennau neu `None`)
- ipa (seinyddol):     ffurf ffonetig (symbolau IPA neu `None`)

phoneme:
    - minimal distinctive unit of sound
grapheme:
    - smallest unit of a writing system that corresponds with a phoneme
    - similar to 'character' in computing
    - e.e. 'mh', 'nh', ngh' (voicless nasals)

Graffemau ansafonol:
--------------------
    1. 'mh', 'nh', 'ngh',
        - mhen, nhad, nghwmni
        - voiceless nasals /m̥ n̥ ŋ̊/
    2. 'si', 'sh'
        - siop, shop
        - postalveolar fricative /ʃ/
    3. 'tsi', 'tsh'
        - tsips, tships
        - postalveolar affricate /tʃ/
"""
from ceibwr.base import TreeNode

from ceibwr.cysonion import (
    llafariaid,
    llafariaid_byrion,
    cytseiniaid,
    atalnodau,
    hir2byr,
    ipa_lookup,
)

import logging
log = logging.getLogger(__name__)


class Nod(TreeNode):
    """
    Class `Nod`. Uned orgraffyddol/seinyddol sylfaenol.

    Dosbarth haniaethol i ddarlunio
    llafariaid, cytseiniaid, deuseiniaid, a bylchau unigol.

    Lefel 0:
    parent: `Cyfres`
    children: `None`
    """

    def __init__(self, s=None, parent=None):
        TreeNode.__init__(self, parent=parent)
        self.text = s
        self.sain = self.text

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.__str__()

    def ipa(self):
        if self.sain.lower() in ipa_lookup:
            return ipa_lookup[self.sain.lower()]
        return ''

    # Hafaledd: er mwyn gallu defnyddio `nod1 == nod2`
    def __eq__(self, other):
        return isinstance(other, Nod) and self is other

    def __hash__(self):
        return id(self)

    def xml(self):
        element = super().xml()
        element.text = self.text
        return element

    def is_bwlch(self):
        return self.text.isspace()

    def is_atalnod(self):
        return self.text in atalnodau

    def is_llafariad(self):
        return self.text in llafariaid

    def is_cytsain(self):
        return self.text in cytseiniaid

    def sain_fer(self):
        if self.sain in hir2byr:
            return hir2byr[self.sain]
        return self.sain

    def is_fer(self):
        if self.sain in llafariaid_byrion:
            return True
        return False

    def is_deusain(self):
        return type(self) is Deusain


# is-dosbarthiadau
class Cytsain(Nod):
    def __init__(self, s="", parent=None):
        Nod.__init__(self, s, parent=parent)


class Llafariad(Nod):
    def __init__(self, s="", parent=None):
        Nod.__init__(self, s, parent=parent)


class Atalnod(Nod):
    def __init__(self, s="", parent=None):
        Nod.__init__(self, s, parent=parent)


class Bwlch(Nod):
    def __init__(self, s=" ", parent=None):
        Nod.__init__(self, s, parent=parent)


class EOL(Nod):
    def __init__(self, s="\n", parent=None):
        Nod.__init__(self, s, parent=parent)


class Deusain(Nod):
    def __init__(self, s="", parent=None):
        Nod.__init__(self, s, parent=parent)

        if type(s) is not str or len(s) != 2 or (
            s[0] not in llafariaid or s[1] not in llafariaid
        ):
            raise ValueError("Mae angen `str` dwy lafariad yn union fan hyn.")


# ------------------------------------------------
# test
def main():

    from lxml import etree
    nod = Nod("ch")
    xml_str = etree.tostring(nod.xml(), pretty_print=True).decode("utf-8")
    print(xml_str)

    cyts = Cytsain('ng')
    xml_str = etree.tostring(cyts.xml(), pretty_print=True).decode("utf-8")
    print(xml_str)

    ds = Deusain('au')
    xml_str = etree.tostring(ds.xml(), pretty_print=True).decode("utf-8")
    print(xml_str)
    print(ds.ipa())


if __name__ == "__main__":
    main()
