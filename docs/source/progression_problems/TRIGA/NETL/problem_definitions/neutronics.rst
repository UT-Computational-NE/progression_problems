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

The first progression-problem set consists of a two-dimensional radial model of the smallest
repeating fuel unit cell in the NETL TRIGA core, with reflective boundary conditions applied
in both the radial and axial directions. Because the core is arranged on a hexagonal lattice,
the smallest repeating unit is formed by two quarter-pin fuel regions on a hexagonal pitch,
which together define a rectangular cell with the quarter pins located at opposite corners,
as shown in :numref:`figure-triga-netl-problem_1`. This problem is intended to assess basic
geometric & depletion capabilities, mesh refinement requirements, and the influence of cross-section
libraries and cross-section processing via reaction-rate edits. As such, it provides a simple but
useful test of fundamental code capabilities.

:numref:`table-problem-1-definitions` provides the specifications for the various cases
to be simulated for this problem.  In these cases, the fuel meat and Zr Filler rod are treated
with the same temperature, and clad and coolant temperatures are treated with the same temperature.
Fuel temperatures range from room temperature up to 900K with several temperatures aligning with
cross-section library temperatures so as to allow for direct comparison to Monte Carlo without the
need for interpolation.  823.15 K represents the peak allowed fuel temperature according to Table
4.4 of Reference 1_.  Coolant temperatures and densities are taken from Table 4.20 of Reference 1_
so as to be representative of the range of anticipated operating conditions.

For depletion assessments, target burnups are defined ineffective full-power days (EFPD), based on a
full-core power of 1 MW distributed across 110 fuel elements. Since this is a 2D single-element model,
the applied model power should preserve the appropriate average power per element per unit height,
(ex: :math:`1\,\mathrm{MW}\left(\frac{\text{model height}}{\text{fuel-meat height}}\right)\left(\frac{0.5\ \text{element in model}}{110\ \text{elements in core}}\right)`).
The 2.0 EFPD and 20.0 EFPD targets were selected to represent the characteristic buildup periods of Xe-135
and Sm-149, respectively. The 265.0 EFPD and 530.0 EFPD targets correspond approximately to
middle-of-life (MOL) and end-of-life (EOL) element burnups, based on an estimated maximum fuel-element burnup
of 6 g of U-235 (Ref. 1_, p. 3-2) and an estimated depletion rate of 1.25 g of U-235 per MWd (Ref. 2_, p. 4).


.. _figure-triga-netl-problem_1:

.. figure:: /_static/images/triga/netl/problem_1.png
   :align: center
   :width: 60%

   Problem 1 Geometry.

.. table:: Problem 1 Definitions
   :name: table-problem-1-definitions

   +---------+----------------------------+--------------------+----------------------+---------------+
   | Problem | Fuel / Zr Filler Temp. (K) | Non-Fuel Temp. (K) | Coolant Dens. (g/cc) | Burnup (EFPD) |
   +=========+============================+====================+======================+===============+
   | 1A      |   293.15                   | 293.15             |  0.9970              | 0.0           |
   +---------+----------------------------+--------------------+----------------------+---------------+
   | 1B      |   600.0                    | 322.15             |  0.9885              | 0.0           |
   +---------+----------------------------+--------------------+----------------------+---------------+
   | 1C      |   823.15                   | 322.15             |  0.9885              | 0.0           |
   +---------+----------------------------+--------------------+----------------------+---------------+
   | 1D      |   900.0                    | 322.15             |  0.9885              | 0.0           |
   +---------+----------------------------+--------------------+----------------------+---------------+
   | 1E      |   600.0                    | 293.15             |  0.9970              | 0.0           |
   +---------+----------------------------+--------------------+----------------------+---------------+
   | 1F      |   600.0                    | 293.15             |  0.9970              | 2.0           |
   +---------+----------------------------+--------------------+----------------------+---------------+
   | 1G      |   600.0                    | 293.15             |  0.9970              | 20.0          |
   +---------+----------------------------+--------------------+----------------------+---------------+
   | 1H      |   600.0                    | 293.15             |  0.9970              | 265.0         |
   +---------+----------------------------+--------------------+----------------------+---------------+
   | 1I      |   600.0                    | 293.15             |  0.9970              | 530.0         |
   +---------+----------------------------+--------------------+----------------------+---------------+


