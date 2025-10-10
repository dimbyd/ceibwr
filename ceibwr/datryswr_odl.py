# prawf_odl.py
"""
Dulliau darganfod odl neu broest rhwng dwy sillaf

JMJ 220: Mae odl yn nodi diwedd llinell neu hanner llinell,
neu i ddangos curiad yng nghanol llinell.

Galw sylw at sillaf mae cytseinedd ac odl fel ei gilydd.
    cytseinedd ar y dechrau: trwm/traeth
    odl ar y diwedd: trwm/plwm

JMJ [355]: Cyfatebiaeth *sillafau* yw odl.
JMJ [312]: Gan nad oes doriad rhwng sillafau ni ddylid 
gwarafun cyfrif cymaint ag a fynner o'r cytseiniaid a 
fo ynghlwn rhyngthynt i lunio odl.

x = x.cyrch|x.cnewyllyn|x.coda + xnesaf.cyrch
y = y.cyrch|y.cnewyllyn|x.coda + ynesaf.cyrch

x = x.a|x.b|x.c   + xnesaf.a
y = y.a|y.b|y.c   + ynesaf.a

odl:    (x.coda == y.coda) a (x.cnew == y.cnew)
proest: (x.ccoda == y.coda) & (x.cnew != y.cnew) # ond yr un pwysau

# dosbarthiadau = {
#    ('ODD', 'odl ddwbwl'), # neu odl gyflawn
#    ('ODL', 'odl'),        # neu odl anghyflawn
#    ('OLA', 'odl lafarog'),
#    ('OLU', 'odl lusg'),
#    ('OLL', 'odl lusg lafarog'),
#    ('PRO', 'proest'),
#    ('PLA', 'proest lafarog'),
# }

Trwm ac Ysgafn (AYG t.61, JMJ 413-7)

JMJ
1. Geiriau unsill yn diweddu -n, -r, -l:
    rhaid i'r llafariaid fod yr un hyd
    tân/glân neu rhan/llan

414 TAY mewn Cynghanedd Lusg
    - dim ond os yw'r odl gyntaf yn air unsill ac
        yn diweddu gyda -n, -r, -l.
        "I wlad Fôn nid â honno" (TAY)
    - nid oes TAY os yw'r odl gyntaf yn ddiacen.
    - nid oes TAY wrth odli unsillafion eraill 

TODO: Mae'r opsiwn `trwm_ac_ysgafn=True` yn gwrthod cynganeddion Lusg
sydd yn torri'r rheol (AYG tud. 61). Oes angen hwn
"""

from ceibwr.cysonion import atalnodau, deuseiniaid, dosbarth_deusain
from ceibwr.sillaf import Sillaf
from ceibwr.gair import Gair

from ceibwr.corfan import Corfan
from ceibwr.rhaniad import Rhaniad

from ceibwr.odlau import Odlau

import logging
log = logging.getLogger(__name__)


