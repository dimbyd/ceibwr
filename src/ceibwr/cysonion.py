# cysonion.py (constants)
"""
Diffiniadau sylfaenol.

Cysonion = constants
nodau:		llafariaid, cytseiniaid, atalnodau, deuseiniaid,
cytseinedd: cyfuniadau caled, meddal, trychben, cysylltben, ...
odl: 		cyfuniadau gwyrdro
dosbarthu:	aceniad, cytseinedd, odl, cynghanedd etc.

and many more ...

"""

from copy import copy

# ------------------------------------------------
# lliwiau
# mae'n gwneud synnwyr bod 
# 1. nodau cysylltben yr un lliw a gefyll
# 2. nodau trychben yr un lliw a nodau traws/canolgoll
# ------------------------------------------------
colormaps = {
    'default': {
        "odlau": "c",
        "odlau_mewnol": "g",
        "odlau_cyrch": "y",
        "GEF": "m",  # gefelliaid
        "TRA": "b",  # nodau traws
        "TRB": "b",  # nodau trychben
        "CYB": "m",  # nodau cysylltben
        "CYS": "r",  # nodau cyswllt
        "GWG": "y",  # nodau gwreiddgoll
        "PEG": "",  # nodau pengoll
        "TOR": "g",  # toriad
    }
}

# ------------------------------------------------
# seinegolion (ipa)
# ------------------------------------------------
ipa_cyts = (
    ('b', 'b'),     # bach, cwbl, mab
    ('d', 'd'),     # dydd, cadw, tad
    ('j', 'dʒ'),    # joio, garej, diengyd
    ('dd', 'ð'),    # ddoe, deuddeg, bedd
    ('ff', 'f'),    # ffenest, ei phen, cyffro, corff
    ('g', 'ɡ'),     # glân, cegin, cig
    ('h', 'h'),     # haul, gwahanol
    ('i', 'j'),     # iaith, geiriadur
    ('c', 'k'),     # cig, acw, ac
    ('l', 'l'),     # leicio, Alban, bol
    ('ll', 'ɬ'),    # llaw, cyllell
    ('m', 'm'),     # mab, cymaint, dim
    ('mh', 'm̥'),    # fy mhen, ym Mhen-y-bont
    ('n', 'n'),     # nerth, anadlu, gwyn
    ('nh', 'n̥'),    # fy nhad, yn Nhywyn
    ('ng', 'ŋ'),    # fy ngwely, trengi, rhwng
    ('ngh', 'ŋ̊'),   # fy nghŵn, yng Nghymru
    ('p', 'p'),     # pen, copa, map
    ('r', 'r̥'),     # radio, garw, dŵr
    ('rh', 'r'),    # rhestr, anrheg
    ('s', 's'),     # Saesnes, swsus
    ('sh', 'ʃ'),    # siarad, siop, brwsh
    ('si', 'ʃ'),    # siarad, siop, brwsh
    ('t', 't'),     # tatws, at
    ('tsh', 'tʃ'),  # tsips, wats
    ('th', 'θ'),    # thus, athro, peth
    ('f', 'v'),     # faint, afal, arf
    ('w', 'w'),     # wedyn, ei wraig, gwlân
    ('ch', 'χ'),    # chwaer, tuchan, bwlch
    ('-', '|'),     # hack
)

ipa_llaf = (
    ('a', 'a'),     # sant, pàs
    ('â', 'aː'),    # mab, sâl
    ('e', 'ɛ'),     # perth, mès
    ('ê', 'eː'),    # peth, trên
    ('i', 'ɪ'),     # tipyn, sgìl
    ('î', 'iː'),    # hir, tîm
    ('ï', 'iː'),    # gwnïo
    ('o', 'ɔ'),     # bron, glòs
    ('ô', 'oː'),    # bro, ôl
    ('u', 'ɨ'),     # punt, gwyn
    ('û', 'ɨː'),    # llun, bûm, rhy, pur
    ('w', 'ʊ'),     # cwm, mẁg
    ('ŵ', 'uː'),    # cwch, dŵr
    ('y', 'ə'),     # cymydog, rỳg
    ('ŷ', 'ɨ'),     # tŷ
)

