import json
import numpy as np
from classifier import Classifier
from matplotlib import pyplot as plt

def smooth(wave, width) :
    smoothed = np.cumsum(wave, dtype=float)
    smoothed[width:] = smoothed[width:] - smoothed[:-width]
    return (smoothed[width - 1:] / width).tolist()

def standardize(wave):
    mean = np.mean(wave)
    sd = np.std(wave)
    return [(i - mean)/sd for i in wave]

def streaming_classifier(wave):
    threshold = 400
    signals = []
    increment = 5000
    i = 0
    count = 0
    event = False
    data = []
    while i < len(wave) - 5000:
        data_temp = wave[i:i+5000]
        smoothed_data_temp = smooth(data_temp, 500)
        #plt.plot(smoothed_data_temp)
        #plt.show()
        if not event:
            if(abs(max(smoothed_data_temp) - min(smoothed_data_temp)) > 30):
                print("event")
                event = True
                data = data_temp
                count += 1
        else:
            data = data + data_temp
            count += 1
            if count >= 3:
                data = smooth(data, 1000)
                count = 0
                event = False
                #eye_movement = classifier.classify(data, threshold_val, wink_threshold_val)
                signals.append(data.copy())
                data = []
        i = i+5000
    return signals

def streaming_classifier2(wave):
    classifier = Classifier()
    i = 0
    signals = []
    while i < len(wave) - 10000:
        data = []
        eye_movement = 'no_movement'
        count = 0
        while eye_movement == 'no_movement':
            data_single = wave[i:i+5000]
            data += data_single
            i += 5000
            if count > 5:
                data = data[5000:]
            #plt.figure()
            #plt.plot(data)
            #plt.show()
            eye_movement = classifier.classify(data, 550, 700)  #eye movement to have an output of either ['no_movement','left','right','blink']
            count += 1
            plt.plot(data)
            plt.show()
        for j in range(1):  #take a few more smaples to minimise error.
            data_single = wave[i:i+5000]
            i += 5000
            data = data + data_single
        signals.append(data.copy())
    return signals

#wave_file = open("wink_data_1_28.json", "r")
wave_file = open("../the_newdata/left20_2.json", "r")
wave = json.load(wave_file)
#plt.plot(smooth(wave,1000))
#plt.show()

'''
for s in signals:
    plt.figure()
    plt.plot(s)
    plt.show()
'''
#plt.plot(signals[3])
#plt.show()
'''
fig, axs = plt.subplots(2)
axs[0].plot(wave)
axs[1].plot(test)
plt.show()
'''
