from datetime import *
import numpy as np
import sys

import general_functions
import my_classes
from intervals import scoring_time_intervals_functions, pairs_functions


def build_products_time_intervals(product, tau):
    """

    :param product: the product that we want to find all its possible up/down-voting intervals
    :param tau: maximum width of interval
    """

    time_range = (product.last_review - product.first_review).days
    up_votes_reviews = []
    down_votes_reviews = []
    checked_date = product.first_review - timedelta(days=1)  # in the loop, it will increase and becomes = first date

    # create the product timeline with reviews of each day
    for i in range(0, time_range + 1):
        checked_date += timedelta(days=1)
        current_date_up = my_classes.DaysReviewsRecord(checked_date)
        current_date_down = my_classes.DaysReviewsRecord(checked_date)
        for review in product.reviews:
            if review.date == checked_date:
                if review.rate == 1 or review.rate == 2:
                    current_date_down.reviews.append(review)
                elif review.rate == 4 or review.rate == 5:
                    current_date_up.reviews.append(review)
                else:
                    current_date_down.reviews.append(review)
                    current_date_up.reviews.append(review)
        up_votes_reviews.append(current_date_up)
        down_votes_reviews.append(current_date_down)

    create_intervals_objects(product, up_votes_reviews, tau, True)
    create_intervals_objects(product, down_votes_reviews, tau, False)


def create_intervals_objects(product, days_reviews_list, tau, flag):
    """

    :param product: the product that we want to find all its possible up/down-voting intervals
    :param days_reviews_list: a list with the reviews of each day of that product
    :param tau: maximum width of interval
    :param flag: True if it's the up-vote intervals case, False otherwise
    """
    for width in range(1, tau+1):

        for i in range(0, len(days_reviews_list) - width + 1):
            interval = my_classes.TimeInterval()
            interval.product = product
            interval.start_date = days_reviews_list[i].checked_date
            interval.width = width
            interval.end_date = days_reviews_list[i+width-1].checked_date
            if not flag:
                interval.up_type = False
            for j in range(i, i+width):
                for review in days_reviews_list[j].reviews:
                    interval.reviews.add(review)
            for review in interval.reviews:
                interval.users.add(review.user)
            if flag:
                time_data_3 = my_classes.TimeData(3)
                time_data_4 = my_classes.TimeData(4)
                time_data_5 = my_classes.TimeData(5)
                for review in interval.reviews:
                    if review.rate == 3:
                        time_data_3.count += 1
                    elif review.rate == 4:
                        time_data_4.count += 1
                    else:
                        time_data_5.count += 1
                interval.data.add(time_data_3)
                interval.data.add(time_data_4)
                interval.data.add(time_data_5)
                product.up_time_intervals.add(interval)
            else:
                time_data_3 = my_classes.TimeData(3)
                time_data_2 = my_classes.TimeData(2)
                time_data_1 = my_classes.TimeData(1)
                for review in interval.reviews:
                    if review.rate == 3:
                        time_data_3.count += 1
                    elif review.rate == 2:
                        time_data_2.count += 1
                    else:
                        time_data_1.count += 1
                interval.data.add(time_data_3)
                interval.data.add(time_data_2)
                interval.data.add(time_data_1)
                product.down_time_intervals.add(interval)


def give_ids_to_intervals(product):
    """

    :param product: the product that we want to give ids to its intervals
    """
    for interval in product.down_time_intervals:
        interval.id = my_classes.IdCounter.interval_counter
        my_classes.IdCounter.interval_counter = my_classes.IdCounter.interval_counter + 1
    for interval in product.up_time_intervals:
        interval.id = my_classes.IdCounter.interval_counter
        my_classes.IdCounter.interval_counter = my_classes.IdCounter.interval_counter + 1


def remove_nearly_empty_intervals(product):
    """

    :param product: the product we want to remove empty intervals from
    """

    intervals_list = []
    general_functions.copy_items_to_another_list(product.all_intervals, intervals_list)
    for i in range(len(intervals_list) - 1, -1, -1):
        if len(intervals_list[i].users) < 2:  # we don't want an interval with 1 user!
            del intervals_list[i]
    product.all_intervals.clear()
    general_functions.copy_items_to_another_set(intervals_list, product.all_intervals)


