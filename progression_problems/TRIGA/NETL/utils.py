from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

import mpactpy
import openmc

from coreforge import materials, mpact_builder
from coreforge.geometry_elements import CylindricalPinCell, PinCellStack, HexLattice
from coreforge.geometry_elements.triga import CoreElement, FuelElement, GraphiteElement
from coreforge.geometry_elements.triga.netl import CentralThimble, SourceHolder, PNT, Reactor
from coreforge.materials.material import Material
from coreforge.mpact_builder.builder_specs import MaterialSpecs, DEFAULT_MPACT_MATERIAL_SPECS

from progression_problems.constants import THERMAL_ENERGY_CUTOFF


def get_pincell(element: CoreElement,
                pincell_section: Optional[str] = None) -> CylindricalPinCell:
    """Retrieve a stored pincell section from a TRIGA core element.

    Parameters
    ----------
    element : CoreElement
        Element supplying the cross section.
    pincell_section : Optional[str]
        Key in ``element.pincell``. If omitted, use the standard section for
        fuel, graphite, central thimble, source holder, or PNT. Rods and
        irradiators require an explicit key. List-valued sections use their
        first entry, ordered from bottom to top.

    Returns
    -------
    CylindricalPinCell
        Selected stored cross section.
    """
    if pincell_section is None:
        if isinstance(element, FuelElement):
            pincell_section = "fuel"
        elif isinstance(element, GraphiteElement):
            pincell_section = "graphite"
        elif isinstance(element, CentralThimble):
            pincell_section = "thimble"
        elif isinstance(element, SourceHolder):
            pincell_section = "cavity"
        elif isinstance(element, PNT):
            pincell_section = "wrapped_tube" if element.wrapper is not None else "tube"

    pincells = element.pincell
    if pincell_section is None or pincell_section not in pincells:
        raise ValueError(
            f"Select a pincell_section for {type(element).__name__} "
            f"from: {', '.join(pincells)}. Got {pincell_section!r}."
        )
    pincell = pincells[pincell_section]
    if isinstance(pincell, list):
        pincell = pincell[0] if pincell else None
    if not isinstance(pincell, CylindricalPinCell):
        raise ValueError(f"Pincell section {pincell_section!r} is unavailable on {element.name!r}.")
    return pincell


def build_coolant_pincell(coolant: openmc.Material,
                          radii: Sequence[float]) -> CylindricalPinCell:
    """Build a coolant-only cylindrical pincell.

    Parameters
    ----------
    coolant : openmc.Material
        Coolant material to fill all regions.
    radii : Sequence[float]
        Cylindrical mesh radii for the coolant-only pincell.

    Returns
    -------
    CylindricalPinCell
        Coolant-only cylindrical pincell.
    """
    filtered_radii = sorted(set(radii))
    assert filtered_radii, "radii must contain at least one value."
    assert all(radius > 0.0 for radius in filtered_radii), "All coolant pincell radii must be positive."
    coolant_material = Material(coolant)
    return CylindricalPinCell(
        radii=filtered_radii,
        materials=[coolant_material for _ in range(len(filtered_radii) + 1)],
        name="coolant_pincell",
    )


def build_multicell_geometry(
    fuel: FuelElement | CylindricalPinCell | PinCellStack,
    central_element: CoreElement | CylindricalPinCell | PinCellStack | None,
    pitch: float,
) -> HexLattice:
    """Arrange supplied geometry elements in the multicell hexagonal lattice.

    Parameters
    ----------
    fuel : FuelElement | CylindricalPinCell | PinCellStack
        Geometry repeated at the fuel locations. Its outer material also fills
        the lattice exterior and any vacant central location.
    central_element : CoreElement | CylindricalPinCell | PinCellStack | None
        Geometry placed at the central location. ``None`` leaves it vacant.
    pitch : float
        Hexagonal lattice pitch [cm].

    Returns
    -------
    HexLattice
        Multicell lattice containing the supplied geometry elements.
    """
    overlay_central_pincell = (isinstance(fuel, CylindricalPinCell) and
                               isinstance(central_element, CylindricalPinCell))
    f = fuel
    c = None if overlay_central_pincell else central_element
    lattice = [[         f,         ],
               [     f,      f,     ],
               [ f,      f,      f, ],
               [     f,      f,     ],
               [ f,      c,      f, ],
               [     f,      f,     ],
               [ f,      f,      f, ],
               [     f,      f,     ],
               [         f,         ]]

    lattice = HexLattice(pitch          = pitch,
                          outer_material = fuel.outer_material,
                          elements       = lattice,
                          orientation    = 'y')
    return lattice.overlay(central_element) if overlay_central_pincell else lattice