# ipa deuseiniaid
ipa_deus = (
    ('ai', 'ai'),   # tai (LL2)
    ('au', 'aɨ'),   # cau, dau, nesáu (LL3)
    # ('ae', 'aːɨ'),  # hael, cae (LL2)
    ('ae', 'aːi'),  # Cymraeg, aelod (LL2)
    ('aw', 'au'),   # llaw, awdur (LL1)
    ('ew', 'ɛu'),   # llew (LL1)
    ('ei', 'ɛi'),   # reis, beic (LL2)
    ('eu', 'eɨ'),   # gwneud (LL3)
    ('yw', 'əu'),   # bywyd, unigryw (LL1)
    ('iw', 'ɪu'),   # lliw (T)
    ('uw', 'ɨu'),   # Duw, menyw (LL1)
    ('oi', 'ɔi'),   # troi (LL2)
    ('ou', 'ɔɨ'),   # ???
    ('ow', 'ɔu'),   # rownd (LL1)
    ('oe', 'ɔɨ'),   # coeden (LL2)
    ('wy', 'ʊɨ'),   # mwy, gŵyl, wyth (LL2)
)

# aloffonau deheuol
ipa_llaf_de = (
    ('u', 'ɪ'),
    ('û', 'iː'),
    ('ŷ', 'ɪ'),
)
ipa_deus_de = (
    ('au', 'ai'),   # cau, nesáu, dau (de: tai)
    ('ae', 'ai'),   # hael, cae = tai
    ('eu', 'ɛi'),   # gwneud = reis
    ('uw', 'ɪu'),   # duw = lliw
    ('oe', 'ɔi'),   # coeden = troi
    ('wy', 'ʊi'),   # gwyl = gwyil
)

# symbol prifacen (primary stress)
ipa_prifacen = "ˈ"

# symbol isacen (secondary stress)
ipa_isacen = "ˌ"

ipa_all = ipa_cyts + ipa_llaf + ipa_deus
ipa_lookup = {ipa[0]: ipa[1] for ipa in ipa_all}

# Dyma'r "scale of vowels" honedig
# Heb ei ddefnyddio hyd yma
graddfa_llafariaid = [
    'iː',  # key
    'eɪ',  # cane
    'aɪ',  # kite
    'ɪ',   # kit
    'ɛ',   # ken
    'æ',   # cat
    'ɝː',  # cur
    'ʌ',   # cut
    'ɑː',  # cot, car
    'aʊ',  # cow
    'ɔɪ',  # coy
    'ɔː',  # caught, core
    'ʊ',   # could
    'oʊ',  # coat
    'uː',  # cool, cute
]

# ------------------------------------------------
# nodau
# ------------------------------------------------
str_atalnodau = ",.'\"\\/!?-;:_@()*^%~{}[]+=|’£–‘‑’"  # inc. alt-apostrophe
str_cytseiniaid_base = "b,c,ch,d,dd,f,ff,g,ng,h,j,l,ll,m,n,p,ph,r,rh,s,t,th"
str_cytseiniaid_ext = "ngh,mh,nh,sh,tsh,k,q,v,x,z"
str_cytseiniaid = ','.join([str_cytseiniaid_base, str_cytseiniaid_ext])
str_cytseiniaid_upper = "Ch,Dd,Ff,Ng,Ll,Mh,Nh,Ngh,Ph,Rh,Sh,Tsh,Th"
# str_llafariaid_byrion = "aeiouwyà"
str_llafariaid_byrion = "aeiouwy"
str_llafariaid_hirion = "âáäêéëîïöôûúŵẃŷý"

atalnodau = list(str_atalnodau)
cytseiniaid = str_cytseiniaid.rsplit(",")
cytseiniaid += str_cytseiniaid.upper().rsplit(",")
cytseiniaid += str_cytseiniaid_upper.rsplit(",")
llafariaid_byrion = list(str_llafariaid_byrion + str_llafariaid_byrion.upper())
llafariaid_hirion = list(str_llafariaid_hirion + str_llafariaid_hirion.upper())
llafariaid = llafariaid_byrion + llafariaid_hirion

# deuseiniaid?

