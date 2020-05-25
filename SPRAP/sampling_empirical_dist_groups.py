from argparse import ArgumentParser
import sys
from igraph import *
import timeit
from humanfriendly import format_timespan
import random
import numpy as np
from datetime import *
from dateutil import parser
import codecs
import json

from parsing import parsing, parsing_functions
import general_functions
import my_classes
from groups import groups_functions
from groups import scoring_groups_functions


def create_bi_user_product_graph(bi_graph, users_dict, products_dict):
    """

    :param bi_graph: an igraph undirected graph which will be filled here
    :param users_dict: dictionary that contains the reviews of each user
    :param products_dict: dictionary where the key is the product and the values are the users who reviewed this product
    """
    edge_list = []
    for user in users_dict:
        for product in users_dict[user]:
            edge_list.append((user, product))
    for user in users_dict:
        bi_graph.add_vertex(user)
    bi_graph.vs["type"] = 0  # give users' nodes a type 0
    for product in products_dict:
        bi_graph.add_vertex(product)
    bi_graph.add_edges(edge_list)
    for i in range(bi_graph.vcount()):
        if bi_graph.vs[i]["type"] != 0:
            bi_graph.vs[i]["type"] = 1 # give products' nodes a type 1
    print("check if the user-product built graph is bipartite : ", bi_graph.is_bipartite())


def sample_seed_group_randomly(users_graph, group_size):
    """

    :param users_graph: user-user co-reviewing graph
    :param group_size: members count of sampled group
    :return: sampled group
    """
    group = set()
    last_added_user = (random.sample(list(users_graph.vs), 1).pop(0)).index
    group.add(last_added_user)
    i = 1
    candidates = set()
    while i < group_size:
        general_functions.copy_items_to_another_set(find_candidates_for_one_user(users_graph, last_added_user, group), candidates)
        if not candidates:
            return group
        last_added_user = random.sample(candidates, 1).pop(0)
        group.add(last_added_user)
        candidates.remove(last_added_user)
        i += 1
    return group


def find_candidates_for_one_user(users_graph, user, group):
    """

    :param users_graph: user-user co-reviewing graph
    :param user: the user we want to find his neighbors
    :param group: current group
    :return: a set of candidates of the user neighbors
    """
    candidates = set()
    neighbors_ids = users_graph.neighbors(user)
    for neighbor in neighbors_ids:
        if neighbor not in group:
            candidates.add(neighbor)
    return candidates


def find_candidates(users_graph, group, connected):
    """

    :param users_graph: user-user co-reviewing graph
    :param group: current group
    :param connected: boolean, if True then take the union, else take the intersection
    :return: a set of candidates of memebers neighbors
    """
    candidates = set()
    if connected:
        for member in group:
            neighbors_ids = users_graph.neighbors(member)
            for neighbor in neighbors_ids:
                if neighbor not in group:
                    candidates.add(neighbor)
    else:
        temp = []
        for member in group:
            temp.append(users_graph.neighbors(member))
        intersection_set = set.intersection(*map(set, temp))
        for neighbor in intersection_set:
            if neighbor not in group:
                candidates.add(neighbor)
    return candidates


def sample_neighbor_group(users_graph, current_group):
    """

    :param users_graph: user-user co-reviewing graph
    :param current_group: the current state
    :return: the next state which is a neighbor valid group
    """
    next_states = create_next_states(users_graph, current_group)
    current_group_degree = len(next_states)
    print("current_state_degree = "+str(current_group_degree))
    moving_probabilities_sum = 0
    next_state_probabilities = []
    for state in next_states:
        state_next_states = create_next_states(users_graph, state)
        state_degree = len(state_next_states)
        moving_probability = np.minimum(1/current_group_degree, 1/state_degree)
        next_state_probabilities.append(moving_probability)
        moving_probabilities_sum += moving_probability
    next_states.append(current_group)
    next_state_probabilities.append(1 - moving_probabilities_sum)
    next_selected_state = np.random.choice(next_states, p=next_state_probabilities)
    return next_selected_state


def create_next_states(users_graph, current_group):
    """

    :param users_graph: user-user co-reviewing graph 
    :param current_group: the current state
    :return: all possible next states
    """
    next_states = []
    for member in current_group:
        temp = {member}
        next_possibility_base = set(current_group.difference(temp))
        if check_if_valid(users_graph, next_possibility_base):  # base is connected so we take all candidates
            candidates = find_candidates(users_graph, next_possibility_base, True)
        else:  # base is not connected anymore so we take the intersection of the candidates
            candidates = find_candidates(users_graph, next_possibility_base, False)
        if member in candidates:
            candidates.remove(member)
        if candidates:
            for candidate in candidates:
                temp_2 = {candidate}
                next_possibility = set(next_possibility_base.union(temp_2))
                next_states.append(next_possibility)
    return next_states


