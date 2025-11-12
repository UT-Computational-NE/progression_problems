import pytest
import progression_problems.TRIGA.NETL as TRIGA

def test_progression_problem_1():
    triga = TRIGA.Reactor()
    assert triga is not None