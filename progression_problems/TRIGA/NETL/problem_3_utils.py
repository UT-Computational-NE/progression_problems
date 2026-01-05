from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from math import cos, radians, sin

import openmc
import mpactpy
from coreforge.materials import Material
from coreforge.geometry_elements import HexLattice
from coreforge.geometry_elements.triga.netl import Reactor, RSRCavity
from coreforge.shapes import Hexagon
from coreforge import openmc_builder
from coreforge import mpact_builder

from progression_problems.TRIGA.default_geometries import DefaultGeometries as TRIGA_DefaultGeometries
from progression_problems.TRIGA.NETL.default_geometries import DefaultGeometries as NETL_DefaultGeometries
from progression_problems.TRIGA.NETL.utils import build_generic_openmc_tallies, DEFAULT_MPACT_SETTINGS
from progression_problems.TRIGA.NETL.problem_2_utils import build_element_pincell_geometry


@dataclass
class ControlRodSpecs:
    """ Specifications for the control rod positions for Problem 3

    Attributes
    ----------
    transient_rod_inserted:  bool
        Whether the transient control rod is inserted.
    shim_1_rod_inserted:     bool
        Whether the shim 1 control rod is inserted.
    shim_2_rod_inserted:     bool
        Whether the shim 2 control rod is inserted.
    regulating_rod_inserted: bool
        Whether the regulating control rod is inserted.
    """
    transient_rod_inserted:  bool = False
    shim_1_rod_inserted:     bool = False
    shim_2_rod_inserted:     bool = False
    regulating_rod_inserted: bool = False


def build_no_excore(reactor:      Reactor,
                    core_lattice: openmc.Universe) -> openmc.Universe:
    """ Build the OpenMC universe for the TRIGA NETL core without excore features.

    Parameters
    ----------
    reactor : Reactor
        The TRIGA NETL reactor geometry element.
    core_lattice : openmc.Universe
        The core lattice to use in the universe.
    """
    boundary_radius = 7.0 * reactor.core.lattice.pitch
    radial_boundary = openmc.ZCylinder(r=boundary_radius, boundary_type="vacuum")
    top_boundary    = openmc.ZPlane(z0=0.5, boundary_type="reflective")
    bottom_boundary = openmc.ZPlane(z0=-0.5, boundary_type="reflective")
    axial_region    = +bottom_boundary & -top_boundary

    lattice_cell = openmc.Cell(fill=core_lattice, region=-radial_boundary & axial_region)
    return openmc.Universe(cells=[lattice_cell])


def build_beamport_excore(reactor:      Reactor,
                          core_lattice: openmc.Universe) -> openmc.Universe:
    """ Build the OpenMC universe for the TRIGA NETL core with beamport excore features.

    Parameters
    ----------
    reactor : Reactor
        The TRIGA NETL reactor geometry element.
    core_lattice : openmc.Universe
        The core lattice to use in the universe.
    """
    pool_universe = build_pool_universe(reactor, core_lattice)

    pool_boundary   = openmc.ZCylinder(r=reactor.pool.radius, boundary_type="vacuum")
    top_boundary    = openmc.ZPlane(z0=0.5, boundary_type="reflective")
    bottom_boundary = openmc.ZPlane(z0=-0.5, boundary_type="reflective")
    axial_region    = +bottom_boundary & -top_boundary

    pool_region = -pool_boundary

    def build_beam_port_regions(beamport: Reactor.BeamPort
    ) -> Tuple[openmc.Region, openmc.Region]:
        def rectangular_region(width: float, height: float) -> openmc.Region:
            half_width  = width * 0.5
            half_height = height * 0.5

            x_min = openmc.XPlane(x0 = -half_width)
            x_max = openmc.XPlane(x0 =  half_width)
            y_min = openmc.YPlane(y0 = -half_height)
            y_max = openmc.YPlane(y0 =  half_height)

            surfaces = [x_min, x_max, y_min, y_max]
            if beamport.rotation:
                surfaces = [surface.rotate((0.0, 0.0, beamport.rotation)) for surface in surfaces]

            translation = (beamport.translation[0], beamport.translation[1], 0.0)
            if translation != (0.0, 0.0, 0.0):
                surfaces = [surface.translate(translation) for surface in surfaces]

            x_min, x_max, y_min, y_max = surfaces
            return +x_min & -x_max & +y_min & -y_max

        inner_region = rectangular_region(beamport.geometry.length,
                                          beamport.geometry.inner_radius * 2.0)
        outer_region = rectangular_region(beamport.geometry.length,
                                          beamport.geometry.outer_radius * 2.0)
        return inner_region, outer_region

    cells = []
    for beamport in [reactor.beam_port_1_5, reactor.beam_port_2,
                     reactor.beam_port_3,   reactor.beam_port_4]:
        inner_region, outer_region = build_beam_port_regions(beamport)

        cells.append(openmc.Cell(fill   = beamport.geometry.fill_material.openmc_material,
                                 region = inner_region & -pool_boundary & axial_region,
                                 name   = beamport.geometry.name + "_fill"))
        cells.append(openmc.Cell(fill   = beamport.geometry.tube_material.openmc_material,
                                 region = outer_region & ~inner_region & -pool_boundary & axial_region,
                                 name   = beamport.geometry.name + "_tube"))
        pool_region &= ~outer_region

    cells.append(openmc.Cell(fill = pool_universe, region = pool_region & axial_region, name="reactor_pool"))
    return openmc.Universe(cells=cells)


