import os
import pytest

import progression_problems.TRIGA as TRIGA
import progression_problems.TRIGA.NETL as NETL
from progression_problems.TRIGA.default_geometries import FuelSpec
from progression_problems.TRIGA.NETL.default_geometries import cosd, sind
from progression_problems.TRIGA.NETL.default_materials import DefaultMaterials as NETLDefaultMaterials
from progression_problems.TRIGA.NETL import problem_1_utils, problem_2_utils, problem_3_utils, problem_4_utils, problem_5_utils
from progression_problems.TRIGA.NETL.utils import (plot_model_2D, default_mpact_material_specs,
                                                  default_mpact_reactor_specs)
from progression_problems.constants import CM_PER_INCH
from coreforge import mpact_builder, materials
from coreforge.geometry_elements.triga.netl import (
    ModifiedThreeElementIrradiator,
    PNT,
    Reactor as NETLReactor,
)
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


def test_default_reactor_beam_port_placements():
    geometry = NETL.DefaultGeometries.beam_port(length=100.0)
    beam_ports = [
        NETL.DefaultGeometries.Reactor.beam_port_1_5(geometry=geometry),
        NETL.DefaultGeometries.Reactor.beam_port_2(geometry=geometry),
        NETL.DefaultGeometries.Reactor.beam_port_3(geometry=geometry),
        NETL.DefaultGeometries.Reactor.beam_port_4(geometry=geometry),
    ]
    expected_translations = [
        (35.2425, 0.0, -6.985),
        (6.222 + cosd(150.0) * 50.0,
         35.255 + sind(150.0) * 50.0,
         -6.985),
        (-50.0 - 26.43188, 0.0, -6.985),
        (-13.216 - cosd(60.0) * 50.0,
         -22.871 - sind(60.0) * 50.0,
         -6.985),
    ]

    for beam_port, expected_rotation, expected_translation in zip(
        beam_ports,
        (90.0, 150.0, 0.0, 60.0),
        expected_translations,
    ):
        assert isinstance(beam_port, NETLReactor.BeamPort)
        assert beam_port.geometry is geometry
        assert beam_port.rotation == pytest.approx(expected_rotation)
        assert beam_port.translation == pytest.approx(expected_translation)


def test_default_reactor_reflector_and_grid_plate_placements():
    reflector_geometry = NETL.DefaultGeometries.reflector()
    upper_grid_geometry = NETL.DefaultGeometries.upper_grid_plate()
    lower_grid_geometry = NETL.DefaultGeometries.lower_grid_plate()

    reflector = NETL.DefaultGeometries.Reactor.reflector(geometry=reflector_geometry)
    upper_grid = NETL.DefaultGeometries.Reactor.upper_grid_plate(geometry=upper_grid_geometry)
    lower_grid = NETL.DefaultGeometries.Reactor.lower_grid_plate(geometry=lower_grid_geometry)

    assert isinstance(reflector, NETLReactor.Reflector)
    assert reflector.geometry is reflector_geometry
    assert reflector.core_centerline_offset == pytest.approx(0.565 * CM_PER_INCH)
    assert isinstance(upper_grid, NETLReactor.GridPlate)
    assert upper_grid.geometry is upper_grid_geometry
    upper_openings = upper_grid.geometry.penetration_map["E-11"]
    assert len(upper_openings) == 1
    assert upper_openings[0][0] == pytest.approx(2.40000)
    assert upper_openings[0][1:] != (0.0, 0.0)
    assert upper_grid.top_to_core_centerline_distance == pytest.approx(
        NETL.DefaultGeometries.UPPER_GRID_PLATE_TOP_TO_CORE_CENTERLINE_DISTANCE
    )
    assert isinstance(lower_grid, NETLReactor.GridPlate)
    assert lower_grid.geometry is lower_grid_geometry
    assert lower_grid.geometry.penetration_map["E-11"][0][1:] == (0.0, 0.0)
    assert lower_grid.top_to_core_centerline_distance == pytest.approx(
        NETL.DefaultGeometries.LOWER_GRID_PLATE_TOP_TO_CORE_CENTERLINE_DISTANCE
    )


def test_default_three_element_irradiator():
    cadmium_irradiator = NETL.DefaultGeometries.three_element_irradiator()
    lead = NETLDefaultMaterials.lead()
    lead_irradiator = NETL.DefaultGeometries.three_element_irradiator(liner_material=lead)

    assert cadmium_irradiator.outer_casing.inner_radius == pytest.approx(2.23393)
    assert cadmium_irradiator.outer_casing.outer_radius == pytest.approx(2.38125)
    assert cadmium_irradiator.outer_casing.length == pytest.approx(127.9524)
    assert cadmium_irradiator.inner_sleeve.inner_radius == pytest.approx(1.93929)
    assert cadmium_irradiator.inner_sleeve.outer_radius == pytest.approx(2.06375)
    assert cadmium_irradiator.liner.thickness == pytest.approx(0.10160)
    assert cadmium_irradiator.liner.material.name == "Cadmium"
    assert lead_irradiator.liner.material.name == "Lead"
    assert lead_irradiator.liner.material.density == pytest.approx(11.35)

    lead_specs = default_mpact_material_specs([lead_irradiator.liner.material])
    assert lead_specs[lead_irradiator.liner.material] == DEFAULT_MPACT_MATERIAL_SPECS[materials.Pb]

    core = NETL.DefaultGeometries.core(three_element_irradiator=lead_irradiator)
    assert core.three_element_irradiator is lead_irradiator
    assert core.full_map["E-11"] is lead_irradiator
    assert core.full_map["F-13"] is lead_irradiator
    assert core.full_map["F-14"] is lead_irradiator

    reactor = NETL.DefaultGeometries.reactor(three_element_irradiator=lead_irradiator)
    assert reactor.core.three_element_irradiator is lead_irradiator


