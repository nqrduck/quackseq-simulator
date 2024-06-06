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
        seq.add_readout_event("rx", "100u", phase=90.0)
        seq.add_blank_event("TR", "1m")

        sim = Simulator()
        sim.set_averages(100)

        sim.settings.noise = 0

        result = sim.run_sequence(seq)
        self.assertIsNotNone(result)
        self.assertTrue(hasattr(result, "tdx"))
        self.assertTrue(hasattr(result, "tdy"))
        self.assertGreater(len(result.tdx), 0)
        self.assertGreater(len(result.tdy), 0)

        # Plotting the result can be useful for visual inspection during development
        plt.plot(result.tdx, result.tdy.imag, label="imaginary")
        plt.plot(result.tdx, result.tdy.real, label="real")
        plt.plot(result.tdx, abs(result.tdy), label="abs")
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
        self.assertGreater(len(result.tdx), 0)
        self.assertGreater(len(result.tdy), 0)

        # Plotting the result can be useful for visual inspection during development
        plt.plot(result.tdx, abs(result.tdy))
        plt.show()

    def test_phase_cycling(self):
        seq = QuackSequence("test - phase cycling")

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
        seq.set_tx_n_phase_cycles(tx2, 4)
        seq.set_tx_phase_cycle_group(tx2, 1)

        tx3 = Event("tx3", "10u", seq)
        seq.add_event(tx3)
        seq.set_tx_amplitude(tx3, 100)
        seq.set_tx_phase(tx3, 2)
        seq.set_tx_n_phase_cycles(tx3, 3)
        seq.set_tx_phase_cycle_group(tx3, 1)

        sim = Simulator()
        sim.set_averages(100)

        result = sim.run_sequence(seq)

        plt.plot(result.tdx, abs(result.tdy))
        plt.show()

        phase_table = PhaseTable(seq)

if __name__ == "__main__":
    unittest.main()
