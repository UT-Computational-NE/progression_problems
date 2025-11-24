.. _progression_problems_triga_netl_system_specifications:

=====================
System Specifications
=====================

This section contains system specifications for those elements which pertaining specifically
to the TRIGA reactor at the University of Texas at Austin's Nuclear Engineering Teaching and
Research Laboratory (NETL).

The reactor system consists of a core assembly of cylindrical fuel elements housed within a
hexagonal stainless steel shroud, which itself is surrounded by a graphite reflector, with the
whole assemblage submerged in a reactor pool.  The core elements are kept in position using upper and lower
grid plates which are located above and below the core, respectively.  Beam ports are located
at various radial locations through the reflector and adjacent to the core shroud to allow for neutron
irradiation of experiments.

A picture of the reactor pool area is provided in :numref:`figure-reactor-pool`, along with a diagram
of the reactor aerial layout in :numref:`figure-reactor-layout` and a schematic of the reactor core in
:numref:`figure-core-diagram`.

.. _figure-reactor-pool:

.. figure:: /_static/images/triga/netl/reactor_pool.png
   :align: center
   :width: 60%

   NETL TRIGA Reactor Pool (Ref. 1_).

.. _figure-reactor-layout:

.. figure:: /_static/images/triga/netl/reactor_layout.png
   :align: center
   :width: 60%

   Reactor Aerial Layout (Ref. 2_).

.. _figure-core-diagram:

.. figure:: /_static/images/triga/netl/core_diagram.png
   :align: center
   :width: 80%

   Reactor Core Diagram (Left) and Core Map (Right) (Ref. 2_).

Reactor Core
============

The reactor core consists of a hexagonal lattice arrangement of various insertable elements.
Some of the core locations may be occupied by fuel elements, graphite elements, experimental
inserts, or simply left "empty", while others are reserved specifically for control rods
or the central thimble.

The labeling of the incore locations may be found in :numref:`figure-core-diagram` (right).
Table :ref:`reserved-core-locations` lists the core locations which are reserved for specific
components, with all other locations available fillable with other insertable elements.
Table :ref:`table-core-geometry` provides other geometric specifications with regards to the
core.

The following section provides specifications for the various core elements to be used for
progression problem analysis. It should be noted that additional core elements not listed
here may be present in the actual reactor core such as experimental inserts (7L & 3L Facilities)
and Pneumatic Sample Transit tubes, but these are not included in the current progression
problem definitions.

.. table:: Reserved Core Locations
   :name: reserved-core-locations

   +------------------------------------------------+-----------+--------------------+
   | Component Type                                 | Location  | Reference          |
   +===============+================================+===========+====================+
   | Central Thimble                                | A-01      | Ref. 2_, pg. 4-9   |
   +---------------+--------------------------------+-----------+--------------------+
   | Transient Control Rod                          | C-01      | Ref. 2_, Fig. 4.4  |
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


.. table:: Core Geometry Specifications
   :name: table-core-geometry

   +------------------------+-------------+------------------+
   | Property               | Value       | Reference        |
   +========================+=============+==================+
   | Hex Lattice Pitch (in) | 1.714       | Ref. 3_, pg. 54  |
   +------------------------+-------------+------------------+

Fuel Element
------------

see: :ref:`progression_problems_triga_fuel_element`

Graphite Element
----------------

see: :ref:`progression_problems_triga_graphite_element`

Transient Control Rod
----------------------

The Transient Control Rod (TCR) is a solid boron-carbide cylinder clad in aluminum and operated pneumatically
to enable rapid position changes for inducing reactor pulses. During steady-state operation, it functions
as an alternate safety rod, held in a partially (or fully) withdrawn position by continuous air supply.
In the event of a scram, the air is released, allowing gravity to insert the rod fully into the core.

General geometric specifications relevant to the NETL TRIGA progression problems are summarized in
:numref:`table-transient-control-rod`, and the axial configuration of the transient rod is depicted in
:numref:`figure-transient-control-rod-axial_profile`.  The axial positioning of the TCR within the core is
assumed such that the center of the absorber material aligns with the axial center of the fuel element
when the rod is fully inserted.  The maximum travel distance of the TCR is 15.0 inches (Ref. 2_, pg. 4-10).

