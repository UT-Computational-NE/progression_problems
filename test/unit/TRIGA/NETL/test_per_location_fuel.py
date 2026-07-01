import pytest

import progression_problems.TRIGA.NETL as NETL
from progression_problems.TRIGA.NETL.default_materials import DefaultMaterials as NETLDefaultMaterials
from progression_problems.TRIGA.NETL.utils import default_mpact_material_specs

from coreforge import materials
from coreforge.mpact_builder.builder_specs import DEFAULT_MPACT_MATERIAL_SPECS


def _named_fuel(name: str):
    """A default fuel material with a custom name (for per-location placement)."""
    material = NETLDefaultMaterials.fresh_fuel()
    material.name = name
    return material


def test_core_without_fuel_materials_uses_default_fuel():
    """Backward compatibility: omitting fuel_materials leaves fuel locations on the default fuel."""
    core = NETL.DefaultGeometries.core()
    assert core.loading["B-01"].fuel_meat.material.name == "Fuel"
    assert core.loading["C-02"].fuel_meat.material.name == "Fuel"


def test_core_places_custom_fuel_by_location():
    """A fuel_materials map places the named fuel only at the requested fuel locations."""
    fuel_b = _named_fuel("Fuel_Ring_B")
    core = NETL.DefaultGeometries.core(fuel_materials={"B-01": fuel_b, "B-02": fuel_b})

    assert core.loading["B-01"].fuel_meat.material.name == "Fuel_Ring_B"
    assert core.loading["B-02"].fuel_meat.material.name == "Fuel_Ring_B"
    # An unlisted fuel location keeps the default fuel.
    assert core.loading["C-02"].fuel_meat.material.name == "Fuel"


@pytest.mark.parametrize("bad_location", ["C-01", "D-03", "B-99"])
def test_core_rejects_non_fuel_locations(bad_location):
    """Keys that are not fuel positions (rod slot, graphite slot, nonexistent) raise ValueError."""
    fuel = _named_fuel("Fuel_Bad")
    with pytest.raises(ValueError):
        NETL.DefaultGeometries.core(fuel_materials={bad_location: fuel})


def test_reactor_forwards_fuel_materials():
    """reactor() forwards fuel_materials to core()."""
    fuel_b = _named_fuel("Fuel_Ring_B")
    reactor = NETL.DefaultGeometries.reactor(fuel_materials={"B-01": fuel_b})
    assert reactor.core.loading["B-01"].fuel_meat.material.name == "Fuel_Ring_B"


def test_mpact_specs_map_custom_and_default_fuel_to_uzrh():
    """Default and custom per-location fuels map to U-ZrH; the fuel follower is left as-is."""
    fuel_b = _named_fuel("Fuel_Ring_B")
    reactor = NETL.DefaultGeometries.reactor(fuel_materials={"B-01": fuel_b})

    reactor_materials = reactor.get_materials()
    specs = default_mpact_material_specs(reactor_materials)
    uzrh_specs = DEFAULT_MPACT_MATERIAL_SPECS[materials.UZrH]

    by_name = {m.name: m for m in reactor_materials}
    # Sanity: the reactor exposes the default fuel, the custom ring fuel, and the follower.
    assert {"Fuel", "Fuel_Ring_B", "Fuel_Follower_Fuel"} <= set(by_name)

    # Default and custom fuels get the U-ZrH spec...
    assert specs[by_name["Fuel"]] is uzrh_specs
    assert specs[by_name["Fuel_Ring_B"]] is uzrh_specs
    # ...but the fuel follower is deliberately excluded (keeps its existing treatment; issue #24).
    assert by_name["Fuel_Follower_Fuel"] not in specs
