import numpy as np
from statsmodels.distributions import ECDF
from scipy.stats import multinomial


def calculate_interval_time_weight(time_interval):
    """

    :param time_interval: the time interval of which we calculate the time weight
    """

    x = time_interval.width - 1
    time_interval.time_weight = np.exp(-x)


def calculate_interval_density(time_interval):
    """

    :param time_interval: the time interval of which we calculate the density
    """

    calculated_density = 0.0
    for time_data in time_interval.data:
        rate_weight = 0.0
        if (time_data.rate == 5) or (time_data.rate == 1):
            rate_weight = 1
        elif (time_data.rate == 4) or (time_data.rate == 2):
            rate_weight = 0.6
        elif time_data.rate == 3:
            rate_weight = 0.2

        for i in range(time_data.count):
            calculated_density += rate_weight

    calculated_density = round(calculated_density, 1)  # sometimes am getting wrong summation results due to python!! so am rounding
    time_interval.density = calculated_density


def calculate_total_weight_for_one_interval(time_interval, empirical_distribution_CDF_lists):
    """

    :param time_interval: the time interval we want to calculate total weight for
    :param empirical_distribution_CDF_lists: CDF distribution of all created intervals for normalizing
    """
    # all_densities = []
    # all_time_weights = []
    # all_users_counts = []
    # for interval in empirical_distribution_intervals:
    #     all_densities.append(interval.density)
    #     all_time_weights.append(interval.time_weight)
    #     all_users_counts.append(len(interval.users))
    #
    # densities_cdf = ECDF(all_densities)
    # time_weights_cdf = ECDF(all_time_weights)
    # users_counts_cdf = ECDF(all_users_counts)

    time_interval.f_density = empirical_distribution_CDF_lists[0](time_interval.density)
    time_interval.f_time_weight = empirical_distribution_CDF_lists[1](time_interval.time_weight)
    time_interval.f_users_count = empirical_distribution_CDF_lists[2](len(time_interval.users))
    features_sum = time_interval.f_density + time_interval.f_time_weight + time_interval.f_users_count
    time_interval.total_weight = features_sum / 3


def calculate_total_weight_for_all_intervals(products_list, empirical_distribution_intervals):
    """

    :param products_list: a list of all products to weight their time intervals
    :param empirical_distribution_intervals: a distribution of all created intervals for normalizing
    """
    all_densities = []
    all_time_weights = []
    all_users_counts = []

    for interval in empirical_distribution_intervals:
        all_densities.append(interval.density)
        all_time_weights.append(interval.time_weight)
        all_users_counts.append(len(interval.users))

    densities_cdf = ECDF(all_densities)
    time_weights_cdf = ECDF(all_time_weights)
    users_counts_cdf = ECDF(all_users_counts)

    for product in products_list:
        for interval in product.all_intervals:
            interval.f_density = densities_cdf(interval.density)
            interval.f_time_weight = time_weights_cdf(interval.time_weight)
            interval.f_users_count = users_counts_cdf(len(interval.users))
            features_sum = interval.f_density + interval.f_time_weight + interval.f_users_count
            interval.total_weight = features_sum / 3


def calculate_spamicity_for_one_interval(time_interval, empirical_distribution_CDF_lists):
    """

    :param time_interval: the time interval we want to calculate spamicity for
    :param empirical_distribution_CDF_lists: CDF distribution of all created intervals for normalizing
    """
    # all_pairs_scores_sums = []
    # all_probabilities = []
    # all_total_weights = []
    # for interval in empirical_distribution_intervals:
    #     all_pairs_scores_sums.append(interval.pairs_scores_sum)
    #     all_probabilities.append(interval.probability)
    #     all_total_weights.append(interval.total_weight)
    #
    # pairs_scores_sums_cdf = ECDF(all_pairs_scores_sums)
    # probabilities_cdf = ECDF(all_probabilities)
    # total_weights_cdf = ECDF(all_total_weights)

    time_interval.f_pairs_scores_sum = empirical_distribution_CDF_lists[3](time_interval.pairs_scores_sum)
    time_interval.f_probability = 1 - empirical_distribution_CDF_lists[4](time_interval.probability)  # here, small is spammy!
    time_interval.f_total_weight = empirical_distribution_CDF_lists[5](time_interval.total_weight)
    features_sum = time_interval.f_pairs_scores_sum + time_interval.f_probability + time_interval.f_total_weight
    time_interval.spamicity = features_sum / 3


def calculate_spamicity_for_all_intervals(products_intervals_list, all_intervals, empirical_distribution_CDF_lists):
    """

    :param products_intervals_list: all products with their intervals
    :param all_intervals: all created intervals
    :param empirical_distribution_CDF_lists: CDF distribution of all created intervals for normalizing
    """
    # all_pairs_scores_sums = []
    # all_probabilities = []
    # all_total_weights = []
    # for interval in empirical_distribution_intervals:
    #     all_pairs_scores_sums.append(interval.pairs_scores_sum)
    #     all_probabilities.append(interval.probability)
    #     all_total_weights.append(interval.total_weight)
    #
    # pairs_scores_sums_cdf = ECDF(all_pairs_scores_sums)
    # probabilities_cdf = ECDF(all_probabilities)
    # total_weights_cdf = ECDF(all_total_weights)

    for i in range(len(products_intervals_list)):
        for interval in products_intervals_list[i]:
            interval.f_pairs_scores_sum = empirical_distribution_CDF_lists[3](interval.pairs_scores_sum)
            interval.f_probability = 1 - empirical_distribution_CDF_lists[4](interval.probability)  # here, small is spammy!
            interval.f_total_weight = empirical_distribution_CDF_lists[5](interval.total_weight)
            features_sum = interval.f_pairs_scores_sum + interval.f_probability + interval.f_total_weight
            interval.spamicity = features_sum / 3
            all_intervals.add(interval)


def calculate_interval_probability(product, time_interval):
    """

    :param product: the product that contains the time interval
    :param time_interval: the interval we want to calculate its probability
    """

    data_list = []
    for review in product.reviews:
        data_list.append(review.rate)
    full_hist, full_bin_edges = np.histogram(data_list, bins=[1, 2, 3, 4, 5, 6])  # we add 6 because this function takes the last 2 bins values together in the result

    product_probabilities = []
    for bin in full_hist:
        product_probabilities.append(bin / len(product.reviews))

    interval_list = []
    for review in time_interval.reviews:
        interval_list.append(review.rate)
    interval_hist, interval_bin_edges = np.histogram(interval_list, bins=[1, 2, 3, 4, 5, 6])  # we add 6 because this function takes the last 2 bins values together in the result

    rv = multinomial(len(time_interval.reviews), product_probabilities)
    time_interval.probability = rv.pmf(interval_hist)