def prawf_odl(x, y,
              llusg=False,
              trwm_ac_ysgafn=False,
              proest_ok=False,
              ):
    """
    input x: `Gair` unigol, neu tuple (`Gair`, `Gair`)
    input y: `Gair` unigol, neu tuple (`Gair`, `Gair`)
    output: dosbarth odl

    odlau cudd: benthyg nod/nodau o'r gair nesaf i greu odl
    """

    # init
    odlau = Odlau()

    # type check
    if type(x) is not Gair:
        raise TypeError("Mae angen Gair fan hyn, nid {}".format(type(x)))
    if type(y) is not Gair:
        raise TypeError("Mae angen Gair fan hyn, nid {}".format(type(y)))

    # Gwirio bod o leiaf un sill bob ochr
    if not x.children or not y.children:
        msg = f"Mae angen o leiaf un sillaf bob ochr: {x[-1]}, {y[-1]}"
        odlau.hysbys.append(msg)
        return odlau
    
    # Echdynnu sill olaf y gair cyntaf
    xs = x.children[-1]

    # Echdynnu sill olaf/olaf-ond-un yr ail air
    if not llusg:
        ys = y.children[-1]  # sill olaf

    else:
        if y.is_acennog() or len(y.children) < 2:
            msg = f"LLU: mae angen gair diacen yn olaf:: {x[-1]}, {y[-1]}"
            odlau.hysbys.append(msg)
            return None

        ys = y.children[-2]  # sill olaf-ond-un

        # gwirio bai trwm-ag-ysgafn os oes angen
        # mae hwn yn gymhleth (gweler JMJ Cerdd Dafod)
        if trwm_ac_ysgafn:
            if str(xs.coda()) in ['n', 'r']:

                if xs.is_ysgafn() and not str(ys.coda()) == str(xs.coda()):
                    print('TAY: mae angen goben drom fan hyn')
                    return odlau

                if xs.is_trwm() and not str(ys.coda()) == 2*str(xs.coda()):
                    print('TAY: mae angen goben ysgafn fan hyn')
                    return odlau
                
            trwm_ac_ysgafn = False

    # print('(xs, ys):', (xs, ys))

    # prawf sylfaenol (dwy sillaf)
    odlau = prawf_odl_sylfaenol(xs, ys, trwm_ac_ysgafn=trwm_ac_ysgafn)


    # dychwelyd os oes llwyddiant
    if odlau and odlau.dosbarth in ['ODL', 'OLA']:
        if llusg:
            if odlau.dosbarth == 'ODL':
                odlau.dosbarth = 'OLU'
            elif odlau.dosbarth == 'OLA':
                odlau.dosbarth = 'OLL'
        return odlau

    if odlau and odlau.dosbarth in ['PGY', 'PLA'] and proest_ok:
        return odlau

    # ... fel arall, parhau i chwilio ...

    # profi am odl gyswllt
    # odlau = prawf_odl_gyswllt(xs, ys)
    # if odlau.dosbarth in ['OGY', 'OLA', 'OLU', 'OLL']:
    #     odlau.hysbys.append('odl gyswllt')
    #     return odlau

    # ----------------------
    # profi am odl gudd
    odlau = prawf_odl_gudd(xs, ys)
    if odlau and odlau.dosbarth in ['ODL', 'OLA', 'OLU', 'OLL']:
        odlau.hysbys.append('odl gudd')
        return odlau

    # methiant
    return odlau  # null


def prawf_odl_gudd(x, y):
    '''
    Mewnbwn: dwy `Sillaf`
    '''
    if not type(x) is Sillaf and type(y) is Sillaf:
        raise TypeError('Mae angen dwy `Sillaf` fan hyn.')

    # TODO: return `None` instead
    odlau = Odlau()

    # cyrchu sillafau nesaf (if any)
    x_nesaf = x.nesaf()
    y_nesaf = y.nesaf()

    def _checkit(z, z_nesaf, w):

        odlau = Odlau()
        if z_nesaf.cyrch():
            z_nodau_nesaf = z_nesaf.cyrch()
            z_nodau = z.coda()
        elif not z.coda():
            z_nodau_nesaf = z_nesaf.cnewyllyn()
            z_nodau = z.cnewyllyn()
        else:
            return odlau  # empty

        end_idx = 0
        for idx, z_nod in enumerate(z_nodau_nesaf):
            end_idx += 1

            z_nodau.append(z_nod)
            odlau = prawf_odl_sylfaenol(z, w)
            if odlau and odlau.dosbarth in ['ODL', 'OLA', 'OLU', 'OLL']:
                # reset
                z.odl().nodau_cudd = z_nodau.children[-end_idx-1:]
                break

        z_nodau.children = z_nodau.children[:-end_idx]
        return odlau

    if x_nesaf:
        odlau = _checkit(x, x_nesaf, y)

    if not odlau and y_nesaf:
        odlau = _checkit(y, y_nesaf, x)

    return odlau


def prawf_odl_gyswllt(x, y):
    '''
    Input: dwy `Sillaf`
    '''
    if not type(x) is Sillaf and type(y) is Sillaf:
        raise TypeError('Mae angen dwy `Sillaf` fan hyn.')

    odlau = Odlau()

    x_cnew = x.cnewyllyn()

    # Mae atalnodau wastad ar ddiwedd cyfres o lafariaid neu cytseiniaid
    # i'r = .i'.r , o'r = .o'.r
    # TODO: meddwl am "i'w"

    # 1. dileu'r coda,
    # 2. dileu'r atalnod o ddiwedd y cnewyllyn
    if x_cnew and x_cnew[-1].text in atalnodau:
        x_atalnod = x_cnew.children.pop()
        x_coda_children = x.coda().children
        x.coda().children = []

        # profi
        odlau = prawf_odl_sylfaenol(x, y)

        # ailosod atalnodau
        x_cnew.append(x_atalnod)
        x.coda().children = x_coda_children

    return odlau


