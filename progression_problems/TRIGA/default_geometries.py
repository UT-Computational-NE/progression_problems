from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import openmc

from coreforge.geometry_elements.triga import (
    FuelElement as TRIGAFuelElement,
    GraphiteElement as TRIGAGraphiteElement,
)
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
        ``TRIGAFuelElement.FuelMeat`` axial-major order (top-to-bottom axial levels,
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
        cladding: TRIGAFuelElement.Cladding | None = None,
        fill_gas: Material | None = None,
        upper_end_fitting: TRIGAFuelElement.EndFitting | None = None,
        upper_air_gap: TRIGAFuelElement.AirGap | None = None,
        upper_graphite_reflector: TRIGAFuelElement.GraphiteReflector | None = None,
        zr_fill_rod: TRIGAFuelElement.ZrFillRod | None = None,
        fuel_meat: TRIGAFuelElement.FuelMeat | None = None,
        moly_disc: TRIGAFuelElement.MolyDisc | None = None,
        lower_graphite_reflector: TRIGAFuelElement.GraphiteReflector | None = None,
        lower_end_fitting: TRIGAFuelElement.EndFitting | None = None,
    ) -> TRIGAFuelElement:
        """Creates and returns the default fuel element geometry.

        Parameters
        ----------
        fuel_temp : float
            Temperature applied to default fuel and zirconium filler materials.
        non_fuel_temp : float
            Temperature applied to default non-fuel materials.
        coolant : Optional[openmc.Material]
            Coolant surrounding the cladding. If omitted, default water is used.
        fuel_spec : Optional[FuelSpec]
            Fuel material and region counts used when ``fuel_meat`` is omitted.
        cladding : Optional[TRIGAFuelElement.Cladding]
            Cladding override. If omitted, the default cladding is used.
        fill_gas : Optional[Material]
            Fill-gas override. If omitted, the default fill gas is used.
        upper_end_fitting : Optional[TRIGAFuelElement.EndFitting]
            Upper-end-fitting override. If omitted, the default fitting is used.
        upper_air_gap : Optional[TRIGAFuelElement.AirGap]
            Upper-air-gap override. If omitted, the default air gap is used.
        upper_graphite_reflector : Optional[TRIGAFuelElement.GraphiteReflector]
            Upper-reflector override. If omitted, the default reflector is used.
        zr_fill_rod : Optional[TRIGAFuelElement.ZrFillRod]
            Zirconium-fill-rod override. If omitted, the default rod is used.
        fuel_meat : Optional[TRIGAFuelElement.FuelMeat]
            Fuel-meat override. If supplied, ``fuel_spec`` is ignored.
        moly_disc : Optional[TRIGAFuelElement.MolyDisc]
            Molybdenum-disc override. If omitted, the default disc is used.
        lower_graphite_reflector : Optional[TRIGAFuelElement.GraphiteReflector]
            Lower-reflector override. If omitted, the default reflector is used.
        lower_end_fitting : Optional[TRIGAFuelElement.EndFitting]
            Lower-end-fitting override. If omitted, the default fitting is used.

        Returns
        -------
        TRIGAFuelElement
            Default CoreForge TRIGA fuel element.
        """
        coolant = coolant or DefaultMaterials.water()
        cladding = cladding if cladding is not None else DefaultGeometries.FuelElement.cladding(temperature=non_fuel_temp)
        fill_gas = fill_gas if fill_gas is not None else DefaultGeometries.FuelElement.fill_gas(temperature=non_fuel_temp)
        upper_end_fitting = (upper_end_fitting if upper_end_fitting is not None else
                             DefaultGeometries.FuelElement.upper_end_fitting(temperature=non_fuel_temp))
        upper_air_gap = (upper_air_gap if upper_air_gap is not None else
                         DefaultGeometries.FuelElement.upper_air_gap())
        upper_graphite_reflector = (upper_graphite_reflector if upper_graphite_reflector is not None else
                                    DefaultGeometries.FuelElement.upper_graphite_reflector(temperature=non_fuel_temp))
        zr_fill_rod = (zr_fill_rod if zr_fill_rod is not None else
                       DefaultGeometries.FuelElement.zr_fill_rod(temperature=fuel_temp))

        if fuel_meat is None:
            if fuel_spec is None:
                fuel_meat = DefaultGeometries.FuelElement.meat(temperature=fuel_temp)
            else:
                fuel_meat = DefaultGeometries.FuelElement.meat(
                    material=fuel_spec.material,
                    num_radial_regions=fuel_spec.num_radial_regions,
                    num_axial_regions=fuel_spec.num_axial_regions,
                )

        moly_disc = (moly_disc if moly_disc is not None else
                     DefaultGeometries.FuelElement.moly_disc(temperature=non_fuel_temp))
        lower_graphite_reflector = (lower_graphite_reflector if lower_graphite_reflector is not None else
                                    DefaultGeometries.FuelElement.lower_graphite_reflector(temperature=non_fuel_temp))
        lower_end_fitting = (lower_end_fitting if lower_end_fitting is not None else
                             DefaultGeometries.FuelElement.lower_end_fitting(temperature=non_fuel_temp))

        return TRIGAFuelElement(
            cladding=cladding,
            upper_end_fitting=upper_end_fitting,
            upper_air_gap=upper_air_gap,
            upper_graphite_reflector=upper_graphite_reflector,
            zr_fill_rod=zr_fill_rod,
            fuel_meat=fuel_meat,
            moly_disc=moly_disc,
            lower_graphite_reflector=lower_graphite_reflector,
            lower_end_fitting=lower_end_fitting,
            fill_gas=fill_gas,
            outer_material=Material(coolant),
            name="fuel_element",
        )


    @staticmethod
    def graphite_element(
        temperature: float = DefaultMaterials.DEFAULT_TEMPERATURE,
        coolant: openmc.Material | None = None,
        cladding: TRIGAGraphiteElement.Cladding | None = None,
        graphite_meat: TRIGAGraphiteElement.GraphiteMeat | None = None,
        upper_end_fitting: TRIGAGraphiteElement.EndFitting | None = None,
        lower_end_fitting: TRIGAGraphiteElement.EndFitting | None = None,
        fill_gas: Material | None = None,
    ) -> TRIGAGraphiteElement:
        """Creates and returns the default graphite element geometry.

        Parameters
        ----------
        temperature : float
            Temperature applied to default graphite-element materials.
        coolant : Optional[openmc.Material]
            Coolant surrounding the cladding. If omitted, default water is used.
        cladding : Optional[TRIGAGraphiteElement.Cladding]
            Cladding override. If omitted, the default cladding is used.
        graphite_meat : Optional[TRIGAGraphiteElement.GraphiteMeat]
            Graphite-meat override. If omitted, the default graphite meat is used.
        upper_end_fitting : Optional[TRIGAGraphiteElement.EndFitting]
            Upper-end-fitting override. If omitted, the default fitting is used.
        lower_end_fitting : Optional[TRIGAGraphiteElement.EndFitting]
            Lower-end-fitting override. If omitted, the default fitting is used.
        fill_gas : Optional[Material]
            Fill-gas override. If omitted, the default fill gas is used.

        Returns
        -------
        TRIGAGraphiteElement
            Default CoreForge TRIGA graphite element.
        """
        coolant = coolant or DefaultMaterials.water()
        cladding = (cladding if cladding is not None else
                    DefaultGeometries.GraphiteElement.cladding(temperature=temperature))
        graphite_meat = (graphite_meat if graphite_meat is not None else
                         DefaultGeometries.GraphiteElement.meat(temperature=temperature))
        upper_end_fitting = (upper_end_fitting if upper_end_fitting is not None else
                             DefaultGeometries.GraphiteElement.upper_end_fitting(temperature=temperature))
        lower_end_fitting = (lower_end_fitting if lower_end_fitting is not None else
                             DefaultGeometries.GraphiteElement.lower_end_fitting(temperature=temperature))
        fill_gas = (fill_gas if fill_gas is not None else
                    DefaultGeometries.GraphiteElement.fill_gas(temperature=temperature))

        return TRIGAGraphiteElement(
            cladding=cladding,
            graphite_meat=graphite_meat,
            upper_end_fitting=upper_end_fitting,
            lower_end_fitting=lower_end_fitting,
            fill_gas=fill_gas,
            outer_material=Material(coolant),
            name="graphite_element",
        )


    class FuelElement:
        """Namespace for default TRIGA fuel-element features and construction."""

        @staticmethod
        def cladding(
            thickness: float | None = None,
            outer_radius: float | None = None,
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> TRIGAFuelElement.Cladding:
            """Creates and returns the default fuel-element cladding.

            Parameters
            ----------
            thickness : Optional[float]
                Cladding thickness in cm. If omitted, the reference value is used.
            outer_radius : Optional[float]
                Cladding outer radius in cm. If omitted, the reference value is used.
            material : Optional[openmc.Material]
                Cladding material. If omitted, ``DefaultMaterials.stainless_steel`` is
                used at ``temperature``.
            temperature : Optional[float]
                Temperature in Kelvin used to construct the default material. If omitted,
                ``DefaultMaterials.DEFAULT_TEMPERATURE`` is used. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            TRIGAFuelElement.Cladding
                CoreForge fuel-element cladding.
            """
            thickness = thickness if thickness is not None else 0.020 * CM_PER_INCH  # Ref. [1]_ Table 4.1
            outer_radius = outer_radius if outer_radius is not None else 1.475 * 0.5 * CM_PER_INCH  # Ref. [1]_ Table 4.1
            temperature = temperature if temperature is not None else DefaultMaterials.DEFAULT_TEMPERATURE
            material = material if material is not None else DefaultMaterials.stainless_steel(temperature)  # Ref. [2]_ pg. 51

            return TRIGAFuelElement.Cladding(thickness, outer_radius, Material(material))

        @staticmethod
        def fill_gas(
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> Material:
            """Creates and returns the default fuel-element fill gas.

            Parameters
            ----------
            material : Optional[openmc.Material]
                Fill-gas material. If omitted, ``DefaultMaterials.air`` is used.
            temperature : Optional[float]
                Temperature in Kelvin used to construct the default material. If omitted,
                ``DefaultMaterials.DEFAULT_TEMPERATURE`` is used. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            Material
                CoreForge fill-gas material.
            """
            temperature = temperature if temperature is not None else DefaultMaterials.DEFAULT_TEMPERATURE
            material = material if material is not None else DefaultMaterials.air(temperature)  # Ref. [2]_ pg. 50
            return Material(material)

        @staticmethod
        def upper_end_fitting(
            length: float | None = None,
            r2: float | None = None,
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> TRIGAFuelElement.EndFitting:
            """Creates and returns the default upper fuel-element end fitting.

            Parameters
            ----------
            length : Optional[float]
                End-fitting length in cm. If omitted, the reference value is used.
            r2 : Optional[float]
                Square of the cone slope. If omitted, the reference value is used.
            material : Optional[openmc.Material]
                End-fitting material. If omitted, ``DefaultMaterials.stainless_steel``
                is used at ``temperature``.
            temperature : Optional[float]
                Temperature in Kelvin used to construct the default material. If omitted,
                ``DefaultMaterials.DEFAULT_TEMPERATURE`` is used. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            TRIGAFuelElement.EndFitting
                CoreForge upper fuel-element end fitting.
            """
            length = length if length is not None else 7.3552  # Ref. [2]_ pg. 55 (cone approx.)
            r2 = r2 if r2 is not None else 0.25  # Ref. [2]_ pg. 55 (slope^2)
            temperature = temperature if temperature is not None else DefaultMaterials.DEFAULT_TEMPERATURE
            material = material if material is not None else DefaultMaterials.stainless_steel(temperature)  # Ref. [2]_ pg. 51

            return TRIGAFuelElement.EndFitting(length, r2, "up", Material(material))

        @staticmethod
        def upper_air_gap(thickness: float | None = None) -> TRIGAFuelElement.AirGap:
            """Creates and returns the default upper fuel-element air gap.

            Parameters
            ----------
            thickness : Optional[float]
                Air-gap thickness in cm. If omitted, the reference value is used.

            Returns
            -------
            TRIGAFuelElement.AirGap
                CoreForge upper fuel-element air gap.
            """
            thickness = thickness if thickness is not None else 0.5 * CM_PER_INCH  # Ref. [1]_ pg. 4-3
            return TRIGAFuelElement.AirGap(thickness)

        @staticmethod
        def upper_graphite_reflector(
            radius: float | None = None,
            thickness: float | None = None,
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> TRIGAFuelElement.GraphiteReflector:
            """Creates and returns the default upper fuel-element graphite reflector.

            Parameters
            ----------
            radius : Optional[float]
                Reflector radius in cm. If omitted, the reference value is used.
            thickness : Optional[float]
                Axial reflector thickness in cm. If omitted, the reference value is used.
            material : Optional[openmc.Material]
                Reflector material. If omitted, ``DefaultMaterials.graphite`` is used at
                ``temperature``.
            temperature : Optional[float]
                Temperature in Kelvin used to construct the default material. If omitted,
                ``DefaultMaterials.DEFAULT_TEMPERATURE`` is used. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            TRIGAFuelElement.GraphiteReflector
                CoreForge upper fuel-element graphite reflector.
            """
            radius = radius if radius is not None else 1.430 * 0.5 * CM_PER_INCH  # Ref. [1]_ pg. 4-4
            thickness = thickness if thickness is not None else 2.56 * CM_PER_INCH  # Ref. [2]_ pg. 55
            temperature = temperature if temperature is not None else DefaultMaterials.DEFAULT_TEMPERATURE
            material = material if material is not None else DefaultMaterials.graphite(temperature)  # Ref. [2]_ pg. 50

            return TRIGAFuelElement.GraphiteReflector(radius, thickness, Material(material))

        @staticmethod
        def zr_fill_rod(
            radius: float | None = None,
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> TRIGAFuelElement.ZrFillRod:
            """Creates and returns the default fuel-element zirconium fill rod.

            Parameters
            ----------
            radius : Optional[float]
                Fill-rod radius in cm. If omitted, the reference value is used.
            material : Optional[openmc.Material]
                Fill-rod material. If omitted, ``DefaultMaterials.zirc_filler`` is used at
                ``temperature``.
            temperature : Optional[float]
                Temperature in Kelvin used to construct the default material. If omitted,
                ``DefaultMaterials.DEFAULT_TEMPERATURE`` is used. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            TRIGAFuelElement.ZrFillRod
                CoreForge fuel-element zirconium fill rod.
            """
            radius = radius if radius is not None else 0.25 * 0.5 * CM_PER_INCH  # Ref. [2]_ pg. 55
            temperature = temperature if temperature is not None else DefaultMaterials.DEFAULT_TEMPERATURE
            material = material if material is not None else DefaultMaterials.zirc_filler(temperature)  # Ref. [2]_ pg. 51

            return TRIGAFuelElement.ZrFillRod(radius, Material(material))

        @staticmethod
        def meat(
            inner_radius: float | None = None,
            outer_radius: float | None = None,
            length: float | None = None,
            material: openmc.Material | Sequence[openmc.Material] | None = None,
            num_radial_regions: int | None = None,
            num_axial_regions: int | None = None,
            temperature: float | None = None,
        ) -> TRIGAFuelElement.FuelMeat:
            """Creates and returns the default fuel meat.

            Parameters
            ----------
            inner_radius : Optional[float]
                Fuel-meat inner radius in cm. If omitted, the reference value is used.
            outer_radius : Optional[float]
                Fuel-meat outer radius in cm. If omitted, the reference value is used.
            length : Optional[float]
                Fuel-meat axial length in cm. If omitted, the reference value is used.
            material : Optional[openmc.Material | Sequence[openmc.Material]]
                Fuel material or one material per region in axial-major order. If omitted,
                ``DefaultMaterials.fresh_fuel`` is used at ``temperature``.
            num_radial_regions : Optional[int]
                Number of equal-volume radial regions. If omitted, one region is used.
            num_axial_regions : Optional[int]
                Number of equal-length axial regions. If omitted, one region is used.
            temperature : Optional[float]
                Temperature in Kelvin used to construct the default material. If omitted,
                ``DefaultMaterials.DEFAULT_TEMPERATURE`` is used. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            TRIGAFuelElement.FuelMeat
                CoreForge fuel meat.
            """
            inner_radius = inner_radius if inner_radius is not None else 0.25 * 0.5 * CM_PER_INCH  # Ref. [1]_ pg. 4-2
            outer_radius = outer_radius if outer_radius is not None else 1.435 * 0.5 * CM_PER_INCH  # Ref. [1]_ Table 4.1
            length = length if length is not None else 15.0 * CM_PER_INCH  # Ref. [1]_ Table 4.1
            num_radial_regions = num_radial_regions if num_radial_regions is not None else 1
            num_axial_regions = num_axial_regions if num_axial_regions is not None else 1
            temperature = temperature if temperature is not None else DefaultMaterials.DEFAULT_TEMPERATURE
            material = material if material is not None else DefaultMaterials.fresh_fuel(temperature)  # Ref. [2]_ pg. 51

            if isinstance(material, openmc.Material):
                fuel_material = Material(material)
            else:
                fuel_material = [Material(region_material) for region_material in material]

            return TRIGAFuelElement.FuelMeat(
                inner_radius,
                outer_radius,
                length,
                fuel_material,
                num_radial_regions,
                num_axial_regions,
            )

        @staticmethod
        def moly_disc(
            radius: float | None = None,
            thickness: float | None = None,
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> TRIGAFuelElement.MolyDisc:
            """Creates and returns the default fuel-element molybdenum disc.

            Parameters
            ----------
            radius : Optional[float]
                Disc radius in cm. If omitted, the reference value is used.
            thickness : Optional[float]
                Disc thickness in cm. If omitted, the reference value is used.
            material : Optional[openmc.Material]
                Disc material. If omitted, ``DefaultMaterials.molybdenum`` is used at
                ``temperature``.
            temperature : Optional[float]
                Temperature in Kelvin used to construct the default material. If omitted,
                ``DefaultMaterials.DEFAULT_TEMPERATURE`` is used. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            TRIGAFuelElement.MolyDisc
                CoreForge fuel-element molybdenum disc.
            """
            radius = radius if radius is not None else 1.431 * 0.5 * CM_PER_INCH  # Ref. [1]_ pg. 4-3
            thickness = thickness if thickness is not None else 0.031 * CM_PER_INCH  # Ref. [1]_ pg. 4-3
            temperature = temperature if temperature is not None else DefaultMaterials.DEFAULT_TEMPERATURE
            material = material if material is not None else DefaultMaterials.molybdenum(temperature)  # Ref. [2]_ pg. 51

            return TRIGAFuelElement.MolyDisc(radius, thickness, Material(material))

        @staticmethod
        def lower_graphite_reflector(
            radius: float | None = None,
            thickness: float | None = None,
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> TRIGAFuelElement.GraphiteReflector:
            """Creates and returns the default lower fuel-element graphite reflector.

            Parameters
            ----------
            radius : Optional[float]
                Reflector radius in cm. If omitted, the reference value is used.
            thickness : Optional[float]
                Axial reflector thickness in cm. If omitted, the reference value is used.
            material : Optional[openmc.Material]
                Reflector material. If omitted, ``DefaultMaterials.graphite`` is used at
                ``temperature``.
            temperature : Optional[float]
                Temperature in Kelvin used to construct the default material. If omitted,
                ``DefaultMaterials.DEFAULT_TEMPERATURE`` is used. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            TRIGAFuelElement.GraphiteReflector
                CoreForge lower fuel-element graphite reflector.
            """
            radius = radius if radius is not None else 1.430 * 0.5 * CM_PER_INCH  # Ref. [1]_ pg. 4-4
            thickness = thickness if thickness is not None else 3.72 * CM_PER_INCH  # Ref. [2]_ pg. 55
            temperature = temperature if temperature is not None else DefaultMaterials.DEFAULT_TEMPERATURE
            material = material if material is not None else DefaultMaterials.graphite(temperature)  # Ref. [2]_ pg. 50

            return TRIGAFuelElement.GraphiteReflector(radius, thickness, Material(material))

        @staticmethod
        def lower_end_fitting(
            length: float | None = None,
            r2: float | None = None,
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> TRIGAFuelElement.EndFitting:
            """Creates and returns the default lower fuel-element end fitting.

            Parameters
            ----------
            length : Optional[float]
                End-fitting length in cm. If omitted, the reference value is used.
            r2 : Optional[float]
                Square of the cone slope. If omitted, the reference value is used.
            material : Optional[openmc.Material]
                End-fitting material. If omitted, ``DefaultMaterials.stainless_steel``
                is used at ``temperature``.
            temperature : Optional[float]
                Temperature in Kelvin used to construct the default material. If omitted,
                ``DefaultMaterials.DEFAULT_TEMPERATURE`` is used. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            TRIGAFuelElement.EndFitting
                CoreForge lower fuel-element end fitting.
            """
            length = length if length is not None else 7.6209  # Ref. [2]_ pg. 55-56 (cone approx.)
            r2 = r2 if r2 is not None else 0.25  # Ref. [2]_ pg. 55 (slope^2)
            temperature = temperature if temperature is not None else DefaultMaterials.DEFAULT_TEMPERATURE
            material = material if material is not None else DefaultMaterials.stainless_steel(temperature)  # Ref. [2]_ pg. 51

            return TRIGAFuelElement.EndFitting(length, r2, "down", Material(material))



    class GraphiteElement:
        """Namespace for default TRIGA graphite-element features."""

        @staticmethod
        def cladding(
            thickness: float | None = None,
            outer_radius: float | None = None,
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> TRIGAGraphiteElement.Cladding:
            """Creates and returns the default graphite-element cladding.

            Parameters
            ----------
            thickness : Optional[float]
                Cladding thickness in cm. If omitted, the default fuel-element
                cladding thickness is used.
            outer_radius : Optional[float]
                Cladding outer radius in cm. If omitted, the default fuel-element
                cladding radius is used.
            material : Optional[openmc.Material]
                Cladding material. If omitted, ``DefaultMaterials.aluminum`` is used
                at ``temperature``.
            temperature : Optional[float]
                Temperature in Kelvin used to construct the default material. If omitted,
                ``DefaultMaterials.DEFAULT_TEMPERATURE`` is used. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            TRIGAGraphiteElement.Cladding
                CoreForge graphite-element cladding.
            """
            if thickness is None or outer_radius is None:
                fuel_cladding = DefaultGeometries.FuelElement.cladding()
                thickness = thickness if thickness is not None else fuel_cladding.thickness  # Ref. [1]_ Section 4.2.3.b
                outer_radius = (outer_radius if outer_radius is not None else
                                fuel_cladding.outer_radius)  # Ref. [1]_ Section 4.2.3.b
            temperature = temperature if temperature is not None else DefaultMaterials.DEFAULT_TEMPERATURE
            material = material if material is not None else DefaultMaterials.aluminum(temperature)  # Ref. [2]_ pg. 50

            return TRIGAGraphiteElement.Cladding(thickness, outer_radius, Material(material))

        @staticmethod
        def meat(
            outer_radius: float | None = None,
            length: float | None = None,
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> TRIGAGraphiteElement.GraphiteMeat:
            """Creates and returns the default graphite meat.

            Parameters
            ----------
            outer_radius : Optional[float]
                Graphite-meat outer radius in cm. If omitted, the default fuel-meat
                outer radius is used.
            length : Optional[float]
                Graphite-meat axial length in cm. If omitted, the default fuel-element
                interior length is used.
            material : Optional[openmc.Material]
                Graphite material. If omitted, ``DefaultMaterials.graphite`` is used
                at ``temperature``.
            temperature : Optional[float]
                Temperature in Kelvin used to construct the default material. If omitted,
                ``DefaultMaterials.DEFAULT_TEMPERATURE`` is used. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            TRIGAGraphiteElement.GraphiteMeat
                CoreForge graphite meat.
            """
            if outer_radius is None or length is None:
                fuel_element = DefaultGeometries.fuel_element()
                outer_radius = (outer_radius if outer_radius is not None else
                                fuel_element.fuel_meat.outer_radius) # Ref. [1]_ Section 4.2.3.b
                length = length if length is not None else fuel_element.interior_length # Ref. [1]_ Section 4.2.3.b

            temperature = temperature if temperature is not None else DefaultMaterials.DEFAULT_TEMPERATURE
            material = material if material is not None else DefaultMaterials.graphite(temperature)  # Ref. [2]_ pg. 50

            return TRIGAGraphiteElement.GraphiteMeat(outer_radius, length, Material(material))

        @staticmethod
        def upper_end_fitting(
            length: float | None = None,
            r2: float | None = None,
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> TRIGAGraphiteElement.EndFitting:
            """Creates and returns the default upper graphite-element end fitting.

            Parameters
            ----------
            length : Optional[float]
                End-fitting length in cm. If omitted, the default upper fuel-element
                fitting length is used.
            r2 : Optional[float]
                Square of the cone slope. If omitted, the reference value is used.
            material : Optional[openmc.Material]
                End-fitting material. If omitted, ``DefaultMaterials.aluminum`` is used
                at ``temperature``.
            temperature : Optional[float]
                Temperature in Kelvin used to construct the default material. If omitted,
                ``DefaultMaterials.DEFAULT_TEMPERATURE`` is used. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            TRIGAGraphiteElement.EndFitting
                CoreForge upper graphite-element end fitting.
            """
            if length is None:
                length = DefaultGeometries.FuelElement.upper_end_fitting().length  # Ref. [1]_ Section 4.2.3.b
            r2 = r2 if r2 is not None else 0.25  # Ref. [2]_ pg. 55 (slope^2)
            temperature = temperature if temperature is not None else DefaultMaterials.DEFAULT_TEMPERATURE
            material = material if material is not None else DefaultMaterials.aluminum(temperature)  # Ref. [2]_ pg. 50

            return TRIGAGraphiteElement.EndFitting(length, r2, "up", Material(material))

        @staticmethod
        def lower_end_fitting(
            length: float | None = None,
            r2: float | None = None,
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> TRIGAGraphiteElement.EndFitting:
            """Creates and returns the default lower graphite-element end fitting.

            Parameters
            ----------
            length : Optional[float]
                End-fitting length in cm. If omitted, the default lower fuel-element
                fitting length is used.
            r2 : Optional[float]
                Square of the cone slope. If omitted, the reference value is used.
            material : Optional[openmc.Material]
                End-fitting material. If omitted, ``DefaultMaterials.aluminum`` is used
                at ``temperature``.
            temperature : Optional[float]
                Temperature in Kelvin used to construct the default material. If omitted,
                ``DefaultMaterials.DEFAULT_TEMPERATURE`` is used. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            TRIGAGraphiteElement.EndFitting
                CoreForge lower graphite-element end fitting.
            """
            if length is None:
                length = DefaultGeometries.FuelElement.lower_end_fitting().length  # Ref. [1]_ Section 4.2.3.b
            r2 = r2 if r2 is not None else 0.25  # Ref. [2]_ pg. 55 (slope^2)
            temperature = temperature if temperature is not None else DefaultMaterials.DEFAULT_TEMPERATURE
            material = material if material is not None else DefaultMaterials.aluminum(temperature)  # Ref. [2]_ pg. 50

            return TRIGAGraphiteElement.EndFitting(length, r2, "down", Material(material))

        @staticmethod
        def fill_gas(
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> Material:
            """Creates and returns the default graphite-element fill gas.

            Parameters
            ----------
            material : Optional[openmc.Material]
                Fill-gas material. If omitted, ``DefaultMaterials.air`` is used.
            temperature : Optional[float]
                Temperature in Kelvin used to construct the default material. If omitted,
                ``DefaultMaterials.DEFAULT_TEMPERATURE`` is used. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            Material
                CoreForge fill-gas material.
            """
            temperature = temperature if temperature is not None else DefaultMaterials.DEFAULT_TEMPERATURE
            material = material if material is not None else DefaultMaterials.air(temperature)
            return Material(material)
