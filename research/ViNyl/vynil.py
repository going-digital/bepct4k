import soundfile as sf
from scipy import signal
import numpy as np

print("Reading sound file")
with sf.SoundFile('harp.wav', 'r') as f:
    data = f.read(f.frames)

def linear_map(x, in_range, out_range):
    # Bound x to in_range
    x = min(in_range[1], max(in_range[0], x))
    # Remap scale
    return (x-in_range[0])/(in_range[1]-in_range[0]) * (out_range[1]-out_range[0]) + out_range[0]

# Prepare
fs = f.samplerate
#rpm = 78; year = 1900; wear = 0.3; click = 0.2
rpm = 78; year = 1950; wear = 0.3; click = 0.2
#rpm = 45; year = 1980; wear = 0.3; click = 0.3
#rpm = 33; year = 2000; wear = 0.2; click = 0.2

# 1912: 78rpm standardised. Mechanical recording
# 1925: Electric recording. Flatter freq response 100-5000Hz
# 1931 33 LP in vinyl
# 1948 78 Switch from shellac to vinyl
# 1949 45 single
# 1958 78 stops production
# 1957 stereo


omega = 960/(rpm*fs) # Angular velocity of platter * 16
age = linear_map(year, (1900,1990), (1, 0.01))
click_prob = ((age * age)/10 + click * 0.02) / 16
noise_amp = (click + wear * 0.3) * 0.12 + linear_map(year, (1900, 1990), (0.2883, 0.01))
bandwidth = linear_map(year, (1900, 1990), (38, 209)) * rpm
noise_lpf = bandwidth*(0.25 - wear * 0.02) + click * 200 + 300
signal_lpf = bandwidth * (1.0 - wear * 0.86)
signal_hpf = linear_map(year, (1900,1990), (1100,80))
#wrap_gain = age * 3.1 + 0.05
#wrap_bias = age * 0.1
Bloud = linear_map(year, (1900, 1990), (5, 0.1))
Bsoft = linear_map(year, (1900, 1990), (2.5, 1))

def rbj_precalc(f0, fs, Q, BW, S, dBgain):
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

def rbj_lpf(f0, fs, Q=None, BW=None, S=None, dBgain=None):
    _, cosw0, alpha, _ = rbj_precalc(f0, fs, Q, BW, S, dBgain)
    sos = np.array([[
        (1 - cosw0) / 2, 1 - cosw0, (1 - cosw0) / 2,
        1 + alpha, -2 * cosw0, 1 - alpha
    ]])
    return sos / sos[:, 3]

def rbj_hpf(f0, fs, Q=None, BW=None, S=None, dBgain=None):
    _, cosw0, alpha, _ = rbj_precalc(f0, fs, Q, BW, S, dBgain)
    sos = np.array([[
        (1 + cosw0) / 2, -1 - cosw0, (1 + cosw0) / 2,
        1 + alpha, -2 * cosw0, 1 - alpha
    ]])
    return sos / sos[:, 3]

def rbj_bpf_const_skirt_gain(f0, fs, Q=None, BW=None, S=None, dBgain=None):
    sinw0, cosw0, alpha, _ = rbj_precalc(f0, fs, Q, BW, S, dBgain)
    sos = np.array([[
        sinw0 / 2, 0, -sinw0 / 2,
        1 + alpha, -2 * cosw0, 1 - alpha
    ]])
    return sos / sos[:, 3]

def rbj_bpf_unity_peak_gain(f0, fs, Q=None, BW=None, S=None, dBgain=None):
    _, cosw0, alpha, _ = rbj_precalc(f0, fs, Q, BW, S, dBgain)
    sos = np.array([[
        alpha, 0, -alpha,
        1 + alpha, -2 * cosw0, 1 - alpha
    ]])
    return sos / sos[:, 3]

def rbj_notch(f0, fs, Q=None, BW=None, S=None, dBgain=None):
    _, cosw0, alpha, _ = rbj_precalc(f0, fs, Q, BW, S, dBgain)
    sos = np.array([[
        1, -2 * cosw0, 1,
        1 + alpha, -2 * cosw0, 1 - alpha
    ]])
    return sos / sos[:, 3]