.. table:: Transient Control Rod Geometry Specifications
   :name: table-transient-control-rod

   +---------------+----------------------+--------------------+----------------------+
   | Component     | Property             | Value              | Reference            |
   +===============+======================+====================+======================+
   | Cladding      | Thickness (in.)      | 0.028              | Ref. 2_, Table 4.2   |
   |               +----------------------+--------------------+----------------------+
   |               | Outer Diameter (in.) | 1.25               | Ref. 2_, Table 4.2   |
   |               +----------------------+--------------------+----------------------+
   |               | Material             | Aluminum           | Ref. 3_, pg. 51      |
   +---------------+----------------------+--------------------+----------------------+
   | Element Plugs | Thickness (in.)      | 0.5                | Ref. 3_, pg. 58      |
   |               +----------------------+--------------------+----------------------+
   |               | Material             | Aluminum           | Ref. 3_, pg. 51      |
   +---------------+----------------------+--------------------+----------------------+
   | Magneform     | Thickness (in.)      | 1.0                | Ref. 3_, pg. 58      |
   | Fittings      +----------------------+--------------------+----------------------+
   |               | Material             | Aluminum           | Ref. 3_, pg. 51      |
   +---------------+----------------------+--------------------+----------------------+
   | Absorber      | Diameter (in.)       | 1.187              | Ref. 3_, pg. 55      |
   |               +----------------------+--------------------+----------------------+
   |               | Length (in.)         | 15.0               | Ref. 2_, Table 4.2   |
   |               +----------------------+--------------------+----------------------+
   |               | Material             | CR Absorber        | Ref. 3_, pg. 51      |
   +---------------+----------------------+--------------------+----------------------+
   | Air Follower  | Length (in.)         | 19.75              | Ref. 2_, pg. 58      |
   +---------------+----------------------+--------------------+----------------------+
   | Fill Gas      | Material             | Air                | Ref. 3_, pg. 51      |
   +---------------+----------------------+--------------------+----------------------+


.. _figure-transient-control-rod-axial_profile:

.. figure:: /_static/images/triga/netl/transient_control_rod_axial_diagram.png
   :align: center
   :width: 60%

   Diagram of Transient Control Rod Axial Profile.


Fuel Follower Control Rod
-------------------------

Fuel Follower Control Rods (FFCRs) are solid boron-carbide cylinders clad in stainless-steel.
Unlike the TCR, the FFCRs are not pneumatically operated; instead, they are mechanically coupled to
control rod drive mechanisms which allows for controlled insertion and withdrawal from the core.
Additionally, the FFCRs are designed with a fuel follower section such that as the control material
is withdrawn from the core, a section of fuel element will follow it.  The Shim 1 and Shim 2 control
rods as well as the Regulating control rod are all FFCRs.

General geometric specifications relevant to the NETL TRIGA progression problems are summarized in
:numref:`table-fuel-follower-control-rod`, and the axial configuration of the transient rod is depicted in
:numref:`figure-fuel-follower-control-rod-axial_profile`.  The axial positioning of the FFCRs within the core are
assumed such that the center of the absorber material aligns with the axial center of the fuel element when the
rods are fully inserted.  The maximum travel distance for FFCRs is 15.0 inches (Ref. 2_, pg. 4-10).

