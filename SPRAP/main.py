import gc
import timeit
from humanfriendly import format_timespan
import sys
from argparse import ArgumentParser
import os

import products_functions
import printing_to_files_functions
from results_evaluation_functions import evaluate_results
import users_functions

from parsing import parsing, parsing_functions
from intervals import intervals
from groups import groups


if __name__ == "__main__":

    start = timeit.default_timer()

    if not os.path.isdir("results"):
        print("creating a directory for results")
        os.mkdir("results")

    if not os.path.isdir("intervals_files"):
        print("creating a directory for intervals files")
        os.mkdir("intervals_files")

    if not os.path.isdir("groups_files"):
        print("creating a directory for groups files")
        os.mkdir("groups_files")


    def parse_config():
        my_args = ArgumentParser('TimeIntervalsAndGroups')
        my_args.add_argument('-f', '--data_file', dest='data_file', help='Data file full path')
        my_args.add_argument('-t', '--tau', dest='tau', help='Max width of time intervals')
        my_args.add_argument('-sr', '--spam_reviews_file', dest='spam_reviews_file', help='Spam reviews file full path')
        my_args.add_argument('-si', '--spam_intervals_file', dest='spam_intervals_file', help='Spam intervals file full path')
        return my_args.parse_args(sys.argv[1:])

    conf = parse_config()

    # ---------to use for run!---------------
    # data_file = conf.data_file
    # tau = int(conf.tau)
    # if conf.spam_reviews_file is None:
    #     spam_reviews_file = ""
    # else:
    #     spam_reviews_file = conf.spam_reviews_file
    #     spam_intervals_file = conf.spam_intervals_file

    # ---------to use for debug!-------------
    # data_file = "/local/data/sukarieh/software.tsv"
    data_file = "syntheticData"
    tau = 3
    spam_reviews_file = "generated_spam_reviews"
    spam_intervals_file = "generated_spamming_intervals"
    # ----------------------------------------------------------
    # products_dict, users_dict, product_reviews_dict, reviews = parsing.parse_files(data_file)
    products_dict, users_dict, product_reviews_dict, reviews = parsing_functions.build_dictionaries(data_file)
    users_count = len(users_dict)
    products_count = len(products_dict)
    reviews_count = len(reviews)
    print("number of products = " + str(products_count))
    print("number of users = " + str(users_count))
    print("number of reviews = " + str(reviews_count))
    # ----------------------------------------------------------
    print("print the adjacency list of the product_user graph into text file")
    products_functions.print_adj_list_to_file(products_dict)
    print("fill the product objects list")
    products_start = timeit.default_timer()
    products_list = products_functions.build_products(products_dict, product_reviews_dict)
    reviews.clear()  # not used any more
    del reviews
    gc.collect()
    products_end = timeit.default_timer()
    products_execution_time_seconds = products_end - products_start
    print("products objects building execution time = ", format_timespan(products_execution_time_seconds))
    # ----------------------------------------------------------
    all_sorted_intervals, raw_top_ranked_intervals, top_ranked_intervals = intervals.create_and_score_intervals(products_list, tau)
    # ----------------------------------------------------------
    collusion_groups = groups.create_and_score_groups(top_ranked_intervals, all_sorted_intervals, users_dict, product_reviews_dict, tau)
    products_dict.clear()  # not used any more
    del products_dict
    users_dict.clear()   # not used any more
    del users_dict
    gc.collect()
    # ----------------------------------------------------------
    targeted_products = set()
    spamming_reviews = set()
    printing_to_files_functions.print_detected_products_to_file(targeted_products, top_ranked_intervals, collusion_groups, "results/targeted_products.txt")
    printing_to_files_functions.print_detected_reviews_to_file(spamming_reviews, raw_top_ranked_intervals, collusion_groups, "results/spamming_reviews.txt")
    detected_spammers = set()
    temp_users = set()
    users_functions.create_detected_spammers(top_ranked_intervals, all_sorted_intervals, collusion_groups, temp_users)
    detected_spammers = sorted(temp_users, key=lambda spammer: (spammer.spamicity, spammer.id), reverse=True)
    printing_to_files_functions.print_spammers_to_file(detected_spammers, "results/detected_spammers.txt")
    # ----------------------------------------------------------
    # -------------------------- to use with generated synthetic files -------------------------------------------------
    if spam_reviews_file != "":
        evaluate_results(spam_reviews_file, spam_intervals_file, users_count, products_count, reviews_count, top_ranked_intervals, all_sorted_intervals, collusion_groups, raw_top_ranked_intervals, targeted_products, spamming_reviews)
    else:
        print("no passed evaluation file, so there is no evaluation")
    # ----------------------------------------------------------
    print("-----------------------------------------------------------------------------------------------------------")
    stop = timeit.default_timer()
    execution_time_seconds = stop - start
    print("Total execution time = ", format_timespan(execution_time_seconds))
    # ----------------------------------------------------------
    # printing_to_files_functions.print_intervals_sizes(top_ranked_intervals, "top_ranked_intervals_sizes.txt")
    # printing_to_files_functions.print_groups_sizes(collusion_groups, "collusion_groups_sizes.txt")
