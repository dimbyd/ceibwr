# seinyddwr.py
"""
Trawsnewid y ffurf orgraffyddol i ffurf seinyddol.

Mae w-gytsan, y-olaudywyll a wy-leddf/dalgron yn COMPLICATED !!!

Last minute decision cyn uwchlwytho i GitHub, yw peidio trio
seinyddio rhain, gan fod llawer o gynganeddion neis yn cael eu
gwrthod o ganlyniad i'r hacks fod yn rybish!!

Felly dim seinyddio wy/wy na y-olau/dywyll am nawr, ond cadw'r
seinyddio w-gystain er mwyn gwragedd a gwlad.

Ai dyma'r lle priodol am benodi acenion `Sillaf` neu `Gair`
    - acen ar un llafariad penodol ymhob `Cnewyllyn`
    - prifacen ar un sillaf penodol ymhob `Gair`

Terminoleg
(1) Mae seineg (phonetics) yn gweithredu ar lefel ffonemau:
    - cywasgu cytseiniaid ddwbl 
    - meddalu cytseiniaid (t -> d, c -> g, p -> b):
    - caledu cytseiniaid (d -> t, g -> c, b -> p)

    ** Mae seinegoli yn digwydd rhwng parau o nodau dilynol
    *** Gall rhain ddigwydd:
        - o fewm cyfresi: e.e. .wa.str|.a.ff -> .wa.sdr|.a.ff
        - ar draws bylchau: e.e. .wy.n|.e.b h.au.l -> .wy.n|e.p h.au.l

(2) Mae seinyddiaeth (phonology) yn gweithredu ar lefel sillafau a geiriau
Ond, mae weithiau angen cyd-destun y `Gair` er mwyn penderfynu os oes
angen trawsnewid yn seinegol e.e.
        - penodi 'y' fel 'y-olau' neu 'y-dywyll'
        - penodi 'w' fel 'w-gytsain'
            - e.e. tric g.w.l|.a.d -> gwl.a.d
        - penodi os yw `Gair` lluosill yn acennog
            - e.e tric 'h-cyn-y-sill-olaf' (parhau)

    (1) Lefel `Sillaf`:
        - prif lafariad (sy'n cario acen y sillaf)
    
    (2) Lefel `Gair`:
        - prif sillaf (prif acen)
        - w-gytsain           # dibynnu ar safle'r sillaf
        - y-olau/y-dywyll     # dibynnu ar safle'r sillaf mewn gair

Hollti sillafau
    Lefel `Gair` (d.uo.n -> d.u.|.o.n)

Cyfuno sillafau
    Lefel `Gair` (g.w.l|.a.d -> gwl.a.d)

Acennu:
    Lefel `Gair` ('parhau -> parh'au)

Odlau deheuol:
    - Lefel ffonemau (u -> i ayb)

Ynganiad ddeheuol:
    - Lefel `Gair` (c.w.bl -> c.w.b|..l neu c.w.b|.w.l

y-olau neu y-dywyll:
    - Lefel `Gair' (dibynnu ar y gair cyfan)

FELLY mae rhagbrosesu drwy:
    1. seinyddio ar lefel `Gair`
    2. seinegoli ar lefel `Uned` (`Gair`, `Llinell`, `Cwpled`, `Pennill`)   

Hen stwff:
    Mae angen seinegoli llinellau, cwpledi a phenillion fel cyfres o sillafau.
    Mae gan bob gwrthrych `Nod` ddau briodwedd:
        Nod.text
        Nod.sain
    Mae'r seinegoli yn dibynnu ar nodau sy'n dod cyn
    neu ar ol y nod o fewn y frawddeg.

    Pan mae gwrthrych `Nod` yn cael ei greu tra'n creu
    gwrthrych `Gair`, `Llinell`, `Cwpled` neu `Pennill`,
    rhaid i'r nod yna bob amser berthyn i'r uned honno, 
    nid i'r `Gair` unigol mewn `Llinell` ayb gan y bydd
    `nod.sain` yn dibynnu ar y nodau cyn ac/neu ar ôl y
    nod hynny yn y dilyniant.

    Bydd dal rhaid check am nodau cyswllt, trychben a chysylltben,
    ac odlau cudd: mae rhain yn symud neu copio nodau ar draws
    bylchau rhwng geiriau (ar ol eu seinegoli os oes angen).

    Felly dydyn ni ddim yn gwneud copi seinegol o'r uned, ond 
    yn hytrach recordio'r trosiadau yn y nodau unigol, a chael 
    dulliau recursive i ddychwelyd y nod lythrennol neu seinegol
    fel sydd angen. Mae hyn yn golygu nad oes angen cadw map o'r
    trosiadau yn y dadansoddiad (mae dadlau nad yw'r broses o
    seinegoli wir yn perthyn i'r dadansoddiad anyway)
    nod.text()
    nod.sain()

    !! Mae angen trin deuseiniaid yn well !!

deuseiniaid.py
    - lookups / dosbarthiadau
    - rheolau odl

    unsain: H, B
    deusain: T, L1, L2, L3
    trisain: (T, T), (T, LL), (LL, T), (LL, LL)

Acennu deuseiniaid
(1) deuseiniaid lleddf (falling or descending diphthong)
    acen ar y llafariad cyntaf

(2) deuseiniaid talgron (rising or ascending diphthong)
    acen ar yr ail lafariad (dim ond yr ail sydd angen odli)

LL1 = ['aw', 'ew', 'iw', 'ow', 'uw', 'yw'],
LL2 = ['ae', 'ai', 'ei', 'oe', 'oi', 'Wy'],
LL3 = ['au', 'eu', 'ou', 'ey', 'oy'],
T = ['ia', 'ie', 'io',  'iw', 'iy', 'ua', 'wa', 'we', 'wi', 'wo',  'wy', 'yu'],

1. Cnewyllyn sengl
Mae angen gwirio am w-gytsain fan hyn
gwr.a.nd|.o.
gwl.a.d

2. Cnewyllyn ddeusain
d.e.d|.wy.dd
.y.ml|.e.d|.ia.d

Mae hefyd angen hollti deuseiniaid deusill ('uo', 'eo', 'ea', 'oa', 'ee')
d.uo.n -> d.u.|.o.n
.eo.s -> .e.|.o.s
cr.ea.d -> cr.e.|.a.d
d.ee.ll|.i.r -> d.e.|.e.ll|.i.r

3. Cnewyllyn deirsain
Dim ond y ddau lafariad olaf sydd angen cyfateb mewn odl
    e.e. pren/awen (LL-T), iaith/gwaith (T-LL)

3a. Lleddf/Lleddf (LL-LL)
Mewn cyfuniad o dri: aew, oew, auw, euw, ouw, eyw, oyw, ywy
gl.oyw. -> gl.oy.|.w.
d.aea.r => d.ae..a.r
b.ywy.d -> b.yw.|.y.d
cr.e.d|.oau. -> cr.e.d|.o.|.au.

3b. Lleddf/Talgron (LL-T)
Dwy lafariaid cryf naill ochr, llafariad cymharol wan yn y canol
  => Mae ANGEN hollti fan hyn
  => Acenion ar y llafariaid cyntaf ac olaf
.awe.n -> .aw.|.e.n
ll.awe.n -> ll.aw.|.e.n
b.ywy.d -> b.yw.|.y.d

3c. Talgron/Lleddf (T-LL)
Dwy lafariaid cymharol wan naill ochr, llafariad gref yn y canol
  => Does DIM ANGEN hollti fan hyn
  => Acen ar y llafariad ganol (T ac LL yn atgyfnerthu eu gilydd)
g.wai.r
g.e.n|.wai.r
.iai.th
g.wai.th

3d. Talgron - Talgron (T-T)
(i) wiw, wyw - does DIM ANGEN hollti (acen ar y llafariad ganol)
g.wiw.
(ii) iwi, iwy - mae ANGEN hollti (tebyg i LL-T dwy sill)
p.iwi.s -> p.iw.|.i.s
d.iwy.d -> d.i.|.wy.d

(4) Cnewyllyn bedairsain
Mae angen hollti cyfresi o bedwar llafariad mewn i ddau hanner
Dim ond yr ail ddeusain sy'n bwysig mewn odl
.ieua.nc -> .ie.|.ua.nc,
g.wywo -> g.wy.|.wo.
gl.awio. -> gl.aw.|.io.
gl.oywi. -> gl.oy.|.wi.
g.wayw.ff|.o.n - > g.wa.|.yw.ff|.o.n

TODO: nb -> mb, np -> mp

TODO: mae ceisio seinegoli y-olau yn torri mwy na mae'n datrys
Am y tro, beth am odli pob "u" a "y" yn ddi-wahan, a hefyd y ddau 'wy'?

"""
from copy import copy

