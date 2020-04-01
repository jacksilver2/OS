from matplotlib import pyplot as plt
import datetime as dt
import numpy as np
import requests
from lxml import html
from smoothing_signal import smooth_out


def get_sick_data():
    page = requests.get(
        'https://he.wikipedia.org/wiki/%D7%94%D7%AA%D7%A4%D7%A8%D7%A6%D7%95%D7%AA_%D7%A0%D7%92%D7%99%D7%A3_%D7%94%D7%A7%D7%95%D7%A8%D7%95%D7%A0%D7%94_%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C')
    search_term = 'display:inline-block">'
    l = list(page.text.split(search_term))

    data = []
    for i in range(1, l.__len__(), 2):
        data.append(int(l[i].split("<")[0].replace(",", "")))
    return data


def get_all_data():
    dates = []
    dead = []
    recovered = []
    sick = []
    page = requests.get(
        'https://he.wikipedia.org/w/index.php?title=%D7%94%D7%AA%D7%A4%D7%A8%D7%A6%D7%95%D7%AA_%D7%A0%D7%92%D7%99%D7%A3_%D7%94%D7%A7%D7%95%D7%A8%D7%95%D7%A0%D7%94_%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C&action=edit&section=5')
    data = page.text.split('rows=\n')[1].split('|caption')[0]
    data = data.replace('{{Medical cases chart/Row|', "")
    data = data.replace('}}', "").strip('\n')
    data = data.split('\n')
    for d in data:
        pass
        sd = d.split('|')
        sd = [sd[i] if sd[i] != '' else '0' for i in range(sd.__len__())]
        dates.append(sd[0])
        dead.append(int(sd[1]))
        recovered.append(int(sd[2]))
        sick.append(int(sd[3]))

    return {'dates': dates,
            'dead': dead,
            'recovered': recovered,
            'sick': sick
            }


all_data = get_all_data()
num_sick = all_data['sick']
dates = all_data['dates']
dead = all_data['dead']
recovered = all_data['recovered']
manual_data_addition = [5591]
num_sick.extend(manual_data_addition)
N = num_sick.__len__()

print('sick', num_sick)
print('dead', dead)
print('recovered', recovered)

GROWTH_RATE = 1.265

OPTIMISTIC_MID_DAY = 39
i_0 = OPTIMISTIC_MID_DAY
OPTIMISTIC_L = num_sick[i_0] * 2
K = 0.22  # manually set...

print('# data points:', N)

deltas = [num_sick[i + 1] - num_sick[i] for i in range(N - 1)]
apparent_exp = [GROWTH_RATE ** i for i in range(N)]
deltas_ratios = np.asarray([(deltas[i + 1] + 1) / (deltas[i] + 1) for i in range(N - 2)])
implied_logistic = [num_sick[N - 1] * 2 / (1 + np.e ** (-K * (i - (N - 1)))) for i in range(0, 6 * N // 4)]
optimistic_logistic = [OPTIMISTIC_L / (1 + np.e ** (-K * (i - i_0))) for i in range(0, 6 * N // 4)]


def plot_all():
    N_PLOTS = 4
    plt.title('Corona in Israel')

    plt.subplot(N_PLOTS, 1, 1)
    plt.plot(num_sick, linewidth=4)
    # plt.plot(apparent_exp, '--')
    plt.plot(optimistic_logistic, ".", markersize=1)
    plt.plot(implied_logistic, "--", linewidth=0.5)
    plt.gca().legend(
        ['# sick', 'optimistic logistic -- 1.04 is midpoint', 'implied logistic', 'recovered', 'dead'])

    plt.subplot(N_PLOTS, 1, 2)
    plt.bar(range(N - 1), deltas)
    plt.gca().legend(['#sick(n)-#sick(n-1)'])

    plt.subplot(N_PLOTS, 1, 3)
    plt.plot(deltas_ratios, color='red')
    plt.plot(smooth_out(deltas_ratios, W=2, s_type='average'), '--', color='purple')
    plt.plot(np.ones(deltas_ratios.__len__()), '--', color='blue', linewidth=1)
    plt.gca().legend(['delta(n)/delta(n-1)', 'W=5 average'])

    plt.subplot(N_PLOTS, 1, 4)

    plt.bar(range(N-manual_data_addition.__len__()), recovered, color='green')
    plt.bar(range(N - manual_data_addition.__len__()), dead, color='red')
    plt.gca().legend(['recovered', 'dead'])


plot_all()

plt.show()
