import my_classes
from groups import scoring_groups_functions
import general_functions
from users_functions import get_sorted_users_by_least_spamicity


def create_initial_groups(top_ranked_intervals, users_dict, tau, empirical_distribution_lists):
    """

    :param top_ranked_intervals: final reported spammy intervals
    :param users_dict: a dictionary for each user with its reviewed products
    :param tau: maximum interval width
    :return: initial created groups of top ranked intervals
    """
    temp_initial = set()
    initial_groups_interval_counter = 0
    for interval in top_ranked_intervals:
        g = my_classes.Group()
        g.id = my_classes.IdCounter.group_counter
        my_classes.IdCounter.group_counter += 1
        g.users = interval.users
        add_all_users_products_to_group(g, users_dict)
        g.intervals.add(interval)
        g.forming_products.add(interval.product)
        scoring_groups_functions.calculate_group_spamicity_terms(g, tau)
        temp_initial.add(g)
        print("top ranked interval counter = ", initial_groups_interval_counter, end="\r")
        initial_groups_interval_counter += 1

    if temp_initial:
        scoring_groups_functions.calculate_spamicity_for_all_groups(temp_initial, empirical_distribution_lists)
    return temp_initial


def add_all_users_products_to_group(group, users_dict):
    """

    :param group: the group we want to fill its user_products set
    :param users_dict: dictionary that contains the products each user reviewed
    """
    for user in group.users:
        user_products = my_classes.UserProducts()
        user_products.id = user
        for product in users_dict[user]:
            user_products.products.add(product)
            group.products.add(product)
        group.users_products.add(user_products)


def refine_initial_groups(initial_groups, users_dict, tau, top_ranked_intervals, all_sorted_intervals, empirical_distribution_lists):
    """

    :param initial_groups: initial groups created for top ranked intervals
    :param users_dict: a dictionary for each user with its reviewed products
    :param tau: maximum interval width
    :param top_ranked_intervals: final reported spammy intervals
    :param all_sorted_intervals: all created intervals
    :return: refined groups after removing non spammy users
    """
    temp_refined = set()
    for group in initial_groups:
        refine_group(temp_refined, group, users_dict, tau, top_ranked_intervals, all_sorted_intervals, empirical_distribution_lists)
    return temp_refined


def refine_group(temp_refined, group, users_dict, tau, top_ranked_intervals, all_sorted_intervals, empirical_distribution_lists):
    """

    :param temp_refined: a set to add the result of refined group
    :param group: the group to refine
    :param users_dict: a dictionary for each user with its reviewed products
    :param tau: maximum interval width
    :param top_ranked_intervals: final reported spammy intervals
    :param all_sorted_intervals: all created intervals
    """
    kicked_out = set()
    n = len(group.users)
    sorted_users = get_sorted_users_by_least_spamicity(group.users, top_ranked_intervals, all_sorted_intervals)
    while n > 3:
        # least_spammy_user = get_least_spammy_user(top_ranked_intervals, group.users, all_sorted_intervals)
        least_spammy_user = sorted_users.pop()[0]
        g1 = my_classes.Group()
        g1.id = my_classes.IdCounter.group_counter
        my_classes.IdCounter.group_counter += 1
        general_functions.copy_items_to_another_set(group.users, g1.users)
        g1.users.remove(least_spammy_user)
        add_all_users_products_to_group(g1, users_dict)
        general_functions.copy_items_to_another_set(group.intervals, g1.intervals)
        general_functions.copy_items_to_another_set(group.forming_products, g1.forming_products)
        scoring_groups_functions.calculate_group_spamicity_terms(g1, tau)
        scoring_groups_functions.calculate_spamicity_for_one_group(g1, empirical_distribution_lists)
        if g1.spamicity >= group.spamicity:
            kicked_out.add(least_spammy_user)
            group = g1
            n = n - 1
        else:
            break
    if (group.spamicity >= my_classes.Thresholds.collusion_spamming_groups_threshold) and (len(group.users) >= 3):
        temp_refined.add(group)
    while len(kicked_out) > 2:
        deal_with_kicked_out_set(temp_refined, kicked_out, group, users_dict, tau, top_ranked_intervals, all_sorted_intervals, empirical_distribution_lists)


