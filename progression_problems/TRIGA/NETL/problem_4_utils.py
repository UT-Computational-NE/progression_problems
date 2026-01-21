from typing import Dict, List, Optional

import openmc
import mpactpy
from coreforge.geometry_elements import HexLattice
from coreforge.materials import Material
from coreforge.geometry_elements.triga import FuelElement, GraphiteElement
from coreforge.geometry_elements.triga.netl import Core, CentralThimble, SourceHolder, Reactor
from coreforge import openmc_builder
from coreforge import mpact_builder

from progression_problems.TRIGA.NETL.default_geometries import DefaultGeometries as NETL_DefaultGeometries
from progression_problems.TRIGA.NETL.problem_1_utils import lattice_dims
from progression_problems.TRIGA.NETL.utils import (build_generic_openmc_tallies,
                                                   DEFAULT_MPACT_SETTINGS,
                                                   default_mpact_material_specs)


reactor          = NETL_DefaultGeometries.reactor()
POOL_HEIGHT      = NETL_DefaultGeometries.pool().height


def build_multicell_geometry(fuel:            FuelElement,
                             coolant:         openmc.Material,
                             central_element: Optional[Core.Element]
    ) -> HexLattice:
    """ Build a multicell CoreForge geometry for a fuel design,
        central element, and coolant material.

    Parameters
    ----------
    fuel : FuelElement
        The TRIGA fuel element to build the fuel cells with.
    coolant : openmc.Material
        The coolant material to use in the multicell geometry.
    central_element : Optional[Core.Element]
        The central element to include in the multicell geometry.

    Returns
    -------
    HexLattice
        The constructed multicell geometry.
    """

    f = fuel
    c = central_element
    elements = [[         f,         ],
                [     f,      f,     ],
                [ f,      f,      f, ],
                [     f,      f,     ],
                [ f,      c,      f, ],
                [     f,      f,     ],
                [ f,      f,      f, ],
                [     f,      f,     ],
                [         f,         ]]

    return HexLattice(
        pitch          = NETL_DefaultGeometries.core().pitch,
        outer_material = Material(coolant),
        elements       = elements,
        orientation    = "y")


def core_location(element: Core.Element) -> str:
    """Get the core location string for a given core element.

    Parameters
    ----------
    element : Core.Element
        The core element to get the location for.

    Returns
    -------
    str
        The core location string.
    """

    if isinstance(element, CentralThimble):
        return "A-01"
    if isinstance(element, Core.ControlRod):
        return "C-01"
    return "B-01"


def element_bottom_axial_position(element: Core.Element,
                                  control_rod_bottom_position: float,
                                  upper_grid_plate: Reactor.GridPlate) -> float:
    """Get the bottom axial position for a core element.

    Parameters
    ----------
    element : Core.Element
        The core element to get the bottom axial position for.
    control_rod_bottom_position : float
        The bottom axial position of control rods [cm].
    upper_grid_plate : Core.GridPlate
        The upper grid plate to use for calculating axial positions.

    Returns
    -------
    float
        The bottom axial position of the element [cm].
    """

    bottom_axial_position = control_rod_bottom_position
    if isinstance(element, CentralThimble):
        bottom_axial_position = -0.5 * element.length
    elif isinstance(element, FuelElement):
        bottom_axial_position = (-0.5 * element.fuel_meat.length -
                element.moly_disc.thickness -
                element.lower_end_fitting.length -
                element.lower_graphite_reflector.thickness)
    elif isinstance(element, GraphiteElement):
        bottom_axial_position = (-0.5 * element.graphite_meat.length -
                element.lower_end_fitting.length)
    elif isinstance(element, SourceHolder):
        bottom_axial_position = (upper_grid_plate.top_to_core_centerline_distance -
                element.length)
    return bottom_axial_position


