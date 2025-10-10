# test_nod.py
from ceibwr.nod import Nod


def test_gofod():
    nod = Nod(" ")
    assert nod.is_bwlch() is True


def test_atalnod():
    nod = Nod(";")
    assert nod.is_atalnod() is True