def build_rsr_excore(reactor:      Reactor,
                     core_lattice: openmc.Universe) -> openmc.Universe:
    """ Build the OpenMC universe for the TRIGA NETL core with RSR excore features.

    Parameters
    ----------
    reactor : Reactor
        The TRIGA NETL reactor geometry element.
    core_lattice : openmc.Universe
        The core lattice to use in the universe.
    """
    pool_universe = build_pool_universe(reactor, core_lattice)

    pool_boundary   = openmc.ZCylinder(r=reactor.pool.radius, boundary_type="vacuum")
    top_boundary    = openmc.ZPlane(z0=0.5, boundary_type="reflective")
    bottom_boundary = openmc.ZPlane(z0=-0.5, boundary_type="reflective")
    axial_region    = +bottom_boundary & -top_boundary

    pool_region = -pool_boundary

    rsr                = reactor.rotary_specimen_rack_cavity
    rsr_outer_cylinder = openmc.ZCylinder(r=rsr.outer_radius)

    shroud            = reactor.shroud
    primary_hex_shape = Hexagon(inner_radius=shroud.primary_hex_inner_radius + shroud.thickness)
    rotated_hex_shape = Hexagon(inner_radius=shroud.rotated_hex_inner_radius + shroud.thickness)
    primary_hex       = openmc.model.HexagonalPrism(edge_length = primary_hex_shape.outer_radius,
                                                     orientation = 'y')
    rotated_hex       = openmc.model.HexagonalPrism(edge_length = rotated_hex_shape.outer_radius,
                                                    orientation = 'y').rotate((0, 0, 30))
    shroud_region     = -primary_hex & -rotated_hex

    rsr_region         = -rsr_outer_cylinder & ~shroud_region

    rsr_universe = build_rsr_universe(rsr, rsr_region)
    rsr_cell     = openmc.Cell(fill   = rsr_universe,
                               region = rsr_region & pool_region & axial_region,
                               name   = "rsr_cavity")
    pool_cell    = openmc.Cell(fill   = pool_universe,
                               region = pool_region & axial_region & ~rsr_region,
                               name   = "reactor_pool")
    return openmc.Universe(cells=[rsr_cell, pool_cell])


def build_core_lattice(reactor: Reactor,
                       coolant: openmc.Material,
                       control_rod_specs: ControlRodSpecs) -> HexLattice:
    """Build the OpenMC hex lattice for the TRIGA NETL core.

    Parameters
    ----------
    reactor : Reactor
        The TRIGA NETL reactor geometry element.
    coolant : openmc.Material
        The coolant material to use in the core lattice.
    control_rod_specs : ControlRodSpecs
        The specifications for the control rod positions.

    Returns
    -------
    openmc.HexLattice
        The OpenMC hex lattice representing the core.
    """

    elements = []
    for ring in reactor.core.lattice.elements:
        entries = []
        for element in ring:
            control_rod_inserted = False
            if element is reactor.core.transient_rod:
                control_rod_inserted = control_rod_specs.transient_rod_inserted
            elif element is reactor.core.shim_1_rod:
                control_rod_inserted = control_rod_specs.shim_1_rod_inserted
            elif element is reactor.core.shim_2_rod:
                control_rod_inserted = control_rod_specs.shim_2_rod_inserted
            elif element is reactor.core.regulating_rod:
                control_rod_inserted = control_rod_specs.regulating_rod_inserted
            pincell = build_element_pincell_geometry(element, coolant, control_rod_inserted)
            entries.append(pincell)
        elements.append(entries)

    return HexLattice(pitch          = NETL_DefaultGeometries.core().pitch,
                      outer_material = Material(coolant),
                      elements       = elements,
                      orientation    = 'y',
                      map_type       = 'ring')