def prawf_odl_sylfaenol(x, y, trwm_ac_ysgafn=False):
    """
    Gwirio am odl neu broest sylfaenol rhwng dwy `Sillaf`
    Mae'r gymhariaeth ar sail `nod.sain` felly maen'n rhaid 
    seinyddio cyn fan hyn!

    Rhwng geiriau neu sillafau? mae angen benthyg nodau o'r 
    gair nesaf -> lefel geiriau yn OK.

    Ond e.e. Llusg mae'n rhaid odli sillafau yn y pendraw 
        neu gallen ni just chopio sill olaf y brifodl
        ond wedyn base angen rhoi fe nol - falle base
        hyn yn haws na symud nodau unigol??

    Rhaid i bob newid/adjustment fod gyda'r nodau gwreiddiol.
    Beth am shallow copy?
    """

    # type check
    if type(x) is Gair and x.children:
        x = x[-1]  # sillaf olaf
    if type(y) is Gair and y.children:
        y = y[-1]

    # type check
    if type(x) is not Sillaf or type(y) is not Sillaf:
        raise ValueError("Mae angen dwy `Sillaf` fan hyn.")

    # echdynnu'r odlau
    x_odl = x.odl()
    y_odl = y.odl()

    # print('(x_odl, y_odl):', (x_odl, y_odl))

    # Echdynnu'r codau (heb atalnodau)
    x_coda = x.coda().nodau(atalnodau=False)
    y_coda = y.coda().nodau(atalnodau=False)

    # Gwirio os yw'r ddau coda yn cyfateb, yn
    # cynnwys am ddau linyn gwag (odl lafarog)
    # Os nad yw'r ddau yn cyfateb, does dim odl.
    x_coda_str = "".join([nod.sain for nod in x_coda])
    y_coda_str = "".join([nod.sain for nod in y_coda])

    # print('x_coda_str, y_coda_str:', x_coda_str, y_coda_str)

    # methiant: dim cyfatebiaeth rhwng y codas
    if x_coda_str and y_coda_str and x_coda_str != y_coda_str:
        return None
    if (not x_coda_str and y_coda_str) or (x_coda_str and not y_coda_str):
        return None

    # echdynnu'r cnewyll (heb atalnodau)
    x_cnew = x.cnewyllyn().nodau(atalnodau=False)
    y_cnew = y.cnewyllyn().nodau(atalnodau=False)

    # talfyrru cnewyll trisain ()
    if len(x_cnew) > 2:
        x_cnew = x_cnew[-2:]
    if len(y_cnew) > 2:
        y_cnew = y_cnew[-2:]

    # echdynnu'r llinynnau ysgafn cyfatebol
    # (ar gyfer lookups dosbarth deusain)
    x_str = "".join([nod.sain_fer() for nod in x_cnew]).lower()
    y_str = "".join([nod.sain_fer() for nod in y_cnew]).lower()

    # Gwirio os yw'r deuseiniaid yn wybyddus i'r system
    if len(x_str) > 1 and x_str not in dosbarth_deusain:
        # raise Warning('Heb adnabod y ddeusain {}'.format(x_str))
        pass

    if len(y_str) > 1 and y_str not in dosbarth_deusain:
        # raise Warning('Heb adnabod y ddeusain {}'.format(y_str))
        pass

    # init
    dosbarth = None

    # ----------------------
    # 1. dwy lafariad unigol
    if len(x_cnew) == 1 and len(y_cnew) == 1:
        # print('TAY:', trwm_ac_ysgafn)

        # odl: cnewyll yn cyfateb
        if not trwm_ac_ysgafn and x_str == y_str:
            dosbarth = 'ODL'

        elif trwm_ac_ysgafn and x_cnew[0].sain.lower() == y_cnew[0].sain.lower():
            dosbarth = 'ODL'

        # proest: cnewyll o'r un pwysau
        elif x_cnew[0].is_fer() == y_cnew[0].is_fer():
            dosbarth = 'PRO'

    # 2. deusain talgron a llafariad unigol
    elif (
        len(x_cnew) > 1 and len(y_cnew) == 1 and
        x_str in deuseiniaid["talgron"]
    ):
        # odl: ail lafariad y ddeusain yn cyfateb
        if x_cnew[1].sain_fer() == y_cnew[0].sain_fer():
            dosbarth = 'ODL'

        # proest: ail lafariad y ddeusain o'r un pwysau
        elif x_cnew[1].is_fer() == y_cnew[0].is_fer():
            dosbarth = 'PRO'

    # 3. llafariad unigol a deusain talgron
    elif (
        len(x_cnew) == 1 and len(y_cnew) > 1 and
        y_str in deuseiniaid["talgron"]
    ):
        # odl: ail lafariad y ddeusain yn cyfateb
        if x_cnew[0].sain_fer() == y_cnew[1].sain_fer():
            dosbarth = 'ODL'

        # proest: ail lafariad y ddeusain o'r un pwysau
        elif x_cnew[0].is_fer() == y_cnew[1].is_fer():
            dosbarth = 'PRO'

    # 4. dwy ddeusain
    elif len(x_cnew) > 1 and len(y_cnew) > 1:

        # odl: cyfatebiaeth union
        if (
            x_cnew[0].sain_fer() == y_cnew[0].sain_fer() and
            x_cnew[1].sain_fer() == y_cnew[1].sain_fer()
        ):
            dosbarth = 'ODL'

        # odl: cyfatebiaeth rhwng dwy ddeusain talgron wahanol
        elif x_str in deuseiniaid["talgron"] and y_str in deuseiniaid["talgron"]:

            # ... os yw'r llafariaid terfynol yn cyfateb
            if x_cnew[1].sain_fer() == y_cnew[1].sain_fer():
                dosbarth = 'ODL'

        # proest: cyfatebiaeth rhwng dwy ddeusain lleddf wahanol
        elif x_str in deuseiniaid["lleddf"] and y_str in deuseiniaid["lleddf"]:

            # ... a'r ddau o'r un dosbarth
            if dosbarth_deusain[x_str] == dosbarth_deusain[y_str]:
                dosbarth = 'PRO'

        # end cases

    # set nbds (cofnodi odlau)
    if dosbarth == 'ODL':
        x.odl().add_neighbours(y.odl().neighbours)
        y.odl().add_neighbours(x.odl().neighbours)
        x.odl().add_neighbour(y.odl())
        y.odl().add_neighbour(x.odl())

    # cofnodi odlau
    odlau = Odlau()

    # dosbarthu
    if not dosbarth:
        return odlau

    if dosbarth == 'ODL':
        dosbarth = 'ODL' if x_coda_str else 'OLA'
    if dosbarth == 'PRO':
        dosbarth = 'PGY' if x_coda_str else 'PLA'

    odlau.dosbarth = dosbarth
    odlau.append(x_odl)
    odlau.append(y_odl)

    if (
        x.coda().children and
        x.coda().children[-1].sain != x.coda().children[-1].text
    ) or (
        y.coda().children and
        y.coda().children[-1].sain != y.coda().children[-1].text
    ):
        odlau.hysbys.append('odl ewinog')

    return odlau


