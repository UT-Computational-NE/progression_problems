.. _progression_problems_triga_system_specifications:

=====================
System Specifications
=====================

This section contains system specifications for those elements which are generally common to
all TRIGA reactors.  Those specifications which are specific to certain TRIGA designs are located
in their respective sub-sections.

Fuel Element
============

The TRIGA fuel is composed of uranium uniformly dispersed within a zirconium-hydride matrix. Each Standard Fuel Element (SFE)
consists of an annular section of this fuel-moderator material, with a central hole that accommodates a zirconium filler rod.
The fuel region is encapsulated within a stainless-steel cladding tube, and the sealed volume surrounding the fuel contains a
fill gas occupying both the radial and axial gaps to accommodate thermal expansion and fission gas release. The fuel is axially
centered by graphite reflectors located at both the upper and lower ends. A gas gap is positioned above the upper reflector to
allow for additional expansion, while a molybdenum disc is placed above the lower reflector to protect the lower graphite section
from potential damage.

End fixtures are welded to both ends of the cladding tube to provide structural support and facilitate coolant flow. Specifically,
the lower end fixture supports the element on the lower grid plate, while the upper end fixture centers the element within the
upper grid plate, provides a flow path for coolant through the top grid plate, and serves as an attachment point for fuel handling
tools. In Instrumented Fuel Elements (IFEs), which contain thermocouples embedded within the fuel matrix, the upper end fixture
also provides a conduit for thermocouple lead wires.

Three distinct end fixture designs have been fabricated—referred to as original, integral, and streamlined—as illustrated in
:numref:`figure-fuel-elements`. General geometric specifications relevant to the TRIGA progression problems are summarized in
:numref:`table-fuel-element`, and the axial configuration of the fuel element is depicted in :numref:`figure-fuel-element-axial_profile`.

.. _figure-fuel-elements:

.. figure:: /_static/images/triga/fuel_element_variations.png
   :align: center
   :width: 60%

   Variations of TRIGA Fuel Elements [1]_.


.. table:: Mark III Fuel Element Geometry Specifications
   :name: table-fuel-element

   +---------------+--------------------------------+------------------+--------------------+
   | Component     | Property                       | Value            | Reference          |
   +===============+================================+==================+====================+
   | Fuel Meat     | Inner Diameter (in.)           | 0.25             | Ref. 1_, pg. 4-2   |
   |               +--------------------------------+------------------+--------------------+
   |               | Outer Diameter (in.)           | 1.435            | Ref. 1_, Table 4.1 |
   |               +--------------------------------+------------------+--------------------+
   |               | Length (in.)                   | 15.0             | Ref. 1_, Table 4.1 |
   |               +--------------------------------+------------------+--------------------+
   |               | Material                       | U-ZrH1.6         | Ref. 1_, pg. 4-2   |
   +---------------+--------------------------------+------------------+--------------------+
   | Zr Filler     | Diameter (in.)                 | 0.25             | Ref. 2_, pg. 55    |
   | Rod           +--------------------------------+------------------+--------------------+
   |               | Material                       | Zirconium        | Ref. 1_, Table 4.1 |
   +---------------+--------------------------------+------------------+--------------------+
   | Cladding      | Thickness (in.)                | 0.02             | Ref. 1_, Table 4.1 |
   |               +--------------------------------+------------------+--------------------+
   |               | Outer Diameter (in.)           | 1.475            | Ref. 1_, Table 4.1 |
   |               +--------------------------------+------------------+--------------------+
   |               | Material                       | Stainless-Steel  | Ref. 1_, Table 4.1 |
   +---------------+--------------------------------+------------------+--------------------+
   | Graphite      | Diameter (in.)                 | 1.430            | Ref. 1_, pg. 4-4   |
   | Reflector     +--------------------------------+------------------+--------------------+
   |               | Upper Reflector Thickness (in.)| 2.56             | Ref. 2_, pg. 55    |
   |               +--------------------------------+------------------+--------------------+
   |               | Lower Reflector Thickness (in.)| 3.72             | Ref. 2_, pg. 55    |
   |               +--------------------------------+------------------+--------------------+
   |               | Material                       | Graphite         | Ref. 1_, pg. 4-4   |
   +---------------+--------------------------------+------------------+--------------------+
   | Molybdenum    | Diameter (in.)                 | 1.431            | Ref. 1_, pg. 4-3   |
   | Disc          +--------------------------------+------------------+--------------------+
   |               | Thickness (in.)                | 0.031            | Ref. 1_, pg. 4-3   |
   |               +--------------------------------+------------------+--------------------+
   |               | Material                       | Graphite         | Ref. 1_, pg. 4-3   |
   +---------------+--------------------------------+------------------+--------------------+
   | Upper Gap     | Thickness (in.)                | 0.5              | Ref. 1_, pg. 4-3   |
   +---------------+--------------------------------+------------------+--------------------+
   | Fill Gas      | Material                       | Air              | Ref. 2_, pg. 50,51 |
   +---------------+--------------------------------+------------------+--------------------+
   | End Fixtures  | Material                       | Stainless-Steel  | Ref. 1_, Table 4.1 |
   +---------------+--------------------------------+------------------+--------------------+