def remove_intervals_with_empty_start(product):
    """

    :param product: the product we want to remove intervals with empty start from
    """

    down_intervals_list = []
    general_functions.copy_items_to_another_list(product.down_time_intervals, down_intervals_list)
    for i in range(len(down_intervals_list) - 1, -1, -1):
        found = False
        for review in down_intervals_list[i].reviews:
            if review.date == down_intervals_list[i].start_date:
                found = True
                break
        if not found:
            del down_intervals_list[i]
    product.down_time_intervals.clear()
    general_functions.copy_items_to_another_set(down_intervals_list, product.down_time_intervals)

    up_intervals_list = []
    general_functions.copy_items_to_another_list(product.up_time_intervals, up_intervals_list)
    for i in range(len(up_intervals_list) - 1, -1, -1):
        found = False
        for review in up_intervals_list[i].reviews:
            if review.date == up_intervals_list[i].start_date:
                found = True
                break
        if not found:
            del up_intervals_list[i]
    product.up_time_intervals.clear()
    general_functions.copy_items_to_another_set(up_intervals_list, product.up_time_intervals)


def remove_intervals_with_empty_end(product):
    """

    :param product: the product we want to remove intervals with empty end from
    """

    down_intervals_list = []
    general_functions.copy_items_to_another_list(product.down_time_intervals, down_intervals_list)
    for i in range(len(down_intervals_list) - 1, -1, -1):
        found = False
        for review in down_intervals_list[i].reviews:
            if review.date == down_intervals_list[i].end_date:
                found = True
                break
        if not found:
            del down_intervals_list[i]
    product.down_time_intervals.clear()
    general_functions.copy_items_to_another_set(down_intervals_list, product.down_time_intervals)

    up_intervals_list = []
    general_functions.copy_items_to_another_list(product.up_time_intervals, up_intervals_list)
    for i in range(len(up_intervals_list) - 1, -1, -1):
        found = False
        for review in up_intervals_list[i].reviews:
            if review.date == up_intervals_list[i].end_date:
                found = True
                break
        if not found:
            del up_intervals_list[i]
    product.up_time_intervals.clear()
    general_functions.copy_items_to_another_set(up_intervals_list, product.up_time_intervals)


def remove_intervals_with_reviews_less_then_threshold(product):
    """

    :param product: the product we want to remove intervals with reviews less than the threshold from
    """

    down_intervals_list = []
    general_functions.copy_items_to_another_list(product.down_time_intervals, down_intervals_list)
    for i in range(len(down_intervals_list) - 1, -1, -1):
        if len(down_intervals_list[i].users) < my_classes.Thresholds.reviews_threshold:
            del down_intervals_list[i]
    product.down_time_intervals.clear()
    general_functions.copy_items_to_another_set(down_intervals_list, product.down_time_intervals)

    up_intervals_list = []
    general_functions.copy_items_to_another_list(product.up_time_intervals, up_intervals_list)
    for i in range(len(up_intervals_list) - 1, -1, -1):
        if len(up_intervals_list[i].users) < my_classes.Thresholds.reviews_threshold:
            del up_intervals_list[i]
    product.up_time_intervals.clear()
    general_functions.copy_items_to_another_set(up_intervals_list, product.up_time_intervals)


def remove_three_star_duplicated_intervals(product):
    """

    :param product: the product we want to remove three-star duplicated intervals from
    """

    down_intervals_list = []
    general_functions.copy_items_to_another_list(product.down_time_intervals, down_intervals_list)
    for i in range(len(down_intervals_list) - 1, -1, -1):
        if check_if_interval_is_pure_three_stars(down_intervals_list[i]):
            for interval in product.up_time_intervals:
                if check_if_duplicated(down_intervals_list[i], interval):
                    del down_intervals_list[i]
                    break
    product.down_time_intervals.clear()
    general_functions.copy_items_to_another_set(down_intervals_list, product.down_time_intervals)

    up_intervals_list = []
    general_functions.copy_items_to_another_list(product.up_time_intervals, up_intervals_list)
    for i in range(len(up_intervals_list) - 1, -1, -1):
        if check_if_interval_is_pure_three_stars(up_intervals_list[i]):
            for interval in product.down_time_intervals:
                if check_if_duplicated(up_intervals_list[i], interval):
                    del up_intervals_list[i]
                    break
    product.up_time_intervals.clear()
    general_functions.copy_items_to_another_set(up_intervals_list, product.up_time_intervals)