def prawf_codas(x, y):
    """
    Gwirio'r berthynas rhwng codas dwy sillaf.
    """

    # type check
    if type(x) is Gair and x.children:
        x = x[-1]
    if type(y) is Gair and y.children:
        y = y[-1]
    if type(x) is not Sillaf or type(y) is not Sillaf:
        raise ValueError("Mae angen dwy `Sillaf` fan hyn.")

    # Echdynnu'r codas (heb atalnodau)
    x_coda = x.coda().nodau(atalnodau=False)
    y_coda = y.coda().nodau(atalnodau=False)

    # Echdynnu'r llinynau sain (er mwyn cymharu)
    x_coda_str = "".join([nod.sain for nod in x_coda])
    y_coda_str = "".join([nod.sain for nod in y_coda])

    # check os yw'r ddwy sillaf yn llafarog
    if not x_coda_str and not y_coda_str:
        return True

    # check os yw'r ddau coda yn cyfateb
    if x_coda_str and y_coda_str and x_coda_str == y_coda_str:
        return True

    return False


def prawf_cnewyll(x, y, trwm_ac_ysgafn=True):
    """
    Gwirio'r berthynas rhwng cnewyll dwy sillaf.

    HAF hafal:      x.cnew == y.cnew
    BRA brashafal:  x.cnew != y.cnew, pwysau tebyg
    ANH anhafal:    x.cnew != y.cnew, pwysau gwahanol
    """

    # type check
    if type(x) is Gair and x.children:
        x = x[-1]  # sillaf olaf
    if type(y) is Gair and y.children:
        y = y[-1]
    if type(x) is not Sillaf or type(y) is not Sillaf:
        raise ValueError("Mae angen dwy `Sillaf` fan hyn.")

    # echdynnu'r cnewyll (heb atalnodau)
    x_cnew = x.cnewyllyn().nodau(atalnodau=False)
    y_cnew = y.cnewyllyn().nodau(atalnodau=False)

    # talfyrru cnewyll trisain (anwybyddu'r gyntaf)
    if len(x_cnew) > 2:
        x_cnew = x_cnew[-2:]
    if len(y_cnew) > 2:
        y_cnew = y_cnew[-2:]

    # echdynnu'r llinynnau ysgafn cyfatebol
    # (ar gyfer lookups)
    x_key = "".join([nod.sain_fer() for nod in x_cnew]).lower()
    y_key = "".join([nod.sain_fer() for nod in y_cnew]).lower()

    # Gwirio os yw'r deuseiniaid yn wybyddus i'r system
    if len(x_key) > 1 and x_key not in dosbarth_deusain:
        # print('Rhybudd: heb adnabod y ddeusain {}'.format(x_key))
        pass

    if len(y_key) > 1 and y_key not in dosbarth_deusain:
        # print('Rhybudd: heb adnabod y ddeusain {}'.format(y_key))
        pass

    # print((x_cnew, x_str), (y_cnew, y_str))
    # print(trwm_ac_ysgafn)

    # ----------------------
    # 1. dwy lafariad unigol
    if len(x_cnew) == 1 and len(y_cnew) == 1:

        # hafal: llafariaid unigolunfath
        if x_cnew[0].sain.lower() == y_cnew[0].sain.lower():
            return 'HAF'

        # bras hafal: llafariaid unigol o'r un pwysau
        elif x_cnew[0].is_fer() == y_cnew[0].is_fer():
            return 'BRA'

    # 2. deusain dalgron a llafariad unigol
    elif (
        len(x_cnew) > 1 and len(y_cnew) == 1 and
        x_key in deuseiniaid["talgron"]
    ):
        # hafal: ail lafariad y ddeusain yn cyfateb
        if x_cnew[1].sain_fer() == y_cnew[0].sain_fer():
            return 'HAF'

        # bras hafal: ail lafariad y ddeusain o'r un pwysau
        elif x_cnew[1].is_fer() == y_cnew[0].is_fer():
            return 'BRA'

    # 3. llafariad unigol a deusain dalgron
    elif (
        len(x_cnew) == 1 and len(y_cnew) > 1 and
        y_key in deuseiniaid["talgron"]
    ):
        # hafal: ail lafariad y ddeusain yn cyfateb
        if x_cnew[0].sain_fer() == y_cnew[1].sain_fer():
            return 'HAF'

        # bras-hafal: ail lafariad y ddeusain o'r un pwysau
        elif x_cnew[0].is_fer() == y_cnew[1].is_fer():
            return 'BRA'

    # 4. dwy ddeusain
    elif len(x_cnew) > 1 and len(y_cnew) > 1:

        # hafal: cyfatebiaeth union
        if (
            x_cnew[0].sain_fer() == y_cnew[0].sain_fer() and
            x_cnew[1].sain_fer() == y_cnew[1].sain_fer()
        ):
            return 'HAF'

        # hafal: cyfatebiaeth rhwng dwy ddeusain dalgron wahanol
        elif x_key in deuseiniaid["talgron"] and y_key in deuseiniaid["talgron"]:

            # ... os yw'r llafariaid terfynol yn cyfateb
            if x_cnew[1].sain_fer() == y_cnew[1].sain_fer():
                return 'HAF'

        # bras-hafal: cyfatebiaeth rhwng dwy ddeusain lleddf wahanol
        elif x_key in deuseiniaid["lleddf"] and y_key in deuseiniaid["lleddf"]:

            # ... a'r ddau o'r un dosbarth
            if dosbarth_deusain[x_key] == dosbarth_deusain[y_key]:
                return 'BRA'

        # end cases

    # anhafal
    return 'ANH'


