from typing import Dict, List, Optional

import openmc
import mpactpy
from coreforge.geometry_elements import HexLattice
from coreforge.geometry_elements.triga import FuelElement
from coreforge.geometry_elements.triga.netl import (Core, CentralThimble, Reactor,
                                                    PNT, ThreeElementIrradiator,
                                                    ModifiedThreeElementIrradiator)
from coreforge import openmc_builder
from coreforge import mpact_builder
from coreforge.geometry_elements.triga.netl.reactor import (element_bottom_axial_position,
                                                          grid_plate_specs)
from coreforge.shapes import Circle

from progression_problems.TRIGA.NETL.default_geometries import DefaultGeometries as NETL_DefaultGeometries
from progression_problems.TRIGA.NETL.problem_1_utils import lattice_dims
from progression_problems.TRIGA.NETL.utils import (build_generic_openmc_tallies,
                                                   build_multicell_geometry,
                                                   DEFAULT_MPACT_SETTINGS,
                                                   default_mpact_material_specs)


reactor = NETL_DefaultGeometries.reactor()


def core_location(element: Optional[Core.Element]) -> str:
    """Select a reference core location for grid-penetration specifications.

    Parameters
    ----------
    element : Optional[Core.Element]
        The core element to get the location for. ``None`` uses the ordinary
        fuel-location penetrations.

    Returns
    -------
    str
        Reference location used to look up the grid-plate penetrations. Three-element
        irradiators use a reserved irradiation location; callers recenter its openings.
    """

    if isinstance(element, CentralThimble):
        return Core.CENTRAL_THIMBLE_LOCATION
    if isinstance(element, Core.ControlRod):
        return Core.CONTROL_ROD_LOCATIONS[0]
    if isinstance(element, PNT):
        return Core.PNT_LOCATION
    if isinstance(element, (ThreeElementIrradiator, ModifiedThreeElementIrradiator)):
        return Core.THREE_ELEMENT_LOCATIONS[0]
    return "B-01"


def _build_core_cell_specs(
    lattice: HexLattice,
    control_rod_bottom_position: float,
    upper_grid_plate: Reactor.GridPlate,
    lower_grid_plate: Reactor.GridPlate,
) -> List[List[Reactor.CoreCellSpecs]]:
    """Resolve per-cell geometry specifications for the multicell lattice.

    Parameters
    ----------
    lattice : HexLattice
        Multicell layout from ``build_multicell_geometry`` and its surrounding
        material. Any three-element irradiator occupies the central cell.
    control_rod_bottom_position : float
        Axial position for the bottom of a control rod [cm].
    upper_grid_plate : Reactor.GridPlate
        Upper-grid geometry and axial placement. Reference openings at the
        three-element location are recentered on the multicell irradiator.
    lower_grid_plate : Reactor.GridPlate
        Lower-grid geometry and axial placement, normally with centered
        fuel-location openings.

    Returns
    -------
    List[List[Reactor.CoreCellSpecs]]
        Geometry specifications in the same ring order as ``lattice.elements``.
    """
    core_cell_specs = []
    for ring in lattice.elements:
        ring_specs = []
        for element in ring:
            location = core_location(element)
            elements = []
            if element is not None:
                if isinstance(element, Core.ControlRod):
                    bottom_position = control_rod_bottom_position
                else:
                    bottom_position = element_bottom_axial_position(element, upper_grid_plate, lower_grid_plate)
                assert bottom_position is not None
                elements.append(Reactor.CoreCellSpecs.ElementSpecs(
                    geometry=element, bottom_axial_position=bottom_position,
                ))
            plate_specs = {}
            for name, plate in (("upper_grid_plate", upper_grid_plate),
                                ("lower_grid_plate", lower_grid_plate)):
                penetrations = plate.geometry.penetration_map[location]
                if location in Core.THREE_ELEMENT_LOCATIONS:
                    penetrations = [(radius, 0.0, 0.0) for radius, _, _ in penetrations]
                plate_specs[name] = grid_plate_specs(plate, penetrations)
            ring_specs.append(Reactor.CoreCellSpecs(
                location=location,
                outer_material=lattice.outer_material,
                elements=elements,
                **plate_specs,
            ))
        core_cell_specs.append(ring_specs)

    central_specs = core_cell_specs[-1][0]
    if central_specs.location not in Core.THREE_ELEMENT_LOCATIONS:
        return core_cell_specs

    irradiator = lattice.elements[-1][0]
    center = lattice.cell_centers[-1][0]
    footprint = irradiator.as_stack().footprint
    opening, = central_specs.upper_grid_plate.penetrations
    assert footprint.outer_radius < opening.radius, \
        "The three-element irradiator must fit within the upper-grid-plate penetration."

    # Extend the central irradiator and its upper-plate opening into neighboring cells.
    for (i, j), (x0, y0) in lattice.cells_intersecting(Circle(opening.radius), center).items():
        neighbor = core_cell_specs[i][j]
        if neighbor is not central_specs:
            neighbor.upper_grid_plate.penetrations.append(Reactor.CoreCellSpecs.PenetrationSpecs(
                radius=opening.radius, x0=x0, y0=y0,
            ))
            neighbor.elements.append(Reactor.CoreCellSpecs.ElementSpecs(
                geometry=irradiator, bottom_axial_position=central_specs.elements[0].bottom_axial_position,
                x0=x0, y0=y0,
            ))

    return core_cell_specs


