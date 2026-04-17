from typing import Dict, List, Optional, Sequence, Tuple

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

from progression_problems.TRIGA.NETL.default_geometries import DefaultGeometries as NETL_DefaultGeometries
from progression_problems.TRIGA.NETL.problem_1_utils import (apply_default_mpact_material_specs,
                                                             lattice_dims)
from progression_problems.TRIGA.NETL.utils import (DEFAULT_MPACT_SETTINGS,
                                                   build_generic_openmc_tallies)


DEFAULT_COOLANT_PINCELL_RADII: Tuple[float, ...] = tuple(sorted({
    NETL_DefaultGeometries.upper_grid_plate().penetration_map["B-01"],
    NETL_DefaultGeometries.lower_grid_plate().penetration_map["B-01"],
}))


def build_coolant_pincell(coolant: openmc.Material,
                          radii: Sequence[float]) -> CylindricalPinCell:
    """Build a coolant-only cylindrical pincell.

    Parameters
    ----------
    coolant : openmc.Material
        Coolant material to fill all regions.
    radii : Sequence[float]
        Cylindrical mesh radii for the coolant-only pincell.

    Returns
    -------
    CylindricalPinCell
        Coolant-only cylindrical pincell.
    """
    filtered_radii = sorted(set(radii))
    assert filtered_radii, "radii must contain at least one value."
    assert all(radius > 0.0 for radius in filtered_radii), "All coolant pincell radii must be positive."
    coolant_material = Material(coolant)
    return CylindricalPinCell(
        radii=filtered_radii,
        materials=[coolant_material for _ in range(len(filtered_radii) + 1)],
        name="coolant_pincell",
    )


def build_element_pincell_geometry(element: Optional[Core.Element],
                                   coolant: openmc.Material,
                                   control_rod_inserted: bool,
                                   coolant_pincell_radii: Sequence[float]) -> CylindricalPinCell:
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
    coolant_pincell_radii : Sequence[float]
        Cylindrical mesh radii to use when ``element`` is ``None`` and a
        coolant-only pincell should be built.

    Returns
    -------
    CylindricalPinCell
        The constructed pincell geometry.
    """

    if element is None:
        pincell = build_coolant_pincell(coolant, coolant_pincell_radii)

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
                             control_rod_inserted: bool = False,
                             coolant_pincell_radii: Sequence[float] = DEFAULT_COOLANT_PINCELL_RADII,
                             pitch:                float = NETL_DefaultGeometries.core().pitch,
                             build_2D_pincells: bool = True,
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
    coolant_pincell_radii : Sequence[float]
        Cylindrical mesh radii to use when ``central_element`` is ``None`` and
        a coolant-only pincell should be built.
    pitch : float
        Hexagonal lattice pitch to use for the multicell geometry. Defaults to
        the NETL core pitch.
    build_2D_pincells : bool
        Whether to build 2-D pincell representations for the lattice elements.
        Set to False to return the raw element lattice.

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

    elements = lattice
    if build_2D_pincells:
        elements = [[build_element_pincell_geometry(e, coolant, control_rod_inserted, coolant_pincell_radii)
                     for e in row] for row in lattice]

    return HexLattice(pitch          = pitch,
                      outer_material = Material(coolant),
                      elements       = elements,
                      orientation    = 'y')


def build_openmc_model(fuel: FuelElement,
                       coolant: openmc.Material,
                       central_element: Optional[Core.Element],
                       control_rod_inserted: bool = False,
                       coolant_pincell_radii: Sequence[float] = DEFAULT_COOLANT_PINCELL_RADII,
                       spectrum_group_structure: str = "MPACT-51",
                       pitch: float = NETL_DefaultGeometries.core().pitch,
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
    lattice        = build_multicell_geometry(
        fuel,
        coolant,
        central_element,
        control_rod_inserted,
        coolant_pincell_radii,
        pitch,
    )
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
                      coolant: openmc.Material,
                      central_element: Optional[Core.Element],
                      control_rod_inserted: bool = False,
                      coolant_pincell_radii: Sequence[float] = DEFAULT_COOLANT_PINCELL_RADII,
                      pitch: float = NETL_DefaultGeometries.core().pitch,
                      fuel_build_specs: Optional[mpact_builder.CylindricalPinCell.Specs] = None,
                      element_build_specs: Optional[mpact_builder.CylindricalPinCell.Specs] = None,
                      filename: str = "mpact.inp",
                      states: Optional[List[Dict[str, str]]] = None,
                      xsec_settings: Optional[Dict[str, str]] = None,
                      options: Optional[Dict[str, str]] = None) -> None:
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
    coolant_pincell_radii : Sequence[float]
        Cylindrical mesh radii to use when ``central_element`` is ``None`` and
        a coolant-only pincell should be built.
    pitch : float
        Hexagonal lattice pitch to use for the multicell geometry. Defaults to
        the NETL core pitch.
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

    lattice         = build_multicell_geometry(
        fuel,
        coolant,
        central_element,
        control_rod_inserted,
        coolant_pincell_radii,
        pitch,
    )
    fuel            = lattice.elements[0][0]
    central_element = lattice.elements[-1][0]

    fuel_build_specs    = apply_default_mpact_material_specs(fuel_build_specs, fuel.get_materials())
    element_build_specs = apply_default_mpact_material_specs(element_build_specs, central_element.get_materials())

    specs    = mpact_builder.HexLattice.Specs(element_specs = {fuel:            fuel_build_specs,
                                                               central_element: element_build_specs})

    # Build the full hex lattice and then trim to the progression problem domain
    # (i.e. remove top and bottom 3 rows and leftmost and rightmost 2 columns)
    core_map = [list(row[1:-1]) \
                for row in mpact_builder.build(lattice, specs).assembly_map[2:-2]]
    geometry = mpactpy.Core(core_map)

    states = [dict(state) for state in (states or [DEFAULT_MPACT_SETTINGS["state"]])]
    xsec_settings = dict(xsec_settings or DEFAULT_MPACT_SETTINGS["xsec"])
    options = dict(options or DEFAULT_MPACT_SETTINGS["options"])

    for state in states:
        state["tinlet"] = state.get("tinlet", f"{coolant.temperature}")

    options["bound_cond"] = "1 1 1 1 1 1"

    mpact_model = mpactpy.Model(geometry, states, xsec_settings, options)
    with open(filename, 'w') as file:
        file.write(mpact_model.write_to_string("TRIGA", indent=4))
