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
this inner tube, wraps it with cadmium, and places the assembly concentrically inside a larger aluminum
tube. The annulus between the cadmium and the larger tube is air-filled.

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
   | Shock/        | Axial Thickness (cm)           | 5.1308           | Ref. 2_, pp. 53--55|
   | Terminus      +--------------------------------+------------------+                    |
   | Section       | Outer Diameter (in.)           | 0.875            |                    |
   |               +--------------------------------+------------------+                    |
   |               | Material                       | Aluminum         |                    |
   +---------------+--------------------------------+------------------+--------------------+
   | Connecting    | Axial Thickness (cm)           | 4.1725           | Ref. 2_, pp. 53--55|
   | Section       +--------------------------------+------------------+                    |
   |               | Outer Diameter (in.)           | 1.250            |                    |
   |               +--------------------------------+------------------+                    |
   |               | Material                       | Aluminum         |                    |
   +---------------+--------------------------------+------------------+--------------------+
   | Lower Section | Axial Thickness (cm)           | 8.3259           | Ref. 2_, pp. 53--55|
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
   | Empty Tube    | Bottom Axial Location Relative | -18.7182         | Ref. 2_, pp. 53--55|
   | Section       | to Core Midplane (cm)          |                  |                    |
   |               +--------------------------------+------------------+--------------------+
   |               | Bore Diameter (in.)            | 0.685            | Ref. 1_, Table 10.3|
   |               |                                |                  | Ref. 2_, pg. 55    |
   |               +--------------------------------+------------------+--------------------+
   |               | Bore Material                  | Air              | Ref. 2_, pg. 53    |
   |               +--------------------------------+------------------+--------------------+
   |               | Inner-Tube Outer Diameter (in.)| 0.875            | Ref. 1_, Table 10.3|
   |               |                                |                  | Ref. 2_, pg. 55    |
   |               +--------------------------------+------------------+--------------------+
   |               | Inner-Tube Material            | Aluminum         | Ref. 2_, pg. 53    |
   +---------------+--------------------------------+------------------+--------------------+
   | Cd-Wrapped    | Start of Section               | Top of Upper     | Ref. 2_, pg. 53    |
   | Section       |                                | Grid Plate       |                    |
   |               +--------------------------------+------------------+--------------------+
   |               | Cd-Wrap Outer Diameter (in.)   | 0.955            | Ref. 2_, pg. 55    |
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
   | Upper Shock   | Axial Thickness (cm)           | 2.5400           | Ref. 2_, pp. 53--55|
   | Section       +--------------------------------+------------------+                    |
   |               | Outer Diameter (in.)           | 1.250            |                    |
   |               +--------------------------------+------------------+                    |
   |               | Material                       | Aluminum         |                    |
   +---------------+--------------------------------+------------------+--------------------+
   | Cd Disk       | Axial Thickness (cm)           | 0.0508           | Ref. 2_, pp. 53--55|
   | Section       +--------------------------------+------------------+                    |
   |               | Cd Disk Diameter (in.)         | 0.685            |                    |
   |               +--------------------------------+------------------+                    |
   |               | Cd Disk Material               | Cadmium          |                    |
   |               +--------------------------------+------------------+                    |
   |               | Aluminum Annulus Outer         | 0.875            |                    |
   |               | Diameter (in.)                 |                  |                    |
   |               +--------------------------------+------------------+                    |
   |               | Annulus Material               | Aluminum         |                    |
   +---------------+--------------------------------+------------------+--------------------+
   | Lower Shock   | Axial Thickness (cm)           | 2.5400           | Ref. 2_, pp. 53--55|
   | Section       +--------------------------------+------------------+                    |
   |               | Outer Diameter (in.)           | 1.435            |                    |
   |               +--------------------------------+------------------+                    |
   |               | Material                       | Aluminum         |                    |
   +---------------+--------------------------------+------------------+--------------------+
   | Connecting    | Axial Thickness (cm)           | 4.1725           | Ref. 2_, pp. 53--55|
   | Section       +--------------------------------+------------------+                    |
   |               | Outer Diameter (in.)           | 1.250            |                    |
   |               +--------------------------------+------------------+                    |
   |               | Material                       | Aluminum         |                    |
   +---------------+--------------------------------+------------------+--------------------+
   | Lower Section | Axial Thickness (cm)           | 8.3259           | Ref. 2_, pp. 53--55|
   |               +--------------------------------+------------------+                    |
   |               | Outer Diameter (in.)           | 1.435            |                    |
   |               +--------------------------------+------------------+                    |
   |               | Material                       | Aluminum         |                    |
   +---------------+--------------------------------+------------------+--------------------+


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

See Also
========

* :ref:`NETL TRIGA Progression Problems <progression_problems_triga_netl>`
* :ref:`Python Tools for NETL TRIGA <python_tools_triga_netl>`
* :ref:`TRIGA-generic Specifications <progression_problems_triga>`
