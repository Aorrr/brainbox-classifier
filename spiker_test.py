import serial
import numpy as np
import matplotlib.pyplot as plt
import time
from matplotlib.animation import FuncAnimation
from dynamic_filter import filter
import wave
import json

def smooth(wave, width) :
    smoothed = np.cumsum(wave, dtype=float)
    smoothed[width:] = smoothed[width:] - smoothed[:-width]
    return (smoothed[width - 1:] / width).tolist()

#plt.style.use('fivethirtyeight')
def read_arduino(ser,inputBufferSize):
    data = ser.read(inputBufferSize)
    out =[(int(data[i])) for i in range(0,len(data))]
    return out

def process_data(data,freq_min=0,freq_max=12):
    data_in = np.array(data)
    result = []
    i = 1
    while i < len(data_in)-1:
        if data_in[i] > 127:
            # Found beginning of frame
            # Extract one sample from 2 bytes
            intout = (np.bitwise_and(data_in[i],127))*128
            i = i + 1
            intout = intout + data_in[i]
            result = np.append(result,intout)
        i=i+1
    result = filter(result,freq_min,freq_max)
    print(result)
    return result

baudrate = 230400
cport = 'COM8'  # set the correct port before you run it
ser = serial.Serial(port=cport, baudrate=baudrate)


# take continuous data stream
inputBufferSize = 10000 # keep betweein 2000-20000
ser.timeout = inputBufferSize/20000.0  # set read timeout, 20000 is one second
total_time = 20.0; # time in seconds [[1 s = 20000 buffer size]]
max_time = 10.0; # time plotted in window [s]
N_loops = 20000.0/inputBufferSize*total_time

T_acquire = inputBufferSize/20000.0    # length of time that data is acquired for
N_max_loops = max_time/T_acquire    # total number of loops to cover desire time window




# sample rate = 20000
# sample interval = 0.05ms
# one data_temp corresponds to 0.25s sample.
read_arduino(ser,inputBufferSize)
read_arduino(ser,inputBufferSize)
read_arduino(ser,inputBufferSize)
read_arduino(ser,inputBufferSize)
read_arduino(ser,inputBufferSize)
def animate(k):
    global data_plot
    global data_to_record
    data = read_arduino(ser,inputBufferSize)
    data_temp = process_data(data).tolist()
    if not data_to_record:
        data_to_record = data_temp
    else:
        data_to_record += data_temp
    if k <= N_max_loops:
        if k==0:
            data_plot = data_temp
        else:
            data_plot = np.append(data_temp,data_plot)
        t = (min(k+1,N_max_loops))*inputBufferSize/20000.0*np.linspace(0,1,len(data_plot))
    else:
        data_plot = np.roll(data_plot,len(data_temp))
        data_plot[0:len(data_temp)] = data_temp
    t = (min(k+1,N_max_loops))*inputBufferSize/20000.0*np.linspace(0,1,len(data_plot))

    print(len(data_temp))

    plt.cla()
    plt.plot(t, data_plot)
    plt.ylim([350,850])

data_plot = []
data_to_record = []
ani = FuncAnimation(plt.gcf(), animate)

plt.tight_layout()
plt.show()
