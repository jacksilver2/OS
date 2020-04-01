import random

from matplotlib import pyplot as plt
import numpy as np

MAX_SIG_AMP = 0.5
MAX_NOISE_AMP = 0.75
NOISE_PROBABILITY = 0.2
N_DATA_POINTS = 1000
HI_SIG_BOUND = 20
LO_SIG_BOUND = 0
W_SIZE = 5


def smooth_out(data, W=5, iters=1, s_type='median'):
    if iters == 0:
        return data
    N = data.__len__()

    if s_type == 'average':
        s_data = [np.mean(data[max(0, i - W):min(i + W, N - 1)]) for i in range(N)]
    if s_type == 'median':
        s_data = [np.median(data[max(0, i - W):min(i + W, N - 1)]) for i in range(N)]

    return smooth_out(s_data, W, iters - 1)


# def dft_smooth(sig):
#     d_sig




def main():
    perfect_signal = [np.sin(x) for x in np.linspace(LO_SIG_BOUND, HI_SIG_BOUND, N_DATA_POINTS)]

    plt.plot(perfect_signal, "-", linewidth=0.7)
    data = [perfect_signal[i] +
            MAX_NOISE_AMP * random.random() * np.random.choice([0, 1, -1], 1, True,
                                                               [1 - NOISE_PROBABILITY, 0.5 * NOISE_PROBABILITY,
                                                                0.5 * NOISE_PROBABILITY])[0]
            for i in range(N_DATA_POINTS)]
    plt.plot(data, "--", linewidth=0.5)
    smooth_data_average = np.asarray(smooth_out(data, W=W_SIZE, iters=1, s_type='average'))
    smooth_data_median = np.asarray(smooth_out(data, W=W_SIZE, iters=1, s_type='median'))
    plt.plot(smooth_data_average, color='red')
    plt.plot(smooth_data_median, color='green')
    av_mse = np.sum(np.square(perfect_signal - smooth_data_average))
    med_mse = np.sum(np.square(perfect_signal - smooth_data_median))
    print('av MSE =', av_mse)
    print('med MSE =', med_mse)

    plt.show()


if __name__ == '__main__':
    main()
