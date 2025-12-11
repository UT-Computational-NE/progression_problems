from __future__ import annotations

from coreforge.geometry_elements.triga.netl import (CentralThimble,
                                                    SourceHolder,
                                                    FuelFollowerControlRod,
                                                    TransientRod,
                                                    GridPlate,
                                                    Pool)
from coreforge.materials import Material
from progression_problems.TRIGA.default_materials import DefaultMaterials as TRIGADefaultMaterials
from progression_problems.TRIGA.NETL.default_materials import DefaultMaterials as NETLDefaultMaterials
from progression_problems.constants import CM_PER_INCH


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

    UPPER_GRID_PLATE_DISTANCE_FROM_CORE_CENTERLINE =  12.75 * CM_PER_INCH  # Ref. [2]_ pg. 55
    LOWER_GRID_PLATE_DISTANCE_FROM_CORE_CENTERLINE =  13.06 * CM_PER_INCH  # Ref. [2]_ pg. 55

    @staticmethod
    def central_thimble() -> CentralThimble:
        """Creates and returns the default central thimble.

        Returns
        -------
        CentralThimble
            Default NETL TRIGA central thimble.
        """
        cladding = CentralThimble.Cladding(
            thickness    = (1.5 * 0.5 * CM_PER_INCH) - (1.33 * 0.5 * CM_PER_INCH),  # Ref. [1]_ Section 10.2.1.b
            outer_radius = 1.5 * 0.5 * CM_PER_INCH,                                 # Ref. [1]_ Section 10.2.1.b
            material     = Material(NETLDefaultMaterials.aluminum()),               # Ref. [2]_ pg. 51
        )

        pool = DefaultGeometries.pool()

        return CentralThimble(
            cladding       = cladding,
            length         = pool.height,                                           # Pool height
            fill_material  = Material(NETLDefaultMaterials.water()),                # Filled with coolant
            outer_material = Material(NETLDefaultMaterials.water()),                # Coolant exterior
            name           = "central_thimble",
        )

    @staticmethod
    def source_holder() -> SourceHolder:
        """Creates and returns the default source holder.

        Returns
        -------
        SourceHolder
            Default NETL TRIGA source holder.
        """
        upper_plate = DefaultGeometries.upper_grid_plate()

        upper_grid_plate_distance  = DefaultGeometries.UPPER_GRID_PLATE_DISTANCE_FROM_CORE_CENTERLINE
        lower_grid_plate_distance  = DefaultGeometries.LOWER_GRID_PLATE_DISTANCE_FROM_CORE_CENTERLINE
        distance_from_lower_plate  = 1.1934  # Ref. [2]_ pg. 55

        length = (upper_grid_plate_distance + lower_grid_plate_distance -
                  distance_from_lower_plate + upper_plate.thickness)

        # Set such that the cavity center is at core centerline Ref. [2]_ pg. 55
        axial_offset = -distance_from_lower_plate

        cavity = SourceHolder.Cavity(
            radius       = 0.981 * 0.5 * CM_PER_INCH,                        # Ref. [1]_ Section 4.2.5
            length       = 3.0 * CM_PER_INCH,                                # Ref. [1]_ Section 4.2.5
            axial_offset = axial_offset,
            material     = Material(NETLDefaultMaterials.air()),             # Ref. [2]_ pg. 54
        )

        cladding = SourceHolder.Cladding(
            outer_radius = 1.435 * 0.5 * CM_PER_INCH,                        # Ref. [2]_ pg. 54 & 55
            material     = Material(NETLDefaultMaterials.aluminum()),        # Ref. [2]_ pg. 54
        )

        return SourceHolder(
            length         = length,
            cavity         = cavity,
            cladding       = cladding,
            outer_material = Material(NETLDefaultMaterials.water()),         # Coolant exterior
            gap_tolerance  = None,
            name           = "source_holder",
        )

    @staticmethod
    def fuel_follower_control_rod() -> FuelFollowerControlRod:
        """Creates and returns the default fuel follower control rod.

        Returns
        -------
        FuelFollowerControlRod
            Default NETL TRIGA fuel follower control rod.
        """
        cladding = FuelFollowerControlRod.Cladding(
            outer_radius = 1.35 * 0.5 * CM_PER_INCH,                                               # Ref. [2]_ pg. 55
            thickness    = 0.02 * CM_PER_INCH,                                                     # Ref. [2]_ pg. 55
            material     = Material(NETLDefaultMaterials.stainless_steel()),                       # Ref. [2]_ pg. 52
        )

        absorber = FuelFollowerControlRod.Absorber(
            radius   = 1.3 * 0.5 * CM_PER_INCH,                                                    # Ref. [2]_ pg. 55
            length   = 15.0 * CM_PER_INCH,                                                         # Ref. [2]_ pg. 58
            material = Material(NETLDefaultMaterials.control_rod_absorber()),                      # Ref. [2]_ pg. 52
        )

        fuel_follower_outer_radius = cladding.outer_radius - cladding.thickness
        fuel_follower = FuelFollowerControlRod.FuelFollower(
            length       = 15.0 * CM_PER_INCH,                                                     # Ref. [2]_ pg. 58
            inner_radius = 0.25 * 0.5 * CM_PER_INCH,                                               # Ref. [2]_ pg. 55
            outer_radius = fuel_follower_outer_radius,
            material     = Material(TRIGADefaultMaterials.fresh_fuel(density=6.0124)),             # Ref. [2]_ pg. 52
        )

        zr_fill_rod = FuelFollowerControlRod.ZrFillRod(
            radius   = 0.25 * 0.5 * CM_PER_INCH,                                                   # Ref. [2]_ pg. 55
            material = Material(NETLDefaultMaterials.zirc_filler()),                               # Ref. [2]_ pg. 52
        )

        upper_element_plug = FuelFollowerControlRod.ElementPlug(
            thickness = 1.5 * CM_PER_INCH,                                                         # Ref. [2]_ pg. 58
            material  = Material(NETLDefaultMaterials.stainless_steel()),                          # Ref. [2]_ pg. 51
        )

        upper_air_gap = FuelFollowerControlRod.AirGap(thickness=3.5 * CM_PER_INCH)                 # Ref. [2]_ pg. 58

        upper_magneform = FuelFollowerControlRod.MagneformFitting(
            thickness = 0.5 * CM_PER_INCH,                                                         # Ref. [2]_ pg. 58
            material  = Material(NETLDefaultMaterials.stainless_steel()),                          # Ref. [2]_ pg. 51
        )

        above_absorber_air_gap = FuelFollowerControlRod.AirGap(thickness=0.125 * CM_PER_INCH)      # Ref. [2]_ pg. 58

        middle_magneform = FuelFollowerControlRod.MagneformFitting(
            thickness = 0.5 * CM_PER_INCH,                                                         # Ref. [2]_ pg. 58
            material  = Material(NETLDefaultMaterials.stainless_steel()),                          # Ref. [2]_ pg. 51
        )

        above_fuel_follower_air_gap = FuelFollowerControlRod.AirGap(thickness=0.25 * CM_PER_INCH)  # Ref. [2]_ pg. 58

        lower_magneform = FuelFollowerControlRod.MagneformFitting(
            thickness = 1.0 * CM_PER_INCH,                                                         # Ref. [2]_ pg. 58
            material  = Material(NETLDefaultMaterials.stainless_steel()),                          # Ref. [2]_ pg. 51
        )

        lower_air_gap = FuelFollowerControlRod.AirGap(thickness=5.375 * CM_PER_INCH)               # Ref. [2]_ pg. 58

        lower_element_plug = FuelFollowerControlRod.ElementPlug(
            thickness = 0.5 * CM_PER_INCH,                                                         # Ref. [2]_ pg. 58
            material  = Material(NETLDefaultMaterials.stainless_steel()),                          # Ref. [2]_ pg. 51
        )

        return FuelFollowerControlRod(
            cladding                    = cladding,
            absorber                    = absorber,
            fuel_follower               = fuel_follower,
            zr_fill_rod                 = zr_fill_rod,
            upper_element_plug          = upper_element_plug,
            upper_air_gap               = upper_air_gap,
            upper_magneform_fitting     = upper_magneform,
            above_absorber_air_gap      = above_absorber_air_gap,
            middle_magneform_fitting    = middle_magneform,
            above_fuel_follower_air_gap = above_fuel_follower_air_gap,
            lower_magneform_fitting     = lower_magneform,
            lower_air_gap               = lower_air_gap,
            lower_element_plug          = lower_element_plug,
            fill_gas                    = Material(NETLDefaultMaterials.air()),     # Ref. [2]_ pg. 51
            outer_material              = Material(NETLDefaultMaterials.water()),   # Coolant exterior
            gap_tolerance               = 1e-8,
            name                        = "fuel_follower_control_rod",
        )

    @staticmethod
    def transient_rod() -> TransientRod:
        """Creates and returns the default transient control rod.

        Returns
        -------
        TransientControlRod
            Default NETL TRIGA transient control rod.
        """
        cladding = TransientRod.Cladding(
            outer_radius = 1.25 * 0.5 * CM_PER_INCH,                           # Ref. [1]_ Table 4.2
            thickness    = 0.028 * CM_PER_INCH,                                # Ref. [1]_ Table 4.2
            material     = Material(NETLDefaultMaterials.aluminum()),          # Ref. [2]_ pg. 51
        )

        absorber = TransientRod.Absorber(
            radius   = 1.187 * 0.5 * CM_PER_INCH,                              # Ref. [2]_ pg. 55
            length   = 15.0 * CM_PER_INCH,                                     # Ref. [1]_ Table 4.2
            material = Material(NETLDefaultMaterials.control_rod_absorber()),  # Ref. [2]_ pg. 51
        )

        upper_element_plug = TransientRod.ElementPlug(
            thickness = 0.5 * CM_PER_INCH,                                     # Ref. [2]_ pg. 58
            material  = Material(NETLDefaultMaterials.aluminum()),             # Ref. [2]_ pg. 51
        )

        upper_magneform = TransientRod.MagneformFitting(
            thickness = 1.0 * CM_PER_INCH,                                     # Ref. [2]_ pg. 58
            material  = Material(NETLDefaultMaterials.aluminum()),             # Ref. [2]_ pg. 51
        )

        lower_magneform = TransientRod.MagneformFitting(
            thickness = 1.0 * CM_PER_INCH,                                     # Ref. [2]_ pg. 58
            material  = Material(NETLDefaultMaterials.aluminum()),             # Ref. [2]_ pg. 51
        )

        air_follower = TransientRod.AirFollower(
            thickness = 19.75 * CM_PER_INCH                                    # Ref. [2]_ pg. 58
        )

        lower_element_plug = TransientRod.ElementPlug(
            thickness = 0.5 * CM_PER_INCH,                                     # Ref. [2]_ pg. 58
            material  = Material(NETLDefaultMaterials.aluminum()),             # Ref. [2]_ pg. 51
        )

        return TransientRod(
            cladding                = cladding,
            absorber                = absorber,
            fill_gas                = Material(NETLDefaultMaterials.air()),        # Ref. [2]_ pg. 51
            outer_material          = Material(NETLDefaultMaterials.water()),      # Coolant exterior
            air_follower            = air_follower,
            upper_element_plug      = upper_element_plug,
            upper_magneform_fitting = upper_magneform,
            lower_magneform_fitting = lower_magneform,
            lower_element_plug      = lower_element_plug,
            gap_tolerance           = None,
            name                    = "transient_rod",
        )

    @staticmethod
    def upper_grid_plate() -> GridPlate:
        """Creates and returns the default upper grid plate geometry.

        Returns
        -------
        GridPlate
            Default NETL TRIGA upper grid plate.
        """
        return GridPlate(
            thickness                     = 0.62 * CM_PER_INCH,                         # Ref. [2]_ pg. 55
            fuel_penetration_radius       = 1.505 * 0.5 * CM_PER_INCH,                  # Ref. [1]_ Section 4.2.4.a
            control_rod_penetration_radius= 1.505 * 0.5 * CM_PER_INCH,                  # Ref. [1]_ Section 4.2.4.a
            material                      = Material(NETLDefaultMaterials.aluminum()),  # Ref. [2]_ pg. 50
            name                          = "upper_grid_plate",
        )

    @staticmethod
    def lower_grid_plate() -> GridPlate:
        """Creates and returns the default lower grid plate geometry.
        Returns
        -------
        GridPlate
            Default NETL TRIGA lower grid plate.
        """
        return GridPlate(
            thickness                     = 1.25 * CM_PER_INCH,                         # Ref. [2]_ pg. 55
            fuel_penetration_radius       = 1.25  * 0.5 * CM_PER_INCH,                  # Ref. [1]_ Section 4.2.4.b
            control_rod_penetration_radius= 1.505 * 0.5 * CM_PER_INCH,                  # Ref. [1]_ Section 4.2.4.b
            material                      = Material(NETLDefaultMaterials.aluminum()),  # Ref. [2]_ pg. 50
            name                          = "lower_grid_plate",
        )

    @staticmethod
    def pool() -> Pool:
        """Creates and returns the default pool.

        Returns
        -------
        Pool
            Default NETL TRIGA pool.
        """
        return Pool(
            radius   = 90.0,                                            # Ref. [2]_ pg. 54
            height   = 160.0,                                           # Ref. [2]_ pg. 54
            material = Material(NETLDefaultMaterials.water()),          # Ref. [2]_ pg. 48
            name     = "pool",
        )
