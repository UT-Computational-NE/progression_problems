import os
import pytest

from progression_problems.TRIGA.fuel_element import FuelElement
from progression_problems.TRIGA.NETL.default_materials import DefaultMaterials as NETLDefaultMaterials
import progression_problems.TRIGA.NETL.problem_1_utils as problem_1_utils


@pytest.fixture
def fuel():
    return FuelElement()

@pytest.fixture
def coolant():
    return NETLDefaultMaterials.water()


def test_problem_1_openmc_tools(fuel, coolant):
    model = problem_1_utils.build_openmc_model(fuel, coolant)
    assert model is not None


def test_problem_1_mpact_tools(fuel, coolant):
    problem_1_utils.write_mpact_input(fuel, coolant, "xs_library.txt")
    assert os.path.exists("mpact.inp")
    os.remove("mpact.inp")