# ------------------------------------------------
# deuseiniaid
# ------------------------------------------------
deuseiniaid = {
    "hiatus": [
        "ao",  # parhaol
        "ea",  # eang, deallwn
        "eo",  # eos
        "oa",  # ffoadur
        "uo",  # duon
        "eë",  # amgaeëdig
        "ïa",  # pïau
        "ïo",  # gwnïo
        "üw",  # düwch
        "ŵa",  # dŵad, pŵer
        "ya",  # lletya, mwyar
    ],
    "talgron": [
        "ia",  # cariad
        "ie",  # colier
        "io",  # cerfio, diolch?, chwiorydd?
        "iw",  # cerfiwr (* hefyd yn lleddf: lliw)
        "iy",  # faliym
        "ua",  # ieuanc
        "wa",  # gwan
        "we",  # gweld
        "wi",  # gwin
        "wo",  # gweddwon
        "wu",
        # "wy",  # gwyn (* wy dalgron *)
        "yu",  #
    ],
    "lleddf_cyntaf": [
        "aw",  # llaw, siawns
        "ew",  # llew
        "iw",  # lliw (* hefyd yn dalgron: cerfiwr *)
        "ow",  # bowns
        "uw",  # buwch, Duw, byw (y-olau)
        "yw",  # bywyd (y-dywyll)
    ],
    "lleddf_ail": [
        "ai",  # tai, pais
        "ae",  # hael, cae, paent, Cymraeg
        "ei",  # seisnig, peint, eira
        "oe",  # croen
        "oi",  # troi
        "wy",  # cwyn (* wy leddf *) - angen unicode!
    ],
    "lleddf_trydydd": [
        "au",  # cau, nesau, paun
        "eu",  # gwneud, gweu
        "ey",  # teyrn
        "ou",  # ymarhous
        "oy",  #
    ],
    "eraill": [
        "ay", "ue", "uy", "yu", "ye", "ii",
        "yo", "oo", "aa", "iu", "yy", "ui", "uu",
    ],
}

dosbarth_deusain = dict([(z, key) for key in deuseiniaid.keys() for z in deuseiniaid[key]])
deuseiniaid["lleddf"] = copy(deuseiniaid["lleddf_cyntaf"])
deuseiniaid["lleddf"] += copy(deuseiniaid["lleddf_ail"])
deuseiniaid["lleddf"] += copy(deuseiniaid["lleddf_trydydd"])

# dosbarthiadau aceniad, odl, cytseinedd, cynghanedd ayb)
llythrenwau = {
    "dim": "Amwys",
    "cytsain": {
        "GEF": "Gefell",
        "GWG": "Gwreiddgoll",
        "CAN": "Canolgoll",
        "TRA": "Traws",
        "CYS": "Cyswllt",
        "PEN": "Pengoll",
        "TRB": "Trychben",
        "CYB": "Cysylltben",
    },
    "cynghanedd": {
        # null
        None: "Amwys",
        "GWA": "Gwallus",
        "LLA": "Llafarog",
        # croes
        "CRO": "Croes",
        "COG": "Croes o Gyswllt",
        # traws
        "TRA": "Traws",
        "TFA": "Traws Fantach",
        # llusg
        "LLU": "Llusg",
        "LLL": "Llusg Lafarog",
        "LLD": "Llusg Deirodl",
        # sain
        "SAI": "Sain",
        "SAL": "Sain Lafarog",
        "SOG": "Sain o Gyswllt",
        "SAG": "Sain Gadwynog",
        "SAD": "Sain Deirodl",
        "SDD": "Sain Ddwbl",
        # cymysg
        "SEG": "Seingroes",
        "SED": "Seindraws",
        "SEL": "Seinlusg",
        "TRG": "Trawsgroes",
        "TRL": "Trawslusg",
        "CRL": "Croeslusg",
        # gwreiddgoll
        "CWG": "Croes Wreiddgoll",
        "TWG": "Traws Wreiddgoll",
        # pengoll
        "CBG": "Croes Bengoll",
        "TBG": "Traws Bengoll",
        "LBG": "Llusg Bengoll",
        "SBG": "Sain Bengoll",
    },
    "acen": {
        "ACE": "Acennog",
        "DIA": "Diacen",
    },
    "aceniad": {
        "CAC": "Cytbwys Acennog",
        "CDI": "Cytbwys Ddiacen",
        "AAC": "Anghytbwys Acennog",
        "ADI": "Anghytbwys Ddiacen",
    },
    "odl": {
        "ODL": "Cyflawn",
        "OLA": "Llafarog",
        "OLU": "Llusg",
        "OLL": "Llusg Lafarog",
        "OGY": "Odl Gyrch",
        "PGY": "Proest",
        "PLA": "Proest Lafarog",
    },
    "cwpled": {
        "CWP": "Cwpled",
        "CCA": "Cwpled Caeth",
        "CC4": "Cwpled Cywydd Bedairsill",
        "CC7": "Cwpled Cywydd Seithsill",
        "CAG": "Cwpled Awdl Gywydd",
        "TOD": "Toddaid",
        "TOB": "Toddaid Byr",
        "TOH": "Toddaid Hir",
        "CHF": "Cyhydedd Fer",
        "CHH": "Cyhydedd Hir",
        "CHN": "Cyhydedd Nawban",
    },
    "mesur": {
        "AWD": "Awdl",

        "EUU": "Englyn Unodl Union",
        "ECR": "Englyn Crwca",
        "EMI": "Englyn Milwr",
        "EPF": "Englyn Penfyr",
        "ECY": "Englyn Cyrch",
        "EPE": "Englyn Pendrwm",
        "ETO": "Englyn Toddaid",

        "CDF": "Cywydd Deuair Fyrion",
        "CDH": "Cywydd Deuair Hirion",

        "CY9": "Cyhydedd Nawban",
        "CYF": "Cyhydedd Fer",
        "CYH": "Cyhydedd Hir",

        "RHB": "Rhupunt byr",
        "RHH": "Rhupunt hir",

        "GWB": "Gwawdodyn Byr",
        "GWH": "Gwawdodyn Hir",

        "BAT": "Byr a Thoddaid",
        "HAT": "Hir a Thoddaid",
    },
    "bai": {
        "TWY": "Twyll gynghanedd",
        "GOR": "Gormod o odl",
        "PRO": "Proest i'r odl",
        "CRY": "Crych a llyfn",
        "TRW": "Trwm ac ysgafn",
        "LLE": "Lleddf a thalgron",
        "TWO": "Twyll odl",
        "GWE": "Gwestodl",
        "DYB": "Dybryd sain",
        "RHY": "Rhy debyg",
        "YMS": "Ymsathr odlau",
        "HAN": "Hanner proest",
        "CAM": "Camacennu",
        "LLY": "Llysiant llusg",
        "CAG": "Camosodiad gorffwysffa",
        "CAR": "Carnymorddiwes",
        "TIN": "Tin ab",
        "TOR": "Tor mesur",
    },
}

