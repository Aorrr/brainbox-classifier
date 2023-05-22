import json
import pickle
import pandas as pd
import numpy as np
import catch22
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


def feature_selection(file_list, label_list, LR_wave_seqs1):
    features_name = catch22.catch22_all(LR_wave_seqs1[0])['names']
    df = pd.DataFrame(columns=features_name)
    label = list()

    for i in range(len(file_list)):
        for w in file_list[i]:
            df.loc[len(df)] = catch22.catch22_all(w)['values']
        label += label_list[i]

    df['label'] = label
    return df


def standardization(df):
    X = df.iloc[:, :-1].values
    y = df.iloc[:, 22].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
    scaler = StandardScaler()
    scaler.fit(X_train)

    scaler_pickle = open('scaler.sav', 'wb')
    pickle.dump(scaler, scaler_pickle)

    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, X_test, y_train, y_test


def knn(df):
    X_train, X_test, y_train, y_test = standardization(df)

    knn = KNeighborsClassifier(n_neighbors=7)
    knn.fit(X_train, y_train)

    # Its important to use binary mode
    knnPickle = open('knnpickle_file', 'wb')

    # source, destination
    pickle.dump(knn, knnPickle)

    # Predict on dataset which model has not seen before
    prediction = knn.predict(X_test)
    # Accuracy
    accuracy = knn.score(X_test, y_test)


    ######################################################################
    # WHY DID WE CHOOSE K = 7
    # (smaller K can be noisy and will have a high influence on result.)
    # prediction = ""
    # accuracy = []
    # K = 1
    # while K < 11:
    #     temp = []
    #     for j in range(50):
    #         knn = KNeighborsClassifier(n_neighbors=K)
    #         knn.fit(X_train, y_train)

    #         #accuracy
    #         temp.append(knn.score(X_test, y_test))

    #     accuracy.append(mean(temp))
    #     K += 1

    # neighbors = np.arange(1, 11)
    # plt.plot(neighbors, accuracy, label = 'Testing dataset Accuracy')

    # plt.legend()
    # plt.xlabel('n_neighbors')
    # plt.ylabel('Accuracy')
    # plt.show()
    #######################################################################

    return prediction, accuracy


def main():
    with open("data/LR_data_1_72.json") as f:
        LR_wave_seqs1 = json.load(f)

    with open("data/LR_label_1_72.json") as f:
        LR_wave_labels1 = json.load(f)

    with open("data/left_data_1_13.json") as f:
        left_wave_seqs1 = json.load(f)

    with open("data/left_label_1_13.json") as f:
        left_wave_labels1 = json.load(f)

    with open("data/right_data_1_40.json") as f:
        right_wave_seqs1 = json.load(f)

    with open("data/right_label_1_40.json") as f:
        right_wave_labels1 = json.load(f)

    with open("data/wink_data_1_28.json") as f:
        wink_wave_seqs1 = json.load(f)

    with open("data/wink_label_1_28.json") as f:
        wink_wave_labels1 = json.load(f)

    file_list = [LR_wave_seqs1, left_wave_seqs1, right_wave_seqs1, wink_wave_seqs1]
    label_list = [LR_wave_labels1, left_wave_labels1, right_wave_labels1, wink_wave_labels1]

    df = feature_selection(file_list, label_list, LR_wave_seqs1)
    knn_prediction, knn_accuracy = knn(df)
    # print(knn_prediction)
    # print(knn_accuracy)


if __name__ == "__main__":
    main()
