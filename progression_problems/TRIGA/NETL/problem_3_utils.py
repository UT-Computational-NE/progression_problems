from typing import List, Optional, Tuple, Dict, Sequence
from dataclasses import dataclass
from math import ceil, cos, radians, sin

import openmc
import mpactpy
from coreforge.materials import Material
from coreforge.shapes import Circle, Hexagon, Rectangle
from coreforge.geometry_elements import HexLattice, InfiniteMedium
from coreforge.geometry_elements.triga.netl import Reactor, Core, RSRCavity
from coreforge import openmc_builder
from coreforge import mpact_builder
from coreforge.mpact_builder.builder import AxisBounds, Bounds
from coreforge.mpact_builder.builder_specs import DEFAULT_MPACT_MATERIAL_SPECS

from progression_problems.TRIGA.NETL.default_geometries import DefaultGeometries as NETL_DefaultGeometries
from progression_problems.TRIGA.NETL.utils import (DEFAULT_MPACT_SETTINGS, build_generic_openmc_tallies,
                                                   default_mpact_material_specs)
from progression_problems.TRIGA.NETL.problem_2_utils import DEFAULT_COOLANT_PINCELL_RADII, build_element_pincell_geometry


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


def build_no_excore(core_lattice: openmc.Universe,
                    pitch:        float) -> openmc.Universe:
    """ Build the OpenMC universe for the TRIGA NETL core without excore features.

    Parameters
    ----------
    core_lattice : openmc.Universe
        The core lattice to use in the universe.
    pitch : float
        Hexagonal lattice pitch used to construct the core lattice.
    """
    boundary_radius = 7.0 * pitch
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
    for beamport_id in (1, 2, 3, 4):
        beamport = reactor.beam_port[beamport_id]
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
                       control_rod_specs: ControlRodSpecs,
                       coolant_pincell_radii: Sequence[float],
                       pitch: float = NETL_DefaultGeometries.core().pitch) -> HexLattice:
    """Build the OpenMC hex lattice for the TRIGA NETL core.

    Parameters
    ----------
    reactor : Reactor
        The TRIGA NETL reactor geometry element.
    coolant : openmc.Material
        The coolant material to use in the core lattice.
    control_rod_specs : ControlRodSpecs
        The specifications for the control rod positions.
    coolant_pincell_radii : Sequence[float]
        Cylindrical mesh radii to use for coolant-only core locations with
        grid plate penetrations.
    pitch : float
        Hexagonal lattice pitch to use for the core lattice. Defaults to the
        NETL core pitch.

    Returns
    -------
    HexLattice
        The Core Forge hex lattice representing the core.
    """

    elements = []
    for location_ring, element_ring in zip(Core.RING_MAP, reactor.core.lattice.elements):
        entries = []
        for location, element in zip(location_ring, element_ring):
            control_rod_inserted = False
            if element is reactor.core.transient_rod:
                control_rod_inserted = control_rod_specs.transient_rod_inserted
            elif element is reactor.core.shim_1_rod:
                control_rod_inserted = control_rod_specs.shim_1_rod_inserted
            elif element is reactor.core.shim_2_rod:
                control_rod_inserted = control_rod_specs.shim_2_rod_inserted
            elif element is reactor.core.regulating_rod:
                control_rod_inserted = control_rod_specs.regulating_rod_inserted

            upper_penetration = reactor.upper_grid_plate.geometry.penetration_map[location]
            lower_penetration = reactor.lower_grid_plate.geometry.penetration_map[location]
            assert (upper_penetration is None) == (lower_penetration is None)

            if element is None and upper_penetration is None:
                entry = InfiniteMedium(Material(coolant), name=f"{location}_core_periphery")
            else:
                entry = build_element_pincell_geometry(
                    element,
                    coolant,
                    control_rod_inserted,
                    coolant_pincell_radii,
                )
            entries.append(entry)
        elements.append(entries)

    return HexLattice(pitch          = pitch,
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
                       control_rod_specs:        Optional[ControlRodSpecs] = None,
                       excore_features:          str = "none",
                       coolant_pincell_radii:    Sequence[float] = DEFAULT_COOLANT_PINCELL_RADII,
                       spectrum_group_structure: str = "MPACT-51",
                       pitch:                    float = NETL_DefaultGeometries.core().pitch) -> openmc.model.Model:
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
    coolant_pincell_radii : Sequence[float]
        Cylindrical mesh radii to use for coolant-only core locations.
    spectrum_group_structure : str
        The energy group structure to use for the multi-group spectrum tally.
    pitch : float
        Hexagonal lattice pitch to use for the core lattice. Defaults to the
        NETL core pitch.

    Returns
    -------
    openmc.model.Model
        The constructed OpenMC model.
    """

    control_rod_specs = control_rod_specs or ControlRodSpecs()

    assert excore_features in ["none", "beamports", "rsr"], \
        f"Invalid excore_features option: {excore_features}. Must be one of 'none', 'beamports', or 'rsr'."

    core_lattice   = build_core_lattice(reactor, coolant, control_rod_specs, coolant_pincell_radii, pitch)
    core_lattice   = openmc_builder.build(core_lattice)

    if excore_features == "none":
        root_universe = build_no_excore(core_lattice, pitch)
    elif excore_features == "beamports":
        root_universe = build_beamport_excore(reactor, core_lattice)
    else:
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



def write_mpact_input(reactor:             Reactor,
                      coolant:             openmc.Material,
                      control_rod_specs:   Optional[ControlRodSpecs] = None,
                      excore_features:     str = "none",
                      coolant_pincell_radii: Sequence[float] = DEFAULT_COOLANT_PINCELL_RADII,
                      pitch:               float = NETL_DefaultGeometries.core().pitch,
                      reactor_build_specs: Optional[mpact_builder.triga.netl.Reactor.Specs] = None,
                      filename:            str = "mpact.inp",
                      states:              Optional[List[Dict[str, str]]] = None,
                      xsec_settings:       Optional[Dict[str, str]] = None,
                      options:             Optional[Dict[str, str]] = None) -> None:
    """Write an MPACT input file for the TRIGA NETL reactor.

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
    coolant_pincell_radii : Sequence[float]
        Cylindrical mesh radii to use for coolant-only core locations.
    pitch : float
        Hexagonal lattice pitch to use for the core lattice. Defaults to the
        NETL core pitch.
    reactor_build_specs : Optional[mpact_builder.triga.netl.Reactor.Specs]
        The specifications for building the MPACT reactor geometry. If None, default specs are used.
    filename : str
        The filename to write the MPACT input to. (Default: "mpact.inp")
    states : List[Dict[str, str]]
        The state settings to use in the MPACT input.
    xsec_settings : Dict[str, str]
        The cross section settings to use in the MPACT input.
    options : Dict[str, str]
        The options settings to use in the MPACT input.
    """

    specs = reactor_build_specs or mpact_builder.triga.netl.Reactor.Specs()

    default_mat_specs    = default_mpact_material_specs(reactor.get_materials())
    specs.material_specs = specs.material_specs or default_mat_specs

    control_rod_specs = control_rod_specs or ControlRodSpecs()

    assert excore_features in ["none", "beamports", "rsr"], \
        f"Invalid excore_features option: {excore_features}. Must be one of 'none', 'beamports', or 'rsr'."

    geometry = _build_mpact_geometry(
        reactor,
        coolant,
        control_rod_specs,
        excore_features,
        coolant_pincell_radii,
        pitch,
        specs,
    )
    states = [dict(state) for state in (states or [DEFAULT_MPACT_SETTINGS["state"]])]
    xsec_settings = dict(xsec_settings or DEFAULT_MPACT_SETTINGS["xsec"])
    options = dict(options or DEFAULT_MPACT_SETTINGS["options"])
    for state in states:
        state["tinlet"] = state.get("tinlet", f"{reactor.pool.material.temperature}")
    options["bound_cond"] = "0 0 0 0 1 1"

    mpact_model = mpactpy.Model(geometry, states, xsec_settings, options)
    with open(filename, "w") as file:
        file.write(mpact_model.write_to_string("TRIGA", indent=4))



def _build_mpact_geometry(reactor:             Reactor,
                          coolant:             openmc.Material,
                          control_rod_specs:   ControlRodSpecs,
                          excore_features:     str,
                          coolant_pincell_radii: Sequence[float],
                          pitch:               float,
                          reactor_build_specs: mpact_builder.triga.netl.Reactor.Specs) -> mpactpy.Core:

    openmc_model = build_openmc_model(reactor,
                                      coolant,
                                      control_rod_specs,
                                      excore_features,
                                      coolant_pincell_radii,
                                      pitch=pitch)
    openmc_universe = openmc_model.geometry.root_universe

    lattice = build_core_lattice(reactor, coolant, control_rod_specs, coolant_pincell_radii, pitch)

    element_specs = {}
    for i, ring in enumerate(Core.RING_MAP):
        for j, loc in enumerate(ring):
            element = reactor.core.full_map.get(loc, None)
            specs   = reactor_build_specs.core_specs.get(loc, None)

            if specs:
                if element:
                    specs = specs.element_specs
                    if isinstance(specs, mpact_builder.triga.FuelElement.Specs):
                        specs = specs.fuel.builder_specs
                    elif isinstance(specs, mpact_builder.triga.GraphiteElement.Specs):
                        specs = specs.graphite.builder_specs
                    elif isinstance(specs, mpact_builder.triga.netl.CentralThimble.Specs):
                        specs = specs.pincell_specs
                    elif isinstance(specs, mpact_builder.triga.netl.SourceHolder.Specs):
                        specs = specs.cavity.builder_specs
                    elif isinstance(specs, mpact_builder.triga.netl.TransientRod.Specs):
                        specs = specs.absorber.builder_specs if control_rod_specs.transient_rod_inserted else \
                                specs.air_follower.builder_specs
                    elif isinstance(specs, mpact_builder.triga.netl.FuelFollowerControlRod.Specs):
                        if element is reactor.core.shim_1_rod:
                            specs = specs.absorber.builder_specs if control_rod_specs.shim_1_rod_inserted else \
                                    specs.fuel_follower.builder_specs
                        elif element is reactor.core.shim_2_rod:
                            specs = specs.absorber.builder_specs if control_rod_specs.shim_2_rod_inserted else \
                                    specs.fuel_follower.builder_specs
                        elif element is reactor.core.regulating_rod:
                            specs = specs.absorber.builder_specs if control_rod_specs.regulating_rod_inserted else \
                                    specs.fuel_follower.builder_specs
                else:
                    outer_region_specs = specs.outer_region_specs
                    assert (isinstance(outer_region_specs, (mpact_builder.triga.CoreElement.SegmentSpecs,
                                                            mpact_builder.triga.netl.Reactor.VoxelizedSegmentSpecs)))
                    specs = outer_region_specs.builder_specs

            lattice_element = lattice.elements[i][j]
            if specs is None:
                specs = (mpact_builder.InfiniteMedium.Specs()
                         if isinstance(lattice_element, InfiniteMedium)
                         else mpact_builder.CylindricalPinCell.Specs())
            specs.material_specs = reactor_build_specs.material_specs | specs.material_specs
            element_specs[lattice_element] = specs

    lattice_specs = mpact_builder.HexLattice.Specs(element_specs = element_specs,
                                                   num_procs     = reactor_build_specs.num_procs)

    mpact_core = mpact_builder.build(lattice, lattice_specs)

    return _apply_openmc_overlay(mpact_core, openmc_universe, reactor, reactor_build_specs, excore_features)



def _apply_openmc_overlay(core:                mpactpy.Core,
                          openmc_universe:     openmc.Universe,
                          reactor:             Reactor,
                          reactor_build_specs: mpact_builder.triga.netl.Reactor.Specs,
                          excore_features:     str
) -> mpactpy.Core:

    core = _add_excore_cells(core, reactor_build_specs, reactor, excore_features)

    # Only overlay pins/modules/lattices/assemblies that contain voxelized pins
    pins_to_overlay = {pin for pin in core.pins if isinstance(pin.pinmesh, mpactpy.RectangularPinMesh)}
    modules_to_overlay = {m for m in core.modules if pins_to_overlay.intersection(m.pins)}
    lattices_to_overlay = {l for l in core.lattices if modules_to_overlay.intersection(l.modules)}
    assemblies_to_overlay = {a for a in core.assemblies if lattices_to_overlay.intersection(a.lattices)}

    # Create overlay masks
    pin_mask:      mpactpy.Pin.OverlayMask      = set(core.materials)
    module_mask:   mpactpy.Module.OverlayMask   = {pin:      pin_mask      for pin      in pins_to_overlay}
    lattice_mask:  mpactpy.Lattice.OverlayMask  = {module:   module_mask   for module   in modules_to_overlay}
    assembly_mask: mpactpy.Assembly.OverlayMask = {lattice:  lattice_mask  for lattice  in lattices_to_overlay}
    include_only:  mpactpy.Core.OverlayMask     = {assembly: assembly_mask for assembly in assemblies_to_overlay}

    overlay_policy = mpactpy.PinMesh.OverlayPolicy(num_procs=reactor_build_specs.num_procs)

    # Map MPACT materials specs to OpenMC materials
    default_material_specs   = {material: DEFAULT_MPACT_MATERIAL_SPECS[type(material)]
                                for material in reactor.get_materials() if type(material) in DEFAULT_MPACT_MATERIAL_SPECS}
    material_specs           = default_material_specs | reactor_build_specs.material_specs
    material_specs           = {material.name: material_specs[material] for material in material_specs.keys()}
    openmc_materials         = openmc.Materials(list(openmc_universe.get_all_materials().values()))
    overlay_policy.mat_specs = {material: material_specs[material.name]
                                for material in openmc_materials if material.name in material_specs}

    offset = reactor_build_specs.offset or (-core.width["X"] * 0.5,
                                            -core.width["Y"] * 0.5,
                                            -core.height * 0.5)

    return core.overlay(openmc.Geometry(openmc_universe), offset, include_only, overlay_policy)


def _add_excore_cells(core:                mpactpy.Core,
                      reactor_build_specs: mpact_builder.triga.netl.Reactor.Specs,
                      reactor:             Reactor,
                      excore_features:     str) -> mpactpy.Core:

    core_map = core.assembly_map
    if not core_map:
        return core

    outer_boundary_radius = 7.0 * reactor.core.pitch if excore_features == "none" else reactor.pool.radius

    row_pitch = next((pitch for pitch in core.pitch["row"] if pitch > 0.0), None)
    col_pitch = next((pitch for pitch in core.pitch["column"] if pitch > 0.0), None)
    assert row_pitch is not None and col_pitch is not None, \
        "MPACT core must have non-zero row and column pitch to add excore cells."

    pad_cols = max(0, ceil((outer_boundary_radius - core.width["X"] * 0.5) / col_pitch))
    pad_rows = max(0, ceil((outer_boundary_radius - core.width["Y"] * 0.5) / row_pitch))
    if pad_rows == 0 and pad_cols == 0:
        return core

    num_rows = len(core_map)
    num_cols = len(core_map[0])
    padded_rows = num_rows + 2 * pad_rows
    padded_cols = num_cols + 2 * pad_cols
    padded_map = [[None for _ in range(padded_cols)]
                  for _ in range(padded_rows)]

    for row_index, row in enumerate(core_map):
        padded_map[row_index + pad_rows][pad_cols:pad_cols + num_cols] = row

    total_width_x = padded_cols * col_pitch
    total_width_y = padded_rows * row_pitch

    for row_index, row in enumerate(padded_map):
        y_center = total_width_y * 0.5 - (row_index + 0.5) * row_pitch
        for col_index, assembly in enumerate(row):
            x_center = (col_index + 0.5) * col_pitch - total_width_x * 0.5
            row[col_index] = _set_cell(assembly,
                                       (col_pitch, row_pitch),
                                       (x_center, y_center),
                                       reactor,
                                       reactor_build_specs,
                                       excore_features,
                                       outer_boundary_radius)
    return mpactpy.Core(padded_map,
                        symmetry_opt=core.symmetry_opt,
                        quarter_sym_opt=core.quarter_sym_opt,
                        min_thickness=reactor_build_specs.min_thickness)


def _set_cell(assembly:            Optional[mpactpy.Assembly],
              side_lengths:        Tuple[float, float],
              radial_location:     Tuple[float, float],
              reactor:             Reactor,
              reactor_build_specs: mpact_builder.triga.netl.Reactor.Specs,
              excore_features:     str,
              outer_boundary_radius: float
    ) -> Optional[mpactpy.Assembly]:

    rect = Rectangle(w=side_lengths[0], h=side_lengths[1])
    if reactor.shroud.contains(rect, radial_location) and assembly is not None:
        return assembly

    if not Circle(outer_boundary_radius).contains(rect, other_center=radial_location):
        return None

    excore_specs = reactor_build_specs.excore_specs

    target_thicknesses: List[float] = []
    if excore_features in ["rsr", "beamports"]:
        if reactor.shroud.intersects(rect, radial_location):
            target_thicknesses.append(excore_specs.shroud.radial)
        if excore_features == "rsr" and reactor.rsr_cavity_intersects(rect, radial_location):
            target_thicknesses.append(excore_specs.rsr_cavity.radial)
        if excore_features == "rsr" and reactor.rsr_tube_intersects(rect, radial_location):
            target_thicknesses.append(excore_specs.rsr_tube.radial)
        if reactor.reflector_intersects(rect, radial_location):
            target_thicknesses.append(excore_specs.reflector.radial)
        if excore_features == "beamports":
            for bp in (1, 2, 3, 4):
                if reactor.beam_port[bp].intersects(rect, radial_location):
                    if reactor.beam_port[bp].contains(rect, radial_location):
                        target_thicknesses.append(excore_specs.beamport_interior.radial)
                    else:
                        target_thicknesses.append(excore_specs.beamport_exterior.radial)

    if not target_thicknesses:
        target_thicknesses.append(excore_specs.pool.radial)

    target_thickness = min(target_thicknesses)
    voxel_build_specs = mpact_builder.InfiniteMedium.Specs(
        target_cell_thicknesses = {"X": target_thickness,
                                   "Y": target_thickness},
        divide_materials        = True,
        material_specs          = reactor_build_specs.material_specs,
    )
    voxel_bounds = Bounds(
        X = AxisBounds(min=0.0, max=side_lengths[0]),
        Y = AxisBounds(min=0.0, max=side_lengths[1]),
        Z = AxisBounds(min=0.0, max=1.0),
    )
    voxel = InfiniteMedium(reactor.pool.material, name="excore_voxel")
    lattice = mpact_builder.build(voxel, voxel_build_specs, voxel_bounds).lattices[0]
    return mpactpy.Assembly([lattice])