def check_if_valid(users_graph, state):
    """

    :param users_graph: user-user co-reviewing graph 
    :param state: the state we want to check if it's valid
    :return: True if the next state is valid, False otherwise
    """
    state_list = list(state)
    for i in range(len(state_list)):
        valid = False
        for j in range(len(state_list)):
            if i != j:
                if users_graph.are_connected(state_list[i], state_list[j]):
                    valid = True
                    break
        if not valid:
            return False
    return True


def find_names_of_groups(groups_ids, users_graph):
    """

    :param groups_ids: the ids of nodes of sampled groups
    :param users_graph: user-user co-reviewing graph 
    :return: the sampled groups with the names of the members
    """
    groups = []
    for group_id in groups_ids:
        group = set()
        for id in group_id:
            group.add(users_graph.vs[id]["name"])
        groups.append(group)
    return groups


def split_reviews(related_reviews):
    """

    :param related_reviews: the set of reviews we want to split
    :return: a set for up-voting reviews, and a set of down-voting ones
    """
    up_reviews = set()
    down_reviews = set()
    for review in related_reviews:
        if review.rate == 1 or review.rate == 2:
            down_reviews.add(review)
        elif review.rate == 4 or review.rate == 5:
            up_reviews.add(review)
        else:
            up_reviews.add(review)
            down_reviews.add(review)
    return up_reviews, down_reviews


def find_first_review(reviews):
    """

    :param reviews: a set of reviews
    :return: the date of first review in the set
    """
    first_review = datetime.date(parser.parse("2050-12-31"))
    for review in reviews:
        if review.date < first_review:
            first_review = review.date
    return first_review


def find_last_review(reviews):
    """

   :param reviews: a set of reviews
   :return: the date of last review in the set
   """

    last_review = datetime.date(parser.parse("1980-01-01"))
    for review in reviews:
        if review.date > last_review:
            last_review = review.date
    return last_review


def filter_intervals(intervals):
    """

    :param intervals: a set of intervals we want to filter
    """
    intervals_list = []
    general_functions.copy_items_to_another_list(intervals, intervals_list)
    for i in range(len(intervals_list) - 1, -1, -1):
        if len(intervals_list[i].users) < 2:  # we don't want an interval with 1 user!
            del intervals_list[i]
        # elif len(intervals_list[i].users) < my_classes.Thresholds.reviews_threshold:
        #     del intervals_list[i]
    for i in range(len(intervals_list) - 1, -1, -1):
        found = False
        for review in intervals_list[i].reviews:
            if review.date == intervals_list[i].start_date:
                found = True
                break
        if not found:
            del intervals_list[i]
    for i in range(len(intervals_list) - 1, -1, -1):
        found = False
        for review in intervals_list[i].reviews:
            if review.date == intervals_list[i].end_date:
                found = True
                break
        if not found:
            del intervals_list[i]
    intervals.clear()
    general_functions.copy_items_to_another_set(intervals_list, intervals)


def build_intervals(product, reviews, tau, flag):
    """

    :param product: the product we want to build its intervals
    :param reviews: the reviews of created intervals
    :param tau: maximum interval width
    :param flag: True if reviews are up-voting, False otherwise
    :return: a set of created intervals
    """
    intervals = set()

    first_review = find_first_review(reviews)
    last_review = find_last_review(reviews)
    time_range = (last_review - first_review).days

    checked_date = first_review - timedelta(days=1)  # in the loop, it will increase and becomes = first date
    days_reviews_list = []

    for i in range(0, time_range + 1):
        checked_date += timedelta(days=1)
        current_date = my_classes.DaysReviewsRecord(checked_date)
        for review in reviews:
            if review.date == checked_date:
                current_date.reviews.append(review)
        days_reviews_list.append(current_date)

    for width in range(1, tau + 1):
        for i in range(0, len(days_reviews_list) - width + 1):
            interval = my_classes.TimeInterval()
            interval.product = product
            if not flag:
                interval.up_type = False
            for j in range(i, i + width):
                for review in days_reviews_list[j].reviews:
                    interval.reviews.add(review)
            for review in interval.reviews:
                interval.users.add(review.user)
            interval.start_date = days_reviews_list[i].checked_date
            interval.end_date = days_reviews_list[i + width - 1].checked_date
            intervals.add(interval)

    filter_intervals(intervals)
    return intervals


def find_group_intervals_and_forming_products(group, product_reviews_dict, tau):
    """

    :param group: the group we want to create intervals for
    :param product_reviews_dict: a dictionary with the reviews of each product
    :param tau: maximum interval width
    """
    for product in group.products:
        related_users = set()
        related_reviews = set()
        for user in group.users:
            if scoring_groups_functions.check_if_connected(group, user, product):
                related_users.add(user)
        for review in product_reviews_dict[product]:
            if review.user in related_users:
                related_reviews.add(review)
        up_reviews, down_reviews = split_reviews(related_reviews)
        up_intervals = build_intervals(product, up_reviews, tau, True)
        general_functions.copy_items_to_another_set(up_intervals, group.intervals)
        down_intervals = build_intervals(product, up_reviews, tau, False)
        general_functions.copy_items_to_another_set(down_intervals, group.intervals)
        for interval in group.intervals:
            group.forming_products.add(interval.product)


