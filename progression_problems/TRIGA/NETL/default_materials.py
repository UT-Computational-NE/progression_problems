import openmc

from progression_problems.TRIGA.default_materials import DefaultMaterials as TRIGADefaultMaterials


class DefaultMaterials(TRIGADefaultMaterials):
    """Dataclass containing default materials for NETL TRIGA reactor models.

    This class extends the base TRIGA materials with NETL-specific materials.
    All common TRIGA materials (fresh_fuel, zirc_filler, stainless_steel, graphite,
    aluminum, air, molybdenum) are inherited from TRIGADefaultMaterials. NETL-
    specific materials include the control-rod absorber, cadmium, lead, enriched-
    boron powder, natural-B4C powder, and silver.

    References
    ----------
    .. [1] D. R. Redhouse, et al., "Radiation Characterization Summary: NETL Beam Port
           1/5 Free-Field Environment at the 128-inch Core Centerline Adjacent Location,
           (NETL-FF-BP1/5-128-cca).", Nov. 2022. https://doi.org/10.2172/1898256
    .. [2] C. C. Hudson, "Development of a Radioisotope Production Facility Using a
           Cryogenic Cooling System", Ph.D. dissertation, The University of Texas at
           Austin, December 2025.

    """

    @staticmethod
    def fuel_follower_fuel(temperature:   float = TRIGADefaultMaterials.DEFAULT_TEMPERATURE,
                           density:       float = 6.0124,
                           density_units: str = 'g/cm3') -> openmc.Material:
        """Creates and returns the NETL fuel follower fuel material.

        Compositions are from [1]_ pg 59-60 and density from pg 52

        Parameters
        ----------
        temperature : float
            Temperature of the material in Kelvin.
        density : float
            Density of the material. Default is 6.0124 g/cm3.
        density_units : str
            Units of density. Default is 'g/cm3'.

        Returns
        -------
        openmc.Material
            The NETL fuel follower fuel material.
        """
        material = TRIGADefaultMaterials.fresh_fuel(temperature, density, density_units)
        material.name = 'Fuel_Follower_Fuel'
        return material

    @staticmethod
    def control_rod_absorber(temperature: float = TRIGADefaultMaterials.DEFAULT_TEMPERATURE,
                             density: float = 2.48,
                             density_units: str = 'g/cm3') -> openmc.Material:
        """Creates and returns fuel follower control rod absorber material.

        Compositions are from [1]_ pg 60 and density from pg 51

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

        Compositions are from [1]_ pg 60 and density from pg 53

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

    @staticmethod
    def lead(temperature: float = TRIGADefaultMaterials.DEFAULT_TEMPERATURE,
             density: float = 11.35,
             density_units: str = 'g/cm3') -> openmc.Material:
        """Creates and returns natural lead material.

        Composition is from Ref. [2]_ page 270 and density from page 187.

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
            The lead material.
        """
        assert temperature >= 0.0, "Temperature must be positive in Kelvin."

        material = openmc.Material(name='Lead')
        material.temperature = temperature
        material.set_density(density_units, density)
        material.add_element('Pb', 1.0, percent_type='ao')
        return material

    @staticmethod
    def enriched_boron(
        temperature: float = TRIGADefaultMaterials.DEFAULT_TEMPERATURE,
        density: float = 1.40,
        density_units: str = 'g/cm3',
    ) -> openmc.Material:
        """Create the enriched-boron powder used by the modified 3-EL.

        The density is from Ref. [2]_ page 187 and the isotopic composition is
        from Ref. [2]_ page 277.

        Parameters
        ----------
        temperature : float
            Material temperature in Kelvin. Defaults to
            ``TRIGADefaultMaterials.DEFAULT_TEMPERATURE``.
        density : float
            Material density. Defaults to 1.40 g/cm3, per Ref. [2]_ page 187.
        density_units : str
            Units associated with ``density``. Defaults to ``'g/cm3'``.

        Returns
        -------
        openmc.Material
            Enriched-boron powder material.
        """

        assert temperature >= 0.0, "Temperature must be positive in Kelvin."

        material = openmc.Material(name='Enriched_Boron')
        material.temperature = temperature
        material.set_density(density_units, density)
        material.add_nuclide('B10', 0.96, percent_type='wo')
        material.add_nuclide('B11', 0.04, percent_type='wo')
        return material

    @staticmethod
    def natural_b4c(
        temperature: float = TRIGADefaultMaterials.DEFAULT_TEMPERATURE,
        density: float = 1.46,
        density_units: str = 'g/cm3',
    ) -> openmc.Material:
        """Create the natural-B4C powder used by the modified 3-EL.

        The density is from Ref. [2]_ page 186 and the atom fractions are from
        Ref. [2]_ page 269.

        Parameters
        ----------
        temperature : float
            Material temperature in Kelvin. Defaults to
            ``TRIGADefaultMaterials.DEFAULT_TEMPERATURE``.
        density : float
            Material density. Defaults to 1.46 g/cm3, per Ref. [2]_ page 186.
        density_units : str
            Units associated with ``density``. Defaults to ``'g/cm3'``.

        Returns
        -------
        openmc.Material
            Natural-B4C powder material.
        """

        assert temperature >= 0.0, "Temperature must be positive in Kelvin."

        material = openmc.Material(name='Natural_B4C')
        material.temperature = temperature
        material.set_density(density_units, density)
        material.add_nuclide('B10', 0.159996, percent_type='ao')
        material.add_nuclide('B11', 0.639985, percent_type='ao')
        material.add_element('C', 0.200019, percent_type='ao')
        return material

    @staticmethod
    def silver(
        temperature: float = TRIGADefaultMaterials.DEFAULT_TEMPERATURE,
        density: float = 10.49,
        density_units: str = 'g/cm3',
    ) -> openmc.Material:
        """Create the silver disk material used by the modified 3-EL.

        The density is from Ref. [2]_ page 187 and the isotopic composition is
        from Ref. [2]_ page 277.

        Parameters
        ----------
        temperature : float
            Material temperature in Kelvin. Defaults to
            ``TRIGADefaultMaterials.DEFAULT_TEMPERATURE``.
        density : float
            Material density. Defaults to 10.49 g/cm3, per Ref. [2]_ page 187.
        density_units : str
            Units associated with ``density``. Defaults to ``'g/cm3'``.

        Returns
        -------
        openmc.Material
            Silver material.
        """

        assert temperature >= 0.0, "Temperature must be positive in Kelvin."

        material = openmc.Material(name='Silver')
        material.temperature = temperature
        material.set_density(density_units, density)
        material.add_nuclide('Ag107', 0.51839, percent_type='wo')
        material.add_nuclide('Ag109', 0.48161, percent_type='wo')
        return material
