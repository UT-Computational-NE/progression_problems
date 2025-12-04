
from typing import Dict, List, Optional

import openmc
import mpactpy
from coreforge.geometry_elements import HexLattice
from coreforge.geometry_elements import CylindricalPinCell
from coreforge.geometry_elements.triga import FuelElement, GraphiteElement
from coreforge.geometry_elements.triga.netl import CentralThimble, SourceHolder, TransientRod, FuelFollowerControlRod
from coreforge.materials import Material
from coreforge import openmc_builder
from coreforge import mpact_builder

from progression_problems import TRIGA
from progression_problems.TRIGA import NETL
from progression_problems.TRIGA.NETL.problem_1_utils \
    import lattice_dims, build_fuel_pincell
from progression_problems.TRIGA.NETL.utils import DEFAULT_MPACT_SETTINGS

def build_coolant_pincell(coolant: openmc.Material) -> CylindricalPinCell:
    """Build a coolant-only pincell using fuel element dimensions.

    Parameters
    ----------
    coolant : openmc.Material
        Coolant material to fill all regions.

    Returns
    -------
    CylindricalPinCell
        Coolant pincell shaped like the fuel geometry.
    """
    filler = TRIGA.FuelElement()
    cladding = FuelElement.Cladding(
        thickness=filler.cladding.thickness,
        outer_radius=filler.cladding.outer_radius,
        material=Material(coolant),
    )

    fuel_meat = FuelElement.FuelMeat(
        inner_radius=filler.fuel_meat.inner_radius,
        outer_radius=filler.fuel_meat.outer_radius,
        length=filler.fuel_meat.length,
        material=Material(coolant),
    )

    zr_fill = FuelElement.ZrFillRod(radius=filler.zr_fill_rod.radius, material=Material(coolant))

    return FuelElement.build_fuel_meat_pincell(
        cladding=cladding,
        fuel_meat=fuel_meat,
        zr_fill_rod=zr_fill,
        fill_gas=Material(coolant),
        outer_material=Material(coolant))

def build_graphite_pincell(element: TRIGA.GraphiteElement, coolant: openmc.Material) -> CylindricalPinCell:
    """Build a graphite element pincell.

    Parameters
    ----------
    element : TRIGA.GraphiteElement
        Graphite element definition from progression_problems.
    coolant : openmc.Material
        Coolant material surrounding the cladding.

    Returns
    -------
    CylindricalPinCell
        CoreForge graphite pincell.
    """
    cladding = GraphiteElement.Cladding(
        thickness=element.cladding.thickness,
        outer_radius=element.cladding.outer_radius,
        material=Material(element.cladding.material),
    )

    meat = GraphiteElement.GraphiteMeat(
        outer_radius=element.graphite_meat.outer_radius,
        length=element.graphite_meat.length,
        material=Material(element.graphite_meat.material),
    )

    return GraphiteElement.build_graphite_meat_pincell(
        cladding=cladding,
        graphite_meat=meat,
        outer_material=Material(coolant)
    )

def build_central_thimble_pincell(element: NETL.CentralThimble, coolant: openmc.Material) -> CylindricalPinCell:
    """Build a central thimble pincell.

    Parameters
    ----------
    element : NETL.CentralThimble
        Central thimble definition from progression_problems.
    coolant : openmc.Material
        Coolant material inside and outside the thimble.

    Returns
    -------
    CylindricalPinCell
        CoreForge central thimble pincell.
    """
    thimble = CentralThimble.Cladding(
        thickness=element.outer_radius - element.inner_radius,
        outer_radius=element.outer_radius,
        material=Material(element.material),
    )

    return CentralThimble.build_thimble_pincell(
        cladding=thimble,
        fill_material=Material(coolant),
        outer_material=Material(coolant),
    )

def build_source_holder_pincell(element: NETL.SourceHolder, coolant: openmc.Material) -> CylindricalPinCell:
    """Build a source holder pincell (cavity + cladding).

    Parameters
    ----------
    element : NETL.SourceHolder
        Source holder definition from progression_problems.
    coolant : openmc.Material
        Coolant surrounding the cladding.

    Returns
    -------
    CylindricalPinCell
        CoreForge source holder pincell.
    """
    cavity = SourceHolder.Cavity(radius   = element.cavity.radius,
                                 length   = element.cavity.length,
                                 material = Material(element.cavity.material))

    cladding = SourceHolder.Cladding(outer_radius = element.cladding.outer_radius,
                                     material     = Material(element.cladding.material))

    return SourceHolder.build_cavity_pincell(
        cavity=cavity,
        cladding=cladding,
        outer_material=Material(coolant),
        gap_tolerance=None,
    )

def build_transient_rod_pincell(element: NETL.TransientRod, coolant: openmc.Material) -> CylindricalPinCell:
    """Build a transient rod pincell (absorber or air follower).

    Parameters
    ----------
    element : NETL.TransientRod
        Transient rod definition from progression_problems.
    coolant : openmc.Material
        Coolant surrounding the cladding.

    Returns
    -------
    CylindricalPinCell
        CoreForge transient rod pincell for absorber or air-follower section.
    """
    cladding = TransientRod.Cladding(
        thickness=element.cladding.thickness,
        outer_radius=element.cladding.outer_radius,
        material=Material(element.cladding.material),
    )

    if element.fraction_withdrawn > 0.0:
        return TransientRod.build_air_follower_pincell(
            cladding=cladding,
            fill_gas=Material(element.fill_gas),
            outer_material=Material(coolant),
        )

    absorber = TransientRod.Absorber(
        radius=element.absorber.radius,
        material=Material(element.absorber.material),
    )

    return TransientRod.build_absorber_pincell(
        cladding=cladding,
        absorber=absorber,
        fill_gas=Material(element.fill_gas),
        outer_material=Material(coolant),
        gap_tolerance=None,
    )

