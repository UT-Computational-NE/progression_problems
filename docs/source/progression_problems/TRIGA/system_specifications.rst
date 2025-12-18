.. _progression_problems_triga_system_specifications:

=====================
System Specifications
=====================

This section contains system specifications for those elements which are generally common to
all TRIGA reactors.  Those specifications which are specific to certain TRIGA designs are located
in their respective sub-sections.

.. _progression_problems_triga_fuel_element:

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
:numref:`figure-fuel-elements`. For the sake of simplicity, these end fittings are typically approximated using a conical geometry.
As such, an conical equivalent estimate is provided for this specification assuming a cone with a base-radius equal to the cladding
outer-radius and a cone slope squared of ``r2 = 0.25``, with the remaining length of the end-fixture treated as a solid cylinder.
General geometric specifications relevant to the TRIGA progression problems are summarized in :numref:`table-fuel-element`, and the
axial configuration of the fuel element is depicted in :numref:`figure-fuel-element-axial_profile`.

.. _figure-fuel-elements:

.. figure:: /_static/images/triga/fuel_element_variations.png
   :align: center
   :width: 60%

   Variations of TRIGA Fuel Elements (Ref. 1_).


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
   |               | Material                       | Molybdenum       | Ref. 2_, pg. 51    |
   +---------------+--------------------------------+------------------+--------------------+
   | Upper Gap     | Thickness (in.)                | 0.5              | Ref. 1_, pg. 4-3   |
   +---------------+--------------------------------+------------------+--------------------+
   | Fill Gas      | Material                       | Air              | Ref. 2_, pg. 50,51 |
   +---------------+--------------------------------+------------------+--------------------+
   | End Fixtures  | Upper Fitting Equivalent Cone  | 7.3552           | Ref. 2_, pg 55     |
   |               | Approximation Length (cm)      |                  |                    |
   |               +--------------------------------+------------------+--------------------+
   |               | Lower Fitting Equivalent Cone  | 7.6209           | Ref. 2_, pg 55-56  |
   |               | Approximation Length (cm)      |                  |                    |
   |               +--------------------------------+------------------+--------------------+
   |               | Cone Slope Squared (r2)        | 0.25 (unitless)  | Ref. 2_, pg. 55    |
   |               +--------------------------------+------------------+--------------------+
   |               | Material                       | Stainless-Steel  | Ref. 1_, Table 4.1 |
   +---------------+--------------------------------+------------------+--------------------+

.. _figure-fuel-element-axial_profile:

.. figure:: /_static/images/triga/fuel_element_axial_diagram.png
   :align: center
   :width: 60%

   Diagram of Fuel Element Axial Profile.

.. _progression_problems_triga_graphite_element:

Graphite Element
================

Graphite dummy elements are rods which may be used to core positions not occupied by fuel elements.
They have the same general dimensions as the fuel elements, but are filled with graphite and clad
in aluminum.

General geometric specifications relevant to the TRIGA progression problems are summarized in
:numref:`table-graphite-element`, and the axial configuration of the graphite element is depicted in
:numref:`figure-graphite-element-axial_profile`.

.. table:: Graphite Rod Geometry Specifications
   :name: table-graphite-element

   +---------------+--------------------------------+-----------------------------------------+----------------------------+
   | Component     | Property                       | Value                                   | Reference                  |
   +===============+================================+=========================================+============================+
   | Graphite Meat | Diameter                       | Fuel Element Fuel Meat OD               | Ref. 1_, Section 4.2.3.b   |
   |               +--------------------------------+-----------------------------------------+----------------------------+
   |               | Length                         | Fuel Element Interior Length  (~22 in.) | Ref. 1_, Section 4.2.3.b   |
   |               +--------------------------------+-----------------------------------------+----------------------------+
   |               | Material                       | Graphite                                | Ref. 1_, Section 4.2.3.b   |
   +---------------+--------------------------------+-----------------------------------------+----------------------------+
   | Cladding      | Thickness                      | Fuel Element Cladding Thickness         | Ref. 1_, Section 4.2.3.b   |
   |               +--------------------------------+-----------------------------------------+----------------------------+
   |               | Outer Diameter                 | Fuel Element Cladding OD                | Ref. 1_, Section 4.2.3.b   |
   |               +--------------------------------+-----------------------------------------+----------------------------+
   |               | Material                       | Aluminum                                | Ref. 1_, Section 4.2.3.b   |
   +---------------+--------------------------------+-----------------------------------------+----------------------------+
   | End Fixtures  | Upper Fitting Equivalent Cone  | Fuel Element Upper End Fitting          | Ref. 1_ Section 4.2.3.b    |
   |               | Approximation Length           | Cone Approximation Length               |                            |
   |               +--------------------------------+-----------------------------------------+----------------------------+
   |               | Lower Fitting Equivalent Cone  | Fuel Element Lower End Fitting          | Ref. 1_ Section 4.2.3.b    |
   |               | Approximation Length           | Cone Approximation Length               |                            |
   |               +--------------------------------+-----------------------------------------+----------------------------+
   |               | Cone Slope Squared (r2)        | 0.25 (unitless)                         | Ref. 2_, pg. 55            |
   |               +--------------------------------+-----------------------------------------+----------------------------+
   |               | Material                       | Aluminum                                | Ref. 2_, pg. 50            |
   +---------------+--------------------------------+-----------------------------------------+----------------------------+