def check_if_interval_is_pure_three_stars(time_interval):
    """

    :param time_interval: the interval we want to check if it only contains 3-star reviews
    :return: True if the interval is a pure 3-star interval, False otherwise
    """
    for review in time_interval.reviews:
        if review.rate > 3:
            return False
    return True


def check_if_duplicated(pure_three_star_interval, opposite_type_mixed_interval):
    """

    :param pure_three_star_interval: the pure 3-star interval that might be a part of another bigger interval
    :param opposite_type_mixed_interval: the other interval that might contain the pure 3-star interval
    :return: True if the pure 3-star interval is a duplicate of a part of the mixed interval, False otherwise.
    """
    if pure_three_star_interval.start_date >= opposite_type_mixed_interval.start_date:
        if pure_three_star_interval.end_date <= opposite_type_mixed_interval.end_date:
            for review in pure_three_star_interval.reviews:
                if review not in opposite_type_mixed_interval.reviews:
                    return False
            return True
        else:
            return False
    else:
        return False


def is_overlapped(interval1, interval2):
    """

    :param interval1: first interval to check
    :param interval2: second interval to check
    :return: True if the two intervals overlap in any order, False otherwise
    """
    if (interval1.end_date >= interval2.start_date) and (interval1.end_date <= interval2.end_date):
        return True
    elif (interval2.end_date >= interval1.start_date) and (interval2.end_date <= interval1.end_date):
        return True
    else:
        return False


def is_sequential(interval1, interval2):
    """

    :param interval1: first interval to check
    :param interval2: second interval to check
    :return: True if the two intervals are sequential, False otherwise
    """
    if (interval1.end_date == interval2.start_date) or (interval2.end_date == interval1.start_date):
        return True
    else:
        return False


def is_sub_interval(interval1, interval2):
    """

    :param interval1: the interval we want to check if it is a sub-interval of interval2
    :param interval2: the interval we want to check if it contains interval1
    :return: True if interval1 is completely contained in interval2
    """
    if (interval1.start_date >= interval2.start_date) and (interval1.end_date <= interval2.end_date):
        if interval1.width < interval2.width:
            return True
        else:
            return False
    else:
        return False


def remove_sub_intervals(raw_top_ranked_intervals, temp):
    """

    :param raw_top_ranked_intervals: the set that we want to remove redundancy from
    :param temp: a temporary set to save results
    """
    removed = False
    raw_top_ranked_intervals_list = list()
    general_functions.copy_items_to_another_list(raw_top_ranked_intervals, raw_top_ranked_intervals_list)
    raw_top_ranked_intervals_list.sort(key=lambda interval: interval.spamicity, reverse=True)
    for i in range(len(raw_top_ranked_intervals_list)):
        j = i+1
        while j < len(raw_top_ranked_intervals_list):
            if raw_top_ranked_intervals_list[i].product.id == raw_top_ranked_intervals_list[j].product.id:
                if raw_top_ranked_intervals_list[i].up_type == raw_top_ranked_intervals_list[j].up_type:  # only remove smaller interval if it's of the same type (up or down)
                    if is_sub_interval(raw_top_ranked_intervals_list[j], raw_top_ranked_intervals_list[i]):
                        if raw_top_ranked_intervals_list[i].spamicity >= raw_top_ranked_intervals_list[j].spamicity:
                            raw_top_ranked_intervals_list.remove(raw_top_ranked_intervals_list[j])
                            removed = True
            if removed:
                j = j - 1
                removed = False
            j += 1
    for interval in raw_top_ranked_intervals_list:
        temp.add(interval)


def merge_sequential_or_overlapped_intervals(initial_top_ranked_intervals, tau, products_list, empirical_distribution_CDF_lists):
    """

    :param initial_top_ranked_intervals: a list of all top-ranked intervals before merging
    :param tau: maximum width of interval
    :param products_list: a list of all products
    :return: the set that will be filled with the merging results
    """
    temp = set()
    products_intervals_dict = dict()
    build_products_intervals_dict(products_intervals_dict, initial_top_ranked_intervals)
    for product in products_intervals_dict:
        products_intervals_dict[product].sort(key=lambda interval: (interval.start_date, interval.spamicity))
        merge_sequential_or_overlapped_intervals_for_product(products_intervals_dict[product], products_list, temp, empirical_distribution_CDF_lists)
    return temp


