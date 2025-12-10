from typing import Dict, List, Optional

import openmc
import mpactpy
from coreforge.geometry_elements import HexLattice
from coreforge.materials import Material
from coreforge.geometry_elements.triga import FuelElement, GraphiteElement
from coreforge.geometry_elements.triga.netl import (Core,
                                                    FuelFollowerControlRod,
                                                    TransientRod,
                                                    CentralThimble,
                                                    SourceHolder,
                                                    GridPlate)
from coreforge import openmc_builder
from coreforge import mpact_builder

from progression_problems import TRIGA
from progression_problems.TRIGA import NETL
from progression_problems.TRIGA.NETL.problem_1_utils import lattice_dims
from progression_problems.TRIGA.NETL.utils import DEFAULT_MPACT_SETTINGS

UPPER_GRID_PLATE = GridPlate(
    thickness=NETL.Reactor().upper_grid_plate.thickness,
    fuel_penetration_radius=NETL.Reactor().upper_grid_plate.fuel_penetration_radius,
    control_rod_penetration_radius=NETL.Reactor().upper_grid_plate.control_rod_penetration_radius,
    material=Material(NETL.Reactor().upper_grid_plate.material),
    name="upper_grid_plate"
)
UPPER_GRID_PLATE_DISTANCE_FROM_CORE_CENTERLINE = \
    NETL.Reactor().upper_grid_plate.distance_from_core_centerline

LOWER_GRID_PLATE = GridPlate(
    thickness=NETL.Reactor().lower_grid_plate.thickness,
    fuel_penetration_radius=NETL.Reactor().lower_grid_plate.fuel_penetration_radius,
    control_rod_penetration_radius=NETL.Reactor().lower_grid_plate.control_rod_penetration_radius,
    material=Material(NETL.Reactor().lower_grid_plate.material),
    name="lower_grid_plate"
)

LOWER_GRID_PLATE_DISTANCE_FROM_CORE_CENTERLINE = \
    NETL.Reactor().lower_grid_plate.distance_from_core_centerline

POOL_HEIGHT = NETL.Reactor().pool.height


