import os
import pytest

import progression_problems.TRIGA as TRIGA
import progression_problems.TRIGA.NETL as NETL
from progression_problems.TRIGA.NETL.default_materials import DefaultMaterials as NETLDefaultMaterials
from progression_problems.TRIGA.NETL import problem_1_utils, problem_2_utils


@pytest.fixture
def fuel_element():
    return TRIGA.FuelElement()

@pytest.fixture
def graphite_element():
  return TRIGA.GraphiteElement()

@pytest.fixture
def central_thimble():
  return NETL.CentralThimble()

@pytest.fixture
def transient_rod():
  def factory(fraction_withdrawn:float = 0.0):
    return NETL.TransientRod(fraction_withdrawn=fraction_withdrawn)
  return factory

@pytest.fixture
def fuel_follower_control_rod():
  def factory(fraction_withdrawn:float = 0.0):
    return NETL.FuelFollowerControlRod(fraction_withdrawn=fraction_withdrawn)
  return factory

@pytest.fixture
def coolant():
    return NETLDefaultMaterials.water()


def test_problem_1_openmc_tools(fuel_element, coolant):
    model = problem_1_utils.build_openmc_model(fuel_element, coolant)
    assert model is not None


def test_problem_1_mpact_tools(fuel_element, coolant):
    problem_1_utils.write_mpact_input(fuel_element, coolant, "xs_library.txt")
    assert os.path.exists("mpact.inp")
    os.remove("mpact.inp")


def test_problem_2_openmc_tools(fuel_element, graphite_element, central_thimble,
                                transient_rod, fuel_follower_control_rod,
                                coolant):

    elements = [None, graphite_element, central_thimble,
                transient_rod(fraction_withdrawn=0.0),
                transient_rod(fraction_withdrawn=1.0),
                fuel_follower_control_rod(fraction_withdrawn=0.0),
                fuel_follower_control_rod(fraction_withdrawn=1.0)]

    for element in elements:
        model = problem_2_utils.build_openmc_model(fuel_element, coolant, element)
        assert model is not None


def test_problem_2_mpact_tools(fuel_element, graphite_element, central_thimble,
                               transient_rod, fuel_follower_control_rod,
                               coolant):

    elements = [None, graphite_element, central_thimble,
                transient_rod(fraction_withdrawn=0.0),
                transient_rod(fraction_withdrawn=1.0),
                fuel_follower_control_rod(fraction_withdrawn=0.0),
                fuel_follower_control_rod(fraction_withdrawn=1.0)]

    for element in elements:
        problem_2_utils.write_mpact_input(fuel_element, coolant, element, "xs_library.txt")
        assert os.path.exists("mpact.inp")
        os.remove("mpact.inp")
