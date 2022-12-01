import numpy as np
import soundfile as sf

def fof(fc, β, a, fs, length, φ=0):
    """
    FOF grain generator
    See https://ccrma.stanford.edu/~serafin/320/lab3/Fundamentals_FOFs.html

    fc = formant frequency
    π/β = width of skirt in seconds so β = pi / width of skirt 
    a = decay time in seconds
    fs = sample rate
    length = length of grain in seconds
    φ = initial phase in radians
    """
    w = fc * 2 * np.pi # Phase increment per sample
    t = np.arange(length) / fs # Sample time
    attack_threshold = int(fs * np.pi / β) # Sample number at which decay starts
    ta = t[:attack_threshold]
    #attack_section = 0.5 * (1 - np.cos(β*na/fs)) * np.exp(-a * na/fs) * np.sin(wc * na + φ)
    #attack_section = np.exp(-a * na) * np.sin(wc * na + φ)
    attack_section = np.sin(w * ta + φ)
    tb = t[attack_threshold:]
    #decay_section = np.exp(-a * nb) * np.sin(wc * nb + φ)
    decay_section = np.sin(w * tb + φ)
    return np.concatenate([attack_section, decay_section])


def fof2(fc, attack, bw, phi, amp, fs):
    # fc centre frequency
    # attack attack time in samples
    # phi phase in radians
    # bw bandwidth in samples
    # amp amplitude of formant
    # fs sample rate
    omega = 2 * np.pi * fc
    beta = np.pi / attack
    alpha = np.pi * bw
    formant_length = -np.log(0.001)/alpha # Decay to T60?
    Ts = 1 / fs
    n = np.arange(0, Ts, formant_length)
    n_attack = n[:int(np.ceil(np.pi / beta / Ts))]
    n_rest = n[int(np.ceil(np.pi / beta / Ts)):]
    s_attack = amp * 0.5 * (1-np.cos(beta*n_attack))*np.exp(-alpha * n_attack) * np.sin(omega * n_attack + phi)
    s_rest = amp * np.exp(-alpha * n_rest) * np.sin(omega * n_rest + phi)
    return np.concatenate([s_attack, s_rest])

formants = {
    "bass a": [(600, 0, 60), (1040, -7, 70), (2250, -9, 110), (2450, -9, 120), (2750, -20, 130)],
    "bass e": [(400, 0, 40), (1620, -12, 80), (2400, -9, 100), (2800, -12, 120), (3100, -18, 120)], 
    "bass i": [(250, 0, 60), (1750, -30, 90), (2600, -16, 100), (3050, -16, 120), (3340, -28, 120)], 
    "bass o": [(400, 0, 40), (750, -11, 80), (2400, -21, 100), (2600, -20, 120), (2900, -40, 120)],
    "bass u": [(350, 0, 40), (600, -20, 80), (2400, -32, 100), (2675, -28, 120), (2950, -36, 120)],
}

fs = 44100
lowest_pitch = 80 # Hz
grain_samples = int(fs / lowest_pitch)
out_array = np.array([0.])
for k, v in formants.items():
    print(k)
    data = np.zeros(grain_samples)
    for formant in v:
        print(formant)
        data += np.power(10, formant[1]/20) * fof(
            fc=formant[0], # fc
            β=np.pi * lowest_pitch, # pi/β = time between lowest pitch cycles
            a=1/(np.pi * formant[2]), # a = delay time = 1/(pi*BW)
            fs=fs,
            length=grain_samples,
            φ=0
        )
    #data *= 0.5
    out_array = np.concatenate([out_array, np.repeat(data, lowest_pitch)])

sf.write('vox_test_fof.wav', out_array, fs)
