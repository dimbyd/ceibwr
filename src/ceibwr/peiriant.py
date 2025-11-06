# peiriant.py
"""
Gwas y Glêr.

Dwy goeden:
    - Text: gair/llinell/pennill
    - Sain: gair/corfan/cynghanedd/mesur

Mae'r ddwy yn uno ar lefel `Gair`.
    Lefel 0: Nod unigol (e.e. cyts/llaf, deus, atalnodau etc.)
    Lefel 1: Sillaf: tri cyfres nodau (cyrch, cnew, coda)
    Lefel 2: Gair: rhestr sillafau
    Lefel 3: Llinell (text) neu Corfan (sain)
    Lefel 4: Pennill (text) neu Rhaniad (sain)
"""

import os
import re
import yaml
import logging
from subprocess import call  # for clrscr

from ceibwr.cysonion import gogwyddeiriau

from ceibwr.nod import EOL
from ceibwr.llinell import Llinell
from ceibwr.pennill import Pennill
from ceibwr.cerdd import Cerdd

from ceibwr.datryswr_llinell import datryswr_llinell
from ceibwr.datryswr_pennill import datryswr_pennill
from ceibwr.datryswr_cerdd import datryswr_cerdd

from ceibwr.datryswr_cwpled import prawf_cwpled

from ceibwr.seinyddwr import Seinyddwr
from ceibwr.beiro import Beiro
from ceibwr.cysonion import colormaps

from ceibwr.odliadur import odl_search
from ceibwr.cleciadur import clec_search

import ceibwr.settings as settings


odlau_file = settings.GEIRIADURON['default']['ODLIADUR']     # json
geirfa_file = settings.GEIRIADURON['default']['GEIRFA']      # txt

cmap_default = colormaps['default']


