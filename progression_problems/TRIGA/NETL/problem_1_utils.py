
from typing import Dict, List, Optional
from math import sqrt

import openmc
import mpactpy
from coreforge.materials import Material
from coreforge.geometry_elements import CylindricalPinCell
from coreforge.geometry_elements.triga import FuelElement
from coreforge import openmc_builder
from coreforge import mpact_builder

from progression_problems import TRIGA
from progression_problems.TRIGA import NETL
from progression_problems.TRIGA.NETL.utils import DEFAULT_MPACT_SETTINGS

pitch = NETL.Core().pitch
lattice_dims = {"width"  : sqrt(pitch**2 - (pitch*0.5)**2) / 2.0,
                "height" : pitch * 0.5}

def build_fuel_pincell(fuel: TRIGA.FuelElement,
                       coolant: openmc.Material) -> CylindricalPinCell:
    """Build a pincell CoreForge geometry for a given TRIGA fuel element.

    Parameters
    ----------
    fuel : TRIGA.FuelElement
        The TRIGA fuel element to build the pincell geometry for.
    coolant : openmc.Material
        The coolant material to use in the pincell geometry.

    Returns
    -------
    CylindricalPinCell
        The constructed pincell geometry.
    """

    cladding = FuelElement.Cladding(
        thickness=fuel.cladding.thickness,
        outer_radius=fuel.cladding.outer_radius,
        material=Material(fuel.cladding.material),
    )

    fuel_meat = FuelElement.FuelMeat(
        inner_radius=fuel.fuel_meat.inner_radius,
        outer_radius=fuel.fuel_meat.outer_radius,
        length=fuel.fuel_meat.length,
        material=Material(fuel.fuel_meat.material),
    )

    zr_fill = FuelElement.ZrFillRod(
        radius=fuel.zr_fill_rod.radius,
        material=Material(fuel.zr_fill_rod.material),
    )

    return FuelElement.build_fuel_meat_pincell(
        cladding=cladding,
        fuel_meat=fuel_meat,
        zr_fill_rod=zr_fill,
        fill_gas=Material(fuel.fill_gas),
        outer_material=Material(coolant))


def build_openmc_model(fuel: TRIGA.FuelElement,
                       coolant: openmc.Material,
                       spectrum_group_structure: str = "MPACT-51"
) -> openmc.model.Model:
    """Build a pincell OpenMC model for a given TRIGA fuel element and coolant material.

    Parameters
    ----------
    fuel : TRIGA.FuelElement
        The TRIGA fuel element to build the pincell geometry for.
    coolant : openmc.Material
        The coolant material to use in the pincell geometry.
    spectrum_group_structure : str
        The energy group structure to use for the multi-group spectrum tally.

    Returns
    -------
    openmc.model.Model
        The constructed OpenMC model.
    """

    pincell = openmc_builder.build(build_fuel_pincell(fuel, coolant))

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


def write_mpact_input(fuel: TRIGA.FuelElement,
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
    fuel : TRIGA.FuelElement
        The TRIGA fuel element to build the pincell geometry for.
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

    pincell = build_fuel_pincell(fuel, coolant)

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
