"""Example Free Induction Decay (FID) simulation using the quackseq simulator.

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

    seq = QuackSequence("FID")
    seq.add_pulse_event("tx", "3u", 100, 0, RectFunction())
    seq.add_blank_event("blank", "5u")
    seq.add_readout_event("rx", "100u")
    seq.add_blank_event("TR", "1m")

    sim = Simulator()
    sim.set_averages(100)

    sim.settings.noise = 1 # microvolts

    result = sim.run_sequence(seq)
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
