import numpy as np

"""
Implements filter types described in
Audio EQ Cookbook by Robert Bristow-Johnson
https://www.musicdsp.org/en/latest/Filters/197-rbj-audio-eq-cookbook.html

These are concise 2 pole filters that are highly efficient.
"""
def _precalc(f0, fs, Q, BW, S, dBgain):
    w0 = 2 * np.pi * f0 / fs
    sinw0 = np.sin(w0)
    cosw0 = np.cos(w0)
    alpha = None
    A = None
    if Q is not None:
        alpha = sinw0 / (2*Q)
    elif BW is not None:
        alpha = sinw0 * np.sinh(np.log(2)/2 * BW * w0 / sinw0)
    else:
        A = pow(10, dBgain / 40)
        alpha = sinw0 / 2 * np.sqrt((A+1/A)*(1/S-1)+2)
    return sinw0, cosw0, alpha, A

def lowpass(f0, fs, Q=None, BW=None, S=None, dBgain=None):
    _, cosw0, alpha, _ = _precalc(f0, fs, Q, BW, S, dBgain)
    sos = np.array([[
        (1 - cosw0) / 2, 1 - cosw0, (1 - cosw0) / 2,
        1 + alpha, -2 * cosw0, 1 - alpha
    ]])
    return sos / sos[:, 3]

def highpass(f0, fs, Q=None, BW=None, S=None, dBgain=None):
    _, cosw0, alpha, _ = _precalc(f0, fs, Q, BW, S, dBgain)
    sos = np.array([[
        (1 + cosw0) / 2, -1 - cosw0, (1 + cosw0) / 2,
        1 + alpha, -2 * cosw0, 1 - alpha
    ]])
    return sos / sos[:, 3]

def bandpass_const_skirt_gain(f0, fs, Q=None, BW=None, S=None, dBgain=None):
    sinw0, cosw0, alpha, _ = _precalc(f0, fs, Q, BW, S, dBgain)
    sos = np.array([[
        sinw0 / 2, 0, -sinw0 / 2,
        1 + alpha, -2 * cosw0, 1 - alpha
    ]])
    return sos / sos[:, 3]

def bandpass_unity_peak_gain(f0, fs, Q=None, BW=None, S=None, dBgain=None):
    _, cosw0, alpha, _ = _precalc(f0, fs, Q, BW, S, dBgain)
    sos = np.array([[
        alpha, 0, -alpha,
        1 + alpha, -2 * cosw0, 1 - alpha
    ]])
    return sos / sos[:, 3]

def notch(f0, fs, Q=None, BW=None, S=None, dBgain=None):
    _, cosw0, alpha, _ = _precalc(f0, fs, Q, BW, S, dBgain)
    sos = np.array([[
        1, -2 * cosw0, 1,
        1 + alpha, -2 * cosw0, 1 - alpha
    ]])
    return sos / sos[:, 3]

def allpass(f0, fs, Q=None, BW=None, S=None, dBgain=None):
    _, cosw0, alpha, _ = _precalc(f0, fs, Q, BW, S, dBgain)
    sos = np.array([[
        1 - alpha, -2 * cosw0, 1 + alpha,
        1 + alpha, -2 * cosw0, 1 - alpha
    ]])
    return sos / sos[:, 3]

def peaking_eq(f0, fs, Q=None, BW=None, S=None, dBgain=None):
    _, cosw0, alpha, A = _precalc(f0, fs, Q, BW, S, dBgain)
    sos = np.array([[
        1 + alpha * A, -2 * cosw0, 1 - alpha * A,
        1 + alpha / A, -2 * cosw0, 1 - alpha / A
    ]])
    return sos / sos[:, 3]

def low_shelf(f0, fs, Q=None, BW=None, S=None, dBgain=None):
    _, cosw0, alpha, A = _precalc(f0, fs, Q, BW, S, dBgain)
    sos = np.array([[
        A * ((A + 1) - (A - 1) * cosw0 + 2 * np.sqrt(A) * alpha),
        2 * A * ((A - 1) - (A + 1) * cosw0),
        A * ((A + 1) - (A - 1) * cosw0 - 2 * np.sqrt(A) * alpha),
        (A + 1) + (A - 1) * cosw0 + 2 * np.sqrt(A) * alpha,
        -2 * ((A - 1) + (A + 1) * cosw0),
        (A + 1) + (A - 1) * cosw0 - 2 * np.sqrt(A) * alpha
    ]])
    return sos / sos[:, 3]

def high_shelf(f0, fs, Q=None, BW=None, S=None, dBgain=None):
    _, cosw0, alpha, A = _precalc(f0, fs, Q, BW, S, dBgain)
    sos = np.array([[
        A * ((A + 1) + (A - 1) * cosw0 + 2 * np.sqrt(A) * alpha),
        -2 * A * ((A - 1) + (A + 1) * cosw0),
        A * ((A + 1) + (A - 1) * cosw0 - 2 * np.sqrt(A) * alpha),
        (A + 1) - (A - 1) * cosw0 + 2 * np.sqrt(A) * alpha,
        2 * ((A - 1) - (A + 1) * cosw0),
        (A + 1) - (A - 1) * cosw0 - 2 * np.sqrt(A) * alpha
    ]])
    return sos / sos[:, 3]