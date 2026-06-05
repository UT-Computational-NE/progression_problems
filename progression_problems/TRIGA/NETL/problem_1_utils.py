from typing import Dict, List, Optional
from math import sqrt

import openmc
import mpactpy
from coreforge.materials import Material
from coreforge.geometry_elements.triga import FuelElement
from coreforge import openmc_builder
from coreforge import mpact_builder

from progression_problems.TRIGA.NETL.default_geometries import DefaultGeometries
from progression_problems.TRIGA.NETL.utils import (DEFAULT_MPACT_SETTINGS,
                                                  build_generic_openmc_tallies,
                                                  default_mpact_material_specs)


def lattice_dims(pitch: float) -> Dict[str, float]:
    """Return lattice dimensions derived from a hexagonal pitch."""
    return {"width": sqrt(pitch**2 - (pitch * 0.5) ** 2) / 2.0, "height": pitch * 0.5}


def build_openmc_model(fuel:                     FuelElement,
                       coolant:                  openmc.Material,
                       spectrum_group_structure: str = "MPACT-51",
                       pitch:                    float = DefaultGeometries.core().pitch,
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
    pitch : float
        Hexagonal lattice pitch to use when constructing the repeated pincell
        geometry. Defaults to the NETL core pitch.

    Returns
    -------
    openmc.model.Model
        The constructed OpenMC model.
    """

    dims = lattice_dims(pitch)

    pincell = FuelElement.build_fuel_meat_pincell(cladding       = fuel.cladding,
                                                  fuel_meat      = fuel.fuel_meat,
                                                  zr_fill_rod    = fuel.zr_fill_rod,
                                                  fill_gas       = fuel.fill_gas,
                                                  outer_material = Material(coolant),
                                                  gap_tolerance  = fuel.gap_tolerance,
                                                  name           = fuel.name + "_fuel_meat_pincell")
    pincell = openmc_builder.build(pincell)

    quadrant = {}

    cell = openmc.Cell(fill=pincell)
    cell.translation = [dims["width"] * 0.5,
                        dims["height"] * 0.5, 0.0]
    quadrant["SW"] = openmc.Universe(cells=[cell])

    cell = openmc.Cell(fill=pincell)
    cell.translation = [-dims["width"] * 0.5,
                        -dims["height"] * 0.5, 0.0]
    quadrant["NE"] = openmc.Universe(cells=[cell])

    lattice            = openmc.RectLattice()
    lattice.lower_left = [-dims["width"], -dims["height"] * 0.5]
    lattice.pitch      = [dims["width"], dims["height"]]
    lattice.universes  = [[quadrant["NE"], quadrant["SW"]]]
    lattice.outer      = openmc.Universe(cells=[openmc.Cell(fill=coolant)])

    outer_surface = openmc.model.RectangularPrism(width         = dims["width"] * 2,
                                                  height        = dims["height"],
                                                  boundary_type = "reflective")
    lattice_cell = openmc.Cell(fill=lattice, region=-outer_surface)

    main_universe = openmc.Universe(cells=[lattice_cell])
    geometry      = openmc.Geometry(main_universe)
    materials     = openmc.Materials(list(geometry.get_all_materials().values()))

    settings           = openmc.Settings()
    settings.batches   = 100
    settings.inactive  = 20
    settings.particles = 10000

    tallies = build_generic_openmc_tallies(spectrum_group_structure)
    tallies = openmc.Tallies(list(tallies.values()))

    return openmc.model.Model(geometry=geometry, materials=materials, settings=settings, tallies=tallies)


def write_mpact_input(fuel:                     FuelElement,
                      coolant:                  openmc.Material,
                      pitch:                    float = DefaultGeometries.core().pitch,
                      build_specs:              Optional[mpact_builder.CylindricalPinCell.Specs] = None,
                      filename:                 str = "mpact.inp",
                      states:                   Optional[List[Dict[str, str]]] = None,
                      xsec_settings:            Optional[Dict[str, str]] = None,
                      options:                  Optional[Dict[str, str]] = None,
) -> None:
    """Write the MPACT input for a given TRIGA fuel element.

    Parameters
    ----------
    fuel : FuelElement
        CoreForge TRIGA fuel element to model.
    coolant : openmc.Material
        The coolant material to use in the pincell geometry.
    pitch : float
        Hexagonal lattice pitch to use when constructing the repeated pincell
        geometry. Defaults to the NETL core pitch.
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

    dims = lattice_dims(pitch)

    pincell = FuelElement.build_fuel_meat_pincell(cladding       = fuel.cladding,
                                                  fuel_meat      = fuel.fuel_meat,
                                                  zr_fill_rod    = fuel.zr_fill_rod,
                                                  fill_gas       = fuel.fill_gas,
                                                  outer_material = Material(coolant),
                                                  gap_tolerance  = fuel.gap_tolerance,
                                                  name           = fuel.name + "_fuel_meat_pincell")

    build_specs = apply_default_mpact_material_specs(build_specs, pincell.get_materials())

    bounds = {"SW": mpact_builder.Bounds(
                  X=mpact_builder.AxisBounds(min=-dims["width"], max=0.0),
                  Y=mpact_builder.AxisBounds(min=-dims["height"], max=0.0)),
              "NE": mpact_builder.Bounds(
                  X=mpact_builder.AxisBounds(min=0.0, max=dims["width"]),
                  Y=mpact_builder.AxisBounds(min=0.0, max=dims["height"]))}

    quadrant = {"SW": mpact_builder.build(pincell, build_specs, bounds["SW"]).assemblies[0],
                "NE": mpact_builder.build(pincell, build_specs, bounds["NE"]).assemblies[0]}

    geometry = mpactpy.Core([[quadrant["NE"], quadrant["SW"]]])

    states = [dict(state) for state in (states or [DEFAULT_MPACT_SETTINGS["state"]])]
    xsec_settings = dict(xsec_settings or DEFAULT_MPACT_SETTINGS["xsec"])
    options = dict(options or DEFAULT_MPACT_SETTINGS["options"])

    for state in states:
        state["tinlet"] = state.get("tinlet", f"{coolant.temperature}")

    options["bound_cond"] = "1 1 1 1 1 1"

    mpact_model = mpactpy.Model(geometry, states, xsec_settings, options)
    with open(filename, "w") as file:
        file.write(mpact_model.write_to_string("TRIGA", indent=4))


def apply_default_mpact_material_specs(
    build_specs: Optional[mpact_builder.CylindricalPinCell.Specs],
    materials: List[Material],
) -> mpact_builder.CylindricalPinCell.Specs:
    """Return build specs with default material specs applied.

    Parameters
    ----------
    build_specs : Optional[mpact_builder.CylindricalPinCell.Specs]
        Build specs to update or create if None.
    materials : List[Material]
        Materials to use for default material specs.

    Returns
    -------
    mpact_builder.CylindricalPinCell.Specs
        Build specs with merged material specs.
    """
    defaults = default_mpact_material_specs(materials)
    if build_specs is None:
        return mpact_builder.CylindricalPinCell.Specs(material_specs=defaults)
    return mpact_builder.CylindricalPinCell.Specs(
        zone_specs            = build_specs.zone_specs,
        divide_into_quadrants = build_specs.divide_into_quadrants,
        material_specs        = defaults | build_specs.material_specs
    )