# blaenoriaeth cynganeddion cymysg
blaenoriaeth = [
    'COG', 'SOG',
    'SDD', 'SAD', 'LLD',
    'SAI', 'CRO', 'LLU', 'TRA',
    'SAG',
    'SAL', 'LLL',
    'TFA',
    'CWG', 'TWG',
    'SBG', 'CBG', 'LBG', 'TBG',
    'SEG', 'SED', 'SEL', 'TRG', 'TRL', 'CRL',  
    None,
]

# gogwyddeiriau (clitics)
gogwyddeiriau = [
    # bannod (article)
    "y",
    "yn",
    "yr",
    # rhagenwau (pronouns)
    "fy",
    "dy",
    "di",
    "ei",
    "ein",
    "eich",
    "eu",
    # cysyllteiriau (conjunctions)
    "a",  # ond nid "â"
    "ac", "ag",
    "na", "nac", "nag",
    "neu",
    # minimis
    "o",
    "o,",
    "i",
    # arddodiadau
    "ar",
    "am",
    "at",
    # eraill
    "yn",
    "yw",
    "yw'r",
    "yw'n",
    # collnodau # TODO: mae angen trawsnewid collnodau i'r nod ASCII pan yn darllen ffeil
    "i’r",
    "i'r",
    "a'r",
    "a’r",
    "i'w",
    "i’w",
    "a'u",
    "a'm",
    "a'i",
    "o'r",
    "o'n",
    "O’r",
    "o'i",
    "o'th",
    "o’th",
    "i'm",
    "i’m",
    "o’r",
    "O’r",
]

# ychwanegu atalnodau i'r gogwyddeiriau (hack)
gogwyddeiriau += atalnodau

# llafariaid hir/ysgafn <-> llafariaid byr/trwm
hir2byr = {
    "â": "a",
    "á": "a",
    "ê": "e",
    "ë": "e",
    "é": "e",
    "î": "i",
    "ï": "i",
    "ô": "o",
    "û": "u",
    "ŵ": "w",
    "ŷ": "y",
    "â".upper(): "A",
    "á".upper(): "A",
    "ê".upper(): "E",
    "ë".upper(): "E",
    "î".upper(): "I",
    "ï".upper(): "I",
    "ô".upper(): "O",
    "û".upper(): "U",
    "ŵ".upper(): "W",
    "ŷ".upper(): "Y",
}

byr2hir = {
    'a': ['â', 'á'],
    'e': ['ê', 'ë', 'é'],
    'i': ['î', 'ï'],
    'o': ['ô'],
    'u': ['û'],
    'w': ['ŵ'],
    'y': ['ŷ'],
}

