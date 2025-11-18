
from typing import Optional
from math import sqrt

import openmc
import mpactpy
from coreforge.geometry_elements import CylindricalPinCell
from coreforge.materials import Material
import coreforge.openmc_builder as openmc_builder
import coreforge.mpact_builder as mpact_builder


import progression_problems.TRIGA as TRIGA
import progression_problems.TRIGA.NETL as NETL

pitch = NETL.Core().pitch
lattice_dims = {"height" : pitch * 0.5 * 2.0/sqrt(3.0),
                "width"  : pitch * 0.5}

def build_pincell_geometry(fuel:    TRIGA.FuelElement,
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

    pincell = CylindricalPinCell(radii = [fuel.fuel_meat.inner_radius,
                                          fuel.fuel_meat.outer_radius,
                                          fuel.cladding.outer_radius],
                                 materials = [Material(fuel.zr_fill_rod.material),
                                              Material(fuel.fuel_meat.material),
                                              Material(fuel.cladding.material),
                                              Material(coolant)])

    return pincell


def build_openmc_model(fuel:    TRIGA.FuelElement,
                       coolant: openmc.Material,
                       spectrum_group_structure: str = "MPACT-51"
) -> openmc.model.Model:
    """Build a pincell OpenMC model for a given TRIGA fuel element.

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

    pincell = openmc_builder.build(build_pincell_geometry(fuel, coolant))

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


def write_mpact_input(fuel:     TRIGA.FuelElement,
                      coolant:  openmc.Material,
                      xslib:    str,
                      build_specs: Optional[mpact_builder.CylindricalPinCell.Specs] = None,
                      filename: str = "mpact.inp") -> None:
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
    """

    pincell = build_pincell_geometry(fuel, coolant)

    bounds = {"SW": mpact_builder.Bounds(X={'min': -lattice_dims["width"],  'max': 0.0},
                                         Y={'min': -lattice_dims["height"], 'max': 0.0}),
              "NE": mpact_builder.Bounds(X={'min':  0.0, 'max': lattice_dims["width"]},
                                         Y={'min':  0.0, 'max': lattice_dims["height"]})}

    quadrant = {"SW": mpact_builder.build(pincell, build_specs, bounds['SW']).assemblies[0],
                "NE": mpact_builder.build(pincell, build_specs, bounds['NE']).assemblies[0]}

    geometry = mpactpy.Core([[quadrant["NE"], quadrant["SW"]]])

    states          = [{"rated_power": "1.0",
                        "power":       "1.0",
                        "pressure":    "1.0",
                        "tinlet":      f"{coolant.temperature}",
                        "rated_flow":  "1.0"}]

    xsec_settings = {'xslib'      : xslib,
                     'xsshielder' : 'T SUBGROUP'}

    options       = {'solver'     : '1 2',
                     'rr_edits'   : 'HDF5',
                     'ray'        : '0.05 CHEBYSHEV-YAMAMOTO 16 3',
                     'conv_crit'  : '1.0E-6 1.0E-6',
                     'iter_lim'   : '50 1 1',
                     'vis_edits'  : 'F',
                     'scatt_meth' : 'TCP0',
                     'nodal'      : 'T SP3',
                     'axial_tl'   : 'T ISO LFLAT',
                     'parallel'   : '1 1 1 1'}

    mpact_model = mpactpy.Model(geometry, states, xsec_settings, options)
    with open(filename, 'w') as file:
        file.write(mpact_model.write_to_string("TRIGA", indent=4))