.. table:: Problem 1 Recommended Outputs

   +--------------------+----------------------------+
   | Output             | Subcategories              |
   +====================+============================+
   | k-eff              |   --                       |
   +--------------------+----------------------------+
   | Reaction Rates     |   One-Group / Multi-Group  |
   |                    +----------------------------+
   |                    |   Fission / Absorption     |
   |                    +----------------------------+
   |                    |   Macro / Micro            |
   |                    +----------------------------+
   |                    |   Global / Material-Wise   |
   +--------------------+----------------------------+
   | Flux Spectrum      |   Global / Material-Wise   |
   +--------------------+----------------------------+
   | Isotopic Inventory |   Fuel                     |
   +--------------------+----------------------------+


Problem 2: 2D Multi-Pin Cell
============================

The second progression-problem set consists of two-dimensional models of a multi-pin region of the
NETL TRIGA core with reflective boundary conditions. In these models, the central lattice position
is occupied either by a non-fuel element or by a vacant water hole and is surrounded by two rings of
fuel pins arranged on a hexagonal lattice, as shown in :numref:`figure-triga-netl-problem_2`. With reflective
boundary conditions, the model provides an approximate representation of an interior core region
surrounding a non-fuel or vacant lattice position. Relative to the single-pin cell problem set, this
progression-problem set introduces additional geometric complexity through increased radial
heterogeneity and the inclusion of additional non-fuel materials. It therefore provides a more
demanding test of geometric modeling, multi-pin depletion for fuel and control rod absorber, and cross-section
treatment while also enabling evaluation of pin-wise quantities such as pin powers. In addition,
it offers an opportunity to assess solver computational scalability in progressing from pin-cell
models to multi-pin configurations. :numref:`table-problem-2-definitions` summarizes the cases
considered in this progression-problem set.

For depletion cases, the target burnup is again specified in EFPD, assuming a full-core power of 1 MW
distributed over 110 fuel elements. Since this is a 2D model representing only a portion of the core,
the applied model power must be scaled to maintain the correct average power per fuel element per unit height.

.. _figure-triga-netl-problem_2:

.. figure:: /_static/images/triga/netl/problem_2.png
   :align: center
   :width: 60%

   Problem 2 Geometry.

.. table:: Problem 2 Definitions
   :name: table-problem-2-definitions


   +---------+-----------------------+----------------------------+--------------------+----------------------+---------------+
   | Problem | Central Element       | Fuel / Zr Filler Temp. (K) | Non-Fuel Temp. (K) | Coolant Dens. (g/cc) | Burnup (EFPD) |
   +=========+=======================+============================+====================+======================+===============+
   | 2A      |   Water Hole          |  293.15                    |  293.15            |  0.9970              | 0.0           |
   +---------+-----------------------+----------------------------+--------------------+----------------------+---------------+
   | 2B      |   Water Hole          |  600.0                     |  322.15            |  0.9885              | 0.0           |
   +---------+-----------------------+----------------------------+--------------------+----------------------+---------------+
   | 2C      |   Water Hole          |  600.0                     |  293.15            |  0.9970              | 530.0         |
   +---------+-----------------------+----------------------------+--------------------+----------------------+---------------+
   | 2D      |   Central Thimble     |  293.15                    |  293.15            |  0.9970              | 0.0           |
   +---------+-----------------------+----------------------------+--------------------+----------------------+---------------+
   | 2E      |   Central Thimble     |  600.0                     |  322.15            |  0.9885              | 0.0           |
   +---------+-----------------------+----------------------------+--------------------+----------------------+---------------+
   | 2F      |   Graphite Element    |  293.15                    |  293.15            |  0.9970              | 0.0           |
   +---------+-----------------------+----------------------------+--------------------+----------------------+---------------+
   | 2G      |   Graphite Element    |  600.0                     |  322.15            |  0.9885              | 0.0           |
   +---------+-----------------------+----------------------------+--------------------+----------------------+---------------+
   | 2H      |   TCR Air Follower    |  293.15                    |  293.15            |  0.9970              | 0.0           |
   +---------+-----------------------+----------------------------+--------------------+----------------------+---------------+
   | 2I      |   TCR Air Follower    |  600.0                     |  322.15            |  0.9885              | 0.0           |
   +---------+-----------------------+----------------------------+--------------------+----------------------+---------------+
   | 2J      |   TCR Absorber        |  293.15                    |  293.15            |  0.9970              | 0.0           |
   +---------+-----------------------+----------------------------+--------------------+----------------------+---------------+
   | 2K      |   TCR Absorber        |  600.0                     |  322.15            |  0.9885              | 0.0           |
   +---------+-----------------------+----------------------------+--------------------+----------------------+---------------+
   | 2L      |   TCR Absorber        |  600.0                     |  293.15            |  0.9970              | 530.0         |
   +---------+-----------------------+----------------------------+--------------------+----------------------+---------------+


