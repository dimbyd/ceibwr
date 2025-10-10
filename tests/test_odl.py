# test_cytseinedd.py
import pytest
from ceibwr.gair import Gair
from ceibwr.datryswr_odl import prawf_odl

profion_odl = [
    ("beic", "haul", None),
    ("buwch", "rhyfedd", None),
    # odlau_cyflawn
    ("cath", "math", "ODL"),
    ("pren", "llen", "ODL"),
    ("mafon", "duon", "ODL"),  # deusain ddwbl
    ("calon", "creulon", "ODL"),
    ("gwlad", "cariad", "ODL"),
    ("galwad", "cariad", "ODL"),  # dwy ddeusiain talgron
    ("wiwd", "liwd", "ODL"),
    ("croes", "oes", "ODL"),
    # odlau_llafarog
    ("tro", "llo", "OLA"),
    ("cadno", "banjo", "OLA"),
]

profion_odl_lusg = [
    ("beiddgar", "cariad"),
    ("morfudd", "cuddio"),
    ("tawel", "heli"),
]


@pytest.mark.parametrize("test_input", profion_odl)
def test_odl(test_input):
    odl = prawf_odl(Gair(test_input[0]), Gair(test_input[1]))
    assert odl.dosbarth == test_input[2]


@pytest.mark.parametrize("test_input", profion_odl_lusg)
def test_odl_lusg(test_input):
    odl = prawf_odl(Gair(test_input[0]), Gair(test_input[1]), llusg=True)
    assert odl.dosbarth in ['OLU', 'OLL']
