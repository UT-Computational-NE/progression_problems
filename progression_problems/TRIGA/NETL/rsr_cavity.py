from __future__ import annotations
from dataclasses import dataclass, field

import openmc

from progression_problems.constants import CM_PER_INCH
from progression_problems.TRIGA.NETL.default_materials import DefaultMaterials


@dataclass
class RSRCavity:
    """Dataclass for TRIGA Rotary Specimen Rack Cavity.

    Instrument tubes are equally spaced around the circumference
    of the rotary specimen rack. (Ref. [1]_ pg. 10-27)

    Attributes
    ----------
    outer_radius : float
        Outer radius of the rotary specimen rack [cm].
        Default: 28.625 * 0.5 inches (Ref. [2]_ pg. 55)
    height : float
        Height of the rotary specimen rack [cm].
        Default: 10.8174 inches (Ref. [2]_ pg. 55)
    number_of_tubes : int
        Number of specimen tubes in the rotary specimen rack.
        Default: 40 (Ref. [1]_ pg. 10-27)
    tube_to_center_distance : float
        Distance from center of rotary specimen rack to center of the specimen tubes [cm].
        Default: 26.312 * 0.5 inches (Ref. [1]_ pg. 10-27)
    tube_specs : RSRCavity.SpecimenTube
        Specimen tube specifications.
        Default: SpecimenTube()
    material : openmc.Material
        Cavity fill material of the rotary specimen rack.
        Default: DefaultMaterials.air() (Ref. [2]_ pg. 48)

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
    class SpecimenTube:
        """Dataclass for specimen tubes.

        Attributes
        ----------
        outer_radius : float
            Outer radius of the specimen tube [cm].
            Default: 1.0 * 0.5 inches (Ref. [2]_ pg. 56 & 57)
        thickness : float
            Thickness of the specimen tube wall [cm].
            Default: 0.058 inches (Ref. [1]_ pg. 10-27)
        material : openmc.Material
            Cladding material of the specimen tube.
            Default: DefaultMaterials.aluminum() (assumed)
        """

        outer_radius: float = 1.0 * 0.5 * CM_PER_INCH
        thickness:    float = 0.058 * CM_PER_INCH
        material: openmc.Material = field(default_factory=DefaultMaterials.aluminum)

        def __post_init__(self):
            assert self.outer_radius > 0, "Specimen Tube outer radius must be positive."
            assert self.thickness > 0, "Specimen Tube thickness must be positive."

    outer_radius:            float        = 28.625 * 0.5 * CM_PER_INCH
    height:                  float        = 10.8174 * CM_PER_INCH
    number_of_tubes:         int          = 40
    tube_to_center_distance: float        = 26.312 * 0.5 * CM_PER_INCH
    tube_specs:              SpecimenTube = field(default_factory=SpecimenTube)
    material:                openmc.Material = field(default_factory=DefaultMaterials.air)

    def __post_init__(self):
        assert self.outer_radius > 0, "Rotary Specimen Rack outer radius must be positive."
        assert self.height > 0, "Rotary Specimen Rack height must be positive."
        assert self.number_of_tubes > 0, "Rotary Specimen Rack number of tubes must be positive."
        assert self.tube_to_center_distance > 0, "Rotary Specimen Rack tube to center distance must be positive."
