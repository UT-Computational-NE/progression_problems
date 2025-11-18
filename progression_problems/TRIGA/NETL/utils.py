from typing import Dict, List

import openmc

from progression_problems.constants import THERMAL_ENERGY_CUTOFF


def build_generic_openmc_tallies(spectrum_group_structure: str = "MPACT-51"
) -> Dict[str, openmc.Tally]:
    """Build a set of generic OpenMC tallies for TRIGA problems.

    Parameters
    ----------
    spectrum_group_structure : str
        The energy group structure to use for the multi-group spectrum tally.

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

    return tallies
