.. _progression_problems_triga_netl_simplified_3l_derivation:

=========================================================
Simplified Modified Three-Element Irradiator Derivation
=========================================================

Simplification Strategy
=======================

The detailed modified three-element irradiation facility geometry is specified in
:numref:`table-modified-three-element-detailed-geometry`. The simplified model is derived from
that geometry with the objective of reducing axial heterogeneity while retaining the radial
detail of the facility wherever practical. Reducing the number of axial interfaces decreases
the number of extruded regions required by deterministic transport solvers such as MPACT [1]_ and
can substantially reduce the associated modeling and computational burden.

The simplifications therefore preferentially combine, rearrange, or eliminate short axial
regions whose explicit representation is not expected to be neutronically significant. Radial
interfaces are left unchanged unless adjusting a radius is necessary to construct a simpler
equivalent region. Material volumes are preserved where practical when regions are combined or
material is redistributed. Each exception to volume preservation, along with each changed
radius or axial interface, is identified explicitly in the corresponding derivation below.

The following sections describe each axial simplification independently. Each derivation
identifies the affected portions of the detailed model, explains the reason for the change,
and states the resulting simplified geometry.

Outer Aluminum Casing Simplification
====================================

The detailed outer aluminum casing consists of two overlapping tubes and a solid upper
portion. Tube #1 has an inner radius of 2.23393 cm, an outer radius of 2.30759 cm, and an
axial length of 124.77400 cm. Tube #2 surrounds the upper 81.27660 cm of Tube #1 and has an
outer radius of 2.38125 cm. Above Tube #1, Tube #2 forms a solid aluminum region with an axial
thickness of 3.39830 cm. This construction introduces changes in the casing cross section at
the bottom of Tube #2 and at the top of Tube #1.

The simplified casing replaces Tube #1 and the annular portion of Tube #2 with a single
constant-radius annular tube. This tube begins at the top of the bottom grid plate and extends
upward 124.77400 cm. The solid upper portion is retained immediately above the annular tube
with its original axial thickness of 3.39830 cm. The annular tube retains the original inner
radius of 2.23393 cm. A single outer radius is used for both the annular tube and the solid
upper portion and is selected to preserve their combined aluminum volume. The original
aluminum volume is

.. math::

   V_{\mathrm{Al}}
   =
   \pi\left(2.30759^2-2.23393^2\right)(124.77400)
   +
   \pi\left(2.38125^2-2.30759^2\right)(81.27660)
   +
   \pi\left(2.38125^2\right)(3.39830),

or

.. math::

   V_{\mathrm{Al}}
   =
   131.13147
   +
   88.18862
   +
   60.53709
   =
   279.85718\ \mathrm{cm^3}.

For a shared simplified outer radius :math:`R_{\mathrm{o,simp}}`, volume preservation requires

.. math::

   \pi\left(R_{\mathrm{o,simp}}^2-2.23393^2\right)(124.77400)
   +
   \pi R_{\mathrm{o,simp}}^2(3.39830)
   =
   279.85718.

Solving for the outer radius gives

.. math::

   R_{\mathrm{o,simp}}
   =
   \sqrt{
   \frac{
   279.85718/\pi+2.23393^2(124.77400)
   }{
   124.77400+3.39830
   }}
   =
   2.35651\ \mathrm{cm}.

The simplified casing therefore consists of a 124.77400-cm-long annular tube with an inner
radius of 2.23393 cm and an outer radius of 2.35651 cm, followed by a modeled solid upper
region of axial length 3.39830 cm with the same outer radius. The casing remains aluminum
and its interior is filled with air wherever another facility component is not present.

This simplification eliminates the casing interface at the lower end of Tube #2. The interface
at the top of Tube #1 is retained because the simplified casing changes from an annulus to
solid aluminum at that location.


Pneumatic System Simplification
================================

The detailed pneumatic system contains separate lower closures for the pneumatic tube and its
outer sleeve. The B-10 canister interior wall also extends below the pneumatic sleeve, forming
an additional implied lower closure. These closely spaced aluminum regions introduce axial
interfaces without changing the principal radial arrangement of the pneumatic system.

The simplified pneumatic system removes all three lower closures. The central air passage,
pneumatic tube, annular air gap, and outer sleeve are extended downward to the top of the solid
lower B-10 section. The B-10 canister interior wall terminates at the same interface and is
therefore annular over its complete axial extent.