from ceibwr.cysonion import (
    cyfuniadau_meddal,
    cyfuniadau_caled,
    cyfuniadau_trychben,
    eithriadau,
)

from ceibwr.sillaf import Sillaf
from ceibwr.gair import Gair

from ceibwr.llinell import Llinell
from ceibwr.pennill import Pennill
from ceibwr.cerdd import Cerdd

from ceibwr.corfan import Corfan
from ceibwr.rhaniad import Rhaniad


def cyfatebiaeth(nod1, nod2):
    """
    Gwirio os yw dau nod yn cyfateb o ran SAIN
    Mewnbwn: dau `Nod`
    Allbwn: bool
    """
    s1 = nod1.sain.lower()
    s2 = nod2.sain.lower()

    if s1 == s2:
        return True
    elif s1 in ["ng", "ngh"] and s2 in ["ng", "ngh"]:
        return True
    elif s1 in ["m", "mh"] and s2 in ["m", "mh"]:
        return True
    elif s1 in ["n", "nh"] and s2 in ["n", "nh"]:
        return True
    elif s1 in ["ph", "ff"] and s2 in ["ph", "ff"]:
        return True
    elif s1 in ["r", "rh"] and s2 in ["r", "rh"]:
        return True
    elif s1 in ["s", "sh"] and s2 in ["s", "sh"]:
        return True
    elif s1 in ["m", "mh"] and s2 in ["m", "mh"]:
        return True
    else:
        return False


