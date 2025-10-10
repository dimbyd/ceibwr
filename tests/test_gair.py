# test_gair.py

import pytest
from ceibwr.gair import Gair
from ceibwr.seinyddwr import Seinyddwr

se = Seinyddwr()

test_inputs = [
    # cyffredin
    ("prydferth", 2),
    ("dramodydd", 3),
    ("cuddio", 2),
    ("rhôm", 1),
    ("â'th", 1),
    # deuseiniaid
    ("dedwydd", 2),
    ("ymadael", 3),
    ("anifeiliaid", 4),
    ("yw", 1),
    # deusain ddeusill
    ("duon", 2),
    ("eos", 2),
    ("suo", 2),
    # lluosill acennog
    ("cymraeg", 2),
    ("cangarŵ", 3),
    ("ffarwél", 2),
    ("dyfalbarhau", 4),
    ("dyfalbarhad", 4),
    # w-gytsain
    ("awen", 2),
    ("llawen", 2),
    ("bywyd", 2),
    # w-gytsain yn olaf
    ("berw", 2),
    ("pitw", 2),
    # w-gytsain gwr, gwl
    ("gwaith", 1),
    ("gwledd", 1),
    ("wledd", 1),
    ("gwrandawiad", 3),
    ("wrandawiad", 3),
    ("gwrando", 2),
    ("gwr", 1),
    ("gwrhydri", 3),
    ("gŵr", 1),
    ("gwrthod", 2),
    # w-gytsain ar y diwedd
    ("berw", 2),
    ("bedw", 2),
    ("llw", 1),
    ("pitw", 2),  # eithriad
    # triawd talgron-talgron (T-T)
    ("haleliwia", 4),
    ("anifeiliaid", 4),
    ("piwis", 2),
    ("gwiw", 1),
    # triawd talgron-lleddf (T-LL)
    ("iaith", 1),
    ("gwaith", 1),
    ("genwair", 2),
    # triawd lleddf-talgron (LL-T)
    ("awen", 2),
    ("distewi", 3),
    ("gwiw", 1),
    ("wiw", 1),
    ("piwis", 2),
    ("distewi", 3),
    # triawd lleddf-lleddf (LL-LL)
    ("gloyw", 2),
    ("gwrandawiad", 3),
    ("glawio", 2),
    ("gloywi", 2),
    # pedwarawd
    ("ieuanc", 2),
    # amrywiol
    ("daear", 2),
    ("ffiniau", 2),
]


@pytest.mark.parametrize("test_input", test_inputs)
def test_nifer_sillafau(test_input):
    x, y = test_input
    z = Gair(x)
    se.seinyddio_gair(z)
    assert z.nifer_sillafau() == y
