from __future__ import annotations
from dataclasses import dataclass, field

import openmc

from progression_problems.constants import CM_PER_INCH
from progression_problems.TRIGA.NETL.default_materials import DefaultMaterials


@dataclass
class Shroud:
    """Dataclass for the TRIGA shroud.

    Attributes
    ----------
    thickness : float
        Thickness of the shroud [cm].
        Default: 3/16 inches (Ref. [2]_ pg. 54 & 55)
    height : float
        Height of the shroud [cm].
        Default: 23.13 inches (Ref. [2]_ pg. 55)
    large_hex_inradius : float
        Inradius of the the shroud large hexagon [cm].
        Default: 10.75 inches (Ref. [2]_ pg. 54)
    small_hex_inradius : float
        Inradius of the the shroud small hexagon [cm].
        Default: 10.21875 inches (Ref. [2]_ pg. 55)
    material : openmc.Material
        Material of the shroud.
        Default: DefaultMaterials.aluminum() (Ref. [2]_ pg. 48)

    References
    ----------
    .. [1] "University of Texas at Austin Nuclear Engineering Teaching Laboratory
           TRIGA Research Reactor", August 2023,
           https://www.nrc.gov/docs/ML2327/ML23279A146.pdf

    .. [2] D. R. Redhouse, et al., "Radiation Characterization Summary: NETL Beam Port
           1/5 Free-Field Environment at the 128-inch Core Centerline Adjacent Location,
           (NETL-FF-BP1/5-128-cca).", Nov. 2022. https://doi.org/10.2172/1898256
    """

    thickness:          float = 0.1875 * CM_PER_INCH
    height:             float = 23.13 * CM_PER_INCH
    large_hex_inradius: float = 10.75 * CM_PER_INCH
    small_hex_inradius: float = 10.21875 * CM_PER_INCH
    material:           openmc.Material = field(default_factory=DefaultMaterials.aluminum)

    def __post_init__(self):
        assert self.thickness > 0, "Shroud thickness must be positive."
        assert self.height > 0, "Shroud height must be positive."
        assert self.large_hex_inradius > 0, "Shroud large hex inradius must be positive."
        assert self.small_hex_inradius > 0, "Shroud small hex inradius must be positive."
        assert self.large_hex_inradius > self.small_hex_inradius, \
            "Shroud large hex inradius must be larger than small hex inradius."
