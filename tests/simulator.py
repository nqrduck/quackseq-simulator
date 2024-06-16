import unittest
import logging
import matplotlib.pyplot as plt
from quackseq.phase_table import PhaseTable
from quackseq.pulsesequence import QuackSequence
from quackseq.event import Event
from quackseq.functions import RectFunction
from quackseq_simulator.simulator import Simulator

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class TestQuackSequence(unittest.TestCase):

    def test_event_creation(self):
        seq = QuackSequence("test - event creation")
        seq.add_pulse_event("tx", "10u", 100, 90.0, RectFunction())
        seq.add_blank_event("blank", "3u")
        seq.add_readout_event("rx", "100u")
        seq.add_blank_event("TR", "1m")

        sim = Simulator()
        sim.set_averages(100)

        sim.settings.noise = 0

        result = sim.run_sequence(seq)
        self.assertIsNotNone(result)
        self.assertTrue(hasattr(result, "tdx"))
        self.assertTrue(hasattr(result, "tdy"))
        self.assertGreater(len(result.tdx[0]), 0)
        self.assertGreater(len(result.tdy[0]), 0)

        logger.info("Plotting imaginary part")
        plt.plot(result.tdx[0], result.tdy[0].imag, label="imaginary")
        logger.info("Plotting real part")
        plt.plot(result.tdx[0], result.tdy[0].real, label="real")
        plt.plot(result.tdx[0], abs(result.tdy[0]), label="abs")
        plt.legend()
        plt.show()

    def test_simulation_run_sequence(self):
        seq = QuackSequence("test - simulation run sequence")

        tx = Event("tx", "10u", seq)
        seq.add_event(tx)
        seq.set_tx_amplitude(tx, 100)
        seq.set_tx_phase(tx, 0)

        rect = RectFunction()
        seq.set_tx_shape(tx, rect)

        blank = Event("blank", "3u", seq)
        seq.add_event(blank)

        rx = Event("rx", "100u", seq)
        seq.set_rx(rx, True)
        seq.add_event(rx)

        TR = Event("TR", "1m", seq)
        seq.add_event(TR)

        sim = Simulator()
        sim.set_averages(100)

        result = sim.run_sequence(seq)
        self.assertIsNotNone(result)
        self.assertTrue(hasattr(result, "tdx"))
        self.assertTrue(hasattr(result, "tdy"))
        self.assertGreater(len(result.tdx[0]), 0)
        self.assertGreater(len(result.tdy[0]), 0)

        plt.plot(result.tdx[0], abs(result.tdy[0]))
        plt.show()

    def test_phase_array_generation(self):
        seq = QuackSequence("test - phase array generation")

        tx = Event("tx", "10u", seq)
        seq.add_event(tx)
        seq.set_tx_amplitude(tx, 100)
        seq.set_tx_phase(tx, 0)
        seq.set_tx_n_phase_cycles(tx, 2)
        seq.set_tx_phase_cycle_group(tx, 0)

        rect = RectFunction()
        seq.set_tx_shape(tx, rect)

        tx2 = Event("tx2", "10u", seq)
        seq.add_event(tx2)
        seq.set_tx_amplitude(tx2, 100)
        seq.set_tx_phase(tx2, 1)
        seq.set_tx_n_phase_cycles(tx2, 2)
        seq.set_tx_phase_cycle_group(tx2, 1)

        tx3 = Event("tx3", "10u", seq)
        seq.add_event(tx3)
        seq.set_tx_amplitude(tx3, 100)
        seq.set_tx_phase(tx3, 2)
        seq.set_tx_n_phase_cycles(tx3, 2)
        seq.set_tx_phase_cycle_group(tx3, 3)

        sim = Simulator()
        sim.set_averages(100)

        result = sim.run_sequence(seq)

        plt.plot(result.tdx[0], abs(result.tdy[0]))
        plt.plot(result.tdx[1], abs(result.tdy[1]))
        plt.show()

        phase_table = PhaseTable(seq)

        logger.info(phase_table.n_phase_cycles)
        self.assertEqual(phase_table.n_phase_cycles, 8)
        self.assertEqual(phase_table.n_parameters, 3)

    def test_phase_cycling(self):

        seq = QuackSequence("test - phase cycling")

        # Simple spin echo sequence with phase cycling.
        # Create the first 90 degree pulse
        pi_half = Event("pi_half", "6u", seq)
        seq.add_event(pi_half)
        seq.set_tx_amplitude(pi_half, 100)
        seq.set_tx_phase(pi_half, 0)
        seq.set_tx_n_phase_cycles(pi_half, 4)  # 0 90 180 270
        seq.set_tx_phase_cycle_group(pi_half, 0)

        # Wait for TE/2 (approx)
        seq.add_blank_event("te/2", "150u")

        # Create the 180 degree pulse
        pi = Event("pi", "12u", seq)
        seq.add_event(pi)
        seq.set_tx_amplitude(pi, 100)
        seq.set_tx_phase(pi, 90)
        seq.set_tx_n_phase_cycles(pi, 1)
        seq.set_tx_phase_cycle_group(pi, 0)

        # Wait another blanking time
        seq.add_blank_event("blank", "100u")

        result = Simulator().run_sequence(seq)

        # Plotting the results
        plt.title("Phase cycling")
        logger.info(f"Number of data sets {len(result.tdy)}")
        plt.plot(result.tdx[0], result.tdy[0].real, label="pc 1")
        plt.plot(result.tdx[1], result.tdy[1].real, label="pc 2")
        plt.plot(result.tdx[2], result.tdy[2].real, label="pc 3")
        plt.plot(result.tdx[3], result.tdy[3].real, label="pc 4")
        plt.legend()
        plt.show()

        rx = Event("rx", "100u", seq)
        seq.add_event(rx)
        seq.set_rx(rx, True)

        # Readout scheme for phase cycling TX pulses have the scheme 0 90 180 270 for the first pulse and 180 always for the second pulse
        readout_scheme = [[1, 0], [1, 90], [1, 180], [1, 270]]

        seq.set_rx_readout_scheme(rx, readout_scheme)

        result = Simulator().run_sequence(seq)

        # Plotting the results
        plt.title("Phase cycling")
        logger.info(f"Number of data sets {len(result.tdy)}")
        plt.plot(result.tdx[0], result.tdy[0].real, label="pc 1 real")
        plt.plot(result.tdx[0], result.tdy[0].imag, label="pc 2 imag")
        plt.legend()
        plt.show()
        plt.plot(result.tdx[1], result.tdy[1].real, label="pc 2")
        plt.plot(result.tdx[1], result.tdy[1].imag, label="pc 2")
        plt.legend()
        plt.show()
        plt.plot(result.tdx[2], result.tdy[2].real, label="pc 3")
        plt.plot(result.tdx[2], result.tdy[2].imag, label="pc 3")
        plt.legend()
        plt.show()
        plt.plot(result.tdx[3], result.tdy[3].real, label="pc 4")
        plt.plot(result.tdx[3], result.tdy[3].imag, label="pc 4")
        plt.legend()
        plt.show()
        plt.plot(result.tdx[4], abs(result.tdy[4]), label="Phase Cycling")
        plt.legend()
        plt.show()
        # seq.add_event(rx)


if __name__ == "__main__":
    unittest.main()
