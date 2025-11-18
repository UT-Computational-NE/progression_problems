import openmc


class DefaultMaterials:
    """Dataclass containing default materials for TRIGA reactor models.

    References
    ----------
    .. [1] D. R. Redhouse, et al., "Radiation Characterization Summary: NETL Beam Port
           1/5 Free-Field Environment at the 128-inch Core Centerline Adjacent Location,
           (NETL-FF-BP1/5-128-cca).", Nov. 2022. https://doi.org/10.2172/1898256

    """

    DEFAULT_TEMPERATURE = 293.6

    @classmethod
    def fresh_fuel(cls,
                   temperature:   float = DEFAULT_TEMPERATURE,
                   density:       float = 5.85,
                   density_units: str = 'g/cm3') -> openmc.Material:
        """Creates and returns the default fresh fuel material for TRIGA reactors.

        Compositions are from [1]_ pg 59-60 and density from pg 51

        Parameters
        ----------
        temperature : float
            Temperature of the material in Kelvin.
            Default is DEFAULT_TEMPERATURE.
        density : float
            Density of the material. Default is 5.85 g/cm3.
        density_units : str
            Units of density. Default is 'g/cm3'.

        Returns
        -------
        openmc.Material
            The fresh fuel material.

        See Also
        --------
        openmc.Material.set_density : For valid density units and constraints.
        """
        assert temperature >= 0.0, "Temperature must be positive in Kelvin."

        material = openmc.Material(name='Fresh_Fuel')
        material.temperature = temperature
        material.set_density(density_units, density)
        material.add_nuclide('H1',   0.014355 , percent_type='wo')
        material.add_nuclide('Mn55', 0.0014287, percent_type='wo')
        material.add_nuclide('U235', 0.0152,    percent_type='wo')
        material.add_nuclide('U238', 0.061568,  percent_type='wo')
        material.add_nuclide('Zr90', 0.43706,   percent_type='wo')
        material.add_nuclide('Zr91', 0.0942,    percent_type='wo')
        material.add_nuclide('Zr92', 0.14253,   percent_type='wo')
        material.add_nuclide('Zr94', 0.14136,   percent_type='wo')
        material.add_nuclide('Zr96', 0.02228,   percent_type='wo')
        material.add_element('Cr',   0.013573,  percent_type='wo')
        material.add_element('Fe',   0.049647,  percent_type='wo')
        material.add_element('Ni',   0.0067863, percent_type='wo')
        material.add_s_alpha_beta('c_H_in_ZrH')
        material.add_s_alpha_beta('c_Zr_in_ZrH')
        return material

    @classmethod
    def zirc_filler(cls,
                    temperature: float = DEFAULT_TEMPERATURE,
                    density: float = 0.0408,
                    density_units: str = 'atom/b-cm') -> openmc.Material:
        """Creates and returns zirconium filler rod material.

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
            The zirconium filler material.

        See Also
        --------
        openmc.Material.set_density : For valid density units and constraints.
        """
        assert temperature >= 0.0, "Temperature must be positive in Kelvin."

        material = openmc.Material(name='Zirc_Filler')
        material.temperature = temperature
        material.set_density(density_units, density)
        material.add_nuclide('Zr90', 0.5145, percent_type='ao')
        material.add_nuclide('Zr91', 0.1122, percent_type='ao')
        material.add_nuclide('Zr92', 0.1715, percent_type='ao')
        material.add_nuclide('Zr94', 0.1738, percent_type='ao')
        material.add_nuclide('Zr96', 0.0280, percent_type='ao')
        return material

    @classmethod
    def stainless_steel(cls,
                        temperature: float = DEFAULT_TEMPERATURE,
                        density: float = 0.0858,
                        density_units: str = 'atom/b-cm') -> openmc.Material:
        """Creates and returns stainless steel material.

        Compositions are from [1]_ pg 60 and density from pg 50

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
            The stainless steel material.

        See Also
        --------
        openmc.Material.set_density : For valid density units and constraints.
        """
        assert temperature >= 0.0, "Temperature must be positive in Kelvin."

        material = openmc.Material(name='Stainless_Steel')
        material.temperature = temperature
        material.set_density(density_units, density)
        material.add_element('C',    0.00031519, percent_type='ao')
        material.add_nuclide('Cr50', 0.000782,   percent_type='ao')
        material.add_nuclide('Cr52', 0.014501,   percent_type='ao')
        material.add_nuclide('Cr53', 0.001613,   percent_type='ao')
        material.add_nuclide('Cr54', 0.000394,   percent_type='ao')
        material.add_nuclide('Fe54', 0.003554,   percent_type='ao')
        material.add_nuclide('Fe56', 0.05511,    percent_type='ao')
        material.add_nuclide('Fe57', 0.001257,   percent_type='ao')
        material.add_nuclide('Fe58', 0.000166,   percent_type='ao')
        material.add_nuclide('Ni58', 0.005558,   percent_type='ao')
        material.add_nuclide('Ni60', 0.00207,    percent_type='ao')
        material.add_nuclide('Ni61', 8.85e-05,   percent_type='ao')
        material.add_nuclide('Ni62', 0.000278,   percent_type='ao')
        material.add_nuclide('Ni64', 6.85e-05,   percent_type='ao')
        return material

    @classmethod
    def graphite(cls,
                 temperature: float = DEFAULT_TEMPERATURE,
                 density: float = 1.6,
                 density_units: str = 'g/cm3') -> openmc.Material:
        """Creates and returns graphite material.

        Compositions are from [1]_ pg 60 and density from pg 48

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
            The graphite material.

        See Also
        --------
        openmc.Material.set_density : For valid density units and constraints.
        """
        assert temperature >= 0.0, "Temperature must be positive in Kelvin."

        material = openmc.Material(name='Graphite')
        material.temperature = temperature
        material.set_density(density_units, density)
        material.add_element('C', 1.0, percent_type='ao')
        material.add_s_alpha_beta('c_Graphite')
        return material

    @classmethod
    def aluminum(cls,
                 temperature: float = DEFAULT_TEMPERATURE,
                 density: float = 2.7,
                 density_units: str = 'g/cm3') -> openmc.Material:
        """Creates and returns aluminum 6061-T6 material.

        Compositions are from [1]_ pg 60 and density from pg 48

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
            The aluminum material.

        See Also
        --------
        openmc.Material.set_density : For valid density units and constraints.
        """
        assert temperature >= 0.0, "Temperature must be positive in Kelvin."

        material = openmc.Material(name='Aluminum')
        material.temperature = temperature
        material.set_density(density_units, density)
        material.add_nuclide('B10',  2.3945e-07, percent_type='ao')
        material.add_nuclide('Mg24', 0.00053511, percent_type='ao')
        material.add_nuclide('Mg25', 6.503e-05,  percent_type='ao')
        material.add_nuclide('Mg26', 6.8851e-05, percent_type='ao')
        material.add_nuclide('Al27', 0.059015,   percent_type='ao')
        material.add_nuclide('Si28', 0.00032153, percent_type='ao')
        material.add_nuclide('Si29', 1.5771e-05, percent_type='ao')
        material.add_nuclide('Si30', 1.0062e-05, percent_type='ao')
        material.add_nuclide('Cr50', 2.6872e-06, percent_type='ao')
        material.add_nuclide('Cr52', 4.983e-05,  percent_type='ao')
        material.add_nuclide('Cr53', 5.5435e-06, percent_type='ao')
        material.add_nuclide('Cr54', 1.3544e-06, percent_type='ao')
        material.add_nuclide('Cu63', 5.0017e-05, percent_type='ao')
        material.add_nuclide('Cu65', 2.1628e-05, percent_type='ao')
        return material

    @classmethod
    def air(cls,
            temperature: float = DEFAULT_TEMPERATURE,
            density: float = 0.001225,
            density_units: str = 'g/cm3') -> openmc.Material:
        """Creates and returns air material.

        Compositions are from [1]_ pg 60 and density from pg 48

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
            The air material.

        See Also
        --------
        openmc.Material.set_density : For valid density units and constraints.
        """
        assert temperature >= 0.0, "Temperature must be positive in Kelvin."

        material = openmc.Material(name='Air')
        material.temperature = temperature
        material.set_density(density_units, density)
        material.add_nuclide('N14', 0.79, percent_type='ao')
        material.add_nuclide('O16', 0.21, percent_type='ao')
        return material

    @classmethod
    def molybdenum(cls,
                   temperature: float = DEFAULT_TEMPERATURE,
                   density: float = 10.3,
                   density_units: str = 'g/cm3') -> openmc.Material:
        """Creates and returns molybdenum material.

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
            The molybdenum material.

        See Also
        --------
        openmc.Material.set_density : For valid density units and constraints.
        """
        assert temperature >= 0.0, "Temperature must be positive in Kelvin."

        material = openmc.Material(name='Molybdenum')
        material.temperature = temperature
        material.set_density(density_units, density)
        material.add_nuclide('Mo92',  0.1477, percent_type='ao')
        material.add_nuclide('Mo94',  0.0923, percent_type='ao')
        material.add_nuclide('Mo95',  0.159,  percent_type='ao')
        material.add_nuclide('Mo96',  0.1668, percent_type='ao')
        material.add_nuclide('Mo97',  0.0956, percent_type='ao')
        material.add_nuclide('Mo98',  0.2419, percent_type='ao')
        material.add_nuclide('Mo100', 0.0967, percent_type='ao')
        return material
