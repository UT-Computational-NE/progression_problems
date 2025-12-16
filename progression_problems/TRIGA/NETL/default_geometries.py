from __future__ import annotations

from coreforge.geometry_elements.triga.netl import (CentralThimble, SourceHolder, FuelFollowerControlRod,
                                                    TransientRod, GridPlate, BeamPort, Pool, RSRCavity,
                                                    Reflector, Shroud, Core, Reactor)
from coreforge.materials import Material
from progression_problems.TRIGA.default_geometries import DefaultGeometries as TRIGADefaultGeometries
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

    UPPER_GRID_PLATE_DISTANCE_FROM_CORE_CENTERLINE = 12.75  * CM_PER_INCH  # Ref. [2]_ pg. 55
    LOWER_GRID_PLATE_DISTANCE_FROM_CORE_CENTERLINE = 13.06 * CM_PER_INCH   # Ref. [2]_ pg. 55
    TRANSIENT_ROD_FULLY_INSERTED_POSITION          = -73.0250              # Ref. [2]_ pg. 58
    FFCR_FULLY_INSERTED_POSITION                   = -76.5180              # Ref. [2]_ pg. 58
    TRANSIENT_ROD_MAX_WITHDRAWAL_DISTANCE          = 15.0  * CM_PER_INCH   # Ref. [1]_ pg. 4-10
    FFCR_MAX_WITHDRAWAL_DISTANCE                   = 15.0  * CM_PER_INCH   # Ref. [1]_ pg. 4-10
    TRANSIENT_ROD_FULLY_WITHDRAWN_POSITION         = TRANSIENT_ROD_FULLY_INSERTED_POSITION + \
                                                     TRANSIENT_ROD_MAX_WITHDRAWAL_DISTANCE
    FFCR_FULLY_WITHDRAWN_POSITION                  = FFCR_FULLY_INSERTED_POSITION + \
                                                     FFCR_MAX_WITHDRAWAL_DISTANCE

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

        # Use published grid offsets directly to avoid recursive calls into reactor/core builders
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

    @staticmethod
    def reflector() -> Reflector:
        """Creates and returns the default reflector.

        Returns
        -------
        Reflector
            Default NETL TRIGA reflector.
        """
        return Reflector(
            radius   = 42.0 * 0.5 * CM_PER_INCH,                       # Ref. [2]_ pg. 54
            height   = 23.13 * CM_PER_INCH,                            # Ref. [2]_ pg. 55
            material = Material(NETLDefaultMaterials.graphite()),      # Ref. [2]_ pg. 48
            name     = "reflector",
        )

    @staticmethod
    def shroud() -> Shroud:
        """Creates and returns the default shroud.

        Returns
        -------
        Shroud
            Default NETL TRIGA shroud.
        """
        return Shroud(
            thickness                = 0.1875 * CM_PER_INCH,                      # Ref. [2]_ pg. 54 & 55
            height                   = 23.13 * CM_PER_INCH,                       # Ref. [2]_ pg. 55
            primary_hex_inner_radius = 10.21875 * CM_PER_INCH,                    # Ref. [2]_ pg. 55
            rotated_hex_inner_radius = 10.75 * CM_PER_INCH,                       # Ref. [2]_ pg. 54
            material                 = Material(NETLDefaultMaterials.aluminum()), # Ref. [2]_ pg. 48
            name                     = "shroud",
        )

    @staticmethod
    def rsr_cavity() -> RSRCavity:
        """Creates and returns the default rotary specimen rack cavity.

        Returns
        -------
        RSRCavity
            Default NETL TRIGA rotary specimen rack cavity.
        """
        specimen_tube = RSRCavity.SpecimenTube(
            outer_radius = 1.0 * 0.5 * CM_PER_INCH,                          # Ref. [2]_ pg. 56 & 57
            thickness    = 0.058 * CM_PER_INCH,                              # Ref. [1]_ pg. 10-27
            material     = Material(NETLDefaultMaterials.aluminum()),        # Assumed
        )

        return RSRCavity(
            outer_radius            = 28.625 * 0.5 * CM_PER_INCH,            # Ref. [2]_ pg. 55
            height                  = 10.8174 * CM_PER_INCH,                 # Ref. [2]_ pg. 55
            number_of_tubes         = 40,                                    # Ref. [1]_ pg. 10-27
            tube_to_center_distance = 26.312 * 0.5 * CM_PER_INCH,            # Ref. [1]_ pg. 10-27
            tube_specs              = specimen_tube,
            material                = Material(NETLDefaultMaterials.air()),  # Ref. [2]_ pg. 48
            name                    = "rsr_cavity",
        )

    @staticmethod
    def beam_port() -> BeamPort:
        """Creates and returns the default beam port geometry.

        Notes
        -----
        The beam port length is set arbitrarily to the pool diameter to ensure sufficient length
        for penetration through pool / reflector and to provide some known length with which to work
        default transformations off of.

        Returns
        -------
        BeamPort
            Default NETL TRIGA beam port.
        """

        return BeamPort(
            length        = DefaultGeometries.pool().radius * 2.0,
            inner_radius  = 6.065 * 0.5 * CM_PER_INCH,                  # Ref. [2]_ Figures 4 & 5
            outer_radius  = 6.625 * CM_PER_INCH,                        # Ref. [2]_ Figures 4 & 5
            tube_material = Material(NETLDefaultMaterials.aluminum()),  # Ref. [2]_ pg. 48
            fill_material = Material(NETLDefaultMaterials.air()),       # Ref. [2]_ pg. 48
            name = "beam_port",
        )

    @staticmethod
    def core() -> Core:
        """Creates and returns a default core geometry.

        Returns
        -------
        Core
            Default NETL TRIGA core geometry.
        """
        fuel          = lambda: TRIGADefaultGeometries.fuel_element()
        graphite      = lambda: TRIGADefaultGeometries.graphite_element()
        source_holder = lambda: DefaultGeometries.source_holder()
        empty         = lambda: None

        def fill(locations, factory):
            return {loc: factory() for loc in locations}

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
        loading["E-11"] = empty()

        loading |= fill(["F-01", "F-02", "F-03", "F-04", "F-05", "F-06",
                         "F-07", "F-08", "F-09", "F-10", "F-11", "F-12",
                                         "F-15", "F-16", "F-17", "F-18",
                         "F-19", "F-20", "F-21", "F-22", "F-23", "F-24",
                         "F-25", "F-26", "F-27", "F-28", "F-29", "F-30"], fuel)
        loading["F-13"] = empty()
        loading["F-14"] = empty()

        loading |= fill([        "G-02", "G-03", "G-04", "G-05", "G-06",
                                 "G-08", "G-09", "G-10", "G-11", "G-12",
                                 "G-14", "G-15", "G-16", "G-17", "G-18",
                                 "G-20", "G-21", "G-22", "G-23", "G-24",
                                 "G-26", "G-27", "G-28", "G-29", "G-30",
                                         "G-33", "G-35", "G-36"], fuel)
        loading["G-32"] = source_holder()
        loading["G-34"] = empty()

        return Core(
            pitch           = 1.714 * CM_PER_INCH,          # Ref. [2]_ pg. 54
            central_thimble = DefaultGeometries.central_thimble(),
            transient_rod   = DefaultGeometries.transient_rod(),
            regulating_rod  = DefaultGeometries.fuel_follower_control_rod(),
            shim_1_rod      = DefaultGeometries.fuel_follower_control_rod(),
            shim_2_rod      = DefaultGeometries.fuel_follower_control_rod(),
            loading         = loading,
            fill_material   = DefaultGeometries.pool().material,
            name            = "core",
        )

    @staticmethod
    def reactor() -> Reactor:
        """Creates and returns a default reactor geometry.

        Returns
        -------
        Reactor
            Default NETL TRIGA reactor geometry.
        """
        return Reactor(
            pool                        = DefaultGeometries.pool(),
            shroud                      = DefaultGeometries.shroud(),
            rotary_specimen_rack_cavity = DefaultGeometries.rsr_cavity(),
            core                        = DefaultGeometries.core(),
            name                        = "reactor",
            reflector = Reactor.Reflector(
                geometry = DefaultGeometries.reflector(),
                core_centerline_offset = 0.565 * CM_PER_INCH  # Ref. [2]_ pg. 55
            ),
            upper_grid_plate = Reactor.GridPlate(
                geometry = DefaultGeometries.upper_grid_plate(),
                distance_from_core_centerline = DefaultGeometries.UPPER_GRID_PLATE_DISTANCE_FROM_CORE_CENTERLINE
            ),
            lower_grid_plate = Reactor.GridPlate(
                geometry = DefaultGeometries.lower_grid_plate(),
                distance_from_core_centerline = DefaultGeometries.LOWER_GRID_PLATE_DISTANCE_FROM_CORE_CENTERLINE
            ),
            transient_rod_position = DefaultGeometries.TRANSIENT_ROD_FULLY_INSERTED_POSITION,
            regulating_rod_position = DefaultGeometries.FFCR_FULLY_INSERTED_POSITION,
            shim_1_rod_position = DefaultGeometries.FFCR_FULLY_INSERTED_POSITION,
            shim_2_rod_position = DefaultGeometries.FFCR_FULLY_INSERTED_POSITION,
            # Beam port 1/5 specifications from Ref. [2]_ pages 48, 56, 59
            beam_port_1_5 = Reactor.BeamPort(
                geometry    = DefaultGeometries.beam_port(),
                translation = (35.2425, 0.0, -6.985),
            ),
            # Beam port 2 specifications from Ref. [2]_ pages 48, 56, 59
            beam_port_2 = Reactor.BeamPort(
                geometry    = DefaultGeometries.beam_port(),
                rotation    = ((150.0,  60.0, 90.0),
                               (120.0, 150.0, 90.0),
                               ( 90.0,  90.0,  0.0)),
                translation = (-18.399365255524088, 77.9004555727542, -6.985),
            ),
            # Beam port 3 specifications from Ref. [2]_ pages 48, 56, 59
            beam_port_3 = Reactor.BeamPort(
                geometry    = DefaultGeometries.beam_port(),
                rotation    = (( 90.0, 180.0, 90.0),
                               (  0.0,  90.0, 90.0),
                               ( 90.0,  90.0,  0.0)),
                translation = (-116.43188, 0.0, -6.985),
            ),
            # Beam port 4 specifications from Ref. [2]_ pages 48, 56, 59
            beam_port_4 = Reactor.BeamPort(
                geometry    = DefaultGeometries.beam_port(),
                rotation    = (( 75.0,  60.0, 90.0),
                               (120.0,  75.0, 90.0),
                               ( 90.0,  90.0,  0.0)),
                translation = (-69.63559769456143, -6.33393280074954, -6.985),
            ),
        )
