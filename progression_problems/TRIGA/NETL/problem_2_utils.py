from typing import Dict, List, Optional

import openmc
import mpactpy
from coreforge.geometry_elements import HexLattice
from coreforge.geometry_elements import CylindricalPinCell
from coreforge.geometry_elements.triga import FuelElement, GraphiteElement
from coreforge.geometry_elements.triga.netl import (CentralThimble, SourceHolder, TransientRod,
                                                    FuelFollowerControlRod, Core)
from coreforge.materials import Material
from coreforge import openmc_builder
from coreforge import mpact_builder

from progression_problems.TRIGA.default_geometries import DefaultGeometries as TRIGA_DefaultGeometries
from progression_problems.TRIGA.NETL.default_geometries import DefaultGeometries as NETL_DefaultGeometries
from progression_problems.TRIGA.NETL.problem_1_utils import lattice_dims
from progression_problems.TRIGA.NETL.utils import DEFAULT_MPACT_SETTINGS, build_generic_openmc_tallies


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
    filler = TRIGA_DefaultGeometries.fuel_element()
    cladding = FuelElement.Cladding(thickness    = filler.cladding.thickness,
                                    outer_radius = filler.cladding.outer_radius,
                                    material     = Material(coolant))

    fuel_meat = FuelElement.FuelMeat(inner_radius = filler.fuel_meat.inner_radius,
                                     outer_radius = filler.fuel_meat.outer_radius,
                                     length       = filler.fuel_meat.length,
                                     material     = Material(coolant))

    zr_fill = FuelElement.ZrFillRod(radius   = filler.zr_fill_rod.radius,
                                    material = Material(coolant))

    return FuelElement.build_fuel_meat_pincell(cladding       = cladding,
                                               fuel_meat      = fuel_meat,
                                               zr_fill_rod    = zr_fill,
                                               fill_gas       = Material(coolant),
                                               outer_material = Material(coolant))


def build_element_pincell_geometry(element: Optional[Core.Element],
                                   coolant: openmc.Material,
                                   control_rod_inserted: bool) -> CylindricalPinCell:
    """Build a pincell CoreForge geometry for a given TRIGA core element.

    Parameters
    ----------
    element : Optional[Core.Element]
        The TRIGA core element to build the pincell geometry for.
        If None, this will return a pincell with only coolant.
    coolant : openmc.Material
        The coolant material to use in the pincell geometry.
    control_rod_inserted : bool
        Whether the control rod is inserted or not (only applies to control rod models).

    Returns
    -------
    CylindricalPinCell
        The constructed pincell geometry.
    """

    if element is None:
        pincell = build_coolant_pincell(coolant)

    elif isinstance(element, FuelElement):
        pincell = FuelElement.build_fuel_meat_pincell(cladding       = element.cladding,
                                                      fuel_meat      = element.fuel_meat,
                                                      zr_fill_rod    = element.zr_fill_rod,
                                                      fill_gas       = element.fill_gas,
                                                      outer_material = Material(coolant),
                                                      gap_tolerance  = element.gap_tolerance,
                                                      name           = element.name + "_fuel_meat_pincell")

    elif isinstance(element, GraphiteElement):
        pincell = GraphiteElement.build_graphite_meat_pincell(cladding       = element.cladding,
                                                              graphite_meat  = element.graphite_meat,
                                                              outer_material = Material(coolant))

    elif isinstance(element, CentralThimble):
        pincell = CentralThimble.build_thimble_pincell(cladding       = element.cladding,
                                                       fill_material  = Material(coolant),
                                                       outer_material = Material(coolant))

    elif isinstance(element, SourceHolder):
        pincell = SourceHolder.build_cavity_pincell(cavity         = element.cavity,
                                                    cladding       = element.cladding,
                                                    outer_material = Material(coolant),
                                                    gap_tolerance  = None)

    elif isinstance(element, TransientRod):
        air_follower = TransientRod.build_air_follower_pincell(cladding       = element.cladding,
                                                               fill_gas       = element.fill_gas,
                                                               outer_material = Material(coolant))

        absorber     = TransientRod.build_absorber_pincell(cladding       = element.cladding,
                                                           absorber       = element.absorber,
                                                           fill_gas       = element.fill_gas,
                                                           outer_material = Material(coolant),
                                                           gap_tolerance  = None)

        pincell = absorber if control_rod_inserted else air_follower

    elif isinstance(element, FuelFollowerControlRod):
        fuel_follower = FuelFollowerControlRod.build_fuel_follower_pincell(cladding       = element.cladding,
                                                                           fuel_follower  = element.fuel_follower,
                                                                           zr_fill_rod    = element.zr_fill_rod,
                                                                           fill_gas       = element.fill_gas,
                                                                           outer_material = Material(coolant),
                                                                           gap_tolerance  = None)

        absorber = FuelFollowerControlRod.build_absorber_pincell(cladding       = element.cladding,
                                                                 absorber       = element.absorber,
                                                                 fill_gas       = element.fill_gas,
                                                                 outer_material = Material(coolant),
                                                                 gap_tolerance  = None)

        pincell = absorber if control_rod_inserted else fuel_follower

    else:
        raise ValueError(f"Unsupported element type: {type(element)}")

    return pincell