def rbj_apf(f0, fs, Q=None, BW=None, S=None, dBgain=None):
    _, cosw0, alpha, _ = rbj_precalc(f0, fs, Q, BW, S, dBgain)
    sos = np.array([[
        1 - alpha, -2 * cosw0, 1 + alpha,
        1 + alpha, -2 * cosw0, 1 - alpha
    ]])
    return sos / sos[:, 3]

def rbj_peaking_eq(f0, fs, Q=None, BW=None, S=None, dBgain=None):
    _, cosw0, alpha, A = rbj_precalc(f0, fs, Q, BW, S, dBgain)
    sos = np.array([[
        1 + alpha * A, -2 * cosw0, 1 - alpha * A,
        1 + alpha / A, -2 * cosw0, 1 - alpha / A
    ]])
    return sos / sos[:, 3]

def rbj_low_shelf(f0, fs, Q=None, BW=None, S=None, dBgain=None):
    _, cosw0, alpha, A = rbj_precalc(f0, fs, Q, BW, S, dBgain)
    sos = np.array([[
        A * ((A + 1) - (A - 1) * cosw0 + 2 * np.sqrt(A) * alpha),
        2 * A * ((A - 1) - (A + 1) * cosw0),
        A * ((A + 1) - (A - 1) * cosw0 - 2 * np.sqrt(A) * alpha),
        (A + 1) + (A - 1) * cosw0 + 2 * np.sqrt(A) * alpha,
        -2 * ((A - 1) + (A + 1) * cosw0),
        (A + 1) + (A - 1) * cosw0 - 2 * np.sqrt(A) * alpha
    ]])
    return sos / sos[:, 3]

def rbj_high_shelf(f0, fs, Q=None, BW=None, S=None, dBgain=None):
    _, cosw0, alpha, A = rbj_precalc(f0, fs, Q, BW, S, dBgain)
    sos = np.array([[
        A * ((A + 1) + (A - 1) * cosw0 + 2 * np.sqrt(A) * alpha),
        -2 * A * ((A - 1) + (A + 1) * cosw0),
        A * ((A + 1) + (A - 1) * cosw0 - 2 * np.sqrt(A) * alpha),
        (A + 1) - (A - 1) * cosw0 + 2 * np.sqrt(A) * alpha,
        2 * ((A - 1) - (A + 1) * cosw0),
        (A + 1) - (A - 1) * cosw0 - 2 * np.sqrt(A) * alpha
    ]])
    return sos / sos[:, 3]

# Wow and flutter placeholder

# Generate click track
print("Generating click track")
click_data = np.zeros(data.size)
click_events = np.random.rand(data.size) < click_prob
for i in zip(*np.where(click_events)):
    # Pick click pitch
    click_omega = (np.random.random() + 0.5) * rpm / 32
    # Pick click volume
    click_gain = noise_amp * 5 * np.random.random()
    # Apply click
    for j in range(int(i[0]), int(i[0]+click_omega)):
        t = (j - i[0])/click_omega
        click_data[j] += click_gain * pow(max(0,1-2*abs(t-0.5)), 8)

# Add clicks pre-lpf
print("Adding click track")
data += click_data


# Lowpass
print("Signal treble rolloff")
data = signal.sosfilt(
    rbj_lpf(signal_lpf, BW=2, fs=f.samplerate),
    data
)

# Välimäki waveshaper
print("Signal waveshaper")
data = np.tanh(data*Bloud) / np.tanh(Bloud) # Model high volume distortion
data = np.copysign(np.power(np.abs(data), Bsoft), data) # Model low volume backlash
# Waveshaper
#print("Signal waveshaper")
#data = age * (np.sin(data * wrap_gain + wrap_bias) - data)
#data = age * (np.arctan(data * wrap_gain + wrap_bias) - data)

# Add clicks post-lpf/waveshaper
print("Adding click track")
data += 0.5 * click_data

# Add noise
print("Add shaped noise")
data += signal.sosfilt(
    rbj_lpf(noise_lpf, BW=4 + wear * 2, fs=f.samplerate),
    noise_amp * np.random.rand(data.size)
)

# Highpass
print("Signal bass rolloff")
data = signal.sosfilt(
    rbj_hpf(signal_hpf, BW=1.5, fs=f.samplerate),
    data
)

sf.write('vynil_test.wav', data, f.samplerate)