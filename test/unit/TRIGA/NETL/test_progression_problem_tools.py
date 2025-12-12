import os
import pytest

import progression_problems.TRIGA as TRIGA
import progression_problems.TRIGA.NETL as NETL
from progression_problems.TRIGA.NETL.default_materials import DefaultMaterials as NETLDefaultMaterials
from progression_problems.TRIGA.NETL import problem_1_utils, problem_2_utils, problem_4_utils


@pytest.fixture
def fuel_element():
    return TRIGA.DefaultGeometries.fuel_element()


@pytest.fixture
def graphite_element():
    return TRIGA.DefaultGeometries.graphite_element()


@pytest.fixture
def central_thimble():
    return NETL.DefaultGeometries.central_thimble()


@pytest.fixture
def transient_rod():
    return NETL.DefaultGeometries.transient_rod()


@pytest.fixture
def fuel_follower_control_rod():
    return NETL.DefaultGeometries.fuel_follower_control_rod()


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

    cases = [(None,                      False),
             (graphite_element,          False),
             (central_thimble,           False),
             (transient_rod,             False),
             (transient_rod,             True),
             (fuel_follower_control_rod, False),
             (fuel_follower_control_rod, True)]

    for element, inserted in cases:
        model = problem_2_utils.build_openmc_model(fuel_element, coolant, element, control_rod_inserted=inserted)
        assert model is not None


def test_problem_2_mpact_tools(fuel_element, graphite_element, central_thimble,
                               transient_rod, fuel_follower_control_rod,
                               coolant):

    cases = [(None,                      False),
             (graphite_element,          False),
             (central_thimble,           False),
             (transient_rod,             False),
             (transient_rod,             True),
             (fuel_follower_control_rod, False),
             (fuel_follower_control_rod, True)]

    for element, inserted in cases:
        problem_2_utils.write_mpact_input(fuel_element, coolant, element, control_rod_inserted=inserted)
        assert os.path.exists("mpact.inp")
        os.remove("mpact.inp")


def test_problem_4_openmc_tools(fuel_element, graphite_element, central_thimble,
                                transient_rod, fuel_follower_control_rod,
                                coolant):

    cases = [(None,                      False),
             (graphite_element,          False),
             (central_thimble,           False),
             (transient_rod,             False),
             (transient_rod,             True),
             (fuel_follower_control_rod, False),
             (fuel_follower_control_rod, True)]

    for element, inserted in cases:
        control_rod_position = 0.0
        if element is transient_rod:
            control_rod_position = NETL.DefaultGeometries.TRANSIENT_ROD_FULLY_INSERTED_POSITION if inserted else \
                                   NETL.DefaultGeometries.TRANSIENT_ROD_FULLY_WITHDRAWN_POSITION
        elif element is fuel_follower_control_rod:
            control_rod_position = NETL.DefaultGeometries.FFCR_FULLY_INSERTED_POSITION if inserted else \
                                   NETL.DefaultGeometries.FFCR_FULLY_WITHDRAWN_POSITION
        model = problem_4_utils.build_openmc_model(fuel_element,
                                                   coolant,
                                                   element,
                                                   control_rod_position)
        assert model is not None
