.. _progression_problems_triga_netl_system_specifications:

=====================
System Specifications
=====================

This section contains system specifications for those elements which pertaining specifically
to the TRIGA reactor at the University of Texas at Austin's Nuclear Engineering Teaching and
Research Laboratory (NETL).

The NETL TRIGA reactor, pictured in :numref:`figure-reactor-pool`, :numref:`figure-reactor-radial-picture`,
and :numref:`figure-reactor-axial-picture`, consists of a core assembly of cylindrical fuel elements housed within
a hexagonal aluminum shroud, which itself is surrounded by a graphite reflector, with the whole assemblage
submerged in a reactor pool.  The core elements are kept in position using upper and lower grid plates which
are located above and below the core, respectively. A rotary specimen rack (RSR) encircles the upper portion
of the core to support neutron irradiation experiments. Additional irradiation capability is provided via a
central thimble, beam ports (BPs) located at various radial positions through the reflector adjacent to the
core shroud, and a special pneumatic tube system for short sample irradiations.  The core is configured as a
hexagonal lattice of positions that can accommodate fuel elements, graphite elements, control rods, a neutron
source holder, irradiation facilities (i.e., central thimble and pneumatic tube system), or vacancies. The
detailed specifications that follow are derived primarily from the TRIGA UFSAR (Ref. 1_) and the
beamport characterization report (Ref. 2_).

.. _figure-reactor-pool:

.. figure:: /_static/images/triga/netl/reactor_pool.png
   :align: center
   :width: 60%

   Top view of the reactor core layout showing various reactor components

.. _figure-reactor-radial-picture:

.. figure:: /_static/images/triga/netl/reactor_radial_picture.png
   :align: center
   :width: 60%

   Radial cross sections at the RSR centerline plane (left) and BP centerline plane (right)

.. _figure-reactor-axial-picture:

.. figure:: /_static/images/triga/netl/reactor_axial_picture.png
   :align: center
   :width: 60%

   Axial cross section along the control-rod centerline plane

Excore Features
===============

As noted previously, the core is surrounded by several excore structures that are relevant to neutronics
and geometry specification, including the core shroud (pictured in :numref:`figure-shroud`), upper and lower
grid plates, rotary specimen rack, and graphite reflector (pictured in :numref:`figure-reflector-canister`).
The core shroud is an aluminum structure that encloses the core and helps direct coolant flow through the active
region. Geometrically, the shroud forms an irregular dodecagon defined by the intersection of two regular hexagons
of different size rotated by 30° relative to one another; in the NETL TRIGA configuration, the shroud is
oriented such that BP 1 and 5 are parallel to one of its long faces. The upper and lower grid plates are aluminum
support structures containing a hexagonal array of cylindrical penetrations corresponding to the core lattice
positions, thereby providing both element alignment and coolant flow paths. The RSR is represented as an air-filled,
watertight annular canister containing specimen tubes arranged for irradiation around the upper core region.
Surrounding these components is the graphite reflector, which improves neutron economy by moderating and reflecting
neutrons leaking from the core and includes penetrations for the BPs. Key specifications for these excore features
are summarized in :numref:`table-excore-features`.

.. _figure-shroud:

.. figure:: /_static/images/triga/netl/shroud.png
   :align: center
   :width: 60%

   Picture of the Inner Shroud Surface (Ref. 1_).


.. _figure-reflector-canister:

.. figure:: /_static/images/triga/netl/reflector_canister.png
   :align: center
   :width: 60%

   Pictures of Reflector and Reflector Canister (Ref. 1_).

.. table:: Excore Feature Specifications
   :name: table-excore-features

   +-------------------+---------------------------+--------------------+----------------------+
   | Component         | Property                  | Value              | Reference            |
   +===================+===========================+====================+======================+
   | Shroud            | Thickness (in.)           | 0.1875             | Ref. 2_, pg. 54-55   |
   |                   +---------------------------+--------------------+----------------------+
   |                   | Height (in.)              | 23.13              | Ref. 2_, pg. 55      |
   |                   +---------------------------+--------------------+----------------------+
   |                   | Small Hexagon             | 10.21875           | Ref. 2_, pg. 55      |
   |                   | Inradius (in.)            |                    |                      |
   |                   +---------------------------+--------------------+----------------------+
   |                   | Large Hexagon             | 10.75              | Ref. 2_, pg. 54      |
   |                   | Inradius (in.)            |                    |                      |
   |                   +---------------------------+--------------------+----------------------+
   |                   | Material                  | Aluminum           | Ref. 2_, pg. 48      |
   +-------------------+---------------------------+--------------------+----------------------+
   | Upper Grid        | Thickness (in.)           | 0.62               | Ref. 2_, pg. 55      |
   | Plate             +---------------------------+--------------------+----------------------+
   |                   | Fuel Element Penetration  | 1.505              | Ref. 1_, Sec. 4.2.4.a|
   |                   | Diameter (in.)            |                    |                      |
   |                   +---------------------------+--------------------+----------------------+
   |                   | Control Rod Penetration   | 1.505              | Ref. 1_, Sec. 4.2.4.a|
   |                   | Diameter (in.)            |                    |                      |
   |                   +---------------------------+--------------------+----------------------+
   |                   | Top to Core Axial         | 12.75              | Ref. 2_, pg. 55      |
   |                   | Centerline Distance (in.) |                    |                      |
   |                   +---------------------------+--------------------+----------------------+
   |                   | Material                  | Aluminum           | Ref. 2_, pg. 50      |
   +-------------------+---------------------------+--------------------+----------------------+
   | Lower Grid        | Thickness (in.)           | 1.25               | Ref. 2_, pg. 55      |
   | Plate             +---------------------------+--------------------+----------------------+
   |                   | Fuel Element Penetration  | 1.25               | Ref. 1_, Sec. 4.2.4.b|
   |                   | Diameter (in.)            |                    |                      |
   |                   +---------------------------+--------------------+----------------------+
   |                   | Control Rod Penetration   | 1.505              | Ref. 1_, Sec. 4.2.4.b|
   |                   | Diameter (in.)            |                    |                      |
   |                   +---------------------------+--------------------+----------------------+
   |                   | Top to Core Axial         | 13.06              | Ref. 2_, pg. 55      |
   |                   | Centerline Distance (in.) |                    |                      |
   |                   +---------------------------+--------------------+----------------------+
   |                   | Material                  | Aluminum           | Ref. 2_, pg. 50      |
   +-------------------+---------------------------+--------------------+----------------------+
   | RSR Cavity        | Outer Diameter (in.)      | 28.625             | Ref. 2_, pg. 55      |
   |                   +---------------------------+--------------------+----------------------+
   |                   | Height (in.)              | 10.8174            | Ref. 2_, pg. 55      |
   |                   +---------------------------+--------------------+----------------------+
   |                   | Material                  | Air                | Ref. 2_, pg. 48      |
   +-------------------+---------------------------+--------------------+----------------------+
   | RSR Specimen      | Number of Tubes           | 40                 | Ref. 1_, pg. 10-27   |
   | Tubes             +---------------------------+--------------------+----------------------+
   |                   | Outer Diameter (in.)      | 1.0                | Ref. 2_, pg. 56-57   |
   |                   +---------------------------+--------------------+----------------------+
   |                   | Wall Thickness (in.)      | 0.058              | Ref. 1_, pg. 10-27   |
   |                   +---------------------------+--------------------+----------------------+
   |                   | Tube-to-Center            | 26.312 x 0.5       | Ref. 1_, pg. 10-27   |
   |                   | Distance (in.)            |                    |                      |
   |                   +---------------------------+--------------------+----------------------+
   |                   | Material                  | Aluminum           | (assumed)            |
   +-------------------+---------------------------+--------------------+----------------------+
   | Reflector         | Diameter (in.)            | 42.0               | Ref. 2_, pg. 54      |
   |                   +---------------------------+--------------------+----------------------+
   |                   | Height (in.)              | 23.13              | Ref. 2_, pg. 55      |
   |                   +---------------------------+--------------------+----------------------+
   |                   | Core Axial Centerline     | 0.565              | Ref. 2_, pg. 55      |
   |                   | Offset (in.)              |                    |                      |
   |                   +---------------------------+--------------------+----------------------+
   |                   | Material                  | Graphite           | Ref. 2_, pg. 48      |
   +-------------------+---------------------------+--------------------+----------------------+


