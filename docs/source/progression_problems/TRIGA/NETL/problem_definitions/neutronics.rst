.. _progression_problems_triga_netl_problem_definitions_neutronics:


==========
Neutronics
==========

This section defines a series of neutronics problems for the TRIGA reactor at
NETL. Each problem gradually increases in complexity, allowing for a progressive
assessment of neutronics simulation capabilities of various codes and methods.
Unless stated otherwise, all problems use the system specifications outlined in the
NETL TRIGA
:ref:`System Specifications <progression_problems_triga_netl_system_specifications>`.

.. admonition:: Recommended publication for citing
   :class: tip

    TBD: Add recommended publication for citing system elements here.

.. only:: html


Problem 1: 2D Pin Cell
======================


The first problem is a 2D representation of the smallest repeating fuel unit cell of the NETL
TRIGA core with reflecting boundary conditions. Given that the NETL TRIGA core is arranged in
a hexagonal lattice, the smallest repeating unit cell is two quarter pins hexagonally pitched,
forming a rectangular cell with the quarter pins centered on opposite corners from each other
as illustrated in :numref:`figure-triga-netl-problem_1`.

This unit cell problem allows for the assessment of basic geometric modeling, model mesh
refinement, and isolating effects associated with cross-section libraries and cross-section
calculations through reaction rate edits. This problem tests the fundamental capabilities of
the codes while also highlighting any material or cross-section processing deficiencies.

:numref:`table-problem-1-definitions` provides the specifications for the various cases
to be simulated for this problem.  In these cases, the fuel meat and Zr Filler rod are treated
with the same temperature, and clad and coolant temperatures are treated with the same temperature.
Fuel temperatures range from room temperature up to 1200K with several temperatures aligning with
cross-section library temperatures so as to allow for direct comparison to Monte Carlo without the
need for interpolation.  823.15 K represents the peak allowed fuel temperature according to Table
4.4 of Reference [1].  Coolant temperatures and densities are taken from Table 4.20 of Reference [1]
so as to be representative of the range of anticipated operating conditions.

Recommended outputs for this problem include:
  - k-effective
  - 1-2 Group Reaction Rates (Fission, Absorption, etc.)
  - Flux Spectrum

.. _figure-triga-netl-problem_1:

.. figure:: /_static/images/triga/netl/problem_1.png
   :align: center
   :width: 60%

   Problem 1 Geometry.


.. table:: Problem 1 Definitions
   :name: table-problem-1-definitions

   +---------+----------------------------------+--------------------------------+------------------------+
   | Problem | Fuel / Zr Filler Temperature (K) | Clad / Coolant Temperature (K) | Coolant Density (g/cc) |
   +=========+==================================+================================+========================+
   | 1A      |   293.15                         | 293.15                         |  0.9970                |
   +---------+----------------------------------+--------------------------------+------------------------+
   | 1B      |   600.0                          | 322.15                         |  0.9885                |
   +---------+----------------------------------+--------------------------------+------------------------+
   | 1C      |   823.15                         | 322.15                         |  0.9885                |
   +---------+----------------------------------+--------------------------------+------------------------+
   | 1D      |   900.0                          |   ↓                            |   ↓                    |
   +---------+----------------------------------+--------------------------------+------------------------+
   | 1E      |  1200.0                          |   ↓                            |   ↓                    |
   +---------+----------------------------------+--------------------------------+------------------------+
   | 1F      |   600.0                          | 293.15                         |  0.9970                |
   +---------+----------------------------------+--------------------------------+------------------------+



Problem 2: 2D Multi-Pin Cell
============================

The second problem is a 2D representation of a multi-pin cell of the NETL TRIGA core
with reflecting boundary conditions. This multi-pin cell consists of a central control
rod cell surrounded by 2 rings of fuel pins in a hexagonal lattice as illustrated in
:numref:`figure-triga-netl-problem_2`.  Since the boundary surface is a rectangular boundary,
the outer ring of fuel pins is only partially represented.  With reflecting boundary conditions,
this model roughly represents the interior region of the core around the control rods.

