from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal

import openmc

from progression_problems.TRIGA.default_materials import DefaultMaterials
from progression_problems.TRIGA.fuel_element import FuelElement


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

    References
    ----------
    .. [1] "University of Texas at Austin Nuclear Engineering Teaching Laboratory
           TRIGA Research Reactor", August 2023,
           https://www.nrc.gov/docs/ML2327/ML23279A146.pdf
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
        outer_radius: float = field(default_factory=lambda: FuelElement.FuelMeat().outer_radius)
        length:       float = field(default_factory=lambda: FuelElement().interior_length)
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
        thickness:    float = field(default_factory=lambda: FuelElement.Cladding().thickness)
        outer_radius: float = field(default_factory=lambda: FuelElement.Cladding().outer_radius)
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
    upper_end_fitting:  EndFitting        = field(default_factory=lambda: GraphiteElement.EndFitting(
                                                      length    = FuelElement().upper_end_fitting.length,
                                                      direction = 'up'))
    graphite_meat:      GraphiteMeat      = field(default_factory=GraphiteMeat)
    lower_end_fitting:  EndFitting        = field(default_factory=lambda: GraphiteElement.EndFitting(
                                                      length    = FuelElement().lower_end_fitting.length,
                                                      direction = 'down'))
