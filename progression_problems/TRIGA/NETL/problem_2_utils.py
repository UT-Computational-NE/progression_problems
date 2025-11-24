
from typing import Dict, List, Optional
from math import sqrt

import openmc
import mpactpy
from coreforge.geometry_elements import CylindricalPinCell, HexLattice
from coreforge.materials import Material
import coreforge.openmc_builder as openmc_builder
import coreforge.mpact_builder as mpact_builder


import progression_problems.TRIGA as TRIGA
import progression_problems.TRIGA.NETL as NETL
from progression_problems.TRIGA.NETL.problem_1_utils \
    import lattice_dims, build_pincell_geometry as build_fuel_pincell_geometry
from progression_problems.TRIGA.NETL.utils import DEFAULT_MPACT_SETTINGS

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
        return CylindricalPinCell(radii = [TRIGA.FuelElement().cladding.outer_radius],
                                  materials = [Material(coolant),
                                               Material(coolant)])
    elif isinstance(element, TRIGA.FuelElement):
        return build_fuel_pincell_geometry(element, coolant)
    elif isinstance(element, TRIGA.GraphiteElement):
        return CylindricalPinCell(radii = [element.graphite_meat.outer_radius,
                                           element.cladding.outer_radius],
                                  materials = [Material(element.graphite_meat.material),
                                               Material(element.cladding.material),
                                               Material(coolant)])
    elif isinstance(element, NETL.CentralThimble):
        return CylindricalPinCell(radii = [element.inner_radius,
                                           element.outer_radius],
                                  materials = [Material(coolant),
                                               Material(element.material),
                                               Material(coolant)])
    elif isinstance(element, NETL.TransientRod):
        clad_inner_radius = element.cladding.outer_radius - element.cladding.thickness
        if element.fraction_withdrawn > 0.0:
            return CylindricalPinCell(radii = [clad_inner_radius,
                                               element.cladding.outer_radius],
                                      materials = [Material(element.fill_gas),
                                                   Material(element.cladding.material),
                                                   Material(coolant)])
        else:
            return CylindricalPinCell(radii = [element.absorber.radius,
                                               clad_inner_radius,
                                               element.cladding.outer_radius],
                                      materials = [Material(element.absorber.material),
                                                   Material(element.fill_gas),
                                                   Material(element.cladding.material),
                                                   Material(coolant)])
    elif isinstance(element, NETL.FuelFollowerControlRod):
        clad_inner_radius = element.cladding.outer_radius - element.cladding.thickness
        if element.fraction_withdrawn > 0.0:
            return CylindricalPinCell(radii = [element.fuel_follower.inner_radius,
                                               clad_inner_radius,
                                               element.cladding.outer_radius],
                                      materials = [Material(element.zr_fill_rod.material),
                                                   Material(element.fuel_follower.material),
                                                   Material(element.cladding.material),
                                                   Material(coolant)])
        else:
            return CylindricalPinCell(radii = [element.absorber.radius,
                                               clad_inner_radius,
                                               element.cladding.outer_radius],
                                      materials = [Material(element.absorber.material),
                                                   Material(element.fill_gas),
                                                   Material(element.cladding.material),
                                                   Material(coolant)])
    else:
        raise ValueError(f"Unsupported element type: {type(element)}")



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
    core_map = [[e for e in row[1:-2]] \
                for row in mpact_builder.build(lattice, specs).assembly_map[3:-4]]
    geometry = mpactpy.Core(core_map)

    for state in states:
        state["tinlet"] = state.get("tinlet", f"{coolant.temperature}")

    xsec_settings["xslib"] = xsec_settings.get("xslib", xslib)

    mpact_model = mpactpy.Model(geometry, states, xsec_settings, options)
    with open(filename, 'w') as file:
        file.write(mpact_model.write_to_string("TRIGA", indent=4))
