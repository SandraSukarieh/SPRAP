import gc
import timeit
from humanfriendly import format_timespan
from statsmodels.distributions import ECDF

import products_functions
from intervals import scoring_time_intervals_functions, time_intervals_functions, pairs_functions
import general_functions
import printing_to_files_functions


def create_and_score_intervals(products_list, tau):
    """

    :param products_list: all products of the data
    :param tau: maximum width of a created interval
    :return: all_sorted_intervals: all created intervals
             raw_top_ranked_intervals: top ranked intervals before filtering and merging
             top_ranked_intervals: final top ranked intervals after filtering and merging
    """
    intervals_creation_start = timeit.default_timer()
    empirical_distribution_intervals = set()
    print("create time intervals")
    counter = 0
    for product in products_list:
        products_functions.find_first_review(product)
        products_functions.find_last_review(product)
        time_intervals_functions.build_products_time_intervals(product, tau)
        time_intervals_functions.remove_intervals_with_empty_start(product)
        time_intervals_functions.remove_intervals_with_empty_end(product)
        time_intervals_functions.remove_three_star_duplicated_intervals(product)
        time_intervals_functions.give_ids_to_intervals(product)  # we give ids after filtering to prevent sparsity

        print("product_counter = ", counter, end="\r")
        counter += 1

    intervals_creation_end = timeit.default_timer()
    intervals_execution_time_seconds = intervals_creation_end - intervals_creation_start
    print("Creating intervals execution time = ", format_timespan(intervals_execution_time_seconds))
    gc.collect()
    # ----------------------------------------------------------
    print("calculate probabilities and total weight for time intervals")
    start_score = timeit.default_timer()
    for product in products_list:
        for interval in product.up_time_intervals:
            scoring_time_intervals_functions.calculate_interval_density(interval)
            scoring_time_intervals_functions.calculate_interval_time_weight(interval)
            scoring_time_intervals_functions.calculate_interval_probability(product, interval)
            interval.data.clear()  # not used any more
        general_functions.copy_items_to_another_set(product.up_time_intervals, product.all_intervals)

        for interval in product.down_time_intervals:
            scoring_time_intervals_functions.calculate_interval_density(interval)
            scoring_time_intervals_functions.calculate_interval_time_weight(interval)
            scoring_time_intervals_functions.calculate_interval_probability(product, interval)
            interval.data.clear()  # not used any more
        general_functions.copy_items_to_another_set(product.down_time_intervals, product.all_intervals)

        general_functions.copy_items_to_another_set(product.all_intervals, empirical_distribution_intervals)
        time_intervals_functions.merge_sequential_or_overlapped_intervals_for_empirical_distribution(product.all_intervals, products_list, empirical_distribution_intervals)

    print("number of intervals of the empirical dist. = ", len(empirical_distribution_intervals))
    scoring_time_intervals_functions.calculate_total_weight_for_all_intervals(products_list, empirical_distribution_intervals)
    end_score = timeit.default_timer()
    intervals_scoring_time_seconds = end_score - start_score
    print("Calculating probabilities and total weight execution time = ", format_timespan(intervals_scoring_time_seconds))
    # ----------------------------------------------------------
    products_intervals_list = []
    analyzed_intervals = set()
    for product in products_list:
        time_intervals_functions.remove_nearly_empty_intervals(product)  # we only want them in the empirical dist
        product.up_time_intervals.clear()  # not used any more
        product.down_time_intervals.clear()  # not used any more
        if len(product.all_intervals) > 0:
            product_intervals = []
            general_functions.copy_items_to_another_list(product.all_intervals, product_intervals)
            general_functions.copy_items_to_another_set(product.all_intervals, analyzed_intervals)
            products_intervals_list.append(product_intervals)
    gc.collect()
    # ----------------------------------------------------------
    print("create and score all pairs of time intervals")
    start_pairs = timeit.default_timer()
    pairs_functions.score_interval_pairs(products_intervals_list)
    end_pairs = timeit.default_timer()
    execution_time_seconds_pairs = end_pairs - start_pairs
    print("creating intervals pairs execution time = ", format_timespan(execution_time_seconds_pairs))
    # ----------------------------------------------------------
    # update empirical dist
    start_updating = timeit.default_timer()
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
    empirical_distribution_CDF_lists = []
    empirical_distribution_CDF_lists.append(densities_cdf)
    empirical_distribution_CDF_lists.append(time_weights_cdf)
    empirical_distribution_CDF_lists.append(users_counts_cdf)

    empirical_only_intervals = set(empirical_distribution_intervals.difference(analyzed_intervals))
    print("number of extra intervals in empirical dist = ", str(len(empirical_only_intervals)))
    for interval in empirical_only_intervals:
        scoring_time_intervals_functions.calculate_total_weight_for_one_interval(interval,empirical_distribution_CDF_lists)
        pairs_functions.score_interval_pairs_for_merging(interval, products_list)
    empirical_distribution_intervals.clear()
    general_functions.copy_items_to_another_set(empirical_only_intervals, empirical_distribution_intervals)
    general_functions.copy_items_to_another_set(analyzed_intervals, empirical_distribution_intervals)
    analyzed_intervals.clear()
    empirical_only_intervals.clear()
    del analyzed_intervals
    del empirical_only_intervals
    # for interval in empirical_distribution_intervals:
    #     if interval.id == -1:  # a merged interval (pairs score already calculated when created) Wrong as nearly empty intervals don't contain pairs score
    #         scoring_time_intervals_functions.calculate_total_weight_for_one_interval(interval, empirical_distribution_intervals)
    #     else:
    #         for i in range(len(products_intervals_list)):
    #             if interval.product.id == products_intervals_list[i][0].product.id:
    #                 for t in products_intervals_list[i]:
    #                     if interval.id == t.id:
    #                         interval.pairs_scores_sum = t.pairs_scores_sum
    #                         interval.total_weight = t.total_weight
    end_updating = timeit.default_timer()
    execution_time_updating = end_updating - start_updating
    print("updating empirical distribution execution time = ", format_timespan(execution_time_updating))
    # ----------------------------------------------------------
    print("calculate spamicity score for each time interval")
    all_densities.clear()
    all_time_weights.clear()
    all_users_counts.clear()
    empirical_distribution_CDF_lists.clear()
    all_pairs_scores_sums = []
    all_probabilities = []
    all_total_weights = []
    for interval in empirical_distribution_intervals:
        all_densities.append(interval.density)
        all_time_weights.append(interval.time_weight)
        all_users_counts.append(len(interval.users))
        all_pairs_scores_sums.append(interval.pairs_scores_sum)
        all_probabilities.append(interval.probability)
        all_total_weights.append(interval.total_weight)
    densities_cdf = ECDF(all_densities)
    time_weights_cdf = ECDF(all_time_weights)
    users_counts_cdf = ECDF(all_users_counts)
    pairs_scores_sums_cdf = ECDF(all_pairs_scores_sums)
    probabilities_cdf = ECDF(all_probabilities)
    total_weights_cdf = ECDF(all_total_weights)
    empirical_distribution_CDF_lists.append(densities_cdf)
    empirical_distribution_CDF_lists.append(time_weights_cdf)
    empirical_distribution_CDF_lists.append(users_counts_cdf)
    empirical_distribution_CDF_lists.append(pairs_scores_sums_cdf)
    empirical_distribution_CDF_lists.append(probabilities_cdf)
    empirical_distribution_CDF_lists.append(total_weights_cdf)
    all_densities.clear()
    all_time_weights.clear()
    all_users_counts.clear()
    all_pairs_scores_sums.clear()
    all_probabilities.clear()
    all_total_weights.clear()
    all_intervals = set()
    scoring_time_intervals_functions.calculate_spamicity_for_all_intervals(products_intervals_list, all_intervals, empirical_distribution_CDF_lists)
    products_intervals_list.clear()  # not used any more
    for product in products_list:
        products_functions.fill_intervals_with_spamicity(product, all_intervals)
    gc.collect()
    # ----------------------------------------------------------
    print("sort all intervals by spamicity to report campaign candidates")
    all_sorted_intervals = sorted(all_intervals, key=lambda interval: (interval.spamicity, interval.id), reverse=True)
    all_intervals.clear()  # not used any more
    gc.collect()
    print("number of all created intervals = ", len(all_sorted_intervals))
    print("print sorted intervals to text file")
    printing_to_files_functions.print_intervals_to_file(all_sorted_intervals, "intervals_files/sorted_time_intervals.txt")
    # ----------------------------------------------------------
    print("get top ranked intervals-----------------------------------------------------------------------------------")
    temp = set()
    for interval in all_sorted_intervals:
        if time_intervals_functions.is_top_ranked_interval(interval):
            temp.add(interval)
    raw_top_ranked_intervals = sorted(temp, key=lambda interval: (interval.spamicity, interval.id), reverse=True)
    print("number of raw top ranked intervals = ", len(raw_top_ranked_intervals))
    printing_to_files_functions.print_intervals_to_file(raw_top_ranked_intervals, "intervals_files/raw_top_ranked_time_intervals.txt")
    print("remove sub-intervals and merge sequential and overlapped intervals-----------------------------------------")
    filtered_temp = set()
    time_intervals_functions.remove_sub_intervals(raw_top_ranked_intervals, filtered_temp)
    initial_top_ranked_intervals = sorted(filtered_temp, key=lambda interval: (interval.spamicity, interval.id), reverse=True)
    printing_to_files_functions.print_intervals_to_file(initial_top_ranked_intervals, "intervals_files/initial_top_ranked_time_intervals.txt")
    print("number of initial top ranked intervals after filtering = ", len(initial_top_ranked_intervals))
    merged_temp = time_intervals_functions.merge_sequential_or_overlapped_intervals(initial_top_ranked_intervals, tau, products_list, empirical_distribution_CDF_lists)
    top_ranked_intervals = sorted(merged_temp, key=lambda interval: (interval.spamicity, interval.id), reverse=True)
    printing_to_files_functions.print_intervals_to_file(top_ranked_intervals, "results/top_ranked_time_intervals.txt")
    printing_to_files_functions.print_intervals_f_scores_to_file(top_ranked_intervals, "intervals_files/f_measures_top_ranked_intervals.txt")
    printing_to_files_functions.print_intervals_f_scores_to_file(all_sorted_intervals, "intervals_files/f_measures_all_sorted_intervals.txt")
    print("number of final top ranked intervals after merging = ", len(top_ranked_intervals))

    return all_sorted_intervals, raw_top_ranked_intervals, top_ranked_intervals
