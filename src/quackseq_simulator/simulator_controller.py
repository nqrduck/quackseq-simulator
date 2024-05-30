"""The controller module for the simulator spectrometer."""

import logging
from datetime import datetime
import numpy as np

from quackseq.spectrometer.spectrometer_controller import SpectrometerController
from quackseq.measurement import Measurement
from quackseq.pulseparameters import TXPulse, RXReadout
from quackseq.pulsesequence import QuackSequence

from nqr_blochsimulator.classes.pulse import PulseArray
from nqr_blochsimulator.classes.sample import Sample
from nqr_blochsimulator.classes.simulation import Simulation

logger = logging.getLogger(__name__)


class SimulatorController(SpectrometerController):
    """The controller class for the nqrduck simulator module."""

    def __init__(self, simulator):
        """Initializes the SimulatorController."""
        super().__init__()
        self.simulator = simulator

    def run_sequence(self, sequence: QuackSequence) -> None:
        """This method  is called when the start_measurement signal is received from the core.

        It will becalled if the simulator is the  active  spectrometer.
        This will start the simulation based on the settings and the pulse sequence.
        """
        logger.debug("Starting simulation")
        sample = self.get_sample_from_settings()
        logger.debug("Sample: %s", sample.name)

        dwell_time = self.calculate_dwelltime(sequence)
        logger.debug("Dwell time: %s", dwell_time)

        try:
            pulse_array = self.translate_pulse_sequence(sequence, dwell_time)
        except AttributeError:
            logger.warning("Could not translate pulse sequence")
            return

        simulation = self.get_simulation(sample, pulse_array)

        result = simulation.simulate()

        tdx = (
            np.linspace(
                0, float(self.calculate_simulation_length(sequence)), len(result)
            )
            * 1e6
        )

        rx_begin, rx_stop = self.translate_rx_event(sequence)
        # If we have a RX event, we need to cut the result to the RX event
        if rx_begin and rx_stop:
            evidx = np.where((tdx > rx_begin) & (tdx < rx_stop))[0]
            tdx = tdx[evidx]
            result = result[evidx]

        # Measurement name date + module + target frequency + averages + sequence name
        name = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Simulator - {self.simulator.model.target_frequency / 1e6} MHz - {self.simulator.model.averages} averages - {sequence.name}"
        logger.debug(f"Measurement name: {name}")

        measurement_data = Measurement(
            name,
            tdx,
            result / simulation.averages,
            sample.resonant_frequency,
            # frequency_shift=self.module.model.if_frequency,
        )

        return measurement_data

    def get_sample_from_settings(self) -> Sample:
        """This method creates a sample object based on the settings in the model.

        Returns:
            Sample: The sample object created from the settings.
        """
        model = self.simulator.model
        atom_density = None
        sample_volume = None
        sample_length = None
        sample_diameter = None

        name = model.settings.sample_name
        density = model.settings.density
        molar_mass = model.settings.molar_mass
        resonant_frequency = model.settings.resonant_frequency
        gamma = model.settings.gamma
        nuclear_spin = model.settings.nuclear_spin
        spin_factor = model.settings.spin_factor
        powder_factor = model.settings.powder_factor
        filling_factor = model.settings.filling_factor
        T1 = model.settings.T1
        T2 = model.settings.T2
        T2_star = model.settings.T2_star

        sample = Sample(
            name=name,
            density=density,
            molar_mass=molar_mass,
            resonant_frequency=resonant_frequency,
            gamma=gamma,
            nuclear_spin=nuclear_spin,
            spin_factor=spin_factor,
            powder_factor=powder_factor,
            filling_factor=filling_factor,
            T1=T1,
            T2=T2,
            T2_star=T2_star,
            atom_density=atom_density,
            sample_volume=sample_volume,
            sample_length=sample_length,
            sample_diameter=sample_diameter,
        )
        return sample

    def translate_pulse_sequence(
        self, sequence: QuackSequence, dwell_time: float
    ) -> PulseArray:
        """This method translates the pulse sequence from the core to a PulseArray object needed for the simulation.

        Args:
            sequence (QuackSequence): The pulse sequence from the core.
            dwell_time (float): The dwell time in seconds.

        Returns:
            PulseArray: The pulse sequence translated to a PulseArray object.
        """
        events = sequence.events

        amplitude_array = list()
        for event in events:
            logger.debug("Event %s has parameters: %s", event.name, event.parameters)
            for parameter in event.parameters.values():
                logger.debug(
                    "Parameter %s has options: %s", parameter.name, parameter.options
                )

                if (
                    parameter.name == sequence.TX_PULSE
                    and parameter.get_option_by_name(TXPulse.RELATIVE_AMPLITUDE).value
                    > 0
                ):
                    logger.debug(f"Adding pulse: {event.duration} s")
                    # If we have a pulse, we need to add it to the pulse array
                    pulse_shape = parameter.get_option_by_name(
                        TXPulse.TX_PULSE_SHAPE
                    ).value
                    pulse_amplitude = abs(
                        pulse_shape.get_pulse_amplitude(
                            event.duration, resolution=dwell_time
                        )
                    )

                    amplitude_array.append(pulse_amplitude)
                elif (
                    parameter.name == sequence.TX_PULSE
                    and parameter.get_option_by_name(TXPulse.RELATIVE_AMPLITUDE).value
                    == 0
                ):
                    # If we have a wait, we need to add it to the pulse array
                    amplitude_array.append(np.zeros(int(event.duration / dwell_time)))

        amplitude_array = np.concatenate(amplitude_array)

        # This has not yet been implemented right now the phase is always 0
        phase_array = np.zeros(len(amplitude_array))

        pulse_array = PulseArray(
            pulseamplitude=amplitude_array,
            pulsephase=phase_array,
            dwell_time=float(dwell_time),
        )

        return pulse_array

    def get_simulation(self, sample: Sample, pulse_array: PulseArray) -> Simulation:
        """This method creates a simulation object based on the settings and the pulse sequence.

        Args:
            sample (Sample): The sample object created from the settings.
            pulse_array (PulseArray): The pulse sequence translated to a PulseArray object.

        Returns:
            Simulation: The simulation object created from the settings and the pulse sequence.
        """
        model = self.simulator.model

        # noise = float(model.get_setting_by_name(model.NOISE).value)
        simulation = Simulation(
            sample=sample,
            pulse=pulse_array,
            number_isochromats=int(model.settings.number_isochromats),
            initial_magnetization=float(model.settings.initial_magnetization),
            gradient=float(model.settings.gradient),
            noise=float(model.settings.noise),
            length_coil=float(model.settings.length_coil),
            diameter_coil=float(model.settings.diameter_coil),
            number_turns=float(model.settings.number_turns),
            q_factor_transmit=float(model.settings.q_factor_transmit),
            q_factor_receive=float(model.settings.q_factor_receive),
            power_amplifier_power=float(model.settings.power_amplifier_power),
            gain=float(model.settings.gain),
            temperature=float(model.settings.temperature),
            averages=int(model.averages),
            loss_TX=float(model.settings.loss_tx),
            loss_RX=float(model.settings.loss_rx),
            conversion_factor=float(model.settings.conversion_factor),
        )
        return simulation

    def calculate_dwelltime(self, sequence: QuackSequence) -> float:
        """This method calculates the dwell time based on the settings and the pulse sequence.

        Returns:
            float: The dwell time in seconds.
        """
        n_points = int(
            self.simulator.model.get_setting_by_display_name(
                self.simulator.model.NUMBER_POINTS
            ).value
        )
        simulation_length = self.calculate_simulation_length(sequence)
        dwell_time = simulation_length / n_points
        return dwell_time