.. table:: Problem 2 Recommended Outputs

   +--------------------+----------------------------+
   | Output             | Subcategories              |
   +====================+============================+
   | k-eff              |   --                       |
   +--------------------+----------------------------+
   | Reaction Rates     |   One-Group / Multi-Group  |
   |                    +----------------------------+
   |                    |   Fission / Absorption     |
   |                    +----------------------------+
   |                    |   Macro / Micro            |
   |                    +----------------------------+
   |                    |   Global / Material-Wise   |
   +--------------------+----------------------------+
   | Flux Spectrum      |   Global / Material-Wise   |
   +--------------------+----------------------------+
   | Isotopic Inventory |   Fuel / TCR Absorber      |
   +--------------------+----------------------------+
   | Pin Powers         |   Radial                   |
   +--------------------+----------------------------+


Problem 3: 2D Full Core
=======================

The third progression-problem set introduces a full-core two-dimensional model of the NETL TRIGA reactor,
thereby increasing radial geometric complexity and removing the reflective radial boundary conditions used
in the earlier problems. This set includes three primary model variations: a non-excore model, an excore model
with the rotary specimen rack (RSR), and an excore model with beam ports. The non-excore model is bounded by a
circular outer surface with radius equal to seven times the core lattice pitch. The excore models, by contrast,
include the core shroud, reflector, reactor pool, and either the RSR cavity or the beam ports. In all cases,
reflective boundary conditions are applied axially. For the beam-port variant, the beam ports are represented
at their full widths, corresponding to the beam-port radius at the beam-port centerline plane. For this
progression-problem set, all core locations are loaded with fresh fuel elements except for the reserved positions
identified in :numref:`reserved-core-locations`, which are occupied by the specified components. In
addition, location G-32 is filled with a source holder, locations E-11, F-13, F-14, and G-34 are modeled as vacant
water holes, and location D-03 contains a graphite element. :numref:`figure-reactor-radial-picture` illustrates the
radial geometry of the two excore cases, while :numref:`table-problem-3-definitions` summarizes the remaining case specifications.


.. table:: Problem 3 Definitions
   :name: table-problem-3-definitions

   +---------+----------+----------+----------+------------------+-----------------+----------------+
   | Problem | Excore   | TCR      | FFCR     | Fuel / Zr Filler | Clad / Coolant  | Coolant        |
   |         | Features | Section  | Section  | Temp. (K)        | Temp. (K)       | Dens. (g/cc)   |
   +=========+==========+==========+==========+==================+=================+================+
   | 3A      |  None    | Air      | Fuel     |  600.0           |  293.15         |  0.9970        |
   |         |          | Follower | Follower |                  |                 |                |
   +---------+----------+----------+----------+------------------+-----------------+----------------+
   | 3B      |  RSR     | Air      | Fuel     |  600.0           |  293.15         |  0.9970        |
   |         |          | Follower | Follower |                  |                 |                |
   +---------+----------+----------+----------+------------------+-----------------+----------------+
   | 3C      |  RSR     | Absorber | Absorber |  600.0           |  293.15         |  0.9970        |
   +---------+----------+----------+----------+------------------+-----------------+----------------+
   | 3D      |  Beam    | Air      | Fuel     |  600.0           |  293.15         |  0.9970        |
   |         |  Ports   | Follower | Follower |                  |                 |                |
   +---------+----------+----------+----------+------------------+-----------------+----------------+
   | 3E      |  Beam    | Absorber | Absorber |  600.0           |  293.15         |  0.9970        |
   |         |  Ports   |          |          |                  |                 |                |
   +---------+----------+----------+----------+------------------+-----------------+----------------+