The reactor excore region also includes several BPs, which are cylindrical aluminum tubes that penetrate
the concrete shield, reactor tank, and graphite reflector to provide access for neutron irradiation
experiments. These BPs are air-filled and allow specimens and/or instrumentation to be positioned either
within the port itself or externally in the emerging neutron beam. BP 1 is connected to BP 5, forming a
through-port arrangement that passes tangentially to the core through the graphite reflector. BP 2 is a
tangential beam port that terminates in the reflector. BP 3 is a radial beam port that penetrates through
the reflector and terminates at its inner edge, while BP 4 is another radial beam port that terminates at
the reflector outer edge, but has an associated void in the graphite reflector to extend the effective
source of neutrons to the reactor core. Geometric specifications used in the progression problems are
summarized in :numref:`table-beam-ports`. Beam-port translations and rotations are defined with respect to
the core orientation shown in :numref:`figure-reactor-radial-picture`, where alignment with the \(x\)-axis
corresponds to zero rotation and the origin is located at the core center and the axial midplane of the
fuel meat. Consistent with MCNP (Ref. 3_) transformation conventions, rotations are applied first and
translations second.


.. table:: Beam Ports Geometry Specifications
   :name: table-beam-ports

   +---------------+-----------------------+--------------------+-------------------------+
   | Component     | Property              | Value              | Reference               |
   +===============+=======================+====================+=========================+
   | All Beam Ports| Inner Diameter (in.)  | 6.065              | Ref. 2_, Fig. 4 & 5     |
   |               +-----------------------+--------------------+-------------------------+
   |               | Outer Diameter (in.)  | 6.625              | Ref. 2_, Fig. 4 & 5     |
   |               +-----------------------+--------------------+-------------------------+
   |               | Core Axial Centerline | -6.985             | Ref. 2_, pg. 56, 59     |
   |               | Offset (cm)           |                    |                         |
   |               +-----------------------+--------------------+-------------------------+
   |               | Tube Material         | Aluminum           | Ref. 2_, pg. 48         |
   |               +-----------------------+--------------------+-------------------------+
   |               | Fill Material         | Air                | Ref. 2_, pg. 48         |
   +---------------+-----------------------+--------------------+-------------------------+
   | Beam Port 1   | Rotation              | 90.0               | Ref. 1_, pg. 4-24       |
   |               | (degrees)             |                    | Ref. 2_, pg. 48, 56     |
   |               +-----------------------+--------------------+-------------------------+
   |               | Center of Tube Length | (35.2425, 0.0)     | Ref. 2_, pg. 48, 56, 59 |
   |               | X-Y Coordinates (cm)  |                    |                         |
   +---------------+-----------------------+--------------------+-------------------------+
   | Beam Port 2   | Rotation              |  150.0             | Ref. 1_, pg. 4-24       |
   |               | (degrees)             |                    | Ref. 2_, pg. 48, 56     |
   |               +-----------------------+--------------------+-------------------------+
   |               | Center of Tip         | (6.222, 35.255)    | Ref. 2_, pg. 48, 56, 59 |
   |               | X-Y Coordinates (cm)  |                    |                         |
   +---------------+-----------------------+--------------------+-------------------------+
   | Beam Port 3   | Rotation              |  0.0               | Ref. 1_, pg. 4-24       |
   |               | (degrees)             |                    | Ref. 2_, pg. 48, 56     |
   |               +-----------------------+--------------------+-------------------------+
   |               | Center of Tip         | (-26.43188, 0.0)   | Ref. 2_, pg. 48, 56, 59 |
   |               | X-Y Coordinates (cm)  |                    |                         |
   +---------------+-----------------------+--------------------+-------------------------+
   | Beam Port 4   | Rotation              |  60.0              | Ref. 1_, pg. 4-24       |
   |               | (degrees)             |                    | Ref. 2_, pg. 48, 56     |
   |               +-----------------------+--------------------+-------------------------+
   |               | Center of Tip         | (-13.216,-22.871)  | Ref. 2_, pg. 48, 56, 59 |
   |               | X-Y Coordinates (cm)  |                    |                         |
   +---------------+-----------------------+--------------------+-------------------------+


Incore Features
===============

The reactor core consists of a configurable hexagonal lattice of the core elements described above,
with a lattice pitch of 1.714~in. A core map, including lattice position labels, is shown in :numref:`figure-reactor-core-map`.
Most lattice positions are configurable and may be occupied by fuel elements, graphite dummy elements,
a neutron source holder, or left vacant as water holes; however, certain positions are reserved for
specific components, as summarized in :numref:`reserved-core-locations`. It should be noted that
the NETL TRIGA reactor contains additional core-associated components not considered here, including insertable
experimental irradiation facilities and the pneumatic sample-transit system. These components may be present
in the actual reactor but are excluded from the current progression-problem definitions.

.. _figure-reactor-core-map:

.. figure:: /_static/images/triga/netl/reactor_core_map.png
   :align: center
   :width: 60%

   Core map showing lattice position labels