.. table:: Fuel Follower Control Rod Geometry Specifications
   :name: table-fuel-follower-control-rod

   +-------------------+------------------------+--------------------+----------------------+
   | Component         | Property               | Value              | Reference            |
   +===================+========================+====================+======================+
   | Cladding          | Thickness (in.)        | 0.02               | Ref. 3_, pg. 55      |
   |                   +------------------------+--------------------+----------------------+
   |                   | Outer Diameter (in.)   | 1.35               | Ref. 3_, pg. 55      |
   |                   +------------------------+--------------------+----------------------+
   |                   | Material               | Stainless Steel    | Ref. 3_, pg. 52      |
   +-------------------+------------------------+--------------------+----------------------+
   | Element Plugs     | Upper Thickness (in.)  | 1.5                | Ref. 3_, pg. 58      |
   |                   +------------------------+--------------------+----------------------+
   |                   | Lower Thickness (in.)  | 0.5                | Ref. 3_, pg. 58      |
   |                   +------------------------+--------------------+----------------------+
   |                   | Material               | Stainless Steel    | Ref. 3_, pg. 51      |
   +-------------------+------------------------+--------------------+----------------------+
   | Magneform         | Upper Thickness (in.)  | 0.5                | Ref. 3_, pg. 58      |
   | Fittings          +------------------------+--------------------+----------------------+
   |                   | Middle Thickness (in.) | 0.5                | Ref. 3_, pg. 58      |
   |                   +------------------------+--------------------+----------------------+
   |                   | Lower Thickness (in.)  | 1.0                | Ref. 3_, pg. 58      |
   |                   +------------------------+--------------------+----------------------+
   |                   | Material               | Stainless Steel    | Ref. 3_, pg. 51      |
   +-------------------+------------------------+--------------------+----------------------+
   | Absorber          | Diameter (in.)         | 1.3                | Ref. 3_, pg. 55      |
   |                   +------------------------+--------------------+----------------------+
   |                   | Length (in.)           | 15.0               | Ref. 3_, pg. 58      |
   |                   +------------------------+--------------------+----------------------+
   |                   | Material               | CR Absorber        | Ref. 3_, pg. 52      |
   +-------------------+------------------------+--------------------+----------------------+
   | Fuel Follower     | Inner Diameter (in.)   | 0.25               | Ref. 3_, pg. 55      |
   |                   +------------------------+--------------------+----------------------+
   |                   | Length (in.)           | 15.0               | Ref. 3_, pg. 58      |
   |                   +------------------------+--------------------+----------------------+
   |                   | Material               | CR U-ZrH1.6        | Ref. 3_, pg. 52      |
   +-------------------+------------------------+--------------------+----------------------+
   | Zr Fill Rod       | Diameter (in.)         | 0.25               | Ref. 3_, pg. 55      |
   |                   +------------------------+--------------------+----------------------+
   |                   | Material               | Zirconium          | Ref. 3_, pg. 52      |
   +-------------------+------------------------+--------------------+----------------------+
   | Air Gaps          | Upper Gap              | 3.5                | Ref. 3_, pg. 58      |
   |                   +------------------------+--------------------+----------------------+
   |                   | Above Absorber (in.)   | 0.125              | Ref. 3_, pg. 58      |
   |                   +------------------------+--------------------+----------------------+
   |                   | Above Fuel Follower    | 0.25               | Ref. 3_, pg. 58      |
   |                   | (in.)                  |                    |                      |
   |                   +------------------------+--------------------+----------------------+
   |                   | Lower Gap              | 5.375              | Ref. 3_, pg. 58      |
   +-------------------+------------------------+--------------------+----------------------+
   | Fill Gas          | Material               | Air                | Ref. 3_, pg. 51      |
   +-------------------+------------------------+--------------------+----------------------+


.. _figure-fuel-follower-control-rod-axial_profile:

.. figure:: /_static/images/triga/netl/fuel_follower_control_rod_axial_diagram.png
   :align: center
   :width: 60%

   Diagram of Fuel Follower Control Rod Axial Profile.


Source Holder
-------------

The source holder is an aluminum cylinder designed to hold a neutron source for monitoring
core reactivity during core shutdown and approach-to-criticality.  The source itself is
positioned within a cylindrical cavity inside the source holder.  The source holder may be
inserted into any core fuel-element location.  The source holder extends down from the upper
grid plate to just above the lower grid plate (Ref. 3_, pg. 55).

General geometric specifications relevant to the NETL TRIGA progression problems are summarized in
:numref:`table-source-holder`.

