from typing import Dict, List, Optional

import openmc
import mpactpy
from coreforge.geometry_elements import PinCellStack, HexLattice
from coreforge.geometry_elements.triga import FuelElement, GraphiteElement
from coreforge.geometry_elements.triga.netl import (Core, CentralThimble, SourceHolder, Reactor,
                                                    PNT, ThreeElementIrradiator,
                                                    ModifiedThreeElementIrradiator)
from coreforge import openmc_builder
from coreforge import mpact_builder
from coreforge.shapes import Circle

from progression_problems.TRIGA.NETL.default_geometries import DefaultGeometries as NETL_DefaultGeometries
from progression_problems.TRIGA.NETL.problem_1_utils import lattice_dims
from progression_problems.TRIGA.NETL.utils import (build_generic_openmc_tallies,
                                                   build_multicell_geometry,
                                                   DEFAULT_MPACT_SETTINGS,
                                                   default_mpact_material_specs)


reactor          = NETL_DefaultGeometries.reactor()


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
        Reference location used to look up the grid-plate penetrations.
    """

    if isinstance(element, CentralThimble):
        return "A-01"
    if isinstance(element, Core.ControlRod):
        return "C-01"
    if isinstance(element, PNT):
        return "G-34"
    return "B-01"


def grid_plate_specs(
    grid_plate: Reactor.GridPlate,
    location: str,
    element: Optional[Core.Element],
) -> Reactor.CoreCellSpecs.GridPlateSpecs:
    """Select grid-plate geometry specifications for a core element.

    Parameters
    ----------
    grid_plate : Reactor.GridPlate
        Plate supplying the material, axial bounds, and penetration radii.
    location : str
        Reference location for the ordinary penetration-map entry.
    element : Optional[Core.Element]
        Element occupying the cell, or ``None`` for a vacant location.

    Returns
    -------
    Reactor.CoreCellSpecs.GridPlateSpecs
        Plate specifications with the selected penetration.
    """
    radius = grid_plate.geometry.penetration_map[location]

    if isinstance(element, (ThreeElementIrradiator, ModifiedThreeElementIrradiator)):
        three_element_radius = grid_plate.geometry.three_element_penetration_radius
        if three_element_radius is not None:
            radius = three_element_radius

    return Reactor.CoreCellSpecs.GridPlateSpecs(
        axial_bounds=grid_plate.axial_bounds,
        material=grid_plate.geometry.material,
        penetrations=[] if radius is None else [Reactor.CoreCellSpecs.PenetrationSpecs(radius=radius)],
    )


def element_bottom_axial_position(element: Core.Element,
                                  control_rod_bottom_position: float,
                                  upper_grid_plate: Reactor.GridPlate,
                                  lower_grid_plate: Reactor.GridPlate) -> float:
    """Get the bottom axial position for a core element.

    Parameters
    ----------
    element : Core.Element
        The core element to get the bottom axial position for.
    control_rod_bottom_position : float
        The bottom axial position of control rods [cm].
    upper_grid_plate : Reactor.GridPlate
        Upper grid plate used to position the source holder.
    lower_grid_plate : Reactor.GridPlate
        Lower grid plate whose top surface supports the three-element irradiator.

    Returns
    -------
    float
        Bottom axial position relative to the fuel centerline [cm].
    """

    bottom_axial_position = control_rod_bottom_position
    if isinstance(element, (PNT, PinCellStack)):
        bottom_axial_position = element.bottom_pos
    elif isinstance(element, (ThreeElementIrradiator, ModifiedThreeElementIrradiator)):
        bottom_axial_position = lower_grid_plate.axial_bounds.upper
    elif isinstance(element, CentralThimble):
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
        Native core-element layout and its surrounding material.
    control_rod_bottom_position : float
        Axial position for the bottom of a control rod [cm].
    upper_grid_plate : Reactor.GridPlate
        Upper-grid geometry and axial placement.
    lower_grid_plate : Reactor.GridPlate
        Lower-grid geometry and axial placement.

    Returns
    -------
    List[List[Reactor.CoreCellSpecs]]
        Geometry specifications in the same ring order as ``lattice.elements``.
    """
    irradiator_cells = {}
    for ring, centers in zip(lattice.elements, lattice.cell_centers):
        for element, center in zip(ring, centers):
            if not isinstance(element, (ThreeElementIrradiator, ModifiedThreeElementIrradiator)):
                continue
            radius = upper_grid_plate.geometry.three_element_penetration_radius
            assert radius is not None, \
                "An upper-grid-plate three-element penetration radius is required when an irradiator is present."
            bottom_position = element_bottom_axial_position(
                element, control_rod_bottom_position, upper_grid_plate, lower_grid_plate,
            )
            for i, j in lattice.cells_intersecting(Circle(radius), center):
                cell_center = lattice.cell_centers[i][j]
                x0, y0 = center[0] - cell_center[0], center[1] - cell_center[1]
                irradiator_cells[i, j] = (
                    Reactor.CoreCellSpecs.ElementSpecs(
                        geometry=element, bottom_axial_position=bottom_position, x0=x0, y0=y0,
                    ),
                    Reactor.CoreCellSpecs.PenetrationSpecs(radius=radius, x0=x0, y0=y0),
                )

    core_cell_specs = []
    for i, ring in enumerate(lattice.elements):
        ring_specs = []
        for j, element in enumerate(ring):
            location = core_location(element)
            elements = []
            if element is not None:
                elements.append(Reactor.CoreCellSpecs.ElementSpecs(
                    geometry=element,
                    bottom_axial_position=element_bottom_axial_position(
                        element,
                        control_rod_bottom_position,
                        upper_grid_plate,
                        lower_grid_plate,
                    ),
                ))

            upper_specs = grid_plate_specs(upper_grid_plate, location, element)
            irradiator_specs = irradiator_cells.get((i, j))
            if irradiator_specs is not None:
                placement, penetration = irradiator_specs
                if placement.geometry is not element:
                    elements.append(placement)
                    upper_specs.penetrations.append(penetration)

            ring_specs.append(Reactor.CoreCellSpecs(
                location=location,
                outer_material=lattice.outer_material,
                elements=elements,
                upper_grid_plate=upper_specs,
                lower_grid_plate=grid_plate_specs(lower_grid_plate, location, element),
            ))
        core_cell_specs.append(ring_specs)

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