def build_openmc_model(fuel:                        FuelElement,
                       central_element:             Optional[Core.Element],
                       control_rod_bottom_position: float = 0.0,
                       upper_grid_plate:            Reactor.GridPlate = reactor.upper_grid_plate,
                       lower_grid_plate:            Reactor.GridPlate = reactor.lower_grid_plate,
                       spectrum_group_structure:    str = "MPACT-51",
                       pitch:                       float = NETL_DefaultGeometries.core().pitch,
                       pool_height:                 float = NETL_DefaultGeometries.pool().height,
) -> openmc.model.Model:
    """Build a multicell OpenMC Model.

    Parameters
    ----------
    fuel : FuelElement
        Fuel element supplying the fuel geometry.
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
    pitch : float
        Hexagonal lattice pitch to use for the multicell geometry. Defaults to
        the NETL core pitch.
    pool_height : float
        Axial pool height to use for the top and bottom vacuum boundaries.
        Defaults to the NETL pool height.

    Returns
    -------
    openmc.model.Model
        The constructed OpenMC model.
    """

    dims           = lattice_dims(pitch)
    lattice        = build_multicell_geometry(fuel            = fuel,
                                              central_element = central_element,
                                              pitch           = pitch)
    outer_material = lattice.outer_material
    outer_universe = openmc.Universe(cells=[openmc.Cell(fill=outer_material.openmc_material)])
    core_cell_specs = _build_core_cell_specs(
        lattice, control_rod_bottom_position, upper_grid_plate, lower_grid_plate,
    )

    universes = []
    for ring in core_cell_specs:
        ring_universes = []
        for geometry_specs in ring:
            universe = openmc_builder.triga.netl.reactor.build_core_element(
                core_cell_specs=geometry_specs,
            )
            ring_universes.append(universe)
        universes.append(ring_universes)

    openmc_lattice = openmc.HexLattice()
    openmc_lattice.orientation = lattice.orientation
    openmc_lattice.pitch = [lattice.pitch]
    openmc_lattice.center = (0.0, 0.0)
    openmc_lattice.universes = universes
    openmc_lattice.outer = outer_universe

    top_boundary    = openmc.ZPlane(z0 =  0.5 * pool_height, boundary_type='vacuum')
    bottom_boundary = openmc.ZPlane(z0 = -0.5 * pool_height, boundary_type='vacuum')
    radial_boundary = openmc.model.RectangularPrism(width         = dims["width"] * 8,
                                                    height        = dims["height"] * 6,
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
                      central_element:             Optional[Core.Element],
                      control_rod_bottom_position: float = 0.0,
                      upper_grid_plate:            Reactor.GridPlate = reactor.upper_grid_plate,
                      lower_grid_plate:            Reactor.GridPlate = reactor.lower_grid_plate,
                      pitch:                       float = NETL_DefaultGeometries.core().pitch,
                      pool_height:                 float = NETL_DefaultGeometries.pool().height,
                      fuel_build_specs:            Optional[mpact_builder.triga.FuelElement.Specs] = None,
                      element_build_specs:         Optional[mpact_builder.triga.netl.Reactor.CoreElementSpecs] = None,
                      outer_region_specs:          Optional[mpact_builder.triga.CoreElement.SegmentSpecs] = None,
                      filename:                    str = "mpact.inp",
                      states:                      Optional[List[Dict[str, str]]] = None,
                      xsec_settings:               Optional[Dict[str, str]] = None,
                      options:                     Optional[Dict[str, str]] = None) -> None:
    """Write the MPACT input for a TRIGA fuel element and central element.

    Parameters
    ----------
    fuel : FuelElement
        Fuel element supplying the fuel geometry.
    central_element : Optional[Core.Element]
        The central element to use for building the multicell geometry.
    control_rod_bottom_position : float
        Axial position for the bottom of a control rod [cm].
    upper_grid_plate : Core.GridPlate
        The upper grid plate to use in the model.
    lower_grid_plate : Core.GridPlate
        The lower grid plate to use in the model.
    pitch : float
        Hexagonal lattice pitch to use for the multicell geometry. Defaults to
        the NETL core pitch.
    pool_height : float
        Axial pool height to use for the outer axial bounds in the model.
        Defaults to the NETL pool height.
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

    lattice = build_multicell_geometry(fuel            = fuel,
                                       central_element = central_element,
                                       pitch           = pitch)
    core_cell_specs = _build_core_cell_specs(
        lattice, control_rod_bottom_position, upper_grid_plate, lower_grid_plate,
    )

    stack_elements = []
    element_specs = {}
    axial_bounds = (-0.5 * pool_height, 0.5 * pool_height)

    for ring in core_cell_specs:
        ring_stacks = []
        for geometry_specs in ring:
            build_specs = []
            materials = []
            for placement in geometry_specs.elements:
                element = placement.geometry
                placement_specs = fuel_build_specs if isinstance(element, FuelElement) else None
                if element is central_element and element_build_specs is not None:
                    placement_specs = element_build_specs
                build_specs.append(placement_specs)
                materials.extend(element.get_materials())

            builder_specs = mpact_builder.triga.netl.Reactor.CoreCellSpecs(
                element_specs=build_specs or None,
                outer_region_specs=outer_region_specs,
                axial_bounds=axial_bounds)

            stack, stack_specs = mpact_builder.triga.netl.reactor.build_core_element(
                geometry_specs=geometry_specs,
                builder_specs=builder_specs)

            ring_stacks.append(stack)
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
    core_map = [list(row[1:-1]) for row in core.assembly_map[2:-2]]
    geometry = mpactpy.Core(core_map)

    states = [dict(state) for state in (states or [DEFAULT_MPACT_SETTINGS["state"]])]
    xsec_settings = dict(xsec_settings or DEFAULT_MPACT_SETTINGS["xsec"])
    options = dict(options or DEFAULT_MPACT_SETTINGS["options"])

    for state in states:
        state["tinlet"] = state.get("tinlet", f"{fuel.outer_material.temperature} K")

    options["bound_cond"] = "1 1 1 1 0 0"

    mpact_model = mpactpy.Model(geometry, states, xsec_settings, options)
    with open(filename, "w") as file:
        file.write(mpact_model.write_to_string("TRIGA", indent=4))