def test_default_modified_three_element_irradiator():
    irradiator = NETL.DefaultGeometries.modified_three_element_irradiator()

    assert isinstance(irradiator, ModifiedThreeElementIrradiator)
    assert not irradiator.simplified
    assert irradiator.outer_casing.tube_1_inner_radius == pytest.approx(2.23393)
    assert irradiator.outer_casing.tube_2_outer_radius == pytest.approx(2.38125)
    assert irradiator.pneumatic_system.open_tube_length == pytest.approx(109.73188)
    assert irradiator.b4c_canister.b4c_region_outer_radius == pytest.approx(1.89230)
    assert irradiator.b10_canister.upper_b10_outer_radius == pytest.approx(2.00660)
    assert irradiator.b10_canister.lower_b10_outer_radius == pytest.approx(2.04724)
    assert irradiator.silver_disk.material.name == "Silver"
    assert irradiator.b4c_canister.b4c_material.name == "Natural_B4C"
    assert irradiator.b10_canister.b10_material.name == "Enriched_Boron"
    assert len(irradiator.as_stack().segments) == 20

    material_specs = default_mpact_material_specs(irradiator.get_materials())
    assert irradiator.silver_disk.material in material_specs
    assert irradiator.b4c_canister.b4c_material in material_specs
    assert irradiator.b10_canister.b10_material in material_specs

    simplified = NETL.DefaultGeometries.modified_three_element_irradiator(
        simplified=True
    )
    assert simplified.simplified
    assert len(simplified.as_stack().segments) == 10

    core = NETL.DefaultGeometries.core(three_element_irradiator=irradiator)
    assert core.three_element_irradiator is irradiator
    assert core.full_map["E-11"] is irradiator
    assert core.full_map["F-13"] is irradiator
    assert core.full_map["F-14"] is irradiator


@pytest.mark.parametrize("liner_material_factory", [None, NETLDefaultMaterials.lead])
def test_default_pnt(liner_material_factory):
    pnt = NETL.DefaultGeometries.pnt()

    assert isinstance(pnt, PNT)
    assert pnt.wrapper is None
    assert pnt.bottom_pos == pytest.approx(-13.06 * CM_PER_INCH - 1.25 * CM_PER_INCH)
    assert pnt.tube.inner_radius == pytest.approx(0.5 * 0.685 * CM_PER_INCH)
    assert pnt.tube.outer_radius == pytest.approx(0.5 * 0.875 * CM_PER_INCH)
    assert pnt.tube.length == pytest.approx(80.0 + 18.7182)
    assert [segment.length for segment in pnt.terminus.segments] == pytest.approx([
        8.3259,
        4.1725,
        5.1308,
    ])
    assert pnt.bottom_pos + pnt.length == pytest.approx(80.0)

    liner_material = liner_material_factory() if liner_material_factory is not None else None
    lined_pnt = NETL.DefaultGeometries.pnt(
        terminus=NETL.DefaultGeometries.PNT.lined_terminus(liner_material=liner_material),
        wrapper=NETL.DefaultGeometries.PNT.wrapper(liner_material=liner_material),
    )
    assert lined_pnt.wrapper is not None
    assert lined_pnt.wrapper.length == pytest.approx(
        12.75 * CM_PER_INCH + 18.7182
    )
    assert [segment.length for segment in lined_pnt.terminus.segments] == pytest.approx([
        8.3259,
        4.1725,
        2.5400,
        0.0508,
        2.5400,
    ])
    disk = lined_pnt.terminus.segments[3].element
    assert [zone.shape.outer_radius for zone in disk.zones] == pytest.approx([0.86995, 1.11125])
    liner_name = liner_material.name if liner_material is not None else "Cadmium"
    assert [zone.material.name for zone in disk.zones] == [liner_name, "Aluminum"]
    assert lined_pnt.wrapper.cross_section.zones[0].material.name == liner_name
    assert disk.outer_material == lined_pnt.outer_material
    assert [segment.element.zones[-1].shape.outer_radius
            for segment in lined_pnt.terminus.segments] == pytest.approx([
        1.82245, 1.5875, 1.82245, 1.11125, 1.5875,
    ])

    custom_terminus = NETL.DefaultGeometries.PNT.lined_terminus(
        disk_radius=0.8, disk_outer_radius=1.2,
    )
    assert [zone.shape.outer_radius for zone in custom_terminus.segments[3].element.zones] == pytest.approx([0.8, 1.2])

    core = NETL.DefaultGeometries.core()
    assert isinstance(core.full_map["G-34"], PNT)

    reactor = NETL.DefaultGeometries.reactor(pnt=lined_pnt)
    assert reactor.core.full_map["G-34"] is lined_pnt