The common simplified length is obtained by extending the detailed open-tube length through
the pneumatic-tube lower cap, pneumatic-sleeve lower cap, and B-10-canister interior-wall
lower cap. The latter can be calculated from the detailed specification to have a thickness of
0.30000 cm. Extending each pneumatic-system region through these three detailed lower closures
therefore gives the common simplified axial length

.. math::

   L_{\mathrm{pneu,simp}}
   =
   109.73188+0.12400+0.12850+0.30000
   =
   110.28438\ \mathrm{cm}.

Pneumatic-Tube Aluminum
-----------------------

The tube outer radius remains 0.79400 cm. Its inner radius is adjusted to preserve the aluminum
volume of the detailed tube wall and its 0.12400-cm-thick lower closure. The detailed volume is

.. math::

   V_{\mathrm{tube}}
   =
   \pi\left(0.79400^2-0.67000^2\right)(109.73188)
   +
   \pi\left(0.79400^2\right)(0.12400)
   =
   62.82702\ \mathrm{cm^3}.

For the simplified tube inner radius :math:`R_{\mathrm{tube,i}}`, volume preservation requires

.. math::

   \pi\left(0.79400^2-R_{\mathrm{tube,i}}^2\right)(110.28438)
   =
   62.82702.

Solving gives

.. math::

   R_{\mathrm{tube,i}}
   =
   0.67015\ \mathrm{cm}.

Pneumatic-Sleeve and B-10-Canister Interior-Wall Aluminum
---------------------------------------------------------

The pneumatic-sleeve outer radius remains 0.95250 cm, and the B-10-canister interior-wall
outer radius remains 1.03759 cm. Because these two adjoining regions contain the same aluminum
material, their combined volume is preserved while the pneumatic-sleeve inner radius is
adjusted.

The detailed pneumatic sleeve consists of a 109.85588-cm-long annulus and a
0.12850-cm-thick lower closure. Its aluminum volume is

.. math::

   V_{\mathrm{sleeve}}
   =
   \pi\left(0.95250^2-0.86350^2\right)(109.85588)
   +
   \pi\left(0.95250^2\right)(0.12850)
   =
   56.14632\ \mathrm{cm^3}.

The detailed B-10-canister interior wall has a total axial length of 57.78500 cm. Its annular
portion is 57.48500 cm long, and its implied solid lower closure is 0.30000 cm thick. Its
aluminum volume is therefore

.. math::

   V_{\mathrm{wall}}
   =
   \pi\left(1.03759^2-0.95250^2\right)(57.48500)
   +
   \pi\left(1.03759^2\right)(0.30000)
   =
   31.59594\ \mathrm{cm^3}.

In the simplified geometry, the pneumatic sleeve is annular over the complete 110.28438-cm
common length, and the B-10-canister interior wall is annular over its complete 57.78500-cm
length. For the simplified sleeve inner radius :math:`R_{\mathrm{sleeve,i}}`, combined volume
preservation requires

.. math::

   \pi\left(0.95250^2-R_{\mathrm{sleeve,i}}^2\right)(110.28438)
   +
   \pi\left(1.03759^2-0.95250^2\right)(57.78500)
   =
   56.14630+31.59594.

Solving gives

.. math::

   R_{\mathrm{sleeve,i}}
   =
   0.86182\ \mathrm{cm}.

The simplified pneumatic system therefore has a common axial length of 110.28438 cm and retains
its alignment with the top of Tube #1. Its tube inner radius is 0.67015 cm, tube outer radius is
0.79400 cm, sleeve inner radius is 0.86182 cm, and sleeve outer radius is 0.95250 cm. The central
passage and the gap between the tube and sleeve remain filled with air. This construction
replaces the three staggered lower closures with the existing interface at the top of the solid
lower B-10 section.


B4C Canister Simplification
============================

The detailed B4C canister contains a 52.00278-cm-long B4C annulus between a 0.19660-cm-thick
top cap and a 0.20000-cm-thick bottom cap. Its complete axial length is therefore

.. math::

   L_{\mathrm{B4C}}
   =
   0.19660+52.00278+0.20000
   =
   52.39938\ \mathrm{cm}.

The simplified canister eliminates both end caps and extends the radial arrangement of the
B4C-bearing region over this complete axial length. The inner aluminum wall extends from the
pneumatic-sleeve outer radius of 0.95250 cm to the unchanged B4C-region inner radius of
1.11125 cm. The B4C annulus extends from 1.11125 cm to an adjusted outer radius, and the outer
aluminum annulus extends from that adjusted radius to the unchanged canister outer radius of
2.19009 cm.

The adjusted B4C-region outer radius is selected to preserve the B4C volume. The detailed B4C
volume is