.. table:: Reserved Core Locations
   :name: reserved-core-locations

   +------------------------------------------------+-----------+--------------------+
   | Component Type                                 | Location  | Reference          |
   +===============+================================+===========+====================+
   | Central Thimble                                | A-01      | Ref. 1_, pg. 4-9   |
   +---------------+--------------------------------+-----------+--------------------+
   | Transient Control Rod                          | C-01      | Ref. 1_, Fig. 4.4  |
   +---------------+------------+-------------------+-----------+                    |
   | Fuel Follower Control Rod  | Regulating Rod    | C-07      |                    |
   |                            +-------------------+-----------+                    |
   |                            | Shim 1 Rod        | D-06      |                    |
   |                            +-------------------+-----------+                    |
   |                            | Shim 2 Rod        | D-14      |                    |
   +---------------+------------+-------------------+-----------+                    |
   | Reserved Empty Locations                       | G-01      |                    |
   |                                                +-----------+                    |
   |                                                | G-07      |                    |
   |                                                +-----------+                    |
   |                                                | G-13      |                    |
   |                                                +-----------+                    |
   |                                                | G-19      |                    |
   |                                                +-----------+                    |
   |                                                | G-25      |                    |
   |                                                +-----------+                    |
   |                                                | G-31      |                    |
   +---------------+------------+-------------------+-----------+--------------------+
   | Pneumatic Sample-Transit Terminal              | G-34      | Ref. 1_, Sec.      |
   |                                                |           | 10.2.2.a.2         |
   +---------------+------------+-------------------+-----------+--------------------+

Fuel Element
------------
see: :ref:`progression_problems_triga_fuel_element`

Graphite Element
----------------
see: :ref:`progression_problems_triga_graphite_element`

Transient Control Rod
----------------------

The Transient Control Rod (TCR) consists of a solid boron–carbide absorber cylinder clad in
aluminum and is pneumatically actuated to permit rapid position changes for pulse operation.
During steady-state operation, the TCR also serves as an alternate safety rod and is held partially
(or fully) withdrawn by a continuous air supply. Geometric specifications used in the NETL TRIGA
progression problems are summarized in :numref:`table-transient-control-rod`, and the axial configuration
is shown in :numref:`figure-transient-control-rod-axial_profile`. For modeling, the TCR axial position
is defined such that, when fully inserted, the absorber midplane is aligned with the fuel-element
axial midplane. The TCR maximum travel distance is 15.0~in.


.. _figure-transient-control-rod-axial_profile:

.. figure:: /_static/images/triga/netl/transient_control_rod_axial_diagram.png
   :align: center
   :width: 60%

   Diagram of Transient Control Rod Axial Profile.
.. table:: Transient Control Rod Geometry Specifications
   :name: table-transient-control-rod

   +---------------+----------------------+--------------------+----------------------+
   | Component     | Property             | Value              | Reference            |
   +===============+======================+====================+======================+
   | Cladding      | Thickness (in.)      | 0.028              | Ref. 1_, Table 4.2   |
   |               +----------------------+--------------------+----------------------+
   |               | Outer Diameter (in.) | 1.25               | Ref. 1_, Table 4.2   |
   |               +----------------------+--------------------+----------------------+
   |               | Material             | Aluminum           | Ref. 2_, pg. 51      |
   +---------------+----------------------+--------------------+----------------------+
   | Element Plugs | Thickness (in.)      | 0.5                | Ref. 2_, pg. 58      |
   |               +----------------------+--------------------+----------------------+
   |               | Material             | Aluminum           | Ref. 2_, pg. 51      |
   +---------------+----------------------+--------------------+----------------------+
   | Magneform     | Thickness (in.)      | 1.0                | Ref. 2_, pg. 58      |
   | Fittings      +----------------------+--------------------+----------------------+
   |               | Material             | Aluminum           | Ref. 2_, pg. 51      |
   +---------------+----------------------+--------------------+----------------------+
   | Absorber      | Diameter (in.)       | 1.187              | Ref. 2_, pg. 55      |
   |               +----------------------+--------------------+----------------------+
   |               | Length (in.)         | 15.0               | Ref. 1_, Table 4.2   |
   |               +----------------------+--------------------+----------------------+
   |               | Material             | CR Absorber        | Ref. 2_, pg. 51      |
   +---------------+----------------------+--------------------+----------------------+
   | Air Follower  | Length (in.)         | 19.75              | Ref. 1_, pg. 58      |
   +---------------+----------------------+--------------------+----------------------+
   | Fill Gas      | Material             | Air                | Ref. 2_, pg. 51      |
   +---------------+----------------------+--------------------+----------------------+



Fuel Follower Control Rod
-------------------------

Fuel-follower control rods (FFCRs) consist of solid boron–carbide absorber cylinders clad in
stainless steel. Unlike the TCR, FFCRs are not pneumatically actuated; instead, they are mechanically
coupled to control-rod drive mechanisms to permit controlled insertion and withdrawal from the core.
Each FFCR incorporates a fuel-follower section such that, as the absorber is withdrawn, a fueled
section occupies the vacated region to help maintain core reactivity and flux shaping. At NETL TRIGA,
three rods—two shim rods and one regulating rod—are FFCRs. The shim rods provide coarse reactivity
control (e.g., for startup and burnup compensation), whereas the regulating rod provides fine control
and may be operated under an automatic controller to maintain an operator-selected power level. Geometric
specifications used in the NETL TRIGA progression problems are summarized in :numref:`table-fuel-follower-control-rod`,
and the axial configuration of the FFCR is shown in :numref:`figure-fuel-follower-control-rod-axial_profile`. For modeling,
the FFCR axial position is defined such that, when fully inserted, the absorber midplane aligns with the
fuel-element axial midplane. The maximum FFCR travel distance is 15.0~in.


.. _figure-fuel-follower-control-rod-axial_profile:

.. figure:: /_static/images/triga/netl/fuel_follower_control_rod_axial_diagram.png
   :align: center
   :width: 60%

   Diagram of Fuel Follower Control Rod Axial Profile.

