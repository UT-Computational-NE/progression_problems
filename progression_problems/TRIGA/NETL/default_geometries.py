from __future__ import annotations
from math import cos, radians, sin
from typing import Sequence

import openmc

from coreforge.geometry_elements.triga import FuelElement, GraphiteElement
from coreforge.geometry_elements.triga.netl import (CentralThimble, SourceHolder as NETLSourceHolder,
                                                    FuelFollowerControlRod as NETLFuelFollowerControlRod,
                                                    TransientRod as NETLTransientRod, GridPlate, BeamPort, Pool,
                                                    RSRCavity as NETLRSRCavity,
                                                    Reflector, Shroud, Core, Reactor)
from coreforge.geometry_elements.triga.netl.grid_plate import grid_plate_penetration_map
from coreforge.materials import Material
from progression_problems.TRIGA.default_geometries import DefaultGeometries as TRIGADefaultGeometries
from progression_problems.TRIGA.default_geometries import FuelSpec
from progression_problems.TRIGA.default_materials import DefaultMaterials as TRIGADefaultMaterials
from progression_problems.TRIGA.NETL.default_materials import DefaultMaterials as NETLDefaultMaterials
from progression_problems.constants import CM_PER_INCH

def sind(degrees: float) -> float:
    return sin(radians(degrees))


def cosd(degrees: float) -> float:
    return cos(radians(degrees))

