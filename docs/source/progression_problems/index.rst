.. _progression_problems:

====================
Progression Problems
====================

This section presents system specifications and progression problem definitions. The specifications
describe the system elements involved in the progression problems, typically including their geometries,
material compositions, and other relevant properties. The progression problem definitions outline the
specific scenarios or configurations to be modeled using these systems. In most cases, the specifications
and problems incorporate geometric simplifications or omit certain elements to focus on the primary
aspects relevant to general modeling and simulation capabilities. Reactor-specific design features vary
across reactor types, often requiring unique approximations addressed on a case-by-case basis.
Consequently, the progression problems defined here are not intended as exhaustive representations of
actual systems, but rather as simplified models to support benchmarking and validation of computational
methods.

For the progression problems, a range of outputs may be examined to assess code performance with respect
to both predictive accuracy and computational resource requirements. In general, all problems should be
evaluated in terms of compute time, scaling for parallel calculations, and memory usage. For each
problem set, a recommended set of outputs will be provided based on subject-matter expertise. However,
users are encouraged to consider any other outputs relevant to their particular applications, including
outputs not specified in the recommended set.

.. toctree::
   :numbered:
   :maxdepth: 3

   TRIGA/index
