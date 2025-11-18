from __future__ import annotations
from dataclasses import dataclass, field

import openmc

from progression_problems.TRIGA.NETL.default_materials import DefaultMaterials


@dataclass
class GridPlate:
    """Class for TRIGA grid plates.

    Attributes
    ----------
    thickness : float
        Thickness of the grid plate [cm].
    fuel_penetration_radius : float
        Radius of penetrations in the grid plate at fuel positions [cm].
    control_rod_penetration_radius : float
        Radius of penetrations in the grid plate at control rod positions [cm].
    distance_from_core_centerline : float
        Distance from the core centerline to the nearest surface of the grid plate [cm].
    material : openmc.Material
        Material of the grid plate.
        Default: DefaultMaterials.aluminum() (Ref. [2]_ pg. 50)

    References
    ----------
    .. [1] "University of Texas at Austin Nuclear Engineering Teaching Laboratory
           TRIGA Research Reactor", August 2023,
           https://www.nrc.gov/docs/ML2327/ML23279A146.pdf

    .. [2] D. R. Redhouse, et al., "Radiation Characterization Summary: NETL Beam Port
           1/5 Free-Field Environment at the 128-inch Core Centerline Adjacent Location,
           (NETL-FF-BP1/5-128-cca).", Nov. 2022. https://doi.org/10.2172/1898256
    """

    thickness: float
    fuel_penetration_radius: float
    control_rod_penetration_radius: float
    distance_from_core_centerline: float
    material: openmc.Material = field(default_factory=DefaultMaterials.aluminum)

    def __post_init__(self):
        assert self.thickness > 0, "Grid Plate thickness must be positive."
        assert self.fuel_penetration_radius > 0, "Grid Plate fuel penetration radius must be positive."
        assert self.control_rod_penetration_radius > 0, "Grid Plate control rod penetration radius must be positive."