This problem introduces additional geometric complexity compared to the single pin cell problem
through radial heterogeneity and introduces for the inclusion of non-fuel materials such
as control elements (e.g., poisons). This problem tests the geometric and cross-section treatment
capabilities with slightly increased model complexity while enabling the evaluation of cell-wise outputs,
such as pin powers.  This also provides an opportunity for assessing solver scalability when going
from pin-cell models to multi-pin models.

:numref:`table-problem-2-definitions` provides the specifications for the various cases
to be simulated for this problem.  For the TCR Air Follower case, temperatures and densities again
range over representative values much like Problem 1.  The other cases introduce the presence of
absorber and fuel follower materials in the control rod, testing the proper treatment of these materials.

Recommended outputs for this problem include:
  - k-effective
  - Flux Spectrum
  - Pin-wise Power Distributions

.. _figure-triga-netl-problem_2:

.. figure:: /_static/images/triga/netl/problem_2.png
   :align: center
   :width: 60%

   Problem 2 Geometry.


.. table:: Problem 2 Definitions
   :name: table-problem-2-definitions


   +---------+-----------------------+----------------------------------+--------------------------------+------------------------+
   | Problem | Description           | Fuel / Zr Filler Temperature (K) | Clad / Coolant Temperature (K) | Coolant Density (g/cc) |
   +=========+=======================+==================================+================================+========================+
   | 2A      |   Water Hole          |  293.15                          |  293.15                        |  0.9970                |
   +---------+-----------------------+----------------------------------+--------------------------------+------------------------+
   | 2B      |   Water Hole          |  600.0                           |  322.15                        |  0.9885                |
   +---------+-----------------------+----------------------------------+--------------------------------+------------------------+
   | 2C      |   Water Hole          |  900.0                           |    ↓                           |    ↓                   |
   +---------+-----------------------+----------------------------------+--------------------------------+------------------------+
   | 2D      |   Water Hole          | 1200.0                           |    ↓                           |    ↓                   |
   +---------+-----------------------+----------------------------------+--------------------------------+------------------------+
   | 2E      |   Water Hole          |  600.0                           |  293.15                        |  0.9970                |
   +---------+-----------------------+----------------------------------+--------------------------------+------------------------+
   | 2F      |   Central Thimble     |   ↓                              |    ↓                           |    ↓                   |
   +---------+-----------------------+----------------------------------+--------------------------------+------------------------+
   | 2G      |   Graphite Element    |   ↓                              |    ↓                           |    ↓                   |
   +---------+-----------------------+----------------------------------+--------------------------------+------------------------+
   | 2H      |   Source Holder       |   ↓                              |    ↓                           |    ↓                   |
   +---------+-----------------------+----------------------------------+--------------------------------+------------------------+
   | 2I      |   TCR Air Follower    |   ↓                              |    ↓                           |    ↓                   |
   +---------+-----------------------+----------------------------------+--------------------------------+------------------------+
   | 2J      |   TCR Absorber        |   ↓                              |    ↓                           |    ↓                   |
   +---------+-----------------------+----------------------------------+--------------------------------+------------------------+
   | 2K      |   FCCR Fuel Follower  |   ↓                              |    ↓                           |    ↓                   |
   +---------+-----------------------+----------------------------------+--------------------------------+------------------------+
   | 2L      |   FCCR Absorber       |   ↓                              |    ↓                           |    ↓                   |
   +---------+-----------------------+----------------------------------+--------------------------------+------------------------+


Problem 3: 2D Full Core
=======================

This problem introduces a full-core 2D representation of the NETL TRIGA reactor which increases
radial geometric complexity and introduces non-reflective boundary conditions.  This problem has
two primary variations, one with essentially no-excore features and one with excore features included.
The geometry for this problem is illustrated in :numref:`figure-triga-netl-problem_3`. The non-excore
model uses a circular boundary terminating at the shroud inner radius, while the excore model includes the
excore features such as shroud, beam ports, and reflector.  Axially, both models are assumed to
have reflective boundary conditions, with the excore model representing the beam ports as their full
widths (i.e. beam port radius at the Centerline plane of the beam ports).

For this problem, the core will be filled with fresh fuel rods in all core locations with the exceptions of
the reserved locations specified in :ref:`reserved-core-locations` table which are filled with those elements
specified in the table, as well as G-32 which will be filled with a source holder, E-11, F-13, and F-14 which
will be empty "water holes", and D-03 which will have a graphite element.  The geometry for this problem is
illustrated in :numref:`figure-triga-netl-problem_3`.