.. table:: Source Holder Geometry Specifications
   :name: table-source-holder

   +---------------+----------------------+--------------------+----------------------+
   | Component     | Property             | Value              | Reference            |
   +===============+======================+====================+======================+
   | Cladding      | Outer Diameter (in.) | 1.435              | Ref. 3_, pg. 54-55   |
   |               +----------------------+--------------------+----------------------+
   |               | Material             | Aluminum           | Ref. 3_, pg. 54      |
   +---------------+----------------------+--------------------+----------------------+
   | Cavity        | Diameter (in.)       | 0.981              | Ref. 2_, Sec. 4.2.5  |
   |               +----------------------+--------------------+----------------------+
   |               | Length (in.)         | 3.0                | Ref. 2_, Sec. 4.2.5  |
   |               +----------------------+--------------------+----------------------+
   |               | Core Axial Center    | 0.0                | Ref. 3_, pg. 55      |
   |               | Offset (in.)         |                    |                      |
   |               +----------------------+--------------------+----------------------+
   |               | Material             | Air                | Ref. 3_, pg. 54      |
   +---------------+----------------------+--------------------+----------------------+
   | Bottom of     | Distance from Lower  | 1.1934             | Ref. 3_, pg. 55      |
   | Source Holder | Grid Plate (cm)      |                    |                      |
   +---------------+----------------------+--------------------+----------------------+

Central Thimble
---------------

The central thimbles is an aluminum tube extending through the central penetrations of
the top and bottom grid plates.  This central thimble allows for the irradiation of
experiments at the point of maximum neutron flux in the core.

General geometric specifications relevant to the NETL TRIGA progression problems are summarized in
:numref:`table-central-thimble`.

.. table:: Central Thimble Geometry Specifications
   :name: table-central-thimble

   +---------------+----------------------+--------------------+----------------------+
   | Component     | Property             | Value              | Reference            |
   +===============+======================+====================+======================+
   | Cladding      | Inner Diameter (in.) | 1.33               | Ref. 2_, Sec.10.2.1.b|
   |               +----------------------+--------------------+----------------------+
   |               | Outer Diameter (in.) | 1.5                | Ref. 2_, Sec.10.2.1.b|
   |               +----------------------+--------------------+----------------------+
   |               | Material             | Aluminum           | Ref. 3_, pg. 51      |
   +---------------+----------------------+--------------------+----------------------+

Shroud
======

The core shroud is an aluminum structure which surrounds the core to help direct coolant flow
through the reactor region.  The shroud shape is that of an irregular dodecagon formed by the
intersection of two regular hexagons, one larger and one smaller, rotated 30 degrees relative
to each other.  The shroud is oriented such that beam port 1/5 is parallel to one of the long
sides of the dodecagon.

General geometric specifications relevant to the NETL TRIGA progression problems are summarized in
:numref:`table-shroud`.  An picture of the shroud is provided in :numref:`figure-shroud`.

.. _figure-shroud:

.. figure:: /_static/images/triga/netl/shroud.png
   :align: center
   :width: 60%

   Picture of the Inner Shroud Surface (Ref. 2_).

.. table:: Shroud Geometry Specifications
   :name: table-shroud

   +---------------+----------------------+--------------------+----------------------+
   | Component     | Property             | Value              | Reference            |
   +===============+======================+====================+======================+
   | Shroud        | Thickness (in.)      | 0.1875             | Ref. 3_, pg. 54-55   |
   |               +----------------------+--------------------+----------------------+
   |               | Height (in.)         | 23.13              | Ref. 3_, pg. 55      |
   |               +----------------------+--------------------+----------------------+
   |               | Large Hexagon        | 10.75              | Ref. 3_, pg. 54      |
   |               | Inradius (in.)       |                    |                      |
   |               +----------------------+--------------------+----------------------+
   |               | Small Hexagon        | 10.21875           | Ref. 3_, pg. 55      |
   |               | Inradius (in.)       |                    |                      |
   |               +----------------------+--------------------+----------------------+
   |               | Material             | Aluminum           | Ref. 3_, pg. 48      |
   +---------------+----------------------+--------------------+----------------------+


Grid Plates
===========

The upper and lower grid plates are aluminum structures which provide alignment support
for the core elements.  The grid plates contain a hexagonal array of cylindrical holes
which correspond to the core lattice locations.  The grid plates also provide flow channels
for coolant to pass through the core region.

General geometric specifications relevant to the NETL TRIGA progression problems are summarized in
:numref:`table-grid-plates`.