class DefaultGeometries:
    """ Dataclass containing default geometries for NETL reactor models

    References
    ----------
    .. [1] "University of Texas at Austin Nuclear Engineering Teaching Laboratory TRIGA
           Research Reactor", August 2023, https://www.nrc.gov/docs/ML2327/ML23279A146.pdf
    .. [2] D. R. Redhouse, et al., "Radiation Characterization Summary: NETL Beam Port
           1/5 Free-Field Environment at the 128-inch Core Centerline Adjacent Location,
           (NETL-FF-BP1/5-128-cca).", Nov. 2022. https://doi.org/10.2172/1898256
    """

    UPPER_GRID_PLATE_TOP_TO_CORE_CENTERLINE_DISTANCE = 12.75  * CM_PER_INCH  # Ref. [2]_ pg. 55
    LOWER_GRID_PLATE_TOP_TO_CORE_CENTERLINE_DISTANCE = 13.06 * CM_PER_INCH   # Ref. [2]_ pg. 55
    TRANSIENT_ROD_FULLY_INSERTED_POSITION            = -73.0250              # Ref. [2]_ pg. 58
    FFCR_FULLY_INSERTED_POSITION                     = -76.5180              # Ref. [2]_ pg. 58
    TRANSIENT_ROD_MAX_WITHDRAWAL_DISTANCE            = 15.0  * CM_PER_INCH   # Ref. [1]_ pg. 4-10
    FFCR_MAX_WITHDRAWAL_DISTANCE                     = 15.0  * CM_PER_INCH   # Ref. [1]_ pg. 4-10
    TRANSIENT_ROD_FULLY_WITHDRAWN_POSITION           = TRANSIENT_ROD_FULLY_INSERTED_POSITION + \
                                                       TRANSIENT_ROD_MAX_WITHDRAWAL_DISTANCE
    FFCR_FULLY_WITHDRAWN_POSITION                    = FFCR_FULLY_INSERTED_POSITION + \
                                                       FFCR_MAX_WITHDRAWAL_DISTANCE

    @staticmethod
    def central_thimble(
        temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        coolant: openmc.Material | None = None,
        thickness: float | None = None,
        outer_radius: float | None = None,
        material: openmc.Material | None = None,
        length: float | None = None,
    ) -> CentralThimble:
        """Creates and returns the default central thimble.

        Parameters
        ----------
        temperature : float
            Temperature applied to the default central-thimble material.
        coolant : Optional[openmc.Material]
            Coolant material used for both the fill and outer materials. If omitted,
            water is used.
        thickness : Optional[float]
            Cladding thickness in cm. If omitted, the reference value is used.
        outer_radius : Optional[float]
            Cladding outer radius in cm. If omitted, the reference value is used.
        material : Optional[openmc.Material]
            Cladding material. If omitted, ``NETLDefaultMaterials.aluminum`` is used
            at ``temperature``. The temperature is ignored when a material is supplied.
        length : Optional[float]
            Central-thimble length in cm. If omitted, the default pool height is used.

        Returns
        -------
        CentralThimble
            Default NETL TRIGA central thimble.
        """
        coolant = coolant or NETLDefaultMaterials.water()
        thickness = (thickness if thickness is not None else
                     (1.5 * 0.5 * CM_PER_INCH) - (1.33 * 0.5 * CM_PER_INCH))  # Ref. [1]_ Section 10.2.1.b
        outer_radius = (outer_radius if outer_radius is not None else
                        1.5 * 0.5 * CM_PER_INCH)  # Ref. [1]_ Section 10.2.1.b
        material = (material if material is not None else
                    NETLDefaultMaterials.aluminum(temperature))  # Ref. [2]_ pg. 51
        length = length if length is not None else DefaultGeometries.pool().height

        cladding = CentralThimble.Cladding(
            thickness=thickness,
            outer_radius=outer_radius,
            material=Material(material),
        )

        coolant_material = Material(coolant)

        return CentralThimble(
            cladding       = cladding,
            length         = length,
            fill_material  = coolant_material,
            outer_material = coolant_material,
            name           = "central_thimble",
        )

    @staticmethod
    def source_holder(
        temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        coolant: openmc.Material | None = None,
        length: float | None = None,
        cavity: NETLSourceHolder.Cavity | None = None,
        cladding: NETLSourceHolder.Cladding | None = None,
    ) -> NETLSourceHolder:
        """Creates and returns the default source holder.

        Parameters
        ----------
        temperature : float
            Temperature applied to default source-holder materials.
        coolant : Optional[openmc.Material]
            Coolant material used as the outer material. If omitted, water is used.
        length : Optional[float]
            Source-holder length in cm. If omitted, the reference value is used.
        cavity : Optional[NETLSourceHolder.Cavity]
            Cavity override. If omitted, ``DefaultGeometries.SourceHolder.cavity`` is used.
        cladding : Optional[NETLSourceHolder.Cladding]
            Cladding override. If omitted, ``DefaultGeometries.SourceHolder.cladding`` is used.

        Returns
        -------
        NETLSourceHolder
            Default NETL TRIGA source holder.
        """
        coolant = coolant or NETLDefaultMaterials.water()

        upper_grid_top  = DefaultGeometries.UPPER_GRID_PLATE_TOP_TO_CORE_CENTERLINE_DISTANCE
        lower_grid_top  = DefaultGeometries.LOWER_GRID_PLATE_TOP_TO_CORE_CENTERLINE_DISTANCE
        length = (length if length is not None else
                  upper_grid_top + lower_grid_top - DefaultGeometries.SourceHolder.DISTANCE_FROM_LOWER_GRID_PLATE)
        cavity = (cavity if cavity is not None else
                  DefaultGeometries.SourceHolder.cavity(temperature=temperature))
        cladding = (cladding if cladding is not None else
                    DefaultGeometries.SourceHolder.cladding(temperature=temperature))

        return NETLSourceHolder(
            length         = length,
            cavity         = cavity,
            cladding       = cladding,
            outer_material = Material(coolant),
            gap_tolerance  = None,
            name           = "source_holder",
        )

    class SourceHolder:
        """Namespace for default NETL source-holder features."""

        DISTANCE_FROM_LOWER_GRID_PLATE = 1.1934  # Ref. [2]_ pg. 55

        @staticmethod
        def cavity(
            radius: float | None = None,
            length: float | None = None,
            axial_offset: float | None = None,
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> NETLSourceHolder.Cavity:
            """Creates and returns the default source-holder cavity.

            Parameters
            ----------
            radius : Optional[float]
                Cavity radius in cm. If omitted, the reference value is used.
            length : Optional[float]
                Cavity length in cm. If omitted, the reference value is used.
            axial_offset : Optional[float]
                Offset of the cavity center from the holder center in cm. If omitted,
                the cavity center is placed at the reactor core centerline.
            material : Optional[openmc.Material]
                Cavity material. If omitted, ``NETLDefaultMaterials.air`` is used at
                ``temperature``.
            temperature : Optional[float]
                Temperature in Kelvin used to construct the default material. If omitted,
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE`` is used. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            NETLSourceHolder.Cavity
                CoreForge NETL source-holder cavity.
            """
            radius = radius if radius is not None else 0.981 * 0.5 * CM_PER_INCH  # Ref. [1]_ Section 4.2.5
            length = length if length is not None else 3.0 * CM_PER_INCH  # Ref. [1]_ Section 4.2.5
            axial_offset = (axial_offset if axial_offset is not None else
                            -DefaultGeometries.SourceHolder.DISTANCE_FROM_LOWER_GRID_PLATE)  # Ref. [2]_ pg. 55
            temperature = temperature if temperature is not None else NETLDefaultMaterials.DEFAULT_TEMPERATURE
            material = material if material is not None else NETLDefaultMaterials.air(temperature)  # Ref. [2]_ pg. 54

            return NETLSourceHolder.Cavity(radius, length, axial_offset, Material(material))

        @staticmethod
        def cladding(
            outer_radius: float | None = None,
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> NETLSourceHolder.Cladding:
            """Creates and returns the default source-holder cladding.

            Parameters
            ----------
            outer_radius : Optional[float]
                Cladding outer radius in cm. If omitted, the reference value is used.
            material : Optional[openmc.Material]
                Cladding material. If omitted, ``NETLDefaultMaterials.aluminum`` is used
                at ``temperature``.
            temperature : Optional[float]
                Temperature in Kelvin used to construct the default material. If omitted,
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE`` is used. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            NETLSourceHolder.Cladding
                CoreForge NETL source-holder cladding.
            """
            outer_radius = outer_radius if outer_radius is not None else 1.435 * 0.5 * CM_PER_INCH  # Ref. [2]_ pg. 54 & 55
            temperature = temperature if temperature is not None else NETLDefaultMaterials.DEFAULT_TEMPERATURE
            material = material if material is not None else NETLDefaultMaterials.aluminum(temperature)  # Ref. [2]_ pg. 54

            return NETLSourceHolder.Cladding(outer_radius, Material(material))

    @staticmethod
    def fuel_follower_control_rod(
        fuel_temp: float = TRIGADefaultMaterials.DEFAULT_TEMPERATURE,
        non_fuel_temp: float = TRIGADefaultMaterials.DEFAULT_TEMPERATURE,
        coolant: openmc.Material | None = None,
        cladding: NETLFuelFollowerControlRod.Cladding | None = None,
        absorber: NETLFuelFollowerControlRod.Absorber | None = None,
        fuel_follower: NETLFuelFollowerControlRod.FuelFollower | None = None,
        zr_fill_rod: NETLFuelFollowerControlRod.ZrFillRod | None = None,
        upper_element_plug: NETLFuelFollowerControlRod.ElementPlug | None = None,
        upper_air_gap: NETLFuelFollowerControlRod.AirGap | None = None,
        upper_magneform_fitting: NETLFuelFollowerControlRod.MagneformFitting | None = None,
        above_absorber_air_gap: NETLFuelFollowerControlRod.AirGap | None = None,
        middle_magneform_fitting: NETLFuelFollowerControlRod.MagneformFitting | None = None,
        above_fuel_follower_air_gap: NETLFuelFollowerControlRod.AirGap | None = None,
        lower_magneform_fitting: NETLFuelFollowerControlRod.MagneformFitting | None = None,
        lower_air_gap: NETLFuelFollowerControlRod.AirGap | None = None,
        lower_element_plug: NETLFuelFollowerControlRod.ElementPlug | None = None,
        fill_gas: Material | None = None,
    ) -> NETLFuelFollowerControlRod:
        """Creates and returns the default fuel follower control rod.

        Parameters
        ----------
        fuel_temp : float
            Temperature applied to default fuel-follower and zirconium materials.
        non_fuel_temp : float
            Temperature applied to default non-fuel materials in the control rod.
        coolant : Optional[openmc.Material]
            Coolant material used as the outer material. If omitted, water is used.
        cladding : Optional[NETLFuelFollowerControlRod.Cladding]
            Cladding override. If omitted, the default cladding is used.
        absorber : Optional[NETLFuelFollowerControlRod.Absorber]
            Absorber override. If omitted, the default absorber is used.
        fuel_follower : Optional[NETLFuelFollowerControlRod.FuelFollower]
            Fuel-follower override. If omitted, the default fuel follower is used.
        zr_fill_rod : Optional[NETLFuelFollowerControlRod.ZrFillRod]
            Zirconium-fill-rod override. If omitted, the default rod is used.
        upper_element_plug : Optional[NETLFuelFollowerControlRod.ElementPlug]
            Upper-element-plug override. If omitted, the default plug is used.
        upper_air_gap : Optional[NETLFuelFollowerControlRod.AirGap]
            Upper-air-gap override. If omitted, the default gap is used.
        upper_magneform_fitting : Optional[NETLFuelFollowerControlRod.MagneformFitting]
            Upper-Magneform-fitting override. If omitted, the default fitting is used.
        above_absorber_air_gap : Optional[NETLFuelFollowerControlRod.AirGap]
            Above-absorber-air-gap override. If omitted, the default gap is used.
        middle_magneform_fitting : Optional[NETLFuelFollowerControlRod.MagneformFitting]
            Middle-Magneform-fitting override. If omitted, the default fitting is used.
        above_fuel_follower_air_gap : Optional[NETLFuelFollowerControlRod.AirGap]
            Above-fuel-follower-air-gap override. If omitted, the default gap is used.
        lower_magneform_fitting : Optional[NETLFuelFollowerControlRod.MagneformFitting]
            Lower-Magneform-fitting override. If omitted, the default fitting is used.
        lower_air_gap : Optional[NETLFuelFollowerControlRod.AirGap]
            Lower-air-gap override. If omitted, the default gap is used.
        lower_element_plug : Optional[NETLFuelFollowerControlRod.ElementPlug]
            Lower-element-plug override. If omitted, the default plug is used.
        fill_gas : Optional[Material]
            Fill-gas override. If omitted, the default fill gas is used.

        Returns
        -------
        NETLFuelFollowerControlRod
            Default NETL TRIGA fuel follower control rod.
        """
        coolant = coolant or NETLDefaultMaterials.water()
        cladding = (cladding if cladding is not None else
                    DefaultGeometries.FuelFollowerControlRod.cladding(temperature=non_fuel_temp))
        absorber = (absorber if absorber is not None else
                    DefaultGeometries.FuelFollowerControlRod.absorber(temperature=non_fuel_temp))
        fuel_follower = (fuel_follower if fuel_follower is not None else
                         DefaultGeometries.FuelFollowerControlRod.fuel_follower(
                             outer_radius=cladding.inner_radius,
                             temperature=fuel_temp,
                         ))
        zr_fill_rod = (zr_fill_rod if zr_fill_rod is not None else
                       DefaultGeometries.FuelFollowerControlRod.zr_fill_rod(temperature=fuel_temp))
        upper_element_plug = (upper_element_plug if upper_element_plug is not None else
                              DefaultGeometries.FuelFollowerControlRod.upper_element_plug(
                                  temperature=non_fuel_temp))
        upper_air_gap = (upper_air_gap if upper_air_gap is not None else
                         DefaultGeometries.FuelFollowerControlRod.upper_air_gap())
        upper_magneform_fitting = (upper_magneform_fitting if upper_magneform_fitting is not None else
                                   DefaultGeometries.FuelFollowerControlRod.upper_magneform_fitting(
                                       temperature=non_fuel_temp))
        above_absorber_air_gap = (above_absorber_air_gap if above_absorber_air_gap is not None else
                                  DefaultGeometries.FuelFollowerControlRod.above_absorber_air_gap())
        middle_magneform_fitting = (middle_magneform_fitting if middle_magneform_fitting is not None else
                                    DefaultGeometries.FuelFollowerControlRod.middle_magneform_fitting(
                                        temperature=non_fuel_temp))
        above_fuel_follower_air_gap = (
            above_fuel_follower_air_gap if above_fuel_follower_air_gap is not None else
            DefaultGeometries.FuelFollowerControlRod.above_fuel_follower_air_gap()
        )
        lower_magneform_fitting = (lower_magneform_fitting if lower_magneform_fitting is not None else
                                   DefaultGeometries.FuelFollowerControlRod.lower_magneform_fitting(
                                       temperature=non_fuel_temp))
        lower_air_gap = (lower_air_gap if lower_air_gap is not None else
                         DefaultGeometries.FuelFollowerControlRod.lower_air_gap())
        lower_element_plug = (lower_element_plug if lower_element_plug is not None else
                              DefaultGeometries.FuelFollowerControlRod.lower_element_plug(
                                  temperature=non_fuel_temp))
        fill_gas = (fill_gas if fill_gas is not None else
                    DefaultGeometries.FuelFollowerControlRod.fill_gas(temperature=non_fuel_temp))

        return NETLFuelFollowerControlRod(
            cladding=cladding,
            absorber=absorber,
            fuel_follower=fuel_follower,
            zr_fill_rod=zr_fill_rod,
            upper_element_plug=upper_element_plug,
            upper_air_gap=upper_air_gap,
            upper_magneform_fitting=upper_magneform_fitting,
            above_absorber_air_gap=above_absorber_air_gap,
            middle_magneform_fitting=middle_magneform_fitting,
            above_fuel_follower_air_gap=above_fuel_follower_air_gap,
            lower_magneform_fitting=lower_magneform_fitting,
            lower_air_gap=lower_air_gap,
            lower_element_plug=lower_element_plug,
            fill_gas=fill_gas,
            outer_material=Material(coolant),
            gap_tolerance=1e-8,
            name="fuel_follower_control_rod",
        )

    class FuelFollowerControlRod:
        """Namespace for default NETL fuel-follower-control-rod features."""

        @staticmethod
        def cladding(
            thickness: float | None = None,
            outer_radius: float | None = None,
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> NETLFuelFollowerControlRod.Cladding:
            """Creates and returns the default control-rod cladding.

            Parameters
            ----------
            thickness : Optional[float]
                Cladding thickness in cm. If omitted, the reference value is used.
            outer_radius : Optional[float]
                Cladding outer radius in cm. If omitted, the reference value is used.
            material : Optional[openmc.Material]
                Cladding material. If omitted, ``NETLDefaultMaterials.stainless_steel``
                is used at ``temperature``.
            temperature : Optional[float]
                Temperature in Kelvin used to construct the default material. If omitted,
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE`` is used. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            NETLFuelFollowerControlRod.Cladding
                CoreForge fuel-follower-control-rod cladding.
            """
            thickness = thickness if thickness is not None else 0.02 * CM_PER_INCH  # Ref. [2]_ pg. 55
            outer_radius = outer_radius if outer_radius is not None else 1.35 * 0.5 * CM_PER_INCH  # Ref. [2]_ pg. 55
            temperature = temperature if temperature is not None else NETLDefaultMaterials.DEFAULT_TEMPERATURE
            material = (material if material is not None else
                        NETLDefaultMaterials.stainless_steel(temperature))  # Ref. [2]_ pg. 52

            return NETLFuelFollowerControlRod.Cladding(thickness, outer_radius, Material(material))

        @staticmethod
        def absorber(
            radius: float | None = None,
            length: float | None = None,
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> NETLFuelFollowerControlRod.Absorber:
            """Creates and returns the default control-rod absorber.

            Parameters
            ----------
            radius : Optional[float]
                Absorber radius in cm. If omitted, the reference value is used.
            length : Optional[float]
                Absorber length in cm. If omitted, the reference value is used.
            material : Optional[openmc.Material]
                Absorber material. If omitted,
                ``NETLDefaultMaterials.control_rod_absorber`` is used at ``temperature``.
            temperature : Optional[float]
                Temperature in Kelvin used to construct the default material. If omitted,
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE`` is used. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            NETLFuelFollowerControlRod.Absorber
                CoreForge fuel-follower-control-rod absorber.
            """
            radius = radius if radius is not None else 1.3 * 0.5 * CM_PER_INCH  # Ref. [2]_ pg. 55
            length = length if length is not None else 15.0 * CM_PER_INCH  # Ref. [2]_ pg. 58
            temperature = temperature if temperature is not None else NETLDefaultMaterials.DEFAULT_TEMPERATURE
            material = (material if material is not None else
                        NETLDefaultMaterials.control_rod_absorber(temperature))  # Ref. [2]_ pg. 52

            return NETLFuelFollowerControlRod.Absorber(radius, length, Material(material))

        @staticmethod
        def fuel_follower(
            length: float | None = None,
            inner_radius: float | None = None,
            outer_radius: float | None = None,
            material: openmc.Material | Sequence[openmc.Material] | None = None,
            num_radial_regions: int | None = None,
            num_axial_regions: int | None = None,
            temperature: float | None = None,
        ) -> NETLFuelFollowerControlRod.FuelFollower:
            """Creates and returns the default fuel follower.

            Parameters
            ----------
            length : Optional[float]
                Fuel-follower length in cm. If omitted, the reference value is used.
            inner_radius : Optional[float]
                Fuel-follower inner radius in cm. If omitted, the reference value is used.
            outer_radius : Optional[float]
                Fuel-follower outer radius in cm. If omitted, the default cladding inner
                radius is used.
            material : Optional[openmc.Material | Sequence[openmc.Material]]
                Fuel material or one material per region in axial-major order. If omitted,
                ``NETLDefaultMaterials.fuel_follower_fuel`` is used at ``temperature``.
            num_radial_regions : Optional[int]
                Number of equal-volume radial regions. If omitted, one region is used.
            num_axial_regions : Optional[int]
                Number of equal-length axial regions. If omitted, one region is used.
            temperature : Optional[float]
                Temperature in Kelvin used to construct the default material. If omitted,
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE`` is used. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            NETLFuelFollowerControlRod.FuelFollower
                CoreForge control-rod fuel follower.
            """
            length = length if length is not None else 15.0 * CM_PER_INCH  # Ref. [2]_ pg. 58
            inner_radius = inner_radius if inner_radius is not None else 0.25 * 0.5 * CM_PER_INCH  # Ref. [2]_ pg. 55
            if outer_radius is None:
                outer_radius = DefaultGeometries.FuelFollowerControlRod.cladding().inner_radius
            num_radial_regions = num_radial_regions if num_radial_regions is not None else 1
            num_axial_regions = num_axial_regions if num_axial_regions is not None else 1
            temperature = temperature if temperature is not None else NETLDefaultMaterials.DEFAULT_TEMPERATURE
            material = (material if material is not None else
                        NETLDefaultMaterials.fuel_follower_fuel(temperature))  # Ref. [2]_ pg. 52

            if isinstance(material, openmc.Material):
                fuel_material = Material(material)
            else:
                fuel_material = [Material(region_material) for region_material in material]

            return NETLFuelFollowerControlRod.FuelFollower(
                length,
                inner_radius,
                outer_radius,
                fuel_material,
                num_radial_regions,
                num_axial_regions,
            )

        @staticmethod
        def zr_fill_rod(
            radius: float | None = None,
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> NETLFuelFollowerControlRod.ZrFillRod:
            """Creates and returns the default zirconium fill rod.

            Parameters
            ----------
            radius : Optional[float]
                Fill-rod radius in cm. If omitted, the reference value is used.
            material : Optional[openmc.Material]
                Fill-rod material. If omitted, ``NETLDefaultMaterials.zirc_filler`` is
                used at ``temperature``.
            temperature : Optional[float]
                Temperature in Kelvin used to construct the default material. If omitted,
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE`` is used. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            NETLFuelFollowerControlRod.ZrFillRod
                CoreForge control-rod zirconium fill rod.
            """
            radius = radius if radius is not None else 0.25 * 0.5 * CM_PER_INCH  # Ref. [2]_ pg. 55
            temperature = temperature if temperature is not None else NETLDefaultMaterials.DEFAULT_TEMPERATURE
            material = material if material is not None else NETLDefaultMaterials.zirc_filler(temperature)  # Ref. [2]_ pg. 52

            return NETLFuelFollowerControlRod.ZrFillRod(radius, Material(material))

        @staticmethod
        def upper_element_plug(
            thickness: float | None = None,
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> NETLFuelFollowerControlRod.ElementPlug:
            """Creates and returns the default upper element plug.

            Parameters
            ----------
            thickness : Optional[float]
                Plug thickness in cm. If omitted, the reference value is used.
            material : Optional[openmc.Material]
                Plug material. If omitted, ``NETLDefaultMaterials.stainless_steel`` is
                used at ``temperature``.
            temperature : Optional[float]
                Temperature used for the default material. Ignored when ``material``
                is supplied; if omitted, the default temperature is used.

            Returns
            -------
            NETLFuelFollowerControlRod.ElementPlug
                CoreForge upper element plug.
            """
            thickness = thickness if thickness is not None else 1.5 * CM_PER_INCH  # Ref. [2]_ pg. 58
            temperature = temperature if temperature is not None else NETLDefaultMaterials.DEFAULT_TEMPERATURE
            material = (material if material is not None else
                        NETLDefaultMaterials.stainless_steel(temperature))  # Ref. [2]_ pg. 51
            return NETLFuelFollowerControlRod.ElementPlug(thickness, Material(material))

        @staticmethod
        def upper_air_gap(thickness: float | None = None) -> NETLFuelFollowerControlRod.AirGap:
            """Creates and returns the default upper air gap.

            Parameters
            ----------
            thickness : Optional[float]
                Air-gap thickness in cm. If omitted, the reference value is used.

            Returns
            -------
            NETLFuelFollowerControlRod.AirGap
                CoreForge upper air gap.
            """
            thickness = thickness if thickness is not None else 3.5 * CM_PER_INCH  # Ref. [2]_ pg. 58
            return NETLFuelFollowerControlRod.AirGap(thickness)

        @staticmethod
        def upper_magneform_fitting(
            thickness: float | None = None,
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> NETLFuelFollowerControlRod.MagneformFitting:
            """Creates and returns the default upper Magneform fitting.

            Parameters
            ----------
            thickness : Optional[float]
                Fitting thickness in cm. If omitted, the reference value is used.
            material : Optional[openmc.Material]
                Fitting material. If omitted, ``NETLDefaultMaterials.stainless_steel``
                is used at ``temperature``.
            temperature : Optional[float]
                Temperature used for the default material. Ignored when ``material``
                is supplied; if omitted, the default temperature is used.

            Returns
            -------
            NETLFuelFollowerControlRod.MagneformFitting
                CoreForge upper Magneform fitting.
            """
            thickness = thickness if thickness is not None else 0.5 * CM_PER_INCH  # Ref. [2]_ pg. 58
            temperature = temperature if temperature is not None else NETLDefaultMaterials.DEFAULT_TEMPERATURE
            material = (material if material is not None else
                        NETLDefaultMaterials.stainless_steel(temperature))  # Ref. [2]_ pg. 51
            return NETLFuelFollowerControlRod.MagneformFitting(thickness, Material(material))

        @staticmethod
        def above_absorber_air_gap(thickness: float | None = None) -> NETLFuelFollowerControlRod.AirGap:
            """Creates and returns the default air gap above the absorber.

            Parameters
            ----------
            thickness : Optional[float]
                Air-gap thickness in cm. If omitted, the reference value is used.

            Returns
            -------
            NETLFuelFollowerControlRod.AirGap
                CoreForge air gap above the absorber.
            """
            thickness = thickness if thickness is not None else 0.125 * CM_PER_INCH  # Ref. [2]_ pg. 58
            return NETLFuelFollowerControlRod.AirGap(thickness)

        @staticmethod
        def middle_magneform_fitting(
            thickness: float | None = None,
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> NETLFuelFollowerControlRod.MagneformFitting:
            """Creates and returns the default middle Magneform fitting.

            Parameters
            ----------
            thickness : Optional[float]
                Fitting thickness in cm. If omitted, the reference value is used.
            material : Optional[openmc.Material]
                Fitting material. If omitted, ``NETLDefaultMaterials.stainless_steel``
                is used at ``temperature``.
            temperature : Optional[float]
                Temperature used for the default material. Ignored when ``material``
                is supplied; if omitted, the default temperature is used.

            Returns
            -------
            NETLFuelFollowerControlRod.MagneformFitting
                CoreForge middle Magneform fitting.
            """
            thickness = thickness if thickness is not None else 0.5 * CM_PER_INCH  # Ref. [2]_ pg. 58
            temperature = temperature if temperature is not None else NETLDefaultMaterials.DEFAULT_TEMPERATURE
            material = (material if material is not None else
                        NETLDefaultMaterials.stainless_steel(temperature))  # Ref. [2]_ pg. 51
            return NETLFuelFollowerControlRod.MagneformFitting(thickness, Material(material))

        @staticmethod
        def above_fuel_follower_air_gap(
            thickness: float | None = None,
        ) -> NETLFuelFollowerControlRod.AirGap:
            """Creates and returns the default air gap above the fuel follower.

            Parameters
            ----------
            thickness : Optional[float]
                Air-gap thickness in cm. If omitted, the reference value is used.

            Returns
            -------
            NETLFuelFollowerControlRod.AirGap
                CoreForge air gap above the fuel follower.
            """
            thickness = thickness if thickness is not None else 0.25 * CM_PER_INCH  # Ref. [2]_ pg. 58
            return NETLFuelFollowerControlRod.AirGap(thickness)

        @staticmethod
        def lower_magneform_fitting(
            thickness: float | None = None,
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> NETLFuelFollowerControlRod.MagneformFitting:
            """Creates and returns the default lower Magneform fitting.

            Parameters
            ----------
            thickness : Optional[float]
                Fitting thickness in cm. If omitted, the reference value is used.
            material : Optional[openmc.Material]
                Fitting material. If omitted, ``NETLDefaultMaterials.stainless_steel``
                is used at ``temperature``.
            temperature : Optional[float]
                Temperature used for the default material. Ignored when ``material``
                is supplied; if omitted, the default temperature is used.

            Returns
            -------
            NETLFuelFollowerControlRod.MagneformFitting
                CoreForge lower Magneform fitting.
            """
            thickness = thickness if thickness is not None else 1.0 * CM_PER_INCH  # Ref. [2]_ pg. 58
            temperature = temperature if temperature is not None else NETLDefaultMaterials.DEFAULT_TEMPERATURE
            material = (material if material is not None else
                        NETLDefaultMaterials.stainless_steel(temperature))  # Ref. [2]_ pg. 51
            return NETLFuelFollowerControlRod.MagneformFitting(thickness, Material(material))

        @staticmethod
        def lower_air_gap(thickness: float | None = None) -> NETLFuelFollowerControlRod.AirGap:
            """Creates and returns the default lower air gap.

            Parameters
            ----------
            thickness : Optional[float]
                Air-gap thickness in cm. If omitted, the reference value is used.

            Returns
            -------
            NETLFuelFollowerControlRod.AirGap
                CoreForge lower air gap.
            """
            thickness = thickness if thickness is not None else 5.375 * CM_PER_INCH  # Ref. [2]_ pg. 58
            return NETLFuelFollowerControlRod.AirGap(thickness)

        @staticmethod
        def lower_element_plug(
            thickness: float | None = None,
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> NETLFuelFollowerControlRod.ElementPlug:
            """Creates and returns the default lower element plug.

            Parameters
            ----------
            thickness : Optional[float]
                Plug thickness in cm. If omitted, the reference value is used.
            material : Optional[openmc.Material]
                Plug material. If omitted, ``NETLDefaultMaterials.stainless_steel`` is
                used at ``temperature``.
            temperature : Optional[float]
                Temperature used for the default material. Ignored when ``material``
                is supplied; if omitted, the default temperature is used.

            Returns
            -------
            NETLFuelFollowerControlRod.ElementPlug
                CoreForge lower element plug.
            """
            thickness = thickness if thickness is not None else 0.5 * CM_PER_INCH  # Ref. [2]_ pg. 58
            temperature = temperature if temperature is not None else NETLDefaultMaterials.DEFAULT_TEMPERATURE
            material = (material if material is not None else
                        NETLDefaultMaterials.stainless_steel(temperature))  # Ref. [2]_ pg. 51
            return NETLFuelFollowerControlRod.ElementPlug(thickness, Material(material))

        @staticmethod
        def fill_gas(
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> Material:
            """Creates and returns the default control-rod fill gas.

            Parameters
            ----------
            material : Optional[openmc.Material]
                Fill-gas material. If omitted, ``NETLDefaultMaterials.air`` is used.
            temperature : Optional[float]
                Temperature used for the default material. Ignored when ``material``
                is supplied; if omitted, the default temperature is used.

            Returns
            -------
            Material
                CoreForge fill-gas material.
            """
            temperature = temperature if temperature is not None else NETLDefaultMaterials.DEFAULT_TEMPERATURE
            material = material if material is not None else NETLDefaultMaterials.air(temperature)  # Ref. [2]_ pg. 51
            return Material(material)

    @staticmethod
    def transient_rod(
        temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        coolant: openmc.Material | None = None,
        cladding: NETLTransientRod.Cladding | None = None,
        absorber: NETLTransientRod.Absorber | None = None,
        upper_element_plug: NETLTransientRod.ElementPlug | None = None,
        upper_magneform_fitting: NETLTransientRod.MagneformFitting | None = None,
        lower_magneform_fitting: NETLTransientRod.MagneformFitting | None = None,
        air_follower: NETLTransientRod.AirFollower | None = None,
        lower_element_plug: NETLTransientRod.ElementPlug | None = None,
        fill_gas: Material | None = None,
    ) -> NETLTransientRod:
        """Creates and returns the default transient control rod.

        Parameters
        ----------
        temperature : float
            Temperature applied to default transient-rod materials.
        coolant : Optional[openmc.Material]
            Coolant material used as the outer material. If omitted, water is used.
        cladding : Optional[NETLTransientRod.Cladding]
            Cladding override. If omitted, the default cladding is used.
        absorber : Optional[NETLTransientRod.Absorber]
            Absorber override. If omitted, the default absorber is used.
        upper_element_plug : Optional[NETLTransientRod.ElementPlug]
            Upper-element-plug override. If omitted, the default plug is used.
        upper_magneform_fitting : Optional[NETLTransientRod.MagneformFitting]
            Upper-Magneform-fitting override. If omitted, the default fitting is used.
        lower_magneform_fitting : Optional[NETLTransientRod.MagneformFitting]
            Lower-Magneform-fitting override. If omitted, the default fitting is used.
        air_follower : Optional[NETLTransientRod.AirFollower]
            Air-follower override. If omitted, the default air follower is used.
        lower_element_plug : Optional[NETLTransientRod.ElementPlug]
            Lower-element-plug override. If omitted, the default plug is used.
        fill_gas : Optional[Material]
            Fill-gas override. If omitted, the default fill gas is used.

        Returns
        -------
        NETLTransientRod
            Default NETL TRIGA transient control rod.
        """
        coolant = coolant or NETLDefaultMaterials.water()
        cladding = (cladding if cladding is not None else
                    DefaultGeometries.TransientRod.cladding(temperature=temperature))
        absorber = (absorber if absorber is not None else
                    DefaultGeometries.TransientRod.absorber(temperature=temperature))
        upper_element_plug = (upper_element_plug if upper_element_plug is not None else
                              DefaultGeometries.TransientRod.upper_element_plug(temperature=temperature))
        upper_magneform_fitting = (upper_magneform_fitting if upper_magneform_fitting is not None else
                                   DefaultGeometries.TransientRod.upper_magneform_fitting(temperature=temperature))
        lower_magneform_fitting = (lower_magneform_fitting if lower_magneform_fitting is not None else
                                   DefaultGeometries.TransientRod.lower_magneform_fitting(temperature=temperature))
        air_follower = (air_follower if air_follower is not None else
                        DefaultGeometries.TransientRod.air_follower())
        lower_element_plug = (lower_element_plug if lower_element_plug is not None else
                              DefaultGeometries.TransientRod.lower_element_plug(temperature=temperature))
        fill_gas = (fill_gas if fill_gas is not None else
                    DefaultGeometries.TransientRod.fill_gas(temperature=temperature))

        return NETLTransientRod(
            cladding=cladding,
            absorber=absorber,
            fill_gas=fill_gas,
            outer_material=Material(coolant),
            air_follower=air_follower,
            upper_element_plug=upper_element_plug,
            upper_magneform_fitting=upper_magneform_fitting,
            lower_magneform_fitting=lower_magneform_fitting,
            lower_element_plug=lower_element_plug,
            gap_tolerance=None,
            name="transient_rod",
        )

    class TransientRod:
        """Namespace for default NETL transient-rod features."""

        @staticmethod
        def cladding(
            thickness: float | None = None,
            outer_radius: float | None = None,
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> NETLTransientRod.Cladding:
            """Creates and returns the default transient-rod cladding.

            Parameters
            ----------
            thickness : Optional[float]
                Cladding thickness in cm. If omitted, the reference value is used.
            outer_radius : Optional[float]
                Cladding outer radius in cm. If omitted, the reference value is used.
            material : Optional[openmc.Material]
                Cladding material. If omitted, ``NETLDefaultMaterials.aluminum`` is used
                at ``temperature``.
            temperature : Optional[float]
                Temperature in Kelvin used to construct the default material. If omitted,
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE`` is used. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            NETLTransientRod.Cladding
                CoreForge NETL transient-rod cladding.
            """
            thickness = thickness if thickness is not None else 0.028 * CM_PER_INCH  # Ref. [1]_ Table 4.2
            outer_radius = outer_radius if outer_radius is not None else 1.25 * 0.5 * CM_PER_INCH  # Ref. [1]_ Table 4.2
            temperature = temperature if temperature is not None else NETLDefaultMaterials.DEFAULT_TEMPERATURE
            material = material if material is not None else NETLDefaultMaterials.aluminum(temperature)  # Ref. [2]_ pg. 51

            return NETLTransientRod.Cladding(thickness, outer_radius, Material(material))

        @staticmethod
        def absorber(
            radius: float | None = None,
            length: float | None = None,
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> NETLTransientRod.Absorber:
            """Creates and returns the default transient-rod absorber.

            Parameters
            ----------
            radius : Optional[float]
                Absorber radius in cm. If omitted, the reference value is used.
            length : Optional[float]
                Absorber length in cm. If omitted, the reference value is used.
            material : Optional[openmc.Material]
                Absorber material. If omitted,
                ``NETLDefaultMaterials.control_rod_absorber`` is used at ``temperature``.
            temperature : Optional[float]
                Temperature in Kelvin used to construct the default material. If omitted,
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE`` is used. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            NETLTransientRod.Absorber
                CoreForge NETL transient-rod absorber.
            """
            radius = radius if radius is not None else 1.187 * 0.5 * CM_PER_INCH  # Ref. [2]_ pg. 55
            length = length if length is not None else 15.0 * CM_PER_INCH  # Ref. [1]_ Table 4.2
            temperature = temperature if temperature is not None else NETLDefaultMaterials.DEFAULT_TEMPERATURE
            material = (material if material is not None else
                        NETLDefaultMaterials.control_rod_absorber(temperature))  # Ref. [2]_ pg. 51

            return NETLTransientRod.Absorber(radius, length, Material(material))

        @staticmethod
        def air_follower(thickness: float | None = None) -> NETLTransientRod.AirFollower:
            """Creates and returns the default transient-rod air follower.

            Parameters
            ----------
            thickness : Optional[float]
                Air-follower thickness in cm. If omitted, the reference value is used.

            Returns
            -------
            NETLTransientRod.AirFollower
                CoreForge NETL transient-rod air follower.
            """
            thickness = thickness if thickness is not None else 19.75 * CM_PER_INCH  # Ref. [2]_ pg. 58
            return NETLTransientRod.AirFollower(thickness)

        @staticmethod
        def upper_element_plug(
            thickness: float | None = None,
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> NETLTransientRod.ElementPlug:
            """Creates and returns the default upper transient-rod element plug.

            Parameters
            ----------
            thickness : Optional[float]
                Plug thickness in cm. If omitted, the reference value is used.
            material : Optional[openmc.Material]
                Plug material. If omitted, ``NETLDefaultMaterials.aluminum`` is used at
                ``temperature``.
            temperature : Optional[float]
                Temperature used for the default material. Ignored when ``material``
                is supplied; if omitted, the default temperature is used.

            Returns
            -------
            NETLTransientRod.ElementPlug
                CoreForge upper transient-rod element plug.
            """
            thickness = thickness if thickness is not None else 0.5 * CM_PER_INCH  # Ref. [2]_ pg. 58
            temperature = temperature if temperature is not None else NETLDefaultMaterials.DEFAULT_TEMPERATURE
            material = material if material is not None else NETLDefaultMaterials.aluminum(temperature)  # Ref. [2]_ pg. 51
            return NETLTransientRod.ElementPlug(thickness, Material(material))

        @staticmethod
        def upper_magneform_fitting(
            thickness: float | None = None,
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> NETLTransientRod.MagneformFitting:
            """Creates and returns the default upper transient-rod Magneform fitting.

            Parameters
            ----------
            thickness : Optional[float]
                Fitting thickness in cm. If omitted, the reference value is used.
            material : Optional[openmc.Material]
                Fitting material. If omitted, ``NETLDefaultMaterials.aluminum`` is used
                at ``temperature``.
            temperature : Optional[float]
                Temperature used for the default material. Ignored when ``material``
                is supplied; if omitted, the default temperature is used.

            Returns
            -------
            NETLTransientRod.MagneformFitting
                CoreForge upper transient-rod Magneform fitting.
            """
            thickness = thickness if thickness is not None else 1.0 * CM_PER_INCH  # Ref. [2]_ pg. 58
            temperature = temperature if temperature is not None else NETLDefaultMaterials.DEFAULT_TEMPERATURE
            material = material if material is not None else NETLDefaultMaterials.aluminum(temperature)  # Ref. [2]_ pg. 51
            return NETLTransientRod.MagneformFitting(thickness, Material(material))

        @staticmethod
        def lower_magneform_fitting(
            thickness: float | None = None,
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> NETLTransientRod.MagneformFitting:
            """Creates and returns the default lower transient-rod Magneform fitting.

            Parameters
            ----------
            thickness : Optional[float]
                Fitting thickness in cm. If omitted, the reference value is used.
            material : Optional[openmc.Material]
                Fitting material. If omitted, ``NETLDefaultMaterials.aluminum`` is used
                at ``temperature``.
            temperature : Optional[float]
                Temperature used for the default material. Ignored when ``material``
                is supplied; if omitted, the default temperature is used.

            Returns
            -------
            NETLTransientRod.MagneformFitting
                CoreForge lower transient-rod Magneform fitting.
            """
            thickness = thickness if thickness is not None else 1.0 * CM_PER_INCH  # Ref. [2]_ pg. 58
            temperature = temperature if temperature is not None else NETLDefaultMaterials.DEFAULT_TEMPERATURE
            material = material if material is not None else NETLDefaultMaterials.aluminum(temperature)  # Ref. [2]_ pg. 51
            return NETLTransientRod.MagneformFitting(thickness, Material(material))

        @staticmethod
        def lower_element_plug(
            thickness: float | None = None,
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> NETLTransientRod.ElementPlug:
            """Creates and returns the default lower transient-rod element plug.

            Parameters
            ----------
            thickness : Optional[float]
                Plug thickness in cm. If omitted, the reference value is used.
            material : Optional[openmc.Material]
                Plug material. If omitted, ``NETLDefaultMaterials.aluminum`` is used at
                ``temperature``.
            temperature : Optional[float]
                Temperature used for the default material. Ignored when ``material``
                is supplied; if omitted, the default temperature is used.

            Returns
            -------
            NETLTransientRod.ElementPlug
                CoreForge lower transient-rod element plug.
            """
            thickness = thickness if thickness is not None else 0.5 * CM_PER_INCH  # Ref. [2]_ pg. 58
            temperature = temperature if temperature is not None else NETLDefaultMaterials.DEFAULT_TEMPERATURE
            material = material if material is not None else NETLDefaultMaterials.aluminum(temperature)  # Ref. [2]_ pg. 51
            return NETLTransientRod.ElementPlug(thickness, Material(material))

        @staticmethod
        def fill_gas(
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> Material:
            """Creates and returns the default transient-rod fill gas.

            Parameters
            ----------
            material : Optional[openmc.Material]
                Fill-gas material. If omitted, ``NETLDefaultMaterials.air`` is used.
            temperature : Optional[float]
                Temperature used for the default material. Ignored when ``material``
                is supplied; if omitted, the default temperature is used.

            Returns
            -------
            Material
                CoreForge fill-gas material.
            """
            temperature = temperature if temperature is not None else NETLDefaultMaterials.DEFAULT_TEMPERATURE
            material = material if material is not None else NETLDefaultMaterials.air(temperature)  # Ref. [2]_ pg. 51
            return Material(material)

    @staticmethod
    def upper_grid_plate(
        temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        fuel_location_radius: float | None = None,
        control_rod_location_radius: float | None = None,
        central_thimble_radius: float | None = None,
        penetration_map: dict[str, float | None] | None = None,
        thickness: float | None = None,
        material: openmc.Material | None = None,
    ) -> GridPlate:
        """Creates and returns the default upper grid plate geometry.

        Parameters
        ----------
        temperature : float
            Temperature applied to the default upper-grid-plate material.
        fuel_location_radius : Optional[float]
            Fuel-location penetration radius in cm. If omitted, the reference value
            is used. Ignored when ``penetration_map`` is supplied.
        control_rod_location_radius : Optional[float]
            Control-rod-location penetration radius in cm. If omitted, the reference
            value is used. Ignored when ``penetration_map`` is supplied.
        central_thimble_radius : Optional[float]
            Central-thimble penetration radius in cm. If omitted, the default central
            thimble outer radius is used. Ignored when ``penetration_map`` is supplied.
        penetration_map : Optional[dict[str, float | None]]
            Complete map of core locations to penetration radii. If omitted, the
            standard map is generated from the three radius parameters.
        thickness : Optional[float]
            Grid-plate thickness in cm. If omitted, the reference value is used.
        material : Optional[openmc.Material]
            Grid-plate material. If omitted, ``NETLDefaultMaterials.aluminum`` is used
            at ``temperature``. The temperature is ignored when a material is supplied.

        Returns
        -------
        GridPlate
            Default NETL TRIGA upper grid plate.
        """
        if penetration_map is None:
            fuel_location_radius = (fuel_location_radius if fuel_location_radius is not None else
                                    1.505 * 0.5 * CM_PER_INCH)  # Ref. [1]_ Section 4.2.4.a
            control_rod_location_radius = (
                control_rod_location_radius if control_rod_location_radius is not None else
                1.505 * 0.5 * CM_PER_INCH  # Ref. [1]_ Section 4.2.4.a
            )
            central_thimble_radius = (
                central_thimble_radius if central_thimble_radius is not None else
                DefaultGeometries.central_thimble().cladding.outer_radius
            )
            penetration_map = grid_plate_penetration_map(
                fuel_location_radius,
                control_rod_location_radius,
                central_thimble_radius,
            )

        thickness = thickness if thickness is not None else 0.62 * CM_PER_INCH  # Ref. [2]_ pg. 55
        material = material if material is not None else NETLDefaultMaterials.aluminum(temperature)  # Ref. [2]_ pg. 50

        return GridPlate(
            penetration_map=penetration_map,
            thickness=thickness,
            material=Material(material),
            name="upper_grid_plate",
        )

    @staticmethod
    def lower_grid_plate(
        temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        fuel_location_radius: float | None = None,
        control_rod_location_radius: float | None = None,
        central_thimble_radius: float | None = None,
        penetration_map: dict[str, float | None] | None = None,
        thickness: float | None = None,
        material: openmc.Material | None = None,
    ) -> GridPlate:
        """Creates and returns the default lower grid plate geometry.

        Parameters
        ----------
        temperature : float
            Temperature applied to the default lower-grid-plate material.
        fuel_location_radius : Optional[float]
            Fuel-location penetration radius in cm. If omitted, the reference value
            is used. Ignored when ``penetration_map`` is supplied.
        control_rod_location_radius : Optional[float]
            Control-rod-location penetration radius in cm. If omitted, the reference
            value is used. Ignored when ``penetration_map`` is supplied.
        central_thimble_radius : Optional[float]
            Central-thimble penetration radius in cm. If omitted, the default central
            thimble outer radius is used. Ignored when ``penetration_map`` is supplied.
        penetration_map : Optional[dict[str, float | None]]
            Complete map of core locations to penetration radii. If omitted, the
            standard map is generated from the three radius parameters.
        thickness : Optional[float]
            Grid-plate thickness in cm. If omitted, the reference value is used.
        material : Optional[openmc.Material]
            Grid-plate material. If omitted, ``NETLDefaultMaterials.aluminum`` is used
            at ``temperature``. The temperature is ignored when a material is supplied.

        Returns
        -------
        GridPlate
            Default NETL TRIGA lower grid plate.
        """

        if penetration_map is None:
            fuel_location_radius = (fuel_location_radius if fuel_location_radius is not None else
                                    1.25 * 0.5 * CM_PER_INCH)  # Ref. [1]_ Section 4.2.4.b
            control_rod_location_radius = (
                control_rod_location_radius if control_rod_location_radius is not None else
                1.505 * 0.5 * CM_PER_INCH  # Ref. [1]_ Section 4.2.4.b
            )
            central_thimble_radius = (
                central_thimble_radius if central_thimble_radius is not None else
                DefaultGeometries.central_thimble().cladding.outer_radius
            )
            penetration_map = grid_plate_penetration_map(
                fuel_location_radius,
                control_rod_location_radius,
                central_thimble_radius,
            )

        thickness = thickness if thickness is not None else 1.25 * CM_PER_INCH  # Ref. [2]_ pg. 55
        material = material if material is not None else NETLDefaultMaterials.aluminum(temperature)  # Ref. [2]_ pg. 50

        return GridPlate(
            penetration_map=penetration_map,
            thickness=thickness,
            material=Material(material),
            name="lower_grid_plate",
        )


    @staticmethod
    def pool(
        coolant: openmc.Material | None = None,
        radius: float | None = None,
        height: float | None = None,
    ) -> Pool:
        """Creates and returns the default pool.

        Parameters
        ----------
        coolant : Optional[openmc.Material]
            Coolant material used for the pool contents. If omitted, water is used.
        radius : Optional[float]
            Pool radius in cm. If omitted, the reference value is used.
        height : Optional[float]
            Pool height in cm. If omitted, the reference value is used.

        Returns
        -------
        Pool
            Default NETL TRIGA pool.
        """
        coolant = coolant or NETLDefaultMaterials.water()
        radius = radius if radius is not None else 90.0  # Ref. [2]_ pg. 54
        height = height if height is not None else 160.0  # Ref. [2]_ pg. 54

        return Pool(
            radius=radius,
            height=height,
            material=Material(coolant),  # Ref. [2]_ pg. 48
            name="pool",
        )

    @staticmethod
    def reflector(
        temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        radius: float | None = None,
        height: float | None = None,
        material: openmc.Material | None = None,
    ) -> Reflector:
        """Creates and returns the default reflector.

        Parameters
        ----------
        temperature : float
            Temperature applied to the default reflector material.
        radius : Optional[float]
            Reflector radius in cm. If omitted, the reference value is used.
        height : Optional[float]
            Reflector height in cm. If omitted, the reference value is used.
        material : Optional[openmc.Material]
            Reflector material. If omitted, ``NETLDefaultMaterials.graphite`` is used
            at ``temperature``. The temperature is ignored when a material is supplied.

        Returns
        -------
        Reflector
            Default NETL TRIGA reflector.
        """
        radius = radius if radius is not None else 42.0 * 0.5 * CM_PER_INCH  # Ref. [2]_ pg. 54
        height = height if height is not None else 23.13 * CM_PER_INCH  # Ref. [2]_ pg. 55
        material = material if material is not None else NETLDefaultMaterials.graphite(temperature)  # Ref. [2]_ pg. 48

        return Reflector(
            radius=radius,
            height=height,
            material=Material(material),
            name="reflector",
        )

    @staticmethod
    def shroud(
        temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        thickness: float | None = None,
        primary_hex_inner_radius: float | None = None,
        rotated_hex_inner_radius: float | None = None,
        material: openmc.Material | None = None,
    ) -> Shroud:
        """Creates and returns the default shroud.

        Parameters
        ----------
        temperature : float
            Temperature applied to the default shroud material.
        thickness : Optional[float]
            Shroud-wall thickness in cm. If omitted, the reference value is used.
        primary_hex_inner_radius : Optional[float]
            Primary-hex inradius in cm. If omitted, the reference value is used.
        rotated_hex_inner_radius : Optional[float]
            Rotated-hex inradius in cm. If omitted, the reference value is used.
        material : Optional[openmc.Material]
            Shroud material. If omitted, ``NETLDefaultMaterials.aluminum`` is used at
            ``temperature``. The temperature is ignored when a material is supplied.

        Returns
        -------
        Shroud
            Default NETL TRIGA shroud.
        """
        thickness = thickness if thickness is not None else 0.1875 * CM_PER_INCH  # Ref. [2]_ pg. 54 & 55
        primary_hex_inner_radius = (primary_hex_inner_radius if primary_hex_inner_radius is not None else
                                    10.21875 * CM_PER_INCH)  # Ref. [2]_ pg. 55
        rotated_hex_inner_radius = (rotated_hex_inner_radius if rotated_hex_inner_radius is not None else
                                    10.75 * CM_PER_INCH)  # Ref. [2]_ pg. 54
        material = material if material is not None else NETLDefaultMaterials.aluminum(temperature)  # Ref. [2]_ pg. 48

        return Shroud(
            thickness=thickness,
            primary_hex_inner_radius=primary_hex_inner_radius,
            rotated_hex_inner_radius=rotated_hex_inner_radius,
            material=Material(material),
            name="shroud",
        )

    @staticmethod
    def rsr_cavity(
        temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        outer_radius: float | None = None,
        height: float | None = None,
        number_of_tubes: int | None = None,
        tube_to_center_distance: float | None = None,
        tube_specs: NETLRSRCavity.SpecimenTube | None = None,
        material: openmc.Material | None = None,
    ) -> NETLRSRCavity:
        """Creates and returns the default rotary specimen rack cavity.

        Parameters
        ----------
        temperature : float
            Temperature applied to default specimen-tube and cavity-fill materials.
        outer_radius : Optional[float]
            RSR cavity outer radius in cm. If omitted, the reference value is used.
        height : Optional[float]
            RSR cavity height in cm. If omitted, the reference value is used.
        number_of_tubes : Optional[int]
            Number of specimen tubes. If omitted, the reference value is used.
        tube_to_center_distance : Optional[float]
            Distance from the rack center to each tube centerline in cm. If omitted,
            the reference value is used.
        tube_specs : Optional[NETLRSRCavity.SpecimenTube]
            Specimen-tube override. If omitted,
            ``DefaultGeometries.RSRCavity.specimen_tube`` is used.
        material : Optional[openmc.Material]
            Cavity fill material. If omitted, ``NETLDefaultMaterials.air`` is used at
            ``temperature``. The temperature is ignored when a material is supplied.

        Returns
        -------
        NETLRSRCavity
            Default NETL TRIGA rotary specimen rack cavity.
        """
        outer_radius = outer_radius if outer_radius is not None else 28.625 * 0.5 * CM_PER_INCH  # Ref. [2]_ pg. 55
        height = height if height is not None else 10.8174 * CM_PER_INCH  # Ref. [2]_ pg. 55
        number_of_tubes = number_of_tubes if number_of_tubes is not None else 40  # Ref. [1]_ pg. 10-27
        tube_to_center_distance = (tube_to_center_distance if tube_to_center_distance is not None else
                                   26.312 * 0.5 * CM_PER_INCH)  # Ref. [1]_ pg. 10-27
        tube_specs = (tube_specs if tube_specs is not None else
                      DefaultGeometries.RSRCavity.specimen_tube(temperature=temperature))
        material = material if material is not None else NETLDefaultMaterials.air(temperature)  # Ref. [2]_ pg. 48

        return NETLRSRCavity(
            outer_radius=outer_radius,
            height=height,
            number_of_tubes=number_of_tubes,
            tube_to_center_distance=tube_to_center_distance,
            tube_specs=tube_specs,
            material=Material(material),
            name="rsr_cavity",
        )

    class RSRCavity:
        """Namespace for default NETL rotary-specimen-rack-cavity features."""

        @staticmethod
        def specimen_tube(
            outer_radius: float | None = None,
            thickness: float | None = None,
            material: openmc.Material | None = None,
            temperature: float | None = None,
        ) -> NETLRSRCavity.SpecimenTube:
            """Creates and returns the default RSR specimen tube.

            Parameters
            ----------
            outer_radius : Optional[float]
                Specimen-tube outer radius in cm. If omitted, the reference value is used.
            thickness : Optional[float]
                Specimen-tube wall thickness in cm. If omitted, the reference value is used.
            material : Optional[openmc.Material]
                Tube material. If omitted, ``NETLDefaultMaterials.aluminum`` is used at
                ``temperature``.
            temperature : Optional[float]
                Temperature in Kelvin used to construct the default material. If omitted,
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE`` is used. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            NETLRSRCavity.SpecimenTube
                CoreForge NETL RSR specimen tube.
            """
            outer_radius = outer_radius if outer_radius is not None else 1.0 * 0.5 * CM_PER_INCH  # Ref. [2]_ pg. 56 & 57
            thickness = thickness if thickness is not None else 0.058 * CM_PER_INCH  # Ref. [1]_ pg. 10-27
            temperature = temperature if temperature is not None else NETLDefaultMaterials.DEFAULT_TEMPERATURE
            material = material if material is not None else NETLDefaultMaterials.aluminum(temperature)  # Assumed

            return NETLRSRCavity.SpecimenTube(outer_radius, thickness, Material(material))

    @staticmethod
    def beam_port(
        temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        length: float | None = None,
        inner_radius: float | None = None,
        outer_radius: float | None = None,
        tube_material: openmc.Material | None = None,
        fill_material: openmc.Material | None = None,
    ) -> BeamPort:
        """Creates and returns the default beam port geometry.

        Notes
        -----
        The beam port length is set arbitrarily to the pool diameter to ensure sufficient length
        for penetration through pool / reflector and to provide some known length with which to work
        default transformations off of.

        Parameters
        ----------
        temperature : float
            Temperature applied to the default beam port tube and fill materials.
        length : Optional[float]
            Beam port length in cm. If omitted, the default pool diameter is used.
        inner_radius : Optional[float]
            Beam port inner radius in cm. If omitted, the reference value is used.
        outer_radius : Optional[float]
            Beam port outer radius in cm. If omitted, the reference value is used.
        tube_material : Optional[openmc.Material]
            Beam port tube material. If omitted, ``NETLDefaultMaterials.aluminum``
            is used at ``temperature``.
        fill_material : Optional[openmc.Material]
            Beam port fill material. If omitted, ``NETLDefaultMaterials.air`` is
            used at ``temperature``.

        Returns
        -------
        BeamPort
            Default NETL TRIGA beam port.
        """

        length = length if length is not None else DefaultGeometries.pool().radius * 2.0
        inner_radius = inner_radius if inner_radius is not None else 6.065 * 0.5 * CM_PER_INCH  # Ref. [2]_ Figures 4 & 5
        outer_radius = outer_radius if outer_radius is not None else 6.625 * 0.5 * CM_PER_INCH  # Ref. [2]_ Figures 4 & 5
        tube_material = (tube_material if tube_material is not None else
                         NETLDefaultMaterials.aluminum(temperature))  # Ref. [2]_ pg. 48
        fill_material = (fill_material if fill_material is not None else
                         NETLDefaultMaterials.air(temperature))  # Ref. [2]_ pg. 48

        return BeamPort(
            length=length,
            inner_radius=inner_radius,
            outer_radius=outer_radius,
            tube_material=Material(tube_material),
            fill_material=Material(fill_material),
            name="beam_port",
        )

    @staticmethod
    def core(
        fuel_temp: float = TRIGADefaultMaterials.DEFAULT_TEMPERATURE,
        non_fuel_temp: float = TRIGADefaultMaterials.DEFAULT_TEMPERATURE,
        coolant: openmc.Material | None = None,
        fuel_materials: dict[str, FuelSpec] | None = None,
        pitch: float | None = None,
        central_thimble: CentralThimble | None = None,
        transient_rod: NETLTransientRod | None = None,
        regulating_rod: NETLFuelFollowerControlRod | None = None,
        shim_1_rod: NETLFuelFollowerControlRod | None = None,
        shim_2_rod: NETLFuelFollowerControlRod | None = None,
        loading: dict[str, Core.Loadable | None] | None = None,
        fill_material: Material | None = None,
    ) -> Core:
        """Creates and returns a default core geometry.

        Parameters
        ----------
        fuel_temp : float
            Temperature applied to fuel-bearing materials in core elements.
        non_fuel_temp : float
            Temperature applied to non-fuel materials in core elements.
        coolant : Optional[openmc.Material]
            Coolant material passed to core element builders that use an outer or fill coolant.
        fuel_materials : Optional[dict[str, FuelSpec]]
            Map of core location (e.g. ``"B-01"``) to the ``FuelSpec`` to place there
            (fuel material(s) plus optional radial/axial region counts). Locations not
            listed use the default fuel. Each distinct fuel composition should have a
            unique ``name``. Supplied materials are used as-is (including their own
            temperature); see ``TRIGADefaultGeometries.fuel_element``. Keys must be fuel
            locations; supplying a non-fuel location raises ``ValueError``. Ignored when
            ``loading`` is supplied.
        pitch : Optional[float]
            Hexagonal lattice pitch in cm. If omitted, the reference value is used.
        central_thimble : Optional[CentralThimble]
            Central-thimble override. If omitted, ``DefaultGeometries.central_thimble``
            is used.
        transient_rod : Optional[NETLTransientRod]
            Transient-rod override. If omitted, ``DefaultGeometries.transient_rod`` is used.
        regulating_rod : Optional[NETLFuelFollowerControlRod]
            Regulating-rod override. If omitted,
            ``DefaultGeometries.fuel_follower_control_rod`` is used.
        shim_1_rod : Optional[NETLFuelFollowerControlRod]
            First shim-rod override. If omitted,
            ``DefaultGeometries.fuel_follower_control_rod`` is used.
        shim_2_rod : Optional[NETLFuelFollowerControlRod]
            Second shim-rod override. If omitted,
            ``DefaultGeometries.fuel_follower_control_rod`` is used.
        loading : Optional[dict[str, Core.Loadable | None]]
            Map of mutable core locations to their contents. If omitted, the standard
            NETL core loading is constructed using ``fuel_materials``.
        fill_material : Optional[Material]
            CoreForge material used to fill unoccupied core locations. If omitted, the
            material from ``DefaultGeometries.pool`` is used.

        Returns
        -------
        Core
            Default NETL TRIGA core geometry.
        """
        coolant = coolant or NETLDefaultMaterials.water()

        pitch = pitch if pitch is not None else 1.714 * CM_PER_INCH  # Ref. [2]_ pg. 54
        central_thimble = (central_thimble if central_thimble is not None else
                           DefaultGeometries.central_thimble(non_fuel_temp, coolant))
        transient_rod = (transient_rod if transient_rod is not None else
                         DefaultGeometries.transient_rod(non_fuel_temp, coolant))
        regulating_rod = (regulating_rod if regulating_rod is not None else
                          DefaultGeometries.fuel_follower_control_rod(fuel_temp, non_fuel_temp, coolant))
        shim_1_rod = (shim_1_rod if shim_1_rod is not None else
                      DefaultGeometries.fuel_follower_control_rod(fuel_temp, non_fuel_temp, coolant))
        shim_2_rod = (shim_2_rod if shim_2_rod is not None else
                      DefaultGeometries.fuel_follower_control_rod(fuel_temp, non_fuel_temp, coolant))
        fill_material = (fill_material if fill_material is not None else
                         DefaultGeometries.pool(coolant).material)

        if loading is None:
            def fuel(location: str) -> FuelElement:
                fuel_spec = fuel_materials.get(location) if fuel_materials else None
                return TRIGADefaultGeometries.fuel_element(
                    fuel_temp,
                    non_fuel_temp,
                    coolant,
                    fuel_spec=fuel_spec,
                )

            def graphite(_location: str | None = None) -> GraphiteElement:
                return TRIGADefaultGeometries.graphite_element(non_fuel_temp, coolant)

            def source_holder(_location: str | None = None) -> NETLSourceHolder:
                return DefaultGeometries.source_holder(non_fuel_temp, coolant)

            def fill(locations, factory):
                return {loc: factory(loc) for loc in locations}

            loading = {}
            loading |= fill(["B-01", "B-02", "B-03", "B-04", "B-05", "B-06"], fuel)

            loading |= fill([        "C-02", "C-03", "C-04", "C-05", "C-06",
                                     "C-08", "C-09", "C-10", "C-11", "C-12"], fuel)

            loading |= fill(["D-01", "D-02",         "D-04", "D-05",
                             "D-07", "D-08", "D-09", "D-10", "D-11", "D-12",
                             "D-13",         "D-15", "D-16", "D-17", "D-18"], fuel)
            loading["D-03"] = graphite()

            loading |= fill(["E-01", "E-02", "E-03", "E-04", "E-05", "E-06",
                             "E-07", "E-08", "E-09", "E-10",         "E-12",
                             "E-13", "E-14", "E-15", "E-16", "E-17", "E-18",
                             "E-19", "E-20", "E-21", "E-22", "E-23", "E-24"], fuel)
            loading["E-11"] = None

            loading |= fill(["F-01", "F-02", "F-03", "F-04", "F-05", "F-06",
                             "F-07", "F-08", "F-09", "F-10", "F-11", "F-12",
                                             "F-15", "F-16", "F-17", "F-18",
                             "F-19", "F-20", "F-21", "F-22", "F-23", "F-24",
                             "F-25", "F-26", "F-27", "F-28", "F-29", "F-30"], fuel)
            loading["F-13"] = None
            loading["F-14"] = None

            loading |= fill([        "G-02", "G-03", "G-04", "G-05", "G-06",
                                     "G-08", "G-09", "G-10", "G-11", "G-12",
                                     "G-14", "G-15", "G-16", "G-17", "G-18",
                                     "G-20", "G-21", "G-22", "G-23", "G-24",
                                     "G-26", "G-27", "G-28", "G-29", "G-30",
                                             "G-33", "G-35", "G-36"], fuel)
            loading["G-32"] = source_holder()
            loading["G-34"] = None

            if fuel_materials:
                fuel_locations = {loc for loc, element in loading.items() if isinstance(element, FuelElement)}
                non_fuel_positions = sorted(set(fuel_materials) - fuel_locations)
                if non_fuel_positions:
                    raise ValueError(
                        f"fuel_materials contains locations that are not fuel positions: {non_fuel_positions}. "
                        f"Valid fuel locations are: {sorted(fuel_locations)}"
                    )

        return Core(
            pitch=pitch,
            central_thimble=central_thimble,
            transient_rod=transient_rod,
            regulating_rod=regulating_rod,
            shim_1_rod=shim_1_rod,
            shim_2_rod=shim_2_rod,
            loading=loading,
            fill_material=fill_material,
            name="core",
        )

    @staticmethod
    def reactor(
        fuel_temp: float = TRIGADefaultMaterials.DEFAULT_TEMPERATURE,
        non_fuel_temp: float = TRIGADefaultMaterials.DEFAULT_TEMPERATURE,
        coolant: openmc.Material | None = None,
        transient_rod_position: float = TRANSIENT_ROD_FULLY_INSERTED_POSITION,
        regulating_rod_position: float = FFCR_FULLY_INSERTED_POSITION,
        shim_1_rod_position: float = FFCR_FULLY_INSERTED_POSITION,
        shim_2_rod_position: float = FFCR_FULLY_INSERTED_POSITION,
        fuel_materials: dict[str, FuelSpec] | None = None,
        pool: Pool | None = None,
        shroud: Shroud | None = None,
        rsr_cavity: NETLRSRCavity | None = None,
        core: Core | None = None,
        beam_port_1_5: Reactor.BeamPort | None = None,
        beam_port_2: Reactor.BeamPort | None = None,
        beam_port_3: Reactor.BeamPort | None = None,
        beam_port_4: Reactor.BeamPort | None = None,
        reflector: Reactor.Reflector | None = None,
        upper_grid_plate: Reactor.GridPlate | None = None,
        lower_grid_plate: Reactor.GridPlate | None = None,
    ) -> Reactor:
        """Creates and returns a default reactor geometry.

        Parameters
        ----------
        fuel_temp : float
            Temperature applied to fuel-bearing materials in reactor subcomponents.
        non_fuel_temp : float
            Temperature applied to non-fuel materials in reactor subcomponents.
        coolant : Optional[openmc.Material]
            Coolant material passed to reactor subcomponents that use a coolant material.
            If omitted, water is used.
        transient_rod_position : float
            Axial position of the transient rod relative to the reactor reference
            frame. Defaults to the fully inserted position.
        regulating_rod_position : float
            Axial position of the regulating rod relative to the reactor reference
            frame. Defaults to the fully inserted position.
        shim_1_rod_position : float
            Axial position of shim rod 1 relative to the reactor reference frame.
            Defaults to the fully inserted position.
        shim_2_rod_position : float
            Axial position of shim rod 2 relative to the reactor reference frame.
            Defaults to the fully inserted position.
        fuel_materials : Optional[dict[str, FuelSpec]]
            Map of core location to ``FuelSpec``, forwarded to ``core``. Locations not
            listed use the default fuel. See ``DefaultGeometries.core`` for details.
            Ignored when ``core`` is supplied.
        pool : Optional[Pool]
            Pool override. If omitted, ``DefaultGeometries.pool`` is used.
        shroud : Optional[Shroud]
            Shroud override. If omitted, ``DefaultGeometries.shroud`` is used.
        rsr_cavity : Optional[NETLRSRCavity]
            Rotary-specimen-rack-cavity override. If omitted,
            ``DefaultGeometries.rsr_cavity`` is used.
        core : Optional[Core]
            Core override. If omitted, ``DefaultGeometries.core`` is used.
        beam_port_1_5 : Optional[Reactor.BeamPort]
            Shared beam-port 1/5 geometry and placement override. If omitted, the
            reference geometry and placement are used.
        beam_port_2 : Optional[Reactor.BeamPort]
            Beam-port 2 geometry and placement override. If omitted, the reference
            geometry and placement are used.
        beam_port_3 : Optional[Reactor.BeamPort]
            Beam-port 3 geometry and placement override. If omitted, the reference
            geometry and placement are used.
        beam_port_4 : Optional[Reactor.BeamPort]
            Beam-port 4 geometry and placement override. If omitted, the reference
            geometry and placement are used.
        reflector : Optional[Reactor.Reflector]
            Reflector geometry and placement override. If omitted, the reference
            geometry and placement are used.
        upper_grid_plate : Optional[Reactor.GridPlate]
            Upper-grid-plate geometry and placement override. If omitted, the
            reference geometry and placement are used.
        lower_grid_plate : Optional[Reactor.GridPlate]
            Lower-grid-plate geometry and placement override. If omitted, the
            reference geometry and placement are used.

        Returns
        -------
        Reactor
            Default NETL TRIGA reactor geometry.
        """
        coolant = coolant or NETLDefaultMaterials.water()

        pool = pool if pool is not None else DefaultGeometries.pool(coolant)
        shroud = shroud if shroud is not None else DefaultGeometries.shroud(non_fuel_temp)
        rsr_cavity = (rsr_cavity if rsr_cavity is not None else
                      DefaultGeometries.rsr_cavity(non_fuel_temp))
        core = (core if core is not None else
                DefaultGeometries.core(fuel_temp, non_fuel_temp, coolant, fuel_materials=fuel_materials))

        # Beam port default specifications from Ref. [1]_ page 4-24 & Ref. [2]_ pages 48, 56, 59
        if any(beam_port is None for beam_port in
               (beam_port_1_5, beam_port_2, beam_port_3, beam_port_4)):
            beam_port_geometry = DefaultGeometries.beam_port(non_fuel_temp)
            bp_length = beam_port_geometry.length
            bp_axial_offset = -6.985

            beam_port_1_5 = (beam_port_1_5 if beam_port_1_5 is not None else
                             Reactor.BeamPort(
                                 geometry=beam_port_geometry,
                                 rotation=90.0,
                                 translation=(35.2425, 0.0, bp_axial_offset),
                             ))
            beam_port_2 = (beam_port_2 if beam_port_2 is not None else
                           Reactor.BeamPort(
                               geometry=beam_port_geometry,
                               rotation=150.0,
                               translation=(
                                   6.222 + cosd(150.0) * bp_length * 0.5,
                                   35.255 + sind(150.0) * bp_length * 0.5,
                                   bp_axial_offset,
                               ),
                           ))
            beam_port_3 = (beam_port_3 if beam_port_3 is not None else
                           Reactor.BeamPort(
                               geometry=beam_port_geometry,
                               rotation=0.0,
                               translation=(-bp_length * 0.5 - 26.43188, 0.0, bp_axial_offset),
                           ))
            beam_port_4 = (beam_port_4 if beam_port_4 is not None else
                           Reactor.BeamPort(
                               geometry=beam_port_geometry,
                               rotation=60.0,
                               translation=(
                                   -13.216 - cosd(60.0) * bp_length * 0.5,
                                   -22.871 - sind(60.0) * bp_length * 0.5,
                                   bp_axial_offset,
                               ),
                           ))

        reflector = (reflector if reflector is not None else
                     Reactor.Reflector(
                         geometry=DefaultGeometries.reflector(non_fuel_temp),
                         core_centerline_offset=0.565 * CM_PER_INCH,
                     ))  # Ref. [2]_ pg. 55
        upper_grid_plate = (upper_grid_plate if upper_grid_plate is not None else
                            Reactor.GridPlate(
                                geometry=DefaultGeometries.upper_grid_plate(non_fuel_temp),
                                top_to_core_centerline_distance=(
                                    DefaultGeometries.UPPER_GRID_PLATE_TOP_TO_CORE_CENTERLINE_DISTANCE
                                ),
                            ))
        lower_grid_plate = (lower_grid_plate if lower_grid_plate is not None else
                            Reactor.GridPlate(
                                geometry=DefaultGeometries.lower_grid_plate(non_fuel_temp),
                                top_to_core_centerline_distance=(
                                    DefaultGeometries.LOWER_GRID_PLATE_TOP_TO_CORE_CENTERLINE_DISTANCE
                                ),
                            ))

        return Reactor(
            name="reactor",
            pool=pool,
            shroud=shroud,
            rotary_specimen_rack_cavity=rsr_cavity,
            core=core,
            transient_rod_position=transient_rod_position,
            regulating_rod_position=regulating_rod_position,
            shim_1_rod_position=shim_1_rod_position,
            shim_2_rod_position=shim_2_rod_position,
            beam_port_1_5=beam_port_1_5,
            beam_port_2=beam_port_2,
            beam_port_3=beam_port_3,
            beam_port_4=beam_port_4,
            reflector=reflector,
            upper_grid_plate=upper_grid_plate,
            lower_grid_plate=lower_grid_plate,
        )
