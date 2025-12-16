import openmc
import mpactpy
from coreforge.geometry_elements.triga import FuelElement
from coreforge.geometry_elements.triga.netl import Reactor
from coreforge import openmc_builder

from progression_problems.TRIGA.NETL.default_geometries import DefaultGeometries
from progression_problems.TRIGA.NETL.utils import build_generic_openmc_tallies

reactor = DefaultGeometries.reactor()

def build_openmc_model(reactor: Reactor,
                       spectrum_group_structure: str = "MPACT-51") -> openmc.Model:
    """Build an OpenMC model of the TRIGA NETL reactor.

    Parameters
    ----------
    reactor : Reactor
        The TRIGA NETL reactor geometry element.
    spectrum_group_structure : str
        The energy group structure to use for the multi-group spectrum tally.

    Returns
    -------
    openmc.Model
        The OpenMC model of the TRIGA NETL reactor.
    """

    root_universe = openmc_builder.build(reactor)
    geometry      = openmc.Geometry(root_universe)
    materials     = openmc.Materials(list(geometry.get_all_materials().values()))

    settings           = openmc.Settings()
    settings.batches   = 100
    settings.inactive  = 20
    settings.particles = 10000

    fuel_element = next(e for ring in reactor.core.lattice.elements
                        for e in ring if isinstance(e, FuelElement))
    mesh_zmin    = -0.5 * fuel_element.interior_length
    mesh_zmax    =  0.5 * fuel_element.interior_length
    lower, upper = geometry.bounding_box

    mesh             = openmc.RegularMesh()
    mesh.lower_left  = (lower[0], lower[1], mesh_zmin)
    mesh.upper_right = (upper[0], upper[1], mesh_zmax)
    mesh.dimension   = (1, 1, 10)

    lattices = geometry.get_all_lattices()
    core_lattice = next((lat for lat in lattices.values() if isinstance(lat, openmc.HexLattice)), None)
    if core_lattice is None:
        raise RuntimeError("Core hex lattice not found in reactor geometry.")

    universe_ids = [universe.id for ring in core_lattice.universes for universe in ring]

    tallies      = build_generic_openmc_tallies(spectrum_group_structure, universe_ids, mesh)
    tallies      = openmc.Tallies(list(tallies.values()))

    model = openmc.Model(geometry  = geometry,
                         materials = materials,
                         settings  = settings,
                         tallies   = tallies)

    return model