def build_products_intervals_dict(products_intervals_dict, initial_top_ranked_intervals):
    """

    :param products_intervals_dict: a dictionary for the intervals of each product
    :param initial_top_ranked_intervals: a list of all top-ranked intervals before merging
    """
    for interval in initial_top_ranked_intervals:
        if interval.product.id not in products_intervals_dict:
            products_intervals_dict[interval.product.id] = [interval]
        else:
            products_intervals_dict[interval.product.id].append(interval)


def merge_sequential_or_overlapped_intervals_for_empirical_distribution(intervals_set, products_list, empirical_distribution_intervals):
    """

    :param intervals_set: the intervals set we want to merge items of
    :param empirical_distribution_intervals: a distribution of all created intervals for normalizing
    """
    intervals_list = []
    general_functions.copy_items_to_another_list(intervals_set, intervals_list)
    while True:
        merging_pair = []
        success = check_intervals_for_merge(intervals_list, merging_pair)
        if success:
            merging_result = my_classes.TimeInterval()
            merge_two_intervals(merging_result, merging_pair[0], merging_pair[1])
            scoring_time_intervals_functions.calculate_interval_density(merging_result)
            scoring_time_intervals_functions.calculate_interval_time_weight(merging_result)
            scoring_time_intervals_functions.calculate_interval_probability(merging_result.product, merging_result)
            pairs_functions.score_interval_pairs_for_merging(merging_result, products_list)
            empirical_distribution_intervals.add(merging_result)
            update_intervals_list(intervals_list, merging_result)
        else:
            break


def merge_sequential_or_overlapped_intervals_for_product(product_intervals, products_list, temp, empirical_distribution_CDF_lists):
    """

    :param product_intervals: the intervals of one product as a list
    :param products_list: a list of all products
    :param temp: the set that will be filled with the merging results
    :param empirical_distribution_intervals: a distribution of all created intervals for normalizing
    """
    while True:
        merging_pair = []
        success = check_intervals_for_merge(product_intervals, merging_pair)
        if success:
            merging_result = my_classes.TimeInterval()
            #  we give the id here to avoid giving ids for merged intervals of the empirical distribution
            merging_result.id = my_classes.IdCounter.interval_counter
            my_classes.IdCounter.interval_counter = my_classes.IdCounter.interval_counter + 1
            merge_two_intervals(merging_result, merging_pair[0], merging_pair[1])

            scoring_time_intervals_functions.calculate_interval_density(merging_result)
            scoring_time_intervals_functions.calculate_interval_time_weight(merging_result)
            scoring_time_intervals_functions.calculate_total_weight_for_one_interval(merging_result, empirical_distribution_CDF_lists)
            scoring_time_intervals_functions.calculate_interval_probability(merging_result.product, merging_result)
            pairs_functions.score_interval_pairs_for_merging(merging_result, products_list)
            scoring_time_intervals_functions.calculate_spamicity_for_one_interval(merging_result, empirical_distribution_CDF_lists)
            update_intervals_list(product_intervals, merging_result)
        else:
            break
    backtracking_queue = []
    for interval in product_intervals:
        if is_top_ranked_interval(interval):
            temp.add(interval)
        else:
            backtracking_queue.append(interval)
    if backtracking_queue:
        merged_intervals_backtracking(backtracking_queue, temp)


def check_intervals_for_merge(intervals_list, merging_pair):
    """

    :param intervals_list: the list of all current intervals
    :param merging_pair: the pair to fill with merging candidate
    :return: True if we find a merging candidate, False otherwise
    """
    i = 0
    while i < len(intervals_list):
        j = i+1
        while j < len(intervals_list):
            if intervals_list[i].product.id == intervals_list[j].product.id:
                if intervals_list[i].up_type == intervals_list[j].up_type:  # only merge if it's of the same type (up or down)
                    if is_overlapped(intervals_list[i], intervals_list[j]):
                        merging_pair.append(intervals_list[i])
                        merging_pair.append(intervals_list[j])
                        return True
                    elif is_sequential(intervals_list[i], intervals_list[j]):
                        merging_pair.append(intervals_list[i])
                        merging_pair.append(intervals_list[j])
                        return True
                    elif is_sub_interval(intervals_list[i], intervals_list[j]):
                        merging_pair.append(intervals_list[i])
                        merging_pair.append(intervals_list[j])
                        return True
                    elif is_sub_interval(intervals_list[j], intervals_list[i]):
                        merging_pair.append(intervals_list[i])
                        merging_pair.append(intervals_list[j])
                        return True
            j += 1
        i += 1
    return False


