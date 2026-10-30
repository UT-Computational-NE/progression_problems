from __future__ import annotations
from math import cos, radians, sin
from typing import Sequence

import openmc

from coreforge.geometry_elements import CylindricalPinCell, PinCellStack, Stack
from coreforge.geometry_elements.triga import FuelElement, GraphiteElement
from coreforge.geometry_elements.triga.netl import (CentralThimble, SourceHolder as NETLSourceHolder,
                                                    FuelFollowerControlRod as NETLFuelFollowerControlRod,
                                                    TransientRod as NETLTransientRod, GridPlate, BeamPort, Pool,
                                                    PNT as NETLPNT, RSRCavity as NETLRSRCavity,
                                                    ThreeElementIrradiator as NETLThreeElementIrradiator,
                                                    ModifiedThreeElementIrradiator as NETLModifiedThreeElementIrradiator,
                                                    Reflector, Shroud, Core, Reactor as NETLReactor)
from coreforge.geometry_elements.triga.netl.grid_plate import PenetrationMap, grid_plate_penetration_map
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
    .. [3] C. C. Hudson, "Development of a Radioisotope Production Facility Using a
           Cryogenic Cooling System", Ph.D. dissertation, The University of Texas at
           Austin, December 2025.
    """

    THREE_ELEMENT_PENETRATION_RADIUS = 2.40000  # Ref. [3]_ pp. 152, 217
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
        thickness: float = (1.5 - 1.33) * 0.5 * CM_PER_INCH,
        outer_radius: float = 1.5 * 0.5 * CM_PER_INCH,
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
        thickness : float
            Cladding thickness in cm. Defaults to ``(1.5-in - 1.33-in) * 0.5``, per
            Ref. [1]_ Section 10.2.1.b.
        outer_radius : float
            Cladding outer radius in cm. Defaults to half the 1.5-in diameter, per Ref. [1]_ Section 10.2.1.b.
        material : Optional[openmc.Material]
            Cladding material. If omitted, ``NETLDefaultMaterials.aluminum`` is used at ``temperature``, per
            Ref. [2]_ pg. 51. The temperature is ignored when a material is supplied.
        length : Optional[float]
            Central-thimble length in cm. If omitted, the default pool height is used.

        Returns
        -------
        CentralThimble
            Default NETL TRIGA central thimble.
        """
        coolant = coolant or NETLDefaultMaterials.water()
        material = (material if material is not None else NETLDefaultMaterials.aluminum(temperature))
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
            Source-holder length in cm. If omitted, it is derived from the default
            upper- and lower-grid-plate positions and the source-holder offset, per
            Ref. [2]_ pg. 55.
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
            radius: float = 0.981 * 0.5 * CM_PER_INCH,
            length: float = 3.0 * CM_PER_INCH,
            axial_offset: float = -DISTANCE_FROM_LOWER_GRID_PLATE,
            material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLSourceHolder.Cavity:
            """Creates and returns the default source-holder cavity.

            Parameters
            ----------
            radius : float
                Cavity radius in cm. Defaults to half the 0.981-in diameter, per Ref. [1]_ Section 4.2.5.
            length : float
                Cavity length in cm. Defaults to 3.0 in, per Ref. [1]_ Section 4.2.5.
            axial_offset : float
                Offset of the cavity center from the holder center in cm. Defaults to
                ``-DISTANCE_FROM_LOWER_GRID_PLATE`` (-1.1934 cm), placing the cavity
                center at the reactor core centerline, per Ref. [2]_ pg. 55.
            material : Optional[openmc.Material]
                Cavity material. If omitted, ``NETLDefaultMaterials.air`` is used at ``temperature``, per Ref. [2]_
                pg. 54.
            temperature : float
                Temperature in Kelvin used to construct the default material. Defaults to
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE``. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            NETLSourceHolder.Cavity
                CoreForge NETL source-holder cavity.
            """
            material = material if material is not None else NETLDefaultMaterials.air(temperature)

            return NETLSourceHolder.Cavity(radius, length, axial_offset, Material(material))

        @staticmethod
        def cladding(
            outer_radius: float = 1.435 * 0.5 * CM_PER_INCH,
            material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLSourceHolder.Cladding:
            """Creates and returns the default source-holder cladding.

            Parameters
            ----------
            outer_radius : float
                Cladding outer radius in cm. Defaults to half the 1.435-in diameter, per Ref. [2]_ pg. 54 & 55.
            material : Optional[openmc.Material]
                Cladding material. If omitted, ``NETLDefaultMaterials.aluminum`` is used at ``temperature``, per
                Ref. [2]_ pg. 54.
            temperature : float
                Temperature in Kelvin used to construct the default material. Defaults to
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE``. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            NETLSourceHolder.Cladding
                CoreForge NETL source-holder cladding.
            """
            material = material if material is not None else NETLDefaultMaterials.aluminum(temperature)

            return NETLSourceHolder.Cladding(outer_radius, Material(material))

    @staticmethod
    def pnt(
        temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        coolant: openmc.Material | None = None,
        bottom_pos: float | None = None,
        tube: NETLPNT.Tube | None = None,
        terminus: PinCellStack | None = None,
        wrapper: NETLPNT.Wrapper | None = None,
    ) -> NETLPNT:
        """Create and return the default NETL pneumatic transport system.

        Parameters
        ----------
        temperature : float
            Temperature applied to default PNT materials.
        coolant : Optional[openmc.Material]
            Material surrounding the PNT. If omitted, water is used, consistent
            with the reactor-coolant fill in Ref. [2]_ pages 53--55.
        bottom_pos : Optional[float]
            Bottom axial position of the PNT relative to the core midplane
            [cm]. If omitted, the bottom of the lower grid plate is used, as
            derived from Ref. [2]_ pages 53--55.
        tube : Optional[NETLPNT.Tube]
            Transport-tube override. If omitted, the unlined transport tube is
            extended from its specified bottom to the top of the default pool.
        terminus : Optional[PinCellStack]
            Terminus override. If omitted,
            ``DefaultGeometries.PNT.unlined_terminus`` is used.
        wrapper : Optional[NETLPNT.Wrapper]
            Optional wrapper around the transport tube. If omitted, the tube is
            unwrapped.

        Returns
        -------
        NETLPNT
            Default NETL PNT geometry.
        """

        coolant = coolant or NETLDefaultMaterials.water()
        bottom_pos = (
            bottom_pos if bottom_pos is not None
            else -DefaultGeometries.LOWER_GRID_PLATE_TOP_TO_CORE_CENTERLINE_DISTANCE
                 - DefaultGeometries.lower_grid_plate(temperature).thickness
        )
        tube = (
            tube if tube is not None
            else DefaultGeometries.PNT.tube(
                length=(
                    0.5 * DefaultGeometries.pool(coolant).height
                    - DefaultGeometries.PNT.TUBE_BOTTOM_AXIAL_LOCATION
                ),
                temperature=temperature,
            )
        )
        terminus = (
            terminus if terminus is not None
            else DefaultGeometries.PNT.unlined_terminus(
                temperature=temperature,
                outer_material=coolant,
            )
        )

        return NETLPNT(
            tube=tube,
            terminus=terminus,
            bottom_pos=bottom_pos,
            wrapper=wrapper,
            outer_material=Material(coolant),
            gap_tolerance=None,
            name="pnt",
        )

    class PNT:
        """Namespace for default NETL pneumatic-transport-system features.

        The unlined transport-tube dimensions are specified in Ref. [1]_
        Table 10.3 and Ref. [2]_ page 55. The detailed unlined and lined
        terminal dimensions, materials, and axial positions follow the MCNP
        model in Ref. [2]_ pages 53--55, with cadmium as the default liner.
        """

        TUBE_BOTTOM_AXIAL_LOCATION = -18.7182  # Ref. [2]_ pp. 53--55

        @staticmethod
        def tube(
            length: float,
            inner_radius: float = 0.5 * 0.685 * CM_PER_INCH,
            outer_radius: float = 0.5 * 0.875 * CM_PER_INCH,
            material: openmc.Material | None = None,
            fill_material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLPNT.Tube:
            """Create the air-filled aluminum PNT transport tube.

            Parameters
            ----------
            length : float
                Tube length in cm. The default PNT factory derives this from
                the -18.7182-cm tube-bottom position in Ref. [2]_ pages 53--55
                and the top of the modeled pool.
            inner_radius : float
                Tube inner radius in cm. Defaults to half the 0.685-in bore
                diameter in Ref. [1]_ Table 10.3 and Ref. [2]_ page 55.
            outer_radius : float
                Tube outer radius in cm. Defaults to half the 0.875-in outer
                diameter in Ref. [1]_ Table 10.3 and Ref. [2]_ page 55.
            material : Optional[openmc.Material]
                Tube-material override. If omitted, aluminum is used at
                ``temperature``, per Ref. [2]_ page 53.
            fill_material : Optional[openmc.Material]
                Bore-fill override. If omitted, air is used at ``temperature``,
                per Ref. [2]_ page 53.
            temperature : float
                Temperature used to construct default materials. Ignored for
                each material supplied explicitly.

            Returns
            -------
            NETLPNT.Tube
                CoreForge PNT transport-tube specification.
            """

            material = (
                material if material is not None
                else NETLDefaultMaterials.aluminum(temperature)
            )
            fill_material = (
                fill_material if fill_material is not None
                else NETLDefaultMaterials.air(temperature)
            )
            return NETLPNT.Tube(
                inner_radius=inner_radius,
                outer_radius=outer_radius,
                length=length,
                material=Material(material),
                fill_material=Material(fill_material),
            )

        @staticmethod
        def unlined_terminus(
            tube_bottom_thickness: float = 8.3259,
            connecting_tube_thickness: float = 4.1725,
            shock_absorber_thickness: float = 5.1308,
            connecting_tube_radius: float = 0.5 * 1.250 * CM_PER_INCH,
            tube_bottom_radius: float = 0.5 * 0.875 * CM_PER_INCH,
            material: openmc.Material | None = None,
            outer_material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> PinCellStack:
            """Create the unlined PNT terminus stack.

            Parameters
            ----------
            tube_bottom_thickness : float
                Axial thickness of the lowest terminal region in cm. Defaults
                to 8.3259 cm, per Ref. [2]_ pages 53--55.
            connecting_tube_thickness : float
                Connecting-tube axial thickness in cm. Defaults to 4.1725 cm,
                per Ref. [2]_ pages 53--55.
            shock_absorber_thickness : float
                Unlined shock-absorber axial thickness in cm. Defaults to
                5.1308 cm, per Ref. [2]_ pages 53--55.
            connecting_tube_radius : float
                Radius of the 1.250-in-OD connecting tube. Defaults to the
                dimension in Ref. [2]_ page 55.
            tube_bottom_radius : float
                Radius of the 0.875-in-OD unlined tube bottom and shock
                absorber. Defaults to the dimensions in Ref. [1]_ Table 10.3
                and Ref. [2]_ page 55.
            material : Optional[openmc.Material]
                Terminal aluminum override. If omitted, aluminum is used at
                ``temperature``, per Ref. [2]_ page 53.
            outer_material : Optional[openmc.Material]
                Temporary outer material for the component pincells. The
                enclosing PNT replaces it with the PNT coolant.
            temperature : float
                Temperature used to construct default materials. Ignored for
                each material supplied explicitly.

            Returns
            -------
            PinCellStack
                CoreForge unlined PNT terminus ordered from bottom to top.
            """

            material = (
                material if material is not None
                else NETLDefaultMaterials.aluminum(temperature)
            )
            outer_material = outer_material or NETLDefaultMaterials.water()
            aluminum = Material(material)
            exterior = Material(outer_material)

            def solid_section(
                radius: float,
                section_material: Material,
                name: str,
            ) -> CylindricalPinCell:
                return CylindricalPinCell(
                    radii=[radius],
                    materials=[section_material, exterior],
                    name=name,
                )

            return PinCellStack(
                segments=[
                    Stack.Segment(
                        solid_section(tube_bottom_radius, aluminum, "pnt_tube_bottom"),
                        tube_bottom_thickness,
                    ),
                    Stack.Segment(
                        solid_section(
                            connecting_tube_radius,
                            aluminum,
                            "pnt_connecting_tube",
                        ),
                        connecting_tube_thickness,
                    ),
                    Stack.Segment(
                        solid_section(tube_bottom_radius, aluminum, "pnt_shock_absorber"),
                        shock_absorber_thickness,
                    ),
                ],
                name="pnt_unlined_terminus",
            )

        @staticmethod
        def lined_terminus(
            lower_section_thickness: float = 8.3259,
            connecting_tube_thickness: float = 4.1725,
            shock_absorber_section_thickness: float = 2.5400,
            disk_thickness: float = 0.0508,
            narrow_radius: float = 0.5 * 1.250 * CM_PER_INCH,
            wide_radius: float = 0.5 * 1.435 * CM_PER_INCH,
            disk_radius: float = 0.5 * 0.685 * CM_PER_INCH,
            disk_outer_radius: float = 0.5 * 0.875 * CM_PER_INCH,
            material: openmc.Material | None = None,
            liner_material: openmc.Material | None = None,
            outer_material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> PinCellStack:
            """Create the lined PNT terminus stack.

            Parameters
            ----------
            lower_section_thickness : float
                Axial thickness of the lowest terminal region in cm. Defaults
                to 8.3259 cm, per Ref. [2]_ pages 53--55.
            connecting_tube_thickness : float
                Connecting-tube axial thickness in cm. Defaults to 4.1725 cm,
                per Ref. [2]_ pages 53--55.
            shock_absorber_section_thickness : float
                Axial thickness of each shock-absorber section in cm. Defaults
                to 2.5400 cm, per Ref. [2]_ pages 53--55.
            disk_thickness : float
                Liner-disk axial thickness in cm. Defaults to 0.0508 cm, per
                Ref. [2]_ pages 53--55.
            narrow_radius : float
                Radius of the 1.250-in-OD connecting tube and upper shock
                absorber. Defaults to the dimension in Ref. [2]_ page 55.
            wide_radius : float
                Radius of the 1.435-in-OD lower section and lower shock absorber.
                Defaults to the dimension in Ref. [2]_ page 55.
            disk_radius : float
                Liner-region radius in cm. Defaults to 0.86995 cm,
                per Ref. [2]_ pages 54--55.
            disk_outer_radius : float
                Outer radius of the aluminum surround in cm. Defaults to
                1.11125 cm, per Ref. [2]_ pages 54--55.
            material : Optional[openmc.Material]
                Terminal aluminum override. If omitted, aluminum is used at
                ``temperature``, per Ref. [2]_ page 53.
            liner_material : Optional[openmc.Material]
                Disk liner material override (cadmium or lead). If omitted,
                cadmium is used at ``temperature``, per Ref. [2]_ page 53.
            outer_material : Optional[openmc.Material]
                Temporary outer material for the component pincells. The
                enclosing PNT replaces it with the PNT coolant.
            temperature : float
                Temperature used to construct default materials. Ignored for
                each material supplied explicitly.

            Returns
            -------
            PinCellStack
                CoreForge lined PNT terminus ordered from bottom to top.
            """

            material = (
                material if material is not None
                else NETLDefaultMaterials.aluminum(temperature)
            )
            liner_material = (
                liner_material if liner_material is not None
                else NETLDefaultMaterials.cadmium(temperature)
            )
            outer_material = outer_material or NETLDefaultMaterials.water()
            aluminum = Material(material)
            liner = Material(liner_material)
            exterior = Material(outer_material)

            def solid_section(
                radius: float,
                section_material: Material,
                name: str,
            ) -> CylindricalPinCell:
                return CylindricalPinCell(
                    radii=[radius],
                    materials=[section_material, exterior],
                    name=name,
                )

            return PinCellStack(
                segments=[
                    Stack.Segment(
                        solid_section(wide_radius, aluminum, "pnt_lower_section"),
                        lower_section_thickness,
                    ),
                    Stack.Segment(
                        solid_section(narrow_radius, aluminum, "pnt_connecting_tube"),
                        connecting_tube_thickness,
                    ),
                    Stack.Segment(
                        solid_section(wide_radius, aluminum, "pnt_shock_absorber_lower"),
                        shock_absorber_section_thickness,
                    ),
                    Stack.Segment(
                        CylindricalPinCell(
                            radii=[disk_radius, disk_outer_radius],
                            materials=[liner, aluminum, exterior],
                            name="pnt_liner_disk",
                        ),
                        disk_thickness,
                    ),
                    Stack.Segment(
                        solid_section(narrow_radius, aluminum, "pnt_shock_absorber_upper"),
                        shock_absorber_section_thickness,
                    ),
                ],
                name="pnt_lined_terminus",
            )

        @staticmethod
        def wrapper(
            length: float | None = None,
            liner_outer_radius: float = 0.5 * 0.955 * CM_PER_INCH,
            air_gap_outer_radius: float = 0.5 * 1.120 * CM_PER_INCH,
            outer_tube_outer_radius: float = 0.5 * 1.250 * CM_PER_INCH,
            liner_material: openmc.Material | None = None,
            fill_material: openmc.Material | None = None,
            outer_tube_material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLPNT.Wrapper:
            """Create the liner wrapper around the transport tube.

            Parameters
            ----------
            length : Optional[float]
                Wrapped axial length in cm. If omitted, it is derived from the
                -18.7182-cm tube-bottom position and the upper-grid-plate top
                position in Ref. [2]_ pages 53--55.
            liner_outer_radius : float
                Liner outer radius in cm. Defaults to half the 0.955-in
                outer diameter in Ref. [2]_ page 55.
            air_gap_outer_radius : float
                Air-gap outer radius in cm. Defaults to half the 1.120-in outer
                diameter in Ref. [2]_ page 55.
            outer_tube_outer_radius : float
                Outer aluminum tube radius in cm. Defaults to half the 1.250-in
                outer diameter in Ref. [1]_ Table 10.3 and Ref. [2]_ page 55.
            liner_material : Optional[openmc.Material]
                Sleeve liner material override (cadmium or lead). If omitted,
                cadmium is used at ``temperature``, per Ref. [2]_ page 53.
            fill_material : Optional[openmc.Material]
                Annular-gap material override. If omitted, air is used at
                ``temperature``, per Ref. [2]_ page 53.
            outer_tube_material : Optional[openmc.Material]
                Outer-tube material override. If omitted, aluminum is used at
                ``temperature``, per Ref. [2]_ page 53.
            temperature : float
                Temperature used to construct default materials. Ignored for
                each material supplied explicitly.

            Returns
            -------
            NETLPNT.Wrapper
                CoreForge PNT wrapper specification.
            """

            length = (
                length if length is not None
                else DefaultGeometries.UPPER_GRID_PLATE_TOP_TO_CORE_CENTERLINE_DISTANCE
                     - DefaultGeometries.PNT.TUBE_BOTTOM_AXIAL_LOCATION
            )
            liner_material = (
                liner_material if liner_material is not None
                else NETLDefaultMaterials.cadmium(temperature)
            )
            fill_material = (
                fill_material if fill_material is not None
                else NETLDefaultMaterials.air(temperature)
            )
            outer_tube_material = (
                outer_tube_material if outer_tube_material is not None
                else NETLDefaultMaterials.aluminum(temperature)
            )
            cross_section = CylindricalPinCell(
                radii=[
                    liner_outer_radius,
                    air_gap_outer_radius,
                    outer_tube_outer_radius,
                ],
                materials=[
                    Material(liner_material),
                    Material(fill_material),
                    Material(outer_tube_material),
                    Material(NETLDefaultMaterials.water()),
                ],
                name="pnt_wrapper_cross_section",
            )
            return NETLPNT.Wrapper(length=length, cross_section=cross_section)

    @staticmethod
    def three_element_irradiator(
        temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        coolant: openmc.Material | None = None,
        fill_material: openmc.Material | None = None,
        liner_material: openmc.Material | None = None,
        outer_casing: NETLThreeElementIrradiator.OuterCasing | None = None,
        inner_sleeve: NETLThreeElementIrradiator.InnerSleeve | None = None,
        liner: NETLThreeElementIrradiator.Liner | None = None,
    ) -> NETLThreeElementIrradiator:
        """Creates and returns the default conventional three-element irradiator.

        Parameters
        ----------
        temperature : float
            Temperature applied to default irradiator materials.
        coolant : Optional[openmc.Material]
            Material surrounding the outer casing. If omitted, water is used.
        fill_material : Optional[openmc.Material]
            Material filling the irradiator interior and interstitial spaces. If
            omitted, air is used at ``temperature``.
        liner_material : Optional[openmc.Material]
            Material assigned to the default liner. If omitted, cadmium is used
            at ``temperature``. Ignored when ``liner`` is supplied.
        outer_casing : Optional[NETLThreeElementIrradiator.OuterCasing]
            Outer-casing override. If omitted,
            ``DefaultGeometries.ThreeElementIrradiator.outer_casing`` is used.
        inner_sleeve : Optional[NETLThreeElementIrradiator.InnerSleeve]
            Inner-sleeve override. If omitted,
            ``DefaultGeometries.ThreeElementIrradiator.inner_sleeve`` is used.
        liner : Optional[NETLThreeElementIrradiator.Liner]
            Liner override. If omitted,
            ``DefaultGeometries.ThreeElementIrradiator.liner`` is used.

        Returns
        -------
        NETLThreeElementIrradiator
            Default conventional NETL three-element irradiator.
        """
        coolant = coolant or NETLDefaultMaterials.water()
        fill_material = (fill_material if fill_material is not None else
                         NETLDefaultMaterials.air(temperature))
        liner_material = (liner_material if liner_material is not None else
                          NETLDefaultMaterials.cadmium(temperature))
        outer_casing = (outer_casing if outer_casing is not None else
                        DefaultGeometries.ThreeElementIrradiator.outer_casing(temperature=temperature))
        inner_sleeve = (inner_sleeve if inner_sleeve is not None else
                        DefaultGeometries.ThreeElementIrradiator.inner_sleeve(temperature=temperature))
        liner = (liner if liner is not None else
                 DefaultGeometries.ThreeElementIrradiator.liner(
                     material=liner_material,
                     temperature=temperature,
                 ))

        return NETLThreeElementIrradiator(
            outer_casing=outer_casing,
            inner_sleeve=inner_sleeve,
            liner=liner,
            fill_material=Material(fill_material),
            outer_material=Material(coolant),
            gap_tolerance=None,
            name="three_element_irradiator",
        )

    class ThreeElementIrradiator:
        """Namespace for default conventional three-element-irradiator features."""

        @staticmethod
        def outer_casing(
            inner_radius: float = 2.23393,
            outer_radius: float = 2.38125,
            length: float = 127.9524,
            solid_upper_end_thickness: float = 3.1750,
            solid_lower_end_thickness: float = 2.5399,
            material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLThreeElementIrradiator.OuterCasing:
            """Creates and returns the default outer casing.

            Dimensions default to the conventional 3-EL specification in Ref.
            [3]_ pages 184, 186, and 217--218.

            Parameters
            ----------
            inner_radius : float
                Casing inner radius in cm.
            outer_radius : float
                Casing outer radius in cm.
            length : float
                Overall casing axial length in cm.
            solid_upper_end_thickness : float
                Solid upper-end axial thickness in cm.
            solid_lower_end_thickness : float
                Solid lower-end axial thickness in cm.
            material : Optional[openmc.Material]
                Material override. If omitted, aluminum is used at
                ``temperature``.
            temperature : float
                Temperature used to construct the default material. Ignored
                when ``material`` is supplied.

            Returns
            -------
            NETLThreeElementIrradiator.OuterCasing
                CoreForge outer-casing specification.
            """
            material = material if material is not None else NETLDefaultMaterials.aluminum(temperature)
            return NETLThreeElementIrradiator.OuterCasing(
                inner_radius=inner_radius,
                outer_radius=outer_radius,
                length=length,
                solid_upper_end_thickness=solid_upper_end_thickness,
                solid_lower_end_thickness=solid_lower_end_thickness,
                material=Material(material),
            )

        @staticmethod
        def inner_sleeve(
            inner_radius: float = 1.93929,
            outer_radius: float = 2.06375,
            sidewall_length: float = 119.6975,
            bottom_thickness: float = 0.3175,
            material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLThreeElementIrradiator.InnerSleeve:
            """Creates and returns the default inner sleeve.

            Dimensions default to the conventional 3-EL specification in Ref.
            [3]_ pages 187 and 217--218.

            Parameters
            ----------
            inner_radius : float
                Sleeve inner radius in cm.
            outer_radius : float
                Sleeve outer radius in cm.
            sidewall_length : float
                Sleeve-sidewall axial length in cm.
            bottom_thickness : float
                Solid-bottom axial thickness in cm.
            material : Optional[openmc.Material]
                Material override. If omitted, aluminum is used at
                ``temperature``.
            temperature : float
                Temperature used to construct the default material. Ignored
                when ``material`` is supplied.

            Returns
            -------
            NETLThreeElementIrradiator.InnerSleeve
                CoreForge inner-sleeve specification.
            """
            material = material if material is not None else NETLDefaultMaterials.aluminum(temperature)
            return NETLThreeElementIrradiator.InnerSleeve(
                inner_radius=inner_radius,
                outer_radius=outer_radius,
                sidewall_length=sidewall_length,
                bottom_thickness=bottom_thickness,
                material=Material(material),
            )

        @staticmethod
        def liner(
            thickness: float = 0.10160,
            sidewall_length: float = 118.1100,
            bottom_thickness: float = 0.1016,
            material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLThreeElementIrradiator.Liner:
            """Creates and returns the default liner.

            Dimensions default to the conventional 3-EL specification in Ref.
            [3]_ pages 140, 187, and 217--218.

            Parameters
            ----------
            thickness : float
                Liner radial thickness in cm.
            sidewall_length : float
                Liner-sidewall axial length in cm.
            bottom_thickness : float
                Solid-bottom axial thickness in cm.
            material : Optional[openmc.Material]
                Material override. If omitted, cadmium is used at
                ``temperature``.
            temperature : float
                Temperature used to construct the default material. Ignored
                when ``material`` is supplied.

            Returns
            -------
            NETLThreeElementIrradiator.Liner
                CoreForge liner specification.
            """
            material = material if material is not None else NETLDefaultMaterials.cadmium(temperature)
            return NETLThreeElementIrradiator.Liner(
                thickness=thickness,
                sidewall_length=sidewall_length,
                bottom_thickness=bottom_thickness,
                material=Material(material),
            )

    @staticmethod
    def modified_three_element_irradiator(
        temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        coolant: openmc.Material | None = None,
        fill_material: openmc.Material | None = None,
        outer_casing: NETLModifiedThreeElementIrradiator.OuterCasing | None = None,
        pneumatic_system: NETLModifiedThreeElementIrradiator.PneumaticSystem | None = None,
        b4c_canister: NETLModifiedThreeElementIrradiator.B4CCanister | None = None,
        b10_canister: NETLModifiedThreeElementIrradiator.B10Canister | None = None,
        silver_disk: NETLModifiedThreeElementIrradiator.Disk | None = None,
        cadmium_disk: NETLModifiedThreeElementIrradiator.Disk | None = None,
        hollow_spacer: NETLModifiedThreeElementIrradiator.HollowSpacer | None = None,
        solid_spacer: NETLModifiedThreeElementIrradiator.SolidSpacer | None = None,
        simplified: bool = False,
    ) -> NETLModifiedThreeElementIrradiator:
        """Create and return the default modified three-element irradiator.

        The detailed geometry defaults follow the active modified-3-EL model
        in Ref. [3]_ pages 186--187, 221--222, 228, and 243. Setting
        ``simplified`` selects the documented volume-preserving ten-region
        representation derived from that detailed geometry.

        Parameters
        ----------
        temperature : float
            Temperature applied to default irradiator materials.
        coolant : Optional[openmc.Material]
            Material surrounding the outer casing. If omitted, water is used.
        fill_material : Optional[openmc.Material]
            Material filling the casing interior and interstitial spaces. If
            omitted, air is used at ``temperature``.
        outer_casing : Optional[NETLModifiedThreeElementIrradiator.OuterCasing]
            Outer-casing override. If omitted, the default is used.
        pneumatic_system : Optional[NETLModifiedThreeElementIrradiator.PneumaticSystem]
            Pneumatic-system override. If omitted, the default is used.
        b4c_canister : Optional[NETLModifiedThreeElementIrradiator.B4CCanister]
            Natural-B4C-canister override. If omitted, the default is used.
        b10_canister : Optional[NETLModifiedThreeElementIrradiator.B10Canister]
            Enriched-boron-canister override. If omitted, the default is used.
        silver_disk : Optional[NETLModifiedThreeElementIrradiator.Disk]
            Silver-disk override. If omitted, the default is used.
        cadmium_disk : Optional[NETLModifiedThreeElementIrradiator.Disk]
            Cadmium-disk override. If omitted, the default is used.
        hollow_spacer : Optional[NETLModifiedThreeElementIrradiator.HollowSpacer]
            Hollow-spacer override. If omitted, the default is used.
        solid_spacer : Optional[NETLModifiedThreeElementIrradiator.SolidSpacer]
            Solid-spacer override. If omitted, the default is used.
        simplified : bool
            Whether to select the ten-region simplified geometry. Defaults to
            ``False`` for the detailed geometry.

        Returns
        -------
        NETLModifiedThreeElementIrradiator
            Default NETL modified three-element irradiator.
        """

        coolant = coolant or NETLDefaultMaterials.water()
        fill_material = (
            fill_material if fill_material is not None
            else NETLDefaultMaterials.air(temperature)
        )
        outer_casing = (
            outer_casing if outer_casing is not None
            else DefaultGeometries.ModifiedThreeElementIrradiator.outer_casing(
                temperature=temperature
            )
        )
        pneumatic_system = (
            pneumatic_system if pneumatic_system is not None
            else DefaultGeometries.ModifiedThreeElementIrradiator.pneumatic_system(
                temperature=temperature
            )
        )
        b4c_canister = (
            b4c_canister if b4c_canister is not None
            else DefaultGeometries.ModifiedThreeElementIrradiator.b4c_canister(
                temperature=temperature
            )
        )
        b10_canister = (
            b10_canister if b10_canister is not None
            else DefaultGeometries.ModifiedThreeElementIrradiator.b10_canister(
                temperature=temperature
            )
        )
        silver_disk = (
            silver_disk if silver_disk is not None
            else DefaultGeometries.ModifiedThreeElementIrradiator.silver_disk(
                temperature=temperature
            )
        )
        cadmium_disk = (
            cadmium_disk if cadmium_disk is not None
            else DefaultGeometries.ModifiedThreeElementIrradiator.cadmium_disk(
                temperature=temperature
            )
        )
        hollow_spacer = (
            hollow_spacer if hollow_spacer is not None
            else DefaultGeometries.ModifiedThreeElementIrradiator.hollow_spacer(
                temperature=temperature
            )
        )
        solid_spacer = (
            solid_spacer if solid_spacer is not None
            else DefaultGeometries.ModifiedThreeElementIrradiator.solid_spacer(
                temperature=temperature
            )
        )

        return NETLModifiedThreeElementIrradiator(
            outer_casing=outer_casing,
            pneumatic_system=pneumatic_system,
            b4c_canister=b4c_canister,
            b10_canister=b10_canister,
            silver_disk=silver_disk,
            cadmium_disk=cadmium_disk,
            hollow_spacer=hollow_spacer,
            solid_spacer=solid_spacer,
            fill_material=Material(fill_material),
            outer_material=Material(coolant),
            gap_tolerance=None,
            simplified=simplified,
            name="modified_three_element_irradiator",
        )

    class ModifiedThreeElementIrradiator:
        """Namespace for default modified three-element-irradiator features.

        Dimensions follow the detailed modified-3-EL specification in Ref.
        [3]_ pages 186--187, 221--222, 228, and 243.
        """

        @staticmethod
        def outer_casing(
            tube_1_inner_radius: float = 2.23393,
            tube_1_outer_radius: float = 2.30759,
            tube_1_length: float = 124.77400,
            tube_2_outer_radius: float = 2.38125,
            tube_2_annulus_length: float = 81.27660,
            tube_2_solid_upper_region_length: float = 3.39830,
            material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLModifiedThreeElementIrradiator.OuterCasing:
            """Create the default two-tube outer casing.

            Dimensions follow Ref. [3]_ pages 186--187, 222, 228, and 243.
            The material defaults to aluminum at ``temperature``.

            Parameters
            ----------
            tube_1_inner_radius : float
                Tube #1 inner radius in cm. Defaults to 2.23393 cm, per Ref.
                [3]_ pages 186--187, 222, 228, and 243.
            tube_1_outer_radius : float
                Tube #1 outer radius in cm. Defaults to 2.30759 cm, per Ref.
                [3]_ pages 186--187, 222, 228, and 243.
            tube_1_length : float
                Tube #1 axial length in cm. Defaults to 124.77400 cm, per Ref.
                [3]_ pages 186--187, 222, 228, and 243.
            tube_2_outer_radius : float
                Tube #2 outer radius in cm. Defaults to 2.38125 cm, per Ref.
                [3]_ pages 186--187, 222, 228, and 243.
            tube_2_annulus_length : float
                Axial length over which Tube #2 surrounds Tube #1 in cm.
                Defaults to 81.27660 cm, per Ref. [3]_ pages 186--187, 222,
                228, and 243.
            tube_2_solid_upper_region_length : float
                Axial length of the modeled solid Tube #2 region above Tube #1
                in cm. This is Defaults to 3.39830 cm,
                per Ref. [3]_ pages 186--187, 222, 228, and 243.
            material : Optional[openmc.Material]
                Casing-material override. Defaults to ``None``, which uses
                aluminum per Ref. [3]_ pages 186--187 and 222.
            temperature : float
                Temperature used to construct the default material. Defaults
                to ``NETLDefaultMaterials.DEFAULT_TEMPERATURE`` and is ignored
                when ``material`` is supplied.

            Returns
            -------
            NETLModifiedThreeElementIrradiator.OuterCasing
                CoreForge modified-3-EL outer-casing specification.
            """

            material = (
                material if material is not None
                else NETLDefaultMaterials.aluminum(temperature)
            )
            return NETLModifiedThreeElementIrradiator.OuterCasing(
                tube_1_inner_radius=tube_1_inner_radius,
                tube_1_outer_radius=tube_1_outer_radius,
                tube_1_length=tube_1_length,
                tube_2_outer_radius=tube_2_outer_radius,
                tube_2_annulus_length=tube_2_annulus_length,
                tube_2_solid_upper_region_length=tube_2_solid_upper_region_length,
                material=Material(material),
            )

        @staticmethod
        def pneumatic_system(
            tube_inner_radius: float = 0.67000,
            tube_outer_radius: float = 0.79400,
            sleeve_inner_radius: float = 0.86350,
            sleeve_outer_radius: float = 0.95250,
            open_tube_length: float = 109.73188,
            tube_lower_end_cap_thickness: float = 0.12400,
            sleeve_lower_end_cap_thickness: float = 0.12850,
            material: openmc.Material | None = None,
            fill_material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLModifiedThreeElementIrradiator.PneumaticSystem:
            """Create the default central pneumatic tube and sleeve.

            Dimensions and the aluminum/air assignments follow Ref. [3]_
            pages 186 and 221. All dimensions are in cm.

            Parameters
            ----------
            tube_inner_radius : float
                Pneumatic-tube inner radius in cm. Defaults to 0.67000 cm, per
                Ref. [3]_ pages 186 and 221.
            tube_outer_radius : float
                Pneumatic-tube outer radius in cm. Defaults to 0.79400 cm, per
                Ref. [3]_ pages 186 and 221.
            sleeve_inner_radius : float
                Pneumatic-sleeve inner radius in cm. Defaults to 0.86350 cm,
                per Ref. [3]_ pages 186 and 221.
            sleeve_outer_radius : float
                Pneumatic-sleeve outer radius in cm. Defaults to 0.95250 cm,
                per Ref. [3]_ pages 186 and 221.
            open_tube_length : float
                Length of the open pneumatic-tube passage below the top of
                Tube #1 in cm. Defaults to 109.73188 cm, per Ref. [3]_ pages
                186 and 221.
            tube_lower_end_cap_thickness : float
                Pneumatic-tube lower-end-cap thickness in cm. Defaults to
                0.12400 cm, per Ref. [3]_ pages 186 and 221.
            sleeve_lower_end_cap_thickness : float
                Pneumatic-sleeve lower-end-cap thickness in cm. Defaults to
                0.12850 cm, per Ref. [3]_ pages 186 and 221.
            material : Optional[openmc.Material]
                Tube-and-sleeve material override. Defaults to ``None``, which
                uses aluminum per Ref. [3]_ pages 186 and 221.
            fill_material : Optional[openmc.Material]
                Passage-and-gap fill override. Defaults to ``None``, which uses
                air per Ref. [3]_ pages 186 and 221.
            temperature : float
                Temperature used to construct default materials. Defaults to
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE`` and is ignored for
                each material supplied explicitly.

            Returns
            -------
            NETLModifiedThreeElementIrradiator.PneumaticSystem
                CoreForge modified-3-EL pneumatic-system specification.
            """

            material = (
                material if material is not None
                else NETLDefaultMaterials.aluminum(temperature)
            )
            fill_material = (
                fill_material if fill_material is not None
                else NETLDefaultMaterials.air(temperature)
            )
            return NETLModifiedThreeElementIrradiator.PneumaticSystem(
                tube_inner_radius=tube_inner_radius,
                tube_outer_radius=tube_outer_radius,
                sleeve_inner_radius=sleeve_inner_radius,
                sleeve_outer_radius=sleeve_outer_radius,
                open_tube_length=open_tube_length,
                tube_lower_end_cap_thickness=tube_lower_end_cap_thickness,
                sleeve_lower_end_cap_thickness=sleeve_lower_end_cap_thickness,
                material=Material(material),
                fill_material=Material(fill_material),
            )

        @staticmethod
        def b4c_canister(
            b4c_region_inner_radius: float = 1.11125,
            b4c_region_outer_radius: float = 1.89230,
            canister_outer_radius: float = 2.19009,
            top_cap_thickness: float = 0.19660,
            b4c_region_thickness: float = 52.00278,
            bottom_cap_thickness: float = 0.20000,
            b4c_material: openmc.Material | None = None,
            canister_material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLModifiedThreeElementIrradiator.B4CCanister:
            """Create the default natural-B4C upper canister.

            Dimensions follow Ref. [3]_ pages 186 and 221. The canister
            defaults to aluminum and the filter material uses the natural-B4C
            powder composition from Ref. [3]_ pages 186 and 269.

            Parameters
            ----------
            b4c_region_inner_radius : float
                Natural-B4C-region inner radius in cm. Defaults to 1.11125 cm,
                per Ref. [3]_ pages 186 and 221.
            b4c_region_outer_radius : float
                Natural-B4C-region outer radius in cm. Defaults to 1.89230 cm,
                per Ref. [3]_ pages 186 and 221.
            canister_outer_radius : float
                Aluminum-canister outer radius in cm. Defaults to 2.19009 cm,
                per Ref. [3]_ pages 186 and 221.
            top_cap_thickness : float
                Canister top-cap axial thickness in cm. Defaults to 0.19660 cm,
                per Ref. [3]_ pages 186 and 221.
            b4c_region_thickness : float
                Natural-B4C-region axial thickness in cm. Defaults to
                52.00278 cm, per Ref. [3]_ pages 186 and 221.
            bottom_cap_thickness : float
                Canister bottom-cap axial thickness in cm. Defaults to
                0.20000 cm, per Ref. [3]_ pages 186 and 221.
            b4c_material : Optional[openmc.Material]
                Filter-material override. Defaults to ``None``, which uses the
                natural-B4C powder density and composition from Ref. [3]_ pages
                186 and 269.
            canister_material : Optional[openmc.Material]
                Canister-material override. Defaults to ``None``, which uses
                aluminum per Ref. [3]_ pages 186 and 221.
            temperature : float
                Temperature used to construct default materials. Defaults to
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE`` and is ignored for
                each material supplied explicitly.

            Returns
            -------
            NETLModifiedThreeElementIrradiator.B4CCanister
                CoreForge natural-B4C-canister specification.
            """

            b4c_material = (
                b4c_material if b4c_material is not None
                else NETLDefaultMaterials.natural_b4c(temperature)
            )
            canister_material = (
                canister_material if canister_material is not None
                else NETLDefaultMaterials.aluminum(temperature)
            )
            return NETLModifiedThreeElementIrradiator.B4CCanister(
                b4c_region_inner_radius=b4c_region_inner_radius,
                b4c_region_outer_radius=b4c_region_outer_radius,
                canister_outer_radius=canister_outer_radius,
                top_cap_thickness=top_cap_thickness,
                b4c_region_thickness=b4c_region_thickness,
                bottom_cap_thickness=bottom_cap_thickness,
                b4c_material=Material(b4c_material),
                canister_material=Material(canister_material),
            )

        @staticmethod
        def b10_canister(
            b10_annulus_inner_radius: float = 1.03759,
            upper_b10_outer_radius: float = 2.00660,
            lower_b10_outer_radius: float = 2.04724,
            canister_exterior_wall_radius: float = 2.12090,
            cadmium_sleeve_outer_radius: float = 2.17090,
            gap_to_b4c_canister: float = 0.10000,
            top_cap_thickness: float = 2.54000,
            upper_b10_region_thickness: float = 22.86000,
            lower_b10_region_thickness: float = 34.92500,
            exterior_wall_lower_end_cap_thickness: float = 0.63500,
            lower_b10_solid_section_thickness: float = 2.54000,
            b10_material: openmc.Material | None = None,
            canister_material: openmc.Material | None = None,
            cadmium_sleeve_material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLModifiedThreeElementIrradiator.B10Canister:
            """Create the default enriched-boron lower canister.

            Dimensions follow Ref. [3]_ pages 186--187 and 221. The canister
            defaults to aluminum, the sleeve to cadmium, and the filter to the
            enriched-boron powder specified by Ref. [3]_ pages 187 and 277.

            Parameters
            ----------
            b10_annulus_inner_radius : float
                Inner radius of the annular B-10 regions in cm. Defaults to
                1.03759 cm, per Ref. [3]_ pages 186--187 and 221.
            upper_b10_outer_radius : float
                Outer radius of the upper B-10 annulus in cm. Defaults to
                2.00660 cm, per Ref. [3]_ pages 186--187 and 221.
            lower_b10_outer_radius : float
                Outer radius of the lower B-10 region in cm. Defaults to
                2.04724 cm, per Ref. [3]_ pages 186--187 and 221.
            canister_exterior_wall_radius : float
                Canister exterior-wall outer radius in cm. Defaults to
                2.12090 cm, per Ref. [3]_ pages 186--187 and 221.
            cadmium_sleeve_outer_radius : float
                Cadmium-sleeve outer radius in cm. Defaults to 2.17090 cm, per
                Ref. [3]_ pages 186--187 and 221.
            gap_to_b4c_canister : float
                Axial air gap to the B4C canister in cm. Defaults to 0.10000 cm,
                per Ref. [3]_ pages 186--187 and 221.
            top_cap_thickness : float
                Canister top-cap axial thickness in cm. Defaults to 2.54000 cm,
                per Ref. [3]_ pages 186--187 and 221.
            upper_b10_region_thickness : float
                Upper B-10-region axial thickness in cm. Defaults to
                22.86000 cm, per Ref. [3]_ pages 186--187 and 221.
            lower_b10_region_thickness : float
                Complete lower B-10-region axial thickness in cm. Defaults to
                34.92500 cm, per Ref. [3]_ pages 186--187 and 221.
            exterior_wall_lower_end_cap_thickness : float
                Canister exterior-wall lower-end-cap thickness in cm. Defaults
                to 0.63500 cm, per Ref. [3]_ pages 186--187 and 221.
            lower_b10_solid_section_thickness : float
                Solid lower portion of the B-10 region in cm. Defaults to
                2.54000 cm, per Ref. [3]_ pages 186--187 and 221.
            b10_material : Optional[openmc.Material]
                Filter-material override. Defaults to ``None``, which uses the
                enriched-boron powder density and composition from Ref. [3]_
                pages 187 and 277.
            canister_material : Optional[openmc.Material]
                Canister-material override. Defaults to ``None``, which uses
                aluminum per Ref. [3]_ pages 186--187 and 221.
            cadmium_sleeve_material : Optional[openmc.Material]
                Sleeve-material override. Defaults to ``None``, which uses
                cadmium per Ref. [3]_ pages 186--187 and 221.
            temperature : float
                Temperature used to construct default materials. Defaults to
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE`` and is ignored for
                each material supplied explicitly.

            Returns
            -------
            NETLModifiedThreeElementIrradiator.B10Canister
                CoreForge enriched-boron-canister specification.
            """

            b10_material = (
                b10_material if b10_material is not None
                else NETLDefaultMaterials.enriched_boron(temperature)
            )
            canister_material = (
                canister_material if canister_material is not None
                else NETLDefaultMaterials.aluminum(temperature)
            )
            cadmium_sleeve_material = (
                cadmium_sleeve_material if cadmium_sleeve_material is not None
                else NETLDefaultMaterials.cadmium(temperature)
            )
            return NETLModifiedThreeElementIrradiator.B10Canister(
                b10_annulus_inner_radius=b10_annulus_inner_radius,
                upper_b10_outer_radius=upper_b10_outer_radius,
                lower_b10_outer_radius=lower_b10_outer_radius,
                canister_exterior_wall_radius=canister_exterior_wall_radius,
                cadmium_sleeve_outer_radius=cadmium_sleeve_outer_radius,
                gap_to_b4c_canister=gap_to_b4c_canister,
                top_cap_thickness=top_cap_thickness,
                upper_b10_region_thickness=upper_b10_region_thickness,
                lower_b10_region_thickness=lower_b10_region_thickness,
                exterior_wall_lower_end_cap_thickness=(
                    exterior_wall_lower_end_cap_thickness
                ),
                lower_b10_solid_section_thickness=lower_b10_solid_section_thickness,
                b10_material=Material(b10_material),
                canister_material=Material(canister_material),
                cadmium_sleeve_material=Material(cadmium_sleeve_material),
            )

        @staticmethod
        def silver_disk(
            thickness: float = 0.10000,
            material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLModifiedThreeElementIrradiator.Disk:
            """Create the silver filter disk.

            Parameters
            ----------
            thickness : float
                Disk axial thickness in cm. Defaults to 0.10000 cm, per Ref.
                [3]_ pages 187 and 221.
            material : Optional[openmc.Material]
                Disk-material override. Defaults to ``None``, which uses the
                silver density and composition from Ref. [3]_ pages 187 and
                277.
            temperature : float
                Temperature used to construct the default material. Defaults
                to ``NETLDefaultMaterials.DEFAULT_TEMPERATURE`` and is ignored
                when ``material`` is supplied.

            Returns
            -------
            NETLModifiedThreeElementIrradiator.Disk
                CoreForge silver-disk specification.
            """

            material = (
                material if material is not None
                else NETLDefaultMaterials.silver(temperature)
            )
            return NETLModifiedThreeElementIrradiator.Disk(
                thickness=thickness,
                material=Material(material),
            )

        @staticmethod
        def cadmium_disk(
            thickness: float = 0.10000,
            material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLModifiedThreeElementIrradiator.Disk:
            """Create the cadmium filter disk.

            Parameters
            ----------
            thickness : float
                Disk axial thickness in cm. Defaults to 0.10000 cm, per Ref.
                [3]_ pages 187 and 221.
            material : Optional[openmc.Material]
                Disk-material override. Defaults to ``None``, which uses
                cadmium per Ref. [3]_ pages 187 and 221.
            temperature : float
                Temperature used to construct the default material. Defaults
                to ``NETLDefaultMaterials.DEFAULT_TEMPERATURE`` and is ignored
                when ``material`` is supplied.

            Returns
            -------
            NETLModifiedThreeElementIrradiator.Disk
                CoreForge cadmium-disk specification.
            """

            material = (
                material if material is not None
                else NETLDefaultMaterials.cadmium(temperature)
            )
            return NETLModifiedThreeElementIrradiator.Disk(
                thickness=thickness,
                material=Material(material),
            )

        @staticmethod
        def hollow_spacer(
            hollow_section_radius: float = 2.03393,
            hollow_section_thickness: float = 3.00000,
            solid_upper_cap_thickness: float = 0.49472,
            material: openmc.Material | None = None,
            fill_material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLModifiedThreeElementIrradiator.HollowSpacer:
            """Create the default air-filled hollow aluminum spacer.

            Dimensions and material assignments follow Ref. [3]_ pages 187
            and 221.

            Parameters
            ----------
            hollow_section_radius : float
                Radius of the air-filled hollow section in cm. Defaults to
                2.03393 cm, per Ref. [3]_ pages 187 and 221.
            hollow_section_thickness : float
                Hollow-section axial thickness in cm. Defaults to 3.00000 cm,
                per Ref. [3]_ pages 187 and 221.
            solid_upper_cap_thickness : float
                Solid upper-cap axial thickness in cm. Defaults to 0.49472 cm,
                per Ref. [3]_ pages 187 and 221.
            material : Optional[openmc.Material]
                Spacer-material override. Defaults to ``None``, which uses
                aluminum per Ref. [3]_ pages 187 and 221.
            fill_material : Optional[openmc.Material]
                Hollow-section fill override. Defaults to ``None``, which uses
                air per Ref. [3]_ pages 187 and 221.
            temperature : float
                Temperature used to construct default materials. Defaults to
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE`` and is ignored for
                each material supplied explicitly.

            Returns
            -------
            NETLModifiedThreeElementIrradiator.HollowSpacer
                CoreForge hollow-spacer specification.
            """

            material = (
                material if material is not None
                else NETLDefaultMaterials.aluminum(temperature)
            )
            fill_material = (
                fill_material if fill_material is not None
                else NETLDefaultMaterials.air(temperature)
            )
            return NETLModifiedThreeElementIrradiator.HollowSpacer(
                hollow_section_radius=hollow_section_radius,
                hollow_section_thickness=hollow_section_thickness,
                solid_upper_cap_thickness=solid_upper_cap_thickness,
                material=Material(material),
                fill_material=Material(fill_material),
            )

        @staticmethod
        def solid_spacer(
            thickness: float = 5.08000,
            material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLModifiedThreeElementIrradiator.SolidSpacer:
            """Create the solid aluminum lower spacer.

            Parameters
            ----------
            thickness : float
                Spacer axial thickness in cm. Defaults to 5.08000 cm, per Ref.
                [3]_ pages 187 and 222.
            material : Optional[openmc.Material]
                Spacer-material override. Defaults to ``None``, which uses
                aluminum per Ref. [3]_ pages 187 and 222.
            temperature : float
                Temperature used to construct the default material. Defaults
                to ``NETLDefaultMaterials.DEFAULT_TEMPERATURE`` and is ignored
                when ``material`` is supplied.

            Returns
            -------
            NETLModifiedThreeElementIrradiator.SolidSpacer
                CoreForge solid-spacer specification.
            """

            material = (
                material if material is not None
                else NETLDefaultMaterials.aluminum(temperature)
            )
            return NETLModifiedThreeElementIrradiator.SolidSpacer(
                thickness=thickness,
                material=Material(material),
            )

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
            thickness: float = 0.02 * CM_PER_INCH,
            outer_radius: float = 1.35 * 0.5 * CM_PER_INCH,
            material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLFuelFollowerControlRod.Cladding:
            """Creates and returns the default control-rod cladding.

            Parameters
            ----------
            thickness : float
                Cladding thickness in cm. Defaults to 0.02 in, per Ref. [2]_ pg. 55.
            outer_radius : float
                Cladding outer radius in cm. Defaults to half the 1.35-in diameter, per Ref. [2]_ pg. 55.
            material : Optional[openmc.Material]
                Cladding material. If omitted, ``NETLDefaultMaterials.stainless_steel`` is used at ``temperature``,
                per Ref. [2]_ pg. 52.
            temperature : float
                Temperature in Kelvin used to construct the default material. Defaults to
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE``. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            NETLFuelFollowerControlRod.Cladding
                CoreForge fuel-follower-control-rod cladding.
            """
            material = (material if material is not None else NETLDefaultMaterials.stainless_steel(temperature))

            return NETLFuelFollowerControlRod.Cladding(thickness, outer_radius, Material(material))

        @staticmethod
        def absorber(
            radius: float = 1.3 * 0.5 * CM_PER_INCH,
            length: float = 15.0 * CM_PER_INCH,
            material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLFuelFollowerControlRod.Absorber:
            """Creates and returns the default control-rod absorber.

            Parameters
            ----------
            radius : float
                Absorber radius in cm. Defaults to half the 1.3-in diameter, per Ref. [2]_ pg. 55.
            length : float
                Absorber length in cm. Defaults to 15.0 in, per Ref. [2]_ pg. 58.
            material : Optional[openmc.Material]
                Absorber material. If omitted, ``NETLDefaultMaterials.control_rod_absorber`` is used at
                ``temperature``, per Ref. [2]_ pg. 52.
            temperature : float
                Temperature in Kelvin used to construct the default material. Defaults to
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE``. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            NETLFuelFollowerControlRod.Absorber
                CoreForge fuel-follower-control-rod absorber.
            """
            material = (material if material is not None else NETLDefaultMaterials.control_rod_absorber(temperature))

            return NETLFuelFollowerControlRod.Absorber(radius, length, Material(material))

        @staticmethod
        def fuel_follower(
            length: float = 15.0 * CM_PER_INCH,
            inner_radius: float = 0.25 * 0.5 * CM_PER_INCH,
            outer_radius: float | None = None,
            material: openmc.Material | Sequence[openmc.Material] | None = None,
            num_radial_regions: int = 1,
            num_axial_regions: int = 1,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLFuelFollowerControlRod.FuelFollower:
            """Creates and returns the default fuel follower.

            Parameters
            ----------
            length : float
                Fuel-follower length in cm. Defaults to 15.0 in, per Ref. [2]_ pg. 58.
            inner_radius : float
                Fuel-follower inner radius in cm. Defaults to half the 0.25-in diameter, per Ref. [2]_ pg. 55.
            outer_radius : Optional[float]
                Fuel-follower outer radius in cm. If omitted, the default cladding inner
                radius is used.
            material : Optional[openmc.Material | Sequence[openmc.Material]]
                Fuel material or one material per region in axial-major order. If omitted,
                ``NETLDefaultMaterials.fuel_follower_fuel`` is used at ``temperature``, per Ref. [2]_ pg. 52.
            num_radial_regions : int
                Number of equal-volume radial regions. Defaults to 1.
            num_axial_regions : int
                Number of equal-length axial regions. Defaults to 1.
            temperature : float
                Temperature in Kelvin used to construct the default material. Defaults to
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE``. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            NETLFuelFollowerControlRod.FuelFollower
                CoreForge control-rod fuel follower.
            """
            if outer_radius is None:
                outer_radius = DefaultGeometries.FuelFollowerControlRod.cladding().inner_radius
            material = (material if material is not None else NETLDefaultMaterials.fuel_follower_fuel(temperature))

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
            radius: float = 0.25 * 0.5 * CM_PER_INCH,
            material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLFuelFollowerControlRod.ZrFillRod:
            """Creates and returns the default zirconium fill rod.

            Parameters
            ----------
            radius : float
                Fill-rod radius in cm. Defaults to half the 0.25-in diameter, per Ref. [2]_ pg. 55.
            material : Optional[openmc.Material]
                Fill-rod material. If omitted, ``NETLDefaultMaterials.zirc_filler`` is used at ``temperature``, per
                Ref. [2]_ pg. 52.
            temperature : float
                Temperature in Kelvin used to construct the default material. Defaults to
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE``. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            NETLFuelFollowerControlRod.ZrFillRod
                CoreForge control-rod zirconium fill rod.
            """
            material = material if material is not None else NETLDefaultMaterials.zirc_filler(temperature)

            return NETLFuelFollowerControlRod.ZrFillRod(radius, Material(material))

        @staticmethod
        def upper_element_plug(
            thickness: float = 1.5 * CM_PER_INCH,
            material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLFuelFollowerControlRod.ElementPlug:
            """Creates and returns the default upper element plug.

            Parameters
            ----------
            thickness : float
                Plug thickness in cm. Defaults to 1.5 in, per Ref. [2]_ pg. 58.
            material : Optional[openmc.Material]
                Plug material. If omitted, ``NETLDefaultMaterials.stainless_steel`` is used at ``temperature``, per
                Ref. [2]_ pg. 51.
            temperature : float
                Temperature used for the default material. Defaults to
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE``. This value is ignored when
                ``material`` is supplied.

            Returns
            -------
            NETLFuelFollowerControlRod.ElementPlug
                CoreForge upper element plug.
            """
            material = (material if material is not None else NETLDefaultMaterials.stainless_steel(temperature))
            return NETLFuelFollowerControlRod.ElementPlug(thickness, Material(material))

        @staticmethod
        def upper_air_gap(thickness: float = 3.5 * CM_PER_INCH) -> NETLFuelFollowerControlRod.AirGap:
            """Creates and returns the default upper air gap.

            Parameters
            ----------
            thickness : float
                Air-gap thickness in cm. Defaults to 3.5 in, per Ref. [2]_ pg. 58.

            Returns
            -------
            NETLFuelFollowerControlRod.AirGap
                CoreForge upper air gap.
            """
            return NETLFuelFollowerControlRod.AirGap(thickness)

        @staticmethod
        def upper_magneform_fitting(
            thickness: float = 0.5 * CM_PER_INCH,
            material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLFuelFollowerControlRod.MagneformFitting:
            """Creates and returns the default upper Magneform fitting.

            Parameters
            ----------
            thickness : float
                Fitting thickness in cm. Defaults to 0.5 in, per Ref. [2]_ pg. 58.
            material : Optional[openmc.Material]
                Fitting material. If omitted, ``NETLDefaultMaterials.stainless_steel`` is used at ``temperature``,
                per Ref. [2]_ pg. 51.
            temperature : float
                Temperature used for the default material. Defaults to
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE``. This value is ignored when
                ``material`` is supplied.

            Returns
            -------
            NETLFuelFollowerControlRod.MagneformFitting
                CoreForge upper Magneform fitting.
            """
            material = (material if material is not None else NETLDefaultMaterials.stainless_steel(temperature))
            return NETLFuelFollowerControlRod.MagneformFitting(thickness, Material(material))

        @staticmethod
        def above_absorber_air_gap(thickness: float = 0.125 * CM_PER_INCH) -> NETLFuelFollowerControlRod.AirGap:
            """Creates and returns the default air gap above the absorber.

            Parameters
            ----------
            thickness : float
                Air-gap thickness in cm. Defaults to 0.125 in, per Ref. [2]_ pg. 58.

            Returns
            -------
            NETLFuelFollowerControlRod.AirGap
                CoreForge air gap above the absorber.
            """
            return NETLFuelFollowerControlRod.AirGap(thickness)

        @staticmethod
        def middle_magneform_fitting(
            thickness: float = 0.5 * CM_PER_INCH,
            material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLFuelFollowerControlRod.MagneformFitting:
            """Creates and returns the default middle Magneform fitting.

            Parameters
            ----------
            thickness : float
                Fitting thickness in cm. Defaults to 0.5 in, per Ref. [2]_ pg. 58.
            material : Optional[openmc.Material]
                Fitting material. If omitted, ``NETLDefaultMaterials.stainless_steel`` is used at ``temperature``,
                per Ref. [2]_ pg. 51.
            temperature : float
                Temperature used for the default material. Defaults to
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE``. This value is ignored when
                ``material`` is supplied.

            Returns
            -------
            NETLFuelFollowerControlRod.MagneformFitting
                CoreForge middle Magneform fitting.
            """
            material = (material if material is not None else NETLDefaultMaterials.stainless_steel(temperature))
            return NETLFuelFollowerControlRod.MagneformFitting(thickness, Material(material))

        @staticmethod
        def above_fuel_follower_air_gap(
            thickness: float = 0.25 * CM_PER_INCH,
        ) -> NETLFuelFollowerControlRod.AirGap:
            """Creates and returns the default air gap above the fuel follower.

            Parameters
            ----------
            thickness : float
                Air-gap thickness in cm. Defaults to 0.25 in, per Ref. [2]_ pg. 58.

            Returns
            -------
            NETLFuelFollowerControlRod.AirGap
                CoreForge air gap above the fuel follower.
            """
            return NETLFuelFollowerControlRod.AirGap(thickness)

        @staticmethod
        def lower_magneform_fitting(
            thickness: float = 1.0 * CM_PER_INCH,
            material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLFuelFollowerControlRod.MagneformFitting:
            """Creates and returns the default lower Magneform fitting.

            Parameters
            ----------
            thickness : float
                Fitting thickness in cm. Defaults to 1.0 in, per Ref. [2]_ pg. 58.
            material : Optional[openmc.Material]
                Fitting material. If omitted, ``NETLDefaultMaterials.stainless_steel`` is used at ``temperature``,
                per Ref. [2]_ pg. 51.
            temperature : float
                Temperature used for the default material. Defaults to
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE``. This value is ignored when
                ``material`` is supplied.

            Returns
            -------
            NETLFuelFollowerControlRod.MagneformFitting
                CoreForge lower Magneform fitting.
            """
            material = (material if material is not None else NETLDefaultMaterials.stainless_steel(temperature))
            return NETLFuelFollowerControlRod.MagneformFitting(thickness, Material(material))

        @staticmethod
        def lower_air_gap(thickness: float = 5.375 * CM_PER_INCH) -> NETLFuelFollowerControlRod.AirGap:
            """Creates and returns the default lower air gap.

            Parameters
            ----------
            thickness : float
                Air-gap thickness in cm. Defaults to 5.375 in, per Ref. [2]_ pg. 58.

            Returns
            -------
            NETLFuelFollowerControlRod.AirGap
                CoreForge lower air gap.
            """
            return NETLFuelFollowerControlRod.AirGap(thickness)

        @staticmethod
        def lower_element_plug(
            thickness: float = 0.5 * CM_PER_INCH,
            material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLFuelFollowerControlRod.ElementPlug:
            """Creates and returns the default lower element plug.

            Parameters
            ----------
            thickness : float
                Plug thickness in cm. Defaults to 0.5 in, per Ref. [2]_ pg. 58.
            material : Optional[openmc.Material]
                Plug material. If omitted, ``NETLDefaultMaterials.stainless_steel`` is used at ``temperature``, per
                Ref. [2]_ pg. 51.
            temperature : float
                Temperature used for the default material. Defaults to
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE``. This value is ignored when
                ``material`` is supplied.

            Returns
            -------
            NETLFuelFollowerControlRod.ElementPlug
                CoreForge lower element plug.
            """
            material = (material if material is not None else NETLDefaultMaterials.stainless_steel(temperature))
            return NETLFuelFollowerControlRod.ElementPlug(thickness, Material(material))

        @staticmethod
        def fill_gas(
            material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> Material:
            """Creates and returns the default control-rod fill gas.

            Parameters
            ----------
            material : Optional[openmc.Material]
                Fill-gas material. If omitted, ``NETLDefaultMaterials.air`` is used, per Ref. [2]_ pg. 51.
            temperature : float
                Temperature used for the default material. Defaults to
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE``. This value is ignored when
                ``material`` is supplied.

            Returns
            -------
            Material
                CoreForge fill-gas material.
            """
            material = material if material is not None else NETLDefaultMaterials.air(temperature)
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
            thickness: float = 0.028 * CM_PER_INCH,
            outer_radius: float = 1.25 * 0.5 * CM_PER_INCH,
            material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLTransientRod.Cladding:
            """Creates and returns the default transient-rod cladding.

            Parameters
            ----------
            thickness : float
                Cladding thickness in cm. Defaults to 0.028 in, per Ref. [1]_ Table 4.2.
            outer_radius : float
                Cladding outer radius in cm. Defaults to half the 1.25-in diameter, per Ref. [1]_ Table 4.2.
            material : Optional[openmc.Material]
                Cladding material. If omitted, ``NETLDefaultMaterials.aluminum`` is used at ``temperature``, per
                Ref. [2]_ pg. 51.
            temperature : float
                Temperature in Kelvin used to construct the default material. Defaults to
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE``. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            NETLTransientRod.Cladding
                CoreForge NETL transient-rod cladding.
            """
            material = material if material is not None else NETLDefaultMaterials.aluminum(temperature)

            return NETLTransientRod.Cladding(thickness, outer_radius, Material(material))

        @staticmethod
        def absorber(
            radius: float = 1.187 * 0.5 * CM_PER_INCH,
            length: float = 15.0 * CM_PER_INCH,
            material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLTransientRod.Absorber:
            """Creates and returns the default transient-rod absorber.

            Parameters
            ----------
            radius : float
                Absorber radius in cm. Defaults to half the 1.187-in diameter, per Ref. [2]_ pg. 55.
            length : float
                Absorber length in cm. Defaults to 15.0 in, per Ref. [1]_ Table 4.2.
            material : Optional[openmc.Material]
                Absorber material. If omitted, ``NETLDefaultMaterials.control_rod_absorber`` is used at
                ``temperature``, per Ref. [2]_ pg. 51.
            temperature : float
                Temperature in Kelvin used to construct the default material. Defaults to
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE``. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            NETLTransientRod.Absorber
                CoreForge NETL transient-rod absorber.
            """
            material = (material if material is not None else
                        NETLDefaultMaterials.control_rod_absorber(temperature))

            return NETLTransientRod.Absorber(radius, length, Material(material))

        @staticmethod
        def air_follower(thickness: float = 19.75 * CM_PER_INCH) -> NETLTransientRod.AirFollower:
            """Creates and returns the default transient-rod air follower.

            Parameters
            ----------
            thickness : float
                Air-follower thickness in cm. Defaults to 19.75 in, per Ref. [2]_ pg. 58.

            Returns
            -------
            NETLTransientRod.AirFollower
                CoreForge NETL transient-rod air follower.
            """
            return NETLTransientRod.AirFollower(thickness)

        @staticmethod
        def upper_element_plug(
            thickness: float = 0.5 * CM_PER_INCH,
            material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLTransientRod.ElementPlug:
            """Creates and returns the default upper transient-rod element plug.

            Parameters
            ----------
            thickness : float
                Plug thickness in cm. Defaults to 0.5 in, per Ref. [2]_ pg. 58.
            material : Optional[openmc.Material]
                Plug material. If omitted, ``NETLDefaultMaterials.aluminum`` is used at ``temperature``, per Ref.
                [2]_ pg. 51.
            temperature : float
                Temperature used for the default material. Defaults to
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE``. This value is ignored when
                ``material`` is supplied.

            Returns
            -------
            NETLTransientRod.ElementPlug
                CoreForge upper transient-rod element plug.
            """
            material = material if material is not None else NETLDefaultMaterials.aluminum(temperature)
            return NETLTransientRod.ElementPlug(thickness, Material(material))

        @staticmethod
        def upper_magneform_fitting(
            thickness: float = 1.0 * CM_PER_INCH,
            material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLTransientRod.MagneformFitting:
            """Creates and returns the default upper transient-rod Magneform fitting.

            Parameters
            ----------
            thickness : float
                Fitting thickness in cm. Defaults to 1.0 in, per Ref. [2]_ pg. 58.
            material : Optional[openmc.Material]
                Fitting material. If omitted, ``NETLDefaultMaterials.aluminum`` is used at ``temperature``, per Ref.
                [2]_ pg. 51.
            temperature : float
                Temperature used for the default material. Defaults to
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE``. This value is ignored when
                ``material`` is supplied.

            Returns
            -------
            NETLTransientRod.MagneformFitting
                CoreForge upper transient-rod Magneform fitting.
            """
            material = material if material is not None else NETLDefaultMaterials.aluminum(temperature)
            return NETLTransientRod.MagneformFitting(thickness, Material(material))

        @staticmethod
        def lower_magneform_fitting(
            thickness: float = 1.0 * CM_PER_INCH,
            material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLTransientRod.MagneformFitting:
            """Creates and returns the default lower transient-rod Magneform fitting.

            Parameters
            ----------
            thickness : float
                Fitting thickness in cm. Defaults to 1.0 in, per Ref. [2]_ pg. 58.
            material : Optional[openmc.Material]
                Fitting material. If omitted, ``NETLDefaultMaterials.aluminum`` is used at ``temperature``, per Ref.
                [2]_ pg. 51.
            temperature : float
                Temperature used for the default material. Defaults to
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE``. This value is ignored when
                ``material`` is supplied.

            Returns
            -------
            NETLTransientRod.MagneformFitting
                CoreForge lower transient-rod Magneform fitting.
            """
            material = material if material is not None else NETLDefaultMaterials.aluminum(temperature)
            return NETLTransientRod.MagneformFitting(thickness, Material(material))

        @staticmethod
        def lower_element_plug(
            thickness: float = 0.5 * CM_PER_INCH,
            material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLTransientRod.ElementPlug:
            """Creates and returns the default lower transient-rod element plug.

            Parameters
            ----------
            thickness : float
                Plug thickness in cm. Defaults to 0.5 in, per Ref. [2]_ pg. 58.
            material : Optional[openmc.Material]
                Plug material. If omitted, ``NETLDefaultMaterials.aluminum`` is used at ``temperature``, per Ref.
                [2]_ pg. 51.
            temperature : float
                Temperature used for the default material. Defaults to
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE``. This value is ignored when
                ``material`` is supplied.

            Returns
            -------
            NETLTransientRod.ElementPlug
                CoreForge lower transient-rod element plug.
            """
            material = material if material is not None else NETLDefaultMaterials.aluminum(temperature)
            return NETLTransientRod.ElementPlug(thickness, Material(material))

        @staticmethod
        def fill_gas(
            material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> Material:
            """Creates and returns the default transient-rod fill gas.

            Parameters
            ----------
            material : Optional[openmc.Material]
                Fill-gas material. If omitted, ``NETLDefaultMaterials.air`` is used, per Ref. [2]_ pg. 51.
            temperature : float
                Temperature used for the default material. Defaults to
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE``. This value is ignored when
                ``material`` is supplied.

            Returns
            -------
            Material
                CoreForge fill-gas material.
            """
            material = material if material is not None else NETLDefaultMaterials.air(temperature)
            return Material(material)

    @staticmethod
    def upper_grid_plate(
        temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        fuel_location_radius: float = 1.505 * 0.5 * CM_PER_INCH,
        control_rod_location_radius: float = 1.505 * 0.5 * CM_PER_INCH,
        pnt_location_radius: float = 1.505 * 0.5 * CM_PER_INCH,
        central_thimble_radius: float | None = None,
        penetration_map: PenetrationMap | None = None,
        thickness: float = 0.62 * CM_PER_INCH,
        material: openmc.Material | None = None,
        three_element_location_radius: float | None = THREE_ELEMENT_PENETRATION_RADIUS,
        core: Core | None = None,
    ) -> GridPlate:
        """Creates and returns the default upper grid plate geometry.

        Parameters
        ----------
        temperature : float
            Temperature applied to the default upper-grid-plate material.
        fuel_location_radius : float
            Fuel-location penetration radius in cm. Defaults to half the 1.505-in diameter, per Ref. [1]_
            Section 4.2.4.a. Ignored when ``penetration_map`` is supplied.
        control_rod_location_radius : float
            Control-rod-location penetration radius in cm. Defaults to half the 1.505-in diameter, per Ref. [1]_
            Section 4.2.4.a. Ignored when ``penetration_map`` is supplied.
        pnt_location_radius : float
            PNT-location (G-34) penetration radius in cm. Defaults to half the
            1.505-in diameter, per Ref. [2]_ pages 53 and 55. Ignored when
            ``penetration_map`` is supplied.
        central_thimble_radius : Optional[float]
            Central-thimble penetration radius in cm. If omitted, the default central
            thimble outer radius is used. Ignored when ``penetration_map`` is supplied.
        penetration_map : Optional[PenetrationMap]
            Complete map of core locations to lists of ``(radius, x_offset,
            y_offset)`` openings [cm]. An empty list describes solid plate.
            If omitted, the standard map is generated from the radius parameters.
        thickness : float
            Grid-plate thickness in cm. Defaults to 0.62 in, per Ref. [2]_ pg. 55.
        material : Optional[openmc.Material]
            Grid-plate material. If omitted, ``NETLDefaultMaterials.aluminum`` is used at ``temperature``, per
            Ref. [2]_ pg. 50. The temperature is ignored when a material is supplied.
        three_element_location_radius : Optional[float]
            Radius of the shared three-element opening [cm]. Defaults to
            2.40000 cm, per Ref. [3]_ pages 152 and 217. ``None`` disables it.
            No shared opening is added when the core has no irradiator.
            Ignored when ``penetration_map`` is supplied.
        core : Optional[Core]
            Core whose lattice and facility center determine the shared opening's
            offsets. If omitted and a three-element radius is supplied, the
            default core is used. Ignored when ``penetration_map`` is supplied.

        Returns
        -------
        GridPlate
            Default NETL TRIGA upper grid plate.
        """
        material = material if material is not None else NETLDefaultMaterials.aluminum(temperature)
        if penetration_map is None:
            if three_element_location_radius is not None and core is None:
                core = DefaultGeometries.core(non_fuel_temp=temperature)
            central_thimble_radius = (
                central_thimble_radius if central_thimble_radius is not None else
                DefaultGeometries.central_thimble().cladding.outer_radius
            )
            penetration_map = grid_plate_penetration_map(
                fuel_location_radius=fuel_location_radius,
                control_rod_location_radius=control_rod_location_radius,
                central_thimble_radius=central_thimble_radius,
                pnt_location_radius=pnt_location_radius,
                three_element_location_radius=three_element_location_radius,
                core=core,
            )

        return GridPlate(
            penetration_map=penetration_map,
            thickness=thickness,
            material=Material(material),
            name="upper_grid_plate",
        )

    @staticmethod
    def lower_grid_plate(
        temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        fuel_location_radius: float = 1.25 * 0.5 * CM_PER_INCH,
        control_rod_location_radius: float = 1.505 * 0.5 * CM_PER_INCH,
        pnt_location_radius: float = 1.505 * 0.5 * CM_PER_INCH,
        central_thimble_radius: float | None = None,
        penetration_map: PenetrationMap | None = None,
        thickness: float = 1.25 * CM_PER_INCH,
        material: openmc.Material | None = None,
    ) -> GridPlate:
        """Creates and returns the default lower grid plate geometry.

        Parameters
        ----------
        temperature : float
            Temperature applied to the default lower-grid-plate material.
        fuel_location_radius : float
            Fuel-location penetration radius in cm. Defaults to half the 1.25-in diameter, per Ref. [1]_ Section
            4.2.4.b. Ignored when ``penetration_map`` is supplied.
        control_rod_location_radius : float
            Control-rod-location penetration radius in cm. Defaults to half the 1.505-in diameter, per Ref. [1]_
            Section 4.2.4.b. Ignored when ``penetration_map`` is supplied.
        pnt_location_radius : float
            PNT-location (G-34) penetration radius in cm. Defaults to half the
            1.505-in diameter, per Ref. [2]_ pages 53 and 55. Ignored when
            ``penetration_map`` is supplied.
        central_thimble_radius : Optional[float]
            Central-thimble penetration radius in cm. If omitted, the default central
            thimble outer radius is used. Ignored when ``penetration_map`` is supplied.
        penetration_map : Optional[PenetrationMap]
            Complete map of core locations to lists of ``(radius, x_offset,
            y_offset)`` openings [cm]. An empty list describes solid plate.
            If omitted, the standard map is generated from the radius parameters.
        thickness : float
            Grid-plate thickness in cm. Defaults to 1.25 in, per Ref. [2]_ pg. 55.
        material : Optional[openmc.Material]
            Grid-plate material. If omitted, ``NETLDefaultMaterials.aluminum`` is used at ``temperature``, per
            Ref. [2]_ pg. 50. The temperature is ignored when a material is supplied.

        Returns
        -------
        GridPlate
            Default NETL TRIGA lower grid plate.
        """

        if penetration_map is None:
            central_thimble_radius = (
                central_thimble_radius if central_thimble_radius is not None else
                DefaultGeometries.central_thimble().cladding.outer_radius
            )
            penetration_map = grid_plate_penetration_map(
                fuel_location_radius=fuel_location_radius,
                control_rod_location_radius=control_rod_location_radius,
                central_thimble_radius=central_thimble_radius,
                pnt_location_radius=pnt_location_radius,
            )

        material = material if material is not None else NETLDefaultMaterials.aluminum(temperature)

        return GridPlate(
            penetration_map=penetration_map,
            thickness=thickness,
            material=Material(material),
            name="lower_grid_plate",
        )


    @staticmethod
    def pool(
        coolant: openmc.Material | None = None,
        radius: float = 90.0,
        height: float = 160.0,
    ) -> Pool:
        """Creates and returns the default pool.

        Parameters
        ----------
        coolant : Optional[openmc.Material]
            Coolant material used for the pool contents. If omitted, water is used,
            per Ref. [2]_ pg. 48.
        radius : float
            Pool radius in cm. Defaults to 90.0 cm, per Ref. [2]_ pg. 54.
        height : float
            Pool height in cm. Defaults to 160.0 cm, per Ref. [2]_ pg. 54.

        Returns
        -------
        Pool
            Default NETL TRIGA pool.
        """
        coolant = coolant or NETLDefaultMaterials.water()

        return Pool(
            radius=radius,
            height=height,
            material=Material(coolant),
            name="pool",
        )

    @staticmethod
    def reflector(
        temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        radius: float = 42.0 * 0.5 * CM_PER_INCH,
        height: float = 23.13 * CM_PER_INCH,
        material: openmc.Material | None = None,
    ) -> Reflector:
        """Creates and returns the default reflector.

        Parameters
        ----------
        temperature : float
            Temperature applied to the default reflector material.
        radius : float
            Reflector radius in cm. Defaults to half the 42.0-in diameter, per Ref. [2]_ pg. 54.
        height : float
            Reflector height in cm. Defaults to 23.13 in, per Ref. [2]_ pg. 55.
        material : Optional[openmc.Material]
            Reflector material. If omitted, ``NETLDefaultMaterials.graphite`` is used at ``temperature``, per
            Ref. [2]_ pg. 48. The temperature is ignored when a material is supplied.

        Returns
        -------
        Reflector
            Default NETL TRIGA reflector.
        """
        material = material if material is not None else NETLDefaultMaterials.graphite(temperature)

        return Reflector(
            radius=radius,
            height=height,
            material=Material(material),
            name="reflector",
        )

    @staticmethod
    def shroud(
        temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        thickness: float = 0.1875 * CM_PER_INCH,
        primary_hex_inner_radius: float = 10.21875 * CM_PER_INCH,
        rotated_hex_inner_radius: float = 10.75 * CM_PER_INCH,
        material: openmc.Material | None = None,
    ) -> Shroud:
        """Creates and returns the default shroud.

        Parameters
        ----------
        temperature : float
            Temperature applied to the default shroud material.
        thickness : float
            Shroud-wall thickness in cm. Defaults to 0.1875 in, per Ref. [2]_ pg. 54 & 55.
        primary_hex_inner_radius : float
            Primary-hex inradius in cm. Defaults to 10.21875 in, per Ref. [2]_ pg. 55.
        rotated_hex_inner_radius : float
            Rotated-hex inradius in cm. Defaults to 10.75 in, per Ref. [2]_ pg. 54.
        material : Optional[openmc.Material]
            Shroud material. If omitted, ``NETLDefaultMaterials.aluminum`` is used at ``temperature``, per Ref.
            [2]_ pg. 48. The temperature is ignored when a material is supplied.

        Returns
        -------
        Shroud
            Default NETL TRIGA shroud.
        """
        material = material if material is not None else NETLDefaultMaterials.aluminum(temperature)

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
        outer_radius: float = 28.625 * 0.5 * CM_PER_INCH,
        height: float = 10.8174 * CM_PER_INCH,
        number_of_tubes: int = 40,
        tube_to_center_distance: float = 26.312 * 0.5 * CM_PER_INCH,
        tube_specs: NETLRSRCavity.SpecimenTube | None = None,
        material: openmc.Material | None = None,
    ) -> NETLRSRCavity:
        """Creates and returns the default rotary specimen rack cavity.

        Parameters
        ----------
        temperature : float
            Temperature applied to default specimen-tube and cavity-fill materials.
        outer_radius : float
            RSR cavity outer radius in cm. Defaults to half the 28.625-in diameter, per Ref. [2]_ pg. 55.
        height : float
            RSR cavity height in cm. Defaults to 10.8174 in, per Ref. [2]_ pg. 55.
        number_of_tubes : int
            Number of specimen tubes. Defaults to 40, per Ref. [1]_ pg. 10-27.
        tube_to_center_distance : float
            Distance from the rack center to each tube centerline in cm. Defaults to half the 26.312-in
            diameter, per Ref. [1]_ pg. 10-27.
        tube_specs : Optional[NETLRSRCavity.SpecimenTube]
            Specimen-tube override. If omitted,
            ``DefaultGeometries.RSRCavity.specimen_tube`` is used.
        material : Optional[openmc.Material]
            Cavity fill material. If omitted, ``NETLDefaultMaterials.air`` is used at ``temperature``, per Ref.
            [2]_ pg. 48. The temperature is ignored when a material is supplied.

        Returns
        -------
        NETLRSRCavity
            Default NETL TRIGA rotary specimen rack cavity.
        """
        tube_specs = (tube_specs if tube_specs is not None else
                      DefaultGeometries.RSRCavity.specimen_tube(temperature=temperature))
        material = material if material is not None else NETLDefaultMaterials.air(temperature)

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
            outer_radius: float = 1.0 * 0.5 * CM_PER_INCH,
            thickness: float = 0.058 * CM_PER_INCH,
            material: openmc.Material | None = None,
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        ) -> NETLRSRCavity.SpecimenTube:
            """Creates and returns the default RSR specimen tube.

            Parameters
            ----------
            outer_radius : float
                Specimen-tube outer radius in cm. Defaults to half the 1.0-in diameter, per Ref. [2]_ pg. 56 & 57.
            thickness : float
                Specimen-tube wall thickness in cm. Defaults to 0.058 in, per Ref. [1]_ pg. 10-27.
            material : Optional[openmc.Material]
                Tube material. If omitted, ``NETLDefaultMaterials.aluminum`` is assumed at ``temperature``.
            temperature : float
                Temperature in Kelvin used to construct the default material. Defaults to
                ``NETLDefaultMaterials.DEFAULT_TEMPERATURE``. This value is ignored
                when ``material`` is supplied.

            Returns
            -------
            NETLRSRCavity.SpecimenTube
                CoreForge NETL RSR specimen tube.
            """
            material = material if material is not None else NETLDefaultMaterials.aluminum(temperature)

            return NETLRSRCavity.SpecimenTube(outer_radius, thickness, Material(material))

    @staticmethod
    def beam_port(
        temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
        length: float | None = None,
        inner_radius: float = 6.065 * 0.5 * CM_PER_INCH,
        outer_radius: float = 6.625 * 0.5 * CM_PER_INCH,
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
        inner_radius : float
            Beam port inner radius in cm. Defaults to half the 6.065-in diameter, per Ref. [2]_ Figures 4 & 5.
        outer_radius : float
            Beam port outer radius in cm. Defaults to half the 6.625-in diameter, per Ref. [2]_ Figures 4 & 5.
        tube_material : Optional[openmc.Material]
            Beam port tube material. If omitted, ``NETLDefaultMaterials.aluminum`` is used at ``temperature``,
            per Ref. [2]_ pg. 48.
        fill_material : Optional[openmc.Material]
            Beam port fill material. If omitted, ``NETLDefaultMaterials.air`` is used at ``temperature``, per
            Ref. [2]_ pg. 48.

        Returns
        -------
        BeamPort
            Default NETL TRIGA beam port.
        """

        length = length if length is not None else DefaultGeometries.pool().radius * 2.0
        tube_material = (tube_material if tube_material is not None else
                         NETLDefaultMaterials.aluminum(temperature))
        fill_material = (fill_material if fill_material is not None else
                         NETLDefaultMaterials.air(temperature))

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
        pitch: float = 1.714 * CM_PER_INCH,
        central_thimble: CentralThimble | None = None,
        transient_rod: NETLTransientRod | None = None,
        regulating_rod: NETLFuelFollowerControlRod | None = None,
        shim_1_rod: NETLFuelFollowerControlRod | None = None,
        shim_2_rod: NETLFuelFollowerControlRod | None = None,
        loading: dict[str, Core.Loadable | None] | None = None,
        fill_material: Material | None = None,
        pnt: NETLPNT | None = None,
        three_element_irradiator: Core.Irradiator | None = None,
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
        pitch : float
            Hexagonal lattice pitch in cm. Defaults to 1.714 in, per Ref. [2]_ pg. 54.
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
        pnt : Optional[NETLPNT]
            PNT placed at G-34. If omitted, the default unlined PNT is used. Ignored
            when ``loading`` is supplied.
        three_element_irradiator : Optional[Core.Irradiator]
            Conventional or modified irradiator, or a custom ``PinCellStack``,
            spanning E-11, F-13, and F-14. If omitted, the detailed modified
            irradiator is built using ``non_fuel_temp`` and ``coolant``.

        Returns
        -------
        Core
            Default NETL TRIGA core geometry.
        """
        coolant = coolant or NETLDefaultMaterials.water()

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

        if three_element_irradiator is None:
            three_element_irradiator = DefaultGeometries.modified_three_element_irradiator(
                temperature=non_fuel_temp,
                coolant=coolant,
            )

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

            pnt = pnt if pnt is not None else DefaultGeometries.pnt(
                non_fuel_temp,
                coolant,
            )

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
                                     "G-20", "G-21", "G-22", "G-23",
                                     "G-26", "G-27", "G-28", "G-29", "G-30",
                                             "G-33", "G-35", "G-36"], fuel)
            loading["G-32"] = source_holder()
            loading["G-34"] = pnt
            loading["G-24"] = None

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
            three_element_irradiator=three_element_irradiator,
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
        beam_port_1_5: NETLReactor.BeamPort | None = None,
        beam_port_2: NETLReactor.BeamPort | None = None,
        beam_port_3: NETLReactor.BeamPort | None = None,
        beam_port_4: NETLReactor.BeamPort | None = None,
        reflector: NETLReactor.Reflector | None = None,
        upper_grid_plate: NETLReactor.GridPlate | None = None,
        lower_grid_plate: NETLReactor.GridPlate | None = None,
        pnt: NETLPNT | None = None,
        three_element_irradiator: Core.Irradiator | None = None,
    ) -> NETLReactor:
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
        beam_port_1_5 : Optional[NETLReactor.BeamPort]
            Shared beam-port 1/5 geometry and placement override. If omitted, the
            reference geometry and placement are used.
        beam_port_2 : Optional[NETLReactor.BeamPort]
            Beam-port 2 geometry and placement override. If omitted, the reference
            geometry and placement are used.
        beam_port_3 : Optional[NETLReactor.BeamPort]
            Beam-port 3 geometry and placement override. If omitted, the reference
            geometry and placement are used.
        beam_port_4 : Optional[NETLReactor.BeamPort]
            Beam-port 4 geometry and placement override. If omitted, the reference
            geometry and placement are used.
        reflector : Optional[NETLReactor.Reflector]
            Reflector geometry and placement override. If omitted, the reference
            geometry and placement are used.
        upper_grid_plate : Optional[NETLReactor.GridPlate]
            Upper-grid-plate geometry and placement override. If omitted, the
            reference geometry and placement are used.
        lower_grid_plate : Optional[NETLReactor.GridPlate]
            Lower-grid-plate geometry and placement override. If omitted, the
            reference geometry and placement are used.
        pnt : Optional[NETLPNT]
            PNT placed at G-34 when constructing the default core. If omitted,
            the default unlined PNT extends from the supplied lower grid plate's
            bottom to the pool top. Ignored when ``core`` is supplied.
        three_element_irradiator : Optional[Core.Irradiator]
            Conventional or modified irradiator, or a custom ``PinCellStack``,
            spanning E-11, F-13, and F-14 when constructing the default core.
            If omitted, the detailed modified irradiator is built using
            ``non_fuel_temp`` and ``coolant``. Ignored when ``core`` is supplied.

        Returns
        -------
        NETLReactor
            Default NETL TRIGA reactor geometry.
        """
        coolant = coolant or NETLDefaultMaterials.water()

        pool = pool if pool is not None else DefaultGeometries.pool(coolant)
        shroud = shroud if shroud is not None else DefaultGeometries.shroud(non_fuel_temp)
        rsr_cavity = (rsr_cavity if rsr_cavity is not None else
                      DefaultGeometries.rsr_cavity(non_fuel_temp))
        lower_grid_plate = (lower_grid_plate if lower_grid_plate is not None else
                            DefaultGeometries.Reactor.lower_grid_plate(non_fuel_temp))
        if core is None:
            if pnt is None:
                pnt_bottom = (
                    -lower_grid_plate.top_to_core_centerline_distance
                    - lower_grid_plate.geometry.thickness
                )
                pnt_terminus = DefaultGeometries.PNT.unlined_terminus(
                    temperature=non_fuel_temp,
                    outer_material=coolant,
                )
                pnt_tube = DefaultGeometries.PNT.tube(
                    length=(
                        0.5 * pool.height
                        - pnt_bottom
                        - pnt_terminus.length
                    ),
                    temperature=non_fuel_temp,
                )
                pnt = DefaultGeometries.pnt(
                    non_fuel_temp,
                    coolant,
                    bottom_pos=pnt_bottom,
                    terminus=pnt_terminus,
                    tube=pnt_tube,
                )
            core = DefaultGeometries.core(
                fuel_temp,
                non_fuel_temp,
                coolant,
                fuel_materials=fuel_materials,
                pnt=pnt,
                three_element_irradiator=three_element_irradiator,
            )

        if any(beam_port is None for beam_port in
               (beam_port_1_5, beam_port_2, beam_port_3, beam_port_4)):
            beam_port_geometry = DefaultGeometries.beam_port(non_fuel_temp)

            beam_port_1_5 = (beam_port_1_5 if beam_port_1_5 is not None else
                             DefaultGeometries.Reactor.beam_port_1_5(geometry=beam_port_geometry))
            beam_port_2 = (beam_port_2 if beam_port_2 is not None else
                           DefaultGeometries.Reactor.beam_port_2(geometry=beam_port_geometry))
            beam_port_3 = (beam_port_3 if beam_port_3 is not None else
                           DefaultGeometries.Reactor.beam_port_3(geometry=beam_port_geometry))
            beam_port_4 = (beam_port_4 if beam_port_4 is not None else
                           DefaultGeometries.Reactor.beam_port_4(geometry=beam_port_geometry))

        reflector = (reflector if reflector is not None else
                     DefaultGeometries.Reactor.reflector(non_fuel_temp))
        if upper_grid_plate is None:
            upper_geometry = DefaultGeometries.upper_grid_plate(
                non_fuel_temp,
                core=core,
            )
            upper_grid_plate = DefaultGeometries.Reactor.upper_grid_plate(
                non_fuel_temp, geometry=upper_geometry,
            )

        return NETLReactor(
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


    class Reactor:
        """Namespace for default reactor-context component placements."""

        @staticmethod
        def beam_port_1_5(
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
            geometry: BeamPort | None = None,
            translation: tuple[float, float, float] = (35.2425, 0.0, -6.985),
            rotation: float = 90.0,
        ) -> NETLReactor.BeamPort:
            """Creates and returns the default shared beam-port 1/5 placement.

            Parameters
            ----------
            temperature : float
                Temperature applied when constructing the default beam-port geometry.
                Ignored when ``geometry`` is supplied.
            geometry : Optional[BeamPort]
                Beam-port geometry override. If omitted,
                ``DefaultGeometries.beam_port`` is used.
            translation : tuple[float, float, float]
                XYZ translation in cm. Defaults to the reference beam-port 1/5
                placement per Ref. [1]_ page 4-24 & Ref. [2]_ pages 48, 56, 59.
            rotation : float
                Rotation about the +z axis in degrees. Defaults to 90 degrees.

            Returns
            -------
            NETLReactor.BeamPort
                Default beam-port 1/5 geometry and placement.
            """
            geometry = (geometry if geometry is not None else
                        DefaultGeometries.beam_port(temperature))
            return NETLReactor.BeamPort(
                geometry=geometry,
                translation=translation,
                rotation=rotation,
            )

        @staticmethod
        def beam_port_2(
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
            geometry: BeamPort | None = None,
            translation: tuple[float, float, float] | None = None,
            rotation: float = 150.0,
        ) -> NETLReactor.BeamPort:
            """Creates and returns the default beam-port 2 placement.

            Parameters
            ----------
            temperature : float
                Temperature applied when constructing the default beam-port geometry.
                Ignored when ``geometry`` is supplied.
            geometry : Optional[BeamPort]
                Beam-port geometry override. If omitted,
                ``DefaultGeometries.beam_port`` is used.
            translation : Optional[tuple[float, float, float]]
                XYZ translation in cm. If omitted, the reference beam-port 2
                placement per Ref. [1]_ page 4-24 & Ref. [2]_ pages 48, 56, 59.
            rotation : float
                Rotation about the +z axis in degrees. Defaults to 150 degrees.

            Returns
            -------
            NETLReactor.BeamPort
                Default beam-port 2 geometry and placement.
            """
            geometry = (geometry if geometry is not None else
                        DefaultGeometries.beam_port(temperature))
            translation = (translation if translation is not None else
                           (
                               6.222 + cosd(150.0) * geometry.length * 0.5,
                               35.255 + sind(150.0) * geometry.length * 0.5,
                               -6.985,
                           ))
            return NETLReactor.BeamPort(
                geometry=geometry,
                translation=translation,
                rotation=rotation,
            )

        @staticmethod
        def beam_port_3(
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
            geometry: BeamPort | None = None,
            translation: tuple[float, float, float] | None = None,
            rotation: float = 0.0,
        ) -> NETLReactor.BeamPort:
            """Creates and returns the default beam-port 3 placement.

            Parameters
            ----------
            temperature : float
                Temperature applied when constructing the default beam-port geometry.
                Ignored when ``geometry`` is supplied.
            geometry : Optional[BeamPort]
                Beam-port geometry override. If omitted,
                ``DefaultGeometries.beam_port`` is used.
            translation : Optional[tuple[float, float, float]]
                XYZ translation in cm. If omitted, the reference beam-port 3
                placement per Ref. [1]_ page 4-24 & Ref. [2]_ pages 48, 56, 59.
            rotation : float
                Rotation about the +z axis in degrees. Defaults to zero degrees.

            Returns
            -------
            NETLReactor.BeamPort
                Default beam-port 3 geometry and placement.
            """
            geometry = (geometry if geometry is not None else
                        DefaultGeometries.beam_port(temperature))
            translation = (translation if translation is not None else
                           (-geometry.length * 0.5 - 26.43188, 0.0, -6.985))
            return NETLReactor.BeamPort(
                geometry=geometry,
                translation=translation,
                rotation=rotation,
            )

        @staticmethod
        def beam_port_4(
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
            geometry: BeamPort | None = None,
            translation: tuple[float, float, float] | None = None,
            rotation: float = 60.0,
        ) -> NETLReactor.BeamPort:
            """Creates and returns the default beam-port 4 placement.

            Parameters
            ----------
            temperature : float
                Temperature applied when constructing the default beam-port geometry.
                Ignored when ``geometry`` is supplied.
            geometry : Optional[BeamPort]
                Beam-port geometry override. If omitted,
                ``DefaultGeometries.beam_port`` is used.
            translation : Optional[tuple[float, float, float]]
                XYZ translation in cm. If omitted, the reference beam-port 4
                placement per Ref. [1]_ page 4-24 & Ref. [2]_ pages 48, 56, 59.
            rotation : float
                Rotation about the +z axis in degrees. Defaults to 60 degrees.

            Returns
            -------
            NETLReactor.BeamPort
                Default beam-port 4 geometry and placement.
            """
            geometry = (geometry if geometry is not None else
                        DefaultGeometries.beam_port(temperature))
            translation = (translation if translation is not None else
                           (
                               -13.216 - cosd(60.0) * geometry.length * 0.5,
                               -22.871 - sind(60.0) * geometry.length * 0.5,
                               -6.985,
                           ))
            return NETLReactor.BeamPort(
                geometry=geometry,
                translation=translation,
                rotation=rotation,
            )

        @staticmethod
        def reflector(
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
            geometry: Reflector | None = None,
            core_centerline_offset: float = 0.565 * CM_PER_INCH,
        ) -> NETLReactor.Reflector:
            """Creates and returns the default reflector placement.

            Parameters
            ----------
            temperature : float
                Temperature applied when constructing the default reflector geometry.
                Ignored when ``geometry`` is supplied.
            geometry : Optional[Reflector]
                Reflector geometry override. If omitted,
                ``DefaultGeometries.reflector`` is used.
            core_centerline_offset : float
                Axial offset of the reflector centerline from the core centerline
                in cm. Defaults to 0.565 in, per Ref. [2]_ pg. 55.

            Returns
            -------
            NETLReactor.Reflector
                Default reflector geometry and placement.
            """
            geometry = (geometry if geometry is not None else
                        DefaultGeometries.reflector(temperature))
            return NETLReactor.Reflector(
                geometry=geometry,
                core_centerline_offset=core_centerline_offset,
            )

        @staticmethod
        def upper_grid_plate(
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
            geometry: GridPlate | None = None,
            top_to_core_centerline_distance: float | None = None,
        ) -> NETLReactor.GridPlate:
            """Creates and returns the default upper-grid-plate placement.

            Parameters
            ----------
            temperature : float
                Temperature applied when constructing the default grid-plate
                geometry. Ignored when ``geometry`` is supplied.
            geometry : Optional[GridPlate]
                Upper-grid-plate geometry override. If omitted,
                ``DefaultGeometries.upper_grid_plate`` is used.
            top_to_core_centerline_distance : Optional[float]
                Distance from the core centerline to the plate's top surface in
                cm. If omitted,
                ``DefaultGeometries.UPPER_GRID_PLATE_TOP_TO_CORE_CENTERLINE_DISTANCE``
                is used.

            Returns
            -------
            NETLReactor.GridPlate
                Default upper-grid-plate geometry and placement.
            """
            geometry = (geometry if geometry is not None else
                        DefaultGeometries.upper_grid_plate(temperature))
            top_to_core_centerline_distance = (
                top_to_core_centerline_distance
                if top_to_core_centerline_distance is not None
                else DefaultGeometries.UPPER_GRID_PLATE_TOP_TO_CORE_CENTERLINE_DISTANCE
            )
            return NETLReactor.GridPlate(
                geometry=geometry,
                top_to_core_centerline_distance=top_to_core_centerline_distance,
            )

        @staticmethod
        def lower_grid_plate(
            temperature: float = NETLDefaultMaterials.DEFAULT_TEMPERATURE,
            geometry: GridPlate | None = None,
            top_to_core_centerline_distance: float | None = None,
        ) -> NETLReactor.GridPlate:
            """Creates and returns the default lower-grid-plate placement.

            Parameters
            ----------
            temperature : float
                Temperature applied when constructing the default grid-plate
                geometry. Ignored when ``geometry`` is supplied.
            geometry : Optional[GridPlate]
                Lower-grid-plate geometry override. If omitted,
                ``DefaultGeometries.lower_grid_plate`` is used.
            top_to_core_centerline_distance : Optional[float]
                Magnitude of the distance from the core centerline to the plate's
                top surface in cm. If omitted,
                ``DefaultGeometries.LOWER_GRID_PLATE_TOP_TO_CORE_CENTERLINE_DISTANCE``
                is used.

            Returns
            -------
            NETLReactor.GridPlate
                Default lower-grid-plate geometry and placement.
            """
            geometry = (geometry if geometry is not None else
                        DefaultGeometries.lower_grid_plate(temperature))
            top_to_core_centerline_distance = (
                top_to_core_centerline_distance
                if top_to_core_centerline_distance is not None
                else DefaultGeometries.LOWER_GRID_PLATE_TOP_TO_CORE_CENTERLINE_DISTANCE
            )
            return NETLReactor.GridPlate(
                geometry=geometry,
                top_to_core_centerline_distance=top_to_core_centerline_distance,
            )