def prawf_odl_newydd(x, y):

    # type check
    if type(x) is Gair and x.children:
        x = x[-1]  # sillaf olaf
    if type(y) is Gair and y.children:
        y = y[-1]
    if type(x) is not Sillaf or type(y) is not Sillaf:
        raise ValueError("Mae angen dwy `Sillaf` fan hyn.")
    
    # echdynnu'r odlau
    x_odl = x.odl()
    y_odl = y.odl()

    # print('(x_odl, y_odl):', (x_odl, y_odl))

    # check coda
    codas_ok = prawf_codas(x, y)
    if not codas_ok:
        return []

    # check cnewyll
    dosbarth_cnew = prawf_cnewyll(x, y, trwm_ac_ysgafn=False)

    odlau = Odlau()

    # dosbarthu
    if dosbarth_cnew == 'ANH':
        return odlau

    odlau.append(x_odl)
    odlau.append(y_odl)

    if dosbarth_cnew == 'HAF':
        odlau.dosbarth = 'ODL' if x.coda() else 'OLA'

    elif dosbarth_cnew == 'BRA':
        odlau.dosbarth = 'PGY' if x.coda() else 'PLA'

    # hac: hysbysu odl ewinog
    if (
        x.coda().children and
        x.coda().children[-1].sain != x.coda().children[-1].text
    ) or (
        y.coda().children and
        y.coda().children[-1].sain != y.coda().children[-1].text
    ):
        odlau.hysbys.append('odl ewinog')

    return odlau


