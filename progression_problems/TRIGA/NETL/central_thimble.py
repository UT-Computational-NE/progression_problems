from __future__ import annotations
from dataclasses import dataclass, field

import openmc

from progression_problems.constants import CM_PER_INCH
from progression_problems.TRIGA.NETL.default_materials import DefaultMaterials


@dataclass
class CentralThimble:
    """Dataclass for the TRIGA central thimble.

    Attributes
    ----------
    inner_radius : float
        Inner radius of the central thimble [cm].
        Default: 1.33 * 0.5 inches (Ref. [1]_ Section 10.2.1.b)
    outer_radius : float
        Outer radius of the central thimble [cm].
        Default: 1.5 * 0.5 inches (Ref. [1]_ Section 10.2.1.b)
    material : openmc.Material
        Material of the central thimble cladding.
        Default: DefaultMaterials.aluminum() (Ref. [2]_ pg. 51)

    References
    ----------
    .. [1] "University of Texas at Austin Nuclear Engineering Teaching Laboratory
           TRIGA Research Reactor", August 2023,
           https://www.nrc.gov/docs/ML2327/ML23279A146.pdf

    .. [2] D. R. Redhouse, et al., "Radiation Characterization Summary: NETL Beam Port
           1/5 Free-Field Environment at the 128-inch Core Centerline Adjacent Location,
           (NETL-FF-BP1/5-128-cca).", Nov. 2022. https://doi.org/10.2172/1898256
    """

    inner_radius: float = 1.33 * 0.5 * CM_PER_INCH
    outer_radius: float = 1.5  * 0.5 * CM_PER_INCH
    material: openmc.Material = field(default_factory=DefaultMaterials.aluminum)

    def __post_init__(self):
        assert self.inner_radius > 0, "Central Thimble inner radius must be positive."
        assert self.outer_radius > self.inner_radius, "Central Thimble outer radius must be larger than inner radius."
