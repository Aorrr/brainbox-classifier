import json
import numpy as np
from matplotlib import pyplot as plt

def smooth(wave, width) :
    smoothed = np.cumsum(wave, dtype=float)
    smoothed[width:] = smoothed[width:] - smoothed[:-width]
    return (smoothed[width - 1:] / width).tolist()

def extract_test(wave):
    test = []
    window_size = 5000
    i = 0
    while i < len(wave) - window_size:
        window = wave[i:i+window_size]
        t = np.std(window)
        test.append(t)
        i += 5000
    return test

def extract_signal_interval_sd(wave):
    window_size = 5000
    i = 0
    signal = []
    signal_temp = []
    event = False
    while i < len(wave) - window_size:
        window = wave[i:i+window_size]
        if(np.std(window) > 10):
            if not event:
                event = True
                signal.append(i)
        elif event:
            #signal_temp.append(i + window_size//2)
            #signal.append(signal_temp.copy())
            #signal_temp = []
            event = False
        i += 100
    print("number of signals extracted: {}".format(len(signal)))
    return signal

def extract_signal_interval_maxmin(wave):
    window_size = 5000
    i = 0
    signal = []
    signal_temp = []
    event = False
    while i < len(wave) - window_size:
        window = wave[i:i+window_size]
        if(max(window)-min(window) > 10):
            if not event:
                event = True
                signal.append(i)
        elif event:
            #signal_temp.append(i + window_size//2)
            #signal.append(signal_temp.copy())
            #signal_temp = []
            event = False
        i += 5000
    print("number of signals extracted: {}".format(len(signal)))
    return signal

def extract_signal(wave, interval):
    signals = []
    for i in interval:
        signals.append(smooth(wave[i:i+15000], 1000))
    return signals

wave_file = open("../the_newdata/left20.json", 'r')
wave = json.load(wave_file)

test = extract_test(wave)
interval = extract_signal_interval_sd(wave)
signals = extract_signal(wave, interval)
plt.plot(test)
plt.show()


file = open("left20_1.json", 'w')
json.dump(signals, file)

'''
wave_file1 = open("wave/wink10_2.json", "r")
wave_file2 = open("wave/wink10_3.json", "r")
wave1 = json.load(wave_file1)
wave2 = json.load(wave_file2)
test1 = extract_test(wave1)
test2 = extract_test(wave2)

interval1 = extract_signal_interval_sd(wave1)
signals1 = extract_signal(wave1, interval1)
interval2 = extract_signal_interval_sd(wave2)
signals2 = extract_signal(wave2, interval2)

signals = signals1 + signals2

file = open('wink20_2.json', 'w')
signals = json.dump(signals, file)
'''
'''
test = extract_test(wave)
plt.plot(test)
plt.show()

for s in signals:
    plt.plot(s)
    plt.show()
'''