# caledu: b -> p, d -> t, g -> c
cyfuniadau_caled = {
    #
    ("b", "h"): ("p", "h"),
    ("b", "b"): ("p", "p"),
    ("b", "p"): ("p", "p"),
    ("p", "b"): ("p", "p"),
    #
    ("g", "h"): ("c", "h"),
    ("g", "g"): ("c", "c"),
    ("g", "c"): ("c", "c"),
    ("c", "g"): ("c", "c"),
    #
    ("d", "h"): ("t", "h"),
    ("d", "d"): ("t", "t"),
    ("d", "t"): ("t", "t"),
    ("t", "d"): ("t", "t"),
    #
    ("ff", "f"): ("ff", "ff"),
    ("ff", "f"): ("ff", "ff"),
    ("ll", "l"): ("ll", "ll"),
    # ("l", "ll"): ("ll", "ll"),
    ("th", "dd"): ("th", "th"),
    #
    ("g", "rh"): ("c", "r"),
    ("d", "rh"): ("t", "r"),
    ("b", "rh"): ("p", "r"),
}

# meddalu: p -> b, t -> d, c -> g
cyfuniadau_meddal = {
    ("s", "t"): "d",
    # ("s", "c"): "g",  # cwmpas/campwaith
    ("s", "p"): "b",
    ("c", "t"): "d",
    # ("ff", "t"): "d",
    # ("ll", "t"): "d",
    # ("ch", "t"): "d",
}

# cyfuniadau gwyrdro (rhaid i'r ei/eu fod yn yr ail odl)
cyfuniadau_gwyrdro = (
    ("aith", "eith"),
    ("ain", "ein"),
    ("aur", "eur"),
    ("au", "eu"),
)

# ------------------------------------------------
# cyfuniadau trychben (trych = truncated)
# ------------------------------------------------
cyfuniadau_trychben = (
    "br",
    "bl",
    "dr",
    "dl",
    "dn",
    "fl",
    "fn",
    "fr",
    "ffr",
    "ffl",
    "gr",
    "gl",
    "gn",
    "ls",
    "lm",
    "ml",
    "nt",
    "pl",
    "pr",
    "tl",
)

# mae angen trefnu rhain yn ol y ddeusain benodol
# Oes patrymau i'w gweld? e.e. hiatus yn 'ia' ac 'io' ar ôl 'd'
# TODO: cynnwys treigliadau yn awtomatig
# Noder bod treigliadau ond yn effeitio ar gyrch y sillaf cyntaf.
eithriadau = {
    "hiatus": (
        "dios",
        "diadell",
        "diofryd", "ddiofryd",
        "dianc", "ddianc",
        "diolch", "ddiolch",
        "dwad",
        "gweddio", "weddio",
        "gweddiwn", "weddiwn",
        'diarddel',
        "diod", "ddiod",
        "diodydd", "ddiodydd",
        "Llio",
        "mieri",
        "piod", "biod",
        "priod", "briod", "phriod",
        "priodfab", "briodfab", "phriodfab",
        "priodferch", "briodferch", "phriodferch",
        "tua", "tuag", "tua'r",
    ),
    "triawdau_deusill_x|yz": (
        "diau",
        "diwyd",
        "gweddiais", "weddiais",
        "rhiain", "riain",
        "triawd",
    ),
    "triawdau_deusill_xy|z": (
        "chwiorydd",
    ),
    # rhestr geiriau lluosill acennog
    "geiriau_lluosill_acennog": (
        "amen",
        "anabl",
        "apel",
        "caerdydd",
        "cangarŵ",
        "cymraeg",
        "dyfalbarhau",
        "erioed",
        "ffarwel",
        "gadewch",
        "gyrfaoedd",
        "iselhau",
        "llawenhau",
        "parhad",
        "ribidires",
        "ymhell",
        "ymysg",
    ),
    # rhestr geiriau gyda wy-dalgron/esgynedig
    # oes rheolau am rhain?
    # a fasai'n well rhestru geiriau wy-leddf/ddisgynedig?
    "wy-dalgron": (
        "dwyn",
        "llwyn",
        "mwyn",
        "nwy",
        "olwyn",
        "plwyf",
        "rhwydd",
        "swyn",
        "trwyn",
    ),
    'w-gytsain': (
        'gwraig', 'wraig', 'ngwraig',
        'gwragedd', 'wragedd',
        'gwlad', 'wlad', 'ngwlad',
        'gwledydd', 'wledydd', 'ngwledydd',
        'gwnaeth', 'wnaeth', 'ngwnaeth'
        'gwledd', 'wledd', 'ngwledd'
        'bedw', 'fedw',
        'berw', 'ferw',
        'gwna', 'wna',
        'gwneud', 'wneud', 'wnawn', 'wnes', 'wnest', 'wnaeth', 'wnaethom',
        'chwerwder',
        'gwraidd', 'gwreiddyn', 'gwreiddiau',
        'gwrando', 'gwrandawiad',
    )
}
