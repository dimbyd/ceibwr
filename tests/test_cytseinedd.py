# test_cytseinedd.py
import pytest
from ceibwr.gair import Gair
from ceibwr.corfan import Corfan
from ceibwr.datryswr_cytseinedd import prawf_cytseinedd
from ceibwr.seinyddwr import Seinyddwr

profion = [
    # croes
    ("Mae llyn hen", "i'm llawenhau", "CRO"),
    ("Y llwybrau gynt", "lle bu'r gan", "CRO"),
    ("Am eu hawr", "yn ymaros", "CRO"),
    ("Si'r oerwynt", "a sêr araul", "CRO"),
    # traws
    ("Ochain cloch", "a gwreichion clir", "TRA"),
    ("Hen derfyn", "nad yw'n darfod", "TRA"),
    ("Ei awen brudd", "dan ein bro", "TRA"),
    # traws_fantach
    ("Y brawd", "o bellafion bro", "TFA"),
    ("Brwd", "yw aderyn brig", "TFA"),
    # croes_o_gyswllt
    ("Aderyn llwyd", "ar un llaw", "COG"),
    ("Daw geiriau duw", "o'i gaer deg", "COG"),
    ("Ewch o'r Llew Coch", "i'r lle cudd", "COG"),
    ("Rhaid y car", "ydyw cyrraedd", "COG"),
    ("Actau ieuanc", "dyhewyd", "COG"),
    # croes_o_gyswllt_gymhleth
    ("Hawdd yw cyrraedd", "y cyrion", "COG"),
    ("Ysgweier llesg", "ar y llawr", "COG"),
    ("Y ferch ofer", "ei chyfoeth", "COG"),
    ("Gwelais y glew", "is y glyn", "COG"),
    ("Drwg ydyw'r gwae", "o dir gwyllt", "COG"),
    ("Trist ŵr trosto", "o'r trawster", "COG"),
    # trychben
    ("Canu mydr", "cyn ymadael", "TRA"),
    ("Nid yn aml", "y down yma", "TRA"),
    ("Ond daw gwefr", "cyn atgofion", "TRA"),
    ("ei hofn", "hefyd", "CRO"),
    # cysylltben
    ("Yma bu", "nwyf i'm beunydd", "TRA"),
    ("Onid bro", "dy baradwys", "CRO"),
    ("A ddaw", "fy mab i Ddyfed", "TFA"),
    ("gwae", "nid gweniaith", "TFA"),
    # dau-yn-ateb-un
    ("Ni rannodd", "yn yr einioes", "CRO"),
    ("Ar warrau", "eryrod", "CRO"),
    ("Fel y cawn", "afal cynnar", "CRO"),
    ("Mae eryr llwyd", "am wyr llen", "CRO"),
    # caledu
    ("Rhwbio pridd", "ar bob brawddeg", "CRO"),
    ("Ond daw gwefr", "cyn atgofion", "TRA"),
    ("Oedd enwog gynt", "heb ddwyn cas", "TRA"),
    ("Aeron per", "ei hwyneb hi", "COG"),
    ("Onid hoff", "yw cofio'n taith", "TRA"),
    ("Meurig hir,", "mawr y carwn", "CRO"),
    ("Pren a ddwg", "bob rhinwedd dda", "TRA"),
    ("Ni bu trist", "yn y byd rhydd", "CRO"),
    ("A fo cryf", "a fag rhyfel", "CRO"),
    # meddalu
    ("Acw drwy gwymp", "Ector gynt", "CRO"),  # c+t > c+d
    # ("Eich tadau", "oedd i'ch deudir", "TRA"),  # ch+t > ch+d
    # ("Crefft rwydd", "i gadw corff draw", "TRA"),  # ff+t > ff+d
    # ("Dy wallt aur", "i dwyllo dyn", "CRO"),  # ll+t > ll+d
    ("Crist a roed", "i ddwyn croes drom", "TRA"),  # s+t > s+d
]


@pytest.mark.parametrize("test_input", profion)
def test_cytseinedd(test_input):
    se = Seinyddwr()
    a = Corfan([Gair(x) for x in test_input[0].split()])
    b = Corfan([Gair(x) for x in test_input[1].split()])
    se.seinyddio(a)
    se.seinyddio(b)
    cyts = prawf_cytseinedd(a, b)
    assert cyts.dosbarth == test_input[2]
