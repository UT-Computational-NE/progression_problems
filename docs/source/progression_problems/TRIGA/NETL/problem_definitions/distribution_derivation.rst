.. _progression_problems_triga_netl_problem_definitions_distribution_derivation:

==========================================
NETL TRIGA Fuel Radial Profile Derivations
==========================================

.. _progression_problems_triga_netl_temperature_profile_derivation:

Temperature Profile Derivation
==============================

The radial temperature profile is based on the steady-state, one-dimensional
heat conduction equation in cylindrical coordinates with volumetric heat
generation, consistent with the annular fuel treatment in Reference [1]_:

.. math::
   :label: eq-triga-derivation-steady-radial-heat-equation

   \frac{1}{r}\frac{d}{dr}
   \left(
   k r \frac{dT}{dr}
   \right)
   +
   \dot{q}
   =
   0

In the actual TRIGA fuel element, neither the volumetric heat-generation rate nor the thermal
conductivity is expected to be spatially constant. The radial power distribution may be biased
toward the fuel periphery due to neutron spatial self-shielding, which would tend to reduce heat
generation near the interior relative to the outer fuel region. In addition, the thermal
conductivity of U-ZrH is temperature dependent and, for commonly used empirical correlations,
increases with temperature over the range of interest [2]_. Both effects would
tend to reduce the center-to-surface temperature difference relative to the constant-conductivity,
uniform-power-generation case, resulting in a flatter radial temperature profile.

For the present assessment, however, the objective is to define a simple and intentionally
challenging temperature distribution for testing temperature-dependent cross-section feedback.
Therefore, the heat-generation rate and thermal conductivity are assumed to be constant over the
U-ZrH fuel meat. These assumptions simplify the analytical treatment while producing a steeper
radial temperature gradient than would generally be expected from a more detailed
temperature- and power-dependent model.

Assuming constant thermal conductivity, :eq:`eq-triga-derivation-steady-radial-heat-equation`
reduces to

.. math::
   :label: eq-triga-derivation-steady-radial-heat-equation-constant-k

   \frac{1}{r}\frac{d}{dr}
   \left(
   r \frac{dT}{dr}
   \right)
   +
   \frac{\dot{q}}{k}
   =
   0

For the U-ZrH fuel meat, the inner boundary is located at
:math:`R_{\mathrm{Zr}}` and the outer fuel boundary is located at
:math:`R_f`. The central zirconium filler rod is assumed to produce no fission
power. Therefore, in the one-dimensional radial model, the inner fuel boundary is
taken to have zero radial heat flux,

.. math::
   :label: eq-triga-derivation-inner-fuel-zero-flux-bc

   \left.\frac{dT}{dr}\right|_{r=R_{\mathrm{Zr}}}
   =
   0

The outer fuel boundary is assigned the prescribed boundary temperature,

.. math::
   :label: eq-triga-derivation-outer-fuel-temperature-bc

   T(R_f) = T_b

Starting from :eq:`eq-triga-derivation-steady-radial-heat-equation-constant-k`,
multiplying by :math:`r` gives

.. math::

   \frac{d}{dr}
   \left(
   r\frac{dT}{dr}
   \right)
   =
   -\frac{\dot{q}}{k}r

Integrating once with respect to :math:`r` gives

.. math::

   r\frac{dT}{dr}
   =
   -\frac{\dot{q}}{2k}r^2
   +
   C_1

Dividing by :math:`r` gives

.. math::

   \frac{dT}{dr}
   =
   -\frac{\dot{q}}{2k}r
   +
   \frac{C_1}{r}

The integration constant :math:`C_1` is determined by applying the zero-flux
inner boundary condition from :eq:`eq-triga-derivation-inner-fuel-zero-flux-bc`:

.. math::

   0
   =
   -\frac{\dot{q}}{2k}R_{\mathrm{Zr}}
   +
   \frac{C_1}{R_{\mathrm{Zr}}}

Solving for :math:`C_1` gives

.. math::

   C_1
   =
   \frac{\dot{q}}{2k}R_{\mathrm{Zr}}^2

