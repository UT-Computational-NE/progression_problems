from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
import math
import matplotlib.pyplot as plt

import mpactpy
import openmc

from coreforge import materials
from coreforge.materials.material import Material
from coreforge.mpact_builder.builder_specs import MaterialSpecs, DEFAULT_MPACT_MATERIAL_SPECS

from progression_problems.constants import THERMAL_ENERGY_CUTOFF


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


DEFAULT_MPACT_MATERIAL_SPECS_MAPPING: Dict[str, MaterialSpecs] = {
    "fuel":                 DEFAULT_MPACT_MATERIAL_SPECS[materials.UZrH],
    "zirc_filler":          DEFAULT_MPACT_MATERIAL_SPECS[materials.Zr],
    "stainless_steel":      DEFAULT_MPACT_MATERIAL_SPECS[materials.SS304],
    "graphite":             DEFAULT_MPACT_MATERIAL_SPECS[materials.Graphite],
    "aluminum":             DEFAULT_MPACT_MATERIAL_SPECS[materials.Al6061T6],
    "air":                  DEFAULT_MPACT_MATERIAL_SPECS[materials.Air],
    "molybdenum":           DEFAULT_MPACT_MATERIAL_SPECS[materials.Mo],
    "water":                DEFAULT_MPACT_MATERIAL_SPECS[materials.Water],
    "control_rod_absorber": DEFAULT_MPACT_MATERIAL_SPECS[materials.B4C],
    "cadmium":              mpactpy.Material.MPACTSpecs({}, False, False, False, False),
}


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
    """

    specs: MaterialSpecs = {}
    for material in materials_list:
        material_name = material.name.lower()
        if material_name in DEFAULT_MPACT_MATERIAL_SPECS_MAPPING:
            specs[material] = DEFAULT_MPACT_MATERIAL_SPECS_MAPPING[material_name]
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
                  min_pixels:       int = 400) -> None:
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
    """

    assert basis in ["xy", "xz", "yz"]


    lower, upper = model.geometry.bounding_box
    origin       = [(lo + hi) * 0.5 for lo, hi in zip(lower, upper)]
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

    effective_legend_kwargs = {"loc":            "center right",
                               "bbox_to_anchor": (1.02, 0.5),
                               "frameon":        False}
    if legend_kwargs:
        effective_legend_kwargs.update(legend_kwargs)

    axes = model.geometry.plot(origin        = origin,
                               width         = width,
                               pixels        = pixels,
                               basis         = basis,
                               color_by      = "material",
                               colors        = colors,
                               legend        = with_legend,
                               legend_kwargs = effective_legend_kwargs if with_legend else None,
                               axis_units    = axis_units)

    output_path = Path(filename)
    if output_path.suffix == "":
        output_path = output_path.with_suffix(".png")

    savefig_kwargs = {"dpi": axes.figure.dpi}
    if with_legend:
        savefig_kwargs["bbox_inches"] = "tight"
    axes.figure.savefig(output_path, **savefig_kwargs)
    plt.close(axes.figure)


def _build_plot_material_colors(materials: Iterable[openmc.Material]) -> Dict[openmc.Material, str]:
    """Build a consistent material-to-color mapping for geometry plots."""

    colors: Dict[openmc.Material, str] = {}
    unique = unique_materials(materials)
    for material in unique:
        name = material.name.lower()
        if "fuel" in name:
            colors[material] = "darkorange"
        elif "follower" in name or "air" in name:
            colors[material] = "white"
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
            colors[material] = "white"

    for material in materials:
        if material not in colors:
            duplicate = next((item for item in unique if item.name.lower() == material.name.lower()), material)
            colors[material] = colors.get(duplicate, "white")

    return colors
