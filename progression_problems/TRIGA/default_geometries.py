from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import openmc

from coreforge.geometry_elements.triga import FuelElement, GraphiteElement
from coreforge.materials import Material
from progression_problems.TRIGA.default_materials import DefaultMaterials
from progression_problems.constants import CM_PER_INCH


@dataclass
class FuelSpec:
    """Fuel-meat specification for a fuel element: material(s) and region counts.

    Attributes
    ----------
    material : openmc.Material | Sequence[openmc.Material]
        Fuel material(s) for the fuel meat. A single material is copied across all
        regions; a sequence assigns one material per region in
        ``FuelElement.FuelMeat`` axial-major order (top-to-bottom axial levels,
        inner-to-outer radial within each level) and must have length
        ``num_axial_regions * num_radial_regions``. Materials are used as-is
        (their own name/temperature); give each distinct composition a unique name.
    num_radial_regions : int
        Number of equal-volume radial fuel regions (default 1).
    num_axial_regions : int
        Number of equal-length axial fuel regions (default 1).
    """

    material: openmc.Material | Sequence[openmc.Material]
    num_radial_regions: int = 1
    num_axial_regions: int = 1


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
    def fuel_element(
        fuel_temp: float = DefaultMaterials.DEFAULT_TEMPERATURE,
        non_fuel_temp: float = DefaultMaterials.DEFAULT_TEMPERATURE,
        coolant: openmc.Material | None = None,
        fuel_spec: FuelSpec | None = None,
    ) -> FuelElement:
        """Creates and returns the default fuel element geometry.

        Parameters
        ----------
        fuel_temp : float
            Temperature applied to the fuel meat and zirconium filler rod materials.
        non_fuel_temp : float
            Temperature applied to the non-fuel materials in the element.
        coolant : Optional[openmc.Material]
            Coolant material used as the outer material. If omitted, DefaultMaterials.water is used.
        fuel_spec : Optional[FuelSpec]
            Fuel-meat specification (material(s) plus radial/axial region counts). If
            omitted, a single-region ``DefaultMaterials.fresh_fuel(fuel_temp)`` is used.
            Supplied materials are used as-is -- including their own ``name`` and
            ``temperature`` (``fuel_temp`` is NOT applied to them; it still drives the Zr
            fill rod). This allows distinct fuel definitions per core location and optional
            multi-region fuel meat. Give each distinct fuel composition a unique ``name`` so
            that CoreForge does not merge or reject them.

        Returns
        -------
        FuelElement
            Default CoreForge fuel element.
        """
        coolant = coolant or DefaultMaterials.water()
        fuel_spec = fuel_spec or FuelSpec(material=DefaultMaterials.fresh_fuel(fuel_temp))
        if isinstance(fuel_spec.material, openmc.Material):
            fuel_meat_material = Material(fuel_spec.material)
        else:
            fuel_meat_material = [Material(material) for material in fuel_spec.material]

        cladding = FuelElement.Cladding(
            thickness    = 0.020 * CM_PER_INCH,                                      # Ref. [1]_ Table 4.1
            outer_radius = 1.475 * 0.5 * CM_PER_INCH,                                # Ref. [1]_ Table 4.1
            material     = Material(DefaultMaterials.stainless_steel(non_fuel_temp)) # Ref. [2]_ pg. 51
        )

        fill_gas = Material(DefaultMaterials.air(non_fuel_temp))                     # Ref. [2]_ pg. 50

        upper_end_fitting = FuelElement.EndFitting(
            length    = 7.3552,                                                      # Ref. [2]_ pg. 55 (cone approx.)
            r2        = 0.25,                                                        # Ref. [2]_ pg. 55 (slope^2)
            direction = 'up',
            material  = Material(DefaultMaterials.stainless_steel(non_fuel_temp))    # Ref. [2]_ pg. 51
        )

        upper_air_gap = FuelElement.AirGap(
            thickness = 0.5 * CM_PER_INCH                                            # Ref. [1]_ pg. 4-3
        )

        upper_graphite_reflector = FuelElement.GraphiteReflector(
            radius    = 1.430 * 0.5 * CM_PER_INCH,                                   # Ref. [1]_ pg. 4-4
            thickness = 2.56 * CM_PER_INCH,                                          # Ref. [2]_ pg. 55
            material  = Material(DefaultMaterials.graphite(non_fuel_temp))           # Ref. [2]_ pg. 50
        )

        zr_fill_rod = FuelElement.ZrFillRod(
            radius   = 0.25 * 0.5 * CM_PER_INCH,                                     # Ref. [2]_ pg. 55
            material = Material(DefaultMaterials.zirc_filler(fuel_temp))             # Ref. [2]_ pg. 51
        )

        fuel_meat = FuelElement.FuelMeat(
            inner_radius=0.25 * 0.5 * CM_PER_INCH,  # Ref. [1]_ pg. 4-2
            outer_radius=1.435 * 0.5 * CM_PER_INCH,  # Ref. [1]_ Table 4.1
            length=15.0 * CM_PER_INCH,  # Ref. [1]_ Table 4.1
            material=fuel_meat_material,  # Ref. [2]_ pg. 51
            num_radial_regions=fuel_spec.num_radial_regions,
            num_axial_regions=fuel_spec.num_axial_regions,
        )

        moly_disc = FuelElement.MolyDisc(
            radius    = 1.431 * 0.5 * CM_PER_INCH,                                   # Ref. [1]_ pg. 4-3
            thickness = 0.031 * CM_PER_INCH,                                         # Ref. [1]_ pg. 4-3
            material  = Material(DefaultMaterials.molybdenum(non_fuel_temp))         # Ref. [2]_ pg. 51
        )

        lower_graphite_reflector = FuelElement.GraphiteReflector(
            radius    = 1.430 * 0.5 * CM_PER_INCH,                                   # Ref. [1]_ pg. 4-4
            thickness = 3.72 * CM_PER_INCH,                                          # Ref. [2]_ pg. 55
            material  = Material(DefaultMaterials.graphite(non_fuel_temp))           # Ref. [2]_ pg. 50
        )

        lower_end_fitting = FuelElement.EndFitting(
            length    = 7.6209,                                                      # Ref. [2]_ pg. 55-56 (cone approx.)
            r2        = 0.25,                                                        # Ref. [2]_ pg. 55 (slope^2)
            direction = 'down',
            material  = Material(DefaultMaterials.stainless_steel(non_fuel_temp))    # Ref. [2]_ pg. 51
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
                           outer_material           = Material(coolant),
                           name                     = "fuel_element")


    @staticmethod
    def graphite_element(temperature: float = DefaultMaterials.DEFAULT_TEMPERATURE,
                         coolant:     openmc.Material | None = None) -> GraphiteElement:
        """Creates and returns the default graphite element geometry.

        Parameters
        ----------
        temperature : float
            Temperature applied to the graphite element materials.
        coolant : Optional[openmc.Material]
            Coolant material used as the outer material. If omitted, DefaultMaterials.water is used.

        Returns
        -------
        GraphiteElement
            Default CoreForge graphite element.
        """
        coolant = coolant or DefaultMaterials.water()
        fuel_element = DefaultGeometries.fuel_element(non_fuel_temp=temperature, coolant=coolant)

        cladding = GraphiteElement.Cladding(
            thickness    = fuel_element.cladding.thickness,                 # Ref. [1]_ Section 4.2.3.b
            outer_radius = fuel_element.cladding.outer_radius,              # Ref. [1]_ Section 4.2.3.b
            material     = Material(DefaultMaterials.aluminum(temperature)) # Ref. [2]_ pg. 50
        )

        graphite_meat = GraphiteElement.GraphiteMeat(
            outer_radius = fuel_element.fuel_meat.outer_radius,             # Ref. [1]_ Section 4.2.3.b
            length       = fuel_element.interior_length,                    # Ref. [1]_ Section 4.2.3.b
            material     = Material(DefaultMaterials.graphite(temperature)) # Ref. [2]_ pg. 50
        )

        upper_end_fitting = GraphiteElement.EndFitting(
            length    =  fuel_element.upper_end_fitting.length,             # Ref. [1]_ Section 4.2.3.b
            r2        =  0.25,                                              # Ref. [2]_ pg. 55 (slope^2)
            direction = 'up',
            material  = Material(DefaultMaterials.aluminum(temperature))    # Ref. [2]_ pg. 50
        )

        lower_end_fitting = GraphiteElement.EndFitting(
            length    =  fuel_element.lower_end_fitting.length,             # Ref. [1]_ Section 4.2.3.b
            r2        =  0.25,                                              # Ref. [2]_ pg. 55 (slope^2)
            direction = 'down',
            material  = Material(DefaultMaterials.aluminum(temperature))    # Ref. [2]_ pg. 50
        )

        return GraphiteElement(cladding          = cladding,
                               graphite_meat     = graphite_meat,
                               upper_end_fitting = upper_end_fitting,
                               lower_end_fitting = lower_end_fitting,
                               fill_gas          = Material(DefaultMaterials.air(temperature)),
                               outer_material    = Material(coolant),
                               name              = "graphite_element")