def deal_with_kicked_out_set(temp_refined, kicked_out, original_group, users_dict, tau, top_ranked_intervals, all_sorted_intervals, empirical_distribution_lists):
    """

    :param temp_refined: a set to add the result of refined group
    :param kicked_out: a set of removed users while refining groups
    :param original_group: the group that was refined and had some users removed from
    :param users_dict: a dictionary for each user with its reviewed products
    :param tau: maximum interval width
    :param top_ranked_intervals: final reported spammy intervals
    :param all_sorted_intervals: all created intervals
    """
    group = my_classes.Group()
    group.id = my_classes.IdCounter.group_counter
    my_classes.IdCounter.group_counter += 1
    general_functions.copy_items_to_another_set(kicked_out, group.users)
    kicked_out.clear()
    n = len(group.users)
    add_all_users_products_to_group(group, users_dict)
    general_functions.copy_items_to_another_set(original_group.intervals, group.intervals)
    general_functions.copy_items_to_another_set(original_group.forming_products, group.forming_products)
    scoring_groups_functions.calculate_group_spamicity_terms(group, tau)
    scoring_groups_functions.calculate_spamicity_for_one_group(group, empirical_distribution_lists)
    sorted_users = get_sorted_users_by_least_spamicity(group.users, top_ranked_intervals, all_sorted_intervals)
    while n > 3:
        # least_spammy_user = get_least_spammy_user(top_ranked_intervals, group.users, all_sorted_intervals)
        least_spammy_user = sorted_users.pop()[0]
        g1 = my_classes.Group()
        g1.id = my_classes.IdCounter.group_counter
        my_classes.IdCounter.group_counter += 1
        g1.users = group.users.difference(least_spammy_user)
        add_all_users_products_to_group(g1, users_dict)
        general_functions.copy_items_to_another_set(group.intervals, g1.intervals)
        general_functions.copy_items_to_another_set(group.forming_products, g1.forming_products)
        scoring_groups_functions.calculate_group_spamicity_terms(g1, tau)
        scoring_groups_functions.calculate_spamicity_for_one_group(g1, empirical_distribution_lists)
        if g1.spamicity > group.spamicity:
            kicked_out.add(least_spammy_user)
            group = g1
            n = n - 1
        else:
            break
    if (group.spamicity >= my_classes.Thresholds.collusion_spamming_groups_threshold) and (len(group.users) >= 3):
        temp_refined.add(group)


def remove_sub_or_equal_groups(groups_set):
    """

    :param groups_set:  the set that we want to remove redundancy from
    :param temp_g: a temporary set to save results
    """
    temp_g = set()
    removed = False
    raw_initial_groups_list = list()
    general_functions.copy_items_to_another_list(groups_set, raw_initial_groups_list)
    raw_initial_groups_list.sort(key=lambda group: group.spamicity, reverse=True)
    for i in range(len(raw_initial_groups_list)):
        j = i + 1
        while j < len(raw_initial_groups_list):
            if is_same_users(raw_initial_groups_list[j], raw_initial_groups_list[i]):
                if raw_initial_groups_list[i].spamicity >= raw_initial_groups_list[j].spamicity:
                    general_functions.copy_items_to_another_set(raw_initial_groups_list[j].products, raw_initial_groups_list[i].products)
                    general_functions.copy_items_to_another_set(raw_initial_groups_list[j].intervals, raw_initial_groups_list[i].redundancy_intervals)
                    general_functions.copy_items_to_another_set(raw_initial_groups_list[j].additional_products, raw_initial_groups_list[i].additional_products)
                    general_functions.copy_items_to_another_set(raw_initial_groups_list[j].additional_reviews, raw_initial_groups_list[i].additional_reviews)
                    general_functions.copy_items_to_another_set(raw_initial_groups_list[j].forming_products,raw_initial_groups_list[i].forming_products)
                    raw_initial_groups_list.remove(raw_initial_groups_list[j])
                    removed = True
                else:
                    general_functions.copy_items_to_another_set(raw_initial_groups_list[i].products, raw_initial_groups_list[j].products)
                    general_functions.copy_items_to_another_set(raw_initial_groups_list[i].intervals, raw_initial_groups_list[j].redundancy_intervals)
                    general_functions.copy_items_to_another_set(raw_initial_groups_list[i].additional_products,raw_initial_groups_list[j].additional_products)
                    general_functions.copy_items_to_another_set(raw_initial_groups_list[i].additional_reviews,raw_initial_groups_list[j].additional_reviews)
                    general_functions.copy_items_to_another_set(raw_initial_groups_list[i].forming_products,raw_initial_groups_list[j].forming_products)
                    raw_initial_groups_list.remove(raw_initial_groups_list[i])
                    removed = True
            if removed:
                j = j - 1
                removed = False
            j += 1
    general_functions.copy_items_to_another_set(raw_initial_groups_list, temp_g)

    return temp_g


def is_same_users(group1, group2):
    """

    :param group1: the first group we want to check
    :param group2: the second group we want to check
    :return: True if group1 and group2 have the same set of users
    """

    if group1.users == group2.users:
        return True
    else:
        return False


