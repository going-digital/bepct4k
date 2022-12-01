import soundfile as sf
from scipy import signal
import numpy as np
import random
import math

# Formant synthesiser

# Formant table




def synth(env_f, master_amp, env_ctrl, osc1_f, osc1_amp, osc2_f, osc2_amp, osc3_f, osc3_amp, osc4_f, osc4_amp, osc5_f, osc5_amp, dist, fs):
    print("F1={} F2={} F2/F1={}".format(osc1_f, osc2_f, osc2_f/osc1_f))
    env_phase = 0
    osc1_phase = 0
    osc2_phase = 0
    osc3_phase = 0
    osc4_phase = 0
    osc5_phase = 0

    data = np.zeros(fs)

    for i in range(int(fs)):
        dist_bias = (1 + dist * random.randrange(-1,1))
        new_env_phase = (env_phase + env_f / fs) % 1
        if (new_env_phase < env_phase) and env_ctrl >= 128:
            osc1_phase = 0
            osc2_phase = 0
            osc3_phase = 0
            osc4_phase = 0
            osc5_phase = 0
        env_phase = new_env_phase
        osc1_phase = (osc1_phase + osc1_f / fs) % 1
        osc2_phase = (osc2_phase + osc2_f / fs) % 1
        osc3_phase = (osc3_phase + osc3_f / fs) % (2 * np.pi)
        osc4_phase = (osc4_phase + osc4_f * dist_bias / fs) % (2 * np.pi)
        osc5_phase = (osc5_phase + osc5_f * dist_bias / fs) % (2 * np.pi)
        if env_ctrl & 3 == 0:
            # Ramp
            env_out = env_phase
        elif env_ctrl & 3 == 1:
            # Raised cosine
            env_out = 0.5 - 0.5 * math.cos(2 * np.pi * env_phase)
        elif env_ctrl & 3 == 2:
            env_out = 1 - 2 * abs(0.5 - env_phase)
        else:
            env_out = 0 if env_phase < 0.5 else 1
        mix1 = np.sin(2 * np.pi * osc1_phase) * osc1_amp
        mix1 += np.sin(2 * np.pi * osc2_phase) * osc2_amp
        mix1 += np.sin(2 * np.pi * osc3_phase) * osc3_amp
        mix2 = np.sin(2 * np.pi * osc4_phase) * osc4_amp
        mix2 += np.sin(2 * np.pi * osc5_phase) * osc5_amp
        if env_ctrl & 128:
            mix1 *= env_out
        if env_ctrl & 256:
            mix2 *= 0.5 + 0.5 * env_out
        out = master_amp * (mix1 + mix2)
        data[i] = out
    return data

fs = 44100
# https://www.classes.cs.uchicago.edu/archive/1999/spring/CS295/Computing_Resources/Csound/CsManual3.48b1.HTML/Appendices/table3.html

# Soprano C4-A5
fsoprano = 16.35*pow(2, 4)
datasa = synth(fsoprano, 0.1, 256+128+1, 800, pow(10, 0/20), 1150, pow(10, -6/20), 2900, pow(10, -32/20), 3900, pow(10, -20/20), 4500, pow(10, -50/20), 0., fs)
datase = synth(fsoprano, 0.1, 256+128+1, 350, pow(10, 0/20), 2000, pow(10, -20/20), 2800, pow(10, -15/20), 3600, pow(10, -40/20), 4950, pow(10, -56/20), 0., fs)
datasi = synth(fsoprano, 0.1, 256+128+1, 270, pow(10, 0/20), 2140, pow(10, -12/20), 2950, pow(10, -26/20), 3900, pow(10, -26/20), 4950, pow(10, -44/20), 0., fs)
dataso = synth(fsoprano, 0.1, 256+128+1, 450, pow(10, 0/20), 800, pow(10, -11/20), 2830, pow(10, -22/20), 3800, pow(10, -22/20), 4950, pow(10, -50/20), 0., fs)
datasu = synth(fsoprano, 0.1, 256+128+1, 325, pow(10, 0/20), 700, pow(10, -16/20), 2700, pow(10, -35/20), 3800, pow(10, -40/20), 4950, pow(10, -60/20), 0., fs)

# Alto F3-D5
falto = 16.35*pow(2, 4)
dataaa = synth(falto, 0.1, 256+128+1, 800, pow(10, 0/20), 1150, pow(10, -4/20), 2800, pow(10, -20/20), 3500, pow(10, -36/20), 4950, pow(10, -60/20), 0., fs)
dataae = synth(falto, 0.1, 256+128+1, 400, pow(10, 0/20), 1600, pow(10, -24/20), 2700, pow(10, -30/20), 3300, pow(10, -35/20), 4950, pow(10, -60/20), 0., fs)
dataai = synth(falto, 0.1, 256+128+1, 350, pow(10, 0/20), 1700, pow(10, -20/20), 2700, pow(10, -30/20), 3700, pow(10, -36/20), 4950, pow(10, -60/20), 0., fs)
dataao = synth(falto, 0.1, 256+128+1, 450, pow(10, 0/20), 800, pow(10, -9/20), 2700, pow(10, -16/20), 3500, pow(10, -28/20), 4950, pow(10, -55/20), 0., fs)
dataau = synth(falto, 0.1, 256+128+1, 325, pow(10, 0/20), 700, pow(10, -12/20), 2830, pow(10, -30/20), 3500, pow(10, -40/20), 4950, pow(10, -64/20), 0., fs)