.. _figure-graphite-element-axial_profile:

.. figure:: /_static/images/triga/graphite_element_axial_diagram.png
   :align: center
   :width: 60%

   Diagram of Graphite Element Axial Profile.

.. _progression_problems_triga_material_compositions:

Material Compositions
=====================

This section specifies the base compositions of the materials used
in the TRIGA progression problems.  Unless specified otherwise, these compositions
should be used for the corresponding materials in all TRIGA progression problems.

.. table:: U-ZrH1.6 Specifications
   :name: table-UZrH-specs

   +-------------------+-----------------------+----------------------+
   | Property          | Value                 | Reference            |
   +===================+=======================+======================+
   | Density (g/cc)    | 5.85                  | Ref. 2_, pg. 51      |
   +-------------------+---------+-------------+----------------------+
   | Composition       | H-1     | 0.014355,   | Ref. 2_, pg. 59-60   |
   + (Iso ID, wt%)     +---------+-------------+                      +
   |                   | Mn-55   | 0.0014287   |                      |
   +                   +---------+-------------+                      +
   |                   | U-235   | 0.0152      |                      |
   +                   +---------+-------------+                      +
   |                   | U-238   | 0.061568    |                      |
   +                   +---------+-------------+                      +
   |                   | Zr-90   | 0.43706     |                      |
   +                   +---------+-------------+                      +
   |                   | Zr-91   | 0.0942      |                      |
   +                   +---------+-------------+                      +
   |                   | Zr-92   | 0.14253     |                      |
   +                   +---------+-------------+                      +
   |                   | Zr-94   | 0.14136     |                      |
   +                   +---------+-------------+                      +
   |                   | Zr-96   | 0.02228     |                      |
   +                   +---------+-------------+                      +
   |                   | Cr-Nat  | 0.013573    |                      |
   +                   +---------+-------------+                      +
   |                   | Fe-Nat  | 0.049647    |                      |
   +                   +---------+-------------+                      +
   |                   | Ni-Nat  | 0.0067863   |                      |
   +-------------------+---------+-------------+----------------------+


.. table:: Zirconium Specifications
   :name: table-zirconium-specs

   +--------------------+-----------------------+----------------------+
   | Property           | Value                 | Reference            |
   +====================+=======================+======================+
   | Density (atom/b-cm)| 0.0408                | Ref. 2_, pg. 51      |
   +--------------------+---------+-------------+----------------------+
   | Composition        | Zr-90   | 0.5145      | Ref. 2_, pg. 60      |
   + (Iso ID, at%)      +---------+-------------+                      +
   |                    | Zr-91   | 0.1122      |                      |
   +                    +---------+-------------+                      +
   |                    | Zr-92   | 0.1715      |                      |
   +                    +---------+-------------+                      +
   |                    | Zr-94   | 0.1738      |                      |
   +                    +---------+-------------+                      +
   |                    | Zr-96   | 0.0280      |                      |
   +--------------------+---------+-------------+----------------------+


.. table:: Stainless-Steel Specifications
   :name: table-stainless-steel-specs

   +--------------------+-----------------------+----------------------+
   | Property           | Value                 | Reference            |
   +====================+=======================+======================+
   | Density (atom/b-cm)| 0.0858                | Ref. 2_, pg. 50      |
   +--------------------+---------+-------------+----------------------+
   | Composition        | C-Nat   | 0.00031519  | Ref. 2_, pg. 60      |
   + (Iso ID, at%)      +---------+-------------+                      +
   |                    | Cr-50   | 0.000782    |                      |
   +                    +---------+-------------+                      +
   |                    | Cr-52   | 0.014501    |                      |
   +                    +---------+-------------+                      +
   |                    | Cr-53   | 0.001613    |                      |
   +                    +---------+-------------+                      +
   |                    | Cr-54   | 0.000394    |                      |
   +                    +---------+-------------+                      +
   |                    | Fe-54   | 0.003554    |                      |
   +                    +---------+-------------+                      +
   |                    | Fe-56   | 0.05511     |                      |
   +                    +---------+-------------+                      +
   |                    | Fe-57   | 0.001257    |                      |
   +                    +---------+-------------+                      +
   |                    | Fe-58   | 0.000166    |                      |
   +                    +---------+-------------+                      +
   |                    | Ni-58   | 0.005558    |                      |
   +                    +---------+-------------+                      +
   |                    | Ni-60   | 0.00207     |                      |
   +                    +---------+-------------+                      +
   |                    | Ni-61   | 8.85e-05    |                      |
   +                    +---------+-------------+                      +
   |                    | Ni-62   | 0.000278    |                      |
   +                    +---------+-------------+                      +
   |                    | Ni-64   | 6.85e-05    |                      |
   +--------------------+---------+-------------+----------------------+


