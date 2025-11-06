# odl.py
'''
Gwrthrych `Odlau` sef rhestr o sillafau.

Gall berthyn i wrthrychau o'r math:
    `Cynghanedd`, `Cwpled`, `Mesur`
'''

from ceibwr.sillaf import Odl


class Odlau():
    '''
    Rhestr o wrthrychau `Odl`, sef ail ran sillaf (h.y. "Rime")
    Gall hyn berthyn i wrthrychau:
     (1) `Cynghanedd`: odl fewnol,
     (2) `Cwpled`: odl / odl gyrch.
     (3) `Mesur`: prifodl

    '''
    def __init__(self, odlau=None):

        self._odlau = []  # inner
        self.dosbarth = None
        self.hysbys = []

        if odlau:
            if not all([type(x) is Odl for x in odlau]):
                raise TypeError('Mae angen `list[Odl]` fan hyn.')
            self._odlau = odlau

    def __str__(self):
        return str(self._odlau)

    def __len__(self):
        return len(self._odlau)

    def __add__(self, other):
        if isinstance(other, Odlau):
            odlau = self._odlau + other._odlau
            odlau = list(set(odlau))  # remove duplicates
            od = Odlau(odlau=odlau)
            return od

    def __bool__(self):
        if len(self._odlau) > 0:
            return True
        return False

    def __setitem__(self, idx, odl):
        if not isinstance(odl, Odl):
            raise ValueError('Mae angen `Odl` fan hyn.')
        self._odlau[idx] = odl

    def __getitem__(self, idx):
        return self._odlau[idx]

    def append(self, item):
        if not isinstance(item, Odl):
            raise TypeError("Mae angen `Odl` fan hyn.")
        self._odlau.append(item)

    def extend(self, items):
        if not all([isinstance(item, Odl) for item in items]):
            raise TypeError("Mae angen rhestr o wrthrychau `Odl` fan hyn.")
        self._odlau.extend(items)


# ------------------------------------------------
# test
def main():
    odlau = Odlau()
    odlau.extend([Odl('ai', 'd'), Odl('ai', 'd'), Odl('ai', 'd')])
    odlau.dosbarth = 'ODL'
    print(odlau)

    odlau2 = Odlau()
    odlau2.extend([Odl('e', 'g'), Odl('e', 'g')])
    odlau2.dosbarth = 'ODL'
    print(odlau2)

    odlau._odlau.extend(odlau2._odlau)
    print(odlau)

    tmp = odlau + odlau2
    print('tmp:', tmp)
    print('type:', type(tmp))
    print('parts:', tmp._odlau)


if __name__ == "__main__":
    main()