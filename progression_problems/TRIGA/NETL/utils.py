from typing import Dict, List, Optional

import mpactpy

from coreforge import materials
from coreforge.materials.material import Material
from coreforge.mpact_builder.builder_specs import MaterialSpecs, DEFAULT_MPACT_MATERIAL_SPECS
import openmc

from progression_problems.constants import THERMAL_ENERGY_CUTOFF


def build_generic_openmc_tallies(spectrum_group_structure: str = "MPACT-51",
                                 universes: Optional[List[int]] = None,
                                 mesh: openmc.RegularMesh = None
) -> Dict[str, openmc.Tally]:
    """Build a set of generic OpenMC tallies for TRIGA problems.

    Parameters
    ----------
    spectrum_group_structure : str
        The energy group structure to use for the multi-group spectrum tally.
    universes : Optional[List[int]]
        A list of universe IDs to which the tallies should be applied.  Defaults to None.
    mesh : openmc.RegularMesh
        An optional mesh to use for mesh tallies.

    Returns
    -------
    Dict[str, openmc.Tally]
        A dictionary of OpenMC tallies with string keys.
    """

    tallies: Dict[str, openmc.Tally] = {}

    TwoGroupFilter  = openmc.EnergyFilter([0., THERMAL_ENERGY_CUTOFF, 20.0e6])

    if spectrum_group_structure not in openmc.mgxs.GROUP_STRUCTURES:
        available_group_structures = ", ".join(sorted(openmc.mgxs.GROUP_STRUCTURES))
        raise ValueError(
            f"Unsupported spectrum_group_structure {spectrum_group_structure!r}. "
            f"Expected one of: {available_group_structures}."
        )

    MultiGroupFilter = openmc.EnergyFilter(
        openmc.mgxs.GROUP_STRUCTURES[spectrum_group_structure]
    )

    tallies['flux'] = openmc.Tally(name='total_flux')
    tallies['flux'].scores = ['flux']

    tallies['total_rates'] = openmc.Tally(name='total_rates')
    tallies['total_rates'].scores = ['absorption', 'scatter', 'fission','nu-fission']   #  [neutrons/source]

    tallies['reaction_rates'] = openmc.Tally(name='reaction_rates')
    tallies['reaction_rates'].filters = [TwoGroupFilter]
    tallies['reaction_rates'].scores = ['absorption', 'scatter', 'fission']

    tallies['fission'] = openmc.Tally(name='fission')
    tallies['fission'].scores = ['fission', 'kappa-fission']     # Total fission reaction rate [fission/source]

    tallies['spectrum'] = openmc.Tally(name='spectrum_tally')
    tallies['spectrum'].filters = [MultiGroupFilter]
    tallies['spectrum'].scores = ['flux']

    tallies['flux_2G'] = openmc.Tally(name='flux_2G')
    tallies['flux_2G'].scores = ['flux']
    tallies['flux_2G'].filters = [TwoGroupFilter]

    tallies['source'] = openmc.Tally(name='source_tally')
    tallies['source'].scores = ['kappa-fission']      # Fission rate multiplied by the pseudo Q. [MeV/source neutron]

    if universes:
        tallies['mesh_tally'] = openmc.Tally(name='mesh_tally')
        tallies['mesh_tally'].scores = ['flux', 'absorption', 'scatter', 'fission', 'nu-fission', 'kappa-fission']
        tallies['mesh_tally'].filters = [openmc.UniverseFilter(universes)]
        if mesh:
            tallies['mesh_tally'].filters.append(openmc.MeshFilter(mesh))

    return tallies


DEFAULT_MPACT_SETTINGS: Dict[str, Dict[str, str]] = {
    "state": {"rated_power": "1.0",
              "power":       "1.0",
              "pressure":    "1.0",
              "rated_flow":  "1.0"},

    "xsec" : {'xslib'      : 'ORNL mpact51n19g_71_4.4m1_02212021.fmt',
              'xsshielder' : 'T SUBGROUP'},

    "options" : {'solver'     : '1 2',
                 'ray'        : '0.05 CHEBYSHEV-YAMAMOTO 16 3',
                 'conv_crit'  : '1.0E-6 1.0E-6',
                 'iter_lim'   : '50 1 1',
                 'vis_edits'  : 'F',
                 'scatt_meth' : 'TCP0',
                 'nodal'      : 'T SP3',
                 'axial_tl'   : 'T ISO LFLAT',
                 'parallel'   : '1 1 1 1'}
}


DEFAULT_MPACT_MATERIAL_SPECS_MAPPING: Dict[str, MaterialSpecs] = {
    "fuel":                 DEFAULT_MPACT_MATERIAL_SPECS[materials.UZrH],
    "zirc_filler":          DEFAULT_MPACT_MATERIAL_SPECS[materials.Zr],
    "stainless_steel":      DEFAULT_MPACT_MATERIAL_SPECS[materials.SS304],
    "graphite":             DEFAULT_MPACT_MATERIAL_SPECS[materials.Graphite],
    "aluminum":             DEFAULT_MPACT_MATERIAL_SPECS[materials.Al6061T6],
    "air":                  DEFAULT_MPACT_MATERIAL_SPECS[materials.Air],
    "molybdenum":           DEFAULT_MPACT_MATERIAL_SPECS[materials.Mo],
    "water":                DEFAULT_MPACT_MATERIAL_SPECS[materials.Water],
    "control_rod_absorber": DEFAULT_MPACT_MATERIAL_SPECS[materials.B4C],
    "cadmium":              mpactpy.Material.MPACTSpecs({}, False, False, False, False),
    }

def default_mpact_material_specs(materials_list: List[Material]) -> MaterialSpecs:
    """Get the default MPACT material specifications for a list of materials.

    Parameters
    ----------
    materials_list : List[Material]
        A list of materials for which to get the default MPACT specifications.

    Returns
    -------
    MaterialSpecs
        A dictionary mapping each material to its default MPACT specifications.
    """

    specs: MaterialSpecs = {}
    for material in materials_list:
        material_name = material.name.lower()
        if material_name in DEFAULT_MPACT_MATERIAL_SPECS_MAPPING:
            specs[material] = DEFAULT_MPACT_MATERIAL_SPECS_MAPPING[material_name]
    return specs