.. table:: Problem 3 Recommended Outputs

   +--------------------+----------------------------+
   | Output             | Subcategories              |
   +====================+============================+
   | k-eff              |   --                       |
   +--------------------+----------------------------+
   | Flux Spectrum      |   Global                   |
   +--------------------+----------------------------+
   | Pin Powers         |   Radial                   |
   +--------------------+----------------------------+


Problem 4: 3D Multi-Pin Cell
============================

The fourth progression-problem set extends the two-dimensional multi-pin cell problems into three dimensions.
In doing so, it introduces axial heterogeneity through full three-dimensional representation of the core elements
and removes the axially reflective boundary conditions used in the earlier sets. This set also provides a basis
for testing control-rod motion within the multi-pin geometry, as well as axial depletion of fuel and absorber materials.
The corresponding geometry is shown in :numref:`figure-triga-netl-problem_4`, and the case specifications are summarized in
:numref:`table-problem-4-definitions`. Axially, the models include the upper and lower grid plates together with
pool-water regions extending to 80 cm above and below the fuel axial centerline.

For depletion cases, the target burnup is again specified in EFPD, based on a full-core power of 1 MW distributed across 110
fuel elements. Because this model represents the full fuel height but not the full core, the applied model power should be
scaled only as needed to preserve the appropriate average power per fuel element.

.. _figure-triga-netl-problem_4:

.. figure:: /_static/images/triga/netl/problem_4.png
   :align: center
   :width: 60%

   Problem 4 Geometry.


.. table:: Problem 4 Definitions
   :name: table-problem-4-definitions


   +---------+----------------------+------------------+-----------------+----------------+---------+
   | Problem | Central Element      | Fuel / Zr Filler | Clad / Coolant  | Coolant        | Burnup  |
   |         |                      | Temp. (K)        | Temp. (K)       | Dens. (g/cc)   | (EFPD)  |
   +=========+======================+==================+=================+================+=========+
   | 4A      |  Water Hole          |  600.0           |  293.15         |  0.9970        |   0.0   |
   +---------+----------------------+------------------+-----------------+----------------+---------+
   | 4B      |  Central Thimble     |  600.0           |  293.15         |  0.9970        |   0.0   |
   +---------+----------------------+------------------+-----------------+----------------+---------+
   | 4C      |  Graphite Element    |  600.0           |  293.15         |  0.9970        |   0.0   |
   +---------+----------------------+------------------+-----------------+----------------+---------+
   | 4D      |  Source Holder       |  600.0           |  293.15         |  0.9970        |   0.0   |
   +---------+----------------------+------------------+-----------------+----------------+---------+
   | 4E      |  TCR                 |  600.0           |  293.15         |  0.9970        |   0.0   |
   |         |  (0%-100% Withdrawn) |                  |                 |                |         |
   +---------+----------------------+------------------+-----------------+----------------+---------+
   | 4F      |  FCCR                |  600.0           |  293.15         |  0.9970        |   0.0   |
   |         |  (0%-100% Withdrawn) |                  |                 |                |         |
   +---------+----------------------+------------------+-----------------+----------------+---------+
   | 4G      |  FCCR                |  600.0           |  293.15         |  0.9970        |  530.0  |
   |         |  (80% Withdrawn)     |                  |                 |                |         |
   +---------+----------------------+------------------+-----------------+----------------+---------+