.. table:: Graphite Specifications
   :name: table-graphite-specs

   +-------------------+-----------------------+----------------------+
   | Property          | Value                 | Reference            |
   +===================+=======================+======================+
   | Density (g/cc)    | 1.6                   | Ref. 2_, pg. 48      |
   +-------------------+---------+-------------+----------------------+
   | Composition       | C-Nat   | 1.0         | Ref. 2_, pg. 60      |
   | (Iso ID, at%)     |         |             |                      |
   +-------------------+---------+-------------+----------------------+


.. table:: Molybdenum Specifications
   :name: table-molybdenum-specs

   +-------------------+-----------------------+----------------------+
   | Property          | Value                 | Reference            |
   +===================+=======================+======================+
   | Density (g/cc)    | 10.3                  | Ref. 2_, pg. 51      |
   +-------------------+---------+-------------+----------------------+
   | Composition       | Mo-92   | 0.1477      | Ref. 2_, pg. 60      |
   + (Iso ID, at%)     +---------+-------------+                      +
   |                   | Mo-94   | 0.0923      |                      |
   +                   +---------+-------------+                      +
   |                   | Mo-95   | 0.159       |                      |
   +                   +---------+-------------+                      +
   |                   | Mo-96   | 0.1668      |                      |
   +                   +---------+-------------+                      +
   |                   | Mo-97   | 0.0956      |                      |
   +                   +---------+-------------+                      +
   |                   | Mo-98   | 0.2419      |                      |
   +                   +---------+-------------+                      +
   |                   | Mo-100  | 0.0967      |                      |
   +-------------------+---------+-------------+----------------------+


.. table:: Air Specifications
   :name: table-air-specs

   +-------------------+-----------------------+----------------------+
   | Property          | Value                 | Reference            |
   +===================+=======================+======================+
   | Density (g/cc)    | 0.001225              | Ref. 2_, pg. 48      |
   +-------------------+---------+-------------+----------------------+
   | Composition       | N-14    | 0.79        | Ref. 2_, pg. 60      |
   + (Iso ID, at%)     +---------+-------------+                      +
   |                   | O-16    | 0.21        |                      |
   +-------------------+---------+-------------+----------------------+


.. table:: Aluminum Specifications
   :name: table-aluminum-specs

   +-------------------+-----------------------+----------------------+
   | Property          | Value                 | Reference            |
   +===================+=======================+======================+
   | Density (g/cc)    | 2.7                   | Ref. 2_, pg. 48      |
   +-------------------+---------+-------------+----------------------+
   | Composition       | B-10    | 2.3945e-07  | Ref. 2_, pg. 60      |
   + (Iso ID, at%)     +---------+-------------+                      +
   |                   | Mg-24   | 0.00053511  |                      |
   +                   +---------+-------------+                      +
   |                   | Mg-25   | 6.503e-05   |                      |
   +                   +---------+-------------+                      +
   |                   | Mg-26   | 6.8851e-05  |                      |
   +                   +---------+-------------+                      +
   |                   | Al-27   | 0.059015    |                      |
   +                   +---------+-------------+                      +
   |                   | Si-28   | 0.00032153  |                      |
   +                   +---------+-------------+                      +
   |                   | Si-29   | 1.5771e-05  |                      |
   +                   +---------+-------------+                      +
   |                   | Si-30   | 1.0062e-05  |                      |
   +                   +---------+-------------+                      +
   |                   | Cr-50   | 2.6872e-06  |                      |
   +                   +---------+-------------+                      +
   |                   | Cr-52   | 4.983e-05   |                      |
   +                   +---------+-------------+                      +
   |                   | Cr-53   | 5.5435e-06  |                      |
   +                   +---------+-------------+                      +
   |                   | Cr-54   | 1.3544e-06  |                      |
   +                   +---------+-------------+                      +
   |                   | Cu-63   | 5.0017e-05  |                      |
   +                   +---------+-------------+                      +
   |                   | Cu-65   | 2.1628e-05  |                      |
   +-------------------+---------+-------------+----------------------+


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

* :ref:`TRIGA-Generic Progression Problems <progression_problems_triga>`
* :ref:`Python Tools for TRIGA <python_tools_triga>`
* :ref:`NETL TRIGA System Specifications <progression_problems_triga_netl>`
