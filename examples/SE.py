"""Example Spin Echo (SE) simulation using the quackseq simulator.

The sample is the default BiPh3 NQR sample.
"""

import logging

from quackseq.sequences.SE import create_SE
from quackseq_simulator.simulator import Simulator
from matplotlib import pyplot as plt

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger(__name__)

    sim = Simulator()
    sim.set_averages(100)

    sim.settings.noise = 1 # microvolts

    SE = create_SE()

    result = sim.run_sequence(SE)
    # Plot time and frequency domain next to each other
    plt.subplot(1, 2, 1)
    plt.title("Time domain Simulation of BiPh3 SE")
    plt.xlabel("Time (µs)")
    plt.ylabel("Signal (a.u.)")
    plt.plot(result.tdx, result.tdy[:, 0].imag, label="imaginary")
    plt.plot(result.tdx, result.tdy[:, 0].real, label="real")
    plt.plot(result.tdx, abs(result.tdy[:, 0]), label="abs")

    plt.subplot(1, 2, 2)
    plt.title("Frequency domain Simulation of BiPh3 SE")
    plt.xlabel("Frequency (kHz)")
    plt.ylabel("Signal (a.u.)")
    plt.plot(result.fdx, result.fdy[:, 0].imag, label="imaginary")
    plt.plot(result.fdx, result.fdy[:, 0].real, label="real")
    plt.plot(result.fdx, abs(result.fdy[:, 0]), label="abs")

    plt.legend()
    plt.show()