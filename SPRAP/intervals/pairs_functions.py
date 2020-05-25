def score_interval_pairs(products_intervals_list):
    """

    :param products_intervals_list: a list of lists to group each intervals by their product and have indices for them
    """
    counter = 0
    for i in range(len(products_intervals_list)):
        for j in range(i+1, len(products_intervals_list)):
            intersection_set = set(products_intervals_list[i][0].product.users.intersection(products_intervals_list[j][0].product.users))
            if len(intersection_set) > 2:
                for n in range(len(products_intervals_list[i])):
                    for m in range(len(products_intervals_list[j])):
                        common_users = set(products_intervals_list[i][n].users.intersection(products_intervals_list[j][m].users))
                        all_users = set(products_intervals_list[i][n].users.union(products_intervals_list[j][m].users))
                        if (len(products_intervals_list[i][n].users) != 0) and (len(products_intervals_list[j][m].users) != 0):
                            common_users_ratio = len(common_users) / len(all_users)
                            if common_users_ratio >= 0.2:
                                products_intervals_list[i][n].pairs_scores_sum += common_users_ratio * products_intervals_list[j][m].total_weight
                                products_intervals_list[i][n].counted_pairs += 1
                                products_intervals_list[i][n].pairs_weights_sum += products_intervals_list[j][m].total_weight
                                products_intervals_list[j][m].pairs_scores_sum += common_users_ratio * products_intervals_list[i][n].total_weight
                                products_intervals_list[j][m].counted_pairs += 1
                                products_intervals_list[j][m].pairs_weights_sum += products_intervals_list[i][n].total_weight
                            else:
                                if is_overlapped_copy(products_intervals_list[i][n], products_intervals_list[j][m]):
                                    products_intervals_list[i][n].pairs_scores_sum += common_users_ratio * products_intervals_list[j][m].total_weight
                                    products_intervals_list[i][n].counted_pairs += 1
                                    products_intervals_list[i][n].pairs_weights_sum += products_intervals_list[j][m].total_weight
                                    products_intervals_list[j][m].pairs_scores_sum += common_users_ratio * products_intervals_list[i][n].total_weight
                                    products_intervals_list[j][m].counted_pairs += 1
                                    products_intervals_list[j][m].pairs_weights_sum += products_intervals_list[i][n].total_weight
                                else:
                                    if products_intervals_list[j][m].start_date > products_intervals_list[i][n].end_date:
                                        delta = products_intervals_list[j][m].start_date - products_intervals_list[i][n].end_date
                                    else:
                                        delta = products_intervals_list[i][n].start_date - products_intervals_list[j][m].end_date
                                    if delta.days <= 90:
                                        products_intervals_list[i][n].pairs_scores_sum += common_users_ratio * products_intervals_list[j][m].total_weight
                                        products_intervals_list[i][n].counted_pairs += 1
                                        products_intervals_list[i][n].pairs_weights_sum += products_intervals_list[j][m].total_weight
                                        products_intervals_list[j][m].pairs_scores_sum += common_users_ratio * products_intervals_list[i][n].total_weight
                                        products_intervals_list[j][m].counted_pairs += 1
                                        products_intervals_list[j][m].pairs_weights_sum += products_intervals_list[i][n].total_weight
        print("product_counter = ", counter, end="\r")
        counter += 1


def is_overlapped_copy(interval1, interval2):  # same as the function in intervals file but I had to rewrite it here to avoid importing cycle
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


def score_interval_pairs_for_merging(time_interval, products_list):
    """
    :param time_interval: the time interval that we want to find all the pairs for
    :param products_list: the list that contains all products of the data
    """
    for product in products_list:
        if product.id != time_interval.product.id:
            intersection_set = set(time_interval.product.users.intersection(product.users))
            if len(intersection_set) > 2:
                for target_interval in product.all_intervals:
                    common_users = set(time_interval.users.intersection(target_interval.users))
                    all_users = set(time_interval.users.union(target_interval.users))
                    if (len(time_interval.users) != 0) and (len(target_interval.users) != 0):
                        common_users_ratio = len(common_users) / len(all_users)
                        if common_users_ratio >= 0.2:
                            time_interval.pairs_scores_sum += common_users_ratio * target_interval.total_weight
                            time_interval.counted_pairs += 1
                            time_interval.pairs_weights_sum += target_interval.total_weight
                        else:
                            if is_overlapped_copy(time_interval, target_interval):
                                time_interval.pairs_scores_sum += common_users_ratio * target_interval.total_weight
                                time_interval.counted_pairs += 1
                                time_interval.pairs_weights_sum += target_interval.total_weight
                            else:
                                if target_interval.start_date > time_interval.end_date:
                                    delta = target_interval.start_date - time_interval.end_date
                                else:
                                    delta = time_interval.start_date - target_interval.end_date
                                if delta.days <= 90:
                                    time_interval.pairs_scores_sum += common_users_ratio * target_interval.total_weight
                                    time_interval.counted_pairs += 1
                                    time_interval.pairs_weights_sum += target_interval.total_weight




