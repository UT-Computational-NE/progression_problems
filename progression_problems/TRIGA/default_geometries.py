from __future__ import annotations

from coreforge.geometry_elements.triga import FuelElement, GraphiteElement
from coreforge.materials import Material
from progression_problems.TRIGA.default_materials import DefaultMaterials
from progression_problems.constants import CM_PER_INCH

class DefaultGeometries:
    """ Dataclass containing default geometries for TRIGA reactor models

    References
    ----------
    .. [1] "University of Texas at Austin Nuclear Engineering Teaching Laboratory TRIGA
           Research Reactor", August 2023, https://www.nrc.gov/docs/ML2327/ML23279A146.pdf
    .. [2] D. R. Redhouse, et al., "Radiation Characterization Summary: NETL Beam Port
           1/5 Free-Field Environment at the 128-inch Core Centerline Adjacent Location,
           (NETL-FF-BP1/5-128-cca).", Nov. 2022. https://doi.org/10.2172/1898256
    """

    @staticmethod
    def fuel_element() -> FuelElement:
        """Creates and returns the default fuel element geometry.

        Returns
        -------
        FuelElement
            Default CoreForge fuel element.
        """
        cladding = FuelElement.Cladding(
            thickness    = 0.020 * CM_PER_INCH,                         # Ref. [1]_ Table 4.1
            outer_radius = 1.475 * 0.5 * CM_PER_INCH,                   # Ref. [1]_ Table 4.1
            material     = Material(DefaultMaterials.stainless_steel()) # Ref. [2]_ pg. 51
        )

        fill_gas = Material(DefaultMaterials.air())                     # Ref. [2]_ pg. 50

        upper_end_fitting = FuelElement.EndFitting(
            length    = 7.3552,                                         # Ref. [2]_ pg. 55 (cone approx.)
            direction = 'up',
            material  = Material(DefaultMaterials.stainless_steel())    # Ref. [2]_ pg. 51
        )

        upper_air_gap = FuelElement.AirGap(
            thickness = 0.5 * CM_PER_INCH                               # Ref. [1]_ pg. 4-3
        )

        upper_graphite_reflector = FuelElement.GraphiteReflector(
            radius    = 1.430 * 0.5 * CM_PER_INCH,                      # Ref. [1]_ pg. 4-4
            thickness = 2.56 * CM_PER_INCH,                             # Ref. [2]_ pg. 55
            material  = Material(DefaultMaterials.graphite())           # Ref. [2]_ pg. 50
        )

        zr_fill_rod = FuelElement.ZrFillRod(
            radius   = 0.25 * 0.5 * CM_PER_INCH,                        # Ref. [2]_ pg. 55
            material = Material(DefaultMaterials.zirc_filler())         # Ref. [2]_ pg. 51
        )

        fuel_meat = FuelElement.FuelMeat(
            inner_radius = 0.25  * 0.5 * CM_PER_INCH,                   # Ref. [1]_ pg. 4-2
            outer_radius = 1.435 * 0.5 * CM_PER_INCH,                   # Ref. [1]_ Table 4.1
            length       = 15.0 * CM_PER_INCH,                          # Ref. [1]_ Table 4.1
            material     = Material(DefaultMaterials.fresh_fuel())      # Ref. [2]_ pg. 51
        )

        moly_disc = FuelElement.MolyDisc(
            radius    = 1.431 * 0.5 * CM_PER_INCH,                      # Ref. [1]_ pg. 4-3
            thickness = 0.031 * CM_PER_INCH,                            # Ref. [1]_ pg. 4-3
            material  = Material(DefaultMaterials.molybdenum())         # Ref. [2]_ pg. 51
        )

        lower_graphite_reflector = FuelElement.GraphiteReflector(
            radius    = 1.430 * 0.5 * CM_PER_INCH,                      # Ref. [1]_ pg. 4-4
            thickness = 3.72 * CM_PER_INCH,                             # Ref. [2]_ pg. 55
            material  = Material(DefaultMaterials.graphite())           # Ref. [2]_ pg. 50
        )

        lower_end_fitting = FuelElement.EndFitting(
            length    = 7.6209,                                         # Ref. [2]_ pg. 55-56 (cone approx.)
            direction = 'down',
            material  = Material(DefaultMaterials.stainless_steel())    # Ref. [2]_ pg. 51
        )

        return FuelElement(cladding                 = cladding,
                           upper_end_fitting        = upper_end_fitting,
                           upper_air_gap            = upper_air_gap,
                           upper_graphite_reflector = upper_graphite_reflector,
                           zr_fill_rod              = zr_fill_rod,
                           fuel_meat                = fuel_meat,
                           moly_disc                = moly_disc,
                           lower_graphite_reflector = lower_graphite_reflector,
                           lower_end_fitting        = lower_end_fitting,
                           fill_gas                 = fill_gas,
                           name                     = "fuel_element")


    @staticmethod
    def graphite_element() -> GraphiteElement:
        """Creates and returns the default graphite element geometry.

        Returns
        -------
        GraphiteElement
            Default CoreForge graphite element.
        """
        fuel_element = DefaultGeometries.fuel_element()

        cladding = GraphiteElement.Cladding(
            thickness    = fuel_element.cladding.thickness,              # Ref. [1]_ Section 4.2.3.b
            outer_radius = fuel_element.cladding.outer_radius,           # Ref. [1]_ Section 4.2.3.b
            material     = Material(DefaultMaterials.aluminum()),        # Ref. [2]_ pg. 50
        )

        graphite_meat = GraphiteElement.GraphiteMeat(
            outer_radius = fuel_element.fuel_meat.outer_radius,          # Ref. [1]_ Section 4.2.3.b
            length       = fuel_element.interior_length,                 # Ref. [1]_ Section 4.2.3.b
            material     = Material(DefaultMaterials.graphite()),        # Ref. [2]_ pg. 50
        )

        upper_end_fitting = GraphiteElement.EndFitting(
            length    =  fuel_element.upper_end_fitting.length,          # Ref. [1]_ Section 4.2.3.b
            direction = 'up',
            material  = Material(DefaultMaterials.aluminum()),           # Ref. [2]_ pg. 50
        )

        lower_end_fitting = GraphiteElement.EndFitting(
            length    =  fuel_element.lower_end_fitting.length,          # Ref. [1]_ Section 4.2.3.b
            direction = 'down',
            material  = Material(DefaultMaterials.aluminum()),           # Ref. [2]_ pg. 50
        )

        return GraphiteElement(cladding          = cladding,
                               graphite_meat     = graphite_meat,
                               upper_end_fitting = upper_end_fitting,
                               lower_end_fitting = lower_end_fitting,
                               name              = "graphite_element")