.. math::

   V_{\mathrm{B4C}}
   =
   \pi\left(1.89230^2-1.11125^2\right)(52.00278).

For the simplified B4C-region outer radius :math:`R_{\mathrm{B4C,o}}`, volume preservation
requires

.. math::

   \pi\left(R_{\mathrm{B4C,o}}^2-1.11125^2\right)(52.39938)
   =
   \pi\left(1.89230^2-1.11125^2\right)(52.00278).

Solving gives

.. math::

   R_{\mathrm{B4C,o}}
   =
   \sqrt{
   1.11125^2
   +
   \left(1.89230^2-1.11125^2\right)
   \frac{52.00278}{52.39938}
   }
   =
   1.88760\ \mathrm{cm}.

Preserving the B4C volume also preserves the total aluminum volume because the complete
canister length, pneumatic-sleeve outer radius, and canister outer radius remain unchanged.
Within this fixed envelope, the volume not occupied by B4C is occupied by aluminum in both the
detailed and simplified geometries. This simplification removes the two internal interfaces
between the B4C region and the detailed end caps while retaining the overall canister ends.


B-10 Canister Simplification
============================

The B-10 canister simplification eliminates the 0.10000-cm axial air gap between the B4C and
B-10 canisters by extending the B-10 canister top cap and cadmium sleeve upward to the bottom
of the B4C canister. The top cap is retained and its axial thickness therefore increases from
2.54000 cm to

.. math::

   L_{\mathrm{top\ cap,simp}}
   =
   2.54000+0.10000
   =
   2.64000\ \mathrm{cm}.

The 0.63500-cm-thick exterior-wall lower end cap is eliminated by extending the lower B-10
radial arrangement and cadmium sleeve downward through that region. The solid lower B-10
section consequently increases from 2.54000 cm to

.. math::

   L_{\mathrm{solid\ B10,simp}}
   =
   2.54000+0.63500
   =
   3.17500\ \mathrm{cm}.

The detailed upper B-10 region and annular portion of the lower B-10 region are combined into
a single annulus with a constant outer radius. Because the lowest 2.54000 cm of the detailed
lower B-10 region is solid, the combined annular length is

.. math::

   L_{\mathrm{annular\ B10,simp}}
   =
   22.86000+(34.92500-2.54000)
   =
   55.24500\ \mathrm{cm}.

The complete simplified canister and cadmium-sleeve length is therefore

.. math::

   L_{\mathrm{canister,simp}}
   =
   2.64000+55.24500+3.17500
   =
   61.06000\ \mathrm{cm}.

The annular-to-solid B-10 interface is retained because it is also the lower boundary of the
simplified pneumatic system. The B-10 annulus inner radius remains 1.03759 cm, and the canister
interior wall continues to begin at the unchanged pneumatic-sleeve outer radius of 0.95250 cm.

B-10 Volume
-----------

The detailed B-10 volume comprises the 22.86000-cm-long upper annulus, the 32.38500-cm-long
annular portion of the lower region, and the 2.54000-cm-thick solid lower section:

.. math::

   V_{\mathrm{B10}}
   =
   \pi\left(2.00660^2-1.03759^2\right)(22.86000)
   +
   \pi\left(2.04724^2-1.03759^2\right)(32.38500)
   +
   \pi\left(2.04724^2\right)(2.54000)
   =
   562.17383\ \mathrm{cm^3}.

For the simplified B-10 outer radius :math:`R_{\mathrm{B10,o}}`, volume preservation requires

.. math::

   \pi\left(R_{\mathrm{B10,o}}^2-1.03759^2\right)(55.24500)
   +
   \pi R_{\mathrm{B10,o}}^2(3.17500)
   =
   562.17383.

Solving gives

.. math::

   R_{\mathrm{B10,o}}
   =
   2.02019\ \mathrm{cm}.

Canister Aluminum Volume
------------------------

The aluminum-volume calculation for this step begins with the geometry resulting from the
pneumatic-system simplification. The B-10-canister interior wall is therefore annular over its
complete axial extent, with an inner radius of 0.95250 cm and an outer radius of 1.03759 cm.

Before the B-10 canister is simplified, the combined aluminum volume of the interior wall,
exterior wall, top cap, and lower end cap is

.. math::

   V_{\mathrm{Al}}
   =
   \pi\left(2.12090^2-0.95250^2\right)(2.54000)
   +
   \pi\left[
   \left(1.03759^2-0.95250^2\right)
   +
   \left(2.12090^2-2.00660^2\right)
   \right](22.86000)
   +
   \pi\left[
   \left(1.03759^2-0.95250^2\right)
   +
   \left(2.12090^2-2.04724^2\right)
   \right](32.38500)
   +
   \pi\left(2.12090^2-2.04724^2\right)(2.54000)
   +
   \pi\left(2.12090^2\right)(0.63500)
   =
   134.58585\ \mathrm{cm^3}.

