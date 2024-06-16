"""The model module for the simulator spectrometer."""

import logging
from quackseq.spectrometer.spectrometer_model import SpectrometerModel
from quackseq.spectrometer.spectrometer_settings import (
    IntSetting,
    FloatSetting,
    StringSetting,
    SelectionSetting,
)

logger = logging.getLogger(__name__)


class SimulatorModel(SpectrometerModel):
    """Model class for the simulator spectrometer."""

    # Simulation settings
    NUMBER_POINTS = "N. simulation points"
    NUMBER_ISOCHROMATS = "N. of isochromats"
    INITIAL_MAGNETIZATION = "Initial magnetization"
    GRADIENT = "Gradient (mT/m))"
    NOISE = "Noise (uV)"

    # Hardware settings
    LENGTH_COIL = "Length coil (mm)"
    DIAMETER_COIL = "Diameter coil (mm)"
    NUMBER_TURNS = "Number turns"
    Q_FACTOR_TRANSMIT = "Q factor Transmit"
    Q_FACTOR_RECEIVE = "Q factor Receive"
    POWER_AMPLIFIER_POWER = "PA power (W)"
    GAIN = "Gain"
    TEMPERATURE = "Temperature (K)"
    AVERAGES = "Averages"
    LOSS_TX = "Loss TX (dB)"
    LOSS_RX = "Loss RX (dB)"
    CONVERSION_FACTOR = "Conversion factor"

    # Sample settings, this will  be done in a separate module later on
    SAMPLE_NAME = "Name"
    NUMBER_ATOMS = "N. atoms (1/m^3)"
    DENSITY = "Density (g/cm^3)"
    MOLAR_MASS = "Molar mass (g/mol)"
    RESONANT_FREQUENCY = "Resonant freq. (MHz)"
    GAMMA = "Gamma (MHz/T)"
    NUCLEAR_SPIN = "Nuclear spin"
    SPIN_FACTOR = "Spin factor"
    POWDER_FACTOR = "Powder factor"
    FILLING_FACTOR = "Filling factor"
    T1 = "T1 (µs)"
    T2 = "T2 (µs)"
    T2_STAR = "T2* (µs)"
    ATOM_DENSITY = "Atom density (1/cm^3)"
    SAMPLE_VOLUME = "Sample volume (m^3)"
    SAMPLE_LENGTH = "Sample length (m)"
    SAMPLE_DIAMETER = "Sample diameter (m)"

    # Categories of the settings
    SIMULATION = "Simulation"
    HARDWARE = "Hardware"
    EXPERIMENTAL_Setup = "Experimental Setup"
    SAMPLE = "Sample"

    def __init__(self):
        """Initializes the SimulatorModel."""
        super().__init__()

        # Simulation settings
        number_of_points_setting = IntSetting(
            self.NUMBER_POINTS,
            self.SIMULATION,
            8192,
            "Number of points used for the simulation. This influences the dwell time in combination with the total event simulation given by the pulse sequence.",
            min_value=0,
        )
        self.add_setting(
            "number_points",
            number_of_points_setting,
        )

        number_of_isochromats_setting = IntSetting(
            self.NUMBER_ISOCHROMATS,
            self.SIMULATION,
            1000,
            "Number of isochromats used for the simulation. This influences the computation time.",
            min_value=0,
            max_value=10000,
        )
        self.add_setting("number_isochromats", number_of_isochromats_setting)

        initial_magnetization_setting = FloatSetting(
            self.INITIAL_MAGNETIZATION,
            self.SIMULATION,
            1,
            "Initial magnetization",
            min_value=0,
        )
        self.add_setting("initial_magnetization", initial_magnetization_setting)

        gradient_setting = FloatSetting(
            self.GRADIENT,
            self.SIMULATION,
            1,
            "Gradient",
        )
        self.add_setting("gradient", gradient_setting)

        noise_setting = FloatSetting(
            self.NOISE,
            self.SIMULATION,
            2,
            "Adds a specified level of noise for one average without gain. The noise is still multiplied with the receiver gain, as is the signal. The noise scales with the square root of the averages whereas the signal scales with the number of averages.",
            min_value=0,
            max_value=100,
            slider=True,
        )
        self.add_setting("noise", noise_setting)

        # Hardware settings
        coil_length_setting = FloatSetting(
            self.LENGTH_COIL,
            self.HARDWARE,
            30,
            "The length of the sample coil within the hardware setup.",
            min_value=1,
            suffix="mm",
        )
        self.add_setting("length_coil", coil_length_setting)

        coil_diameter_setting = FloatSetting(
            self.DIAMETER_COIL,
            self.HARDWARE,
            8,
            "The diameter of the sample coil.",
            min_value=1,
            suffix="mm",
        )
        self.add_setting("diameter_coil", coil_diameter_setting)

        number_turns_setting = FloatSetting(
            self.NUMBER_TURNS,
            self.HARDWARE,
            8,
            "The total number of turns of the sample coil.",
            min_value=1,
        )
        self.add_setting("number_turns", number_turns_setting)

        q_factor_transmit_setting = FloatSetting(
            self.Q_FACTOR_TRANSMIT,
            self.HARDWARE,
            80,
            "The quality factor of the transmit path, which has an effect on the field strength for excitation.",
            min_value=1,
        )
        self.add_setting("q_factor_transmit", q_factor_transmit_setting)

        q_factor_receive_setting = FloatSetting(
            self.Q_FACTOR_RECEIVE,
            self.HARDWARE,
            80,
            "The quality factor of the receive path, which has an effect on the final SNR.",
            min_value=1,
        )
        self.add_setting("q_factor_receive", q_factor_receive_setting)

        power_amplifier_power_setting = FloatSetting(
            self.POWER_AMPLIFIER_POWER,
            self.HARDWARE,
            110,
            "The power output capability of the power amplifier, determines the strength of pulses that can be generated.",
            min_value=0.1,
        )
        self.add_setting("power_amplifier_power", power_amplifier_power_setting)

        gain_setting = FloatSetting(
            self.GAIN,
            self.HARDWARE,
            6000,
            "The amplification factor of the receiver chain, impacting the final measured signal amplitude.",
            min_value=0.1,
        )
        self.add_setting("gain", gain_setting)

        temperature_setting = FloatSetting(
            self.TEMPERATURE,
            self.EXPERIMENTAL_Setup,
            300,
            "The absolute temperature during the experiment. This influences the SNR of the measurement.",
            min_value=0.1,
            max_value=400,
            slider=True,
        )
        self.add_setting("temperature", temperature_setting)

        loss_tx_setting = FloatSetting(
            self.LOSS_TX,
            self.EXPERIMENTAL_Setup,
            25,
            "The signal loss occurring in the transmission path, affecting the effective RF pulse power.",
            min_value=0.1,
            max_value=60,
            slider=True,
        )
        self.add_setting("loss_tx", loss_tx_setting)

        loss_rx_setting = FloatSetting(
            self.LOSS_RX,
            self.EXPERIMENTAL_Setup,
            25,
            "The signal loss in the reception path, which can reduce the signal that is ultimately detected.",
            min_value=0.1,
            max_value=60,
            slider=True,
        )
        self.add_setting("loss_rx", loss_rx_setting)

        conversion_factor_setting = FloatSetting(
            self.CONVERSION_FACTOR,
            self.EXPERIMENTAL_Setup,
            2884,
            "Conversion factor  (spectrometer units / V)",
        )
        self.add_setting(
            "conversion_factor", conversion_factor_setting
        )  # Conversion factor for the LimeSDR based spectrometer

        # Sample settings
        sample_name_setting = StringSetting(
            self.SAMPLE_NAME,
            self.SAMPLE,
            "BiPh3",
            "The name of the sample.",
        )
        self.add_setting("sample_name", sample_name_setting)

        sample_n_atoms_setting = IntSetting(
            self.NUMBER_ATOMS,
            self.SAMPLE,
            0,
            "The number of atoms per unit volume of the sample (1/m^3). If this value is zero the molar mass and density will be used for calculation of the atoms per unit volume. If this value is not zero the molar mass and density",
            min_value=0,
            scientific_notation=True,
        )
        self.add_setting("n_atoms", sample_n_atoms_setting)

        density_setting = FloatSetting(
            self.DENSITY,
            self.SAMPLE,
            1.585e6,
            "The density of the sample. This is used to calculate the number of spins in the sample volume.",
            min_value=0.1,
        )
        self.add_setting("density", density_setting)

        molar_mass_setting = FloatSetting(
            self.MOLAR_MASS,
            self.SAMPLE,
            440.3,
            "The molar mass of the sample. This is used to calculate the number of spins in the sample volume.",
            min_value=0.1,
        )
        self.add_setting("molar_mass", molar_mass_setting)

        resonant_frequency_setting = FloatSetting(
            self.RESONANT_FREQUENCY,
            self.SAMPLE,
            83.56,
            "The resonant frequency of the observed transition.",
            min_value=1,
            suffix="MHz",
        )
        self.add_setting("resonant_frequency", resonant_frequency_setting)

        gamma_setting = FloatSetting(
            self.GAMMA,
            self.SAMPLE,
            43.42,
            "The gyromagnetic ratio of the sample’s nuclei.",
            min_value=0.001,
            suffix="MHz/T",
        )
        self.add_setting("gamma", gamma_setting)

        spin_options = ["3/2", "5/2", "7/2", "9/2"]
        nuclear_spin_setting = SelectionSetting(
            self.NUCLEAR_SPIN,
            self.SAMPLE,
            spin_options,
            default="9/2",
            description="The nuclear spin of the sample’s nuclei.",
        )
        self.add_setting("nuclear_spin", nuclear_spin_setting)

        spin_factor_setting = FloatSetting(
            self.SPIN_FACTOR,
            self.SAMPLE,
            2,
            "The spin factor represents the scaling coefficient for observable nuclear spin transitions along the x-axis, derived from the Pauli I x 0 -matrix elements.",
            min_value=0,
        )
        self.add_setting("spin_factor", spin_factor_setting)

        powder_factor_setting = FloatSetting(
            self.POWDER_FACTOR,
            self.SAMPLE,
            0.75,
            "A factor representing the crystallinity of the solid sample. A value of 0.75 corresponds to a powder sample.",
            min_value=0,
            max_value=1,
        )
        self.add_setting("powder_factor", powder_factor_setting)

        filling_factor_setting = FloatSetting(
            self.FILLING_FACTOR,
            self.SAMPLE,
            0.7,
            "The ratio of the sample volume that occupies the coil’s sensitive volume.",
            min_value=0,
            max_value=1,
        )
        self.add_setting("filling_factor", filling_factor_setting)

        t1_setting = FloatSetting(
            self.T1,
            self.SAMPLE,
            83,
            "The longitudinal or spin-lattice relaxation time of the sample, influencing signal recovery between pulses.",
            min_value=1,
            suffix="µs",
        )
        self.add_setting("T1", t1_setting)

        t2_setting = FloatSetting(
            self.T2,
            self.SAMPLE,
            396,
            "The transverse or spin-spin relaxation time, determining the rate at which spins dephase and the signal decays in the xy plane",
            min_value=1,
            suffix="µs",
        )
        self.add_setting("T2", t2_setting)

        t2_star_setting = FloatSetting(
            self.T2_STAR,
            self.SAMPLE,
            50,
            "The effective transverse relaxation time, incorporating effects of EFG inhomogeneities and other dephasing factors.",
            min_value=1,
            suffix="µs",
        )
        self.add_setting("T2_star", t2_star_setting)

        self.averages = 1
        self.target_frequency = 100e6

    @property
    def averages(self):
        """The number of averages used for the simulation.

        More averages improve the signal-to-noise ratio of the simulated signal.
        """
        return self._averages

    @averages.setter
    def averages(self, value):
        self._averages = value

    @property
    def target_frequency(self):
        """The target frequency for the simulation.

        Doesn't do anything at the moment.
        """
        return self._target_frequency

    @target_frequency.setter
    def target_frequency(self, value):
        self._target_frequency = value