Flux measurements and detector responses are to be simulated in the excore model. Experimental flux locations
for beam ports 2 thru for are to be along the centerline of the beam ports 1 inch from the tip of the beam port.
For beam port 1 / 5, the experimental flux location is to be at the point where the centerline of the beam port
intersects the centerline of the core.  For the central thimble, the experimental flux location is to be at the
center of the thimble.  To represent an excore detector, reaction rates for B-10 absorption and U-235 fission
shall be tallied within a circular region of 1-inch radius, centered 1 inch outside the reflector along the core
centerline in the southern direction :numref:`table-problem-3-definitions` provides the remaining specifications
for the cases to be simulated for this problem.

Recommended outputs for this problem include:
  - k-effective
  - Flux Spectrum
  - Pin-wise Power Distributions
  - Ex-core Detector Responses
  - Flux at experiment locations

.. _figure-triga-netl-problem_3:

.. figure:: /_static/images/triga/netl/problem_3.png
   :align: center
   :width: 60%

   Problem 3 Geometry.

.. table:: Problem 3 Definitions
   :name: table-problem-3-definitions

   +---------+----------+----------+----------+------------------+-----------------+----------------+
   | Problem | Excore   | TCR      | FFCR     | Fuel / Zr Filler | Clad / Coolant  | Coolant        |
   |         | Features?| Section  | Section  | Temperature (K)  | Temperature (K) | Density (g/cc) |
   +=========+==========+==========+==========+==================+=================+================+
   | 3A      |  No      | Air      | Fuel     |  293.15          |  293.15         |  0.9970        |
   |         |          | Follower | Follower |                  |                 |                |
   +---------+----------+----------+----------+------------------+-----------------+----------------+
   | 3B      |  No      | Air      | Fuel     |  600.0           |  322.15         |  0.9885        |
   |         |          | Follower | Follower |                  |                 |                |
   +---------+----------+----------+----------+------------------+-----------------+----------------+
   | 3C      |  No      | Air      | Fuel     |  600.0           |  293.15         |  0.9970        |
   |         |          | Follower | Follower |                  |                 |                |
   +---------+----------+----------+----------+------------------+-----------------+----------------+
   | 3D      |  Yes     | Air      | Fuel     |    ↓             |    ↓            |    ↓           |
   |         |          | Follower | Follower |                  |                 |                |
   +---------+----------+----------+----------+------------------+-----------------+----------------+
   | 3E      |  Yes     | Absorber | Absorber |    ↓             |    ↓            |    ↓           |
   +---------+----------+----------+----------+------------------+-----------------+----------------+




Problem 4: 3D Multi-Pin Cell
============================

This problem is essentially an extension of 2D multi-pin cell problem into 3D space.  This model introduces
axial heterogeneity through the full 3D representation of the core elements as well the us of axial vacuum
boundary conditions.  This problems also tests the movement of control rods within the multi-pin cell
geometry.  The geometry for this problem is illustrated in :numref:`figure-triga-netl-problem_4`.

:numref:`table-problem-4-definitions` provides the specifications for the various cases
to be simulated for this problem.  Axially, these models should include the upper and lower grid plates as
well as upper and lower pool water regions extending as far as 80 cm above and below the fuel axial centerline.

Recommended outputs for this problem include:
  - k-effective
  - Flux Spectrum
  - Pin-wise Power Distributions

.. _figure-triga-netl-problem_4:

.. figure:: /_static/images/triga/netl/problem_4.png
   :align: center
   :width: 60%

   Problem 4 Geometry.


