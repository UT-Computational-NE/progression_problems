from __future__ import annotations
from dataclasses import dataclass, field
from math import cos, radians
from typing import List, Optional, Tuple

import openmc

from progression_problems.constants import CM_PER_INCH
from progression_problems.TRIGA.NETL.default_materials import DefaultMaterials


@dataclass
class BeamPort:
    """Dataclass for TRIGA beam ports.

    Attributes
    ----------
    inner_radius : float
        Inner radius of the beam port [cm].
        Default: 6.065 * 0.5 inches (Ref. [2]_ Figure 4 & 5)
    outer_radius : float
        Outer radius of the beam port [cm].
        Default: 6.625 inches (Ref. [2]_ Figure 4 & 5)
    rotation : List[List[float]]
        Rotation matrix (in degrees) of the beam port. Rotation is applied before translation.
        The beam port centerline is aligned with the y-axis before rotation.
        Default: [[0, 90, 90], [90, 0, 90], [90, 90, 0]] (i.e. no rotation).
    translation : Tuple[float, float, float]
        Translation vector of the beamport centerline from the center of the core [cm].
        Translation is applied after rotation.
    termination_plane : Optional[openmc.Plane]
        Plane representing the end (i.e. termination) of the beam port.
    tube_material : openmc.Material
        Material of the beam port tube.
        Default: DefaultMaterials.aluminum() (Ref. [2]_ pg. 48)
    fill_material : openmc.Material
        Fill material of the beam port.
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

    inner_radius:      float = 6.065 * 0.5 * CM_PER_INCH
    outer_radius:      float = 6.625 * CM_PER_INCH
    rotation:          List[List[float]] = field(default_factory=lambda: [[0.0, 90.0, 90.0],
                                                                          [90.0, 0.0, 90.0],
                                                                          [90.0, 90.0, 0.0]])
    translation:       Tuple[float, float, float] = (0.0, 0.0, 0.0)
    termination_plane: Optional[openmc.Plane] = None
    tube_material:     openmc.Material = field(default_factory=DefaultMaterials.aluminum)
    fill_material:     openmc.Material = field(default_factory=DefaultMaterials.air)

    def __post_init__(self):
        assert self.inner_radius > 0, "Beam Port inner radius must be positive."
        assert self.outer_radius > self.inner_radius, "Beam Port outer radius must be larger than inner radius."


def default_beamport_1_5() -> BeamPort:
    """Default beam port 1/5 specifications.

    Returns
    -------
    BeamPort
        Beam port 1/5 specifications from Ref. [2]_ pages 48, 56, 59
    """
    return BeamPort(translation = (35.2425, 0.0, -6.985),
                    rotation    = [[ 90.0, 180.0, 90.0],
                                   [  0.0,  90.0, 90.0],
                                   [ 90.0,  90.0,  0.0]])


def default_beamport_2() -> BeamPort:
    """Default beam port 2 specifications.

    Returns
    -------
    BeamPort
        Beam port 2 specifications from Ref. [2]_ pages 48, 56, 59
    """
    return BeamPort(translation       = (6.222, 35.255, -6.985),
                    rotation          = [[150.0,  60.0, 90.0],
                                         [120.0, 150.0, 90.0],
                                         [ 90.0,  90.0,  0.0]],
                    termination_plane = openmc.YPlane(y0=-12.621).rotate(
                    rotation          = [[cos(radians( 20.0)), cos(radians(125.0)), cos(radians(90.0))],
                                         [cos(radians(100.0)), cos(radians( 20.0)), cos(radians(90.0))],
                                         [cos(radians( 90.0)), cos(radians( 90.0)), cos(radians( 0.0))]]))


def default_beamport_3() -> BeamPort:
    """Default beam port 3 specifications.

    Returns
    -------
    BeamPort
        Beam port 3 specifications from Ref. [2]_ pages 48, 56, 59
    """
    return BeamPort(translation       = (0.0, 0.0, -6.985),
                    termination_plane = openmc.YPlane(y0 = 26.43188))


def default_beamport_4() -> BeamPort:
    """Default beam port 4 specifications.

    Returns
    -------
    BeamPort
        Beam port 4 specifications from Ref. [2]_ pages 48, 56, 59
    """
    return BeamPort(translation       = (-13.216, 22.871, -6.985),
                    rotation          = [[ 75.0, 60.0, 90.0],
                                         [120.0, 75.0, 90.0],
                                         [ 90.0, 90.0,  0.0]],
                    termination_plane = openmc.Plane(0.866025403784, 0.5, 0, -26.43188))
