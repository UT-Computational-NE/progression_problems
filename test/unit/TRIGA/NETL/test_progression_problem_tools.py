import os
import pytest

import progression_problems.TRIGA as TRIGA
import progression_problems.TRIGA.NETL as NETL
from progression_problems.TRIGA.default_geometries import FuelSpec
from progression_problems.TRIGA.NETL.default_materials import DefaultMaterials as NETLDefaultMaterials
from progression_problems.TRIGA.NETL import problem_1_utils, problem_2_utils, problem_3_utils, problem_4_utils, problem_5_utils
from progression_problems.TRIGA.NETL.utils import plot_model_2D, default_mpact_material_specs
from coreforge import mpact_builder, materials
from coreforge.mpact_builder.builder_specs import DEFAULT_MPACT_MATERIAL_SPECS


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


def test_problem_1_openmc_tools(fuel_element, coolant, tmp_path):
    model = problem_1_utils.build_openmc_model(fuel_element, coolant)
    assert model is not None

    plot_path = tmp_path / "problem_1_plot.png"
    try:
        plot_model_2D(model, basis="xy", filename=str(plot_path), pixels=(200, 200))
        assert plot_path.exists()
    finally:
        if plot_path.exists():
            plot_path.unlink()


def test_problem_1_mpact_tools(fuel_element, coolant):
    problem_1_utils.write_mpact_input(fuel_element, coolant)
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


def test_problem_3_openmc_tools(coolant):
    reactor = NETL.DefaultGeometries.reactor()

    control_cases = [problem_3_utils.ControlRodSpecs(),
                     problem_3_utils.ControlRodSpecs(transient_rod_inserted=True,
                                                     shim_1_rod_inserted=True,
                                                     shim_2_rod_inserted=True,
                                                     regulating_rod_inserted=True)]

    excore_cases = ["none", "rsr", "beamports"]

    for excore in excore_cases:
        for specs in control_cases:
            model = problem_3_utils.build_openmc_model(reactor,
                                                       coolant,
                                                       control_rod_specs = specs,
                                                       excore_features   = excore)
            assert model is not None

def test_problem_3_mpact_tools(coolant, num_procs):
    reactor = NETL.DefaultGeometries.reactor()
    reactor_build_specs = mpact_builder.triga.netl.Reactor.Specs(num_procs=num_procs)

    control_cases = [problem_3_utils.ControlRodSpecs(),
                     problem_3_utils.ControlRodSpecs(transient_rod_inserted=True,
                                                     shim_1_rod_inserted=True,
                                                     shim_2_rod_inserted=True,
                                                     regulating_rod_inserted=True)]

    excore_cases = ["none", "rsr", "beamports"]

    for excore in excore_cases:
        for specs in control_cases:
            problem_3_utils.write_mpact_input(reactor,
                                              coolant,
                                              control_rod_specs   = specs,
                                              excore_features     = excore,
                                              reactor_build_specs = reactor_build_specs)
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


def test_problem_4_mpact_tools(fuel_element, graphite_element, central_thimble,
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
        problem_4_utils.write_mpact_input(fuel_element,
                                          coolant,
                                          element,
                                          control_rod_position)
        assert os.path.exists("mpact.inp")
        os.remove("mpact.inp")


def test_problem_5_openmc_tools():
    reactor = NETL.DefaultGeometries.reactor()
    model = problem_5_utils.build_openmc_model(reactor)
    assert model is not None


def test_problem_5_mpact_tools(num_procs):
    """Excluding excore build for the sake of expediency. It's already being tested in CoreForge."""
    reactor = NETL.DefaultGeometries.reactor()
    reactor_build_specs = mpact_builder.triga.netl.Reactor.Specs(exclude_excore=True, num_procs=num_procs)
    problem_5_utils.write_mpact_input(reactor, reactor_build_specs=reactor_build_specs)
    assert os.path.exists("mpact.inp")
    os.remove("mpact.inp")


def _fuel_spec(name, **kwargs):
    """A default fuel with a custom name, wrapped in a FuelSpec (for placement tests)."""
    material = NETLDefaultMaterials.fresh_fuel()
    material.name = name
    return FuelSpec(material=material, **kwargs)


@pytest.fixture(scope="module")
def per_location_reactor():
    """A reactor with custom fuel placed at a few locations (built once)."""
    ring_b = _fuel_spec("Fuel_Ring_B")
    regioned = _fuel_spec("Fuel_Regioned", num_radial_regions=2)
    return NETL.DefaultGeometries.reactor(fuel_materials={"B-01": ring_b, "B-02": ring_b, "C-02": regioned})


def test_per_location_fuel(per_location_reactor):
    # Placement: custom fuel where assigned (also exercises fuel_element + core), default elsewhere.
    loading = per_location_reactor.core.loading
    assert loading["B-01"].fuel_meat.material.name == "Fuel_Ring_B"
    assert loading["C-02"].fuel_meat.num_radial_regions == 2  # multi-region FuelSpec honored
    assert loading["D-01"].fuel_meat.material.name == "Fuel"

    # MPACT specs: default and custom fuels -> U-ZrH; the fuel follower is left as-is (issue #24).
    material_by_name = {m.name: m for m in per_location_reactor.get_materials()}
    specs = default_mpact_material_specs(list(material_by_name.values()))
    uzrh_specs = DEFAULT_MPACT_MATERIAL_SPECS[materials.UZrH]
    assert specs[material_by_name["Fuel"]] is uzrh_specs
    assert specs[material_by_name["Fuel_Ring_B"]] is uzrh_specs
    assert material_by_name["Fuel_Follower_Fuel"] not in specs


def test_per_location_fuel_rejects_non_fuel_location():
    with pytest.raises(ValueError):
        NETL.DefaultGeometries.core(fuel_materials={"D-03": _fuel_spec("Fuel_Bad")})