def build_multicell_geometry(fuel:                 FuelElement,
                             coolant:              openmc.Material,
                             central_element:      Optional[Core.Element],
                             control_rod_inserted: bool
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
    control_rod_inserted : bool
        Whether the control rod is inserted or not (only applies to control rod models).
        Default is False.

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

    elements = [[build_element_pincell_geometry(e, coolant, control_rod_inserted)
                 for e in row] for row in lattice]
    return HexLattice(pitch          = NETL_DefaultGeometries.core().pitch,
                      outer_material = Material(coolant),
                      elements       = elements,
                      orientation    = 'y')


def build_openmc_model(fuel: FuelElement,
                       coolant: openmc.Material,
                       central_element: Optional[Core.Element],
                       control_rod_inserted: bool = False,
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
    control_rod_inserted : bool
        Whether the control rod is inserted or not (only applies to control rod models).
        Default is False.
    spectrum_group_structure : str
        The energy group structure to use for the multi-group spectrum tally.

    Returns
    -------
    openmc.model.Model
        The constructed OpenMC model.
    """

    lattice        = build_multicell_geometry(fuel, coolant, central_element, control_rod_inserted)
    lattice        = openmc_builder.build(lattice)
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
    tallies   = build_generic_openmc_tallies(spectrum_group_structure, universes)
    tallies   = openmc.Tallies(list(tallies.values()))

    return openmc.model.Model(geometry=geometry, materials=materials, settings=settings, tallies=tallies)


def write_mpact_input(fuel: FuelElement,
                      coolant: openmc.Material,
                      central_element: Optional[Core.Element],
                      control_rod_inserted: bool = False,
                      fuel_build_specs: Optional[mpact_builder.CylindricalPinCell.Specs] = None,
                      element_build_specs: Optional[mpact_builder.CylindricalPinCell.Specs] = None,
                      filename: str = "mpact.inp",
                      states: List[Dict[str, str]] = [DEFAULT_MPACT_SETTINGS["state"]],
                      xsec_settings: Dict[str, str] = DEFAULT_MPACT_SETTINGS["xsec"],
                      options: Dict[str, str] = DEFAULT_MPACT_SETTINGS["options"]) -> None:
    """Write the MPACT input for a given TRIGA fuel element, coolant, and central element.

    Parameters
    ----------
    fuel : FuelElement
        The TRIGA fuel element to use for building the multicell geometry.
    coolant : openmc.Material
        The coolant material to use in the multicell geometry.
    central_element : Optional[Core.Element]
        The central element to use for building the multicell geometry.
    control_rod_inserted : bool
        Whether the control rod is inserted or not (only applies to control rod models).
        Default is False.
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

    lattice         = build_multicell_geometry(fuel, coolant, central_element, control_rod_inserted)
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

    mpact_model = mpactpy.Model(geometry, states, xsec_settings, options)
    with open(filename, 'w') as file:
        file.write(mpact_model.write_to_string("TRIGA", indent=4))
