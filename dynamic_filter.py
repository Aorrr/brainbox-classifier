from scipy.io import wavfile
import numpy as np
import sys
import matplotlib.pyplot as plt

def filter(data,freq_min,freq_max):
    ####### Fourier Filter #######
    fs = 24975
    timestep = 1/fs
    #print(fs)

    data_fft = np.fft.fft(data)
    freq = np.fft.fftfreq(data.shape[-1],d=timestep)

    data_fft[abs(freq)>freq_max] = 0
    data_fft[abs(freq)<freq_min] = 0

    filtered_data = np.fft.ifft(data_fft).real
    return filtered_data