def build_collusion_spamming_groups(filtered_refined_groups, users_dict, tau, empirical_distribution_lists):
    """

    :param filtered_refined_groups: refined groups after removing redundancy
    :param users_dict: a dictionary for each user with its reviewed products
    :param tau: maximum interval width
    :param empirical_distribution_lists: a distribution of sampled groups for normalizing
    :return: collusion groups created after merging filtered refined groups
    """
    temp_cg = set()
    filtered_refined_groups_list = list()
    general_functions.copy_items_to_another_list(filtered_refined_groups, filtered_refined_groups_list)
    filtered_refined_groups_list.sort(key=lambda group: group.spamicity, reverse=True)
    groups_queue = create_groups_queue(filtered_refined_groups_list)
    groups_queue.sort(key=lambda group_tuple: (group_tuple[2], group_tuple[3], group_tuple[0].id, group_tuple[1].id), reverse=True)
    removed_groups = set()
    while groups_queue:
        selected_tuple = groups_queue.pop(0)
        if selected_tuple[2] == 0:  # if the best combining score is 0 then stop merging anything!
            break
        if selected_tuple[0].id not in removed_groups and selected_tuple[1].id not in removed_groups:
            selected_pair = [selected_tuple[0], selected_tuple[1]]
            merging_result = my_classes.Group()
            merge_selected_pair(merging_result, selected_pair, users_dict, tau, empirical_distribution_lists)
            if merging_result.spamicity >= my_classes.Thresholds.collusion_spamming_groups_threshold:
                update_groups_list(filtered_refined_groups_list, selected_pair, merging_result)
                removed_groups.add(selected_pair[0].id)
                removed_groups.add(selected_pair[1].id)
                create_tuples_for_new_group(merging_result, filtered_refined_groups_list, groups_queue)
                groups_queue.sort(key=lambda group_tuple: (group_tuple[2], group_tuple[3], group_tuple[0].id, group_tuple[1].id), reverse=True)

    backtracking_queue = []
    for group in filtered_refined_groups_list:
        if group.spamicity >= my_classes.Thresholds.collusion_spamming_groups_threshold:
            temp_cg.add(group)
        else:
            backtracking_queue.append(group)
            print("added to backtrack so something is wrong")
    if backtracking_queue:
        merged_groups_backtracking(backtracking_queue, temp_cg)

    groups_list = []
    general_functions.copy_items_to_another_list(temp_cg, groups_list)
    if merge_subgroups(groups_list, users_dict, tau, empirical_distribution_lists):
        temp_cg.clear()
        backtracking_queue = []
        for group in groups_list:
            if group.spamicity >= my_classes.Thresholds.collusion_spamming_groups_threshold:
                temp_cg.add(group)
            else:
                backtracking_queue.append(group)
        if backtracking_queue:
            merged_groups_backtracking(backtracking_queue, temp_cg)

    return temp_cg


def create_groups_queue(filtered_refined_groups_list):
    """

    :param filtered_refined_groups_list: the set of filtered initial groups created in previous step
    :return: a queue with all created tuples of merging candidates
    """
    groups_queue = []
    for i in range(len(filtered_refined_groups_list)):
        j = i + 1
        while j < len(filtered_refined_groups_list):
            combining_score = calculate_combining_score(filtered_refined_groups_list[i], filtered_refined_groups_list[j])
            if combining_score >= 0.05:
                total_users_set = set(filtered_refined_groups_list[i].users.union(filtered_refined_groups_list[j].users))
                groups_tuple = [filtered_refined_groups_list[i], filtered_refined_groups_list[j], combining_score, len(total_users_set)]
                groups_queue.append(groups_tuple)
            j = j + 1
    return groups_queue


def calculate_combining_score(group1, group2):
    """

    :param group1: the first group of the pair
    :param group2: the second group of the pair
    :return: a combining score calculating the rate of common users between the two groups
    """
    combining_score = 0
    intersection_set = set(group1.users.intersection(group2.users))
    union_set = set(group1.users.union(group2.users))
    if len(union_set) != 0:
        combining_score = len(intersection_set) / len(union_set)
    return combining_score


def merge_selected_pair(merging_result, selected_pair, users_dict, tau, empirical_distribution_lists):
    """

    :param users_dict: dictionary that contains the products each user reviewed
    :param merging_result: the new group after merging the selected pair
    :param selected_pair: the selected pair to merge
    :param tau: maximum width of interval
    :param empirical_distribution_lists: a distribution of sampled groups for normalizing
    """
    merging_result.id = my_classes.IdCounter.group_counter
    my_classes.IdCounter.group_counter += 1
    merging_result.users = set(selected_pair[0].users.union(selected_pair[1].users))
    merging_result.products = set(selected_pair[0].products.union(selected_pair[1].products))
    add_all_users_products_to_group(merging_result, users_dict)
    merging_result.intervals = set(selected_pair[0].intervals.union(selected_pair[1].intervals))
    merging_result.redundancy_intervals = set(selected_pair[0].redundancy_intervals.union(selected_pair[1].redundancy_intervals))
    merging_result.parents.append(selected_pair[0])
    merging_result.parents.append(selected_pair[1])

    merging_result.additional_products = set((selected_pair[0].additional_products.union(selected_pair[1].additional_products)))
    merging_result.additional_reviews = set((selected_pair[0].additional_reviews.union(selected_pair[1].additional_reviews)))
    merging_result.forming_products = set((selected_pair[0].forming_products.union(selected_pair[1].forming_products)))

    scoring_groups_functions.calculate_group_spamicity_terms(merging_result, tau)
    scoring_groups_functions.calculate_spamicity_for_one_group(merging_result, empirical_distribution_lists)


