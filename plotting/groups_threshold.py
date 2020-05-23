import numpy as np


def plot_groups_spamicity():

    # groups precision results 0.4 --> 0.9
    threshold_1 = [0.833333333333333, 0.959459459459459, 0.92079207920792, 0.963302752293578, 0.969696969696969]
    threshold_2 = [0.833333333333333, 0.959459459459459, 0.92079207920792, 0.963302752293578, 0.969696969696969]
    threshold_3 = [0.833333333333333, 0.959459459459459, 0.92079207920792, 0.963302752293578, 0.969696969696969]
    threshold_4 = [0.833333333333333, 0.959459459459459, 0.91919191919191, 0.963302752293578, 1]
    threshold_5 = [0.833333333333333, 0.958904109589041, 0.91919191919191, 0.963302752293578, 0]
    threshold_6 = [0.833333333333333, 1, 0.924242424242424, 0.989130434782608, 0]

    threshold_1_mean = np.mean(threshold_1)
    threshold_2_mean = np.mean(threshold_2)
    threshold_3_mean = np.mean(threshold_3)
    threshold_4_mean = np.mean(threshold_4)
    threshold_5_mean = np.mean(threshold_5)
    threshold_6_mean = np.mean(threshold_6)

    threshold_1_std = np.std(threshold_1)
    threshold_2_std = np.std(threshold_2)
    threshold_3_std = np.std(threshold_3)
    threshold_4_std = np.std(threshold_4)
    threshold_5_std = np.std(threshold_5)
    threshold_6_std = np.std(threshold_6)

    materials = ['0,4', '0,5', '0,6', '0,7', '0,8', '0,9']
    x_pos = np.arange(len(materials))
    CTEs = [threshold_1_mean, threshold_2_mean, threshold_3_mean, threshold_4_mean, threshold_5_mean, threshold_6_mean]
    error = [threshold_1_std, threshold_2_std, threshold_3_std, threshold_4_std, threshold_5_std, threshold_6_std]

    return materials, x_pos, CTEs, error