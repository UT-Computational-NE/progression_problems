
from typing import Dict, List, Optional
from math import sqrt

import openmc
import mpactpy
from coreforge.materials import Material
from coreforge.geometry_elements import CylindricalPinCell
from coreforge.geometry_elements.triga import FuelElement
from coreforge import openmc_builder
from coreforge import mpact_builder

from progression_problems.TRIGA import NETL
from progression_problems.TRIGA.NETL.utils import DEFAULT_MPACT_SETTINGS

pitch = NETL.Core().pitch
lattice_dims = {"width"  : sqrt(pitch**2 - (pitch*0.5)**2) / 2.0,
                "height" : pitch * 0.5}


def build_openmc_model(fuel: FuelElement,
                       coolant: openmc.Material,
                       spectrum_group_structure: str = "MPACT-51"
) -> openmc.model.Model:
    """Build a pincell OpenMC model for a given TRIGA fuel element and coolant material.

    Parameters
    ----------
    fuel : FuelElement
        CoreForge TRIGA fuel element to model.
    coolant : openmc.Material
        The coolant material to use in the pincell geometry.
    spectrum_group_structure : str
        The energy group structure to use for the multi-group spectrum tally.

    Returns
    -------
    openmc.model.Model
        The constructed OpenMC model.
    """

    pincell = FuelElement.build_fuel_meat_pincell(cladding       = fuel.cladding,
                                                  fuel_meat      = fuel.fuel_meat,
                                                  zr_fill_rod    = fuel.zr_fill_rod,
                                                  fill_gas       = fuel.fill_gas,
                                                  outer_material = Material(coolant),
                                                  gap_tolerance  = fuel.gap_tolerance,
                                                  name           = fuel.name + "_fuel_meat_pincell")
    pincell = openmc_builder.build(pincell)

    quadrant = {}

    cell             = openmc.Cell(fill = pincell)
    cell.translation = [lattice_dims["width"]*0.5,
                        lattice_dims["height"]*0.5, 0.0]
    quadrant["SW"]  = openmc.Universe(cells=[cell])

    cell             = openmc.Cell(fill = pincell)
    cell.translation = [-lattice_dims["width"]*0.5,
                        -lattice_dims["height"]*0.5, 0.0]
    quadrant["NE"]  = openmc.Universe(cells=[cell])

    lattice            = openmc.RectLattice()
    lattice.lower_left = [-lattice_dims["width"], -lattice_dims["height"]*0.5]
    lattice.pitch      = [lattice_dims["width"], lattice_dims["height"]]
    lattice.universes  = [[quadrant['NE'], quadrant['SW']]]
    lattice.outer      = openmc.Universe(cells=[openmc.Cell(fill=coolant)])

    outer_surface = openmc.model.RectangularPrism(width         = lattice_dims["width"] * 2,
                                                  height        = lattice_dims["height"],
                                                  boundary_type = 'reflective')
    lattice_cell = openmc.Cell(fill=lattice, region=-outer_surface)

    main_universe = openmc.Universe(cells=[lattice_cell])
    geometry      = openmc.Geometry(main_universe)
    materials     = openmc.Materials(list(geometry.get_all_materials().values()))

    settings           = openmc.Settings()
    settings.batches   = 100
    settings.inactive  = 20
    settings.particles = 10000

    tallies = NETL.build_generic_openmc_tallies(spectrum_group_structure)
    tallies = openmc.Tallies(list(tallies.values()))

    return openmc.model.Model(geometry=geometry, materials=materials, settings=settings, tallies=tallies)


def write_mpact_input(fuel: FuelElement,
                      coolant: openmc.Material,
                      xslib: str,
                      build_specs: Optional[mpact_builder.CylindricalPinCell.Specs] = None,
                      filename: str = "mpact.inp",
                      states: List[Dict[str, str]] = [DEFAULT_MPACT_SETTINGS["state"]],
                      xsec_settings: Dict[str, str] = DEFAULT_MPACT_SETTINGS["xsec"],
                      options: Dict[str, str] = DEFAULT_MPACT_SETTINGS["options"]) -> None:
    """Write the MPACT input for a given TRIGA fuel element.

    Parameters
    ----------
    fuel : FuelElement
        CoreForge TRIGA fuel element to model.
    coolant : openmc.Material
        The coolant material to use in the pincell geometry.
    xslib : str
        The cross section library file to use in the MPACT input.
    build_specs : Optional[mpact_builder.CylindricalPinCell.Specs]
        The mpact_builder specifications to use when building the pincell geometry.
    filename : str
        The filename to write the MPACT input to. (Default: "mpact.inp")
    states : List[Dict[str, str]]
        The state settings to use in the MPACT input.
    xsec_settings : Dict[str, str]
        The cross section settings to use in the MPACT input.
    options : Dict[str, str]
        The options settings to use in the MPACT input.
    """

    pincell = FuelElement.build_fuel_meat_pincell(cladding       = fuel.cladding,
                                                  fuel_meat      = fuel.fuel_meat,
                                                  zr_fill_rod    = fuel.zr_fill_rod,
                                                  fill_gas       = fuel.fill_gas,
                                                  outer_material = Material(coolant),
                                                  gap_tolerance  = fuel.gap_tolerance,
                                                  name           = fuel.name + "_fuel_meat_pincell")

    bounds = {"SW": mpact_builder.Bounds(X={'min': -lattice_dims["width"],  'max': 0.0},
                                         Y={'min': -lattice_dims["height"], 'max': 0.0}),
              "NE": mpact_builder.Bounds(X={'min':  0.0, 'max': lattice_dims["width"]},
                                         Y={'min':  0.0, 'max': lattice_dims["height"]})}

    quadrant = {"SW": mpact_builder.build(pincell, build_specs, bounds['SW']).assemblies[0],
                "NE": mpact_builder.build(pincell, build_specs, bounds['NE']).assemblies[0]}

    geometry = mpactpy.Core([[quadrant["NE"], quadrant["SW"]]])

    for state in states:
        state["tinlet"] = state.get("tinlet", f"{coolant.temperature}")

    xsec_settings["xslib"] = xsec_settings.get("xslib", xslib)

    options["rr_edits"] = options.get("rr_edits", "HDF5")

    mpact_model = mpactpy.Model(geometry, states, xsec_settings, options)
    with open(filename, 'w') as file:
        file.write(mpact_model.write_to_string("TRIGA", indent=4))
