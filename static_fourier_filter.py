from scipy.io import wavfile
import numpy as np
import sys
import matplotlib.pyplot as plt

def filter(data,freq_min,freq_max):
    ############ I/O #############
    if len(sys.argv) != 4:
        print('Please specify a file name and/or a frequency range')
        sys.exit()

    file_name = sys.argv[1]
    try:
        fs, data = wavfile.read(file_name)
    except:
        print('Invalid file name')
        sys.extt()

    try:
        freq_min = float(sys.argv[2])
        freq_max = float(sys.argv[3])
    except:
        print('Please input valid frequencies')
        sys.exit()

    if freq_min >= freq_max:
        print('Minimum frequency is larger than or equal to maximum frequency. Exiting...')
        sys.exit()

    ##############################
    #plt.plot(data)
    ####### Fourier Filter #######
    fs = 24975
    timestep = 1/fs
    #print(fs)

    data_fft = np.fft.fft(data)
    freq = np.fft.fftfreq(data.shape[-1],d=timestep)

    data_fft[abs(freq)>freq_max] = 0
    data_fft[abs(freq)<freq_min] = 0

    filtered_data = np.fft.ifft(data_fft).real
    plt.plot(filtered_data)
    plt.legend(['Unfiltered data', 'Filtered data'])
    plt.plot(freq,abs(data_fft))
    plt.show()

    write_file_name = file_name[:-4] + '_filtered_' + str(freq_min) + '_' + str(freq_max) + '.wav'
    wavfile.write(write_file_name,fs,filtered_data)