def build_generic_openmc_tallies(spectrum_group_structure: str = "MPACT-51",
                                 universes: Optional[List[int]] = None,
                                 mesh: openmc.RegularMesh = None
) -> Dict[str, openmc.Tally]:
    """Build a set of generic OpenMC tallies for TRIGA problems.

    Parameters
    ----------
    spectrum_group_structure : str
        The energy group structure to use for the multi-group spectrum tally.
    universes : Optional[List[int]]
        A list of universe IDs to which the tallies should be applied. Defaults
        to None.
    mesh : openmc.RegularMesh
        An optional mesh to use for mesh tallies.

    Returns
    -------
    Dict[str, openmc.Tally]
        A dictionary of OpenMC tallies with string keys.
    """

    tallies: Dict[str, openmc.Tally] = {}

    two_group_filter = openmc.EnergyFilter([0.0, THERMAL_ENERGY_CUTOFF, 20.0e6])

    if spectrum_group_structure not in openmc.mgxs.GROUP_STRUCTURES:
        available_group_structures = ", ".join(sorted(openmc.mgxs.GROUP_STRUCTURES))
        raise ValueError(
            f"Unsupported spectrum_group_structure {spectrum_group_structure!r}. "
            f"Expected one of: {available_group_structures}."
        )

    multi_group_filter = openmc.EnergyFilter(
        openmc.mgxs.GROUP_STRUCTURES[spectrum_group_structure]
    )

    tallies["flux"] = openmc.Tally(name="total_flux")
    tallies["flux"].scores = ["flux"]

    tallies["total_rates"] = openmc.Tally(name="total_rates")
    tallies["total_rates"].scores = ["absorption", "scatter", "fission", "nu-fission"]

    tallies["reaction_rates"] = openmc.Tally(name="reaction_rates")
    tallies["reaction_rates"].filters = [two_group_filter]
    tallies["reaction_rates"].scores = ["absorption", "scatter", "fission"]

    tallies["fission"] = openmc.Tally(name="fission")
    tallies["fission"].scores = ["fission", "kappa-fission"]

    tallies["spectrum"] = openmc.Tally(name="spectrum_tally")
    tallies["spectrum"].filters = [multi_group_filter]
    tallies["spectrum"].scores = ["flux"]

    tallies["flux_2G"] = openmc.Tally(name="flux_2G")
    tallies["flux_2G"].scores = ["flux"]
    tallies["flux_2G"].filters = [two_group_filter]

    tallies["source"] = openmc.Tally(name="source_tally")
    tallies["source"].scores = ["kappa-fission"]

    if universes:
        tallies["mesh_tally"] = openmc.Tally(name="mesh_tally")
        tallies["mesh_tally"].scores = ["flux", "absorption", "scatter", "fission", "nu-fission", "kappa-fission"]
        tallies["mesh_tally"].filters = [openmc.UniverseFilter(universes)]
        if mesh:
            tallies["mesh_tally"].filters.append(openmc.MeshFilter(mesh))

    return tallies


DEFAULT_MPACT_SETTINGS: Dict[str, Dict[str, str]] = {
    "state": {"rated_power": "1.0",
              "power":       "1.0",
              "pressure":    "1.0",
              "rated_flow":  "1.0"},

    "xsec": {"xslib":      "ORNL mpact51n19g_71_4.4m1_02212021.fmt",
              "xsshielder": "T SUBGROUP"},

    "options": {"solver":     "1 2",
                 "ray":        "0.05 CHEBYSHEV-YAMAMOTO 16 3",
                 "conv_crit":  "1.0E-6 1.0E-6",
                 "iter_lim":   "50 1 1",
                 "vis_edits":  "F",
                 "scatt_meth": "TCP0",
                 "nodal":      "T SP3",
                 "axial_tl":   "T ISO LFLAT",
                 "parallel":   "1 1 1 1"}
}


