from __future__ import annotations
from dataclasses import dataclass, field
from functools import partial
from math import cos, radians
from typing import ClassVar, Literal, Optional, Dict, Tuple, List, TypeAlias

import openmc

from progression_problems.constants import CM_PER_INCH
from progression_problems.TRIGA.NETL.default_materials import DefaultMaterials


@dataclass
class TRIGA:
    """Dataclass for TRIGA specifications

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
    pool : TRIGA.Pool
        The TRIGA pool specifications.
        Default: TRIGA.Pool()
    reflector : TRIGA.Reflector
        The TRIGA reflector specifications.
        Default: TRIGA.Reflector()
    upper_grid_plate : TRIGA.GridPlate
        The TRIGA upper grid plate specifications.
        Default: thickness                      = 0.62  * CM_PER_INCH (Ref. [2]_ pg. 55)
                 fuel_penetration_radius        = 1.505 * 0.5 * CM_PER_INCH (Ref. [1]_ Section 4.2.4.a)
                 control_rod_penetration_radius = 1.505 * 0.5 * CM_PER_INCH (Ref. [1]_ Section 4.2.4.a)
                 distance_from_core_centerline  = 12.75 * CM_PER_INCH (Ref. [2]_ pg. 55)
    lower_grid_plate : TRIGA.GridPlate
        The TRIGA lower grid plate specifications.
        Default: thickness                      = 1.25  * CM_PER_INCH (Ref. [2]_ pg. 55)
                 fuel_penetration_radius        = 1.25  * 0.5 * CM_PER_INCH (Ref. [1]_ Section 4.2.4.b)
                 control_rod_penetration_radius = 1.505 * 0.5 * CM_PER_INCH (Ref. [1]_ Section 4.2.4.b)
                 distance_from_core_centerline  = 13.06 * CM_PER_INCH (Ref. [2]_ pg. 55)
    shroud : TRIGA.Shroud
        The TRIGA shroud specifications.
        Default: TRIGA.Shroud()
    beam_port_1_5 : TRIGA.BeamPort
        The TRIGA beam port 1/5 specifications.
        Default: TRIGA.default_beamport_1_5()
    beam_port_2 : TRIGA.BeamPort
        The TRIGA beam port 2 specifications.
        Default: TRIGA.default_beamport_2()
    beam_port_3 : TRIGA.BeamPort
        The TRIGA beam port 3 specifications.
        Default: TRIGA.default_beamport_3()
    beam_port_4 : TRIGA.BeamPort
        The TRIGA beam port 4 specifications.
        Default: TRIGA.default_beamport_4()
    rotary_specimen_rack_cavity : TRIGA.RSRCavity
        The TRIGA rotary specimen rack specifications.
        Default: TRIGA.RSRCavity()
    core : TRIGA.Core
        The TRIGA core specifications.
        Default: TRIGA.Core()
    """

    @dataclass
    class FuelElement:
        """Dataclass for TRIGA fuel elements.

        Attributes
        ----------
        cladding : FuelElement.Cladding
            Cladding specifications.
            Default: Cladding()
        upper_end_fitting : FuelElement.EndFitting
            Upper End Fitting specifications.
            Default length: 7.3552 cm (Ref. [2]_ pg. 55)
            This is a value that when approximating the shape of the upper end fitting as
            a cone gives a reasonable approximation.
        upper_air_gap : FuelElement.AirGap
            Above Upper Graphite Reflector Air Gap specifications.
            Default: AirGap()
        upper_graphite_reflector : FuelElement.GraphiteReflector
            Upper Graphite Reflector specifications.
            Default thickness: 2.6 inches (Ref. [2]_ pg. 55)
        zr_fill_rod : FuelElement.ZrFillRod
            Zr fill rod specifications.
            Default: ZrFillRod()
        fuel_meat : FuelElement.FuelMeat
            Fuel meat specifications.
            Default: FuelMeat()
        moly_disc : FuelElement.MolyDisc
            Molybdenum Disc specifications.
            Default: MolyDisc()
        lower_graphite_reflector : FuelElement.GraphiteReflector
            Lower Graphite Reflector specifications.
            Default thickness: 3.7 inches (Ref. [2]_ pg. 55)
        lower_end_fitting : FuelElement.EndFitting
            Lower End Fitting specifications.
            Default length: 7.6209 cm (Ref. [2]_ pg. 55)
            This is a value that when approximating the shape of the lower end fitting as
            a cone gives a reasonable approximation.
        interior_length : float
            Interior length of the fuel element [cm]. This is the length from the bottom of the
            lower graphite reflector to the top of the upper air gap.
        """

        @dataclass
        class ZrFillRod:
            """Dataclass for Zr Fill Rod.

            Attributes
            ----------
            radius : float
                Radius at room temperature [cm]. At operating temperatures,
                the Zr rod typically expands to fill the inner radius of the fuel meat.
                Default: 0.25 * 0.5 inches (Ref. [2]_ pg. 55)
            material : openmc.Material
                Material of the Zr Fill Rod.
                Default: DefaultMaterials.zirc_filler() (Ref. [2]_ pg. 51)
            """
            radius: float = 0.25 * 0.5 * CM_PER_INCH
            material: openmc.Material = field(default_factory=DefaultMaterials.zirc_filler)

            def __post_init__(self):
                assert self.radius > 0, "Zr Fill Rod radius must be positive."

        @dataclass
        class FuelMeat:
            """Dataclass for Fuel Meat.

            Attributes
            ----------
            inner_radius : float
                Inner radius of the fuel meat [cm].
                Default: 0.25 * 0.5 inches (Ref. [1]_ pg. 4-2)
            outer_radius : float
                Outer radius of the fuel meat [cm].
                Default: 1.435 * 0.5 inches (Ref. [1]_ Table 4.1)
            length : float
                Length of the fuel meat [cm].
                Default: 15.0 inches (Ref. [1]_ Table 4.1)
            material : openmc.Material
                Material of the Fuel Meat.
                Default: DefaultMaterials.fresh_fuel() (Ref. [2]_ pg. 51)
            """
            inner_radius: float = 0.25  * 0.5 * CM_PER_INCH
            outer_radius: float = 1.435 * 0.5 * CM_PER_INCH
            length:       float = 15.0 * CM_PER_INCH
            material:     openmc.Material = field(default_factory=DefaultMaterials.fresh_fuel)

            def __post_init__(self):
                assert self.inner_radius > 0, "Fuel Meat inner radius must be positive."
                assert self.outer_radius > self.inner_radius, "Fuel Meat outer radius must be larger than inner radius."
                assert self.length > 0, "Fuel Meat length must be positive."

        @dataclass
        class Cladding:
            """Dataclass for Cladding.

            Attributes
            ----------
            thickness : float
                Thickness of the fuel cladding [cm].
                Default: 0.020 inches (Ref. [1]_ Table 4.1)
            outer_radius : float
                Outer radius of the fuel cladding [cm].
                Default: 1.475 * 0.5 inches (Ref. [1]_ Table 4.1)
            material : openmc.Material
                Material of the Cladding.
                Default: DefaultMaterials.stainless_steel() (Ref. [2]_ pg. 51)
            """
            thickness:    float = 0.020 * CM_PER_INCH
            outer_radius: float = 1.475 * 0.5 * CM_PER_INCH
            material:     openmc.Material = field(default_factory=DefaultMaterials.stainless_steel)

            def __post_init__(self):
                assert self.thickness > 0, "Cladding thickness must be positive."
                assert self.outer_radius > 0, "Cladding outer radius must be positive."

        @dataclass
        class GraphiteReflector:
            """Dataclass for Graphite Reflector.

            Attributes
            ----------
            radius : float
                Radius of the graphite reflector [cm].
                Default: 1.430 * 0.5 inches (Ref. [1]_ pg. 4-4)
            thickness : float
                Thickness of the graphite reflector [cm].
                Default: 3.420 inches (Ref. [1]_ pg. 4-4)
            material : openmc.Material
                Material of the Graphite Reflector.
                Default: DefaultMaterials.graphite() (Ref. [2]_ pg. 50)
            """
            radius:    float = 1.430 * 0.5 * CM_PER_INCH
            thickness: float = 3.420 * CM_PER_INCH
            material:  openmc.Material = field(default_factory=DefaultMaterials.graphite)

            def __post_init__(self):
                assert self.radius > 0, "Graphite Reflector radius must be positive."
                assert self.thickness > 0, "Graphite Reflector thickness must be positive."

        @dataclass
        class MolyDisc:
            """Dataclass for Molybdenum Discs.

            Attributes
            ----------
            radius : float
                Radius of the molybdenum disc [cm].
                Default: 1.431 * 0.5 inches (Ref. [1]_ pg. 4-3)
            thickness : float
                Thickness of the molybdenum disc [cm].
                Default: 0.031 inches (Ref. [1]_ pg. 4-3)
            material : openmc.Material
                Material of the Moly Disc.
                Default: DefaultMaterials.molybdenum() (Ref. [2]_ pg. 51)
            """
            radius:    float = 1.431 * 0.5 * CM_PER_INCH
            thickness: float = 0.031 * CM_PER_INCH
            material:  openmc.Material = field(default_factory=DefaultMaterials.molybdenum)

            def __post_init__(self):
                assert self.radius > 0, "Moly Disc radius must be positive."
                assert self.thickness > 0, "Moly Disc thickness must be positive."

        @dataclass
        class AirGap:
            """Dataclass for Air Gaps.

            Attributes
            ----------
            thickness : float
                Thickness of the air gap above the upper graphite reflector [cm].
                Default: 0.5 inches (Ref. [1]_ pg. 4-3)
            material : openmc.Material
                Material of the air gap.
                Default: DefaultMaterials.air() (Ref. [2]_ pg. 50)
            """
            thickness: float = 0.5 * CM_PER_INCH
            material:  openmc.Material = field(default_factory=DefaultMaterials.air)

            def __post_init__(self):
                assert self.thickness > 0, "Air Gap thickness must be positive."

        @dataclass
        class EndFitting:
            """Dataclass for End Fittings.

            When constructing neutronics models, the end fittings will
            be approximated as a cone with the given length (i.e. distance from base to apex)

            Attributes
            ----------
            length : float
                Length of the end fitting [cm].
            direction : Literal['up', 'down']
                Direction of the end fitting, either 'up' or 'down'.
            material : openmc.Material
                Material of the end fitting.
                Default: DefaultMaterials.stainless_steel() (Ref. [2]_ pg. 51)
            """
            length:    float
            direction: Literal['up', 'down']
            material:  openmc.Material = field(default_factory=DefaultMaterials.stainless_steel)

            def __post_init__(self):
                assert self.length > 0, "End Fitting length must be positive."
                assert self.direction in ('up', 'down'), "End Fitting direction must be either 'up' or 'down'."

        cladding:                 Cladding          = field(default_factory=Cladding)
        upper_end_fitting:        EndFitting        = field(default_factory=
                                                            partial(EndFitting, length=7.3552, direction='up'))
        upper_air_gap:            AirGap            = field(default_factory=AirGap)
        upper_graphite_reflector: GraphiteReflector = field(default_factory=
                                                            partial(GraphiteReflector, thickness=2.56 * CM_PER_INCH))
        zr_fill_rod:              ZrFillRod         = field(default_factory=ZrFillRod)
        fuel_meat:                FuelMeat          = field(default_factory=FuelMeat)
        moly_disc:                MolyDisc          = field(default_factory=MolyDisc)
        lower_graphite_reflector: GraphiteReflector = field(default_factory=
                                                            partial(GraphiteReflector, thickness=3.72 * CM_PER_INCH))
        lower_end_fitting:        EndFitting        = field(default_factory=
                                                            partial(EndFitting, length=7.6209, direction='down'))

        def __post_init__(self):
            self.interior_length = self.lower_graphite_reflector.thickness + \
                                   self.moly_disc.thickness                + \
                                   self.fuel_meat.length                   + \
                                   self.upper_graphite_reflector.thickness + \
                                   self.upper_air_gap.thickness


    @dataclass
    class GraphiteElement:
        """Dataclass for TRIGA graphite elements.

        Attributes
        ----------
        cladding : GraphiteElement.Cladding
            Cladding specifications.
            Default: Cladding()
        upper_end_fitting : GraphiteElement.EndFitting
            Upper End Fitting specifications.
            Default: EndFitting(length=TRIGA.FuelElement().upper_end_fitting.length, direction='up')
            (Ref. [1]_ Section 4.2.3.b)
        graphite_meat : GraphiteElement.GraphiteMeat
            Graphite Meat specifications.
            Default: GraphiteMeat()
        lower_end_fitting : GraphiteElement.EndFitting
            Lower End Fitting specifications.
            Default: EndFitting(length=TRIGA.FuelElement().lower_end_fitting.length, direction='down')
            (Ref. [1]_ Section 4.2.3.b)
        """

        @dataclass
        class GraphiteMeat:
            """Dataclass for Graphite Meat.

            Attributes
            ----------
            outer_radius : float
                Outer radius of the graphite meat [cm].
                Default: Same as default FuelElement.FuelMeat outer_radius (Ref. [1]_ Section 4.2.3.b)
            length : float
                Length of the graphite meat [cm].
                Default: Same as default FuelElement interior_length (Ref. [1]_ Section 4.2.3.b)
            material : openmc.Material
                Material of the graphite meat.
                Default: DefaultMaterials.graphite() (Ref. [2]_ pg. 50)
            """
            outer_radius: float = field(default_factory=lambda: TRIGA.FuelElement.FuelMeat().outer_radius)
            length:       float = field(default_factory=lambda: TRIGA.FuelElement().interior_length)
            material:     openmc.Material = field(default_factory=DefaultMaterials.graphite)

            def __post_init__(self):
                assert self.outer_radius > 0, "Graphite Meat outer radius must be positive."
                assert self.length > 0, "Graphite Meat length must be positive."

        @dataclass
        class Cladding:
            """Dataclass for Cladding.

            Attributes
            ----------
            thickness : float
                Thickness of the fuel cladding [cm].
                Default: Same as default FuelElement.Cladding thickness (Ref. [1]_ Section 4.2.3.b)
            outer_radius : float
                Outer radius of the fuel cladding [cm].
                Default: Same as default FuelElement.Cladding outer_radius (Ref. [1]_ Section 4.2.3.b)
            material : openmc.Material
                Material of the cladding.
                Default: DefaultMaterials.aluminum() (Ref. [2]_ pg. 50)
            """
            thickness:    float = field(default_factory=lambda: TRIGA.FuelElement.Cladding().thickness)
            outer_radius: float = field(default_factory=lambda: TRIGA.FuelElement.Cladding().outer_radius)
            material:     openmc.Material = field(default_factory=DefaultMaterials.aluminum)

            def __post_init__(self):
                assert self.thickness > 0, "Cladding thickness must be positive."
                assert self.outer_radius > 0, "Cladding outer radius must be positive."

        @dataclass
        class EndFitting:
            """Dataclass for End Fittings.

            When constructing neutronics models, the end fittings will
            be approximated as a cone with the given length (i.e. distance from base to apex)

            Attributes
            ----------
            length : float
                Length of the end fitting [cm].
            direction : Literal['up', 'down']
                Direction of the end fitting, either 'up' or 'down'.
            material : openmc.Material
                Material of the end fitting.
                Default: DefaultMaterials.aluminum() (Ref. [2]_ pg. 50)
            """
            length:    float
            direction: Literal['up', 'down']
            material:  openmc.Material = field(default_factory=DefaultMaterials.aluminum)

            def __post_init__(self):
                assert self.length > 0, "End Fitting length must be positive."
                assert self.direction in ('up', 'down'), "End Fitting direction must be either 'up' or 'down'."

        cladding:           Cladding          = field(default_factory=Cladding)
        upper_end_fitting:  EndFitting        = field(default_factory=lambda: TRIGA.GraphiteElement.EndFitting(
                                                          length    = TRIGA.FuelElement().upper_end_fitting.length,
                                                          direction = 'up'))
        graphite_meat:      GraphiteMeat      = field(default_factory=GraphiteMeat)
        lower_end_fitting:  EndFitting        = field(default_factory=lambda: TRIGA.GraphiteElement.EndFitting(
                                                          length    = TRIGA.FuelElement().lower_end_fitting.length,
                                                          direction = 'down'))


    @dataclass
    class TransientRod:
        """Dataclass for the TRIGA transient rod.

        Attributes
        ----------
        cladding : TransientRod.Cladding
            Transient rod cladding specifications.
            Default: Cladding()
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
        air_follower : TransientRod.AirFollower
            Air follower specifications.
            Default: AirFollower()
        lower_element_plug : TransientRod.ElementPlug
            Lower element plug specifications.
            Default: 0.5 inches (Ref. [2]_ pg. 58)
        position : int
            Rod positions (in steps) from 0 (fully inserted) to 960 (fully withdrawn)
            Default 0.
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
            length : float
                Length of the air gap [cm].
                Default: 19.75 inches (Ref. [2]_ pg. 58)
            material : openmc.Material
                Material of the air gap.
                Default: DefaultMaterials.air() (Ref. [2]_ pg. 51)
            """

            thickness: float = 19.75 * CM_PER_INCH
            material:  openmc.Material = field(default_factory=DefaultMaterials.air)

            def __post_init__(self):
                assert self.thickness > 0, "Air Gap thickness must be positive."

        cladding:                Cladding         = field(default_factory=Cladding)
        upper_element_plug:      ElementPlug      = field(default_factory=ElementPlug)
        upper_magneform_fitting: MagneformFitting = field(default_factory=MagneformFitting)
        absorber:                Absorber         = field(default_factory=Absorber)
        lower_magneform_fitting: MagneformFitting = field(default_factory=MagneformFitting)
        air_follower:            AirGap           = field(default_factory=AirGap)
        lower_element_plug:      ElementPlug      = field(default_factory=ElementPlug)
        position:                int              = 0

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
        position : int
            Rod positions (in steps) from 0 (fully inserted) to 960 (fully withdrawn)
            Default 0.
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
        position:                    int              = 0


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
        """

        inner_radius: float = 1.33 * 0.5 * CM_PER_INCH
        outer_radius: float = 1.5  * 0.5 * CM_PER_INCH
        material: openmc.Material = field(default_factory=DefaultMaterials.aluminum)

        def __post_init__(self):
            assert self.inner_radius > 0, "Central Thimble inner radius must be positive."
            assert self.outer_radius > self.inner_radius, "Central Thimble outer radius must be larger than inner radius."

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


    @dataclass
    class Shroud:
        """Dataclass for the TRIGA shroud.

        Attributes
        ----------
        thickness : float
            Thickness of the shroud [cm].
            Default: 3/16 inches (Ref. [2]_ pg. 54 & 55)
        height : float
            Height of the shroud [cm].
            Default: 23.13 inches (Ref. [2]_ pg. 55)
        large_hex_inradius : float
            Inradius of the the shroud large hexagon [cm].
            Default: 10.75 inches (Ref. [2]_ pg. 54)
        small_hex_inradius : float
            Inradius of the the shroud small hexagon [cm].
            Default: 10.21875 inches (Ref. [2]_ pg. 55)
        material : openmc.Material
            Material of the shroud.
            Default: DefaultMaterials.aluminum() (Ref. [2]_ pg. 48)
        """

        thickness:          float = 0.1875 * CM_PER_INCH
        height:             float = 23.13 * CM_PER_INCH
        large_hex_inradius: float = 10.75 * CM_PER_INCH
        small_hex_inradius: float = 10.21875 * CM_PER_INCH
        material:           openmc.Material = field(default_factory=DefaultMaterials.aluminum)

        def __post_init__(self):
            assert self.thickness > 0, "Shroud thickness must be positive."
            assert self.height > 0, "Shroud height must be positive."
            assert self.large_hex_inradius > 0, "Shroud large hex inradius must be positive."
            assert self.small_hex_inradius > 0, "Shroud small hex inradius must be positive."
            assert self.large_hex_inradius > self.small_hex_inradius, \
                "Shroud large hex inradius must be larger than small hex inradius."


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
        """

        radius:                 float = 42.0 * 0.5 * CM_PER_INCH
        height:                 float = 23.13 * CM_PER_INCH
        core_centerline_offset: float = 0.565 * CM_PER_INCH
        material:               openmc.Material = field(default_factory=DefaultMaterials.graphite)

        def __post_init__(self):
            assert self.radius > 0, "Reflector radius must be positive."
            assert self.height > 0, "Reflector height must be positive."


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
        """
        radius: float = 90.0
        height: float = 160.0
        material: openmc.Material = field(default_factory=DefaultMaterials.water)

        def __post_init__(self):
            assert self.radius > 0, "Pool radius must be positive."
            assert self.height > 0, "Pool height must be positive."


    @dataclass
    class Core:
        """ Dataclass for the TRIGA core.

        Default core loading and control rod positions are arbitrarily set to
        524 steps (approximately half withdrawn).  The following core locations
        are reserved for non-fuel elements (Ref [1]_ Figure 4.4 & pg 4-9):
        - Transient Rod:   C-01
        - Regulating Rod:  C-07
        - Shim 1 Rod:      D-06
        - Shim 2 Rod:      D-14
        - Central Thimble: A-01

        Attributes
        ----------
        pitch : float
            Hexagonal lattice pitch [cm].
            Default:  1.714 * CM_PER_INCH (Ref. [2]_ pg 54)
        central_thimble : TRIGA.CentralThimble
            The TRIGA central thimble specifications.
            Default: TRIGA.CentralThimble()
        transient_rod : TRIGA.TransientRod
            The TRIGA transient rod specifications.
            Default: TRIGA.TransientRod(position = 524)
        regulating_rod : TRIGA.FuelFollowerControlRod
            The TRIGA regulating rod specifications.
            Default: TRIGA.FuelFollowerControlRod(position = 524)
        shim_1_rod : TRIGA.FuelFollowerControlRod
            The TRIGA shim 1 rod specifications.
            Default: TRIGA.FuelFollowerControlRod(position = 524)
        shim_2_rod : TRIGA.FuelFollowerControlRod
            The TRIGA shim 2 rod specifications.
            Default: TRIGA.FuelFollowerControlRod(position = 524)
        core_loading : Dict[str, Optional[TRIGA.Core.Loadable]]
            Map of mutable core locations and their contents.  Keys must be in RING_MAP and not in
            the locations reserved for the control rods or central thimble (i.e. 'A-01', 'C-01', 'C-07', 'D-06', 'D-14').
            Keys in RING_MAP that are not specified in core_loading will take the value of the missing keys
            in the dictionary generated by TRIGA.Core.default_loading.
        core_map : Dict[str, Optional[TRIGA.Core.Element]]
            Map of core locations and their contents.  Keys are all locations in RING_MAP.

        RING_MAP : ClassVar[List[List[str]]]
            List of lists representing the TRIGA core ring map. Each inner list represents a ring in the core.  Rings are
            ordered from outermost ring (first list) to innermost ring (last list). Ref. [1]_ Figure 1.2
        """

        RING_MAP: ClassVar[List[List[str]]] = [
            ["G-01", "G-02", "G-03", "G-04", "G-05", "G-06",
             "G-07", "G-08", "G-09", "G-10", "G-11", "G-12",
             "G-13", "G-14", "G-15", "G-16", "G-17", "G-18",
             "G-19", "G-20", "G-21", "G-22", "G-23", "G-24",
             "G-25", "G-26", "G-27", "G-28", "G-29", "G-30",
             "G-31", "G-32", "G-33", "G-34", "G-35", "G-36"],
            ["F-01", "F-02", "F-03", "F-04", "F-05", "F-06",
             "F-07", "F-08", "F-09", "F-10", "F-11", "F-12",
             "F-13", "F-14", "F-15", "F-16", "F-17", "F-18",
             "F-19", "F-20", "F-21", "F-22", "F-23", "F-24",
             "F-25", "F-26", "F-27", "F-28", "F-29", "F-30"],
            ["E-01", "E-02", "E-03", "E-04", "E-05", "E-06",
             "E-07", "E-08", "E-09", "E-10", "E-11", "E-12",
             "E-13", "E-14", "E-15", "E-16", "E-17", "E-18",
             "E-19", "E-20", "E-21", "E-22", "E-23", "E-24"],
            ["D-01", "D-02", "D-03", "D-04", "D-05", "D-06",
             "D-07", "D-08", "D-09", "D-10", "D-11", "D-12",
             "D-13", "D-14", "D-15", "D-16", "D-17", "D-18"],
            ["C-01", "C-02", "C-03", "C-04", "C-05", "C-06",
             "C-07", "C-08", "C-09", "C-10", "C-11", "C-12"],
            ["B-01", "B-02", "B-03", "B-04", "B-05", "B-06"],
            ["A-01"]]

        Loadable: TypeAlias = "TRIGA.FuelElement | TRIGA.GraphiteElement | TRIGA.SourceHolder"
        Fixture:  TypeAlias = "TRIGA.CentralThimble | TRIGA.TransientRod | TRIGA.FuelFollowerControlRod"
        Element:  TypeAlias = "TRIGA.FuelElement | TRIGA.GraphiteElement | TRIGA.SourceHolder | +" \
                              "TRIGA.CentralThimble | TRIGA.TransientRod | TRIGA.FuelFollowerControlRod"

        pitch:           float                         = 1.714 * CM_PER_INCH
        central_thimble: TRIGA.CentralThimble          = field(default_factory=lambda: TRIGA.CentralThimble)
        core_loading:    Dict[str, Optional[Loadable]] = field(default_factory=lambda: TRIGA.Core.default_loading())  # pylint: disable=unnecessary-lambda
        transient_rod:   TRIGA.TransientRod            = field(default_factory=lambda:
                                                               TRIGA.TransientRod(position=524))
        regulating_rod:  TRIGA.FuelFollowerControlRod  = field(default_factory=lambda:
                                                               TRIGA.FuelFollowerControlRod(position=524))
        shim_1_rod:      TRIGA.FuelFollowerControlRod  = field(default_factory=lambda:
                                                               TRIGA.FuelFollowerControlRod(position=524))
        shim_2_rod:      TRIGA.FuelFollowerControlRod  = field(default_factory=lambda:
                                                               TRIGA.FuelFollowerControlRod(position=524))

        def __post_init__(self):
            for location in self.core_loading:
                assert any(location in ring for ring in TRIGA.Core.RING_MAP), \
                    f"Invalid core location '{location}' in core_loading."
                assert location not in ["A-01", "C-01", "C-07", "D-06", "D-14"], \
                    f"Core location '{location}' is reserved for control rods or central thimble."

            core_map: Dict[str, Optional[TRIGA.Core.Element]] = {
                "A-01": self.central_thimble,
                "C-01": self.transient_rod,
                "C-07": self.regulating_rod,
                "D-06": self.shim_1_rod,
                "D-14": self.shim_2_rod}

            default_loading = TRIGA.Core.default_loading()
            for ring in TRIGA.Core.RING_MAP:
                for location in ring:
                    core_map[location] = self.core_loading.get(location, default_loading.get(location, None))

        @classmethod
        def default_loading(cls) -> Dict[str, Optional[Loadable]]:
            """Generates an arbitrary default core loading map.

            This is similar though not entirely identical to the
            loading map presented in Ref. [2]_ pg. 48-49

            Returns
            -------
            Dict[str, Optional[TRIGA.Core.Loadable]]
                A copy of the default core loading map.
            """
            return  {
                "B-01": TRIGA.FuelElement(), "B-02": TRIGA.FuelElement(), "B-03": TRIGA.FuelElement(),
                "B-04": TRIGA.FuelElement(), "B-05": TRIGA.FuelElement(), "B-06": TRIGA.FuelElement(),
                                             "C-02": TRIGA.FuelElement(), "C-03": TRIGA.FuelElement(),
                "C-04": TRIGA.FuelElement(), "C-05": TRIGA.FuelElement(), "C-06": TRIGA.FuelElement(),
                                             "C-08": TRIGA.FuelElement(), "C-09": TRIGA.FuelElement(),
                "C-10": TRIGA.FuelElement(), "C-11": TRIGA.FuelElement(), "C-12": TRIGA.FuelElement(),
                "D-01": TRIGA.FuelElement(), "D-02": TRIGA.FuelElement(), "D-03": TRIGA.FuelElement(),
                "D-04": TRIGA.FuelElement(), "D-05": TRIGA.FuelElement(),
                "D-07": TRIGA.FuelElement(), "D-08": TRIGA.FuelElement(), "D-09": TRIGA.FuelElement(),
                "D-10": TRIGA.FuelElement(), "D-11": TRIGA.FuelElement(), "D-12": TRIGA.FuelElement(),
                "D-13": TRIGA.FuelElement(),                              "D-15": TRIGA.FuelElement(),
                "D-16": TRIGA.FuelElement(), "D-17": TRIGA.FuelElement(), "D-18": TRIGA.FuelElement(),
                "E-01": TRIGA.FuelElement(), "E-02": TRIGA.FuelElement(), "E-03": TRIGA.FuelElement(),
                "E-04": TRIGA.FuelElement(), "E-05": TRIGA.FuelElement(), "E-06": TRIGA.FuelElement(),
                "E-07": TRIGA.FuelElement(), "E-08": TRIGA.FuelElement(), "E-09": TRIGA.FuelElement(),
                "E-10": TRIGA.FuelElement(), "E-11": None,                "E-12": TRIGA.FuelElement(),
                "E-13": TRIGA.FuelElement(), "E-14": TRIGA.FuelElement(), "E-15": TRIGA.FuelElement(),
                "E-16": TRIGA.FuelElement(), "E-17": TRIGA.FuelElement(), "E-18": TRIGA.FuelElement(),
                "E-19": TRIGA.FuelElement(), "E-20": TRIGA.FuelElement(), "E-21": TRIGA.FuelElement(),
                "E-22": TRIGA.FuelElement(), "E-23": TRIGA.FuelElement(), "E-24": TRIGA.FuelElement(),
                "F-01": TRIGA.FuelElement(), "F-02": TRIGA.FuelElement(), "F-03": TRIGA.FuelElement(),
                "F-04": TRIGA.FuelElement(), "F-05": TRIGA.FuelElement(), "F-06": TRIGA.FuelElement(),
                "F-07": TRIGA.FuelElement(), "F-08": TRIGA.FuelElement(), "F-09": TRIGA.FuelElement(),
                "F-10": TRIGA.FuelElement(), "F-11": TRIGA.FuelElement(), "F-12": TRIGA.FuelElement(),
                "F-13": None,                "F-14": None,                "F-15": TRIGA.FuelElement(),
                "F-16": TRIGA.FuelElement(), "F-17": TRIGA.FuelElement(), "F-18": TRIGA.FuelElement(),
                "F-19": TRIGA.FuelElement(), "F-20": TRIGA.FuelElement(), "F-21": TRIGA.FuelElement(),
                "F-22": TRIGA.FuelElement(), "F-23": TRIGA.FuelElement(), "F-24": TRIGA.FuelElement(),
                "F-25": TRIGA.FuelElement(), "F-26": TRIGA.FuelElement(), "F-27": TRIGA.FuelElement(),
                "F-28": TRIGA.FuelElement(), "F-29": TRIGA.FuelElement(), "F-30": TRIGA.FuelElement(),
                "G-01": None,                "G-02": TRIGA.FuelElement(), "G-03": TRIGA.FuelElement(),
                "G-04": TRIGA.FuelElement(), "G-05": TRIGA.FuelElement(), "G-06": TRIGA.FuelElement(),
                "G-07": None,                "G-08": TRIGA.FuelElement(), "G-09": TRIGA.FuelElement(),
                "G-10": TRIGA.FuelElement(), "G-11": TRIGA.FuelElement(), "G-12": TRIGA.FuelElement(),
                "G-13": None,                "G-14": TRIGA.FuelElement(), "G-15": TRIGA.FuelElement(),
                "G-16": TRIGA.FuelElement(), "G-17": TRIGA.FuelElement(), "G-18": TRIGA.FuelElement(),
                "G-19": None,                "G-20": TRIGA.FuelElement(), "G-21": TRIGA.FuelElement(),
                "G-22": TRIGA.FuelElement(), "G-23": TRIGA.FuelElement(), "G-24": TRIGA.FuelElement(),
                "G-25": None,                "G-26": TRIGA.FuelElement(), "G-27": TRIGA.FuelElement(),
                "G-28": TRIGA.FuelElement(), "G-29": TRIGA.FuelElement(), "G-30": TRIGA.FuelElement(),
                "G-31": None,                "G-32": TRIGA.SourceHolder(),"G-33": TRIGA.FuelElement(),
                "G-34": None,                "G-35": TRIGA.FuelElement(), "G-36": TRIGA.FuelElement()}

    pool :                        TRIGA.Pool              = field(default_factory=Pool)
    reflector_canister :          TRIGA.ReflectorCanister = field(default_factory=ReflectorCanister)
    shroud :                      TRIGA.Shroud            = field(default_factory=Shroud)
    beam_port_1_5 :               TRIGA.BeamPort          = field(default_factory=lambda: TRIGA.default_beamport_1_5()) # pylint: disable=unnecessary-lambda
    beam_port_2 :                 TRIGA.BeamPort          = field(default_factory=lambda: TRIGA.default_beamport_2())   # pylint: disable=unnecessary-lambda
    beam_port_3 :                 TRIGA.BeamPort          = field(default_factory=lambda: TRIGA.default_beamport_3())   # pylint: disable=unnecessary-lambda
    beam_port_4 :                 TRIGA.BeamPort          = field(default_factory=lambda: TRIGA.default_beamport_4())   # pylint: disable=unnecessary-lambda
    rotary_specimen_rack_cavity : TRIGA.RSRCavity         = field(default_factory=RSRCavity)
    core:                         TRIGA.Core              = field(default_factory=Core)
    upper_grid_plate :            TRIGA.GridPlate         = field(default_factory=partial(GridPlate,
                                                                thickness                      = 0.62 * CM_PER_INCH,
                                                                fuel_penetration_radius        = 1.505 * 0.5 * CM_PER_INCH,
                                                                control_rod_penetration_radius = 1.505 * CM_PER_INCH,
                                                                distance_from_core_centerline  = 12.75 * CM_PER_INCH))
    lower_grid_plate :            TRIGA.GridPlate         = field(default_factory=partial(GridPlate,
                                                                thickness                      = 1.25 * CM_PER_INCH,
                                                                fuel_penetration_radius        = 1.25 * 0.5 * CM_PER_INCH,
                                                                control_rod_penetration_radius = 1.505 * CM_PER_INCH,
                                                                distance_from_core_centerline  = 13.06 * CM_PER_INCH))


    @classmethod
    def default_beamport_1_5(cls) -> BeamPort:
        """Default beam port 1/5 specifications.

        Returns
        -------
        BeamPort
            Beam port 1/5 specifications from Ref. [2]_ pages 48, 56, 59
        """
        return cls.BeamPort(translation = (35.2425, 0.0, -6.985),
                            rotation    = [[ 90.0, 180.0, 90.0],
                                           [  0.0,  90.0, 90.0],
                                           [ 90.0,  90.0,  0.0]])

    @classmethod
    def default_beamport_2(cls) -> BeamPort:
        """Default beam port 2 specifications.

        Returns
        -------
        BeamPort
            Beam port 2 specifications from Ref. [2]_ pages 48, 56, 59
        """
        return cls.BeamPort(translation       = (6.222, 35.255, -6.985),
                            rotation          = [[150.0,  60.0, 90.0],
                                                 [120.0, 150.0, 90.0],
                                                 [ 90.0,  90.0,  0.0]],
                            termination_plane = openmc.YPlane(y0=-12.621).rotate(
                            rotation          =[[cos(radians( 20.0)), cos(radians(125.0)), cos(radians(90.0))],
                                                [cos(radians(100.0)), cos(radians( 20.0)), cos(radians(90.0))],
                                                [cos(radians( 90.0)), cos(radians( 90.0)), cos(radians( 0.0))]]))

    @classmethod
    def default_beamport_3(cls) -> BeamPort:
        """Default beam port 3 specifications.

        Returns
        -------
        BeamPort
            Beam port 3 specifications from Ref. [2]_ pages 48, 56, 59
        """
        return cls.BeamPort(translation       = (0.0, 0.0, -6.985),
                            termination_plane = openmc.YPlane(y0 = 26.43188))

    @classmethod
    def default_beamport_4(cls) -> BeamPort:
        """Default beam port 4 specifications.

        Returns
        -------
        BeamPort
            Beam port 4 specifications from Ref. [2]_ pages 48, 56, 59
        """
        return cls.BeamPort(translation       = (-13.216, 22.871, -6.985),
                            rotation          = [[ 75.0, 60.0, 90.0],
                                                 [120.0, 75.0, 90.0],
                                                 [ 90.0, 90.0,  0.0]],
                            termination_plane = openmc.Plane(0.866025403784, 0.5, 0, -26.43188))
