# prawf_llinell.py
"""
Dulliau darganfod cynghanedd mewn `Llinell`.

Os yw'r gynghanedd yn bengoll ac yn rhan o bennill, mae
`datryswr_pennill` yn profi'r linell nesaf am TOB/TOD/TOH

"""

from ceibwr.gair import Gair
from ceibwr.llinell import Llinell
from ceibwr.rhaniad import Trychwr

from ceibwr.datryswr_cynghanedd import (
    prawf_cynghanedd,
    chwynnu,
    best_guess,
)

from ceibwr.cysonion import gogwyddeiriau

from ceibwr.corfan import Corfan
from ceibwr.datrysiad import Amwys
from ceibwr.seinyddwr import Seinyddwr

import logging
log = logging.getLogger(__name__)


def datryswr_llinell(llinell, unigol=True, pengoll=False):
    '''
    input: `Llinell`
    output:
        - datrysiad os yw unigol=True
        - rhestr o ddatrysiadau fel arall
    '''

    # type check
    if type(llinell) is not Llinell:
        raise ValueError("Mae angen `Llinell` fan hyn, nid {}.".format(type(llinell)))

    # double check
    if not all([type(x) is Gair for x in llinell.children]):
        raise TypeError("Mae angen `list` o wrthrychau `Gair` fan hyn")

    se = Seinyddwr()
    se.seinyddio_llinell(llinell)

    tr = Trychwr()
    rhaniadau = tr.rhaniadau(llinell.children)

    # datrysiadau
    datrysiadau = []
    for rhaniad in rhaniadau:
        # print('rh:', repr(rhaniad))

        # hepgor gogwyddeiriau ar yr orffwysfa
        if any([str(rhan[-1]).lower() in gogwyddeiriau for rhan in rhaniad]):
            continue

        datrysiad = prawf_cynghanedd(rhaniad, pengoll=pengoll)
        # print('dat:', datrysiad.dosbarth)
        
        datrysiadau.append(datrysiad)

    datrysiadau = chwynnu(datrysiadau, dileu_gwreiddgoll=True)

    # dim byd
    if not datrysiadau:
        datrysiadau = [Amwys([Corfan(llinell.children)])]

    if unigol:
        return best_guess(datrysiadau, cyfuno=False)
    

    return datrysiadau


# ------------------------------------------------
# test
def main():

    from ceibwr.seinyddwr import Seinyddwr
    from ceibwr.beiro import Beiro
    from ceibwr.profion_llinell import profion
    from ceibwr.cysonion import colormaps

    cmap = colormaps['default']
    se = Seinyddwr()
    beiro = Beiro()

    profion['problem'] = (
        # "Canlyniad cariad yw cosb",
        # "Awdur mad a dramodydd",
        # "Ni chaf un haf o afiaith"
        # "Ym mhob byw y mae pawen",
        # "Y cawr mawr yn curo myrdd",
        # "Myn Pedr, heb na chledr na chlwyd",
        # "Aderyn llwyd ar un llaw",
        # "Ni all lladd ond ennyn llid",
        # "Gwynt y rhew yn distewi",
        # "Eu plaid yw duw rhai drwyu hoes",  # dwyochrog?
        # "Eu plaid yw duw rhaid rwyu hoes",  # alt
        # "Nid â dy gariad o gof",
        # "Boch goch gain rhiain rywiog",
        # "y deuwn a diolch",
        "Ymysg y bedw yn ddedwydd",  # w-gytsain
        "Â Brutus ap Sylus wyf",
        # "Ont tent gwraig, tu hwnt i Gred.",
        # "er pan rodded trwydded trwch,",
        # "Gardd lysau'r gerdd luosawg,",
        # "Eos Aled is olew;",
        # "O chuddiwyd ei chywyddawl!",
        "Os gwir rhoi - nid ysgar rhew -",
        # "I wlad nef eled, yn iach!",
        # "Deunaw oed yn ei hyder, - deunaw oed",
        "Deunaw oed yn ei hyder, deunaw oed",
        # "ddaw yn hardd i ardd yr hydd",
        "O luoedd Ei welïau;",
        "Dewi gâr, lle dug urael,",
        "ac i gymuned o gamau unig.",
        "A'i dylwyth yn wyth neu naw",
        "A’i cheraint a’i chwiorydd:",
        "Ym mhob marchnad, trefniad drwg,",
        "Y brawd o bellafion bro",
        "Ar wely’r ferch; alar fu.",
        # "Wedi cysgu, tru tremyn",
        # "Cyffredin, a gwin a gawn.",
        # "Canfod rhiain addfeindeg",
        # "Prynu rhost, nid er bostiaw,",
        # "Pan elai y minteioedd",
        "I'm hôl, fo'i clywid ymhell",
        "A gorau gair gan Fair fu.",
        "Cymryd, balch o febyd fum,",  
        # "Cyffredin, a gwin a gawn.",  # proest
        "fy nyn gan mewn llan a llys,",
    )

    profion['problem_seinyddio'] = (
        # heb seinego ar draws yr atalnod (brig, gwraidd)
        "Bwrw cerdd bêr, brig, gwraidd a bôn;",
        # wedi seinego "byd heb" -> "byt heb"
        "Bid y brud a'r byd heb wres,",
        "Pob serchog caliog a’m cais,",
        "A’i ’sgyrsio ymysg gorsedd",
    )

    profion['pengoll'] = (
        "Wele rith fel ymyl rhod o'n cwmpas",
        "Rhwydd gamwr hawdd ei gymell - i'r bryniau",
        "Oriau ei dyddiau diddig - a dreuliodd",
        "Talog, boed law, boed heulwen, - y saif hi",
        "Mab Rhys aeth o'i lys i lawr - yr  Erwig:",
        "Dan oer hin yn dwyn y rhaw - mewn trymwaith",
        "Ac yn nyfnder y weryd - gwn y caf",
    )

    for key in [
            # 'croes',
            # 'traws',
            # 'llusg',
            # 'sain',
            # 'croes_o_gyswllt',
            # 'sain_o_gyswllt',
            # 'sain_gadwynog',
            # 'trychben',
            # 'cysylltben',
            # 'traws_fantach',
            # 'llusg_lafarog',
            # 'llusg_gudd',
            # 'llusg_ewinog',
            # 'sain_gudd', 
            # 'sain_ewinog',
            # 'sain_lafarog',
            # 'seingroes',
            # 'trawsgroes',
            # 'seindraws',
            # 'croeslusg',
            # 'seinlusg',
            # 'trawslusg',
            # 'llusg_deirodl',
            # 'sain_deirodl',
            # 'sain_ddwbl',
            # 'misc',
            # 'sain_siwr',
            # 'problem',
            # 'aberteifi',
            # 'randoms',
            # 'prawf_me',
            # 'prawf_metoo',
            # 'ac_nid_ag',
            # 'sicr_wallus',
            # 'posib_wallus',
            # 'problem_seinyddio',
            # 'pengoll',
            'problem',
            # 'pengoll',
    ]:

        print('\n\n==============================')
        print('***', key.upper(), '***')
        print('==============================')
        for s in profion[key]:

            llinell = Llinell(s)
            # print(repr(llinell))
            se.seinyddio(llinell)
            # print(llinell.sain())
             
            # datrys
            dat = datryswr_llinell(llinell, pengoll=True)

            # show
            print()
            # print(dat.sain())
            print(dat.show_fancy(toriad='|', cmap=cmap))
            print(beiro.cyan(dat.dosbarth) if dat.dosbarth else beiro.coch('XXX'))
            print('----------')
    return None


if __name__ == '__main__':

    main()