.. _figure-fuel-element-axial_profile:

.. figure:: /_static/images/triga/fuel_element_axial_diagram.png
   :align: center
   :width: 60%

   Diagram of Fuel Element Axial Profile.

Graphite Element
================

Graphite dummy elements are rods which may be used to core positions not occupied by fuel elements.
They have the same general dimensions as the fuel elements, but are filled with graphite and clad
in aluminum.

General geometric specifications relevant to the TRIGA progression problems are summarized in
:numref:`table-graphite-element`, and the axial configuration of the fuel element is depicted in
:numref:`figure-graphite-element-axial_profile`.

.. table:: Graphite Rod Geometry Specifications
   :name: table-graphite-element

   +---------------+----------------+-----------------------------------------+----------------------------+
   | Component     | Property       | Value                                   | Reference                  |
   +===============+================+=========================================+============================+
   | Graphite Meat | Diameter       | Fuel Element Fuel Meat OD               | Ref. 1_, Section 4.2.3.b   |
   |               +----------------+-----------------------------------------+----------------------------+
   |               | Length         | Fuel Element Interior Length  (~22 in.) | Ref. 1_, Section 4.2.3.b   |
   |               +----------------+-----------------------------------------+----------------------------+
   |               | Material       | Graphite                                | Ref. 1_, Section 4.2.3.b   |
   +---------------+----------------+-----------------------------------------+----------------------------+
   | Cladding      | Thickness      | Fuel Element Cladding Thickness         | Ref. 1_, Section 4.2.3.b   |
   |               +----------------+-----------------------------------------+----------------------------+
   |               | Outer Diameter | Fuel Element Cladding OD                | Ref. 1_, Section 4.2.3.b   |
   |               +----------------+-----------------------------------------+----------------------------+
   |               | Material       | Aluminum                                | Ref. 1_, Section 4.2.3.b   |
   +---------------+----------------+-----------------------------------------+----------------------------+
   | End Fixtures  | Material       | Aluminum                                | Ref. 2_, pg. 50            |
   +---------------+----------------+-----------------------------------------+----------------------------+

.. _figure-graphite-element-axial_profile:

.. figure:: /_static/images/triga/graphite_element_axial_diagram.png
   :align: center
   :width: 60%

   Diagram of Graphite Element Axial Profile.


Material Compositions
=====================

This section specifies the base compositions of the materials used
in the TRIGA progression problems.  Unless specified otherwise, these compositions
should be used for the corresponding materials in all TRIGA progression problems.

References
==========

.. [1] "University of Texas at Austin Nuclear Engineering Teaching Laboratory
   TRIGA Research Reactor", August 2023,
   https://www.nrc.gov/docs/ML2327/ML23279A146.pdf

.. [2] D. R. Redhouse, et al., "Radiation Characterization Summary: NETL Beam Port
   1/5 Free-Field Environment at the 128-inch Core Centerline Adjacent Location,
   (NETL-FF-BP1/5-128-cca).", Nov. 2022. https://doi.org/10.2172/1898256

See Also
========

* :ref:`progression_problems_triga` - TRIGA progression problems overview
* :ref:`python_tools_triga` - Python tools for TRIGA analysis
* :ref:`progression_problems_triga_netl` - NETL-specific specifications