DEFAULT_MPACT_MATERIAL_SPECS_MAPPING: Dict[str, mpactpy.Material.MPACTSpecs] = {
    "zirc_filler":          DEFAULT_MPACT_MATERIAL_SPECS[materials.Zr],
    "stainless_steel":      DEFAULT_MPACT_MATERIAL_SPECS[materials.SS304],
    "graphite":             DEFAULT_MPACT_MATERIAL_SPECS[materials.Graphite],
    "aluminum":             DEFAULT_MPACT_MATERIAL_SPECS[materials.Al6061T6],
    "air":                  DEFAULT_MPACT_MATERIAL_SPECS[materials.Air],
    "molybdenum":           DEFAULT_MPACT_MATERIAL_SPECS[materials.Mo],
    "water":                DEFAULT_MPACT_MATERIAL_SPECS[materials.Water],
    "control_rod_absorber": DEFAULT_MPACT_MATERIAL_SPECS[materials.B4C],
    "cadmium":              DEFAULT_MPACT_MATERIAL_SPECS[materials.Cd],
    "lead":                 DEFAULT_MPACT_MATERIAL_SPECS[materials.Pb],
    "enriched_boron":       mpactpy.Material.MPACTSpecs({}, False, False, False, False),
    "natural_b4c":          DEFAULT_MPACT_MATERIAL_SPECS[materials.B4C],
    "silver":               mpactpy.Material.MPACTSpecs({}, False, False, True, False),
    "fuel":                 DEFAULT_MPACT_MATERIAL_SPECS[materials.UZrH].using_fission_product_ids(
        exclude=["Zr91","Zr93","Zr95","Zr96"]
    ),
}

def default_mpact_reactor_specs(reactor: Reactor) -> mpact_builder.triga.netl.Reactor.Specs:
    """Create default MPACT build specifications for a NETL reactor.

    Parameters
    ----------
    reactor : Reactor
        Reactor supplying the optional three-element irradiator geometry.

    Returns
    -------
    mpact_builder.triga.netl.Reactor.Specs
        Fresh reactor specifications with two material divisions in each
        irradiator pin cell's outer region. Physical cylindrical zones retain
        one division. Modified-irradiator feature lists contain one segment spec
        per pin cell, in the geometry's bottom-to-top order. Other settings
        retain the CoreForge defaults.

    Notes
    -----
    The offset three-element irradiator can leave rectangular MPACT quadrants
    entirely enclosed within its physical cylinders. A GCYL mesh requires a radial
    interface intersecting each quadrant. Subdividing the outer coolant adds
    an interface for the default NETL layout without refining physical zones.
    This is a NETL meshing choice, not a guarantee for arbitrary lattice pitches
    or offsets. Callers may modify the returned specifications before building.
    """
    specs = mpact_builder.triga.netl.Reactor.Specs()
    irradiator = reactor.core.three_element_irradiator
    if irradiator is None:
        return specs

    element_specs = mpact_builder.get_builder(irradiator).Specs()
    if isinstance(irradiator, PinCellStack):
        element_specs.segment_specs = {
            segment: _default_irradiator_segment_specs(len(segment.element.zones))
            for segment in irradiator.segments
        }
    else:
        for name, pincells in irradiator.pincell.items():
            if isinstance(pincells, list):
                region_specs = [_default_irradiator_segment_specs(len(pincell.zones))
                                for pincell in pincells]
            else:
                region_specs = _default_irradiator_segment_specs(len(pincells.zones))
            setattr(element_specs, name, region_specs)
    specs.three_element_irradiator_specs = mpact_builder.triga.netl.Reactor.CoreCellSpecs(
        element_specs=element_specs,
        outer_region_specs=_default_irradiator_segment_specs(1),
    )
    return specs


def _default_irradiator_segment_specs(num_zones: int) -> mpact_builder.triga.CoreElement.SegmentSpecs:
    """Create segment specifications that divide only the outer radial region.

    Parameters
    ----------
    num_zones : int
        Number of physical cylindrical zones in the pin cell.

    Returns
    -------
    mpact_builder.triga.CoreElement.SegmentSpecs
        One material division per physical zone and two in the outer region.
    """
    return mpact_builder.triga.CoreElement.SegmentSpecs(
        builder_specs=mpact_builder.CylindricalPinCell.Specs(
            zone_specs=mpact_builder.CylindricalPinCell.meshing(
                ndivr_mat=[1] * num_zones + [2],
            ),
        ),
    )