def build_ffcr_pincell(element: NETL.FuelFollowerControlRod, coolant: openmc.Material) -> CylindricalPinCell:
    """Build a fuel-follower control rod pincell (absorber or follower section).

    Parameters
    ----------
    element : NETL.FuelFollowerControlRod
        Fuel-follower control rod definition from progression_problems.
    coolant : openmc.Material
        Coolant surrounding the cladding.

    Returns
    -------
    CylindricalPinCell
        CoreForge pincell for the requested control rod state.
    """
    cladding = FuelFollowerControlRod.Cladding(
        thickness=element.cladding.thickness,
        outer_radius=element.cladding.outer_radius,
        material=Material(element.cladding.material),
    )

    if element.fraction_withdrawn > 0.0:
        follower = FuelFollowerControlRod.FuelFollower(
            inner_radius=element.fuel_follower.inner_radius,
            outer_radius=cladding.inner_radius,
            material=Material(element.fuel_follower.material),
        )
        zr_fill = FuelFollowerControlRod.ZrFillRod(
            radius=element.zr_fill_rod.radius,
            material=Material(element.zr_fill_rod.material),
        )
        return FuelFollowerControlRod.build_fuel_follower_pincell(
            cladding=cladding,
            fuel_follower=follower,
            zr_fill_rod=zr_fill,
            fill_gas=Material(element.fill_gas),
            outer_material=Material(coolant),
            gap_tolerance=None,
        )

    absorber = FuelFollowerControlRod.Absorber(
        radius=element.absorber.radius,
        material=Material(element.absorber.material),
    )

    return FuelFollowerControlRod.build_absorber_pincell(
        cladding=cladding,
        absorber=absorber,
        fill_gas=Material(element.fill_gas),
        outer_material=Material(coolant),
        gap_tolerance=None,
    )


def build_element_pincell_geometry(element: Optional[NETL.Core.Element],
                                   coolant: openmc.Material) -> CylindricalPinCell:
    """Build a pincell CoreForge geometry for a given TRIGA core element.

    Parameters
    ----------
    element : Optional[NETL.Core.Element]
        The TRIGA core element to build the pincell geometry for.
        If None, this will return a pincell with only coolant.
    coolant : openmc.Material
        The coolant material to use in the pincell geometry.

    Returns
    -------
    CylindricalPinCell
        The constructed pincell geometry.
    """

    if element is None:
        pincell = build_coolant_pincell(coolant)
    elif isinstance(element, TRIGA.FuelElement):
        pincell = build_fuel_pincell(element, coolant)
    elif isinstance(element, TRIGA.GraphiteElement):
        pincell = build_graphite_pincell(element, coolant)
    elif isinstance(element, NETL.CentralThimble):
        pincell = build_central_thimble_pincell(element, coolant)
    elif isinstance(element, NETL.SourceHolder):
        pincell = build_source_holder_pincell(element, coolant)
    elif isinstance(element, NETL.TransientRod):
        pincell = build_transient_rod_pincell(element, coolant)
    elif isinstance(element, NETL.FuelFollowerControlRod):
        pincell = build_ffcr_pincell(element, coolant)
    else:
        raise ValueError(f"Unsupported element type: {type(element)}")

    return pincell


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

    elements = [[build_element_pincell_geometry(e, coolant) for e in row] for row in lattice]
    return HexLattice(pitch          = NETL.Core().pitch,
                      outer_material = Material(coolant),
                      elements       = elements,
                      orientation    = 'y')


def build_openmc_model(fuel: TRIGA.FuelElement,
                       coolant: openmc.Material,
                       central_element: Optional[NETL.Core.Element],
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
    spectrum_group_structure : str
        The energy group structure to use for the multi-group spectrum tally.

    Returns
    -------
    openmc.model.Model
        The constructed OpenMC model.
    """

    lattice = openmc_builder.build(build_multicell_geometry(fuel, coolant, central_element))
    outer_surface = openmc.model.RectangularPrism(width         = lattice_dims["width"] * 8,
                                                  height        = lattice_dims["height"] * 6,
                                                  boundary_type = 'reflective')
    lattice_cell = openmc.Cell(fill=lattice, region=-outer_surface)

    main_universe = openmc.Universe(cells=[lattice_cell])
    geometry      = openmc.Geometry(main_universe)
    materials     = openmc.Materials(list(geometry.get_all_materials().values()))

    settings           = openmc.Settings()
    settings.batches   = 100
    settings.inactive  = 20
    settings.particles = 10000

    universes = list(lattice.get_all_universes().keys())
    tallies = NETL.build_generic_openmc_tallies(spectrum_group_structure, universes)
    tallies = openmc.Tallies(list(tallies.values()))

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

    lattice         = build_multicell_geometry(fuel, coolant, central_element)
    fuel            = lattice.elements[0][0]
    central_element = lattice.elements[-1][0]
    specs    = mpact_builder.HexLattice.Specs(element_specs = {fuel:            fuel_build_specs,
                                                               central_element: element_build_specs})

    # Build the full hex lattice and then trim to the progression problem domain
    # (i.e. remove top and bottom 3 rows and leftmost and rightmost 2 columns)
    core_map = [list(row[1:-2]) \
                for row in mpact_builder.build(lattice, specs).assembly_map[3:-4]]
    geometry = mpactpy.Core(core_map)

    for state in states:
        state["tinlet"] = state.get("tinlet", f"{coolant.temperature}")

    xsec_settings["xslib"] = xsec_settings.get("xslib", xslib)

    mpact_model = mpactpy.Model(geometry, states, xsec_settings, options)
    with open(filename, 'w') as file:
        file.write(mpact_model.write_to_string("TRIGA", indent=4))
