# celfi.py
'''
Ymdrech i uniaethu dulliau darganfod clecs ac odlau.

Mae hyn yn "work in progress". Mae angen defnyddio
`prawf_cytseinedd` a `prawf_odl` yn lle regexp er 
mwyn cael aceniad geiriau yn iawn.

Base'n dda creu database ar gyfer y cleciadur, er mwyn
osgoi gorfod cyfrifo "from scratch" a'r lleihau yr amser
mae hynny yn cymryd. Ond bydd yn anodd cynnwys pob
ymholiad posib, h.y. pan fydd angen chwilio am "fragments".
'''
import os
import re
import json

from ceibwr.settings import GEIRIADURON

from ceibwr.cysonion import (
    eithriadau,
)

from ceibwr.gair import Gair
from ceibwr. datryswr_cytseinedd import prawf_cytseinedd
from ceibwr.datryswr_odl import prawf_odl_sylfaenol


geirfa = GEIRIADURON['default']['GEIRFA']       # txt
# odliadur = GEIRIADURON['default']['ODLIADUR']   # json

geiriau_lluosill_acennog = eithriadau['geiriau_lluosill_acennog']


class Geirfa():
    def __init__(self, s):

        # type check
        if type(s) is str:
            s = s.split(os.linesep)
        elif not type(s) is list and all([type(x) is str for x in s]):
            raise TypeError("Mae angen `str` neu `list[str]` fan hyn.")

        self.geiriau = [Gair(x) for x in s if len(x) > 0 and not x.isspace()]

    def __repr__(self):
        return '\n'.join([repr(x) for x in self.geiriau])


class Odliadur():

    def __init__(self):
        self.odlau = {}
        self.odlau_llusg = {}

    def create(self, geirfa):

        # type check
        if type(geirfa) is not Geirfa:
            raise TypeError("Mae angen `Geirfa` fan hyn.")

        # Mae angen dau wrthrych `Sillaf` ar prawf_odl_sylfaenol
        # Erbyn hyn (cf Geirfa) dylai'r geiriau wedi cael eu 
        # hacennu'n gywir ac mae'r sillaf olaf ydy hynny go iawn
        # Felly does dim drwg yn creu `Sillaf` newydd o'r `odl_str`
        # cyfredol a'i fwydo i `prawf_odl_sylfaenol`.
        # TODO: check seinyddiaeth

        keys = list(set([str(x.children[-1].odl()) for x in geirfa.geiriau]))

        # hac i droi -os -> os (di-os -> d.i.|.-o.s)
        keys = [''.join(x for x in key if x.isalnum()) for key in keys]

        keys.sort()
        print('\n'.join(keys))

        self.odlau = {}
        self.odlau_llusg = {}
        for odl_str in keys:

            # init (creu `Gair` er mwyn cael yr aceniad yn gywir)
            print('odl_str:', odl_str)
            x = Gair(odl_str)
            if not x.children:
                continue
            qsillaf = x.children[-1]

            odlau = []
            odlau_llusg = []

            # chwilio
            for gair in geirfa.geiriau:

                sillaf_olaf = gair.children[-1]
                od = prawf_odl_sylfaenol(qsillaf, sillaf_olaf)
                if od and od.dosbarth in ['ODL', 'OLA']:
                    odlau.append(str(gair))

                if gair.nifer_sillafau() > 1 and not gair.is_acennog():
                    goben = gair.children[-2]
                    od = prawf_odl_sylfaenol(qsillaf, goben)
                    if od and od.dosbarth in ['ODL', 'OLA']:
                        odlau_llusg.append(str(gair))

            if odlau:
                self.odlau[odl_str] = odlau
            if odlau_llusg:
                self.odlau_llusg[odl_str] = odlau_llusg

    def search(self, qstr, acennog=False, llusg=False):

        if llusg and qstr in self.odlau_llusg:
            odlog = self.odlau_llusg[qstr]

        elif qstr in self.odlau:
            odlog = self.odlau[qstr]
        else:
            return None

        if acennog:
            return [s for s in odlog if Gair(s).is_acennog()]
        return odlog

    def read(self, fname, llusg=False):
        with open(fname, 'r') as f:
            if llusg:
                self.odlau_llusg = json.load(f)
            else:
                self.odlau = json.load(f)

    def write(self, fname, llusg=False):
        odlau = self.odlau_llusg if llusg else self.odlau
        s = json.dumps(odlau, indent=4, ensure_ascii=False)
        with open(fname, 'w') as f:
            f.write(s)