Therefore, the radial temperature gradient can be written as

.. math::

   \frac{dT}{dr}
   =
   \frac{\dot{q}}{2k}
   \left(
   \frac{R_{\mathrm{Zr}}^2}{r}
   -
   r
   \right)

Integrating again with respect to :math:`r` gives the general temperature
profile,

.. math::

   T(r)
   =
   \frac{\dot{q}}{2k}
   \left[
   R_{\mathrm{Zr}}^2\ln r
   -
   \frac{r^2}{2}
   \right]
   +
   C_2

The second integration constant is determined using the prescribed outer
fuel-boundary temperature from :eq:`eq-triga-derivation-outer-fuel-temperature-bc`:

.. math::

   T_b
   =
   \frac{\dot{q}}{2k}
   \left[
   R_{\mathrm{Zr}}^2\ln R_f
   -
   \frac{R_f^2}{2}
   \right]
   +
   C_2

Solving for :math:`C_2` and substituting back into the general solution gives

.. math::
   :label: eq-triga-derivation-radial-temperature-dimensional

   T(r)
   =
   T_b
   +
   \frac{\dot{q}}{4k}
   \left[
   R_f^2-r^2
   +
   2R_{\mathrm{Zr}}^2\ln\left(r/R_f\right)
   \right],
   \qquad
   R_{\mathrm{Zr}} < r \le R_f

This expression still contains the ratio :math:`\dot{q}/k`. To express the
profile in terms of the imposed maximum fuel temperature, the expression is
evaluated at the inner fuel boundary. Because the inner boundary is adiabatic,
the maximum fuel temperature occurs at :math:`r = R_{\mathrm{Zr}}`:

.. math::

   T_{\max}
   =
   T(R_{\mathrm{Zr}})
   =
   T_b
   +
   \frac{\dot{q}}{4k}
   \left[
   R_f^2-R_{\mathrm{Zr}}^2
   +
   2R_{\mathrm{Zr}}^2
   \ln\left(R_{\mathrm{Zr}}/R_f\right)
   \right]

Rearranging gives

.. math::

   \frac{\dot{q}}{4k}
   =
   \frac{
   T_{\max}-T_b
   }{
   \left(R_f^2-R_{\mathrm{Zr}}^2\right)
   +
   2R_{\mathrm{Zr}}^2
   \ln\left(R_{\mathrm{Zr}}/R_f\right)
   }

Substituting this expression into
:eq:`eq-triga-derivation-radial-temperature-dimensional` gives the normalized
fuel-meat temperature profile:

.. math::
   :label: eq-triga-derivation-radial-temperature-profile-derived

   T(r)
   =
   T_b
   +
   \left(T_{\max}-T_b\right)
   \frac{
   \left(R_f^2-r^2\right)
   +
   2R_{\mathrm{Zr}}^2\ln\left(r/R_f\right)
   }{
   \left(R_f^2-R_{\mathrm{Zr}}^2\right)
   +
   2R_{\mathrm{Zr}}^2\ln\left(R_{\mathrm{Zr}}/R_f\right)
   },
   \qquad
   R_{\mathrm{Zr}} < r \le R_f



.. _progression_problems_triga_netl_temperature_profile_discretization:

Temperature Profile Discretization
----------------------------------

Although :eq:`eq-triga-derivation-radial-temperature-profile-derived` defines a
continuous radial temperature distribution, the neutronics models will typically
represent the fuel meat using a finite number of annular material regions.
Therefore, each radial fuel ring is assigned a single representative temperature.
For consistency with the cylindrical geometry, this representative temperature is
taken to be the area-weighted average temperature over the annulus.

For a fuel ring bounded by :math:`r_{i-1}` and :math:`r_i`, the ring-averaged
temperature is

.. math::
   :label: eq-triga-derivation-ring-average-temperature-definition

   T_i
   =
   \frac{
   \int_{r_{i-1}}^{r_i} T(r)\,2\pi r\,dr
   }{
   \int_{r_{i-1}}^{r_i} 2\pi r\,dr
   }

