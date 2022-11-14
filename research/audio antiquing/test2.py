import soundfile as sf
import numpy as np
import scipy.signal as signal

data, samplerate = sf.read('harp.wav')

# Uniform noise in range 0-1
noise = np.random.random(data.size)

# Slight filtering
k = 0.1
noise += k * (np.roll(noise, 1) - noise)

# Bias heavily towards 0 
noise = np.power(noise, 80)

# Mix in signal
k = -8 # dB of noise
data += pow(10, k/20) * (noise-data)

# DC blocker
sos = signal.butter(2, 200, 'hp', fs=samplerate, output='sos')
data = signal.sosfilt(sos, data)

# Lowpass filter
# Using a Chebyshev type 1 to give some deliberate passband ripple
#sos = signal.butter(4, 4000, 'lp', fs=samplerate, output='sos')
#sos = signal.butter(6, 4000, 'lp', fs=samplerate, output='sos')
sos = signal.cheby1(6, 10, 4000, 'lp', fs=samplerate, output='sos')
data = signal.sosfilt(sos, data)

# Loud noise distortion
bloud = 5
data = np.tanh(data * bloud) / np.tanh(bloud)

# Soft noise distortion
bsoft = 1.5
#data = np.copysign(np.power(np.absolute(data), bsoft), data)
data *= np.sqrt(np.absolute(data))

# Amplify
data_min = min(data)
data_max = max(data)
#data = (data - data_min) / (data_max - data_min)

sf.write('test1.wav', data, samplerate)