def build_fuel_element(fuel: TRIGA.FuelElement,
                       coolant: openmc.Material) -> FuelElement:
    """ Build a fuel element CoreForge geometry for a given TRIGA fuel element.

    Parameters
    ----------
    fuel : TRIGA.FuelElement
        The TRIGA fuel element to build the geometry for.
    coolant : openmc.Material
        The coolant material to use in the geometry.

    Returns
    -------
    FuelElement
        The constructed CoreForge fuel element geometry.
    """
    cladding = FuelElement.Cladding(
        thickness=fuel.cladding.thickness,
        outer_radius=fuel.cladding.outer_radius,
        material=Material(fuel.cladding.material),
    )

    upper_end_fitting = FuelElement.EndFitting(
        length=fuel.upper_end_fitting.length,
        direction=fuel.upper_end_fitting.direction,
        material=Material(fuel.upper_end_fitting.material),
    )

    upper_air_gap = FuelElement.AirGap(thickness=fuel.upper_air_gap.thickness)

    upper_graphite_reflector = FuelElement.GraphiteReflector(
        radius=fuel.upper_graphite_reflector.radius,
        thickness=fuel.upper_graphite_reflector.thickness,
        material=Material(fuel.upper_graphite_reflector.material),
    )

    zr_fill = FuelElement.ZrFillRod(
        radius=fuel.zr_fill_rod.radius,
        material=Material(fuel.zr_fill_rod.material),
    )

    fuel_meat = FuelElement.FuelMeat(
        inner_radius=fuel.fuel_meat.inner_radius,
        outer_radius=fuel.fuel_meat.outer_radius,
        length=fuel.fuel_meat.length,
        material=Material(fuel.fuel_meat.material),
    )

    moly_disc = FuelElement.MolyDisc(
        radius=fuel.moly_disc.radius,
        thickness=fuel.moly_disc.thickness,
        material=Material(fuel.moly_disc.material),
    )

    lower_graphite_reflector = FuelElement.GraphiteReflector(
        radius=fuel.lower_graphite_reflector.radius,
        thickness=fuel.lower_graphite_reflector.thickness,
        material=Material(fuel.lower_graphite_reflector.material),
    )

    lower_end_fitting = FuelElement.EndFitting(
        length=fuel.lower_end_fitting.length,
        direction=fuel.lower_end_fitting.direction,
        material=Material(fuel.lower_end_fitting.material),
    )

    return FuelElement(
        cladding=cladding,
        upper_end_fitting=upper_end_fitting,
        upper_air_gap=upper_air_gap,
        upper_graphite_reflector=upper_graphite_reflector,
        zr_fill_rod=zr_fill,
        fuel_meat=fuel_meat,
        moly_disc=moly_disc,
        lower_graphite_reflector=lower_graphite_reflector,
        lower_end_fitting=lower_end_fitting,
        fill_gas=Material(fuel.fill_gas),
        outer_material=Material(coolant),
    )

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
    filler = TRIGA.FuelElement()

    cladding = FuelElement.Cladding(
        thickness=filler.cladding.thickness,
        outer_radius=filler.cladding.outer_radius,
        material=Material(coolant),
    )

    upper_end_fitting = FuelElement.EndFitting(
        length=filler.upper_end_fitting.length,
        direction=filler.upper_end_fitting.direction,
        material=Material(coolant),
    )

    upper_air_gap = FuelElement.AirGap(thickness=filler.upper_air_gap.thickness)

    upper_graphite_reflector = FuelElement.GraphiteReflector(
        radius=filler.upper_graphite_reflector.radius,
        thickness=filler.upper_graphite_reflector.thickness,
        material=Material(coolant),
    )

    zr_fill = FuelElement.ZrFillRod(
        radius=filler.zr_fill_rod.radius,
        material=Material(coolant),
    )

    fuel_meat = FuelElement.FuelMeat(
        inner_radius=filler.fuel_meat.inner_radius,
        outer_radius=filler.fuel_meat.outer_radius,
        length=filler.fuel_meat.length,
        material=Material(coolant),
    )

    moly_disc = FuelElement.MolyDisc(
        radius=filler.moly_disc.radius,
        thickness=filler.moly_disc.thickness,
        material=Material(coolant),
    )

    lower_graphite_reflector = FuelElement.GraphiteReflector(
        radius=filler.lower_graphite_reflector.radius,
        thickness=filler.lower_graphite_reflector.thickness,
        material=Material(coolant),
    )

    lower_end_fitting = FuelElement.EndFitting(
        length=filler.lower_end_fitting.length,
        direction=filler.lower_end_fitting.direction,
        material=Material(coolant),
    )

    return FuelElement(
        cladding=cladding,
        upper_end_fitting=upper_end_fitting,
        upper_air_gap=upper_air_gap,
        upper_graphite_reflector=upper_graphite_reflector,
        zr_fill_rod=zr_fill,
        fuel_meat=fuel_meat,
        moly_disc=moly_disc,
        lower_graphite_reflector=lower_graphite_reflector,
        lower_end_fitting=lower_end_fitting,
        fill_gas=Material(coolant),
        outer_material=Material(coolant),
    )

def build_graphite_element(element: TRIGA.GraphiteElement, coolant: openmc.Material) -> GraphiteElement:
    """Build a graphite element.

    Parameters
    ----------
    element : TRIGA.GraphiteElement
        Graphite element definition from progression_problems.
    coolant : openmc.Material
        Coolant material surrounding the cladding.

    Returns
    -------
    GraphiteElement
        CoreForge graphite element.
    """
    cladding = GraphiteElement.Cladding(
        thickness=element.cladding.thickness,
        outer_radius=element.cladding.outer_radius,
        material=Material(element.cladding.material),
    )

    upper_end_fitting = GraphiteElement.EndFitting(
        length=element.upper_end_fitting.length,
        direction=element.upper_end_fitting.direction,
        material=Material(element.upper_end_fitting.material),
    )

    graphite_meat = GraphiteElement.GraphiteMeat(
        outer_radius=element.graphite_meat.outer_radius,
        length=element.graphite_meat.length,
        material=Material(element.graphite_meat.material),
    )

    lower_end_fitting = GraphiteElement.EndFitting(
        length=element.lower_end_fitting.length,
        direction=element.lower_end_fitting.direction,
        material=Material(element.lower_end_fitting.material),
    )

    return GraphiteElement(
        cladding=cladding,
        graphite_meat=graphite_meat,
        upper_end_fitting=upper_end_fitting,
        lower_end_fitting=lower_end_fitting,
        outer_material=Material(coolant),
    )

