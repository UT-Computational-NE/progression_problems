from __future__ import annotations
from dataclasses import dataclass, field
from functools import partial

from progression_problems.constants import CM_PER_INCH
from progression_problems.TRIGA.NETL.beam_port import (BeamPort, default_beamport_1_5,
                                                                 default_beamport_2,
                                                                 default_beamport_3,
                                                                 default_beamport_4)
from progression_problems.TRIGA.NETL.core import Core
from progression_problems.TRIGA.NETL.grid_plate import GridPlate
from progression_problems.TRIGA.NETL.pool import Pool
from progression_problems.TRIGA.NETL.reflector_canister import ReflectorCanister
from progression_problems.TRIGA.NETL.rsr_cavity import RSRCavity
from progression_problems.TRIGA.NETL.shroud import Shroud


@dataclass
class Reactor:
    """Dataclass for NETL TRIGA reactor specifications.

    This is the top-level container that brings together all NETL TRIGA
    reactor components including the pool, core, grid plates, beam ports,
    and other structures.

    References
    ----------
    .. [1] "University of Texas at Austin Nuclear Engineering Teaching Laboratory
           TRIGA Research Reactor", August 2023,
           https://www.nrc.gov/docs/ML2327/ML23279A146.pdf

    .. [2] D. R. Redhouse, et al., "Radiation Characterization Summary: NETL Beam Port
           1/5 Free-Field Environment at the 128-inch Core Centerline Adjacent Location,
           (NETL-FF-BP1/5-128-cca).", Nov. 2022. https://doi.org/10.2172/1898256

    Attributes
    ----------
    pool : Pool
        The TRIGA pool specifications.
        Default: Pool()
    reflector_canister : ReflectorCanister
        The TRIGA reflector canister specifications.
        Default: ReflectorCanister()
    shroud : Shroud
        The TRIGA shroud specifications.
        Default: Shroud()
    beam_port_1_5 : BeamPort
        The TRIGA beam port 1/5 specifications.
        Default: default_beamport_1_5()
    beam_port_2 : BeamPort
        The TRIGA beam port 2 specifications.
        Default: default_beamport_2()
    beam_port_3 : BeamPort
        The TRIGA beam port 3 specifications.
        Default: default_beamport_3()
    beam_port_4 : BeamPort
        The TRIGA beam port 4 specifications.
        Default: default_beamport_4()
    rotary_specimen_rack_cavity : RSRCavity
        The TRIGA rotary specimen rack specifications.
        Default: RSRCavity()
    core : Core
        The TRIGA core specifications.
        Default: Core()
    upper_grid_plate : GridPlate
        The TRIGA upper grid plate specifications.
        Default: thickness                      = 0.62  * CM_PER_INCH (Ref. [2]_ pg. 55)
                 fuel_penetration_radius        = 1.505 * 0.5 * CM_PER_INCH (Ref. [1]_ Section 4.2.4.a)
                 control_rod_penetration_radius = 1.505 * CM_PER_INCH (Ref. [1]_ Section 4.2.4.a)
                 distance_from_core_centerline  = 12.75 * CM_PER_INCH (Ref. [2]_ pg. 55)
    lower_grid_plate : GridPlate
        The TRIGA lower grid plate specifications.
        Default: thickness                      = 1.25  * CM_PER_INCH (Ref. [2]_ pg. 55)
                 fuel_penetration_radius        = 1.25  * 0.5 * CM_PER_INCH (Ref. [1]_ Section 4.2.4.b)
                 control_rod_penetration_radius = 1.505 * CM_PER_INCH (Ref. [1]_ Section 4.2.4.b)
                 distance_from_core_centerline  = 13.06 * CM_PER_INCH (Ref. [2]_ pg. 55)

    References
    ----------
    .. [1] "University of Texas at Austin Nuclear Engineering Teaching Laboratory
           TRIGA Research Reactor", August 2023,
           https://www.nrc.gov/docs/ML2327/ML23279A146.pdf

    .. [2] D. R. Redhouse, et al., "Radiation Characterization Summary: NETL Beam Port
           1/5 Free-Field Environment at the 128-inch Core Centerline Adjacent Location,
           (NETL-FF-BP1/5-128-cca).", Nov. 2022. https://doi.org/10.2172/1898256
    """

    pool: Pool = field(default_factory=Pool)
    reflector_canister: ReflectorCanister = field(default_factory=ReflectorCanister)
    shroud: Shroud = field(default_factory=Shroud)
    beam_port_1_5: BeamPort = field(default_factory=default_beamport_1_5)
    beam_port_2: BeamPort = field(default_factory=default_beamport_2)
    beam_port_3: BeamPort = field(default_factory=default_beamport_3)
    beam_port_4: BeamPort = field(default_factory=default_beamport_4)
    rotary_specimen_rack_cavity: RSRCavity = field(default_factory=RSRCavity)
    core: Core = field(default_factory=Core)
    upper_grid_plate: GridPlate = field(default_factory=partial(GridPlate,
                                                                 thickness=0.62 * CM_PER_INCH,
                                                                 fuel_penetration_radius=1.505 * 0.5 * CM_PER_INCH,
                                                                 control_rod_penetration_radius=1.505 * CM_PER_INCH,
                                                                 distance_from_core_centerline=12.75 * CM_PER_INCH))
    lower_grid_plate: GridPlate = field(default_factory=partial(GridPlate,
                                                                 thickness=1.25 * CM_PER_INCH,
                                                                 fuel_penetration_radius=1.25 * 0.5 * CM_PER_INCH,
                                                                 control_rod_penetration_radius=1.505 * CM_PER_INCH,
                                                                 distance_from_core_centerline=13.06 * CM_PER_INCH))
