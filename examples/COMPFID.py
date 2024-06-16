"""Composite FID example.

This example demonstrates how to simulate a composite FID signal using the quackseq simulator.

See the paper: 
Sauer, K.L., Klug, C.A., Miller, J.B. et al. Using quaternions to design composite pulses for spin-1 NQR. Appl. Magn. Reson. 25, 485–500 (2004). https://doi.org/10.1007/BF03166543

This also works for Samples with spin > 1.
"""

import logging

from quackseq_simulator.simulator import Simulator
from quackseq.pulsesequence import QuackSequence
from quackseq.functions import RectFunction
from matplotlib import pyplot as plt

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger(__name__)

    seq = QuackSequence("COMPFID")
    seq.add_pulse_event("tx1", "3u", 100, 0, RectFunction())
    seq.add_pulse_event("tx2", "6u", 100, 45, RectFunction())
    # This makes the phase 45, 135, 225, 315
    seq.set_tx_n_phase_cycles("tx2", 4)
    seq.add_blank_event("blank", "5u")
    
    seq.add_readout_event("rx", "100u")

    # No phase shifiting of the receive data but weighting of -1 for the 45 degree pulse, +1 for the 135 degree pulse, -1 for the 225 degree pulse and +1 for the 315 degree pulse
    readout_scheme = [[1, 0], [-1, 0], [1, 0], [-1, 0]]

    sim = Simulator()
    sim.set_averages(100)

    sim.settings.noise = 1 # microvolts

    result = sim.run_sequence(seq)
    # Plot time and frequency domain next to each other
    plt.subplot(1, 2, 1)
    plt.title("Time domain Simulation of BiPh3 COMPFID")
    plt.xlabel("Time (µs)")
    plt.ylabel("Signal (a.u.)")
    plt.plot(result.tdx[-1], result.tdy[-1].imag, label="imaginary")
    plt.plot(result.tdx[-1], result.tdy[-1].real, label="real")
    plt.plot(result.tdx[-1], abs(result.tdy[-1]), label="abs")

    plt.subplot(1, 2, 2)
    plt.title("Frequency domain Simulation of BiPh3 COMPFID")
    plt.xlabel("Frequency (kHz)")
    plt.ylabel("Signal (a.u.)")
    plt.plot(result.fdx[-1], result.fdy[-1].imag, label="imaginary")
    plt.plot(result.fdx[-1], result.fdy[-1].real, label="real")
    plt.plot(result.fdx[-1], abs(result.fdy[-1]), label="abs")

    plt.legend()
    plt.show()