def test_problem_1_openmc_tools(fuel_element, tmp_path):
    model = problem_1_utils.build_openmc_model(fuel_element)
    assert model is not None

    plot_path = tmp_path / "problem_1_plot.png"
    try:
        plot_model_2D(model, basis="xy", filename=str(plot_path), pixels=(200, 200))
        assert plot_path.exists()
    finally:
        if plot_path.exists():
            plot_path.unlink()


def test_problem_1_mpact_tools(fuel_element):
    problem_1_utils.write_mpact_input(fuel_element)
    assert os.path.exists("mpact.inp")
    os.remove("mpact.inp")


def test_problem_2_openmc_tools(fuel_element, graphite_element, central_thimble,
                                transient_rod, fuel_follower_control_rod):

    cases = [(None,                      None),
             (graphite_element,          None),
             (central_thimble,           None),
             (transient_rod,             "air_follower"),
             (transient_rod,             "absorber"),
             (fuel_follower_control_rod, "fuel_follower"),
             (fuel_follower_control_rod, "absorber")]

    for element, section in cases:
        model = problem_2_utils.build_openmc_model(fuel_element, element, central_pincell_section=section)
        assert model is not None


def test_problem_2_mpact_tools(fuel_element, graphite_element, central_thimble,
                               transient_rod, fuel_follower_control_rod):

    cases = [(None,                      None),
             (graphite_element,          None),
             (central_thimble,           None),
             (transient_rod,             "air_follower"),
             (transient_rod,             "absorber"),
             (fuel_follower_control_rod, "fuel_follower"),
             (fuel_follower_control_rod, "absorber")]

    for element, section in cases:
        problem_2_utils.write_mpact_input(fuel_element, element, central_pincell_section=section)
        assert os.path.exists("mpact.inp")
        os.remove("mpact.inp")


def test_problem_3_openmc_tools():
    reactor = NETL.DefaultGeometries.reactor()

    control_cases = [problem_3_utils.ControlRodSpecs(),
                     problem_3_utils.ControlRodSpecs(transient_rod_section="absorber",
                                                     shim_1_rod_section="absorber",
                                                     shim_2_rod_section="absorber",
                                                     regulating_rod_section="absorber")]

    excore_cases = ["none", "rsr", "beamports"]

    for excore in excore_cases:
        for specs in control_cases:
            model = problem_3_utils.build_openmc_model(reactor,
                                                       control_rod_specs = specs,
                                                       excore_features   = excore)
            assert model is not None

def test_problem_3_mpact_tools(num_procs):
    reactor = NETL.DefaultGeometries.reactor()
    reactor_build_specs = default_mpact_reactor_specs(reactor)
    reactor_build_specs.num_procs = num_procs

    control_cases = [problem_3_utils.ControlRodSpecs(),
                     problem_3_utils.ControlRodSpecs(transient_rod_section="absorber",
                                                     shim_1_rod_section="absorber",
                                                     shim_2_rod_section="absorber",
                                                     regulating_rod_section="absorber")]

    excore_cases = ["none", "rsr", "beamports"]

    for excore in excore_cases:
        for specs in control_cases:
            problem_3_utils.write_mpact_input(reactor,
                                              control_rod_specs   = specs,
                                              excore_features     = excore,
                                              reactor_build_specs = reactor_build_specs)
            assert os.path.exists("mpact.inp")
            os.remove("mpact.inp")


def test_problem_4_openmc_tools(fuel_element, graphite_element, central_thimble,
                                transient_rod, fuel_follower_control_rod):

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
                                                   element,
                                                   control_rod_position)
        assert model is not None


def test_problem_4_mpact_tools(fuel_element, graphite_element, central_thimble,
                               transient_rod, fuel_follower_control_rod):

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
    reactor_build_specs = default_mpact_reactor_specs(reactor)
    reactor_build_specs.num_procs = num_procs
    reactor_build_specs.exclude_excore = True
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

    material_by_name = {m.name: m for m in per_location_reactor.get_materials()}
    specs = default_mpact_material_specs(list(material_by_name.values()))
    uzrh_specs = DEFAULT_MPACT_MATERIAL_SPECS[materials.UZrH].using_fission_product_ids(
        exclude=["Zr91","Zr93","Zr95","Zr96"]
    )
    assert specs[material_by_name["Fuel"]] == uzrh_specs
    assert specs[material_by_name["Fuel_Ring_B"]] == uzrh_specs


def test_per_location_fuel_rejects_non_fuel_location():
    with pytest.raises(ValueError):
        NETL.DefaultGeometries.core(fuel_materials={"D-03": _fuel_spec("Fuel_Bad")})
