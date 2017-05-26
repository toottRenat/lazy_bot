# main ideas were taken from https://habrahabr.ru/post/144491/

import numpy as np
import pyaudio
import scipy.fftpack

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 16000
N = 0.128  # длина кадра
RECORD_SECONDS = 3
WIDTH_TO_BITS = {1: np.int8, 2: np.int16, 4: np.int32}
SAMPLE_WIDTH = 2


def read_data():
    p = pyaudio.PyAudio()

    speakers = p.get_default_output_device_info()["hostApi"]

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_host_api_specific_stream_info=speakers)

    print("* recording")

    frames = b''

    for i in range(int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames += data
    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()
    return frames


def normalize(data):
    return data/max(np.abs(min(data)), max(data))


def cutting(data):
    n_rate = int(N * RATE)  # длина одного блока
    overlap = n_rate//2
    cutted_ints = [data[:n_rate]]
    for i in range(1, len(data)//n_rate):
        cutted_ints.append(data[i*n_rate - overlap:i*n_rate + overlap])
    cutted_ints.append(data[len(data) - n_rate:])
    return np.array(cutted_ints)


def apply_hamming(data):
    w = [0.53836 - 0.46164*np.cos(2*np.pi*i/(len(data[0]) - 1)) for i in range(len(data[0]))]
    for i in range(len(data)):
        data[i] *= w
    return data


def rfft(data):
    return np.array([scipy.fftpack.rfft(i) ** 2 for i in data])


def convert_to_mels(data):
    return np.array([1127*np.log(1 + i/700) for i in data])

if __name__ == '__main__':
    ints = np.fromstring(read_data(), WIDTH_TO_BITS[SAMPLE_WIDTH])
    ints = normalize(ints)
    lf, rf = ints[0::2], ints[1::2]  # left and right channel
    lf = convert_to_mels(rfft(apply_hamming(cutting(lf))))
    rf = convert_to_mels(rfft(apply_hamming(cutting(rf))))
