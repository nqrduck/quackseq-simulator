"""Composite FID example.

This example demonstrates how to simulate a composite FID signal using the quackseq simulator.

See the paper: 
Sauer, K.L., Klug, C.A., Miller, J.B. et al. Using quaternions to design composite pulses for spin-1 NQR. Appl. Magn. Reson. 25, 485–500 (2004). https://doi.org/10.1007/BF03166543

This also works for Samples with spin > 1.
"""

import logging

from quackseq.sequences.COMPFID import create_COMPFID
from quackseq_simulator.simulator import Simulator
from matplotlib import pyplot as plt

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger(__name__)

    sim = Simulator()
    sim.set_averages(100)

    sim.settings.noise = 1  # microvolts

    COMPFID = create_COMPFID()

    result = sim.run_sequence(COMPFID)
    # Plot time and frequency domain next to each other
    plt.subplot(1, 2, 1)
    plt.title("Time domain Simulation of BiPh3 COMPFID")
    plt.xlabel("Time (µs)")
    plt.ylabel("Signal (a.u.)")
    plt.plot(result.tdx, result.tdy[:, -1].imag, label="imaginary")
    plt.plot(result.tdx, result.tdy[:, -1].real, label="real")
    plt.plot(result.tdx, abs(result.tdy[:, -1]), label="abs")

    plt.subplot(1, 2, 2)
    plt.title("Frequency domain Simulation of BiPh3 COMPFID")
    plt.xlabel("Frequency (kHz)")
    plt.ylabel("Signal (a.u.)")
    plt.plot(result.fdx, result.fdy[:, -1].imag, label="imaginary")
    plt.plot(result.fdx, result.fdy[:, -1].real, label="real")
    plt.plot(result.fdx, abs(result.fdy[:, -1]), label="abs")

    plt.legend()
    plt.show()
