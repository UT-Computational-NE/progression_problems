from __future__ import annotations
from dataclasses import dataclass, field

import openmc

from progression_problems.constants import CM_PER_INCH
from progression_problems.TRIGA.NETL.default_materials import DefaultMaterials


@dataclass
class ReflectorCanister:
    """Dataclass for the TRIGA reflector canister.

    Attributes
    ----------
    radius : float
        Radius of the reflector canister [cm].
        Default: 42.0 * 0.5 inches (Ref. [2]_ pg. 54)
    height : float
        Height of the reflector canister [cm].
        Default: 23.13 inches (Ref. [2]_ pg. 55)
    core_centerline_offset : float
        Distance from core centerline to center of reflector canister [cm].
        Positive values indicate the canister center is above the core centerline, and
        negative values indicate it is below.
        Default: 0.565 inches (Ref. [2]_ pg. 55)
    material : openmc.Material
        Material of the reflector canister.
        Default: DefaultMaterials.graphite() (Ref. [2]_ pg. 48)

    References
    ----------
    .. [1] "University of Texas at Austin Nuclear Engineering Teaching Laboratory
           TRIGA Research Reactor", August 2023,
           https://www.nrc.gov/docs/ML2327/ML23279A146.pdf

    .. [2] D. R. Redhouse, et al., "Radiation Characterization Summary: NETL Beam Port
           1/5 Free-Field Environment at the 128-inch Core Centerline Adjacent Location,
           (NETL-FF-BP1/5-128-cca).", Nov. 2022. https://doi.org/10.2172/1898256
    """

    radius:                 float = 42.0 * 0.5 * CM_PER_INCH
    height:                 float = 23.13 * CM_PER_INCH
    core_centerline_offset: float = 0.565 * CM_PER_INCH
    material:               openmc.Material = field(default_factory=DefaultMaterials.graphite)

    def __post_init__(self):
        assert self.radius > 0, "Reflector radius must be positive."
        assert self.height > 0, "Reflector height must be positive."