class Cleciadur():

    def __init__(self):

        self.clecs = {}

    def create(self, geirfa):
        """
        Sut mae osgoi double loop? 
        Oes modd llunio patrymau regex?
        """

        # type check
        if type(geirfa) is not Geirfa:
            raise TypeError("Mae angen `Geirfa` fan hyn.")

        # loop
        self.clecs = {}
        for idx, x in enumerate(geirfa.geiriau):  # ugh!

            print(f'{idx}:', x)
            cofnod = self.compute_clecs(geirfa, x)
            print('cofnod:', cofnod)
            print()

            self.clecs[str(x)] = cofnod

    def compute_clecs(self, geirfa, x):

        # type checks
        if type(geirfa) is not Geirfa:
            raise TypeError("Mae angen `Geirfa` fan hyn.")
        if type(x) is not Gair:
            raise TypeError("Mae angen `Gair` fan hyn.")

        cofnod = {
            'CAC': [],
            'CDI': [],
            'AAC': [],
            'ADI': [],
        }

        for y in geirfa.geiriau:
            # print('    y:', y)

            # reject llafariaid tebyg dan yr acen
            if x.prif_sillaf().cnewyllyn().sain() == y.prif_sillaf().cnewyllyn().sain():
                continue

            # TODO: mwy o checks fan hyn?

            # x ar yr orffwysfa
            cyts = prawf_cytseinedd(x, y)
            if cyts.dosbarth and cyts.dosbarth == 'CRO':
                if x.is_acennog() and y.is_acennog():
                    cofnod['CAC'].append(str(y))
                elif x.is_acennog() and not y.is_acennog():
                    cofnod['ADI'].append(str(y))
                elif not x.is_acennog() and y.is_acennog():
                    cofnod['AAC'].append(str(y))
                else:
                    cofnod['CDI'].append(str(y))

            # x ar y diwedd
            cyts2 = prawf_cytseinedd(y, x)
            if cyts2.dosbarth and cyts2.dosbarth == 'CRO':
                if x.is_acennog() and not y.is_acennog():
                    cofnod['AAC'].append(str(y))
                elif not x.is_acennog() and y.is_acennog():
                    cofnod['ADI'].append(str(y))

        # cofnodi
        return cofnod

    def query(self, qstr, geirfa=None):
        qstr = qstr.lower()

        if qstr in self.clecs:
            return self.clecs[qstr]

        elif geirfa and type(geirfa) is Geirfa:
            return self.compute_clecs(Gair(qstr))

        return None

    def write(self, fname):
        s = json.dumps(self.clecs, indent=4, ensure_ascii=False)
        print(s)
        with open(fname, 'w') as f:
            f.write(s)


def main():

    # filenames
    # geirfa_fname = "/Users/scmde/ceibwr/src/ceibwr/data/miniJGJ.txt"
    geirfa_fname = "/Users/scmde/ceibwr/src/ceibwr/data/geirfaJGJ.txt"
    odliadur_fname = "/Users/scmde/ceibwr/src/ceibwr/data/odliadurCC.json"
    llusgiadur_fname = "/Users/scmde/ceibwr/src/ceibwr/data/llusgiadurCC.json"
    cleciadur_fname  = "/Users/scmde/ceibwr/src/ceibwr/data/cleciadurCC.json"

    # --------------
    # Test Geirfa

    with open(geirfa_fname) as f:
        s = f.read()
    geirfa = Geirfa(s)
    print(repr(geirfa))

    # return

    # --------------
    # Test Odliadur

    # creu odliadur (araf)
    # od = Odliadur()
    # od.create(geirfa)

    # write odliadur (json)
    # od.write(odliadur_fname)
    # od.write(llusgiadur_fname, llusg=True)

    # # read odliadur (json)
    # od = Odliadur()
    # od.read(odliadur_fname)
    # od.read(llusgiadur_fname, llusg=True)

    # # test
    # print(od.search('ydd'))
    # print()
    # print(od.search('ydd', llusg=True))
    # print()
    # print(od.search('ydd', acennog=True))

    # --------------
    # Test cleciadur

    # creu cleciadur (araf)
    cc = Cleciadur()
    cc.create(geirfa)

    cc.write(cleciadur_fname)

    for key in cc.clecs.keys():
        print(key)

    if 'cariad' in cc.clecs:
        res = cc.query('cariad')
        print(res)
    else:
        print('dim byd')

    print(cc.clecs.keys())
    # print(cc.clecs['cariad'])

    # write cleciadur (json)
    # cc.write(clecs_fname)

    return


if __name__ == '__main__':
    main()
