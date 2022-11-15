import soundfile as sf
import rbj
from scipy import signal
import numpy as np
from tqdm import tqdm

print("Reading sound file")
with sf.SoundFile('harp.wav', 'r') as f:
    data = f.read(f.frames)

def compressor(data, attack_rate=1e-3, decay_rate=1e-5, threshold=0.1, ratio=2):
    energy = threshold
    print("Compressor")
    for i in tqdm(range(data.size)):
        d2 = data[i]
        d2 *= d2
        energy += (d2 - energy) * (attack_rate if d2 > energy else decay_rate)
        rms_level = np.sqrt(energy)
        if rms_level > threshold:
            # Trigger compressor
            data[i] *= threshold * np.power(rms_level/threshold, 1/ratio) / rms_level
    return data

def waveshaper(x, a):
    # Keeps high levels the same
    k = 2*a/(1-a)
    return (1+k)*x/(1+k*np.abs(x))

def svf(data, f0, fs, q):
    # Trapesium optimised state variable filter
    # https://cytomic.com/files/dsp/SvfLinearTrapOptimised2.pdf
    # Low and High pass responses have been modified so low + high has unity
    # response. This allows perfect reconstruction from filter bank. 
    g = np.tan(np.pi * f0 / fs)
    k = 1/q
    a1 = 1/(1+g*(g+k))
    a2 = g * a1
    a3 = g * a2
    ic1eq = 0
    ic2eq = 0
    out_low = np.zeros_like(data)
    #out_band = np.zeros_like(data)
    out_high = np.zeros_like(data)
    #out_notch = np.zeros_like(data)
    #out_peak = np.zeros_like(data)
    out_all = np.zeros_like(data)
    print("State variable filter")
    for i in tqdm(range(data.size)):
        v0 = data[i]
        v3 = v0 - ic2eq
        v1 = a1 * ic1eq + a2 * v3
        v2 = ic2eq + a2 * ic1eq + a3 * v3
        ic1eq = 2 * v1 - ic1eq
        ic2eq = 2 * v2 - ic2eq
        #out_low[i] = v2
        out_low[i] = v2 - 0.5 * k * v1
        #out_band[i] = v1
        #out_high[i] = v0 - k * v1 - v2
        out_high[i] = v0 - 1.5 * k * v1 - v2
        #out_notch[i] = v0 - k * v1
        #out_peak[i] = v0 - k * v1 - 2 * v2
        out_all[i] = v0 - 2 * k * v1
    return {
        'low': out_low,
        #'band': out_band,
        'high': out_high,
        #'notch': out_notch,
        #'peak': out_peak,
        'all': out_all,
    }

def svf_bandsplit(data, f0, fs, q):
    # Trapesium optimised state variable filter
    # https://cytomic.com/files/dsp/SvfLinearTrapOptimised2.pdf
    # Low and High pass responses have been modified so low + high has unity
    # response. This allows perfect reconstruction from filter bank. 
    g = np.tan(np.pi * f0 / fs)
    k = 1/q
    a1 = 1/(1+g*(g+k))
    a2 = g * a1
    a3 = g * a2
    ic1eq = 0
    ic2eq = 0
    out_low = np.zeros_like(data)
    out_high = np.zeros_like(data)
    print("State variable filter band split")
    for i in tqdm(range(data.size)):
        v0 = data[i]
        v3 = v0 - ic2eq
        v1 = a1 * ic1eq + a2 * v3
        v2 = ic2eq + a2 * ic1eq + a3 * v3
        ic1eq = 2 * v1 - ic1eq
        ic2eq = 2 * v2 - ic2eq
        out_low[i] = v2 - 0.5 * k * v1
        out_high[i] = v0 - 1.5 * k * v1 - v2
    return [out_low, out_high]

def svf_allpass(data, f0, fs, q):
    # Trapesium optimised state variable filter
    # https://cytomic.com/files/dsp/SvfLinearTrapOptimised2.pdf
    g = np.tan(np.pi * f0 / fs)
    k = 1/q
    a1 = 1/(1+g*(g+k))
    a2 = g * a1
    a3 = g * a2
    ic1eq = 0
    ic2eq = 0
    out_all = np.zeros_like(data)
    print("State variable filter all pass")
    for i in tqdm(range(data.size)):
        v0 = data[i]
        v3 = v0 - ic2eq
        v1 = a1 * ic1eq + a2 * v3
        v2 = ic2eq + a2 * ic1eq + a3 * v3
        ic1eq = 2 * v1 - ic1eq
        ic2eq = 2 * v2 - ic2eq
        out_all[i] = v0 - 2 * k * v1
    return out_all
    
def fourband(data, f, q, fs):
    data = svf_bandsplit(data, f[1], fs, q[1])
    return [
        *svf_bandsplit(
            svf_allpass(data[0], f[2], fs, q[2]),
            f[0], fs, q[0]
        ),
        *svf_bandsplit(
            svf_allpass(data[1], f[0], fs, q[0]),
            f[2], fs, q[2]
        )
    ]

def exciter(data, f, bw, fs, comp_a, comp_d, comp_t, comp_r, dist, gain):
    # Split into four frequency bands
    data_bands = fourband(data, f, bw, fs)
    data_out = np.zeros_like(data)
    for i in range(4):
        data_out += waveshaper(
            gain[i] * compressor(
                data_bands[i],
                comp_a[i],
                comp_d[i],
                comp_t[i],
                comp_r[i]
            ),
            dist[i]
        )
    return data_out


data_b, data_l, data_m, data_h = fourband(data, (150, 500, 2000), (2,2,2), fs=f.samplerate)
sf.write('test0.wav', data_b, f.samplerate)
sf.write('test1.wav', data_l, f.samplerate)
sf.write('test2.wav', data_m, f.samplerate)
sf.write('test3.wav', data_h, f.samplerate)
sf.write('testA.wav', data_b+data_l+data_m+data_h, f.samplerate)

data_excited = exciter(
    data,
    (250, 800, 2000), # Band split frequencies
    (1, 1, 1), # Bandwidth
    f.samplerate,
    (1e-2, 1e-2, 1e-2, 1e-3), # Attack rate
    (1e-5, 1e-5, 1e-5, 1e-5), # Decay rate
    (0.1, 0.1, 0.1, 0.1), # Compressor threshold
    (2, 1.5, 2, 2), # Compression ratio
    (0.1, 0., 0.2, 0.2), # Distortion
    (3, 3, 3, 2) # Band gain
)
sf.write('testE.wav', data_excited, f.samplerate)