.. table:: Problem 4 Recommended Outputs

   +--------------------+----------------------------+
   | Output             | Subcategories              |
   +====================+============================+
   | k-eff              |   --                       |
   +--------------------+----------------------------+
   | Flux Spectrum      |   Global                   |
   +--------------------+----------------------------+
   | Isotopic Inventory |   Fuel / TCR Absorber      |
   +--------------------+----------------------------+
   | Pin Powers         |   Radial / Axial / 3D      |
   +--------------------+----------------------------+
   | Rod Worths         |   Differential / Integral  |
   +--------------------+----------------------------+

Problem 5: 3D Full Core
=======================

The fifth progression-problem set extends progression-problem set 3 to a full three-dimensional core model
with all excore features included. As such, it introduces the full axial heterogeneity of the reactor, including
cylindrical beam ports, axial core-element structures, and the rotary specimen rack, together with both axial and
radial vacuum boundary conditions. The geometry for this set is shown in :numref:`figure-reactor-radial-picture`,
and :numref:`figure-reactor-axial-picture`, and the corresponding case specifications are summarized in :numref:`table-problem-5-definitions`.
Axially, the models include upper and lower pool-water regions extending to 80 cm above and below the fuel axial centerline.

.. table:: Problem 5 Definitions
   :name: table-problem-5-definitions

   +---------+------------------------+------------------+-----------------+----------------+
   | Problem | Description            | Fuel / Zr Filler | Clad / Coolant  | Coolant        |
   |         |                        | Temperature (K)  | Temperature (K) | Density (g/cc) |
   +=========+========================+==================+=================+================+
   | 5A      | All Rods Out           | 600.0            | 293.15          | 0.9970         |
   +---------+------------------------+------------------+-----------------+----------------+
   | 5B      | All Rods In            | 600.0            | 293.15          | 0.9970         |
   +---------+------------------------+------------------+-----------------+----------------+
   | 5C      | Transient Rod          | 600.0            | 293.15          | 0.9970         |
   |         | (0%-100% Withdrawn)    |                  |                 |                |
   +---------+------------------------+------------------+-----------------+----------------+
   | 5D      | Regulating Rod         | 600.0            | 293.15          | 0.9970         |
   |         | (0%-100% Withdrawn)    |                  |                 |                |
   +---------+------------------------+------------------+-----------------+----------------+
   | 5E      | Shim Rod 1             | 600.0            | 293.15          | 0.9970         |
   |         | (0%-100% Withdrawn)    |                  |                 |                |
   +---------+------------------------+------------------+-----------------+----------------+
   | 5F      | Shim Rod 2             | 600.0            | 293.15          | 0.9970         |
   |         | (0%-100% Withdrawn)    |                  |                 |                |
   +---------+------------------------+------------------+-----------------+----------------+

.. note::
   For Cases 5C through 5F, all other rods are fully withdrawn.

.. table:: Problem 5 Recommended Outputs

   +--------------------+----------------------------+
   | Output             | Subcategories              |
   +====================+============================+
   | k-eff              |   --                       |
   +--------------------+----------------------------+
   | Flux Spectrum      |   Global                   |
   +--------------------+----------------------------+
   | Pin Powers         |   Radial / Axial / 3D      |
   +--------------------+----------------------------+
   | Rod Worths         |   Differential / Integral  |
   +--------------------+----------------------------+
   | PKE Parameters     |   Beta-effective /         |
   |                    |   Prompt Neutron           |
   |                    |   Generation Time          |
   +--------------------+----------------------------+


References
==========

.. [1] "University of Texas at Austin Nuclear Engineering Teaching Laboratory
       TRIGA Research Reactor", August 2023,
       https://www.nrc.gov/docs/ML2327/ML23279A146.pdf

.. [2] Boeck, H., M. Villa, and Vienna University of Technology,
       Atomic Institute of the Austrian Universities, Vienna (Austria).
       “TRIGA Reactor Characteristics”. 2007.


See Also
========

* :ref:`TRIGA General Specifications <progression_problems_triga_system_specifications>`
* :ref:`NETL TRIGA System Specifications <progression_problems_triga_netl_system_specifications>`
* :ref:`Python Tools for NETL TRIGA <python_tools_triga_netl>`