.. table:: Fuel Follower Control Rod Geometry Specifications
   :name: table-fuel-follower-control-rod

   +-------------------+------------------------+--------------------+----------------------+
   | Component         | Property               | Value              | Reference            |
   +===================+========================+====================+======================+
   | Cladding          | Thickness (in.)        | 0.02               | Ref. 2_, pg. 55      |
   |                   +------------------------+--------------------+----------------------+
   |                   | Outer Diameter (in.)   | 1.35               | Ref. 2_, pg. 55      |
   |                   +------------------------+--------------------+----------------------+
   |                   | Material               | Stainless Steel    | Ref. 2_, pg. 52      |
   +-------------------+------------------------+--------------------+----------------------+
   | Element Plugs     | Upper Thickness (in.)  | 1.5                | Ref. 2_, pg. 58      |
   |                   +------------------------+--------------------+----------------------+
   |                   | Lower Thickness (in.)  | 0.5                | Ref. 2_, pg. 58      |
   |                   +------------------------+--------------------+----------------------+
   |                   | Material               | Stainless Steel    | Ref. 2_, pg. 51      |
   +-------------------+------------------------+--------------------+----------------------+
   | Magneform         | Upper Thickness (in.)  | 0.5                | Ref. 2_, pg. 58      |
   | Fittings          +------------------------+--------------------+----------------------+
   |                   | Middle Thickness (in.) | 0.5                | Ref. 2_, pg. 58      |
   |                   +------------------------+--------------------+----------------------+
   |                   | Lower Thickness (in.)  | 1.0                | Ref. 2_, pg. 58      |
   |                   +------------------------+--------------------+----------------------+
   |                   | Material               | Stainless Steel    | Ref. 2_, pg. 51      |
   +-------------------+------------------------+--------------------+----------------------+
   | Absorber          | Diameter (in.)         | 1.3                | Ref. 2_, pg. 55      |
   |                   +------------------------+--------------------+----------------------+
   |                   | Length (in.)           | 15.0               | Ref. 2_, pg. 58      |
   |                   +------------------------+--------------------+----------------------+
   |                   | Material               | CR Absorber        | Ref. 2_, pg. 52      |
   +-------------------+------------------------+--------------------+----------------------+
   | Fuel Follower     | Inner Diameter (in.)   | 0.25               | Ref. 2_, pg. 55      |
   |                   +------------------------+--------------------+----------------------+
   |                   | Length (in.)           | 15.0               | Ref. 2_, pg. 58      |
   |                   +------------------------+--------------------+----------------------+
   |                   | Material               | CR U-ZrH1.6        | Ref. 2_, pg. 52      |
   +-------------------+------------------------+--------------------+----------------------+
   | Zr Fill Rod       | Diameter (in.)         | 0.25               | Ref. 2_, pg. 55      |
   |                   +------------------------+--------------------+----------------------+
   |                   | Material               | Zirconium          | Ref. 2_, pg. 52      |
   +-------------------+------------------------+--------------------+----------------------+
   | Air Gaps          | Upper Gap              | 3.5                | Ref. 2_, pg. 58      |
   |                   +------------------------+--------------------+----------------------+
   |                   | Above Absorber (in.)   | 0.125              | Ref. 2_, pg. 58      |
   |                   +------------------------+--------------------+----------------------+
   |                   | Above Fuel Follower    | 0.25               | Ref. 2_, pg. 58      |
   |                   | (in.)                  |                    |                      |
   |                   +------------------------+--------------------+----------------------+
   |                   | Lower Gap              | 5.375              | Ref. 2_, pg. 58      |
   +-------------------+------------------------+--------------------+----------------------+
   | Fill Gas          | Material               | Air                | Ref. 2_, pg. 51      |
   +-------------------+------------------------+--------------------+----------------------+


Source Holder
-------------

The neutron source holder is an aluminum cylindrical insert that houses a startup neutron source
used to monitor reactivity during shutdown and approach-to-criticality. The source is located within
a cylindrical internal cavity, and the assembly can be installed in any fuel-element lattice position.
Axially, the source holder spans from the top of the upper grid plate to a location just above the lower grid plate.
Geometric specifications used in the NETL TRIGA progression problems are summarized in :numref:`table-source-holder`
and the axial configuration of the source holder is shown in :numref:`figure-source_holder-axial_profile`.


.. _figure-source_holder-axial_profile:

.. figure:: /_static/images/triga/netl/source_holder_axial_diagram.png
   :align: center
   :width: 60%

   Diagram of Source Holder Axial Profile.

.. table:: Source Holder Geometry Specifications
   :name: table-source-holder

   +---------------+----------------------+--------------------+----------------------+
   | Component     | Property             | Value              | Reference            |
   +===============+======================+====================+======================+
   | Cladding      | Outer Diameter (in.) | 1.435              | Ref. 2_, pg. 54-55   |
   |               +----------------------+--------------------+----------------------+
   |               | Material             | Aluminum           | Ref. 2_, pg. 54      |
   +---------------+----------------------+--------------------+----------------------+
   | Cavity        | Diameter (in.)       | 0.981              | Ref. 1_, Sec. 4.2.5  |
   |               +----------------------+--------------------+----------------------+
   |               | Length (in.)         | 3.0                | Ref. 1_, Sec. 4.2.5  |
   |               +----------------------+--------------------+----------------------+
   |               | Core Axial Center    | 0.0                | Ref. 2_, pg. 55      |
   |               | Offset (in.)         |                    |                      |
   |               +----------------------+--------------------+----------------------+
   |               | Material             | Air                | Ref. 2_, pg. 54      |
   +---------------+----------------------+--------------------+----------------------+
   | Bottom of     | Distance from Lower  | 1.1934             | Ref. 2_, pg. 55      |
   | Source Holder | Grid Plate (cm)      |                    |                      |
   +---------------+----------------------+--------------------+----------------------+

Central Thimble
---------------

the central thimble: an aluminum tube that passes through the central penetrations of the upper
and lower grid plates. The central thimble provides an irradiation position at the point of maximum
neutron flux in the core, enabling high-flux experiment irradiation. Geometric specifications used
in the progression problems are summarized in :numref:`table-central-thimble` and the axial configuration
of the central thimble is shown in :numref:`figure-central_thimble-axial_profile`.


.. _figure-central_thimble-axial_profile:

.. figure:: /_static/images/triga/netl/central_thimble_axial_diagram.png
   :align: center
   :width: 60%

   Diagram of Central Thimble Axial Profile.

.. table:: Central Thimble Geometry Specifications
   :name: table-central-thimble

   +---------------+----------------------+--------------------+----------------------+
   | Component     | Property             | Value              | Reference            |
   +===============+======================+====================+======================+
   | Cladding      | Inner Diameter (in.) | 1.33               | Ref. 1_, Sec.10.2.1.b|
   |               +----------------------+--------------------+----------------------+
   |               | Outer Diameter (in.) | 1.5                | Ref. 1_, Sec.10.2.1.b|
   |               +----------------------+--------------------+----------------------+
   |               | Material             | Aluminum           | Ref. 2_, pg. 51      |
   +---------------+----------------------+--------------------+----------------------+


Pneumatic Neutron Transport System
-----------------------------------

The pneumatic neutron transport (PNT) system transfers small irradiation capsules between an
external loading station and an in-core terminal. For the progression problems, only the
neutronics-relevant in-core terminal is modeled; the ex-core transport tubing, valves, blower,
receiving stations, and control equipment are excluded. The modeled in-core PNT hardware is
centered in lattice position ``G-34`` and extends from the top of the model (i.e., top of pool)
to the bottom of the lower grid plate, passing through both grid-plate penetrations.

Two terminal configurations are defined: an unlined configuration (see: :numref:`table-pnt-unlined`)
and a cadmium-lined (see: :numref:`table-pnt-cd-lined`) configuration. The unlined configuration
consists of a small aluminum tube with an air-filled bore. The cadmium-lined configuration retains
this inner tube wraps it with cadmium, and places the assembly concentrically inside a larger
aluminum tube. The annulus between the cadmium and the larger tube is air-filled.

These baseline specifications contain air in the empty tube section and do not explicitly represent a
polyethylene rabbit, sample container, or irradiated specimen.

