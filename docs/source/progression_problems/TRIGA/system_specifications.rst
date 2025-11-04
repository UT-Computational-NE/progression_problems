.. _progression_problems_triga_system_specifications:

=====================
System Specifications
=====================

This section contains system specifications for those elements which are generally common to
all TRIGA reactors.  Those specifications which are specific to certain TRIGA designs are located
in their respective sub-sections.

Fuel Elements
=============

TRIGA fuel is uranium homogeneously distributed in zirconium-hydride, with Standard Fuel Elements (SFEs)
consisting of annular fuel-moderator material with a central hole in which a zirconium filler rod occupies.
The fuel is axially centered in a stainless-steel cladding tube with a graphite reflector on the top and bottom
ends, has a gas gap above the upper reflector, and molybdenum disc above the lower reflector to prevent damage
to the lower reflector.

End fixtures are welded to the top and bottom of the cladding tube to support the fuel on the lower grid plate,
to center the fuel in the upper grid plate, provide a path for cooling flow through the top grid plate, and to
provide a connection point for fuel handling tools.  For fuel elements with thermocouples embedded in the fuel
matrix, also known as Instrumented Fuel Elements (IFEs), the upper end fixture provides a passage for lead wires.
These end fittings have been manufactured in three distinct designs, known as "original", "integral", and
"streamlined", and are illustrated in :numref:`figure-fuel-elements`.

General geometric specifications for the TRIGA progression problems are provided in
:numref:`table-fuel-element`.

.. _figure-fuel-elements:

.. figure:: /_static/images/triga/fuel_element_variations.png
   :align: center
   :width: 60%

   Variations of TRIGA Fuel Elements [1]_.


.. table:: Mark III Fuel Element Geometry Specifications
   :name: table-fuel-element

   +-------------+-------------------------------+-----------+--------------------+
   | Component   | Property                      | Value     | Reference          |
   +=============+===============================+===========+====================+
   | Fuel Meat   | Inner Diameter (in)           | 0.25      | Ref. 1_, pg. 4-2   |
   |             +-------------------------------+-----------+--------------------+
   |             | Outer Diameter (in)           | 1.435     | Ref. 1_, Table 4.1 |
   |             +-------------------------------+-----------+--------------------+
   |             | Length (in)                   | 15.0      | Ref. 1_, Table 4.1 |
   |             +-------------------------------+-----------+--------------------+
   |             | Material                      | U-ZrH1.6  | Ref. 1_, pg. 4-2   |
   +=============+===============================+===========+====================+
   | Cladding    | Inner Diameter (in)           | 0.25      | Ref. 1_, pg. 4-2   |
   |             +-------------------------------+-----------+--------------------+
   |             | Outer Diameter (in)           | 1.435     | Ref. 1_, Table 4.1 |
   |             +-------------------------------+-----------+--------------------+
   |             | Length (in)                   | 15.0      | Ref. 1_, Table 4.1 |
   |             +-------------------------------+-----------+--------------------+
   |             | Material                      | U-ZrH1.6  | Ref. 1_, pg. 4-2   |
   +-------------+-------------------------------+-----------+--------------------+


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
