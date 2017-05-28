import numpy as np
import pyaudio
import matplotlib.pyplot as plt
from speech_auth import *
from sklearn.neural_network import MLPClassifier

people = ['ren.txt', 'yak.txt']


def manh_d(unknown, cluster):
    return np.sum([np.abs(unknown[i] - cluster[i]) for i in range(len(unknown))])


def get_cluster(data):
    clusters = []
    y = []
    for i in range(len(people)):
        #features = []
        try:
            with open(people[i], 'r') as f:
                for line in f:
                    #features.append([float(j) for j in line.split(' ')])
                    clusters.append([float(j) for j in line.split(' ')])
                    y.append(i)
            #ans = np.array([0.0 for j in features[0]])
            #for j in features:
            #    ans += np.array(j)
            #ans /= len(features)
            #clusters.append(features)  # todo
        except FileNotFoundError:
            print('file', people[i], "doesn't exists")
    clf = MLPClassifier(solver='sgd', alpha=1e-5, activation='logistic',
                        hidden_layer_sizes=(40, 20, 10, 5), random_state=1,
                        learning_rate='adaptive')
    clf.fit(clusters, y)
    print(clf.predict([data]))
    print(clf.predict_proba([data]))
    print(clf.predict_log_proba([data]))

if __name__ == '__main__':
    ints = np.fromstring(read_data(), WIDTH_TO_BITS[SAMPLE_WIDTH])
    ints = normalize(ints)
    lf, rf = ints[0::2], ints[1::2]  # left and right channel
    lf = melkepstr(convert_to_mels(rfft(apply_hamming(cutting(lf)))))[1:]
    rf = melkepstr(convert_to_mels(rfft(apply_hamming(cutting(rf)))))[1:]
    for_class = [(rf[i] + lf[i])/2 for i in range(len(rf))]
    get_cluster(for_class)
