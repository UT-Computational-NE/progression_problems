from __future__ import annotations
from dataclasses import dataclass, field

import openmc

from progression_problems.TRIGA.NETL.default_materials import DefaultMaterials


@dataclass
class Pool:
    """Dataclass for the TRIGA pool.

    Attributes
    ----------
    radius : float
        Radius of the pool [cm].
        Default: 90 cm (Ref. [2]_ pg. 54)
    height : float
        Height of the pool [cm].
        Default: 160 cm (Ref. [2]_ pg. 54)
    material : openmc.Material
        Material of the pool.
        Default: DefaultMaterials.water() (Ref. [2]_ pg. 48)

    References
    ----------
    .. [1] "University of Texas at Austin Nuclear Engineering Teaching Laboratory
           TRIGA Research Reactor", August 2023,
           https://www.nrc.gov/docs/ML2327/ML23279A146.pdf

    .. [2] D. R. Redhouse, et al., "Radiation Characterization Summary: NETL Beam Port
           1/5 Free-Field Environment at the 128-inch Core Centerline Adjacent Location,
           (NETL-FF-BP1/5-128-cca).", Nov. 2022. https://doi.org/10.2172/1898256
    """
    radius: float = 90.0
    height: float = 160.0
    material: openmc.Material = field(default_factory=DefaultMaterials.water)

    def __post_init__(self):
        assert self.radius > 0, "Pool radius must be positive."
        assert self.height > 0, "Pool height must be positive."
