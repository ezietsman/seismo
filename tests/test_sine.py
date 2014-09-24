from seismo import fitting
import numpy as np


def test_fitting_init():
    sine = fitting.sinewave()
    assert(sine)


def test_evaluate_sine():
    s = fitting.sinewave(1, 1, 1, 1)
    correct = np.array([1.841470984807897, 1.99190379965505,
                        1.678213802860806, 1.04718003020117,
                        0.394070197062779, 0.024481652878359,
                        0.111348984990933, 0.614026003282171,
                        1.297304544260835, 1.841470984807895])
    assert(np.allclose(s.evaluate(np.linspace(0, 10, 10)), correct,
                       atol=1e-15))


def test_signal_eval():
    correct = np.array([0.838994692557355, 0.837327409972626,
                        -0.031207568389303, 1.657908483235176,
                        -0.360441537030637, 0.168059166213009,
                        0.160726869260051, -1.587990964413157,
                        0.181569295634131, -1.137612460021985])

    t = np.linspace(0, 0.25, 10)
    s1 = fitting.sinewave(1, 50, 0.5, 0.0)
    s2 = fitting.sinewave(0.75, 75, 0.5, 0.0)
    signal = fitting.signal()
    signal.add_component(s1)
    signal.add_component(s2)
    assert(np.allclose(signal.eval_components(t), correct, atol=1e-15))
