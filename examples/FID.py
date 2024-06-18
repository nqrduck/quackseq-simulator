"""Example Free Induction Decay (FID) simulation using the quackseq simulator.

The sample is the default BiPh3 NQR sample.
"""

import logging

from quackseq.sequences.FID import create_FID
from quackseq_simulator.simulator import Simulator
from matplotlib import pyplot as plt

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger(__name__)

    sim = Simulator()
    sim.set_averages(100)

    sim.settings.noise = 1  # microvolts

    FID = create_FID()

    # Run the imported FID sequence
    result = sim.run_sequence(FID)

    # Plot time and frequency domain next to each other
    plt.subplot(1, 2, 1)
    plt.title("Time domain Simulation of BiPh3 FID")
    plt.xlabel("Time (µs)")
    plt.ylabel("Signal (a.u.)")
    plt.plot(result.tdx[0], result.tdy[0].imag, label="imaginary")
    plt.plot(result.tdx[0], result.tdy[0].real, label="real")
    plt.plot(result.tdx[0], abs(result.tdy[0]), label="abs")

    plt.subplot(1, 2, 2)
    plt.title("Frequency domain Simulation of BiPh3 FID")
    plt.xlabel("Frequency (kHz)")
    plt.ylabel("Signal (a.u.)")
    plt.plot(result.fdx[0], result.fdy[0].imag, label="imaginary")
    plt.plot(result.fdx[0], result.fdy[0].real, label="real")
    plt.plot(result.fdx[0], abs(result.fdy[0]), label="abs")

    plt.legend()
    plt.show()
