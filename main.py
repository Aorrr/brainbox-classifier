import time
import serial
import numpy as np
import sys
from pyautogui import press, keyDown, keyUp
from classifier import Classifier
from dynamic_filter import filter
import matplotlib.pyplot as plt

def read_arduino(ser,inputBufferSize):
    #Outputs a signal list of length inputBufferSize from ser (the serial port object)
    data = ser.read(inputBufferSize)
    out =[(int(data[i])) for i in range(0,len(data))]
    return out

def process_data(data,freq_min,freq_max):
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
    return result

def smooth(wave, width) :
    smoothed = np.cumsum(wave, dtype=float)
    smoothed[width:] = smoothed[width:] - smoothed[:-width]
    return (smoothed[width - 1:] / width).tolist()

def standardize(wave):
    mean = np.mean(wave)
    sd = np.std(wave)
    return [(i - mean)/sd for i in wave]

def run():
    classifier = Classifier()
    #argpass
    eye_left_key = sys.argv[1]
    eye_right_key = sys.argv[2]
    blink_key = sys.argv[3]

    freq_min = float(sys.argv[4])
    freq_max = float(sys.argv[5])

    model_selection = sys.argv[6]

    threshold_val = float(sys.argv[7])
    wink_threshold_val = float(sys.argv[8])

    classifier.model = model_selection

    baudrate = 230400
    cport = 'COM8'  # set the correct port before you run it  ls /dev/tty.*
    ser = serial.Serial(port=cport, baudrate=baudrate)

    # take continuous data stream
    inputBufferSize = 10000 # keep betweein 2000-20000

    plt.ion()
    data = []
    event = False
    count = 0
    while True:
        eye_movement = 'N'
        data_single = read_arduino(ser,inputBufferSize)
        data_temp = process_data(data_single, freq_min, freq_max).tolist()
        if not event:
            smoothed_data_temp = smooth(data_temp, 500)
            if(abs(max(smoothed_data_temp) - min(smoothed_data_temp)) > threshold_val):
                print("event")
                event = True
                data = data_temp.copy()
                count += 1
        else:
            data = data + data_temp
            count += 1
            if count >= 3:
                data = smooth(data, 1000)
                count = 0
                event = False
                eye_movement = classifier.classify(data, wink_threshold_val)
                data = []
                print(eye_movement)

        if eye_movement == 'N':
            continue
        elif eye_movement == 'L':
            print(eye_movement)
            keyDown(eye_left_key)
            time.sleep(1)
            keyUp(eye_left_key)
        elif eye_movement == 'R':
            print(eye_movement)
            keyDown(eye_right_key)
            time.sleep(1)
            keyUp(eye_right_key)
        elif eye_movement == 'W':
            print(eye_movement)
            press(blink_key)
            time.sleep(0.3)



if __name__ == "__main__":
    print("ok")
    run()