def build_central_thimble_element(element: NETL.CentralThimble, coolant: openmc.Material) -> CentralThimble:
    """Build a central thimble pincell.

    Parameters
    ----------
    element : NETL.CentralThimble
        Central thimble definition from progression_problems.
    coolant : openmc.Material
        Coolant material inside and outside the thimble.

    Returns
    -------
    CentralThimble
        CoreForge central thimble.
    """
    cladding = CentralThimble.Cladding(
        thickness=element.outer_radius - element.inner_radius,
        outer_radius=element.outer_radius,
        material=Material(element.material),
    )

    return CentralThimble(
        cladding=cladding,
        length=POOL_HEIGHT,
        fill_material=Material(coolant),
        outer_material=Material(coolant),
    )

def build_source_holder_element(element: NETL.SourceHolder, coolant: openmc.Material) -> SourceHolder:
    """Build a source holder core element.

    Parameters
    ----------
    element : NETL.SourceHolder
        Source holder definition from progression_problems.
    coolant : openmc.Material
        Coolant surrounding the cladding.

    Returns
    -------
    SourceHolder
        CoreForge source holder.
    """
    cavity = SourceHolder.Cavity(
        radius=element.cavity.radius,
        length=element.cavity.length,
        material=Material(element.cavity.material),
    )

    cladding = SourceHolder.Cladding(
        outer_radius=element.cladding.outer_radius,
        material=Material(element.cladding.material),
    )

    source_holder_length = UPPER_GRID_PLATE_DISTANCE_FROM_CORE_CENTERLINE + \
                           LOWER_GRID_PLATE_DISTANCE_FROM_CORE_CENTERLINE - \
                           element.distance_from_lower_grid_plate + \
                           UPPER_GRID_PLATE.thickness

    return SourceHolder(
        length=source_holder_length,
        cavity=cavity,
        cladding=cladding,
        outer_material=Material(coolant),
        gap_tolerance=None,
    )

def build_transient_rod_element(element: NETL.TransientRod, coolant: openmc.Material) -> TransientRod:
    """Build a transient rod core element.

    Parameters
    ----------
    element : NETL.TransientRod
        Transient rod definition from progression_problems.
    coolant : openmc.Material
        Coolant surrounding the cladding.

    Returns
    -------
    TransientRod
        CoreForge transient rod element.
    """
    cladding = TransientRod.Cladding(
        thickness=element.cladding.thickness,
        outer_radius=element.cladding.outer_radius,
        material=Material(element.cladding.material),
    )

    absorber = TransientRod.Absorber(
        radius=element.absorber.radius,
        length=element.absorber.length,
        material=Material(element.absorber.material),
    )

    air_follower = TransientRod.AirFollower(thickness=element.air_follower.thickness)

    upper_element_plug = TransientRod.ElementPlug(
        thickness=element.upper_element_plug.thickness,
        material=Material(element.upper_element_plug.material),
    )

    upper_magneform_fitting = TransientRod.MagneformFitting(
        thickness=element.upper_magneform_fitting.thickness,
        material=Material(element.upper_magneform_fitting.material),
    )

    lower_magneform_fitting = TransientRod.MagneformFitting(
        thickness=element.lower_magneform_fitting.thickness,
        material=Material(element.lower_magneform_fitting.material),
    )

    lower_element_plug = TransientRod.ElementPlug(
        thickness=element.lower_element_plug.thickness,
        material=Material(element.lower_element_plug.material),
    )

    return TransientRod(
        cladding=cladding,
        absorber=absorber,
        air_follower=air_follower,
        upper_element_plug=upper_element_plug,
        upper_magneform_fitting=upper_magneform_fitting,
        lower_magneform_fitting=lower_magneform_fitting,
        lower_element_plug=lower_element_plug,
        fill_gas=Material(element.fill_gas),
        outer_material=Material(coolant),
        gap_tolerance=None,
    )