def build_openmc_model(fuel:                        FuelElement,
                       coolant:                     openmc.Material,
                       central_element:             Optional[Core.Element],
                       control_rod_bottom_position: float = 0.0,
                       upper_grid_plate:            Reactor.GridPlate = reactor.upper_grid_plate,
                       lower_grid_plate:            Reactor.GridPlate = reactor.lower_grid_plate,
                       spectrum_group_structure:    str = "MPACT-51"
) -> openmc.model.Model:
    """Build a multicell OpenMC Model.

    Parameters
    ----------
    fuel : FuelElement
        The TRIGA fuel element to build the fuel cells with.
    coolant : openmc.Material
        The coolant material to use in the multicell geometry.
    central_element : Optional[Core.Element]
        The central element to include in the multicell geometry.
    control_rod_bottom_position : float
        Axial position for the bottom of a control rod [cm].
    upper_grid_plate : Core.GridPlate
        The upper grid plate to use in the model.
    lower_grid_plate : Core.GridPlate
        The lower grid plate to use in the model.
    spectrum_group_structure : str
        The energy group structure to use for the multi-group spectrum tally.

    Returns
    -------
    openmc.model.Model
        The constructed OpenMC model.
    """

    lattice        = build_multicell_geometry(fuel, coolant, central_element)
    outer_material = lattice.outer_material.openmc_material
    outer_universe = openmc.Universe(cells=[openmc.Cell(fill=outer_material)])

    universes = []
    for ring in lattice.elements:
        ring_universes = []
        for element in ring:
            universe = openmc_builder.triga.netl.reactor.build_core_element(
                core_location=core_location(element),
                upper_grid_plate=upper_grid_plate,
                lower_grid_plate=lower_grid_plate,
                element=element,
                element_bottom_axial_position=element_bottom_axial_position(
                    element,
                    control_rod_bottom_position,
                    upper_grid_plate
                ),
                outer_material=outer_material,
            )
            ring_universes.append(universe)
        universes.append(ring_universes)

    openmc_lattice = openmc.HexLattice()
    openmc_lattice.orientation = lattice.orientation
    openmc_lattice.pitch = [lattice.pitch]
    openmc_lattice.center = (0.0, 0.0)
    openmc_lattice.universes = universes
    openmc_lattice.outer = outer_universe

    top_boundary    = openmc.ZPlane(z0 =  0.5 * POOL_HEIGHT, boundary_type='vacuum')
    bottom_boundary = openmc.ZPlane(z0 = -0.5 * POOL_HEIGHT, boundary_type='vacuum')
    radial_boundary = openmc.model.RectangularPrism(width         = lattice_dims["width"] * 8,
                                                    height        = lattice_dims["height"] * 6,
                                                    boundary_type = 'reflective')
    lattice_cell    = openmc.Cell(fill   = openmc_lattice,
                                  region = -radial_boundary & +bottom_boundary & -top_boundary)

    main_universe = openmc.Universe(cells=[lattice_cell])
    geometry      = openmc.Geometry(main_universe)
    materials     = openmc.Materials(list(geometry.get_all_materials().values()))

    settings           = openmc.Settings()
    settings.batches   = 100
    settings.inactive  = 20
    settings.particles = 10000

    fuel_element = next(e for ring in lattice.elements for e in ring if isinstance(e, FuelElement))
    mesh_zmin    = -0.5 * fuel_element.interior_length
    mesh_zmax    =  0.5 * fuel_element.interior_length
    lower, upper = geometry.bounding_box

    mesh             = openmc.RegularMesh()
    mesh.lower_left  = (lower[0], lower[1], mesh_zmin)
    mesh.upper_right = (upper[0], upper[1], mesh_zmax)
    mesh.dimension   = (1, 1, 10)

    universe_ids = [universe.id for ring in openmc_lattice.universes for universe in ring]

    tallies      = build_generic_openmc_tallies(spectrum_group_structure, universe_ids, mesh)
    tallies      = openmc.Tallies(list(tallies.values()))

    return openmc.model.Model(geometry=geometry, materials=materials, settings=settings, tallies=tallies)