def default_mpact_material_specs(materials_list: List[Material]) -> MaterialSpecs:
    """Get the default MPACT material specifications for a list of materials.

    Parameters
    ----------
    materials_list : List[Material]
        A list of materials for which to get the default MPACT specifications.

    Returns
    -------
    MaterialSpecs
        A dictionary mapping each material to its default MPACT specifications.

    Notes
    -----
    Materials are matched by name (case-insensitive). Any material whose name is not an
    exact key in the mapping but starts with ``"fuel"`` is treated as U-ZrH fuel, so that
    custom per-location fuels get the correct cross-section / thermal-scattering specs.
    """

    specs: MaterialSpecs = {}
    uzrh_specs = DEFAULT_MPACT_MATERIAL_SPECS_MAPPING["fuel"]
    for material in materials_list:
        material_name = material.name.lower()
        if material_name in DEFAULT_MPACT_MATERIAL_SPECS_MAPPING:
            specs[material] = DEFAULT_MPACT_MATERIAL_SPECS_MAPPING[material_name]
        elif material_name.startswith("fuel"):
            specs[material] = uzrh_specs
    return specs


def unique_materials(materials: Iterable[openmc.Material]) -> List[openmc.Material]:
    """Return materials with duplicate names removed.

    Parameters
    ----------
    materials : Iterable[openmc.Material]
        Materials to scan in input order.

    Returns
    -------
    List[openmc.Material]
        A list containing the first occurrence of each material name, using a
        case-insensitive comparison on ``material.name``.

    Notes
    -----
    The returned objects are the original material instances from ``materials``.
    Later materials with the same name are omitted.
    """

    seen = set()
    unique = []
    for material in materials:
        key = material.name.lower()
        if key not in seen:
            seen.add(key)
            unique.append(material)
    return unique