# ------------------------------------------------
# test
def main():

    from ceibwr.profion_odl import profion
    from ceibwr.seinyddwr import Seinyddwr
    from ceibwr.beiro import Beiro
    beiro = Beiro()

    profion["trwm_ac_ysgafn"] = (
        ("sôn", "digonol"),
        ("môr", "oriau"),
        ("ton", "honno"),
        ("car", "carreg"),
        ("sen", "henaint"),
        ("mân", "llannerch"),
    )

    profion["problem"] = (
        ("serchog", "caliog"),
        ("hynny", "Gymru"),
        ("caniatâd", "adeilad"),
        ("helynt", "gwynt"),
        ("ddôr", "agor")
    )

    for key in [
        "odlau_cyflawn",
        "odlau_llafarog",
        "proestau_cyflawn",
        "proestau_llafarog",
        # "odlau_llusg",
        # "odlau_llusg_cudd",
        # "odlau_llusg_ewinog",
        # "trwm_ac_ysgafn",
        "problem",
    ]:
        print("==============================")
        print(key.upper())
        print("==============================")
        for prawf in profion[key]:

            if len(prawf) == 2:
                rhaniad = Rhaniad([
                    Corfan([Gair(prawf[0])]),
                    Corfan([Gair(prawf[1])]),
                ])
            elif len(prawf) == 3:
                rhaniad = Rhaniad([
                    Corfan([Gair(prawf[0]), Gair(prawf[1])]),
                    Corfan([Gair(prawf[2])]),
                ])
            else:
                print('err: dau neu dri gair yn unig fan hyn.')

            # pwysig!!
            se = Seinyddwr()
            se.seinyddio(rhaniad)

            x = rhaniad[0][0]
            y = rhaniad[1][-1]

            if len(prawf) == 2:
                print("{}/{}".format(x, y))               
                print("{}/{}".format(x.sain(), y.sain()))
            else:
                print("{}+{}/{}".format(x, x.nesaf(), y))
                print("{}+{}/{}".format(x.sain(), x.nesaf().sain(), y.sain()))

            odlau = Odlau()

            if key in [
                "odlau_llusg",
                "odlau_llusg_cudd",
                "odlau_llusg_ewinog",
                "trwm_ac_ysgafn"
            ]:
                odlau = prawf_odl(x, y, llusg=True, trwm_ac_ysgafn=True)
            
            elif key in [
                "proestau_cyflawn",
                "proestau_llafarog",
            ]:
                odlau = prawf_odl(x, y, proest_ok=True)
            
            elif key in ["problem"]:
                odlau = prawf_odl(x, y, trwm_ac_ysgafn=False)
            
            else:
                odlau = prawf_odl(x, y)

            # show
            if odlau and odlau.dosbarth:
                print(beiro.cyan(odlau.dosbarth))
                print(odlau)
            else:
                print(beiro.coch('XXX'))
            print("--------------------")

            # odlau = prawf_odl_newydd(x, y)
            # if odlau and odlau.dosbarth:
            #     print(beiro.magenta(odlau.dosbarth))
            #     print(odlau)
            # else:
            #     print(beiro.coch('XXX'))
            print("--------------------")

    return


def main2():
    data = [
        ('car', 'dar'),     # odl (cyfatebiaeth gyflawn)
        ('car', 'cor'),     # proest (hanner odl)
        ('car', 'cat'),     # generig
        ('car', 'con'),     # dim
    ]

    for s, t in data:
        print(s, '/', t)
        x = Gair(s)
        y = Gair(t)
        codas_hafal = prawf_codas(x, y)
        print(codas_hafal)
        dosb_cnew = prawf_cnewyll(x, y)
        print(dosb_cnew)
        print('----------')


if __name__ == "__main__":
    main()
