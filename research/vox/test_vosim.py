import numpy as np

# https://www.kaegi.nl/vosim/docs/JAES-1978.pdf
def vosim(T, N, b):
    # T is duration of raised cosine
    # N is number of cosines
    # b is decay rate
    n = np.arange(int(T*N))
    phase = 2 * np.pi * np.mod(n / T, 1)
    amplitude = np.power(b, np.floor(n))
    return amplitude * (1-np.cos(phase))

def freq_vosim(fc, fs, ttot, decay):
    return vosim(
        fs/fc, # Cosine is at fc pitch when played back at fs rate
        np.floor(ttot*fc/fs), # Stop before repetition interval
        
    )