import pickle
import catch22
import json
import tensorflow as tf
import numpy as np
import time
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

class Classifier:

    def __init__(self):
        self.svm_model = pickle.load(open('models/svm_model.sav','rb'))
        self.knn_model = pickle.load(open('models/knn_model.sav', 'rb'))
        self.ann_model = tf.keras.models.load_model('models/ann/')
        self.lda_model = pickle.load(open('models/lda_model.sav', 'rb'))
        self.scaler = pickle.load(open('models/scaler.sav', 'rb'))
        self.model = 'simple'

    def extract_features_uni(self, data):
        features = []
        features.append(catch22.DN_HistogramMode_5(data))
        features.append(catch22.DN_HistogramMode_10(data))
        features.append(catch22.CO_f1ecac(data))
        features.append(catch22.CO_FirstMin_ac(data))
        features.append(catch22.CO_HistogramAMI_even_2_5(data))
        features.append(catch22.PD_PeriodicityWang_th0_01(data))
        features.append(catch22.DN_OutlierInclude_p_001_mdrmd(data))
        features.append(catch22.DN_OutlierInclude_n_001_mdrmd(data))
        features.append(catch22.SP_Summaries_welch_rect_centroid(data))
        return features

    def extract_features_rec(self, data):
        features = []
        features.append(catch22.DN_HistogramMode_10(data))
        features.append(catch22.CO_f1ecac(data))
        features.append(catch22.CO_FirstMin_ac(data))
        features.append(catch22.CO_HistogramAMI_even_2_5(data))
        features.append(catch22.PD_PeriodicityWang_th0_01(data))
        features.append(catch22.DN_OutlierInclude_p_001_mdrmd(data))
        features.append(catch22.DN_OutlierInclude_n_001_mdrmd(data))
        features.append(catch22.SP_Summaries_welch_rect_area_5_1(data))
        features.append(catch22.SC_FluctAnal_2_rsrangefit_50_1_logi_prop_r1(data))
        return features

    def simple_classifier(self, data, wink_threshold): # threshold 30, wink_threshold 400
        #data = data.tolist()
        #print(max(data))
        #print(len(data))
        if max(data) - min(data) > wink_threshold:
            return 'W'
        elif data.index(max(data)) < data.index(min(data)):
            return "L"
        else:
            return "R"

    def svm(self, data):
        data = data[::10]
        features = self.extract_features_rec(data)
        features.append(np.std(data))
        X = self.scaler.transform([features])
        prediction = self.svm_model.predict(X)
        return prediction[0]

    def knn(self, data):
        data = data[::10]
        features = self.extract_features_rec(data)
        features.append(np.std(data))
        X = self.scaler.transform([features])
        prediction = self.knn_model.predict(X)
        return prediction[0]

    def ann(self, data):
        class_names = ['L','R','W']
        data = data[::10]
        features = self.extract_features_rec(data)
        features.append(np.std(data))
        X = self.scaler.transform([features])
        return class_names[np.argmax(self.ann_model.predict(X.reshape((1, 10))))]

    def lda(self, data):
        data = data[::10]
        features = self.extract_features_rec(data)
        features.append(np.std(data))
        X = self.scaler.transform([features])
        prediction = self.lda_model.predict(X)
        return prediction[0]

    def classify(self, data, wink_threshold=0):
        if self.model == 'simple':
            assert wink_threshold != 0
            return self.simple_classifier(data, wink_threshold)
        elif self.model == 'knn':
            return self.knn(data)
        elif self.model == 'svm':
            return self.svm(data)
        elif self.model == 'lda':
            return self.lda(data)
        elif self.model == 'ann':
            return self.ann(data)
        else:
            raise Exception('Invalid classifier model specifier.')

'''
# For testing
c = Classifier()
file = open('./left20_1.json')
test = json.load(file)[19]
test = test
plt.plot(test)
plt.show()

start_time = time.time()
print(len(test))
print(c.lda(test))
print(time.time()-start_time)
'''
# import matplotlib.pyplot as plt
# import numpy as np
# import wave
# import sys
#
# def simple_classifier(data):
#     Y = np.array(data)
#
#     max_time = len(data)
#     frameRate = 50000
#
#     max_time_second =max_time/frameRate
#
#     xtime = np.arange(0, max_time, 0.0001)
#
#
#     # CLASSIFIER FOR ZERO CROSSING
#     import pandas as pd
#     # python start from 0. r start from 1 !!
#     lower_interval = 0
#     windowSize = 5000
#     predictThreshold = 17
#     increment = windowSize/10
#     predictedIncre = 10000
#     predictedlabels = "no_movement"
#
#     while max_time > lower_interval + windowSize:
#         upper_interval = lower_interval + windowSize
#         lower_interval = int(lower_interval)
#         upper_interval = int(upper_interval)
#         interval = Y[lower_interval:upper_interval+1]
#         interval = interval.astype(np.int32)
#         test_stat = np.sum(np.multiply(interval[0:-1],interval[1:]) <= 0 )
#
#         if test_stat < predictThreshold:
#             maxVal = np.argmax(interval)
#             minVal = np.argmin(interval)
#             predicted = 'L' if maxVal < minVal else 'R'
#             #print(predicted)
#             predictedlabels = predictedlabels + predicted
#             lower_interval = lower_interval + predictedIncre
#         else:
#             lower_interval = lower_interval + increment
#     return predictedlabels
#myclassifier = Classifiers()
#file = open("data/wink_data_1_28.json", 'r')
#X = json.load(file)
#values = catch22.catch22_all(X[2])['values']
#print(myclassifier.svm(X[2]))