def build_pool_universe(reactor:      Reactor,
                        core_lattice: openmc.Universe) -> openmc.Universe:
    """Build an OpenMC universe for the pool, reflector, and shroud region.

    Parameters
    ----------
    reactor : Reactor
        The TRIGA NETL reactor geometry element.
    core_lattice : openmc.Universe
        The core lattice to embed inside the shroud.

    Returns
    -------
    openmc.Universe
        Universe containing shroud, reflector, and pool regions.
    """
    shroud    = reactor.shroud
    reflector = reactor.reflector.geometry

    primary_hex_shape = Hexagon(inner_radius=shroud.primary_hex_inner_radius + shroud.thickness)
    rotated_hex_shape = Hexagon(inner_radius=shroud.rotated_hex_inner_radius + shroud.thickness)

    primary_hex = openmc.model.HexagonalPrism(edge_length = primary_hex_shape.outer_radius,
                                              orientation = "y")
    rotated_hex = openmc.model.HexagonalPrism(edge_length = rotated_hex_shape.outer_radius,
                                              orientation = "y").rotate((0.0, 0.0, 30.0))
    shroud_region = -primary_hex & -rotated_hex

    cells = []
    cells.append(openmc.Cell(fill   = build_shroud_universe(reactor, core_lattice),
                             region = shroud_region,
                             name   = "shroud"))

    reflector_cylinder = openmc.ZCylinder(r=reflector.radius)
    reflector_region   = -reflector_cylinder & ~shroud_region

    cells.append(openmc.Cell(fill   = reflector.material.openmc_material,
                             region = reflector_region,
                             name   = "reflector"))

    pool_region = +reflector_cylinder
    cells.append(openmc.Cell(fill   = reactor.pool.material.openmc_material,
                             region = pool_region,
                             name   = "pool"))

    return openmc.Universe(cells=cells)


def build_shroud_universe(reactor:      Reactor,
                          core_lattice: openmc.Universe) -> openmc.Universe:
    """Build an OpenMC universe for the shroud and core interior.

    Parameters
    ----------
    reactor : Reactor
        The TRIGA NETL reactor geometry element.
    core_lattice : openmc.Universe
        The core lattice to place inside the shroud.

    Returns
    -------
    openmc.Universe
        Universe containing the core lattice and shroud wall.
    """
    shroud        = reactor.shroud

    primary_hex_shape = Hexagon(inner_radius=shroud.primary_hex_inner_radius)
    rotated_hex_shape = Hexagon(inner_radius=shroud.rotated_hex_inner_radius)

    primary_hex = openmc.model.HexagonalPrism(edge_length = primary_hex_shape.outer_radius,
                                              orientation = "y")
    rotated_hex = openmc.model.HexagonalPrism(edge_length = rotated_hex_shape.outer_radius,
                                              orientation = "y").rotate((0.0, 0.0, 30.0))
    inner_region = -primary_hex & -rotated_hex

    primary_hex_shape = Hexagon(inner_radius=shroud.primary_hex_inner_radius + shroud.thickness)
    rotated_hex_shape = Hexagon(inner_radius=shroud.rotated_hex_inner_radius + shroud.thickness)

    primary_hex = openmc.model.HexagonalPrism(edge_length = primary_hex_shape.outer_radius,
                                              orientation = "y")
    rotated_hex = openmc.model.HexagonalPrism(edge_length = rotated_hex_shape.outer_radius,
                                              orientation = "y").rotate((0.0, 0.0, 30.0))
    shroud_region = -primary_hex & -rotated_hex & ~inner_region

    cells = []
    cells.append(openmc.Cell(fill   = core_lattice,
                             region = inner_region,
                             name   = "core_lattice"))
    cells.append(openmc.Cell(fill   = shroud.material.openmc_material,
                             region = shroud_region,
                             name   = "shroud"))

    return openmc.Universe(cells=cells)