.. table:: Unlined PNT Terminal Geometry Specifications
   :name: table-pnt-unlined

   +---------------+--------------------------------+------------------+--------------------+
   | Component     | Property                       | Value            | Reference          |
   +===============+================================+==================+====================+
   | Empty Tube    | Bottom Axial Location Relative | -18.7182         | Ref. 2_, pp. 53--55|
   | Section       | to Core Midplane (cm)          |                  |                    |
   |               +--------------------------------+------------------+--------------------+
   |               | Bore Diameter (in.)            | 0.685            | Ref. 1_, Table 10.3|
   |               |                                |                  | Ref. 2_, pg. 55    |
   |               +--------------------------------+------------------+--------------------+
   |               | Bore Material                  | Air              | Ref. 2_, pg. 53    |
   |               +--------------------------------+------------------+--------------------+
   |               | Tube Outer Diameter (in.)      | 0.875            | Ref. 1_, Table 10.3|
   |               |                                |                  | Ref. 2_, pg. 55    |
   |               +--------------------------------+------------------+--------------------+
   |               | Tube Material                  | Aluminum         | Ref. 2_, pg. 53    |
   +---------------+--------------------------------+------------------+--------------------+
   | Shock         | Axial Thickness (cm)           | 5.1308           | Ref. 2_, pp. 53--55|
   | Absorber      +--------------------------------+------------------+                    |
   |               | Outer Diameter (in.)           | 0.875            |                    |
   |               +--------------------------------+------------------+                    |
   |               | Material                       | Aluminum         |                    |
   +---------------+--------------------------------+------------------+--------------------+
   | Terminus      | Axial Thickness (cm)           | 4.1725           | Ref. 2_, pp. 53--55|
   | Connecting    +--------------------------------+------------------+                    |
   | Tube          | Outer Diameter (in.)           | 1.250            |                    |
   |               +--------------------------------+------------------+                    |
   |               | Material                       | Aluminum         |                    |
   +---------------+--------------------------------+------------------+--------------------+
   | Tube Bottom   | Axial Thickness (cm)           | 8.3259           | Ref. 2_, pp. 53--55|
   |               +--------------------------------+------------------+                    |
   |               | Outer Diameter (in.)           | 0.875            |                    |
   |               +--------------------------------+------------------+                    |
   |               | Material                       | Aluminum         |                    |
   +---------------+--------------------------------+------------------+--------------------+


.. table:: Cadmium-Lined PNT Terminal Geometry Specifications
   :name: table-pnt-cd-lined

   +---------------+--------------------------------+------------------+--------------------+
   | Component     | Property                       | Value            | Reference          |
   +===============+================================+==================+====================+
   | Empty Tube    | see :numref:`table-pnt-unlined` Empty Tube Section                     |
   +---------------+--------------------------------+------------------+--------------------+
   | Cd-Wrapped    | Start of Section               | Top of Upper     | Ref. 2_, pg. 53    |
   | Section       |                                | Grid Plate       |                    |
   |               +--------------------------------+------------------+--------------------+
   |               | Cd-Wrap Outer Diameter (in.)   | 0.955            | Ref. 2_, pg. 55    |
   |               +--------------------------------+------------------+--------------------+
   |               | Air-Gap Outer Diameter (in.)   | 1.120            | Ref. 2_, pg. 55    |
   |               +--------------------------------+------------------+--------------------+
   |               | Outer-Tube Outer Diameter (in.)| 1.250            | Ref. 1_, Table 10.3|
   |               |                                |                  | Ref. 2_, pg. 55    |
   |               +--------------------------------+------------------+--------------------+
   |               | Outer-Tube Material            | Aluminum         | Ref. 2_, pg. 53    |
   +---------------+--------------------------------+------------------+--------------------+
   | Shock         | Axial Thickness (cm)           | 2.5400           | Ref. 2_, pp. 53--55|
   | Absorber      +--------------------------------+------------------+                    |
   | Upper         | Outer Diameter (in.)           | 1.250            |                    |
   | Section       +--------------------------------+------------------+                    |
   |               | Material                       | Aluminum         |                    |
   +---------------+--------------------------------+------------------+--------------------+
   | Cd Disk       | Axial Thickness (cm)           | 0.0508           | Ref. 2_, pp. 53--55|
   |               +--------------------------------+------------------+                    |
   |               | Cd Disk Material               | Cadmium          |                    |
   +---------------+--------------------------------+------------------+--------------------+
   | Shock         | Axial Thickness (cm)           | 2.5400           | Ref. 2_, pp. 53--55|
   | Absorber      +--------------------------------+------------------+                    |
   | Lower         | Outer Diameter (in.)           | 1.435            |                    |
   | Section       +--------------------------------+------------------+                    |
   |               | Material                       | Aluminum         |                    |
   +---------------+--------------------------------+------------------+--------------------+
   | Terminus      | Axial Thickness (cm)           | 4.1725           | Ref. 2_, pp. 53--55|
   | Connecting    +--------------------------------+------------------+                    |
   | Tube          | Outer Diameter (in.)           | 1.250            |                    |
   |               +--------------------------------+------------------+                    |
   |               | Material                       | Aluminum         |                    |
   +---------------+--------------------------------+------------------+--------------------+
   | Lower Section | Axial Thickness (cm)           | 8.3259           | Ref. 2_, pp. 53--55|
   |               +--------------------------------+------------------+                    |
   |               | Outer Diameter (in.)           | 1.435            |                    |
   |               +--------------------------------+------------------+                    |
   |               | Material                       | Aluminum         |                    |
   +---------------+--------------------------------+------------------+--------------------+


Conventional Three-Element Irradiator
--------------------------------------

The conventional three-element irradiation facility (3-EL) replaces the fuel elements in lattice
positions ``E-11``, ``F-13``, and ``F-14``. The irradiation canister is centered at the centroid of
these three positions. Both the lead-lined and cadmium-lined configurations use the same geometry;
only the liner material changes. The lead-lined configuration supports thermal and epithermal
irradiations, whereas the cadmium-lined configuration suppresses the thermal component for
epithermal irradiations.

This specification follows the conventional 3-EL model described by Hudson (Ref. 4_).
Following the simplifications in that model, the three standard fuel-element penetrations
in the upper grid plate are replaced by a single cylindrical penetration centered on the canister.
The detailed alignment frame, its coolant-flow holes, the centered lower-grid alignment penetration,
handling fixtures, valves, seals, and other mechanical details are not represented. The upper and
lower ends of the canister are consequently represented as simple aluminum cylinders.
Experiment-specific samples are excluded and the sample volume is filled with air. The axial regions
are listed from top to bottom in :numref:`table-three-element-geometry`.

