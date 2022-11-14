import soundfile as sf
import rbj
from scipy import signal
import numpy as np

print("Reading sound file")
with sf.SoundFile('harp.wav', 'r') as f:
    data = f.read(f.frames)

def compressor(data, attack_rate=1e-3, decay_rate=1e-5, energy=.01):
    for i in range(data.size):
        d2 = data[i]
        d2 *= d2
        energy += (d2-energy) * (attack_rate if d2 > energy else decay_rate)
        data[i] *= 0.7 * np.power(energy, -0.5)
    return data

data = compressor(data)

sf.write('test1.wav', data, f.samplerate)
