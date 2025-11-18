from __future__ import annotations
from dataclasses import dataclass, field
from functools import partial
from typing import Literal

import openmc

from progression_problems.constants import CM_PER_INCH
from progression_problems.TRIGA.default_materials import DefaultMaterials


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
        Default thickness: 2.56 inches (Ref. [2]_ pg. 55)
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
        Default thickness: 3.72 inches (Ref. [2]_ pg. 55)
    lower_end_fitting : FuelElement.EndFitting
        Lower End Fitting specifications.
        Default length: 7.6209 cm (Ref. [2]_ pg. 55-56)
        This is a value that when approximating the shape of the lower end fitting as
        a cone gives a reasonable approximation.
    interior_length : float
        Interior length of the fuel element [cm]. This is the length from the bottom of the
        lower graphite reflector to the top of the upper air gap.

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
            Default: DefaultMaterials.zirc_filler() (Ref. [1]_ pg. 51)
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