.. table:: Conventional 3-EL Geometry Specifications
   :name: table-three-element-geometry

   +----------------------+----------------------------------------+------------------+------------------------+
   | Component            | Property                               | Value            | Reference              |
   +======================+========================================+==================+========================+
   | Facility Placement   | Replaced Lattice Positions             | E-11, F-13, F-14 | Ref. 4_, pp. 140       |
   |                      +----------------------------------------+------------------+------------------------+
   |                      | Radial Location                        | Centroid of the  | Ref. 4_,               |
   |                      | (Derived / Model Evidence)             | Three Positions  | pp. 217, 231--232      |
   |                      +----------------------------------------+------------------+------------------------+
   |                      | Bottom Axial Location                  | Top of Lower     | Ref. 4_, pp. 218, 228  |
   |                      |                                        | Grid Plate       | Ref. 1_, pp. 10-14     |
   |                      +----------------------------------------+------------------+------------------------+
   |                      | Upper Grid Penetration Radius (cm)     | 2.40000          | Ref. 4_, pp. 152, 217  |
   +----------------------+----------------------------------------+------------------+------------------------+
   | Outer Casing         | Inner Radius (cm)                      | 2.23393          | Ref. 4_, pp. 184, 186, |
   |                      |                                        |                  | 217--218               |
   |                      +----------------------------------------+------------------+                        +
   |                      | Outer Radius (cm)                      | 2.38125          |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Overall Axial Length (cm)              | 127.9524         |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Solid Upper-End Thickness (cm)         | 3.1750           |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Solid Lower-End Thickness (cm)         | 2.5399           |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Material                               | Aluminum         |                        |
   +----------------------+----------------------------------------+------------------+------------------------+
   | Inner Sleeve         | Inner Radius (cm)                      | 1.93929          | Ref. 4_, pp. 187,      |
   |                      |                                        |                  | 217--218               |
   |                      +----------------------------------------+------------------+                        +
   |                      | Outer Radius (cm)                      | 2.06375          |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Sidewall Axial Length (cm)             | 119.6975         |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Bottom Thickness (cm)                  | 0.3175           |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Material                               | Aluminum         |                        |
   +----------------------+----------------------------------------+------------------+------------------------+
   | Liner                | Thickness (cm)                         | 0.10160          | Ref. 4_, pp. 140, 187  |
   |                      |                                        |                  | 217--218               |
   |                      +----------------------------------------+------------------+                        +
   |                      | Sidewall Axial Length (cm)             | 118.1100         |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Bottom Thickness (cm)                  | 0.1016           |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Material                               | Lead / Cadmium   |                        |
   +----------------------+----------------------------------------+------------------+------------------------+
   | Interior Fill        | Material                               | Air              | Ref. 4_, pp. 184--185  |
   +----------------------+----------------------------------------+------------------+------------------------+

Modified Three-Element Irradiator
----------------------------------

The modified three-element irradiation facility uses the same lattice positions, radial center,
and simplified grid-plate penetration as the conventional 3-EL. It contains concentric cadmium,
enriched-boron, and natural-boron-carbide filters surrounding an air-filled pneumatic transfer
passage. The baseline specification does not include a rabbit, sample container, or irradiated
specimen. The detailed specification in :numref:`table-modified-three-element-detailed-geometry` follows
the active modified-3-EL cell and surface cards in Hudson's later MCNP model (Ref. 4_).

.. table:: Detailed Modified 3-EL Geometry Specifications
   :name: table-modified-three-element-detailed-geometry

   +----------------------+----------------------------------------+------------------+------------------------+
   | Component            | Property                               | Value            | Reference              |
   +======================+========================================+==================+========================+
   | Outer Aluminum       | Tube #1 Inner Radius (cm)              | 2.23393          | Ref. 4_, pp. 186--187, |
   | Casing               +----------------------------------------+------------------+ 222, 228, 243          +
   |                      | Tube #1 Outer Radius (cm)              | 2.30759          |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Tube #1 Axial Length (cm)              | 124.77400        |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Tube #1 Bottom Axial Location          | Top of Bottom    |                        |
   |                      |                                        | Grid Plate       |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Tube #2 Outer Radius (cm)              | 2.38125          |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Tube #2 End-Cap Thickness (cm)         | 3.39830          |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Tube #2 Annulus Axial Length (cm)      | 81.27660         |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Tube #2 Solid / Annulus Interface      | Top of Tube #1   |                        |
   |                      | Axial Location                         |                  |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Material                               | Aluminum         |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Interior Fill Material                 | Air              |                        |
   +----------------------+----------------------------------------+------------------+------------------------+
   | Pneumatic System     | Tube Inner Radius (cm)                 | 0.67000          | Ref. 4_, pp. 186, 221  |
   |                      +----------------------------------------+------------------+                        +
   |                      | Tube Outer Radius (cm)                 | 0.79400          |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Sleeve Inner Radius (cm)               | 0.86350          |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Sleeve Outer Radius (cm)               | 0.95250          |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Open-Tube Axial Length (cm)            | 109.73188        |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Tube Lower-End-Cap Thickness (cm)      | 0.12400          |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Sleeve Lower-End-Cap Thickness (cm)    | 0.12850          |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Top Axial Location                     | Top of Tube #1   |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Tube and Sleeve Material               | Aluminum         |                        |
   +----------------------+----------------------------------------+------------------+------------------------+
   | B4C Canister         | B4C-Region Inner Radius (cm)           | 1.11125          | Ref. 4_, pp. 186, 221  |
   | (Upper Insert)       +----------------------------------------+------------------+                        +
   |                      | B4C-Region Outer Radius (cm)           | 1.89230          |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Canister Outer Radius (cm)             | 2.19009          |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Top-Cap Axial Thickness (cm)           | 0.19660          |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | B4C-Region Axial Thickness (cm)        | 52.00278         |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Bottom-Cap Axial Thickness (cm)        | 0.20000          |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Canister Top Alignment                 | Top of Tube #1   |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Canister Material                      | Aluminum         |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | B4C-Region Material                    | Natural B4C      |                        |
   +----------------------+----------------------------------------+------------------+------------------------+
   | B-10 Canister        | B-10 Annulus Inner Radius (cm)         | 1.03759          | Ref. 4_, pp. 186--187, |
   | (Lower Insert)       +----------------------------------------+------------------+ 221                    +
   |                      | Upper B-10 Outer Radius (cm)           | 2.00660          |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Lower B-10 Outer Radius (cm)           | 2.04724          |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Canister Exterior Wall Radius (cm)     | 2.12090          |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Cadmium-Sleeve Outer Radius (cm)       | 2.17090          |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Gap to B4C Canister (cm)               | 0.10000          |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Top-Cap Axial Thickness (cm)           | 2.54000          |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Upper B-10 Region Axial Thickness (cm) | 22.86000         |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Lower B-10 Region Axial Thickness (cm) | 34.92500         |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Canister Exterior Wall Lower-End-Cap   | 0.63500          |                        |
   |                      | Axial Thickness (cm)                   |                  |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Lower B-10 Solid-Section Axial         | 2.54000          |                        |
   |                      | Thickness (cm)                         |                  |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Cadmium-Sleeve Axial Extent            | Canister Top to  |                        |
   |                      |                                        | Bottom of B-10   |                        |
   |                      |                                        | Region           |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Canister and Sleeve Material           | Aluminum         |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | B-10 Region Material                   | Enriched Boron   |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Liner Material                         | Cadmium          |                        |
   +----------------------+----------------------------------------+------------------+------------------------+
   | Silver Disk          | Axial Thickness (cm)                   | 0.10000          | Ref. 4_, pp. 187, 221  |
   |                      +----------------------------------------+------------------+                        +
   |                      | Material                               | Silver           |                        |
   +----------------------+----------------------------------------+------------------+------------------------+
   | Cadmium Disk         | Axial Thickness (cm)                   | 0.10000          | Ref. 4_, pp. 187, 221  |
   |                      +----------------------------------------+------------------+                        +
   |                      | Material                               | Cadmium          |                        |
   +----------------------+----------------------------------------+------------------+------------------------+
   | Hollow Aluminum      | Hollow-Section Radius (cm)             | 2.03393          | Ref. 4_, pp. 187, 221  |
   | Spacer               +----------------------------------------+------------------+                        +
   |                      | Hollow-Section Axial Thickness (cm)    | 3.00000          |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Solid Upper-Cap Axial Thickness (cm)   | 0.49472          |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Hollow-Section Fill Material           | Air              |                        |
   |                      +----------------------------------------+------------------+                        +
   |                      | Spacer Material                        | Aluminum         |                        |
   +----------------------+----------------------------------------+------------------+------------------------+
   | Solid Aluminum       | Axial Thickness (cm)                   | 5.08000          | Ref. 4_, pp. 187, 222  |
   | Spacer               +----------------------------------------+------------------+                        +
   |                      | Material                               | Aluminum         |                        |
   +----------------------+----------------------------------------+------------------+------------------------+