The factor of :math:`2\pi` cancels, and the denominator evaluates to
:math:`(r_i^2-r_{i-1}^2)/2`. Therefore,

.. math::

   T_i
   =
   \frac{
   2
   }{
   r_i^2-r_{i-1}^2
   }
   \int_{r_{i-1}}^{r_i} T(r)\,r\,dr

Substituting the fuel-meat temperature profile from
:eq:`eq-triga-derivation-radial-temperature-profile-derived` gives

.. math::

   T_i
   =
   \frac{
   2
   }{
   r_i^2-r_{i-1}^2
   }
   \int_{r_{i-1}}^{r_i}
   \left[
   T_b
   +
   \left(T_{\max}-T_b\right)
   \frac{
   \left(R_f^2-r^2\right)
   +
   2R_{\mathrm{Zr}}^2\ln\left(r/R_f\right)
   }{
   \left(R_f^2-R_{\mathrm{Zr}}^2\right)
   +
   2R_{\mathrm{Zr}}^2\ln\left(R_{\mathrm{Zr}}/R_f\right)
   }
   \right]
   r\,dr

Define the denominator of the normalized temperature profile as

.. math::

   D_T
   =
   \left(R_f^2-R_{\mathrm{Zr}}^2\right)
   +
   2R_{\mathrm{Zr}}^2\ln\left(R_{\mathrm{Zr}}/R_f\right)

Then the ring-averaged temperature may be written as

.. math::

   T_i
   =
   T_b
   +
   \left(T_{\max}-T_b\right)
   \frac{
   2
   }{
   \left(r_i^2-r_{i-1}^2\right)D_T
   }
   \int_{r_{i-1}}^{r_i}
   \left[
   \left(R_f^2-r^2\right)
   +
   2R_{\mathrm{Zr}}^2\ln\left(r/R_f\right)
   \right]
   r\,dr

The remaining integral can be evaluated analytically by defining

.. math::
   :label: eq-triga-derivation-ring-average-temperature-g-function

   \begin{aligned}
   G(r)
   &=
   \int
   \left[
   \left(R_f^2-r^2\right)
   +
   2R_{\mathrm{Zr}}^2\ln\left(r/R_f\right)
   \right]
   r\,dr \\
   &=
   \frac{R_f^2 r^2}{2}
   -
   \frac{r^4}{4}
   +
   R_{\mathrm{Zr}}^2 r^2\ln\left(r/R_f\right)
   -
   \frac{R_{\mathrm{Zr}}^2 r^2}{2}
   \end{aligned}

Using this antiderivative, the final closed-form ring-averaged temperature is

.. math::
   :label: eq-triga-derivation-ring-average-temperature-closed-form

   T_i
   =
   T_b
   +
   \left(T_{\max}-T_b\right)
   \frac{
   2\left[
   G(r_i)-G(r_{i-1})
   \right]
   }{
   \left(r_i^2-r_{i-1}^2\right)
   D_T
   }

This expression applies to annular rings in the U-ZrH fuel meat, where
:math:`R_{\mathrm{Zr}} < r_{i-1} < r_i \le R_f`. If the central zirconium
filler region is discretized, each filler-region ring is assigned

.. math::

   T_i = T_{\max}

Thus, :eq:`eq-triga-derivation-ring-average-temperature-closed-form` provides
the ring-wise temperature used for each U-ZrH material region in the neutronics
model.


.. _progression_problems_triga_netl_hydrogen_profile_derivation:

Hydrogen Distribution Profile Derivation
========================================

The preceding temperature-profile derivation defines a representative radial
temperature distribution through the U-ZrH fuel meat. Given this temperature
profile, a corresponding radial hydrogen redistribution profile can be estimated
using the thermal-migration model described by Huang et al. [3_].

Huang et al. model hydrogen migration in zirconium hydride using traditional
diffusion theory. In one-dimensional radial form, their hydrogen flux expression
can be written as

.. math::
   :label: eq-triga-derivation-hydrogen-flux

   J_H =
   -D
   \left[
   \frac{dC}{dr}
   +
   \frac{Q^\ast C}{R_g T^2}
   \frac{dT}{dr}
   \right]