def write_mpact_input(fuel:                        FuelElement,
                      coolant:                     openmc.Material,
                      central_element:             Optional[Core.Element],
                      control_rod_bottom_position: float = 0.0,
                      upper_grid_plate:            Reactor.GridPlate = reactor.upper_grid_plate,
                      lower_grid_plate:            Reactor.GridPlate = reactor.lower_grid_plate,
                      fuel_build_specs:            Optional[mpact_builder.triga.FuelElement.Specs] = None,
                      element_build_specs:         Optional[mpact_builder.triga.netl.Reactor.CoreElementSpecs] = None,
                      outer_region_specs:          Optional[mpact_builder.triga.CoreElement.SegmentSpecs] = None,
                      filename:                    str = "mpact.inp",
                      states:                      List[Dict[str, str]] = [DEFAULT_MPACT_SETTINGS["state"]],
                      xsec_settings:               Dict[str, str] = DEFAULT_MPACT_SETTINGS["xsec"],
                      options:                     Dict[str, str] = DEFAULT_MPACT_SETTINGS["options"]) -> None:
    """Write the MPACT input for a given TRIGA fuel element, coolant, and central element.

    Parameters
    ----------
    fuel : FuelElement
        The TRIGA fuel element to use for building the multicell geometry.
    coolant : openmc.Material
        The coolant material to use in the multicell geometry.
    central_element : Optional[Core.Element]
        The central element to use for building the multicell geometry.
    control_rod_bottom_position : float
        Axial position for the bottom of a control rod [cm].
    upper_grid_plate : Core.GridPlate
        The upper grid plate to use in the model.
    lower_grid_plate : Core.GridPlate
        The lower grid plate to use in the model.
    fuel_build_specs : Optional[mpact_builder.triga.FuelElement.Specs]
        The mpact_builder specifications to use when building the fuel elements.
    element_build_specs : Optional[mpact_builder.triga.netl.CoreElementSpecs]
        The mpact_builder specifications to use when building the central element, if provided.
    outer_region_specs : Optional[mpact_builder.triga.CoreElement.SegmentSpecs]
        The mpact_builder specifications to use when building the outer axial regions
        (coolant above/below the elements).
    filename : str
        The filename to write the MPACT input to. (Default: "mpact.inp")
    states : List[Dict[str, str]]
        The state settings to use in the MPACT input.
    xsec_settings : Dict[str, str]
        The cross section settings to use in the MPACT input.
    options : Dict[str, str]
        The options settings to use in the MPACT input.
    """

    lattice = build_multicell_geometry(fuel, coolant, central_element)

    stack_elements = []
    element_specs = {}
    axial_bounds = (-0.5 * POOL_HEIGHT, 0.5 * POOL_HEIGHT)

    for ring in lattice.elements:
        ring_stacks = []
        for element in ring:
            build_specs = fuel_build_specs if isinstance(element, FuelElement) else None
            if element is not None and element is central_element and element_build_specs is not None:
                build_specs = element_build_specs

            bottom_position = None
            if element is not None:
                bottom_position = element_bottom_axial_position(element,
                                                                control_rod_bottom_position,
                                                                upper_grid_plate)

            core_cell_specs = mpact_builder.triga.netl.Reactor.CoreCellSpecs(
                element_specs=build_specs,
                outer_region_specs=outer_region_specs,
                axial_bounds=axial_bounds)

            stack, stack_specs = mpact_builder.triga.netl.reactor.build_core_element(
                core_location                 = core_location(element),
                upper_grid_plate              = upper_grid_plate,
                lower_grid_plate              = lower_grid_plate,
                element                       = element,
                element_bottom_axial_position = bottom_position,
                outer_material                = lattice.outer_material,
                core_cell_specs               = core_cell_specs)

            ring_stacks.append(stack)
            materials = element.get_materials() if element is not None else []
            stack_specs.apply_material_specs(stack, default_mpact_material_specs(materials))
            element_specs[stack] = stack_specs
        stack_elements.append(ring_stacks)

    stack_lattice = HexLattice(pitch          = lattice.pitch,
                               outer_material = lattice.outer_material,
                               elements       = stack_elements,
                               orientation    = lattice.orientation,
                               map_type       = "ring")
    specs = mpact_builder.HexLattice.Specs(element_specs=element_specs)

    core = mpact_builder.build(stack_lattice, specs)
    core_map = [list(row[1:-2]) for row in core.assembly_map[3:-4]]
    geometry = mpactpy.Core(core_map)

    for state in states:
        state["tinlet"] = state.get("tinlet", f"{coolant.temperature}")

    mpact_model = mpactpy.Model(geometry, states, xsec_settings, options)
    with open(filename, "w") as file:
        file.write(mpact_model.write_to_string("TRIGA", indent=4))