def build_ffcr_element(element: NETL.FuelFollowerControlRod, coolant: openmc.Material) -> FuelFollowerControlRod:
    """Build a fuel-follower control rod element.

    Parameters
    ----------
    element : NETL.FuelFollowerControlRod
        Fuel-follower control rod definition from progression_problems.
    coolant : openmc.Material
        Coolant surrounding the cladding.

    Returns
    -------
    FuelFollowerControlRod
        CoreForge fuel-follower control rod element.
    """
    cladding = FuelFollowerControlRod.Cladding(
        thickness=element.cladding.thickness,
        outer_radius=element.cladding.outer_radius,
        material=Material(element.cladding.material),
    )

    absorber = FuelFollowerControlRod.Absorber(
        radius=element.absorber.radius,
        length=element.absorber.length,
        material=Material(element.absorber.material),
    )

    fuel_follower = FuelFollowerControlRod.FuelFollower(
        inner_radius=element.fuel_follower.inner_radius,
        outer_radius=cladding.inner_radius,
        length=element.fuel_follower.length,
        material=Material(element.fuel_follower.material),
    )

    zr_fill = FuelFollowerControlRod.ZrFillRod(
        radius=element.zr_fill_rod.radius,
        material=Material(element.zr_fill_rod.material),
    )

    upper_element_plug = FuelFollowerControlRod.ElementPlug(
        thickness=element.upper_element_plug.thickness,
        material=Material(element.upper_element_plug.material),
    )

    upper_air_gap = FuelFollowerControlRod.AirGap(thickness=element.upper_air_gap.thickness)

    upper_magneform_fitting = FuelFollowerControlRod.MagneformFitting(
        thickness=element.upper_magneform_fitting.thickness,
        material=Material(element.upper_magneform_fitting.material),
    )

    above_absorber_air_gap = FuelFollowerControlRod.AirGap(
        thickness=element.above_absorber_air_gap.thickness,
    )

    middle_magneform_fitting = FuelFollowerControlRod.MagneformFitting(
        thickness=element.middle_magneform_fitting.thickness,
        material=Material(element.middle_magneform_fitting.material),
    )

    above_fuel_follower_air_gap = FuelFollowerControlRod.AirGap(
        thickness=element.above_fuel_follower_air_gap.thickness,
    )

    lower_magneform_fitting = FuelFollowerControlRod.MagneformFitting(
        thickness=element.lower_magneform_fitting.thickness,
        material=Material(element.lower_magneform_fitting.material),
    )

    lower_air_gap = FuelFollowerControlRod.AirGap(thickness=element.lower_air_gap.thickness)

    lower_element_plug = FuelFollowerControlRod.ElementPlug(
        thickness=element.lower_element_plug.thickness,
        material=Material(element.lower_element_plug.material),
    )

    return FuelFollowerControlRod(
        cladding=cladding,
        absorber=absorber,
        fuel_follower=fuel_follower,
        zr_fill_rod=zr_fill,
        upper_element_plug=upper_element_plug,
        upper_air_gap=upper_air_gap,
        upper_magneform_fitting=upper_magneform_fitting,
        above_absorber_air_gap=above_absorber_air_gap,
        middle_magneform_fitting=middle_magneform_fitting,
        above_fuel_follower_air_gap=above_fuel_follower_air_gap,
        lower_magneform_fitting=lower_magneform_fitting,
        lower_air_gap=lower_air_gap,
        lower_element_plug=lower_element_plug,
        fill_gas=Material(element.fill_gas),
        outer_material=Material(coolant),
        gap_tolerance=None,
    )