class Seinyddwr():

    def __init__(self):
        pass

    # --------------------
    # omnibus
    def seinyddio(self, uned, deheuol=False):

        if type(uned) is Gair:
            self.seinyddio_gair(uned, deheuol=deheuol)

        elif type(uned) is Llinell:
            self.seinyddio_llinell(uned, deheuol=deheuol)

        elif type(uned) is Pennill:
            for llinell in uned.children:
                self.seinyddio_llinell(llinell, deheuol=deheuol)

        elif type(uned) is Cerdd:
            for pennill in uned.children:
                for llinell in pennill.children:
                    self.seinyddio_llinell(llinell, deheuol=deheuol)

        elif type(uned) is Corfan:
            self.seinyddio_llinell(Llinell(uned.geiriau()))

        elif type(uned) is Rhaniad:
            self.seinyddio_llinell(Llinell(uned.geiriau()))

        else:
            raise TypeError('Mae angen `Gair`, `Llinell`, `Pennill`, `Cerdd`, `Corfan` neu `Rhaniad` fan hyn.')

    # Gair
    def seinyddio_gair(self, gair,
                       cywasgu=True,
                       meddalu=True,
                       caledu=True,
                       deheuol=False):

        # type check
        if not isinstance(gair, Gair):
            raise TypeError("Mae angen `Gair` fan hyn.")
        
        self.seinyddio_yolau(gair)
        self.seinyddio_wgytsain(gair)
        self.seinyddio_ac(gair)

        # seinyddio fesul pâr o nodau
        nodau = gair.nodau()
        for x, x_next in zip(nodau[:-1], nodau[1:]):

            # cywasgu cytseiniaid ddwbl
            if cywasgu:
                self.cywasgu(x, x_next)

            # meddalu dan effaith y gytsain flaenorol
            if meddalu:
                self.meddalu(x, x_next)

            # caledu dan effaith cytsain gyfagos
            if caledu:
                self.caledu(x, x_next)

        # TODO: seinyddio deheuol
        if deheuol:
            pass

    def seinyddio_ac(self, gair):
        if str(gair).lower() in ['ac', 'nac']:
            gair[-1].coda().children[-1].sain = 'g'

    def seinyddio_wgytsain(self, gair):
        '''
        Hacks pur fan hyn!

        Ymysg y bedw yn ddedwydd (!!)
        Beth am "gwrol" vs "gwraig"?
        '''

        if gair.nifer_sillafau() < 2:
            return

        # gwlad, gwneud, ond beth am gwn? neu gwrol?
        x = gair.children[0]
        if (
            str(x.cyrch()).lower() in ["", "g"] and
            str(x.cnewyllyn()).lower() in ["w"] and
            str(x.coda()).lower() in ["l", "n", "r"]
        ):
            if not str(gair.children[1].cnewyllyn()).lower() in ["o"]:
                gair.children = gair.children[1:]
                nodau_newydd = x.nodau() + gair.children[0].cyrch().children 
                gair.children[0].cyrch().children = nodau_newydd

        # check eithriadau
        if str(gair) in eithriadau["w-gytsain"]:
            # print('G:', gair)
            for sillaf in gair.sillafau():
                if str(sillaf.cnewyllyn()) == 'w'.lower():
                    # print(sillaf)
                    if sillaf.nesaf():
                        sillaf_nesaf = sillaf.nesaf()
                        # print('S1:', sillaf_nesaf)
                        nodau = sillaf.nodau()
                        cyrch_nesaf = sillaf_nesaf.cyrch()
                        cyrch_nesaf.children = nodau + cyrch_nesaf.children
                        # print('S2:', sillaf_nesaf)
                        gair.children.remove(sillaf)

    def seinyddio_yolau(self, gair):
        """
        Hacks pur fan hyn!

        Mae angen gosod sain y-olau i "u". Mae pob 'y' sy'n 
        weddill yn dywyll. Y broblem yw penderfynnu pa rai
        sy'n olau, a pha rai sy'n dywyll.

        y-dywyll yw "schwa", sef 'ə' (y llafariad wanaf)
        y-olau: 'ɨ' (gog) neu 'ɪ' (de) (u-bedol)

        e.e. "tywyll": cyntaf yn dywyll, olaf yn olau

        Tric: 
            y-olau yn y sill olaf, y-dywyll fel arall
        
        Eithriadau:
            1. sillaf unsill, dim cyrch
                yn, y, yng, ..
            2. sillaf unsill, dim coda
                fy, dy, ...

        NITEMARE: Rhaid dewis rhwng y-dywyll neu y-olau ar ôl
        i'r sillafau gael eu hollti ac aceniad y gair ei 
        ddatrys. HOWEVER mae rhai penderfyniadau am
        hollti clymau llafariaid yn dibynnu ar os mai 
        y-olau neu y-dywyll sy'n bresennol, yn enwedig
        yn achos wy-dalgron (y-olau) neu wy-leddf (y-dywyll).

        y-olau/wy-dalgron: diwyd -> d.iw.|.y.d
        y-dywyll/wy-leddf: bwriwyd -> b.w.r|.iwy.d
        """

        if gair.nifer_sillafau() == 1:

            cyrch = gair.children[0].cyrch()
            cnewyllyn = gair.children[0].cnewyllyn()
            coda = gair.children[0].coda()
            if (
                len(cnewyllyn.children) == 1 and
                str(cnewyllyn).lower() in ['y']
            ):
                if cyrch.children and coda.children:
                    cnewyllyn.children[-1].sain = 'u'

        elif gair.nifer_sillafau() > 1:
            if 'wy' not in str(gair.children[-1].cnewyllyn()):  # TODO
                for nod in gair.children[-1].cnewyllyn():
                    if str(nod) in ['y']:
                        nod.sain = 'u'

    def cywasgu(self, x, x_next):
        '''
        Cywasgu cytseiniaid ddwbl
        Mae angen defnyddio `cyfatebiaeth(s1, s2) fan hyn
         e.e. er mwyn cywasgu 'm' a 'mh' cyfagos
        "Ym mhob byw y mae pawen"
        '''
        if cyfatebiaeth(x, x_next):
            # x_next.sain = ' '*len(x_next.text)
            x_next.sain = ''

    def meddalu(self, x, x_next):
        '''
        Meddalu dan effaith y gytsain flaenorol
        dim ond 't', 'c' a 'p' sydd yn berthnasol
        '''
        key = (x.text.lower(), x_next.text.lower())
        if key in cyfuniadau_meddal:
            x_next.sain = cyfuniadau_meddal[key]

    def caledu(self, x, x_next):
        '''
        Caledu dan effaith cytsain gyfagos
        Gall un neu'r ddau gytsain drawsnewid
        '''
        if (x.text.lower(), x_next.text.lower()) in cyfuniadau_caled:
            seinau_caled = cyfuniadau_caled[x.text.lower(), x_next.text.lower()]
            x.sain = seinau_caled[0]
            x_next.sain = seinau_caled[1]

    # --------------------
    # Llinell
    def seinyddio_llinell(self, llinell,
                          cywasgu=True,
                          meddalu=True,
                          caledu=True,
                          deheuol=False):

        if not isinstance(llinell, Llinell):
            raise TypeError('Mae angen `Llinell` fan hyn')

        # seinyddio geiriau unigol
        geiriau = llinell.children
        for gair in geiriau:
            self.seinyddio_gair(gair,
                                cywasgu=cywasgu,
                                meddalu=meddalu,
                                caledu=caledu,
                                deheuol=deheuol)

        # seinyddio fesul pâr
        for x, x_nesaf in zip(geiriau[:-1], geiriau[1:]):

            # hack: skip atalnodau ar ddiwedd y coda
            # cco = copy(x[-1].coda())
            # print('CCO-1:', cco)
            # while cco and cco[-1].is_atalnod():
            #     cco.children = cco.children[:-1]
            # print('CCO-2:', cco)
            # cyts = cco + x_nesaf[0].cyrch().children
            cyts = x[-1].coda().children + x_nesaf[0].cyrch().children
            for c, c_nesaf in zip(cyts[:-1], cyts[1:]):

                # cywasgu cytseiniaid ddwbl
                if cywasgu:
                    self.cywasgu(c, c_nesaf)

                # meddalu dan effaith y gytsain flaenorol
                if meddalu:
                    self.meddalu(c, c_nesaf)

                # caledu dan effaith cytsain gyfagos
                if caledu:
                    self.caledu(c, c_nesaf)
    
    # --------------------
    # TODO: seinyddiaeth ddeheuol
    def seinyddio_ddeheuol(self, uned):
        """
        1. Ailosod pob 'u' ac 'y-olau' gyda 'i'
        2. Ailosod pob 'ae' gyda 'ai' etc.
        """
        pass

    def odlau_ddeheuol(self, uned):
        pass

    def trychben_ddeheuol(self, uned):
        '''
        Ehangu cyfuniadau trychben
        Hack am y llafariad ymwthiol.
        '''
        for gair in uned.geiriau():
            coda = gair.children[-1].coda()
            cyts = coda.llythrennau()
            if len(cyts) > 1:
                tr = ''.join([c.text for c in cyts[-2:]])
                if tr in cyfuniadau_trychben:
                    cytsain_olaf = coda.children.pop()
                    cnewyllyn = gair.children[-1].cnewyllyn()

                    # copio'r llafariad wreiddiol ??
                    # neu rhoi y-dywyll (schwa) bob amser
                    # cwbl -> cwbwl, pobl -> pobol
                    # llwybr -> llwybyr,
                    # parabl -> parabyl
                    # chwedl -> chwedyl
                    cnew_str = cnewyllyn[-1].text  # copy
                    sillaf_newydd = Sillaf(
                        cyrch='',
                        cnewyllyn=cnew_str,
                        coda=str(cytsain_olaf)
                    )
                    gair.children.append(sillaf_newydd)


