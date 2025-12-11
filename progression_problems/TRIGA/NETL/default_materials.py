import openmc

from progression_problems.TRIGA.default_materials import DefaultMaterials as TRIGADefaultMaterials


class DefaultMaterials(TRIGADefaultMaterials):
    """Dataclass containing default materials for NETL TRIGA reactor models.

    This class extends the base TRIGA materials with NETL-specific materials.
    All common TRIGA materials (fresh_fuel, zirc_filler, stainless_steel, graphite,
    aluminum, air, molybdenum) are inherited from TRIGADefaultMaterials.

    References
    ----------
    .. [1] D. R. Redhouse, et al., "Radiation Characterization Summary: NETL Beam Port
           1/5 Free-Field Environment at the 128-inch Core Centerline Adjacent Location,
           (NETL-FF-BP1/5-128-cca).", Nov. 2022. https://doi.org/10.2172/1898256

    """

    @staticmethod
    def water(temperature: float = TRIGADefaultMaterials.DEFAULT_TEMPERATURE,
              density: float = 1.0,
              density_units: str = 'g/cm3') -> openmc.Material:
        """Creates and returns water material.

        Compositions are from [1] pg 60 and density from pg 48

        Parameters
        ----------
        temperature : float
            Temperature of the material in Kelvin.
        density : float
            Density of the material.
        density_units : str
            Units of density.

        Returns
        -------
        openmc.Material
            The water material.

        See Also
        --------
        openmc.Material.set_density : For valid density units and constraints.
        """
        assert temperature >= 0.0, "Temperature must be positive in Kelvin."

        material = openmc.Material(name='Water')
        material.temperature = temperature
        material.set_density(density_units, density)
        material.add_nuclide('H1',  0.6667, percent_type='ao')
        material.add_nuclide('O16', 0.3333, percent_type='ao')
        material.add_s_alpha_beta('c_H_in_H2O')
        return material

    @staticmethod
    def control_rod_absorber(temperature: float = TRIGADefaultMaterials.DEFAULT_TEMPERATURE,
                             density: float = 2.48,
                             density_units: str = 'g/cm3') -> openmc.Material:
        """Creates and returns fuel follower control rod absorber material.

        Compositions are from [1] pg 60 and density from pg 51

        Parameters
        ----------
        temperature : float
            Temperature of the material in Kelvin.
        density : float
            Density of the material.
        density_units : str
            Units of density.

        Returns
        -------
        openmc.Material
            The FFCR absorber material.

        See Also
        --------
        openmc.Material.set_density : For valid density units and constraints.
        """
        assert temperature >= 0.0, "Temperature must be positive in Kelvin."

        material = openmc.Material(name='Control_Rod_Absorber')
        material.temperature = temperature
        material.set_density(density_units, density)
        material.add_nuclide('B10', 0.1592, percent_type='ao')
        material.add_nuclide('B11', 0.6408, percent_type='ao')
        material.add_element('C',   0.2,    percent_type='ao')
        return material

    @staticmethod
    def cadmium(temperature: float = TRIGADefaultMaterials.DEFAULT_TEMPERATURE,
                density: float = 8.65,
                density_units: str = 'g/cm3') -> openmc.Material:
        """Creates and returns cadmium material.

        Compositions are from [1] pg 60 and density from pg 53

        Parameters
        ----------
        temperature : float
            Temperature of the material in Kelvin.
        density : float
            Density of the material.
        density_units : str
            Units of density.

        Returns
        -------
        openmc.Material
            The cadmium material.
        """
        assert temperature >= 0.0, "Temperature must be positive in Kelvin."

        material = openmc.Material(name='Cadmium')
        material.temperature = temperature
        material.set_density(density_units, density)
        material.add_nuclide('Cd106', 0.0125, percent_type='ao')
        material.add_nuclide('Cd108', 0.0089, percent_type='ao')
        material.add_nuclide('Cd110', 0.1249, percent_type='ao')
        material.add_nuclide('Cd111', 0.128,  percent_type='ao')
        material.add_nuclide('Cd112', 0.2413, percent_type='ao')
        material.add_nuclide('Cd113', 0.1222, percent_type='ao')
        material.add_nuclide('Cd114', 0.2873, percent_type='ao')
        material.add_nuclide('Cd116', 0.0749, percent_type='ao')
        return material
