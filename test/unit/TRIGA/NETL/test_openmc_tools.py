import pytest
from progression_problems.TRIGA.NETL.geometry_specs import TRIGA

def test_progression_problem_1():
    triga = TRIGA()
    assert triga is not None