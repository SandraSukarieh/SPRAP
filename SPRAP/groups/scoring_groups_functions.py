from datetime import *
from dateutil import parser
from statsmodels.distributions import ECDF
import pdb

import general_functions


def calculate_group_spamicity_terms(group, tau):
    """

    :param group: the group we want to calculate spamicity terms for
    :param tau: maximum interval width
    """
    calculate_group_density(group)
    calculate_group_sparsity(group)
    calculate_group_time_window(group, tau)
    calculate_group_co_reviewing_ratio(group)


def check_if_connected(group, user, product):
    """

    :param group: the group that contains the user and the product
    :param user: a user member of the group
    :param product: a product member of the group
    :return: True if the user reviewed the product, False otherwise
    """
    for user_products in group.users_products:
        if user_products.id == user:
            if product in user_products.products:
                return True
            else:
                return False


def calculate_group_density(group):
    """

    :param group: the group we want to calculate density for
    """
    dense_products_counter = 0
    mu_d = len(group.users) * 0.5
    for product in group.products:
        counter = 0
        for user in group.users:
            if check_if_connected(group, user, product):
                counter = counter + 1
        if counter >= mu_d:
            dense_products_counter = dense_products_counter + 1

    group.density = dense_products_counter / len(group.products)


def calculate_group_sparsity(group):
    """

    :param group: the group we want to calculate sparsity for
    """
    sparse_products_counter = 0
    mu_s = len(group.users) * 0.2
    for product in group.products:
        counter = 0
        for user in group.users:
            if check_if_connected(group, user, product):
                counter = counter + 1
        if counter <= mu_s:
            sparse_products_counter = sparse_products_counter + 1

    group.sparsity = sparse_products_counter / len(group.products)


def calculate_group_time_window(group, tau):
    """

    :param group: the group we want to calculate time window for
    :param tau: maximum interval width
    """
    max_time_window = 0
    for interval in group.intervals:
        related_reviews = set()
        for review in interval.reviews:
            for user in group.users:
                if user == review.user:
                    related_reviews.add(review)
                    break
        product_time_window = find_product_time_window(related_reviews, tau)
        if product_time_window > max_time_window:
            max_time_window = product_time_window

    for interval in group.redundancy_intervals:
        related_reviews = set()
        for review in interval.reviews:
            for user in group.users:
                if user == review.user:
                    related_reviews.add(review)
                    break
        product_time_window = find_product_time_window(related_reviews, tau)
        if product_time_window > max_time_window:
            max_time_window = product_time_window

    group.time_window = max_time_window


def find_product_time_window(related_reviews, tau):
    """

    :param related_reviews: the reviews of the group related to a specific interval (product)
    :param tau: maximum width of interval
    :return: the calculated time window of the given interval (product)
    """
    earliest_review = datetime.date(parser.parse("2050-12-31"))
    latest_review = datetime.date(parser.parse("1980-01-01"))
    for review in related_reviews:
        if review.date < earliest_review:
            earliest_review = review.date
        if review.date > latest_review:
            latest_review = review.date
    delta = (latest_review - earliest_review).days + 1
    if delta > 28:
        return 0
    else:
        return 1 - (delta / 28)


def calculate_group_co_reviewing_ratio(group):
    """

    :param group: the group we want to calculate co-reviewing ratio for
    """
    co_reviewing_counter = 0

    users_products_list = []
    general_functions.copy_items_to_another_list(group.users_products, users_products_list)

    for i in range(len(users_products_list)):
        j = i + 1
        while j < len(users_products_list):
            intersection = set(users_products_list[i].products.intersection(users_products_list[j].products))
            if len(intersection) > 0:
                co_reviewing_counter += 1
            j += 1

    users_count = len(group.users)
    pairs_count = (users_count * (users_count - 1)) / 2
    if pairs_count != 0:
        group.co_reviewing_ratio = co_reviewing_counter / pairs_count
    else:
        group.co_reviewing_ratio = 0


def calculate_spamicity_for_one_group(group, empirical_distribution_CDF_lists):
    """

    :param group: the group we want to calculate spamicity score for
    :param empirical_distribution_groups: CDF distribution of sampled groups for normalizing
    """

    group.f_density = empirical_distribution_CDF_lists[0](group.density)
    group.f_sparsity = 1 - empirical_distribution_CDF_lists[1](group.f_sparsity)  # here, small is spammy!
    group.f_users_count = empirical_distribution_CDF_lists[2](len(group.users))
    group.f_products_count = empirical_distribution_CDF_lists[3](len(group.forming_products))
    group.f_time_window = empirical_distribution_CDF_lists[4](group.time_window)
    group.f_co_reviewing_ratio = empirical_distribution_CDF_lists[5](group.co_reviewing_ratio)
    features_sum = group.f_density + group.f_sparsity + group.f_users_count + group.f_products_count + group.f_time_window + group.f_co_reviewing_ratio
    calculated_spamicity = features_sum / 6
    group.spamicity = calculated_spamicity


def calculate_spamicity_for_all_groups(initial_groups, empirical_distribution_CDF_lists):
    """

    :param initial_groups: initial created groups for top ranked intervals
    :param empirical_distribution_groups: CDF distribution of sampled groups for normalizing
    """

    for group in initial_groups:
        group.f_density = empirical_distribution_CDF_lists[0](group.density)
        group.f_sparsity = 1 - empirical_distribution_CDF_lists[1](group.f_sparsity)  # here, small is spammy!
        group.f_users_count = empirical_distribution_CDF_lists[2](len(group.users))
        group.f_products_count = empirical_distribution_CDF_lists[3](len(group.forming_products))
        group.f_time_window = empirical_distribution_CDF_lists[4](group.time_window)
        group.f_co_reviewing_ratio = empirical_distribution_CDF_lists[5](group.co_reviewing_ratio)
        features_sum = group.f_density + group.f_sparsity + group.f_users_count + group.f_products_count + group.f_time_window + group.f_co_reviewing_ratio
        group.spamicity = features_sum / 6