def build_element_geometry(element: Optional[NETL.Core.Element],
                           coolant: openmc.Material) -> Core.Element:
    """ Build a CoreForge geometry element for a given TRIGA NETL core element.

    Parameters
    ----------
    element : Optional[NETL.Core.Element]
        The TRIGA core element to build the geometry for.
        If None, this will return a geometry element which is only coolant.
    coolant : openmc.Material
        The coolant material to use in the geometry.

    Returns
    -------
    Core.Element
        The constructed core element geometry.
    """

    if element is None:
        core_element = build_coolant_element(coolant)
    elif isinstance(element, TRIGA.FuelElement):
        core_element = build_fuel_element(element, coolant)
    elif isinstance(element, TRIGA.GraphiteElement):
        core_element = build_graphite_element(element, coolant)
    elif isinstance(element, NETL.CentralThimble):
        core_element = build_central_thimble_element(element, coolant)
    elif isinstance(element, NETL.SourceHolder):
        core_element = build_source_holder_element(element, coolant)
    elif isinstance(element, NETL.TransientRod):
        core_element = build_transient_rod_element(element, coolant)
    elif isinstance(element, NETL.FuelFollowerControlRod):
        core_element = build_ffcr_element(element, coolant)
    else:
        raise ValueError(f"Unsupported element type: {type(element)}")

    return core_element

def build_multicell_geometry(fuel: TRIGA.FuelElement,
                             coolant: openmc.Material,
                             central_element: Optional[NETL.Core.Element]
    ) -> HexLattice:
    """ Build a multicell CoreForge geometry for a fuel design,
        central element, and coolant material.

    Parameters
    ----------
    fuel : TRIGA.FuelElement
        The TRIGA fuel element design to build the fuel cells with.
    coolant : openmc.Material
        The coolant material to use in the multicell geometry.
    central_element : Optional[NETL.Core.Element]
        The central element to include in the multicell geometry.

    Returns
    -------
    HexLattice
        The constructed multicell geometry.
    """

    f = fuel
    c = central_element
    lattice = [[         f,         ],
               [     f,      f,     ],
               [ f,      f,      f, ],
               [     f,      f,     ],
               [ f,      c,      f, ],
               [     f,      f,     ],
               [ f,      f,      f, ],
               [     f,      f,     ],
               [         f,         ]]

    elements = [[build_element_geometry(e, coolant) for e in row] for row in lattice]
    return HexLattice(pitch          = NETL.Core().pitch,
                      outer_material = Material(coolant),
                      elements       = elements,
                      orientation    = 'y')


def build_openmc_model(fuel: TRIGA.FuelElement,
                       coolant: openmc.Material,
                       central_element: Optional[NETL.Core.Element],
                       control_rod_bottom_position: float = 0.0,
                       spectrum_group_structure: str = "MPACT-51"
) -> openmc.model.Model:
    """Build a multicell OpenMC Model.

    Parameters
    ----------
    fuel : TRIGA.FuelElement
        The TRIGA fuel element design to build the fuel cells with.
    coolant : openmc.Material
        The coolant material to use in the multicell geometry.
    central_element : Optional[NETL.Core.Element]
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


def write_mpact_input(fuel: TRIGA.FuelElement,
                      coolant: openmc.Material,
                      central_element: Optional[NETL.Core.Element],
                      xslib: str,
                      fuel_build_specs: Optional[mpact_builder.CylindricalPinCell.Specs] = None,
                      element_build_specs: Optional[mpact_builder.CylindricalPinCell.Specs] = None,
                      filename: str = "mpact.inp",
                      states: List[Dict[str, str]] = [DEFAULT_MPACT_SETTINGS["state"]],
                      xsec_settings: Dict[str, str] = DEFAULT_MPACT_SETTINGS["xsec"],
                      options: Dict[str, str] = DEFAULT_MPACT_SETTINGS["options"]) -> None:
    """Write the MPACT input for a given TRIGA fuel element, coolant, and central element.

    Parameters
    ----------
    fuel : TRIGA.FuelElement
        The TRIGA fuel element to use for building the multicell geometry.
    coolant : openmc.Material
        The coolant material to use in the multicell geometry.
    central_element : Optional[NETL.Core.Element]
        The central element to use for building the multicell geometry.
    xslib : str
        The cross section library file to use in the MPACT input.
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