def build_rsr_universe(rsr: RSRCavity,
                       rsr_region: openmc.Region) -> openmc.Universe:
    """Build an OpenMC universe for the rotary specimen rack (RSR) cavity.

    Parameters
    ----------
    rsr : RSRCavity
        The RSR cavity geometry element.
    rsr_region : openmc.Region
        Region defining the outer boundary of the cavity.

    Returns
    -------
    openmc.Universe
        Universe containing specimen tubes and cavity fill.
    """
    r               = rsr.tube_to_center_distance
    number_of_tubes = rsr.number_of_tubes
    d_theta         = 360.0 / number_of_tubes
    outer_radius    = rsr.tube_specs.outer_radius
    inner_radius    = outer_radius - rsr.tube_specs.thickness

    cavity_fill_material = rsr.material.openmc_material
    tube_clad_material   = rsr.tube_specs.material.openmc_material

    cells          = []
    outside_region = None
    for i in range(1, number_of_tubes + 1):
        angle = 90.0 + (i - 1) * -d_theta
        x     = r * cos(radians(angle))
        y     = r * sin(radians(angle))
        tube  = f"rsr_tube_{i:02d}"

        inner_surface = openmc.ZCylinder(r=inner_radius, x0=x, y0=y, name=tube + "_id")
        outer_surface = openmc.ZCylinder(r=outer_radius, x0=x, y0=y, name=tube + "_od")
        cells.append(openmc.Cell(fill   = cavity_fill_material,
                                 region = -inner_surface & rsr_region,
                                 name   = tube + "_fill"))
        cells.append(openmc.Cell(fill   = tube_clad_material,
                                 region = -outer_surface & +inner_surface & rsr_region,
                                 name   = tube + "_clad"))
        outside_region = (
            +outer_surface if outside_region is None else outside_region & +outer_surface
        )

    cavity_region = rsr_region & outside_region if outside_region is not None else rsr_region
    cells.append(openmc.Cell(fill   = cavity_fill_material,
                             region = cavity_region,
                             name   = "rsr_cavity_fill"))

    return openmc.Universe(cells=cells)


def build_openmc_model(reactor:                  Reactor,
                       coolant:                  openmc.Material,
                       control_rod_specs:        ControlRodSpecs = ControlRodSpecs(),
                       excore_features:          str = "none",
                       spectrum_group_structure: str = "MPACT-51") -> openmc.model.Model:
    """Build a multicell OpenMC Model.

    Parameters
    ----------
    reactor: Reactor
        The TRIGA NETL reactor geometry element.
    coolant : openmc.Material
        The coolant material to use in the core lattice.
    control_rod_specs : ControlRodSpecs
        The specifications for the control rod positions. Defaults to all rods withdrawn.
    excore_features : str, optional
        The excore features to include in the model. Options are "none", "beamports", and "rsr"
    spectrum_group_structure : str
        The energy group structure to use for the multi-group spectrum tally.

    Returns
    -------
    openmc.model.Model
        The constructed OpenMC model.
    """

    assert excore_features in ["none", "beamports", "rsr"], \
        f"Invalid excore_features option: {excore_features}. Must be one of 'none', 'beamports', or 'rsr'."

    core_lattice   = build_core_lattice(reactor, coolant, control_rod_specs)
    core_lattice   = openmc_builder.build(core_lattice)

    if excore_features == "none":
        root_universe = build_no_excore(reactor, core_lattice)
    if excore_features == "beamports":
        root_universe = build_beamport_excore(reactor, core_lattice)
    if excore_features == "rsr":
        root_universe = build_rsr_excore(reactor, core_lattice)
    geometry      = openmc.Geometry(root_universe)
    materials     = openmc.Materials(list(geometry.get_all_materials().values()))

    settings           = openmc.Settings()
    settings.batches   = 100
    settings.inactive  = 20
    settings.particles = 10000

    universes = list(core_lattice.get_all_universes().keys())
    tallies   = build_generic_openmc_tallies(spectrum_group_structure, universes)
    tallies   = openmc.Tallies(list(tallies.values()))

    return openmc.model.Model(geometry=geometry, materials=materials, settings=settings, tallies=tallies)
