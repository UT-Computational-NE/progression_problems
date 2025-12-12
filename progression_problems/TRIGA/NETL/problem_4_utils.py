from typing import Dict, List, Optional

import openmc
import mpactpy
from coreforge.geometry_elements import HexLattice
from coreforge.materials import Material
from coreforge.geometry_elements.triga import FuelElement, GraphiteElement
from coreforge.geometry_elements.triga.netl import (Core,
                                                    CentralThimble,
                                                    SourceHolder)
from coreforge import openmc_builder
from coreforge import mpact_builder

from progression_problems import TRIGA
from progression_problems.TRIGA import NETL
from progression_problems.TRIGA.NETL.problem_1_utils import lattice_dims


UPPER_GRID_PLATE = NETL.DefaultGeometries.upper_grid_plate()
UPPER_GRID_PLATE_DISTANCE_FROM_CORE_CENTERLINE = \
    NETL.DefaultGeometries.reactor().upper_grid_plate_distance_from_core_centerline

LOWER_GRID_PLATE = NETL.DefaultGeometries.lower_grid_plate()
LOWER_GRID_PLATE_DISTANCE_FROM_CORE_CENTERLINE = \
    NETL.DefaultGeometries.reactor().lower_grid_plate_distance_from_core_centerline

POOL_HEIGHT = NETL.DefaultGeometries.pool().height


def build_coolant_element(coolant: openmc.Material) -> FuelElement:
    """Build a coolant-only core element using fuel element dimensions.

    Parameters
    ----------
    coolant : openmc.Material
        Coolant material to fill all regions.

    Returns
    -------
    FuelElement
        Coolant core element shaped like the fuel geometry.
    """
    filler = TRIGA.DefaultGeometries.fuel_element()

    cladding = FuelElement.Cladding(thickness    = filler.cladding.thickness,
                                    outer_radius = filler.cladding.outer_radius,
                                    material     = Material(coolant))

    fuel_meat = FuelElement.FuelMeat(inner_radius = filler.fuel_meat.inner_radius,
                                     outer_radius = filler.fuel_meat.outer_radius,
                                     length       = filler.fuel_meat.length,
                                     material     = Material(coolant))

    zr_fill = FuelElement.ZrFillRod(radius   = filler.zr_fill_rod.radius,
                                    material = Material(coolant))

    upper_end_fitting = FuelElement.EndFitting(length    = filler.upper_end_fitting.length,
                                               direction = filler.upper_end_fitting.direction,
                                               material  = Material(coolant))

    upper_graphite_reflector = FuelElement.GraphiteReflector(radius    = filler.upper_graphite_reflector.radius,
                                                             thickness = filler.upper_graphite_reflector.thickness,
                                                             material  = Material(coolant))

    moly_disc = FuelElement.MolyDisc(radius    = filler.moly_disc.radius,
                                     thickness = filler.moly_disc.thickness,
                                     material  = Material(coolant))

    lower_graphite_reflector = FuelElement.GraphiteReflector(radius    = filler.lower_graphite_reflector.radius,
                                                             thickness = filler.lower_graphite_reflector.thickness,
                                                             material  = Material(coolant))

    lower_end_fitting = FuelElement.EndFitting(length    = filler.lower_end_fitting.length,
                                               direction = filler.lower_end_fitting.direction,
                                               material  = Material(coolant))

    return FuelElement(cladding                 = cladding,
                       upper_end_fitting        = upper_end_fitting,
                       upper_air_gap            = filler.upper_air_gap,
                       upper_graphite_reflector = upper_graphite_reflector,
                       zr_fill_rod              = zr_fill,
                       fuel_meat                = fuel_meat,
                       moly_disc                = moly_disc,
                       lower_graphite_reflector = lower_graphite_reflector,
                       lower_end_fitting        = lower_end_fitting,
                       fill_gas                 = Material(coolant),
                       outer_material           = Material(coolant))


def build_multicell_geometry(fuel: FuelElement,
                             coolant: openmc.Material,
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
    c = central_element or build_coolant_element(coolant)
    elements = [[         f,         ],
                [     f,      f,     ],
                [ f,      f,      f, ],
                [     f,      f,     ],
                [ f,      c,      f, ],
                [     f,      f,     ],
                [ f,      f,      f, ],
                [     f,      f,     ],
                [         f,         ]]

    return HexLattice(pitch          = NETL.Core().pitch,
                      outer_material = Material(coolant),
                      elements       = elements,
                      orientation    = 'y')


def build_openmc_model(fuel: FuelElement,
                       coolant: openmc.Material,
                       central_element: Optional[Core.Element],
                       control_rod_bottom_position: float = 0.0,
                       spectrum_group_structure: str = "MPACT-51"
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
            element_bottom_axial_position = control_rod_bottom_position
            if isinstance(element, (FuelElement, GraphiteElement, CentralThimble)):
                element_bottom_axial_position = -0.5 * element.length
            elif isinstance(element, SourceHolder):
                element_bottom_axial_position = UPPER_GRID_PLATE_DISTANCE_FROM_CORE_CENTERLINE + \
                                                UPPER_GRID_PLATE.thickness - element.length
            universe = openmc_builder.triga.netl.reactor.build_element_cell_universe(
                element, element_bottom_axial_position, outer_material,
                UPPER_GRID_PLATE, UPPER_GRID_PLATE_DISTANCE_FROM_CORE_CENTERLINE,
                LOWER_GRID_PLATE, LOWER_GRID_PLATE_DISTANCE_FROM_CORE_CENTERLINE
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

    universe_ids = [universe.id for ring in universes for universe in ring]

    tallies      = NETL.build_generic_openmc_tallies(spectrum_group_structure, universe_ids, mesh)
    tallies      = openmc.Tallies(list(tallies.values()))

    return openmc.model.Model(geometry=geometry, materials=materials, settings=settings, tallies=tallies)


def write_mpact_input(fuel: FuelElement,
                      coolant: openmc.Material,
                      central_element: Optional[Core.Element],
                      control_rod_bottom_position: float = 0.0,
                      fuel_build_specs: Optional[mpact_builder.CylindricalPinCell.Specs] = None,
                      element_build_specs: Optional[mpact_builder.CylindricalPinCell.Specs] = None,
                      filename: str = "mpact.inp",
                      states: List[Dict[str, str]] = [NETL.DEFAULT_MPACT_SETTINGS["state"]],
                      xsec_settings: Dict[str, str] = NETL.DEFAULT_MPACT_SETTINGS["xsec"],
                      options: Dict[str, str] = NETL.DEFAULT_MPACT_SETTINGS["options"]) -> None:
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
    fuel_build_specs : Optional[mpact_builder.CylindricalPinCell.Specs]
        The mpact_builder specifications to use when building the fuel pincell geometry.
    element_build_specs : Optional[mpact_builder.CylindricalPinCell.Specs]
        The mpact_builder specifications to use when building the central element pincell geometry.
    filename : str
        The filename to write the MPACT input to. (Default: "mpact.inp")
    states : List[Dict[str, str]]
        The state settings to use in the MPACT input.
    xsec_settings : Dict[str, str]
        The cross section settings to use in the MPACT input.
    options : Dict[str, str]
        The options settings to use in the MPACT input.
    """