# ------------------------------------------------
# test
def main():

    test_llinellau = [
        "O dad, yn deulu dedwydd",
        "Lle i enaid gael llonydd",
        "Ond daw gwefr cyn atgofion",
        "Y ddinas draw yn wastraff",
        "Yn wyneb haul ar Epynt",
        "Yr esgob biau popeth",
        "Aeth fy nghariad hyd ato",
        "O'r garreg hon daeth eco",
        "I'r esgob pur rhoed popeth",
        "Fy nghariad troaf atat",
        "O'r garreg clywaid eco",
        "Gwae nid gweniaeth",
        "Yma bu cydnabod",
        "Mwyar duon",
        "Ond daw gwefr cyn atgofion",
        "tywyll",
    ]

    seinyddwr = Seinyddwr()
    for s in test_llinellau:

        llinell = Llinell(s)
        seinyddwr.seinyddio(llinell)
        print(llinell, end='')
        print(llinell.sain())


def main2():
    test_geiriau = {
        'unsain': [
            'car',
            'da',
            'afal',
        ],
        'deugraffau_deusill': [
            'duon', 'eos',
            'priod', 'piod', 'diod', 'diog'
            'dianc', 'diadell',
        ],
        'LL-T': [
            'awel',
            'ieuanc'
        ],
        'LL-LL': [
            'hoyw',
            'gloyw',
        ],
        'T-T': [
            'piwis',
        ],
        'T-LL': [
            'anifeiliaid',
            'triawd',
        ],
        'pedwarsain': [
            'gloywi',
            'glawio',
            'hoywon',
            'rywiog',
        ],
        'pumsain': [
            'lliwiau',
            'crawiau',
            'ieuainc',
            'sioeau',
        ],
        'chwesain': [
            'wiwiau',
        ],
    }

    seinyddwr = Seinyddwr()
    for s in test_geiriau:
        for key in test_geiriau:
            print("==============================")
            print(key.upper())
            print("==============================")
            for s in test_geiriau[key]:
                gair = Gair(s)
                seinyddwr.seinyddio(gair)
                print(repr(gair))
                print(gair.show_acenion())
                print(gair)
                print('-----')


if __name__ == "__main__":
    main()
    # main2()
