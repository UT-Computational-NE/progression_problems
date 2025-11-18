from __future__ import annotations
from dataclasses import dataclass, field
from functools import partial

import openmc

from progression_problems.constants import CM_PER_INCH
from progression_problems.TRIGA.NETL.default_materials import DefaultMaterials


@dataclass
class FuelFollowerControlRod:
    """Dataclass for TRIGA fuel follower control rods.

    Attributes
    ----------
    cladding : Cladding
        Cladding specifications.
        Default: Cladding()
    upper_element_plug : ElementPlug
        Upper element plug specifications.
        Default thickness: 1.5 inches (Ref. [2]_ pg. 58)
    upper_air_gap : AirGap
        Above the upper magneform fitting gap specifications.
        Default thickness: 3.5 inches (Ref. [2]_ pg. 58)
    upper_magneform_fitting : MagneformFitting
        Upper Magneform fitting specifications.
        Default thickness: 0.5 inches (Ref. [2]_ pg. 58)
    above_absorber_air_gap : AirGap
        Above the absorber air gap specifications.
        Default thickness: 1/8 inches (Ref. [2]_ pg. 58)
    absorber : Absorber
        Absorber specifications.
        Default: Absorber()
    middle_magneform_fitting : MagneformFitting
        Middle Magneform fitting specifications.
        Default thickness: 0.5 inches (Ref. [2]_ pg. 58)
    above_fuel_follower_air_gap : AirGap
        Above the fuel follower air gap specifications.
        Default thickness: 0.25 inches (Ref. [2]_ pg. 58)
    zr_fill_rod : ZrFillRod
        Zr Fill Rod specifications.
        Default: ZrFillRod()
    fuel_follower : FuelFollower
        Fuel follower specifications.
        Default: FuelFollower()
    lower_magneform_fitting : MagneformFitting
        Lower Magneform fitting specifications.
        Default thickness: 1.0 inches (Ref. [2]_ pg. 58)
    lower_air_gap : AirGap
        Below the lower element plug air gap specifications.
        Default thickness: 5.375 inches (Ref. [2]_ pg. 58)
    lower_element_plug : ElementPlug
        Lower element plug specifications.
        Default thickness: 0.5 inches (Ref. [2]_ pg. 58)
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
            Outer radius of the cladding [cm].
            Default: 1.31 * 0.5 inches (Ref. [2]_ pg. 55)
        thickness : float
            Thickness of the cladding [cm].
            Default: 0.02 inches (Ref. [2]_ pg. 55)
        material : openmc.Material
            Material of the cladding.
            Default: DefaultMaterials.stainless_steel() (Ref. [2]_ pg. 52)
        """

        outer_radius: float = 1.31 * 0.5 * CM_PER_INCH
        thickness:    float = 0.02 * CM_PER_INCH
        material:     openmc.Material = field(default_factory=DefaultMaterials.stainless_steel)

        def __post_init__(self):
            assert self.outer_radius > 0, "Fuel Follower Control Rod Cladding outer radius must be positive."
            assert self.thickness > 0, "Fuel Follower Control Rod Cladding thickness must be positive."

    @dataclass
    class ElementPlug:
        """Dataclass for the element plugs.

        Attributes
        ----------
        thickness : float
            Thickness of the element plug [cm].
        material : openmc.Material
            Material of the element plug.
            Default: DefaultMaterials.stainless_steel() (Ref. [2]_ pg. 51)
        """

        thickness: float
        material:  openmc.Material = field(default_factory=DefaultMaterials.stainless_steel)

        def __post_init__(self):
            assert self.thickness > 0, "Element Plug thickness must be positive."

    @dataclass
    class MagneformFitting:
        """Dataclass for the Magneform fittings.

        Attributes
        ----------
        thickness : float
            Thickness of the Magneform fitting [cm].
        material : openmc.Material
            Material of the Magneform fitting.
            Default: DefaultMaterials.stainless_steel() (Ref. [2]_ pg. 51)
        """

        thickness: float
        material:  openmc.Material = field(default_factory=DefaultMaterials.stainless_steel)

        def __post_init__(self):
            assert self.thickness > 0, "Magneform Fitting thickness must be positive."

    @dataclass
    class Absorber:
        """Dataclass for the absorber.

        Attributes
        ----------
        radius : float
            Radius of the absorber [cm].
            Default: 1.3 * 0.5 inches (Ref. [2]_ pg. 55)
        length : float
            Length of the absorber [cm].
            Default: 15.0 inches (Ref. [2]_ pg. 58)
        material : openmc.Material
            Material of the absorber.
            Default: DefaultMaterials.control_rod_absorber() (Ref. [2]_ pg. 52)
        """

        radius:   float = 1.3 * 0.5 * CM_PER_INCH
        length:   float = 15.0 * CM_PER_INCH
        material: openmc.Material = field(default_factory=DefaultMaterials.control_rod_absorber)

        def __post_init__(self):
            assert self.radius > 0, "Absorber radius must be positive."
            assert self.length > 0, "Absorber length must be positive."

    @dataclass
    class FuelFollower:
        """Dataclass for the fuel follower specification.

        Attributes
        ----------
        inner_radius : float
            Inner radius of the fuel follower [cm].
            Default: 0.25 * 0.5 inches (Ref. [2]_ pg. 55)
        length : float
            Length of the fuel follower [cm].
            Default: 15.0 inches (Ref. [2]_ pg. 58)
        material : openmc.Material
            Material of the fuel follower.
            Default: DefaultMaterials.fresh_fuel(density=6.0124)
            The default material density is set to 6.0124 g/cm3 to match the
            fuel follower density in Ref. [2]_ pg. 52, which is slightly different
            from the fuel meat density.  Normally the fuel composition would reflect some
            burnup, but this specification is not provided in the reference, so fresh
            fuel is used instead.
        """

        inner_radius: float = 0.25 * 0.5 * CM_PER_INCH
        length:       float = 15.0 * CM_PER_INCH
        material:     openmc.Material = field(default_factory=lambda: DefaultMaterials.fresh_fuel(density=6.0124))

        def __post_init__(self):
            assert self.inner_radius > 0, "Fuel Follower inner radius must be positive."
            assert self.length > 0, "Fuel Follower length must be positive."

    @dataclass
    class ZrFillRod:
        """Dataclass for the Zr Fill Rod.

        Attributes
        ----------
        radius : float
            Default: 0.25 * 0.5 inches (Ref. [2]_ pg. 55)
            Radius at room temperature [cm]. At operating temperatures,
            the Zr rod typically expands to fill the inner radius of the fuel follower.
        material : openmc.Material
            Material of the Zr Fill Rod.
            Default: DefaultMaterials.zirc_filler() (Ref. [2]_ pg. 52)
        """
        radius:   float = 0.25 * 0.5 * CM_PER_INCH
        material: openmc.Material = field(default_factory=DefaultMaterials.zirc_filler)

        def __post_init__(self):
            assert self.radius > 0, "Zr Fill Rod radius must be positive."

    @dataclass
    class AirGap:
        """Dataclass for the air gaps.

        Attributes
        ----------
        thickness : float
            Thickness of the air gap [cm].
        material : openmc.Material
            Material of the air gap.
            Default: DefaultMaterials.air() (Ref. [2]_ pg. 51)
        """

        thickness: float
        material:  openmc.Material = field(default_factory=DefaultMaterials.air)

        def __post_init__(self):
            assert self.thickness > 0, "Air Gap thickness must be positive."

    cladding:                    Cladding         = field(default_factory=Cladding)
    upper_element_plug:          ElementPlug      = field(default_factory=
                                                          partial(ElementPlug, thickness=1.5 * CM_PER_INCH))
    upper_air_gap:               AirGap           = field(default_factory=partial(AirGap, thickness=3.5 * CM_PER_INCH))
    upper_magneform_fitting:     MagneformFitting = field(default_factory=
                                                          partial(MagneformFitting, thickness=0.5 * CM_PER_INCH))
    above_absorber_air_gap:      AirGap           = field(default_factory=partial(AirGap, thickness=0.125 * CM_PER_INCH))
    absorber:                    Absorber         = field(default_factory=Absorber)
    middle_magneform_fitting:    MagneformFitting = field(default_factory=
                                                          partial(MagneformFitting, thickness=0.5 * CM_PER_INCH))
    above_fuel_follower_air_gap: AirGap           = field(default_factory=partial(AirGap, thickness=0.25 * CM_PER_INCH))
    zr_fill_rod:                 ZrFillRod        = field(default_factory=ZrFillRod)
    fuel_follower:               FuelFollower     = field(default_factory=FuelFollower)
    lower_magneform_fitting:     MagneformFitting = field(default_factory=
                                                          partial(MagneformFitting, thickness=1.0 * CM_PER_INCH))
    lower_air_gap:               AirGap           = field(default_factory=partial(AirGap, thickness=5.375 * CM_PER_INCH))
    lower_element_plug:          ElementPlug      = field(default_factory=
                                                          partial(ElementPlug, thickness=0.5 * CM_PER_INCH))
    maximum_withdrawal_distance: float = 15.0 * CM_PER_INCH
    fraction_withdrawn:          float = 0.0
    core_centerline_offset:      float = 0.0

    def __post_init__(self):
        assert self.fraction_withdrawn >= 0.0, "Fraction withdrawn must be non-negative."
        assert self.fraction_withdrawn <= 1.0, "Fraction withdrawn cannot exceed 1.0."
        assert self.maximum_withdrawal_distance > 0.0, "Maximum withdrawal distance must be positive."