.. table:: Grid Plates Geometry Specifications
   :name: table-grid-plates

   +---------------+---------------------------+--------------------+----------------------+
   | Component     | Property                  | Value              | Reference            |
   +===============+===========================+====================+======================+
   | Upper Grid    | Thickness (in.)           | 0.62               | Ref. 3_, pg. 55      |
   | Plate         +---------------------------+--------------------+----------------------+
   |               | Fuel Element Penetration  | 1.505              | Ref. 2_, Sec. 4.2.4.a|
   |               | Diameter (in.)            |                    |                      |
   |               +---------------------------+--------------------+----------------------+
   |               | Control Rod Penetration   | 1.505              | Ref. 2_, Sec. 4.2.4.a|
   |               | Diameter (in.)            |                    |                      |
   |               +---------------------------+--------------------+----------------------+
   |               | Distance from Core        | 12.75              | Ref. 3_, pg. 55      |
   |               | Axial Centerline (in.)    |                    |                      |
   |               +---------------------------+--------------------+----------------------+
   |               | Material                  | Aluminum           | Ref. 3_, pg. 50      |
   +---------------+---------------------------+--------------------+----------------------+
   | Lower Grid    | Thickness (in.)           | 1.25               | Ref. 3_, pg. 55      |
   | Plate         +---------------------------+--------------------+----------------------+
   |               | Fuel Element Penetration  | 1.25               | Ref. 2_, Sec. 4.2.4.b|
   |               | Diameter (in.)            |                    |                      |
   |               +---------------------------+--------------------+----------------------+
   |               | Control Rod Penetration   | 1.505              | Ref. 2_, Sec. 4.2.4.b|
   |               | Diameter (in.)            |                    |                      |
   |               +---------------------------+--------------------+----------------------+
   |               | Distance from Core        | 13.06              | Ref. 3_, pg. 55      |
   |               | Axial Centerline (in.)    |                    |                      |
   |               +---------------------------+--------------------+----------------------+
   |               | Material                  | Aluminum           | Ref. 3_, pg. 50      |
   +---------------+---------------------------+--------------------+----------------------+

Rotary Specimen Rack
====================

The Rotary Specimen Rack (RSR) is an air-filled water-tight canister enclosing a sample rack with
a pinion drive assembly attached to the sample rack.  The sample rack is an assemblage of upper and
lower rings attached to tubes with the tubes designed to hold specimens for irradiation.

General geometric specifications relevant to the NETL TRIGA progression problems are summarized in
:numref:`table-rotary-specimen-rack`.

.. table:: Rotary Specimen Rack Geometry Specifications
   :name: table-rotary-specimen-rack

   +---------------+----------------------+--------------------+----------------------+
   | Component     | Property             | Value              | Reference            |
   +===============+======================+====================+======================+
   | Cavity        | Outer Diameter (in.) | 28.625             | Ref. 3_, pg. 55      |
   |               +----------------------+--------------------+----------------------+
   |               | Height (in.)         | 10.8174            | Ref. 3_, pg. 55      |
   |               +----------------------+--------------------+----------------------+
   |               | Material             | Air                | Ref. 3_, pg. 48      |
   +---------------+----------------------+--------------------+----------------------+
   | Specimen      | Number of Tubes      | 40                 | Ref. 2_, pg. 10-27   |
   | Tubes         +----------------------+--------------------+----------------------+
   |               | Outer Diameter (in.) | 1.0                | Ref. 3_, pg. 56-57   |
   |               +----------------------+--------------------+----------------------+
   |               | Wall Thickness (in.) | 0.058              | Ref. 2_, pg. 10-27   |
   |               +----------------------+--------------------+----------------------+
   |               | Tube-to-Center       | 26.312 * 0.5       | Ref. 2_, pg. 10-27   |
   |               | Distance (in.)       |                    |                      |
   |               +----------------------+--------------------+----------------------+
   |               | Material             | Aluminum           | (assumed)            |
   +---------------+----------------------+--------------------+----------------------+

Reflector
=========

The reflector is a graphite structure which surrounds the core shroud and acts as both
moderator and reflector for neutrons emitted from the core to improve neutron economy.  The
reflector has holes to accommodate the various beam ports which penetrate through the reflector
to allow for neutron irradiation of experiments.