An axially simplified version of the modified 3-EL is specified in
:numref:`table-modified-three-element-simplified-geometry`. The simplification reduces the
number of distinct axial regions from 20 to 10 by eliminating short axial features and making
small adjustments to selected radii to preserve the affected material volumes. The basis and
calculations for these changes are provided in the :ref:`simplified modified 3-EL derivation
<progression_problems_triga_netl_simplified_3l_derivation>`.

.. table:: Simplified Modified 3-EL Geometry Specifications
   :name: table-modified-three-element-simplified-geometry

   +----------------------+----------------------------------------------+-----------------------------------------------------------------+
   | Component            | Property                                     | Value                                                           |
   +======================+==============================================+=================================================================+
   | Outer Aluminum       | Casing-Tube Inner Radius (cm)                | 2.23393                                                         |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   | Casing               | Casing-Tube Outer Radius (cm)                | 2.35651                                                         |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | Casing-Tube Axial Length (cm)                | 124.77400                                                       |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | Casing-Tube Bottom Axial Location            | Top of Bottom Grid Plate                                        |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | Solid Upper-Portion Axial Thickness (cm)     | 3.39830                                                         |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | Solid Upper-Portion Location                 | Immediately Above Casing Tube                                   |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | Material                                     | Aluminum                                                        |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | Interior Fill Material                       | Air                                                             |
   +----------------------+----------------------------------------------+-----------------------------------------------------------------+
   | Pneumatic System     | Tube Inner Radius (cm)                       | 0.67015                                                         |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | Tube Outer Radius (cm)                       | 0.79400                                                         |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | Sleeve Inner Radius (cm)                     | 0.86182                                                         |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | Sleeve Outer Radius (cm)                     | 0.95250                                                         |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | Axial Length (cm)                            | 110.28438                                                       |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | Top Axial Location                           | Top of Casing Tube                                              |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | Tube and Sleeve Material                     | Aluminum                                                        |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | Central-Passage and Annular-Gap Fill         | Air                                                             |
   +----------------------+----------------------------------------------+-----------------------------------------------------------------+
   | B4C Canister         | B4C-Region Inner Radius (cm)                 | 1.11125                                                         |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   | (Upper Insert)       | B4C-Region Outer Radius (cm)                 | 1.88760                                                         |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | Canister Outer Radius (cm)                   | 2.19009                                                         |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | Canister and B4C-Region Axial Length (cm)    | 52.39938                                                        |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | Canister Top Alignment                       | Top of Casing Tube                                              |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | Canister Material                            | Aluminum                                                        |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | B4C-Region Material                          | Natural B4C                                                     |
   +----------------------+----------------------------------------------+-----------------------------------------------------------------+
   | B-10 Canister        | B-10 Annulus Inner Radius (cm)               | 1.03759                                                         |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   | (Lower Insert)       | B-10 Outer Radius (cm)                       | 2.02019                                                         |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | Canister Exterior Radius (cm)                | 2.11951                                                         |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | Cadmium-Sleeve Outer Radius (cm)             | 2.16895                                                         |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | Top-Cap Axial Thickness (cm)                 | 2.64000                                                         |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | Annular B-10 Region Axial Thickness (cm)     | 55.24500                                                        |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | Solid Lower B-10 Region Axial Thickness (cm) | 3.17500                                                         |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | Interior-Wall Axial Extent                   | Canister Top to Top of Solid Lower B-10 Region                  |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | Canister Top Alignment                       | Bottom of B4C Canister                                          |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | Cadmium-Sleeve Axial Extent                  | Complete Canister Length                                        |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | Canister and Interior-Wall Material          | Aluminum                                                        |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | B-10 Region Material                         | Enriched Boron                                                  |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | Sleeve Material                              | Cadmium                                                         |
   +----------------------+----------------------------------------------+-----------------------------------------------------------------+
   | Silver Disk          | Geometry and Material                        | See :numref:`table-modified-three-element-detailed-geometry`.   |
   +----------------------+----------------------------------------------+-----------------------------------------------------------------+
   | Cadmium Disk         | Geometry and Material                        | See :numref:`table-modified-three-element-detailed-geometry`.   |
   +----------------------+----------------------------------------------+-----------------------------------------------------------------+
   | Hollow Aluminum      | Hollow-Section Radius (cm)                   | 1.88448                                                         |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   | Spacer               | Axial Thickness (cm)                         | 3.49472                                                         |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | Hollow-Section Fill Material                 | Air                                                             |
   +                      +----------------------------------------------+-----------------------------------------------------------------+
   |                      | Spacer Material                              | Aluminum                                                        |
   +----------------------+----------------------------------------------+-----------------------------------------------------------------+
   | Solid Aluminum       | Geometry and Material                        | See :numref:`table-modified-three-element-detailed-geometry`.   |
   | Spacer               |                                              |                                                                 |
   +----------------------+----------------------------------------------+-----------------------------------------------------------------+


Material Compositions
=====================

This section specifies the base compositions of the materials specific to the NETL
TRIGA progression problems.  Materials from the above specification which are common to
other TRIGA progression problems are not repeated here, but may be found in the
:ref:`progression_problems_triga_material_compositions` section.