class Peiriant(object):
    '''
    Gwas y Glêr.
    '''
    def __init__(self, cmap=None):

        # start
        # logging.info("Ganwyd y Peiriant, Gwas y Glêr")

        # tools
        self.seinyddwr = Seinyddwr()
        self.beiro = Beiro()
        if not cmap:
            self.cmap = cmap_default

    def __str__(self):
        return r'\n\n'.join([str(uned) for uned in self.unedau])

    def __repr__(self):
        return r'\n\n'.join([repr(uned) for uned in self.unedau])

    # TODO: check am unicode yn unig (catch UnicodeDecodeError)
    # Ar hyn o bryd mae'n crasho pan yn uwchlwytho PDF i'r gronfa
    def read(self, infile):
        with open(infile) as f:
            return f.read()

    def parse(self, s):
        """Parse YAML header into `dict` then apply `chomp` to remainder.

        If no header, returns (`None`, `Uned`).
        The usual case is a single header at the beginning, 
        so the first part is '', second is the header
        and the third is the text.
        """
        # split yaml headers
        parts = s.split('---')

        # no header
        if len(parts) == 1:
            return (None, self.chomp(s))

        # check pairs
        elif len(parts) % 2 == 0:
            raise ValueError("Mae angen '---' fesul pâr fan hyn.")

        # hack (anwybyddu bloc wag cyn yr '---' cyntaf)
        if not parts[0] or parts[0].isspace():
            parts = parts[1:]

        s = ''
        meta = {}
        for head, body in [(parts[i], parts[i+1]) for i in range(0, len(parts), 2)]:
            head = dict(yaml.safe_load(head))
            for key, value in head.items():
                key, value = str(key).strip(), str(value).strip()
            meta = meta | head
            s += body

        return (meta, self.chomp(s))

    def chomp(self, s):
        """
        Adeiladu rhestr penillion o fewnbwn str (utf-8)
            - <CR> ar ddiwedd llinell (\n)
            - <CR><CR> ar ddiwedd penillion (\n\n)
            - anwybyddu llinellau sy'n dechrau gyda '#'
            - anwybyddu llinellau rhwng '---' a '---' (yaml)

        Return types: `Llinell`, `Pennill` neu `Cerdd`

        Dylai'r yaml headers wedi cael eu stripio cyn hyn!
        TODO: prosesu fesul `char` (stream processing)
        """

        # type check
        if type(s) is not str:
            raise TypeError('Mae angen `str` fan hyn.')

        hysbys = []

        # strip trailing newlines
        s = s.strip()
        
        # strip comments
        ss = []
        for line in s.splitlines():
            if line.startswith('#'):
                hysbys.append(line)
            else:
                ss.append(line)
        s = os.linesep.join(ss)

        # mae hwn yn methu os oes mwy nag un 
        # "blank line" rhwng penillion
        # blociau = s.strip().split(os.linesep + os.linesep)

        # hac
        pattern = r'\n{2,}'
        blociau = re.split(pattern, s.strip())
        s = (os.linesep + os.linesep).join(blociau)
        # print('BLOCIAU:', blociau)
        # print('SNEW:>', s, '<')

        if len(blociau) > 1:
            return Cerdd(s)

        bloc = blociau[0].strip().split(os.linesep)
        if len(bloc) > 1:
            return Pennill(s)

        return Llinell(s)

    def datryswr(self, uned, unigol=True):
        """
        Datrys Llinell, Pennill neu Cerdd.
        """

        # type check
        if type(uned) not in [Llinell, Pennill, Cerdd]:
            raise TypeError("Mae angen `Llinell`, `Pennill` neu `Cerdd` fan hyn.")

        # type
        if type(uned) is Llinell:
            return datryswr_llinell(uned)
        elif type(uned) is Pennill:
            return datryswr_pennill(uned)
        else:
            return datryswr_cerdd(uned)

    def pysgotwr(self, s, min_sillafau=4, max_sillafau=10):
        '''
        Darganfod enghreifftiau cynghanedd mewn testun rydd (free text).
        input:  str
        return: rhestr o ddatrysiadau
        '''
        # Mae problem gyda dyfynod ar ôl atalnod llawn ar ddiwedd paragraff
        # s = s.replace("'.", ".'")
        # s = s.replace('".', '."')

        dats = []
        dim_diolch = ['LLL', 'SAL', 'CWG', 'TWG']

        paragraffau = s.strip().split(os.linesep)
        for parag in paragraffau:

            brawddegau = parag.strip().split('.')
            for brawdd in brawddegau:

                # hack: remove leading non-alphanumeric
                # er mwyn delio â dyfynod ar ôl atalnod llawn.
                while brawdd and not brawdd[0].isalnum():
                    brawdd = brawdd[1:]

                # hack remove empty words (from mutiple consecutive spaces?)
                parts = brawdd.split(' ')
                brawdd = ' '.join([s.strip() for s in parts if s])
                if not brawdd:
                    continue

                # creu `Llinell` er mwyn amgodio terfynnau
                br = Llinell(brawdd)

                # echdynnu rhestr geiriau
                geiriau = br.geiriau()

                idx_chw = 0
                idx_dde = 1

                while idx_chw < len(geiriau) - 1:

                    idx_dde = idx_chw + 1
                    # print('A', idx_chw, idx_dde, geiriau[idx_chw: idx_dde])

                    while (
                        idx_dde < len(geiriau)-1 and
                        sum([g.nifer_sillafau()
                            for g in geiriau[idx_chw: idx_dde]
                             ]) < min_sillafau
                    ):
                        idx_dde = idx_dde + 1

                    while (
                        idx_dde < len(geiriau) and
                        sum([g.nifer_sillafau()
                            for g in geiriau[idx_chw: idx_dde]
                             ]) <= max_sillafau
                    ):
                        # print('B', idx_chw, idx_dde, geiriau[idx_chw: idx_dde])

                        # hepgor gogwyddeiriau ar y brifodl
                        if str(geiriau[idx_dde]).lower() not in gogwyddeiriau:

                            llinell = Llinell(geiriau[idx_chw:idx_dde])
                            dat = datryswr_llinell(llinell, pengoll=False)
                            if dat.dosbarth and dat.dosbarth not in dim_diolch:
                                dat.gair_olaf().terfyn = [EOL()]
                                dats.append(dat)
                                idx_chw = idx_dde
                                break

                        idx_dde += 1
                    idx_chw += 1

        return dats

    def odliadur(self, qstr, llusg=False, acennog=False):
        return odl_search(qstr, acennog=acennog, llusg=llusg)

    def cleciadur(self, qstr):
        return clec_search(qstr)

    def demo_penillion(self):
        """
        Datrys llinellau o'r ffeil `profion_pennill`.
        """

        from ceibwr.profion_pennill import profion

        for dosbarth, test_cases in profion.items():

            for s in test_cases:

                # tudalen newydd bob pennill
                call(["clear"])
                print('========================================')
                print(dosbarth.upper())
                print('========================================')

                # print(test_case)
                pennill = Pennill(s)
                print(pennill)

                dat = datryswr_pennill(pennill)

                # show
                # print(repr(dat))
                # print()
                print(dat.create_tabular(fancy=True, toriad='|', cmap=self.cmap))
                print(self.beiro.cyan(dat.dosbarth) if dat.dosbarth else self.beiro.coch('XXX'))

                try:
                    input("...")

                except KeyboardInterrupt:
                    print(' Beth ...?')
                    return
            # print('----------------------------------------')

    def demo_cwpledi(self):
        """
        Datrys llinellau o'r ffeil `profion_cwpled`.
        """

        from ceibwr.profion_cwpled import profion

        for dosbarth, test_cases in profion.items():

            for s in test_cases:

                # tudalen newydd bob cwpled
                call(["clear"])

                print('========================================')
                print(dosbarth.upper())
                print('========================================')

                # s1 = test_cases[0]
                # s2 = test_cases[1]

                x1 = Llinell(s[0])
                x2 = Llinell(s[1])
                # print('x1:', x1)
                # print('x2:', x2)

                dat1 = datryswr_llinell(x1, pengoll=True)
                dat2 = datryswr_llinell(x2)

                # print(test_case)
                # pennill = Pennill(s)
                dat = prawf_cwpled(dat1, dat2)

                # show
                # print(repr(dat))
                print(dat)
                print(dat.create_tabular(fancy=True, toriad='|', cmap=self.cmap))
                print(self.beiro.cyan(dat.dosbarth) if dat.dosbarth else self.beiro.coch('XXX'))

                try:
                    input("...")
                except KeyboardInterrupt:
                    print(' Beth ...?')
                    return
            # print('----------------------------------------')

    def demo_llinellau(self):
        """
        Datrys llinellau o'r ffeil `profion_llinell`.
        """

        # mae angen hwn am clrscr
        from subprocess import call

        from ceibwr.seinyddwr import Seinyddwr
        seinyddwr = Seinyddwr()

        # darllen profion
        from ceibwr.profion_llinell import profion

        for dosbarth, test_cases in profion.items():
            call(["clear"])
            print('========================================')
            print(dosbarth.upper())
            print('========================================')
            for test_case in test_cases:
                llinell = Llinell(test_case)

                # seinyddio a datrys
                seinyddwr.seinyddio(llinell)
                dat = datryswr_llinell(llinell)

                # show
                print(dat, end='')
                print()
                print(dat.show_fancy(toriad='|', cmap=self.cmap))
                if dat.dosbarth:
                    print(self.beiro.cyan(dat.dosbarth))
                else:
                    print(self.beiro.coch('XXX'))
                print('--------------------')

            try:
                input("...")

            except KeyboardInterrupt:
                print(' Beth...?')
                return


# ------------------------------------------------
# test
def main():

    pe = Peiriant()
    
    s = "Dwyglust feinion aflonydd"

#     s = "Trydar mwyn adar mynydd"

#     s = """Wele rith fel ymyl rhod - o'n cwmpas
# Campwaith dewin hynod.
# Hen linell bell nad yw'n bod
# Hen derfyn nad yw'n darfod."""

#     s = """
# ---
# teitl: Bechingalw
# awdur: Gerallt Emrys
# ---
# Wele rith fel ymyl rhod - o'n cwmpas
# Campwaith dewin hynod.
# Hen linell bell nad yw'n bod
# Hen derfyn nad yw'n darfod.

# Nid eiddil pob eiddilwch,
# Tra dyn, nid llychyn pob llwch;
# Ac am hynny, Gymru, gwêl
# Y gŵr sydd ar y gorwel."""

    meta, uned = pe.parse(s)
    print('meta:', meta)
    print('uned:', uned)
    print(type(uned))
    dat = pe.datryswr(uned)
    print(repr(dat))


if __name__ == "__main__":
    main()