def merge_two_intervals(merging_result, interval1, interval2):
    """

    :param merging_result: the new interval of merging interval1 and interval2
    :param interval1: the first interval to be merged
    :param interval2: the second interval to be merged
    """
    merging_result.product = interval1.product
    merging_result.up_type = interval1.up_type
    if interval1.start_date < interval2.start_date:
        merging_result.start_date = interval1.start_date
    else:
        merging_result.start_date = interval2.start_date
    if interval1.end_date < interval2.end_date:
        merging_result.end_date = interval2.end_date
    else:
        merging_result.end_date = interval1.end_date
    merging_result.width = (merging_result.end_date - merging_result.start_date).days + 1

    temp_users = set(interval1.users.union(interval2.users))
    general_functions.copy_items_to_another_set(temp_users, merging_result.users)

    temp_reviews_ids = set()
    for review in interval1.reviews:
        if review.id not in temp_reviews_ids:
            merging_result.reviews.add(review)
            temp_reviews_ids.add(review.id)  # to prevent redundancy
    for review in interval2.reviews:
        if review.id not in temp_reviews_ids:
            merging_result.reviews.add(review)
            temp_reviews_ids.add(review.id)  # to prevent redundancy

    if merging_result.up_type:
        time_data_3 = my_classes.TimeData(3)
        time_data_4 = my_classes.TimeData(4)
        time_data_5 = my_classes.TimeData(5)

        for review in merging_result.reviews:
            if review.rate == 3:
                time_data_3.count += 1
            elif review.rate == 4:
                time_data_4.count += 1
            else:
                time_data_5.count += 1
        merging_result.data.add(time_data_3)
        merging_result.data.add(time_data_4)
        merging_result.data.add(time_data_5)
    else:
        time_data_3 = my_classes.TimeData(3)
        time_data_2 = my_classes.TimeData(2)
        time_data_1 = my_classes.TimeData(1)
        for review in merging_result.reviews:
            if review.rate == 1:
                time_data_1.count += 1
            elif review.rate == 2:
                time_data_2.count += 1
            else:
                time_data_3.count += 1
        merging_result.data.add(time_data_3)
        merging_result.data.add(time_data_2)
        merging_result.data.add(time_data_1)

    merging_result.parents.append(interval1)
    merging_result.parents.append(interval2)


def update_intervals_list(intervals_list, merging_result):
    """

    :param intervals_list: the list of current time intervals
    :param merging_result: the new interval after merging
    """
    for i in range(len(intervals_list)):
        if merging_result.parents[0].id == intervals_list[i].id:
            del intervals_list[i]
            break

    for i in range(len(intervals_list)):
        if merging_result.parents[1].id == intervals_list[i].id:
            del intervals_list[i]
            break

    intervals_list.append(merging_result)


def merged_intervals_backtracking(backtracking_queue, temp):
    """

    :param backtracking_queue: a list of all merged intervals that needs to be splitted again
    :param temp: the final intervals set that would be returned
    """

    while backtracking_queue:
        current_interval = backtracking_queue.pop(0)
        if is_top_ranked_interval(current_interval.parents[0]):
            temp.add(current_interval.parents[0])
        else:
            backtracking_queue.append(current_interval.parents[0])
        if is_top_ranked_interval(current_interval.parents[1]):
            temp.add(current_interval.parents[1])
        else:
            backtracking_queue.append(current_interval.parents[1])


def is_top_ranked_interval(interval):
    """

    :param interval: the interval we want to check whether it should be reported or not
    :return: True if the interval should be reported as top-ranked interval, False otherwise
    """
    
    if interval.pairs_scores_sum == 0 or interval.probability == 1 or interval.total_weight == 0:
        return False

    if interval.spamicity >= my_classes.Thresholds.top_ranked_intervals_threshold:
        return True
    else:
        return False