General geometric specifications relevant to the NETL TRIGA progression problems are summarized in
:numref:`table-reflector`.  An picture of the reflector canister and reflector are provided in
:numref:`figure-reflector-canister`.

.. _figure-reflector-canister:

.. figure:: /_static/images/triga/netl/reflector_canister.png
   :align: center
   :width: 60%

   Pictures of Reflector and Reflector Canister (Ref. 2_).

.. table:: Reflector Geometry Specifications
   :name: table-reflector

   +-------------------+----------------------+--------------------+----------------------+
   | Component         | Property             | Value              | Reference            |
   +===================+======================+====================+======================+
   | Reflector         | Diameter (in.)       | 42.0               | Ref. 3_, pg. 54      |
   |                   +----------------------+--------------------+----------------------+
   |                   | Height (in.)         | 23.13              | Ref. 3_, pg. 55      |
   |                   +----------------------+--------------------+----------------------+
   |                   | Core Axial Centerline| 0.565              | Ref. 3_, pg. 55      |
   |                   | Offset (in.)         |                    |                      |
   |                   +----------------------+--------------------+----------------------+
   |                   | Material             | Graphite           | Ref. 3_, pg. 48      |
   +-------------------+----------------------+--------------------+----------------------+

Beam Ports
==========

The Beam Ports are cylindrical aluminum tubes which penetrate through the concrete shield, water
tank, and graphite reflector to accommodate neutron irradiation experiments.  The beam ports are air-filled
and allow for specimens and / or equipment to be placed inside the beam port, or outside the beam port
in a neutron beam from the beam port.  The locations of the beam ports and their orientations are shown
in :numref:`figure-reactor-layout` and :numref:`figure-core-diagram`.

Beam Port 1 is connected to Beam Port 5, forming a through port, which penetrates the graphite reflector
tangentially to the core.  This configuration allows for placing specimen adjacent to the core as well as
providing a beam of thermal neutrons with low fast-neutron and gamma-ray contamination.

Beam Port 2 is a tangential beam port terminating at the outer edge of the reflector.  This tangential
configuration provides a softer beam of neutrons due to the scattering required to direct neutrons down
the axis of the beam port.

Beam Port 3 is a radial beam port that "pierces the graphite reflector" and terminates at the inner edge of the
reflector.  This beam port provides access to a core adjacent location as well as a neutron beam with
relatively high fluxes of fast-neutrons and gamma-rays due to its direct orientation with respect to the core.

Beam Port 4 is another radial beam port that terminates at the outer edge of the reflector.  This beam port
provides a neutron beam with a harder spectrum due to direct line-of-sight to the core.

General geometric specifications relevant to the NETL TRIGA progression problems are summarized in
:numref:`table-beam-ports`.  Translations and rotations of the beam ports are provided with respect to the core
orientation shown in :numref:`figure-core-diagram`, with alignment with the Y-axis denoting no rotation.
Translations and rotations are provided in the manner consistent with MCNP transformations, with rotations being
applied first and translations second.

