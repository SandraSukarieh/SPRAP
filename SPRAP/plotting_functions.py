import matplotlib.pyplot as plt


def plot_indicators_empirical_analysis(all_sorted_intervals):
    """

    :param all_sorted_intervals: all created time intervals
    """

    spam_x = []
    spam_y = []
    non_x = []
    non_y = []
    counter = 0
    for interval in all_sorted_intervals:
        if interval.spam_label:
            spam_x.append(counter)
            spam_y.append(interval.density)
        else:
            non_y.append(interval.density)
            non_x.append(counter)

        counter += 1

    plt.scatter(spam_x, spam_y, c='red')
    plt.scatter(non_x, non_y, c='green')
    plt.xlabel('Interval')
    plt.ylabel('Density')
    plt.show()