def update_groups_list(initial_groups_list, selected_pair, merging_result):
    """

    :param initial_groups_list: the list  of initial groups
    :param selected_pair: a pair that contains the best 2 groups to merge
    :param merging_result: the new group after merging the selected pair
    """

    # finding the first element to remove it
    for i in range(len(initial_groups_list)):
        if selected_pair[0].id == initial_groups_list[i].id:
            del initial_groups_list[i]
            break

    # finding the second element to remove it
    for i in range(len(initial_groups_list)):
        if selected_pair[1].id == initial_groups_list[i].id:
            del initial_groups_list[i]
            break

    initial_groups_list.append(merging_result)


def create_tuples_for_new_group(merging_result, initial_groups_list, groups_queue):
    """

    :param merging_result: the new merged group we want to create tuple for
    :param initial_groups_list: the set of initial groups
    :param groups_queue: a queue with all created tuples of merging candidates
    """
    for group in initial_groups_list:
        if group.id != merging_result.id:
            combining_score = calculate_combining_score(merging_result, group)
            if combining_score >= 0.05:
	            total_users_set = set(merging_result.users.union(group.users))
	            groups_tuple = [merging_result, group, combining_score, len(total_users_set)]
	            groups_queue.append(groups_tuple)


def merged_groups_backtracking(backtracking_queue, temp_cg):
    """

    :param backtracking_queue: a list of all merged groups that needs to be splitted again
    :param temp_cg: the final collusion group set that would be returned
    """

    while backtracking_queue:
        current_group = backtracking_queue.pop(0)
        if current_group.parents[0].spamicity >= my_classes.Thresholds.collusion_spamming_groups_threshold:
            temp_cg.add(current_group.parents[0])
        else:
            backtracking_queue.append(current_group.parents[0])
        if current_group.parents[1].spamicity >= my_classes.Thresholds.collusion_spamming_groups_threshold:
            temp_cg.add(current_group.parents[1])
        else:
            backtracking_queue.append(current_group.parents[1])


def merge_subgroups(groups_list, users_dict, tau, empirical_distribution_lists):
    """

    :param groups_list: a list of all groups
    :param users_dict: dictionary that contains the products each user reviewed
    :param tau: maximum width of interval
    :param empirical_distribution_lists: a distribution of sampled groups for normalizing
    :return: True if something was merged, False otherwise
    """

    merged = False
    for i in range(len(groups_list)):
        j = i+1
        while j < len(groups_list):
            if is_sub_group(groups_list[i], groups_list[j]) or is_sub_group(groups_list[j], groups_list[i]):
                merged = True
                pair = [groups_list[i], groups_list[j]]
                merging_result = my_classes.Group()
                merge_selected_pair(merging_result, pair, users_dict, tau, empirical_distribution_lists)
                update_groups_list(groups_list, pair, merging_result)

            j += 1

    return merged


def is_sub_group(group1, group2):
    """

    :param group1: the group we want to check if it is a sub-group of the second one
    :param group2: the group we want to check if it contains the first one
    :return: True if group1 is contained in group2
    """
    users_difference = set(group2.users.difference(group1.users))
    if not users_difference:
        return True
    else:
        return False


def find_products_co_reviewed_by_all_members(group, product_reviews_dict):
    """

    :param product_reviews_dict: a dictionary with the reviews of each product
    :param group: the group to which we want to find all products that are co-reviewed by all members
    """
    for product in group.products:
        should_be_added = True
        for user in group.users:
            if not scoring_groups_functions.check_if_connected(group, user, product):
                should_be_added = False
                break
        if should_be_added:
            group.additional_products.add(product)

    for product in group.additional_products:
        for review in product_reviews_dict[product]:
            if review.user in group.users:
                group.additional_reviews.add(review)






