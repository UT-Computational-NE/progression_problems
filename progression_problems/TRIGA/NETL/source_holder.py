from __future__ import annotations
from dataclasses import dataclass, field

import openmc

from progression_problems.constants import CM_PER_INCH
from progression_problems.TRIGA.NETL.default_materials import DefaultMaterials


@dataclass
class SourceHolder:
    """Dataclass for the TRIGA source holder.

    The source holder typically extends from the top grid plate to
    just above the bottom grid plate. (Ref. [2]_ pg. 54-55)

    Attributes
    ----------
    cavity : Cavity
        Source holder cavity specifications.
        Default: Cavity()
    cladding : Cladding
        Source holder cladding specifications.
        Default: Cladding()
    distance_from_lower_grid_plate : float
        Distance from the lower grid plate to the bottom of the source holder [cm].
        Default: 1.1934 cm (Ref. [2]_ pg. 55)

    References
    ----------
    .. [1] "University of Texas at Austin Nuclear Engineering Teaching Laboratory
           TRIGA Research Reactor", August 2023,
           https://www.nrc.gov/docs/ML2327/ML23279A146.pdf

    .. [2] D. R. Redhouse, et al., "Radiation Characterization Summary: NETL Beam Port
           1/5 Free-Field Environment at the 128-inch Core Centerline Adjacent Location,
           (NETL-FF-BP1/5-128-cca).", Nov. 2022. https://doi.org/10.2172/1898256
    """

    @dataclass
    class Cavity:
        """Dataclass for the source holder cavity.

        Attributes
        ----------
        radius : float
            Radius of the cavity [cm].
            Default: 0.981 * 0.5 inches (Ref. [1]_ Section 4.2.5)
        length : float
            Length of the cavity [cm].
            Default: 3.0 inches (Ref. [1]_ Section 4.2.5)
        core_centerline_offset : float
            Distance from core centerline to center of source holder cavity [cm].
            Positive values indicate the cavity center is above the core centerline, and
            negative values indicate it is below.
            Default: 0.0 inches (Ref. [2]_ pg. 55)
        material : openmc.Material
            Material of the cavity.
            Default: DefaultMaterials.air() (Ref. [2]_ pg. 54)
        """

        radius:                 float = 0.981 * 0.5 * CM_PER_INCH
        length:                 float = 3.0 * CM_PER_INCH
        core_centerline_offset: float = 0.0 * CM_PER_INCH
        material:               openmc.Material = field(default_factory=DefaultMaterials.air)

        def __post_init__(self):
            assert self.radius > 0, "Source Holder Cavity radius must be positive."
            assert self.length > 0, "Source Holder Cavity length must be positive."

    @dataclass
    class Cladding:
        """Dataclass for the source holder cladding.

        Attributes
        ----------
        outer_radius : float
            Outer radius of the source holder cladding [cm].
            Default: 1.435 * 0.5 inches (Ref. [2]_ pg. 54 & 55)
        material : openmc.Material
            Material of the cladding.
            Default: DefaultMaterials.aluminum() (Ref. [2]_ pg. 54)
        """

        outer_radius: float = 1.435 * 0.5 * CM_PER_INCH
        material:     openmc.Material = field(default_factory=DefaultMaterials.aluminum)

        def __post_init__(self):
            assert self.outer_radius > 0, "Source Holder Cladding outer radius must be positive."

    cavity:                         Cavity   = field(default_factory=Cavity)
    cladding:                       Cladding = field(default_factory=Cladding)
    core_centerline_offset:         float    = 0.0
    distance_from_lower_grid_plate: float    = 1.1934

    def __post_init__(self):
        assert self.distance_from_lower_grid_plate >= 0, "Distance from lower grid plate must be non-negative."