.. table:: Beam Ports Geometry Specifications
   :name: table-beam-ports

   +---------------+-----------------------+--------------------+-------------------------+
   | Component     | Property              | Value              | Reference               |
   +===============+=======================+====================+=========================+
   | All Beam Ports| Inner Diameter (in.)  | 6.065              | Ref. 3_, Fig. 4 & 5     |
   |               +-----------------------+--------------------+-------------------------+
   |               | Outer Diameter (in.)  | 6.625              | Ref. 3_, Fig. 4 & 5     |
   |               +-----------------------+--------------------+-------------------------+
   |               | Core Axial Centerline | -6.985             | Ref. 3_, pg. 56, 59     |
   |               | Offset (cm)           |                    |                         |
   |               +-----------------------+--------------------+-------------------------+
   |               | Tube Material         | Aluminum           | Ref. 3_, pg. 48         |
   |               +-----------------------+--------------------+-------------------------+
   |               | Fill Material         | Air                | Ref. 3_, pg. 48         |
   +---------------+-----------------------+--------------------+-------------------------+
   | Beam Port 1   | Rotation Matrix       | None               | Ref. 3_, pg. 48, 56     |
   |               | (degrees)             |                    |                         |
   |               +-----------------------+--------------------+-------------------------+
   |               | Radial Translation    | (35.2425, 0.0)     | Ref. 3_, pg. 48, 56     |
   |               | Vector (cm)           |                    |                         |
   +---------------+-----------------------+--------------------+-------------------------+
   | Beam Port 2   | Rotation Matrix       | 150  60  90        | Ref. 3_, pg. 48, 56, 59 |
   |               | (degrees)             | 120 150  90        |                         |
   |               |                       | 90  90   0         |                         |
   |               +-----------------------+--------------------+-------------------------+
   |               | Radial Translation    | (6.222, 35.255)    | Ref. 3_, pg. 48, 56, 59 |
   |               | Vector (cm)           |                    |                         |
   |               +-----------------------+--------------------+-------------------------+
   |               | Termination X-Plane   | x0 = -12.621       | Ref. 3_, pg. 48, 56, 59 |
   |               +-----------------------+--------------------+-------------------------+
   |               | Termination X-Plane   | 20 125  90         | Ref. 3_, pg. 48, 56, 59 |
   |               | Rotation Matrix       | 100  20  90        |                         |
   |               | (degrees)             | 90  90   0         |                         |
   +---------------+-----------------------+--------------------+-------------------------+
   | Beam Port 3   | Rotation Matrix       | 90 180  90         | Ref. 3_, pg. 48, 56     |
   |               | (degrees)             | 0  90  90          |                         |
   |               |                       | 90  90   0         |                         |
   |               +-----------------------+--------------------+-------------------------+
   |               | Radial Translation    | None               | Ref. 3_, pg. 48, 56     |
   |               | Vector (cm)           |                    |                         |
   |               +-----------------------+--------------------+-------------------------+
   |               | Terminates at         | Shroud Outer Wall  | Ref. 3_, pg. 48, 56, 59 |
   +---------------+-----------------------+--------------------+-------------------------+
   | Beam Port 4   | Rotation Matrix       | 75  60  90         | Ref. 3_, pg. 48, 56, 59 |
   |               | (degrees)             | 120  75  90        |                         |
   |               |                       | 90  90   0         |                         |
   |               +-----------------------+--------------------+-------------------------+
   |               | Radial Translation    | (-13.216, 22.871)  | Ref. 3_, pg. 48, 56, 59 |
   |               | Vector (cm)           |                    |                         |
   |               +-----------------------+--------------------+-------------------------+
   |               | Terminates at         | Shroud Outer Wall  | Ref. 3_, pg. 48, 56, 59 |
   +---------------+-----------------------+--------------------+-------------------------+


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
   | Density (g/cc)    | 2.48                  | Ref. 3_, pg. 51      |
   +-------------------+---------+-------------+----------------------+
   | Composition       | B-10    | 0.1592      | Ref. 3_, pg. 60      |
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
   | Density (g/cc)    | 6.0124                     | Ref. 3_, pg. 52      |
   +-------------------+----------------------------+----------------------+
   | Composition       | Same as                    | Ref. 3_, pg. 52      |
   | (Iso ID, at%)     | :numref:`table-UZrH-specs` |                      |
   +-------------------+----------------------------+----------------------+




References
==========

.. [1] https://www.me.utexas.edu/research/research-topics/nuclear-and-radiation-engineering

.. [2] "University of Texas at Austin Nuclear Engineering Teaching Laboratory
   TRIGA Research Reactor", August 2023,
   https://www.nrc.gov/docs/ML2327/ML23279A146.pdf

.. [3] D. R. Redhouse, et al., "Radiation Characterization Summary: NETL Beam Port
   1/5 Free-Field Environment at the 128-inch Core Centerline Adjacent Location,
   (NETL-FF-BP1/5-128-cca).", Nov. 2022. https://doi.org/10.2172/1898256

See Also
========

* :ref:`NETL TRIGA Progression Problems <progression_problems_triga_netl>`
* :ref:`Python Tools for NETL TRIGA <python_tools_triga_netl>`
* :ref:`TRIGA-generic Specifications <progression_problems_triga>`