where:

* :math:`J_H` is the hydrogen flux,
* :math:`D` is the hydrogen diffusion coefficient,
* :math:`C` is the local hydrogen concentration,
* :math:`Q^\ast` is the heat of transport for hydrogen in zirconium hydride,
* :math:`R_g` is the universal gas constant,
* :math:`T` is the local temperature, and
* :math:`r` is the radial position.

For the present application, the goal is to estimate a steady-state hydrogen
redistribution profile corresponding to the imposed radial temperature profile.
At steady state, assuming no net radial hydrogen flux,

.. math::

   J_H = 0

Applying this condition to :eq:`eq-triga-derivation-hydrogen-flux`, Huang et al. show
in Eq. (3) that this will produce the following expression for the hydrogen concentration:

.. math::
   :label: eq-triga-derivation-hydrogen-concentration

   C(r)
   =
   A
   \exp\left(
   \frac{Q^\ast}{R_g T(r)}
   \right)

where :math:`A` is a proportionality constant. Since the local H/Zr ratio,
:math:`x(r)`, is proportional to the local hydrogen concentration if the
zirconium atom density is treated as spatially uniform, the same functional form
is used for the local hydrogen-to-zirconium ratio:

.. math::

   x(r)
   =
   A
   \exp\left(
   \frac{Q^\ast}{R_g T(r)}
   \right)

The expression above defines the relative radial shape of the hydrogen
redistribution profile, but the proportionality constant :math:`A` must still be
determined. To do this, define the temperature-dependent migration weighting
function

.. math::
   :label: eq-triga-derivation-hydrogen-weighting-function

   f(r)
   =
   \exp\left(
   \frac{Q^\ast}{R_g T(r)}
   \right)

Then

.. math::

   x(r) = A f(r)

The constant :math:`A` is chosen so that the area-averaged H/Zr ratio over the
U-ZrH fuel meat is equal to the nominal fuel stoichiometry. For U-ZrH
:sub:`1.6` fuel,

.. math::

   \bar{x} = 1.6

The area-averaged H/Zr ratio over the fuel meat is

.. math::
   :label: eq-triga-derivation-hydrogen-area-average-definition

   \bar{x}
   =
   \left\langle x(r) \right\rangle_A
   =
   \frac{
   \int_{R_{\mathrm{Zr}}}^{R_f} x(r)\,2\pi r\,dr
   }{
   \int_{R_{\mathrm{Zr}}}^{R_f} 2\pi r\,dr
   }

Substituting :math:`x(r)=A f(r)` gives

.. math::

   \bar{x}
   =
   \left\langle A f(r) \right\rangle_A

Since :math:`A` is constant, it can be pulled outside the area average:

.. math::

   \bar{x}
   =
   A \left\langle f(r) \right\rangle_A

Solving for :math:`A` gives

.. math::

   A
   =
   \frac{\bar{x}}{\left\langle f(r) \right\rangle_A}

Substituting this result back into :math:`x(r)=A f(r)` gives

.. math::

   x(r)
   =
   \bar{x}
   \frac{
   f(r)
   }{
   \left\langle f(r) \right\rangle_A
   }

Finally, substituting the definition of :math:`f(r)` gives

.. math::
   :label: eq-triga-derivation-radial-hydrogen-profile

   x(r)
   =
   \bar{x}
   \frac{
   \exp\left(
   \frac{Q^\ast}{R_g T(r)}
   \right)
   }{
   \left\langle
   \exp\left(
   \frac{Q^\ast}{R_g T(r)}
   \right)
   \right\rangle_A
   }

The central zirconium filler region is not included in this normalization because
it is not part of the U-ZrH fuel meat. With the sign convention used above, a
positive value of :math:`Q^\ast` produces hydrogen depletion in the hotter fuel
region and hydrogen enrichment toward the colder fuel boundary.

Following Huang et al., the heat of transport is taken as
:math:`Q^\ast = 5.3 \times 10^3\ \mathrm{J/mol}`. The universal gas constant is
:math:`R_g = 8.314\ \mathrm{J/(mol\cdot K)}`.