# Tenor B2-G4
ftenor = 16.35*pow(2, 4)
datata = synth(ftenor, 0.1, 256+128+1, 600, pow(10, 0/20), 1080, pow(10, -6/20), 2650, pow(10, -7/20), 2900, pow(10, -8/20), 3250, pow(10, -22/20), 0., fs)
datate = synth(ftenor, 0.1, 256+128+1, 400, pow(10, 0/20), 1700, pow(10, -14/20), 2600, pow(10, -12/20), 3200, pow(10, -14/20), 3580, pow(10, -20/20), 0., fs)
datati = synth(ftenor, 0.1, 256+128+1, 290, pow(10, 0/20), 1870, pow(10, -15/20), 2800, pow(10, -18/20), 3250, pow(10, -20/20), 3540, pow(10, -30/20), 0., fs)
datato = synth(ftenor, 0.1, 256+128+1, 400, pow(10, 0/20), 800, pow(10, -10/20), 2600, pow(10, -12/20), 2800, pow(10, -12/20), 3000, pow(10, -26/20), 0., fs)
datatu = synth(ftenor, 0.1, 256+128+1, 350, pow(10, 0/20), 600, pow(10, -20/20), 2700, pow(10, -17/20), 2900, pow(10, -14/20), 3300, pow(10, -26/20), 0., fs)

# Bass E2-C4
fbass = 16.35*pow(2, 4)
databa = synth(fbass, 0.1, 256+128+1, 600, pow(10, 0/20), 1040, pow(10, -7/20), 2250, pow(10, -9/20), 2450, pow(10, -9/20), 2750, pow(10, -20/20), 0., fs)
databe = synth(fbass, 0.1, 256+128+1, 400, pow(10, 0/20), 1620, pow(10, -12/20), 2400, pow(10, -9/20), 2800, pow(10, -12/20), 3100, pow(10, -18/20), 0., fs)
databi = synth(fbass, 0.1, 256+128+1, 250, pow(10, 0/20), 1750, pow(10, -30/20), 2600, pow(10, -16/20), 3050, pow(10, -22/20), 3340, pow(10, -28/20), 0., fs)
databo = synth(fbass, 0.1, 256+128+1, 400, pow(10, 0/20), 750, pow(10, -11/20), 2400, pow(10, -21/20), 2600, pow(10, -20/20), 2900, pow(10, -40/20), 0., fs)
databu = synth(fbass, 0.1, 256+128+1, 350, pow(10, 0/20), 600, pow(10, -20/20), 2400, pow(10, -32/20), 2675, pow(10, -28/20), 2950, pow(10, -36/20), 0., fs)

# Countertenor
fct = 16.35*pow(2, 4)
dataca = synth(fct, 0.1, 256+128+1, 660, pow(10, 0/20), 1120, pow(10, -6/20), 2750, pow(10, -23/20), 3000, pow(10, -24/20), 3350, pow(10, -38/20), 0., fs)
datace = synth(fct, 0.1, 256+128+1, 440, pow(10, 0/20), 1800, pow(10, -14/20), 2700, pow(10, -18/20), 3000, pow(10, -20/20), 3300, pow(10, -20/20), 0., fs)
dataci = synth(fct, 0.1, 256+128+1, 270, pow(10, 0/20), 1850, pow(10, -24/20), 2900, pow(10, -24/20), 3350, pow(10, -36/20), 3590, pow(10, -36/20), 0., fs)
dataco = synth(fct, 0.1, 256+128+1, 430, pow(10, 0/20), 820, pow(10, -10/20), 2700, pow(10, -26/20), 3000, pow(10, -22/20), 3300, pow(10, -34/20), 0., fs)
datacu = synth(fct, 0.1, 256+128+1, 370, pow(10, 0/20), 630, pow(10, -20/20), 2750, pow(10, -23/20), 3000, pow(10, -30/20), 3400, pow(10, -34/20), 0., fs)

data = np.concatenate([
    datasa, datase, datasi, dataso, datasu,
    datata, datate, datati, datato, datatu,
    dataaa, dataae, dataai, dataao, dataau,
    databa, databe, databi, databo, databu,
    dataca, datace, dataci, dataco, datacu,
])
sf.write('vox_test.wav', data, fs)