The simplified top cap includes both the exterior cap and interior wall and extends from the
pneumatic-sleeve outer radius to the adjusted canister exterior radius. The interior wall is
also retained along the complete simplified B-10 annulus. For an adjusted canister exterior
radius :math:`R_{\mathrm{canister,o}}`, aluminum-volume preservation requires

.. math::

   \pi\left(R_{\mathrm{canister,o}}^2-0.95250^2\right)(2.64000)
   +
   \pi\left[
   \left(1.03759^2-0.95250^2\right)
   +
   \left(R_{\mathrm{canister,o}}^2-2.02019^2\right)
   \right](55.24500)
   +
   \pi\left(R_{\mathrm{canister,o}}^2-2.02019^2\right)(3.17500)
   =
   134.58585.

Solving gives

.. math::

   R_{\mathrm{canister,o}}
   =
   2.11951\ \mathrm{cm}.

Cadmium Volume
--------------

The detailed cadmium sleeve has an inner radius of 2.12090 cm, an outer radius of 2.17090 cm,
and an axial length of 60.32500 cm. The simplified sleeve extends over the complete
61.06000-cm canister length and uses the adjusted canister exterior radius as its inner radius.
For the simplified cadmium outer radius :math:`R_{\mathrm{Cd,o}}`, volume preservation requires

.. math::

   \pi\left(R_{\mathrm{Cd,o}}^2-2.11951^2\right)(61.06000)
   =
   \pi\left(2.17090^2-2.12090^2\right)(60.32500).

Solving gives

.. math::

   R_{\mathrm{Cd,o}}
   =
   2.16895\ \mathrm{cm}.

The simplified B-10 canister therefore contacts the B4C canister above and the silver disk
below. It retains a 2.64000-cm-thick aluminum top cap, followed by a 55.24500-cm-long B-10
annulus and a 3.17500-cm-thick solid B-10 region. The B-10 outer radius is 2.02019 cm, the
canister exterior radius is 2.11951 cm, and the cadmium outer radius is 2.16895 cm. The cadmium
sleeve extends over the complete 61.06000-cm canister length. These changes eliminate the axial
air gap above the canister, the exterior-wall lower end cap, the cadmium termination at that
cap, and the radius change between the detailed upper and lower B-10 regions.


Hollow Aluminum Spacer Simplification
======================================

The detailed hollow aluminum spacer contains a 3.00000-cm-long air-filled hollow section with
a radius of 2.03393 cm, followed by a 0.49472-cm-thick solid aluminum upper cap. Its outer
radius is fixed by the 2.23393-cm inner radius of the outer aluminum casing. The simplified
spacer eliminates the upper cap and extends the hollow region over the complete spacer length

.. math::

   L_{\mathrm{spacer,simp}}
   =
   3.00000+0.49472
   =
   3.49472\ \mathrm{cm}.

The hollow-section radius is adjusted to preserve the aluminum volume. The detailed aluminum
volume is

.. math::

   V_{\mathrm{Al}}
   =
   \pi\left(2.23393^2-2.03393^2\right)(3.00000)
   +
   \pi\left(2.23393^2\right)(0.49472)
   =
   15.80092\ \mathrm{cm^3}.

For the simplified hollow-section radius :math:`R_{\mathrm{hollow}}`, volume preservation
requires

.. math::

   \pi\left(2.23393^2-R_{\mathrm{hollow}}^2\right)(3.49472)
   =
   15.80092.

Solving gives

.. math::

   R_{\mathrm{hollow}}
   =
   1.88448\ \mathrm{cm}.

The simplified spacer therefore has a 2.23393-cm outer radius and a 1.88448-cm air-filled
hollow radius over its complete 3.49472-cm axial thickness. Because the total cylindrical
envelope remains unchanged, preserving the aluminum volume also preserves the air volume.
This simplification removes the internal interface between the hollow section and the solid
upper cap while retaining the overall spacer ends.


References
==========

.. [1] A. Graham, E. Larsen, B. Collins, B. Kochunas, and S. Stimpson, eds.,
   "MPACT 4.4 Theory Manual," ORNL/SPR-2023/3090, Oak Ridge National Laboratory,
   December 2023, https://info.ornl.gov/sites/publications/Files/Pub202495.pdf