.. _progression_problems_triga_netl_hydrogen_profile_discretization:

Hydrogen Profile Discretization
-------------------------------

Although :eq:`eq-triga-derivation-radial-hydrogen-profile` defines a continuous
hydrogen redistribution profile, the neutronics model represents the U-ZrH fuel
meat using a finite number of annular material regions. Therefore, each radial
fuel ring is assigned a single representative H/Zr ratio.

For fuel ring :math:`i`, bounded by :math:`r_{i-1}` and :math:`r_i`, the
corresponding ring-averaged migration weighting is defined as

.. math::
   :label: eq-triga-derivation-hydrogen-ring-averaged-weighting

   f_i
   =
   \frac{
   2
   }{
   r_i^2-r_{i-1}^2
   }
   \int_{r_{i-1}}^{r_i}
   f(r)\,r\,dr.

The ring-wise H/Zr ratio is then computed by normalizing the ring-wise migration
weighting so that the area-averaged H/Zr ratio over the U-ZrH fuel meat remains
equal to the nominal stoichiometry:

.. math::
   :label: eq-triga-derivation-ring-hydrogen-profile

   x_i
   =
   \bar{x}
   \frac{
   f_i
   }{
   \sum_{j=1}^{N} w_j f_j
   },

where :math:`w_j` is the area fraction of fuel ring :math:`j`,

.. math::
   :label: eq-triga-derivation-hydrogen-ring-area-weight

   w_j
   =
   \frac{
   r_j^2-r_{j-1}^2
   }{
   R_f^2-R_{\mathrm{Zr}}^2
   }.

With this definition, the discrete hydrogen distribution preserves the nominal
fuel stoichiometry:

.. math::

   \sum_{i=1}^{N} w_i x_i = \bar{x}.

The remaining task is evaluating :math:`f_i` for each fuel ring. Substituting
the definition of :math:`f(r)` gives

.. math::

   f_i
   =
   \frac{
   2
   }{
   r_i^2-r_{i-1}^2
   }
   \int_{r_{i-1}}^{r_i}
   \exp\left(
   \frac{Q^\ast}{R_g T(r)}
   \right)
   r\,dr.

Because :math:`T(r)` contains both polynomial and logarithmic radial terms, this
integral does not have a convenient closed-form expression. For sufficiently
thin radial rings, the migration weighting may be approximated by evaluating the
continuous weighting function at the ring-averaged temperature,

.. math::

   f_i
   \approx
   \exp\left(
   \frac{Q^\ast}{R_g T_i}
   \right),

where :math:`T_i` is the area-averaged ring temperature from the preceding
section. However, because the migration weighting is nonlinear in temperature,
this approximation is not exactly equivalent to area-averaging :math:`f(r)` over
the ring:

.. math::

   \left\langle
   f(T(r))
   \right\rangle_i
   \ne
   f\left(
   \left\langle T(r) \right\rangle_i
   \right).

Therefore, if the radial rings are not sufficiently fine, :math:`f_i` should be
evaluated numerically using the continuous temperature profile
:math:`T(r)`. This numerical integration is straightforward because
:math:`T(r)` is known analytically, but the resulting expression for
:math:`f_i` is not itself a simple closed-form expression.


References
==========

.. [1] Todreas, N. E. and Kazimi, M. S., "Nuclear Systems I:
       Thermal Hydraulic Fundamentals", Hemisphere Publishing Corporation,
       New York, 1990, ISBN 1-56032-051-6.

.. [2] Simnad, M. T. and Foushee, F. C. and West, G. B. (1976),
       "Fuel Elements for Pulsed TRIGA® Research Reactors",
       Nuclear Technology, 28(1), 31–56. https://doi.org/10.13182/NT76-A31537

.. [3] Huang, J., Tsuchiya, B., Konashi, K., & Yamawaki, M
       "Estimation of Hydrogen Redistribution in Zirconium Hydride under Temperature Gradient"
       Journal of Nuclear Science and Technology, 37(10), 887–892.
       https://doi.org/10.1080/18811248.2000.9714969