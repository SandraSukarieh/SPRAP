import matplotlib.pyplot as plt
import numpy as np


import groups_threshold
import histogram_functions
import roc_functions


def plot_error_bars():
    materials, x_pos, CTEs, error = groups_threshold.plot_groups_spamicity_with_filtering()

    fig, ax = plt.subplots()
    ax.bar(x_pos, CTEs, yerr=error, align='center', alpha=0.5, ecolor='black', capsize=10)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(materials)
    ax.yaxis.grid(True)

    plt.tight_layout()
    plt.show()


def plot_bar_chart():
    n_groups = 6
    score_1, score_2, score_3, plt.title = interval_spamicity_formula_experiments.plot_reviews_recall()

    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.1
    opacity = 0.8

    rects1 = plt.bar(index, score_1, bar_width,
                     alpha=opacity,
                     color='b',
                     # label='spam >= 0.5 & p.score >= 75%'
                     )

    rects2 = plt.bar(index + bar_width, score_2, bar_width,
                     alpha=opacity,
                     color='g',
                     # label='spam >= 0.56 & p.score >= 75%'
                     )

    rects3 = plt.bar(index + bar_width + bar_width, score_3, bar_width,
                     alpha=opacity,
                     color='r',
                     # label='spam >= 0.56 || p.score >= 85% || prob. <= 0.001'
                     )

    plt.xlabel('Reporting Intervals Scores')
    plt.ylabel('Performance')
    plt.xticks(index + bar_width, ('1', '2', '3', '4', '5', '6'))
    plt.legend()

    plt.tight_layout()
    plt.show()


roc_functions.plot_roc_baselines()
plot_error_bars()