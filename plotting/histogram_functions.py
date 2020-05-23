import codecs
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def read_file(file_name, data_list, data_set):
    file = codecs.open(file_name, "r", "utf-8")
    lines = file.readlines()
    for line in lines:
        value = int(line)
        data_list.append(value)
        data_set.add(value)
    file.close()


def plot_intervals_histogram():
    intervals_sizes = []
    intervals_set = set()
    read_file("top_ranked_intervals_sizes.txt", intervals_sizes, intervals_set)
    print("number of unique values = ", len(intervals_set))
    print(intervals_set)
    # sns.distplot(intervals_sizes, bins=72, kde=False, hist_kws={'edgecolor':'black'}, kde_kws={'linewidth':5})
    sns.distplot(intervals_sizes, bins=72, kde=False)
    plt.xlim(0, 30)
    plt.title('Reported Intervals Sizes')
    plt.xlabel('Interval Width')
    plt.ylabel('Frequency')
    plt.grid(linestyle='--',  alpha=0.9)
    plt.show()


def remove_non_printable_characters(content):
    """
    :param content: the content of the file
    :return: the content after removing any in the black list
    """
    for ch in ['\u2028', '\u001D', '\u000B', '\u0085', '\u00A0', '\u2029', '\u000c', '\u0013', '\u001c', '\u001d', '\u0019']:
        if ch in content:
            content = content.replace(ch, ' ')
    return content


def plot_groups_histogram():
    groups_sizes = []
    groups_set = set()
    read_file("collusion_groups_sizes.txt", groups_sizes, groups_set)
    print("number of unique values = ", len(groups_set))
    print(groups_set)
    sns.distplot(groups_sizes, bins=1140, kde=False, hist_kws={'edgecolor':'black'}, kde_kws={'linewidth':5})
    plt.title('Reported Groups Sizes')
    plt.xlabel('Members Count')
    plt.ylabel('Frequency')
    plt.xlim(0, 30)
    plt.grid(linestyle='--',  alpha=0.9)
    plt.show()


def plot_groups_targets_histogram():
    file = codecs.open("collusion_groups.txt", "r", "utf-8")
    content = file.read()
    lines = remove_non_printable_characters(content).splitlines()
    targets = []
    my_set = set()
    for line in lines:
        group_targets = set()
        line = line.strip().split(", ")
        targets_set = line[2]
        for char in targets_set:
            if char in "{}":
                targets_set = targets_set.replace(char, " ")
        for p in targets_set.split(','):
            for char in p:
                if char in " ":
                    p = p.replace(char, "")
            group_targets.add(p)
        if '' in group_targets:
            group_targets.remove('')
        targets.append(len(group_targets))
        my_set.add(len(group_targets))
    file.close()
    print(len(my_set))
    print(my_set)
    sns.distplot(targets, bins=6, kde=False, hist_kws={'edgecolor':'black'}, kde_kws={'linewidth':5})
    plt.title('Collusion Groups Targets Count')
    plt.xlabel('Group Targets Count')
    plt.ylabel('Frequency')
    plt.xlim(0, 10)
    plt.grid(linestyle='--', alpha=0.9)
    plt.show()

plot_intervals_histogram()
plot_groups_histogram()
plot_groups_targets_histogram()