.. table:: Problem 4 Definitions
   :name: table-problem-4-definitions


   +---------+----------------------+------------------+-----------------+----------------+
   | Problem | Description          | Fuel / Zr Filler | Clad / Coolant  | Coolant        |
   |         |                      | Temperature (K)  | Temperature (K) | Density (g/cc) |
   +=========+======================+==================+=================+================+
   | 4A      |  Water Hole          |  293.15          |  293.15         |  0.9970        |
   +---------+----------------------+------------------+-----------------+----------------+
   | 4B      |  Water Hole          |  600.0           |  322.15         |  0.9885        |
   +---------+----------------------+------------------+-----------------+----------------+
   | 4C      |  Water Hole          |  600.0           |  293.15         |  0.9970        |
   +---------+----------------------+------------------+-----------------+----------------+
   | 4D      |  Central Thimble     |    ↓             |    ↓            |    ↓           |
   +---------+----------------------+------------------+-----------------+----------------+
   | 4E      |  Graphite Element    |    ↓             |    ↓            |    ↓           |
   +---------+----------------------+------------------+-----------------+----------------+
   | 4F      |  Source Holder       |    ↓             |    ↓            |    ↓           |
   +---------+----------------------+------------------+-----------------+----------------+
   | 4G      |  TCR                 |    ↓             |    ↓            |    ↓           |
   |         |  (0%-100% Withdrawn) |                  |                 |                |
   +---------+----------------------+------------------+-----------------+----------------+
   | 4H      |  FCCR                |    ↓             |    ↓            |    ↓           |
   |         |  (0%-100% Withdrawn) |                  |                 |                |
   +---------+----------------------+------------------+-----------------+----------------+


Problem 5: 3D Full Core
=======================

This progression problem is a 3D extension of Problem 3 with all ex-core features, introducing
all axial heterogeneities of the full core (cylindrical beam ports, core element axial structures,
rotary specimen rack, etc.) as well as both axial and radial vacuum boundary conditions.  The
geometry for this problem is illustrated in :numref:`figure-triga-netl-problem_5`.

:numref:`table-problem-5-definitions` provides the specifications for the various cases
to be simulated for this problem.  Axially, these models should include upper and lower axial
pool water regions extending as far as 80 cm above and below the fuel axial centerline.

Recommended outputs for this problem include:
  - k-effective
  - Flux Spectrum
  - Pin-wise Power Distributions
  - In-core / Ex-core Detector Responses
  - Flux at experiment locations


.. _figure-triga-netl-problem_5:

.. figure:: /_static/images/triga/netl/problem_5.png
   :align: center
   :width: 60%

   Problem 5 Geometry.


.. table:: Problem 5 Definitions
   :name: table-problem-5-definitions

   +---------+----------------------+------------------+-----------------+----------------+
   | Problem | Description          | Fuel / Zr Filler | Clad / Coolant  | Coolant        |
   |         |                      | Temperature (K)  | Temperature (K) | Density (g/cc) |
   +=========+======================+==================+=================+================+
   | 5A      |  All Rods Out        |  293.15          |  293.15         |  0.9970        |
   +---------+----------------------+------------------+-----------------+----------------+
   | 5B      |  All Rods Out        |  600.0           |  322.15         |  0.9885        |
   +---------+----------------------+------------------+-----------------+----------------+
   | 5C      |  All Rods Out        |  600.0           |  293.15         |  0.9970        |
   +---------+----------------------+------------------+-----------------+----------------+
   | 5D      |  Transient Rod       |    ↓             |    ↓            |    ↓           |
   |         |  (0%-100% Withdrawn) |                  |                 |                |
   +---------+----------------------+------------------+-----------------+----------------+
   | 5E      |  Regulating Rod      |    ↓             |    ↓            |    ↓           |
   |         |  (0%-100% Withdrawn) |                  |                 |                |
   +---------+----------------------+------------------+-----------------+----------------+
   | 5F      |  Shim Rod 1          |    ↓             |    ↓            |    ↓           |
   |         |  (0%-100% Withdrawn) |                  |                 |                |
   +---------+----------------------+------------------+-----------------+----------------+
   | 5G      |  Shim Rod 2          |    ↓             |    ↓            |    ↓           |
   |         |  (0%-100% Withdrawn) |                  |                 |                |
   +---------+----------------------+------------------+-----------------+----------------+

References
==========

.. [1] "University of Texas at Austin Nuclear Engineering Teaching Laboratory
   TRIGA Research Reactor", August 2023,
   https://www.nrc.gov/docs/ML2327/ML23279A146.pdf

See Also
========

* :ref:`TRIGA General Specifications <progression_problems_triga_system_specifications>`
* :ref:`NETL TRIGA System Specifications <progression_problems_triga_netl_system_specifications>`
* :ref:`Python Tools for NETL TRIGA <python_tools_triga_netl>`