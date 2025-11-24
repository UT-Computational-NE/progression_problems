from typing import Dict, List

import openmc

from progression_problems.constants import THERMAL_ENERGY_CUTOFF


def build_generic_openmc_tallies(spectrum_group_structure: str = "MPACT-51",
                                 universes: List[int] = []
) -> Dict[str, openmc.Tally]:
    """Build a set of generic OpenMC tallies for TRIGA problems.

    Parameters
    ----------
    spectrum_group_structure : str
        The energy group structure to use for the multi-group spectrum tally.
    universes : List[int]
        A list of universe IDs to which the tallies should be applied.

    Returns
    -------
    Dict[str, openmc.Tally]
        A dictionary of OpenMC tallies with string keys.
    """

    tallies: Dict[str, openmc.Tally] = {}

    TwoGroupFilter  = openmc.EnergyFilter([0., THERMAL_ENERGY_CUTOFF, 20.0e6])
    MultiGroupFilter = openmc.EnergyFilter(openmc.mgxs.GROUP_STRUCTURES[spectrum_group_structure])

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
        tallies['mesh_tally'].filters = [openmc.UniverseFilter(list(u for u in universes))]
        tallies['mesh_tally'].scores = ['flux', 'absorption', 'scatter', 'fission', 'nu-fission', 'kappa-fission']

    return tallies


DEFAULT_MPACT_SETTINGS: Dict[str, Dict[str, str]] = {
    "state": {"rated_power": "1.0",
              "power":       "1.0",
              "pressure":    "1.0",
              "rated_flow":  "1.0"},

    "xsec" : {'xsshielder' : 'T SUBGROUP'},

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