def build_groups(groups, users_dict, product_reviews_dict, tau):
    """

    :param groups: sampled groups with users ids
    :param users_dict: a dictionary for each user with its reviewed products
    :param product_reviews_dict: a dictionary with the reviews of each product
    :param tau: maximum interval width
    :return: a set of groups objects with created intervals and calculated features
    """
    group_objects = set()
    for group in groups:
        group_object = my_classes.Group()
        general_functions.copy_items_to_another_set(group, group_object.users)
        for user in group_object.users:
            general_functions.copy_items_to_another_set(users_dict[user], group_object.products)
        groups_functions.add_all_users_products_to_group(group_object, users_dict)
        find_group_intervals_and_forming_products(group_object, product_reviews_dict, tau)
        scoring_groups_functions.calculate_group_density(group_object)
        scoring_groups_functions.calculate_group_sparsity(group_object)
        scoring_groups_functions.calculate_group_time_window(group_object, tau)
        scoring_groups_functions.calculate_group_co_reviewing_ratio(group_object)
        group_objects.add(group_object)
    return group_objects


def parse_config():
    my_args = ArgumentParser('TimeIntervalsAndGroups')
    my_args.add_argument('-f', '--data_file', dest='data_file', help='Data file full path')
    my_args.add_argument('-t', '--tau', dest='tau', help='Max width of time intervals')
    my_args.add_argument('-c', '--count', dest='groups_count', help='number of groups to sample')
    my_args.add_argument('-m', '--msize', dest='maximum_size', help='maximum_size_of_a_sampled_group')
    return my_args.parse_args(sys.argv[1:])


conf = parse_config()

# ---------to use for run!---------------
# data_file = conf.data_file
# tau = int(conf.tau)
# groups_count = int(conf.groups_count)
# maximum_group_size = int(conf.maximum_size)
# ---------to use for debug!-------------
tau = 3
data_file = "syntheticData"
groups_count = 40
maximum_size = 15
# ----------------------------------------------------------
products_dict, users_dict, product_reviews_dict, reviews = parsing_functions.build_dictionaries(data_file)
users_count = len(users_dict)
products_count = len(products_dict)
reviews_count = len(reviews)

bi_graph = Graph(directed=False)
create_bi_user_product_graph(bi_graph, users_dict, products_dict)
print("take the projection of the user-product bipartite graph into a user-user graph")
users_graph = bi_graph.bipartite_projection(which=0)
start = timeit.default_timer()
groups = []
while groups_count > 0:
    group_size = random.randint(2, maximum_size)
    current_groups_count = random.randint(1, groups_count)
    while True:
        current_state = sample_seed_group_randomly(users_graph, group_size)
        if len(current_state) == group_size:
            added_group = set()
            general_functions.copy_items_to_another_set(current_state, added_group)
            groups.append(added_group)
            break
    for i in range(1, current_groups_count):
        go_random = np.random.choice(range(0, 2), p=(0.99, 0.01))
        if not go_random:
            next_state = sample_neighbor_group(users_graph, current_state)
            temp = set()
            general_functions.copy_items_to_another_set(next_state, temp)
            groups.append(temp)
            current_state.clear()
            general_functions.copy_items_to_another_set(temp, current_state)
        else:
            current_state.clear()
            while True:
                current_state = sample_seed_group_randomly(users_graph, group_size)
                if len(current_state) == group_size:
                    added_group = set()
                    general_functions.copy_items_to_another_set(current_state, added_group)
                    groups.append(added_group)
                    break
    groups_count -= current_groups_count
    print("groups left = " + str(groups_count))

groups_names = find_names_of_groups(groups, users_graph)

stop = timeit.default_timer()
execution_time_seconds = stop - start
print("Sampling execution time = ", format_timespan(execution_time_seconds))

start = timeit.default_timer()
group_objects = build_groups(groups_names, users_dict, product_reviews_dict, tau)
stop = timeit.default_timer()
execution_time_seconds = stop - start
print("Creating groups objects execution time = ", format_timespan(execution_time_seconds))

grps = {}
counter = 0
for group in group_objects:
    grps[counter] = {'users': len(group.users), 'products': len(group.products), 'intervals': len(group.intervals),
                     'density': group.density, 'sparsity': group.sparsity, 'time_window': group.time_window,
                     'co_reviewing_ratio': group.co_reviewing_ratio,
                     'forming_products': len(group.forming_products)}
    counter += 1

with codecs.open("group_objects.json", 'w') as fp:
    json.dump(grps, fp)
fp.close()