def plot_model_2D(model:            openmc.Model,
                  basis:            str,
                  filename:         str,
                  slice_coordinate: Optional[float] = None,
                  pixels:           Optional[Tuple[int, int]] = None,
                  with_legend:      bool = False,
                  axis_units:       str = "cm",
                  legend_kwargs:    Optional[Dict[str, object]] = None,
                  max_pixels:       int = 1800,
                  min_pixels:       int = 400,
                  show_axes:        bool = True) -> Path:
    """Render a 2-D geometry plot with OpenMC's Python plotting interface.

    Parameters
    ----------
    model : openmc.Model
        Model whose geometry will be plotted.
    basis : str
        Plot basis understood by OpenMC, such as ``"xy"``, ``"xz"``, or
        ``"yz"``.
    filename : str
        Basename for the output image file.
    slice_coordinate : Optional[float], default: None
        Coordinate of the out-of-plane axis for the requested slice. If omitted,
        the model center is used for that axis.
    pixels : Optional[Tuple[int, int]], default: None
        Explicit pixel resolution. If omitted, the resolution is derived from
        ``width`` using ``max_pixels`` and ``min_pixels``.
    with_legend : bool, default: False
        If ``True``, draw a material or cell legend directly on the saved plot.
    axis_units : str, default: "cm"
        Units used for matplotlib axis labels.
    legend_kwargs : Optional[Dict[str, object]], default: None
        Keyword arguments forwarded to ``matplotlib.pyplot.legend`` when
        ``with_legend`` is enabled.
    max_pixels : int, default: 1800
        Target pixel count along the largest plotted span when ``pixels`` is not
        provided.
    min_pixels : int, default: 400
        Lower bound applied to each computed pixel dimension.
    show_axes : bool, default: True
        Show the plot frame, ticks, and coordinate labels. If ``False``, hide
        them and tightly crop the saved image without exterior padding.

    Returns
    -------
    pathlib.Path
        Path to the saved plot image.
    """

    assert basis in ["xy", "xz", "yz"]


    lower, upper = model.geometry.bounding_box
    origin       = [0.5 * (lo + hi) if math.isfinite(lo) and math.isfinite(hi) else 0.0
                    for lo, hi in zip(lower, upper)]
    span         = [hi - lo for lo, hi in zip(lower, upper)]

    out_of_plane_axis = {"xy": 2, "xz": 1, "yz": 0}.get(basis)
    if slice_coordinate is not None:
        origin[out_of_plane_axis] = float(slice_coordinate)

    width = {"xy": [span[0], span[1]],
             "xz": [span[0], span[2]],
             "yz": [span[1], span[2]]}.get(basis)

    if not all(math.isfinite(value) and value > 0.0 for value in width):
        raise ValueError("Plot width could not be determined from the model geometry.")

    if pixels is None:
        max_span = max(width)
        scale    = max_pixels / max_span if max_span > 0.0 else 1.0
        pixels   = [max(min_pixels, int(width[0] * scale)),
                    max(min_pixels, int(width[1] * scale))]
    else:
        pixels = [int(pixels[0]), int(pixels[1])]

    colors = _build_plot_material_colors(model.materials)

    effective_legend_kwargs = {"loc":            "center left",
                               "bbox_to_anchor": (1.02, 0.5),
                               "frameon":        False}
    if legend_kwargs:
        effective_legend_kwargs.update(legend_kwargs)

    axes = model.geometry.plot(origin     = origin,
                               width      = width,
                               pixels     = pixels,
                               basis      = basis,
                               color_by   = "material",
                               colors     = colors,
                               legend     = False,
                               axis_units = axis_units)

    if with_legend:
        handles = []
        for material in unique_materials(model.materials):
            label = material.name or f"Material {material.id}"
            handles.append(Patch(facecolor=colors[material], edgecolor="black", label=label))
        axes.legend(handles=handles, **effective_legend_kwargs)

    output_path = Path(filename)
    if output_path.suffix == "":
        output_path = output_path.with_suffix(".png")

    savefig_kwargs = {"dpi": axes.figure.dpi}
    if with_legend:
        savefig_kwargs["bbox_inches"] = "tight"
    if not show_axes:
        axes.set_axis_off()
        savefig_kwargs.update(bbox_inches="tight", pad_inches=0)
    axes.figure.savefig(output_path, **savefig_kwargs)
    plt.close(axes.figure)
    return output_path


def _build_plot_material_colors(materials: Iterable[openmc.Material]) -> Dict[openmc.Material, str]:
    """Build a consistent material-to-color mapping for geometry plots.

    Parameters
    ----------
    materials : Iterable[openmc.Material]
        Materials whose names identify their plotting colors.

    Returns
    -------
    Dict[openmc.Material, str]
        Explicit plotting colors, shared by materials with matching names.

    Raises
    ------
    ValueError
        If a material name has no color assignment. Unknown materials must
        not silently appear white like air.
    """

    materials = list(materials)
    colors: Dict[openmc.Material, str] = {}
    unique = unique_materials(materials)
    for material in unique:
        name = material.name.lower()
        if "fuel" in name:
            colors[material] = "darkorange"
        elif "follower" in name or "air" in name:
            colors[material] = "white"
        elif "cadmium" in name or name == "cd":
            colors[material] = "magenta"
        elif "lead" in name or name == "pb":
            colors[material] = "gold"
        elif "silver" in name or name == "ag":
            colors[material] = "teal"
        elif "moly" in name or name == "mo":
            colors[material] = "darkviolet"
        elif "b4c" in name or "boron_carbide" in name or "boron carbide" in name:
            colors[material] = "crimson"
        elif "absorber" in name or "boron" in name:
            colors[material] = "sienna"
        elif "zirc" in name or "zr" in name:
            colors[material] = "limegreen"
        elif "graphite" in name:
            colors[material] = "royalblue"
        elif "aluminum" in name or "aluminium" in name:
            colors[material] = "darkgrey"
        elif "clad" in name or "stainless" in name or "steel" in name:
            colors[material] = "dimgray"
        elif "water" in name or "coolant" in name or "void" in name:
            colors[material] = "skyblue"
        else:
            raise ValueError(f"No plotting color is assigned to material {material.name!r}.")

    for material in materials:
        if material not in colors:
            duplicate = next(item for item in unique if item.name.lower() == material.name.lower())
            colors[material] = colors[duplicate]

    return colors
