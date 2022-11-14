import soundfile as sf
import rbj
from scipy import signal
import numpy as np

print("Reading sound file")
with sf.SoundFile('harp.wav', 'r') as f:
    data = f.read(f.frames)

# High pass filter 2 pole set in range 500-5kHz("Tuning") with damping control ("Damping")
# Gain control ("Drive")
# LPF and DC stop
# Full wave rectifier
# Slow rolloff LPF and DC stop
# Mix ratio (timbre mixing between even and odd)


# Cut-down effect:
# High pass filter, clipping

def dist_atan(x, a):
    # Divide by a to keep low levels the same
    # Divide by arctan(a) to keep high levels the same
    return np.atan(a * x) / a

def dist_simple(x, a):
    # Heeps high levels the same
    k = 2*a/(1-a)
    return (1+k)*x/(1+k*np.abs(x))

aural_transition_freq = 3850 # 700-7000
damping = 2

# Extract frequencies above transition band
data_hpf = signal.sosfilt(
    rbj.lowpass(aural_transition_freq, BW=damping, fs=f.samplerate),
    data
)
# Full wave rectify
data_new_harmonics = np.abs(data_hpf)

# HF rolloff
data_new_harmonics = signal.sosfilt(
    rbj.lowpass(2*aural_transition_freq, fs=f.samplerate, BW=2),
    data_new_harmonics
)

# Remove DC component
data_new_harmonics = signal.sosfilt(
    rbj.highpass(10, BW=2, fs=f.samplerate),
    data_new_harmonics
)
# Mix back into signal
new_data = data + 0.1 * (data_new_harmonics - data)

sf.write('test1.wav', new_data, f.samplerate)
