"""Spin Echo with Phase Cycling (SEPC) simulation using the quackseq simulator.

The sample is the default BiPh3 NQR sample.
"""

import logging

from quackseq_simulator.simulator import Simulator
from quackseq.pulsesequence import QuackSequence
from quackseq.functions import RectFunction
from matplotlib import pyplot as plt

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger(__name__)

    seq = QuackSequence("SEPC")
    seq.add_pulse_event("pi-half", "3u", 100, 0, RectFunction())
    # This causes the phase to cycle through 0, 90, 180, 270
    seq.set_tx_n_phase_cycles("pi-half", 4)

    seq.add_blank_event("te-half", "150u")
    # For the second pulse we just need a phase of 180
    seq.add_pulse_event("pi", "6u", 100, 180, RectFunction())
    seq.add_blank_event("blank", "50u")

    seq.add_readout_event("rx", "200u")
    # Readout scheme for phase cycling TX pulses have the scheme 0 90 180 270 for the first pulse and 180 always for the second pulse
    readout_scheme = [[1, 0], [1, 90], [1, 180], [1, 270]]

    seq.set_rx_readout_scheme("rx", readout_scheme)

    sim = Simulator()
    sim.set_averages(100)

    sim.settings.noise = 1 # microvolts

    result = sim.run_sequence(seq)
    # Plot time and frequency domain next to each other
    plt.subplot(1, 2, 1)
    plt.title("Time domain Simulation of BiPh3 SEPC")
    plt.xlabel("Time (µs)")
    plt.ylabel("Signal (a.u.)")
    plt.plot(result.tdx[-1], result.tdy[-1].imag, label="imaginary")
    plt.plot(result.tdx[-1], result.tdy[-1].real, label="real")
    plt.plot(result.tdx[-1], abs(result.tdy[-1]), label="abs")

    plt.subplot(1, 2, 2)
    plt.title("Frequency domain Simulation of BiPh3 SEPC")
    plt.xlabel("Frequency (kHz)")
    plt.ylabel("Signal (a.u.)")
    plt.plot(result.fdx[-1], result.fdy[-1].imag, label="imaginary")
    plt.plot(result.fdx[-1], result.fdy[-1].real, label="real")
    plt.plot(result.fdx[-1], abs(result.fdy[-1]), label="abs")

    plt.legend()
    plt.show()