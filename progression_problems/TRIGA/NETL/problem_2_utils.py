from typing import Dict, List, Optional, Sequence, Tuple

import openmc
import mpactpy
from coreforge.geometry_elements import CylindricalPinCells
from coreforge.geometry_elements.triga import CoreElement, FuelElement
from coreforge import openmc_builder
from coreforge import mpact_builder

from progression_problems.TRIGA.NETL.default_geometries import DefaultGeometries as NETL_DefaultGeometries
from progression_problems.TRIGA.NETL.problem_1_utils import (apply_default_mpact_material_specs,
                                                             lattice_dims)
from progression_problems.TRIGA.NETL.utils import (DEFAULT_MPACT_SETTINGS,
                                                   get_pincell,
                                                   build_coolant_pincell,
                                                   build_multicell_geometry,
                                                   build_generic_openmc_tallies)


DEFAULT_COOLANT_PINCELL_RADII: Tuple[float, ...] = tuple(sorted({
    NETL_DefaultGeometries.upper_grid_plate().penetration_map["B-01"][0][0],
    NETL_DefaultGeometries.lower_grid_plate().penetration_map["B-01"][0][0],
}))


def build_openmc_model(fuel: FuelElement,
                       central_element: Optional[CoreElement],
                       central_pincell_section: Optional[str] = None,
                       coolant_pincell_radii: Sequence[float] = DEFAULT_COOLANT_PINCELL_RADII,
                       spectrum_group_structure: str = "MPACT-51",
                       pitch: float = NETL_DefaultGeometries.core().pitch,
) -> openmc.model.Model:
    """Build a multicell OpenMC Model.

    Parameters
    ----------
    fuel : FuelElement
        Fuel element supplying the first fuel section and the lattice coolant.
    central_element : Optional[CoreElement]
        Element supplying the central cross section. Its stored pincells must
        contain the desired coolant. ``None`` represents a coolant-only location.
    central_pincell_section : Optional[str]
        Key in ``central_element.pincell``. Rods and irradiators require an
        explicit key, such as ``"absorber"``, ``"air_follower"``,
        ``"fuel_follower"``, ``"lined"``, ``"b4c_region"``, or
        ``"lower_b10_region"``. Simple elements use their standard section
        when omitted. List-valued sections use the first entry, ordered from
        bottom to top. Detailed or simplified sections follow the element's
        configuration.
    coolant_pincell_radii : Sequence[float]
        Cylindrical mesh radii to use when ``central_element`` is ``None`` and
        a coolant-only pincell should be built.
    spectrum_group_structure : str
        The energy group structure to use for the multi-group spectrum tally.
    pitch : float
        Hexagonal lattice pitch to use for the multicell geometry. Defaults to
        the NETL core pitch.

    Returns
    -------
    openmc.model.Model
        The constructed OpenMC model.
    """

    dims           = lattice_dims(pitch)
    fuel_pincell = get_pincell(fuel)
    central_pincell = (get_pincell(central_element, central_pincell_section)
                      if central_element is not None else
                      build_coolant_pincell(fuel.outer_material.openmc_material, coolant_pincell_radii))
    lattice        = build_multicell_geometry(fuel_pincell, central_pincell, pitch)
    lattice        = openmc_builder.build(lattice)
    outer_surface = openmc.model.RectangularPrism(width         = dims["width"] * 8,
                                                  height        = dims["height"] * 6,
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
                      central_element: Optional[CoreElement],
                      central_pincell_section: Optional[str] = None,
                      coolant_pincell_radii: Sequence[float] = DEFAULT_COOLANT_PINCELL_RADII,
                      pitch: float = NETL_DefaultGeometries.core().pitch,
                      fuel_build_specs: Optional[mpact_builder.CylindricalPinCell.Specs] = None,
                      element_build_specs: Optional[mpact_builder.CylindricalPinCell.Specs] = None,
                      filename: str = "mpact.inp",
                      states: Optional[List[Dict[str, str]]] = None,
                      xsec_settings: Optional[Dict[str, str]] = None,
                      options: Optional[Dict[str, str]] = None) -> None:
    """Write the MPACT input for a TRIGA fuel element and central element.

    Parameters
    ----------
    fuel : FuelElement
        Fuel element supplying the first fuel section and the lattice coolant.
    central_element : Optional[CoreElement]
        Element supplying the central cross section. Its stored pincells must
        contain the desired coolant. ``None`` represents a coolant-only location.
    central_pincell_section : Optional[str]
        Key in ``central_element.pincell``. Rods and irradiators require an
        explicit key, such as ``"absorber"``, ``"air_follower"``,
        ``"fuel_follower"``, ``"lined"``, ``"b4c_region"``, or
        ``"lower_b10_region"``. Simple elements use their standard section
        when omitted. List-valued sections use the first entry, ordered from
        bottom to top. Detailed or simplified sections follow the element's
        configuration.
    coolant_pincell_radii : Sequence[float]
        Cylindrical mesh radii to use when ``central_element`` is ``None`` and
        a coolant-only pincell should be built.
    pitch : float
        Hexagonal lattice pitch to use for the multicell geometry. Defaults to
        the NETL core pitch.
    fuel_build_specs : Optional[mpact_builder.CylindricalPinCell.Specs]
        The mpact_builder specifications to use when building the fuel pincell geometry.
    element_build_specs : Optional[mpact_builder.CylindricalPinCell.Specs]
        The mpact_builder specifications to use when building the central pincell geometry.
        If ``central_element`` is ``None``, these specs are applied to the coolant-only
        water-hole pincell.
    filename : str
        The filename to write the MPACT input to. (Default: "mpact.inp")
    states : List[Dict[str, str]]
        The state settings to use in the MPACT input.
    xsec_settings : Dict[str, str]
        The cross section settings to use in the MPACT input.
    options : Dict[str, str]
        The options settings to use in the MPACT input.
    """

    fuel_pincell = get_pincell(fuel)
    central_pincell = (get_pincell(central_element, central_pincell_section)
                      if central_element is not None else
                      build_coolant_pincell(fuel.outer_material.openmc_material, coolant_pincell_radii))
    lattice = build_multicell_geometry(fuel_pincell, central_pincell, pitch)

    fuel_build_specs    = apply_default_mpact_material_specs(fuel_build_specs, fuel_pincell.get_materials())
    element_build_specs = apply_default_mpact_material_specs(element_build_specs, central_pincell.get_materials())

    specs    = mpact_builder.HexLattice.Specs(element_specs = {fuel_pincell:    fuel_build_specs,
                                                               central_pincell: element_build_specs})
    for ring in lattice.elements:
        for element in ring:
            if isinstance(element, CylindricalPinCells):
                specs.element_specs[element] = mpact_builder.CylindricalPinCells.Specs(
                    pincell_specs={element.pincells[0]: fuel_build_specs,
                                   element.pincells[1]: element_build_specs},
                )

    # Build the full hex lattice and then trim to the progression problem domain
    # (i.e. remove top and bottom 3 rows and leftmost and rightmost 2 columns)
    core_map = [list(row[1:-1]) \
                for row in mpact_builder.build(lattice, specs).assembly_map[2:-2]]
    geometry = mpactpy.Core(core_map)

    states = [dict(state) for state in (states or [DEFAULT_MPACT_SETTINGS["state"]])]
    xsec_settings = dict(xsec_settings or DEFAULT_MPACT_SETTINGS["xsec"])
    options = dict(options or DEFAULT_MPACT_SETTINGS["options"])

    for state in states:
        state["tinlet"] = state.get("tinlet", f"{fuel.outer_material.temperature} K")

    options["bound_cond"] = "1 1 1 1 1 1"

    mpact_model = mpactpy.Model(geometry, states, xsec_settings, options)
    with open(filename, 'w') as file:
        file.write(mpact_model.write_to_string("TRIGA", indent=4))