# import my_classes
# from groups import scoring_groups_functions
# import general_functions
# from users_functions import get_sorted_users_by_least_spamicity
#
#
# def create_initial_groups(top_ranked_intervals, users_dict, tau, empirical_distribution_lists):
#     """
#
#     :param top_ranked_intervals: final reported spammy intervals
#     :param users_dict: a dictionary for each user with its reviewed products
#     :param tau: maximum interval width
#     :return: initial created groups of top ranked intervals
#     """
#     temp_initial = set()
#     initial_groups_interval_counter = 0
#     for interval in top_ranked_intervals:
#         g = my_classes.Group()
#         g.id = my_classes.IdCounter.group_counter
#         my_classes.IdCounter.group_counter += 1
#         g.users = interval.users
#         add_all_users_products_to_group(g, users_dict)
#         g.intervals.add(interval)
#         g.forming_products.add(interval.product)
#         scoring_groups_functions.calculate_group_spamicity_terms(g, tau)
#         temp_initial.add(g)
#         print("top ranked interval counter = ", initial_groups_interval_counter, end="\r")
#         initial_groups_interval_counter += 1
#
#     if temp_initial:
#         scoring_groups_functions.calculate_spamicity_for_all_groups(temp_initial, empirical_distribution_lists)
#     return temp_initial
#
#
# def add_all_users_products_to_group(group, users_dict):
#     """
#
#     :param group: the group we want to fill its user_products set
#     :param users_dict: dictionary that contains the products each user reviewed
#     """
#     for user in group.users:
#         user_products = my_classes.UserProducts()
#         user_products.id = user
#         for product in users_dict[user]:
#             user_products.products.add(product)
#             group.products.add(product)
#         group.users_products.add(user_products)
#
#
# def refine_initial_groups(initial_groups, users_dict, tau, top_ranked_intervals, all_sorted_intervals, empirical_distribution_lists):
#     """
#
#     :param initial_groups: initial groups created for top ranked intervals
#     :param users_dict: a dictionary for each user with its reviewed products
#     :param tau: maximum interval width
#     :param top_ranked_intervals: final reported spammy intervals
#     :param all_sorted_intervals: all created intervals
#     :return: refined groups after removing non spammy users
#     """
#     temp_refined = set()
#     for group in initial_groups:
#         refine_group(temp_refined, group, users_dict, tau, top_ranked_intervals, all_sorted_intervals, empirical_distribution_lists)
#     return temp_refined
#
#
# def refine_group(temp_refined, group, users_dict, tau, top_ranked_intervals, all_sorted_intervals, empirical_distribution_lists):
#     """
#
#     :param temp_refined: a set to add the result of refined group
#     :param group: the group to refine
#     :param users_dict: a dictionary for each user with its reviewed products
#     :param tau: maximum interval width
#     :param top_ranked_intervals: final reported spammy intervals
#     :param all_sorted_intervals: all created intervals
#     """
#     kicked_out = set()
#     n = len(group.users)
#     sorted_users = get_sorted_users_by_least_spamicity(group.users, top_ranked_intervals, all_sorted_intervals)
#     while n > 3:
#         # least_spammy_user = get_least_spammy_user(top_ranked_intervals, group.users, all_sorted_intervals)
#         least_spammy_user = sorted_users.pop()[0]
#         g1 = my_classes.Group()
#         g1.id = my_classes.IdCounter.group_counter
#         my_classes.IdCounter.group_counter += 1
#         general_functions.copy_items_to_another_set(group.users, g1.users)
#         g1.users.remove(least_spammy_user)
#         add_all_users_products_to_group(g1, users_dict)
#         general_functions.copy_items_to_another_set(group.intervals, g1.intervals)
#         general_functions.copy_items_to_another_set(group.forming_products, g1.forming_products)
#         scoring_groups_functions.calculate_group_spamicity_terms(g1, tau)
#         scoring_groups_functions.calculate_spamicity_for_one_group(g1, empirical_distribution_lists)
#         if g1.spamicity >= group.spamicity:
#             kicked_out.add(least_spammy_user)
#             group = g1
#             n = n - 1
#         else:
#             break
#     if (group.spamicity >= my_classes.Thresholds.collusion_spamming_groups_threshold) and (len(group.users) >= 3):
#         temp_refined.add(group)
#     while len(kicked_out) > 2:
#         deal_with_kicked_out_set(temp_refined, kicked_out, group, users_dict, tau, top_ranked_intervals, all_sorted_intervals, empirical_distribution_lists)
#
#
# def deal_with_kicked_out_set(temp_refined, kicked_out, original_group, users_dict, tau, top_ranked_intervals, all_sorted_intervals, empirical_distribution_lists):
#     """
#
#     :param temp_refined: a set to add the result of refined group
#     :param kicked_out: a set of removed users while refining groups
#     :param original_group: the group that was refined and had some users removed from
#     :param users_dict: a dictionary for each user with its reviewed products
#     :param tau: maximum interval width
#     :param top_ranked_intervals: final reported spammy intervals
#     :param all_sorted_intervals: all created intervals
#     """
#     group = my_classes.Group()
#     group.id = my_classes.IdCounter.group_counter
#     my_classes.IdCounter.group_counter += 1
#     general_functions.copy_items_to_another_set(kicked_out, group.users)
#     kicked_out.clear()
#     n = len(group.users)
#     add_all_users_products_to_group(group, users_dict)
#     general_functions.copy_items_to_another_set(original_group.intervals, group.intervals)
#     general_functions.copy_items_to_another_set(original_group.forming_products, group.forming_products)
#     scoring_groups_functions.calculate_group_spamicity_terms(group, tau)
#     scoring_groups_functions.calculate_spamicity_for_one_group(group, empirical_distribution_lists)
#     sorted_users = get_sorted_users_by_least_spamicity(group.users, top_ranked_intervals, all_sorted_intervals)
#     while n > 3:
#         # least_spammy_user = get_least_spammy_user(top_ranked_intervals, group.users, all_sorted_intervals)
#         least_spammy_user = sorted_users.pop()[0]
#         g1 = my_classes.Group()
#         g1.id = my_classes.IdCounter.group_counter
#         my_classes.IdCounter.group_counter += 1
#         g1.users = group.users.difference(least_spammy_user)
#         add_all_users_products_to_group(g1, users_dict)
#         general_functions.copy_items_to_another_set(group.intervals, g1.intervals)
#         general_functions.copy_items_to_another_set(group.forming_products, g1.forming_products)
#         scoring_groups_functions.calculate_group_spamicity_terms(g1, tau)
#         scoring_groups_functions.calculate_spamicity_for_one_group(g1, empirical_distribution_lists)
#         if g1.spamicity > group.spamicity:
#             kicked_out.add(least_spammy_user)
#             group = g1
#             n = n - 1
#         else:
#             break
#     if (group.spamicity >= my_classes.Thresholds.collusion_spamming_groups_threshold) and (len(group.users) >= 3):
#         temp_refined.add(group)
#
#
# def remove_sub_or_equal_groups(groups_set):
#     """
#
#     :param groups_set:  the set that we want to remove redundancy from
#     :param temp_g: a temporary set to save results
#     """
#     temp_g = set()
#     removed = False
#     raw_initial_groups_list = list()
#     general_functions.copy_items_to_another_list(groups_set, raw_initial_groups_list)
#     raw_initial_groups_list.sort(key=lambda group: group.spamicity, reverse=True)
#     for i in range(len(raw_initial_groups_list)):
#         j = i + 1
#         while j < len(raw_initial_groups_list):
#             if is_same_users(raw_initial_groups_list[j], raw_initial_groups_list[i]):
#                 if raw_initial_groups_list[i].spamicity >= raw_initial_groups_list[j].spamicity:
#                     general_functions.copy_items_to_another_set(raw_initial_groups_list[j].products, raw_initial_groups_list[i].products)
#                     general_functions.copy_items_to_another_set(raw_initial_groups_list[j].intervals, raw_initial_groups_list[i].redundancy_intervals)
#                     general_functions.copy_items_to_another_set(raw_initial_groups_list[j].additional_products, raw_initial_groups_list[i].additional_products)
#                     general_functions.copy_items_to_another_set(raw_initial_groups_list[j].additional_reviews, raw_initial_groups_list[i].additional_reviews)
#                     general_functions.copy_items_to_another_set(raw_initial_groups_list[j].forming_products,raw_initial_groups_list[i].forming_products)
#                     raw_initial_groups_list.remove(raw_initial_groups_list[j])
#                     removed = True
#                 else:
#                     general_functions.copy_items_to_another_set(raw_initial_groups_list[i].products, raw_initial_groups_list[j].products)
#                     general_functions.copy_items_to_another_set(raw_initial_groups_list[i].intervals, raw_initial_groups_list[j].redundancy_intervals)
#                     general_functions.copy_items_to_another_set(raw_initial_groups_list[i].additional_products,raw_initial_groups_list[j].additional_products)
#                     general_functions.copy_items_to_another_set(raw_initial_groups_list[i].additional_reviews,raw_initial_groups_list[j].additional_reviews)
#                     general_functions.copy_items_to_another_set(raw_initial_groups_list[i].forming_products,raw_initial_groups_list[j].forming_products)
#                     raw_initial_groups_list.remove(raw_initial_groups_list[i])
#                     removed = True
#             if removed:
#                 j = j - 1
#                 removed = False
#             j += 1
#     general_functions.copy_items_to_another_set(raw_initial_groups_list, temp_g)
#
#     return temp_g
#
#
# def is_same_users(group1, group2):
#     """
#
#     :param group1: the first group we want to check
#     :param group2: the second group we want to check
#     :return: True if group1 and group2 have the same set of users
#     """
#
#     if group1.users == group2.users:
#         return True
#     else:
#         return False
#
#
# def build_collusion_spamming_groups(filtered_refined_groups, users_dict, tau, empirical_distribution_lists):
#     """
#
#     :param filtered_refined_groups: refined groups after removing redundancy
#     :param users_dict: a dictionary for each user with its reviewed products
#     :param tau: maximum interval width
#     :param empirical_distribution_lists: a distribution of sampled groups for normalizing
#     :return: collusion groups created after merging filtered refined groups
#     """
#     temp_cg = set()
#     filtered_refined_groups_list = list()
#     general_functions.copy_items_to_another_list(filtered_refined_groups, filtered_refined_groups_list)
#     filtered_refined_groups_list.sort(key=lambda group: group.spamicity, reverse=True)
#     groups_queue = create_groups_queue(filtered_refined_groups_list)
#     groups_queue.sort(key=lambda group_tuple: (group_tuple[2], group_tuple[3], group_tuple[0].id, group_tuple[1].id), reverse=True)
#     removed_groups = set()
#     while groups_queue:
#         selected_tuple = groups_queue.pop(0)
#         if selected_tuple[2] == 0:  # if the best combining score is 0 then stop merging anything!
#             break
#         if selected_tuple[0].id not in removed_groups and selected_tuple[1].id not in removed_groups:
#             selected_pair = [selected_tuple[0], selected_tuple[1]]
#             merging_result = my_classes.Group()
#             merge_selected_pair(merging_result, selected_pair, users_dict, tau, empirical_distribution_lists)
#             if merging_result.spamicity >= my_classes.Thresholds.collusion_spamming_groups_threshold:
#                 update_groups_list(filtered_refined_groups_list, selected_pair, merging_result)
#                 removed_groups.add(selected_pair[0].id)
#                 removed_groups.add(selected_pair[1].id)
#                 create_tuples_for_new_group(merging_result, filtered_refined_groups_list, groups_queue)
#                 groups_queue.sort(key=lambda group_tuple: (group_tuple[2], group_tuple[3], group_tuple[0].id, group_tuple[1].id), reverse=True)
#
#     backtracking_queue = []
#     for group in filtered_refined_groups_list:
#         if group.spamicity >= my_classes.Thresholds.collusion_spamming_groups_threshold:
#             temp_cg.add(group)
#         else:
#             backtracking_queue.append(group)
#             print("added to backtrack so something is wrong")
#     if backtracking_queue:
#         merged_groups_backtracking(backtracking_queue, temp_cg)
#
#     groups_list = []
#     general_functions.copy_items_to_another_list(temp_cg, groups_list)
#     if merge_subgroups(groups_list, users_dict, tau, empirical_distribution_lists):
#         temp_cg.clear()
#         backtracking_queue = []
#         for group in groups_list:
#             if group.spamicity >= my_classes.Thresholds.collusion_spamming_groups_threshold:
#                 temp_cg.add(group)
#             else:
#                 backtracking_queue.append(group)
#         if backtracking_queue:
#             merged_groups_backtracking(backtracking_queue, temp_cg)
#
#     return temp_cg
#
#
# def create_groups_queue(filtered_refined_groups_list):
#     """
#
#     :param filtered_refined_groups_list: the set of filtered initial groups created in previous step
#     :return: a queue with all created tuples of merging candidates
#     """
#     groups_queue = []
#     for i in range(len(filtered_refined_groups_list)):
#         j = i + 1
#         while j < len(filtered_refined_groups_list):
#             combining_score = calculate_combining_score(filtered_refined_groups_list[i], filtered_refined_groups_list[j])
#             if combining_score >= 0:
#                 total_users_set = set(filtered_refined_groups_list[i].users.union(filtered_refined_groups_list[j].users))
#                 groups_tuple = [filtered_refined_groups_list[i], filtered_refined_groups_list[j], combining_score, len(total_users_set)]
#                 groups_queue.append(groups_tuple)
#             j = j + 1
#     return groups_queue
#
#
# def calculate_combining_score(group1, group2):
#     """
#
#     :param group1: the first group of the pair
#     :param group2: the second group of the pair
#     :return: a combining score calculating the rate of common users between the two groups
#     """
#     combining_score = 0
#     intersection_set = set(group1.users.intersection(group2.users))
#     union_set = set(group1.users.union(group2.users))
#     if len(union_set) != 0:
#         combining_score = len(intersection_set) / len(union_set)
#     return combining_score
#
#
# def merge_selected_pair(merging_result, selected_pair, users_dict, tau, empirical_distribution_lists):
#     """
#
#     :param users_dict: dictionary that contains the products each user reviewed
#     :param merging_result: the new group after merging the selected pair
#     :param selected_pair: the selected pair to merge
#     :param tau: maximum width of interval
#     :param empirical_distribution_lists: a distribution of sampled groups for normalizing
#     """
#     merging_result.id = my_classes.IdCounter.group_counter
#     my_classes.IdCounter.group_counter += 1
#     merging_result.users = set(selected_pair[0].users.union(selected_pair[1].users))
#     merging_result.products = set(selected_pair[0].products.union(selected_pair[1].products))
#     add_all_users_products_to_group(merging_result, users_dict)
#     merging_result.intervals = set(selected_pair[0].intervals.union(selected_pair[1].intervals))
#     merging_result.redundancy_intervals = set(selected_pair[0].redundancy_intervals.union(selected_pair[1].redundancy_intervals))
#     merging_result.parents.append(selected_pair[0])
#     merging_result.parents.append(selected_pair[1])
#
#     merging_result.additional_products = set((selected_pair[0].additional_products.union(selected_pair[1].additional_products)))
#     merging_result.additional_reviews = set((selected_pair[0].additional_reviews.union(selected_pair[1].additional_reviews)))
#     merging_result.forming_products = set((selected_pair[0].forming_products.union(selected_pair[1].forming_products)))
#
#     scoring_groups_functions.calculate_group_spamicity_terms(merging_result, tau)
#     scoring_groups_functions.calculate_spamicity_for_one_group(merging_result, empirical_distribution_lists)
#
#
# def update_groups_list(initial_groups_list, selected_pair, merging_result):
#     """
#
#     :param initial_groups_list: the list  of initial groups
#     :param selected_pair: a pair that contains the best 2 groups to merge
#     :param merging_result: the new group after merging the selected pair
#     """
#
#     # finding the first element to remove it
#     for i in range(len(initial_groups_list)):
#         if selected_pair[0].id == initial_groups_list[i].id:
#             del initial_groups_list[i]
#             break
#
#     # finding the second element to remove it
#     for i in range(len(initial_groups_list)):
#         if selected_pair[1].id == initial_groups_list[i].id:
#             del initial_groups_list[i]
#             break
#
#     initial_groups_list.append(merging_result)
#
#
# def create_tuples_for_new_group(merging_result, initial_groups_list, groups_queue):
#     """
#
#     :param merging_result: the new merged group we want to create tuple for
#     :param initial_groups_list: the set of initial groups
#     :param groups_queue: a queue with all created tuples of merging candidates
#     """
#     for group in initial_groups_list:
#         if group.id != merging_result.id:
#             combining_score = calculate_combining_score(merging_result, group)
#             total_users_set = set(merging_result.users.union(group.users))
#             groups_tuple = [merging_result, group, combining_score, len(total_users_set)]
#             groups_queue.append(groups_tuple)
#
#
# def merged_groups_backtracking(backtracking_queue, temp_cg):
#     """
#
#     :param backtracking_queue: a list of all merged groups that needs to be splitted again
#     :param temp_cg: the final collusion group set that would be returned
#     """
#
#     while backtracking_queue:
#         current_group = backtracking_queue.pop(0)
#         if current_group.parents[0].spamicity >= my_classes.Thresholds.collusion_spamming_groups_threshold:
#             temp_cg.add(current_group.parents[0])
#         else:
#             backtracking_queue.append(current_group.parents[0])
#         if current_group.parents[1].spamicity >= my_classes.Thresholds.collusion_spamming_groups_threshold:
#             temp_cg.add(current_group.parents[1])
#         else:
#             backtracking_queue.append(current_group.parents[1])
#
#
# def merge_subgroups(groups_list, users_dict, tau, empirical_distribution_lists):
#     """
#
#     :param groups_list: a list of all groups
#     :param users_dict: dictionary that contains the products each user reviewed
#     :param tau: maximum width of interval
#     :param empirical_distribution_lists: a distribution of sampled groups for normalizing
#     :return: True if something was merged, False otherwise
#     """
#
#     merged = False
#     for i in range(len(groups_list)):
#         j = i+1
#         while j < len(groups_list):
#             if is_sub_group(groups_list[i], groups_list[j]) or is_sub_group(groups_list[j], groups_list[i]):
#                 merged = True
#                 pair = [groups_list[i], groups_list[j]]
#                 merging_result = my_classes.Group()
#                 merge_selected_pair(merging_result, pair, users_dict, tau, empirical_distribution_lists)
#                 update_groups_list(groups_list, pair, merging_result)
#
#             j += 1
#
#     return merged
#
#
# def is_sub_group(group1, group2):
#     """
#
#     :param group1: the group we want to check if it is a sub-group of the second one
#     :param group2: the group we want to check if it contains the first one
#     :return: True if group1 is contained in group2
#     """
#     users_difference = set(group2.users.difference(group1.users))
#     if not users_difference:
#         return True
#     else:
#         return False
#
#
# def find_products_co_reviewed_by_all_members(group, product_reviews_dict):
#     """
#
#     :param product_reviews_dict: a dictionary with the reviews of each product
#     :param group: the group to which we want to find all products that are co-reviewed by all members
#     """
#     for product in group.products:
#         should_be_added = True
#         for user in group.users:
#             if not scoring_groups_functions.check_if_connected(group, user, product):
#                 should_be_added = False
#                 break
#         if should_be_added:
#             group.additional_products.add(product)
#
#     for product in group.additional_products:
#         for review in product_reviews_dict[product]:
#             if review.user in group.users:
#                 group.additional_reviews.add(review)
