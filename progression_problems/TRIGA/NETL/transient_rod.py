from __future__ import annotations
from dataclasses import dataclass, field

import openmc

from progression_problems.constants import CM_PER_INCH
from progression_problems.TRIGA.NETL.default_materials import DefaultMaterials


@dataclass
class TransientRod:
    """Dataclass for the TRIGA transient rod.

    Attributes
    ----------
    cladding : TransientRod.Cladding
        Transient rod cladding specifications.
        Default: Cladding()
    fill_gas : openmc.Material
        Fill gas material.
        Default: DefaultMaterials.air() (Ref. [2]_ pg. 51)
    upper_element_plug : TransientRod.ElementPlug
        Upper element plug specifications.
        Default: 0.5 inches (Ref. [2]_ pg. 58)
    upper_magneform_fitting : TransientRod.MagneformFitting
        Upper Magneform fitting specifications.
        Default: MagneformFitting()
    absorber : TransientRod.Absorber
        Absorber specifications.
        Default: Absorber()
    lower_magneform_fitting : TransientRod.MagneformFitting
        Lower Magneform fitting specifications.
        Default: MagneformFitting()
    air_follower : TransientRod.AirGap
        Air follower specifications.
        Default: AirGap()
    lower_element_plug : TransientRod.ElementPlug
        Lower element plug specifications.
        Default: 0.5 inches (Ref. [2]_ pg. 58)
    maximum_withdrawal_distance : float
        Maximum withdrawal distance [cm].
        Default: 15 inches (Ref. [1]_ pg. 4-10)
    fraction_withdrawn : float
        Fraction of the maximum withdrawal distance the rod is withdrawn.
        Default: 0.0 (Fully Inserted).
    core_centerline_offset : float
        Offset of the absorber centerline from the core centerline
        when the control rod is fully inserted [cm].
        Default: 0.0 (assumed).

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
    class Cladding:
        """Dataclass for the cladding.

        Attributes
        ----------
        outer_radius : float
            Outer radius of the transient rod cladding [cm].
            Default: 1.25 * 0.5 inches (Ref. [1]_ Table 4.2)
        thickness : float
            Thickness of the transient rod cladding [cm].
            Default: 0.028 inches (Ref. [1]_ Table 4.2)
        material : openmc.Material
            Material of the cladding.
            Default: DefaultMaterials.aluminum() (Ref. [2]_ pg. 51)
        """

        outer_radius: float = 1.25 * 0.5 * CM_PER_INCH
        thickness:    float = 0.028 * CM_PER_INCH
        material:     openmc.Material = field(default_factory=DefaultMaterials.aluminum)

        def __post_init__(self):
            assert self.outer_radius > 0, "Transient Rod Cladding outer radius must be positive."
            assert self.thickness > 0, "Transient Rod Cladding thickness must be positive."

    @dataclass
    class ElementPlug:
        """Dataclass for the element plugs.

        Attributes
        ----------
        thickness : float
            Thickness of the element plug [cm].
            Default: 0.5 inches (Ref. [2]_ pg. 58)
        material : openmc.Material
            Material of the element plug.
            Default: DefaultMaterials.aluminum() (Ref. [2]_ pg. 51)
        """

        thickness: float = 0.5 * CM_PER_INCH
        material:  openmc.Material = field(default_factory=DefaultMaterials.aluminum)

        def __post_init__(self):
            assert self.thickness > 0, "Element Plug thickness must be positive."

    @dataclass
    class MagneformFitting:
        """
        Dataclass for the Magneform fittings.

        Attributes
        ----------
        thickness : float
            Thickness of the Magneform fitting [cm].
            Default: 1.0 inches (Ref. [2]_ pg. 58)
        material : openmc.Material
            Material of the Magneform fitting.
            Default: DefaultMaterials.aluminum() (Ref. [2]_ pg. 51)
        """

        thickness: float = 1.0 * CM_PER_INCH
        material:  openmc.Material = field(default_factory=DefaultMaterials.aluminum)

        def __post_init__(self):
            assert self.thickness > 0, "Magneform Fitting thickness must be positive."

    @dataclass
    class Absorber:
        """Dataclass for the absorber.

        Attributes
        ----------
        radius : float
            Radius of the absorber [cm].
            Default: 1.187 * 0.5 inches (Ref. [2]_ pg. 55)
        length : float
            Length of the absorber [cm].
            Default: 15.0 inches (Ref. [1]_ Table 4.2)
        material : openmc.Material
            Material of the absorber.
            Default: DefaultMaterials.control_rod_absorber() (Ref. [2]_ pg. 51)
        """

        radius:   float = 1.187 * 0.5 * CM_PER_INCH
        length:   float = 15.0 * CM_PER_INCH
        material: openmc.Material = field(default_factory=DefaultMaterials.control_rod_absorber)

        def __post_init__(self):
            assert self.radius > 0, "Absorber radius must be positive."
            assert self.length > 0, "Absorber length must be positive."

    @dataclass
    class AirGap:
        """Dataclass for the air gaps.

        Attributes
        ----------
        thickness : float
            Length of the air gap [cm].
            Default: 19.75 inches (Ref. [2]_ pg. 58)
        """

        thickness: float = 19.75 * CM_PER_INCH

        def __post_init__(self):
            assert self.thickness > 0, "Air Gap thickness must be positive."

    cladding:                    Cladding         = field(default_factory=Cladding)
    fill_gas:                    openmc.Material  = field(default_factory=DefaultMaterials.air)
    upper_element_plug:          ElementPlug      = field(default_factory=ElementPlug)
    upper_magneform_fitting:     MagneformFitting = field(default_factory=MagneformFitting)
    absorber:                    Absorber         = field(default_factory=Absorber)
    lower_magneform_fitting:     MagneformFitting = field(default_factory=MagneformFitting)
    air_follower:                AirGap           = field(default_factory=AirGap)
    lower_element_plug:          ElementPlug      = field(default_factory=ElementPlug)
    maximum_withdrawal_distance: float = 15.0 * CM_PER_INCH
    fraction_withdrawn:          float = 0.0
    core_centerline_offset:      float = 0.0

    def __post_init__(self):
        assert self.fraction_withdrawn >= 0.0, "Fraction withdrawn must be non-negative."
        assert self.fraction_withdrawn <= 1.0, "Fraction withdrawn cannot exceed 1.0."
        assert self.maximum_withdrawal_distance > 0.0, "Maximum withdrawal distance must be positive."