.. table:: CR Absorber Specifications
   :name: table-cr-absorber-specs

   +-------------------+-----------------------+----------------------+
   | Property          | Value                 | Reference            |
   +===================+=======================+======================+
   | Density (g/cc)    | 2.48                  | Ref. 2_, pg. 51      |
   +-------------------+---------+-------------+----------------------+
   | Composition       | B-10    | 0.1592      | Ref. 2_, pg. 60      |
   + (Iso ID, at%)     +---------+-------------+                      +
   |                   | B-11    | 0.6408      |                      |
   +                   +---------+-------------+                      +
   |                   | C-Nat   | 0.2         |                      |
   +-------------------+---------+-------------+----------------------+



.. table:: CR U-ZrH1.6 Specifications
   :name: table-ffcr-UZrH-specs

   +-------------------+----------------------------+----------------------+
   | Property          | Value                      | Reference            |
   +===================+============================+======================+
   | Density (g/cc)    | 6.0124                     | Ref. 2_, pg. 52      |
   +-------------------+----------------------------+----------------------+
   | Composition       | Same as                    | Ref. 2_, pg. 52      |
   | (Iso ID, at%)     | :numref:`table-UZrH-specs` |                      |
   +-------------------+----------------------------+----------------------+


.. table:: Cadmium Specifications
   :name: table-cadmium-specs

   +-------------------+-----------------------+----------------------+
   | Property          | Value                 | Reference            |
   +===================+=======================+======================+
   | Density (g/cc)    | 8.65                  | Ref. 2_, pg. 53      |
   +-------------------+---------+-------------+----------------------+
   | Composition       | Cd-106  | 0.0125      | Ref. 2_, pg. 60;     |
   + (Iso ID, at%)     +---------+-------------+                      +
   |                   | Cd-108  | 0.0089      |                      |
   +                   +---------+-------------+                      +
   |                   | Cd-110  | 0.1249      |                      |
   +                   +---------+-------------+                      +
   |                   | Cd-111  | 0.1280      |                      |
   +                   +---------+-------------+                      +
   |                   | Cd-112  | 0.2413      |                      |
   +                   +---------+-------------+                      +
   |                   | Cd-113  | 0.1222      |                      |
   +                   +---------+-------------+                      +
   |                   | Cd-114  | 0.2873      |                      |
   +                   +---------+-------------+                      +
   |                   | Cd-116  | 0.0749      |                      |
   +-------------------+---------+-------------+----------------------+


.. table:: Lead Specifications
   :name: table-lead-specs

   +-------------------+-----------------------+----------------------+
   | Property          | Value                 | Reference            |
   +===================+=======================+======================+
   | Density (g/cc)    | 11.35                 | Ref. 4_, pg. 187     |
   +-------------------+---------+-------------+----------------------+
   | Composition       | Pb-Nat  | 1.0         | Ref. 4_, pg. 270     |
   | (Iso ID, at%)     |         |             |                      |
   +-------------------+---------+-------------+----------------------+


The enriched-boron density is another difference between the source models. De Luna's embedded
MCNP model uses 1.55 g/cc, while the accompanying discussion reports a measured tapped-density
range of approximately 1.3--1.5 g/cc (Ref. 5_, pp. 45, 107). The progression-problem specification
uses Hudson's later value of 1.40 g/cc, which lies within that measured range.

.. table:: Enriched-Boron Powder Specifications
   :name: table-enriched-boron-powder-specs

   +-------------------+-----------------------+----------------------+
   | Property          | Value                 | Reference            |
   +===================+=======================+======================+
   | Density (g/cc)    | 1.40                  | Ref. 4_, pg. 187     |
   +-------------------+---------+-------------+----------------------+
   | Composition       | B-10    | 0.96        | Ref. 4_, pg. 277     |
   + (Iso ID, wt%)     +---------+-------------+                      +
   |                   | B-11    | 0.04        |                      |
   +-------------------+---------+-------------+----------------------+


.. table:: Natural-B4C Powder Specifications
   :name: table-natural-b4c-powder-specs

   +-------------------+-----------------------+----------------------+
   | Property          | Value                 | Reference            |
   +===================+=======================+======================+
   | Density (g/cc)    | 1.46                  | Ref. 4_, pg. 186     |
   +-------------------+---------+-------------+----------------------+
   | Composition       | B-10    | 0.159996    | Ref. 4_, pg. 269     |
   + (Iso ID, at%)     +---------+-------------+                      +
   |                   | B-11    | 0.639985    |                      |
   +                   +---------+-------------+                      +
   |                   | C-Nat   | 0.200019    |                      |
   +-------------------+---------+-------------+----------------------+


.. table:: Silver Specifications
   :name: table-silver-specs

   +-------------------+-----------------------+----------------------+
   | Property          | Value                 | Reference            |
   +===================+=======================+======================+
   | Density (g/cc)    | 10.49                 | Ref. 4_, pg. 187     |
   +-------------------+---------+-------------+----------------------+
   | Composition       | Ag-107  | 0.51839     | Ref. 4_, pg. 277     |
   + (Iso ID, wt%)     +---------+-------------+                      +
   |                   | Ag-109  | 0.48161     |                      |
   +-------------------+---------+-------------+----------------------+



References
==========

.. [1] "University of Texas at Austin Nuclear Engineering Teaching Laboratory
   TRIGA Research Reactor", August 2023,
   https://www.nrc.gov/docs/ML2327/ML23279A146.pdf

.. [2] D. R. Redhouse, et al., "Radiation Characterization Summary: NETL Beam Port
   1/5 Free-Field Environment at the 128-inch Core Centerline Adjacent Location,
   (NETL-FF-BP1/5-128-cca).", Nov. 2022. https://doi.org/10.2172/1898256

.. [3] J. A. Kulesza, et al., "MCNP® Code Version 6.3.1 Theory & User Manual",
       LA-UR-24-24602, Rev. 1, Los Alamos National Laboratory, Los Alamos,
       NM, USA (2024), https://www.osti.gov/biblio/2372634

.. [4] C. C. Hudson, "Development of a Radioisotope Production Facility Using a
   Cryogenic Cooling System", Ph.D. dissertation, The University of Texas at
   Austin, December 2025,
   https://repositories.lib.utexas.edu/items/6cd629db-6ab7-4ec3-920b-254b52cb7c45

.. [5] B. A. De Luna, "Design of an In-core Fission Spectrum Neutron Irradiation
   Facility with Pneumatic Sample Transfer at a Research Reactor", M.S.E. thesis,
   The University of Texas at Austin, 2019,
   https://repositories.lib.utexas.edu/bitstreams/e3f6e914-7811-4752-9650-0851d50978d8/download

See Also
========

* :ref:`NETL TRIGA Progression Problems <progression_problems_triga_netl>`
* :ref:`Python Tools for NETL TRIGA <python_tools_triga_netl>`
* :ref:`TRIGA-generic Specifications <progression_problems_triga>`
