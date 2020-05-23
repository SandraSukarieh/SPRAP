import gc
import timeit
from humanfriendly import format_timespan
import codecs
import json
from statsmodels.distributions import ECDF

import printing_to_files_functions
import general_functions
from groups import groups_functions
from my_classes import SampledGroup


def create_and_score_groups(top_ranked_intervals, all_sorted_intervals, users_dict, product_reviews_dict, tau):
    """

    :param top_ranked_intervals: the reported intervals as spamming campaigns
    :param all_sorted_intervals: all created valid intervals of all products
    :param users_dict: dictionary that contains the reviews of each user
    :param product_reviews_dict: dictionary with the reviews of each product
    :param tau: maximum interval width
    :return: created collusion groups after merging and scoring
    """
    print("parsing the empirical distribution groups---------------------------------------------------------")
    empirical_distribution_groups = set()
    with codecs.open("group_objects.json", 'r', "utf-8") as fp:
        groups_objects = json.load(fp)
        for group_object in groups_objects:
            sampled_group = SampledGroup()
            sampled_group.users_count = groups_objects[group_object]['users']
            sampled_group.products_count = groups_objects[group_object]['products']
            sampled_group.intervals_count = groups_objects[group_object]['intervals']
            sampled_group.forming_products_count = groups_objects[group_object]['forming_products']
            sampled_group.density = groups_objects[group_object]['density']
            sampled_group.sparsity = groups_objects[group_object]['sparsity']
            sampled_group.time_window = groups_objects[group_object]['time_window']
            sampled_group.co_reviewing_ratio = groups_objects[group_object]['co_reviewing_ratio']
            empirical_distribution_groups.add(sampled_group)

    all_densities = []
    all_sparsities = []
    all_users_counts = []
    all_products_counts = []
    all_time_windows = []
    all_co_reviewing_ratios = []
    for group in empirical_distribution_groups:
        all_densities.append(group.density)
        all_sparsities.append(group.sparsity)
        all_users_counts.append(group.users_count)
        all_products_counts.append(group.forming_products_count)
        all_time_windows.append(group.time_window)
        all_co_reviewing_ratios.append(group.co_reviewing_ratio)

    densities_cdf = ECDF(all_densities)
    sparsities_cdf = ECDF(all_sparsities)
    users_counts_cdf = ECDF(all_users_counts)
    products_counts_cdf = ECDF(all_products_counts)
    time_windows_cdf = ECDF(all_time_windows)
    co_reviewing_ratios_cdf = ECDF(all_co_reviewing_ratios)

    empirical_distribution_CDF_lists = []
    empirical_distribution_CDF_lists.append(densities_cdf)
    empirical_distribution_CDF_lists.append(sparsities_cdf)
    empirical_distribution_CDF_lists.append(users_counts_cdf)
    empirical_distribution_CDF_lists.append(products_counts_cdf)
    empirical_distribution_CDF_lists.append(time_windows_cdf)
    empirical_distribution_CDF_lists.append(co_reviewing_ratios_cdf)

    empirical_distribution_groups.clear()
    del empirical_distribution_groups
    gc.collect()

    start_groups = timeit.default_timer()
    temp_initial = groups_functions.create_initial_groups(top_ranked_intervals, users_dict, tau, empirical_distribution_CDF_lists)
    initial_groups = sorted(temp_initial, key=lambda group: (
    group.spamicity, len(group.intervals), len(group.redundancy_intervals), len(group.users), group.id), reverse=True)
    printing_to_files_functions.print_groups_to_file(initial_groups, "groups_files/initial_groups.txt")
    end_groups = timeit.default_timer()
    execution_time_seconds_groups = end_groups - start_groups
    print("creating initial groups execution time = ", format_timespan(execution_time_seconds_groups))
    initial_users = set()
    for group in initial_groups:
        general_functions.copy_items_to_another_set(group.users, initial_users)
    # ----------------------------------------------------------
    print("refine initial spamming groups candidates------------------------------------------------------------------")
    start_groups = timeit.default_timer()
    temp_refined = groups_functions.refine_initial_groups(initial_groups, users_dict, tau, top_ranked_intervals,
                                                          all_sorted_intervals, empirical_distribution_CDF_lists)
    refined_groups = sorted(temp_refined, key=lambda group: (
    group.spamicity, len(group.intervals), len(group.redundancy_intervals), len(group.users), group.id), reverse=True)
    end_groups = timeit.default_timer()
    execution_time_seconds_groups = end_groups - start_groups
    print("refining initial groups execution time = ", format_timespan(execution_time_seconds_groups))
    print("number of refined initial groups = ", len(refined_groups))
    printing_to_files_functions.print_groups_to_file(refined_groups, "groups_files/refined_groups.txt")
    refined_users = set()
    for group in refined_groups:
        general_functions.copy_items_to_another_set(group.users, refined_users)
    print("number of users before refining = ", len(initial_users))
    print("number of users after refining = ", len(refined_users))
    # ----------------------------------------------------------
    print("remove sub or equal groups from initial groups and sort them based on spamicity----------------------------")
    temp_g = groups_functions.remove_sub_or_equal_groups(refined_groups)
    filtered_refined_groups = sorted(temp_g, key=lambda group: (
        group.spamicity, len(group.intervals), len(group.redundancy_intervals), len(group.users), group.id),
                                     reverse=True)
    printing_to_files_functions.print_groups_to_file(filtered_refined_groups,
                                                     "groups_files/filtered_refined_groups.txt")
    print("number of FILTERED refined groups = ", len(filtered_refined_groups))
    # ----------------------------------------------------------
    print("create collusion spamming groups candidates----------------------------------------------------------------")
    start_groups = timeit.default_timer()
    temp_cg = groups_functions.build_collusion_spamming_groups(filtered_refined_groups, users_dict, tau, empirical_distribution_CDF_lists)
    collusion_groups = sorted(temp_cg, key=lambda group: (
    group.spamicity, len(group.intervals), len(group.redundancy_intervals), len(group.users), group.id), reverse=True)
    end_groups = timeit.default_timer()
    execution_time_seconds_groups = end_groups - start_groups
    print("creating collusion groups execution time = ", format_timespan(execution_time_seconds_groups))
    for group in collusion_groups:
        groups_functions.find_products_co_reviewed_by_all_members(group, product_reviews_dict)
    product_reviews_dict.clear()  # not used any more
    del product_reviews_dict
    gc.collect()
    printing_to_files_functions.print_groups_to_file(collusion_groups, "results/collusion_groups.txt")
    printing_to_files_functions.print_grouped_spammers_to_file(collusion_groups,
                                                               "results/detected_grouped_spammers.txt")
    printing_to_files_functions.print_groups_f_scores_to_file(collusion_groups,
                                                              "groups_files/f_measures_collusion_groups.txt")
    print("number of collusion groups = ", len(collusion_groups))

    return collusion_groups
