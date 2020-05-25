from intervals.time_intervals_functions import is_sub_interval
from parsing import parsing_functions
from my_classes import EvaluationObject


def evaluate_results(spam_reviews_file, spam_intervals_file, users_count, products_count, reviews_count, top_ranked_intervals, all_sorted_intervals, collusion_groups, raw_top_ranked_intervals, targeted_products, spamming_reviews):
    """

    :param targeted_products: set of all detected targeted products
    :param spamming_reviews: set of all detected spamming reviews
    :param raw_top_ranked_intervals: the reported intervals as spamming campaigns before removing redundancy
    :param spam_reviews_file: file containing the generated spam reviews before parsing
    :param spam_intervals_file: file containing the generated spam intervals before parsing
    :param users_count: number of all users
    :param products_count: number of all products
    :param reviews_count: number of all reviews
    :param top_ranked_intervals: the reported intervals as spamming campaigns
    :param all_sorted_intervals: all created valid intervals of all products
    :param collusion_groups: the reported groups as spamming collusion groups
    """
    print("parse spam reviews file, and interval file, then evaluate results------------------------------------------")
    spam_reviews_list = []
    spam_intervals_list = []
    parsing_functions.parse_spamming_reviews(spam_reviews_list, spam_reviews_file)
    parsing_functions.parse_spamming_intervals(spam_intervals_list, spam_intervals_file)

    reviews_evaluation_object = EvaluationObject()
    evaluate_detected_reviews(reviews_evaluation_object, reviews_count, spamming_reviews, spam_reviews_list)
    print("detected reviews evaluation:")
    print("----------------------------")
    reviews_evaluation_object.print()

    spammers_evaluation_object = EvaluationObject()
    evaluate_detected_spammers(spammers_evaluation_object, users_count, top_ranked_intervals, spam_reviews_list)
    print("detected spammers evaluation:")
    print("-----------------------------")
    spammers_evaluation_object.print()

    grouped_spammers_evaluation_object = EvaluationObject()
    evaluate_detected_grouped_spammers(grouped_spammers_evaluation_object, users_count, collusion_groups, spam_reviews_list)
    print("detected grouped spammers evaluation:")
    print("-----------------------------")
    grouped_spammers_evaluation_object.print()

    products_evaluation_object = EvaluationObject()
    evaluate_detected_products(products_evaluation_object, products_count, spam_reviews_list, targeted_products)
    print("detected targeted products evaluation:")
    print("--------------------------------------")
    products_evaluation_object.print()

    intervals_evaluation_object = EvaluationObject()
    evaluate_detected_intervals(intervals_evaluation_object, raw_top_ranked_intervals, all_sorted_intervals, spam_intervals_list)
    print("detected spamming intervals evaluation:")
    print("--------------------------------------")
    intervals_evaluation_object.print()

    # evaluate_defrauder_output(spam_reviews_list, products_count, users_count)


def evaluate_detected_reviews(reviews_evaluation_object, reviews_count, spamming_reviews, spam_reviews_list):
    """

    :param spamming_reviews: set of all detected spamming reviews
    :param reviews_evaluation_object: object to save results
    :param reviews_count: number of total reviews
    :param spam_reviews_list: true generated spam reviews
    """

    spam_reviews_of_generated_intervals = set()
    for review in spam_reviews_list:
        spam_reviews_of_generated_intervals.add(review.id)
    reported_reviews = set()
    for review in spamming_reviews:
        reported_reviews.add(review)  # this only contains the IDs not the objects

    true_positives_set = set(spam_reviews_of_generated_intervals.intersection(reported_reviews))
    false_positives_set = set(reported_reviews.difference(true_positives_set))

    TP = len(true_positives_set)
    FP = len(false_positives_set)

    false_negatives_set = set(spam_reviews_of_generated_intervals.difference(true_positives_set))

    FN = len(false_negatives_set)

    reviews_evaluation_object.true_positives = TP
    reviews_evaluation_object.false_positives = FP
    reviews_evaluation_object.false_negatives = FN
    TN = reviews_count - TP - FP - FN
    reviews_evaluation_object.true_negatives = TN

    if (TP + FP) > 0:
        reviews_evaluation_object.precision = TP / (TP + FP)
    else:
        reviews_evaluation_object.precision = 0
    if (TP + FN) > 0:
        reviews_evaluation_object.recall = TP / (TP + FN)
    else:
        reviews_evaluation_object.recall = 0
    if (reviews_evaluation_object.precision == 0) and (reviews_evaluation_object.recall == 0):
        reviews_evaluation_object.F1_score = 0
    else:
        reviews_evaluation_object.F1_score = (2 * reviews_evaluation_object.precision * reviews_evaluation_object.recall) / (reviews_evaluation_object.precision + reviews_evaluation_object.recall)

    if TP == 0 and FP == 0 and FN == 0:
        reviews_evaluation_object.precision = 1
        reviews_evaluation_object.recall = 1
        reviews_evaluation_object.F1_score = 1

    reviews_evaluation_object.tpr = reviews_evaluation_object.recall
    if (FP + TN) > 0:
        reviews_evaluation_object.fpr = FP / (FP + TN)
    else:
        reviews_evaluation_object.fpr = 0


def evaluate_detected_spammers(spammers_evaluation_object, users_count, top_ranked_intervals, spam_reviews_list):
    """

    :param spammers_evaluation_object: object to save results
    :param users_count: number of all users
    :param top_ranked_intervals: the reported intervals as spamming campaigns
    :param spam_reviews_list: true generated spam reviews
    """

    detected_spammers = set()
    for interval in top_ranked_intervals:
        for user in interval.users:
            detected_spammers.add(user)
    true_spammers = set()

    for review in spam_reviews_list:
        true_spammers.add(review.user)

    true_positives_set = set(true_spammers.intersection(detected_spammers))
    false_positives_set = set(detected_spammers.difference(true_positives_set))

    TP = len(true_positives_set)
    FP = len(false_positives_set)

    false_negatives_set = set(true_spammers.difference(true_positives_set))

    FN = len(false_negatives_set)

    spammers_evaluation_object.true_positives = TP
    spammers_evaluation_object.false_positives = FP
    spammers_evaluation_object.false_negatives = FN
    TN = users_count - TP - FP - FN
    spammers_evaluation_object.true_negatives = TN

    if (TP + FP) > 0:
        spammers_evaluation_object.precision = TP / (TP + FP)
    else:
        spammers_evaluation_object.precision = 0

    if (TP + FN) > 0:
        spammers_evaluation_object.recall = TP / (TP + FN)
    else:
        spammers_evaluation_object.recall = 0

    if (spammers_evaluation_object.precision == 0) and (spammers_evaluation_object.recall == 0):
        spammers_evaluation_object.F1_score = 0
    else:
        spammers_evaluation_object.F1_score = (2 * spammers_evaluation_object.precision * spammers_evaluation_object.recall) / (spammers_evaluation_object.precision + spammers_evaluation_object.recall)

    if TP == 0 and FP == 0 and FN == 0:
        spammers_evaluation_object.precision = 1
        spammers_evaluation_object.recall = 1
        spammers_evaluation_object.F1_score = 1

    spammers_evaluation_object.tpr = spammers_evaluation_object.recall
    if (FP + TN) > 0:
        spammers_evaluation_object.fpr = FP / (FP + TN)
    else:
        spammers_evaluation_object.fpr = 0


def evaluate_detected_grouped_spammers(grouped_spammers_evaluation_object, users_count, collusion_groups, spam_reviews_list):
    """

    :param grouped_spammers_evaluation_object: object to save results
    :param users_count: number of all users
    :param collusion_groups: reported collusion groups
    :param spam_reviews_list: true generated spam reviews
    """

    detected_spammers = set()
    for group in collusion_groups:
        for user in group.users:
            detected_spammers.add(user)
    true_spammers = set()

    for review in spam_reviews_list:
        true_spammers.add(review.user)

    true_positives_set = set(true_spammers.intersection(detected_spammers))
    false_positives_set = set(detected_spammers.difference(true_positives_set))

    TP = len(true_positives_set)
    FP = len(false_positives_set)

    false_negatives_set = set(true_spammers.difference(true_positives_set))

    FN = len(false_negatives_set)

    grouped_spammers_evaluation_object.true_positives = TP
    grouped_spammers_evaluation_object.false_positives = FP
    grouped_spammers_evaluation_object.false_negatives = FN
    TN = users_count - TP - FP - FN
    grouped_spammers_evaluation_object.true_negatives = TN

    if (TP + FP) > 0:
        grouped_spammers_evaluation_object.precision = TP / (TP + FP)
    else:
        grouped_spammers_evaluation_object.precision = 0

    if (TP + FN) > 0:
        grouped_spammers_evaluation_object.recall = TP / (TP + FN)
    else:
        grouped_spammers_evaluation_object.recall = 0

    if (grouped_spammers_evaluation_object.precision == 0) and (grouped_spammers_evaluation_object.recall == 0):
        grouped_spammers_evaluation_object.F1_score = 0
    else:
        grouped_spammers_evaluation_object.F1_score = (2 * grouped_spammers_evaluation_object.precision * grouped_spammers_evaluation_object.recall) / (grouped_spammers_evaluation_object.precision + grouped_spammers_evaluation_object.recall)

    if TP == 0 and FP == 0 and FN == 0:
        grouped_spammers_evaluation_object.precision = 1
        grouped_spammers_evaluation_object.recall = 1
        grouped_spammers_evaluation_object.F1_score = 1

    grouped_spammers_evaluation_object.tpr = grouped_spammers_evaluation_object.recall
    if (FP + TN) > 0:
        grouped_spammers_evaluation_object.fpr = FP / (FP + TN)
    else:
        grouped_spammers_evaluation_object.fpr = 0


def evaluate_detected_products(products_evaluation_object, products_count, spam_reviews_list, targeted_products):
    """

    :param targeted_products: set of all detected targeted products
    :param products_evaluation_object: object to save results
    :param products_count: number of all products
    :param spam_reviews_list: true generated spam reviews
    """
    detected_targeted_products = set()
    for product in targeted_products:
        detected_targeted_products.add(product)
    true_targeted_products = set()
    for review in spam_reviews_list:
        true_targeted_products.add(review.product)

    true_positives_set = set(true_targeted_products.intersection(detected_targeted_products))
    false_positives_set = set(detected_targeted_products.difference(true_positives_set))

    TP = len(true_positives_set)
    FP = len(false_positives_set)

    false_negatives_set = set(true_targeted_products.difference(true_positives_set))

    FN = len(false_negatives_set)

    products_evaluation_object.true_positives = TP
    products_evaluation_object.false_positives = FP
    products_evaluation_object.false_negatives = FN
    TN = products_count - TP - FP - FN
    products_evaluation_object.true_negatives = TN

    if (TP + FP) > 0:
        products_evaluation_object.precision = TP / (TP + FP)
    else:
        products_evaluation_object.precision = 0

    if (TP + FN) > 0:
        products_evaluation_object.recall = TP / (TP + FN)
    else:
        products_evaluation_object.recall = 0

    if (products_evaluation_object.precision == 0) and (products_evaluation_object.recall == 0):
        products_evaluation_object.F1_score = 0
    else:
        products_evaluation_object.F1_score = (2 * products_evaluation_object.precision * products_evaluation_object.recall) / ( products_evaluation_object.precision + products_evaluation_object.recall)

    if TP == 0 and FP == 0 and FN == 0:
        products_evaluation_object.precision = 1
        products_evaluation_object.recall = 1
        products_evaluation_object.F1_score = 1

    products_evaluation_object.tpr = products_evaluation_object.recall
    if (FP + TN) > 0:
        products_evaluation_object.fpr = FP / (FP + TN)
    else:
        products_evaluation_object.fpr = 0


def evaluate_detected_intervals(intervals_evaluation_object, raw_top_ranked_intervals, all_sorted_intervals, spam_intervals_list):
    """

    :param spam_intervals_list: true generated spam intervals
    :param intervals_evaluation_object: object to save results
    :param raw_top_ranked_intervals: detected spamming intervals before removing redundancy
    :param all_sorted_intervals: all created intervals
    """

    true_spam_intervals = set(spam_intervals_list)

    should_be_reported = set()
    should_NOT_be_reported = set()

    TP = 0
    FP = 0
    for interval in all_sorted_intervals:
        found = False
        for spam_interval in true_spam_intervals:
            if is_sub_interval(interval, spam_interval) and interval.product.id == spam_interval.product:
                if (interval.up_type and spam_interval.up_type) or (not interval.up_type and not spam_interval.up_type):
                    should_be_reported.add(interval)
                    interval.spam_label = True
                    found = True
                    break
            elif interval.start_date == spam_interval.start_date and interval.end_date == spam_interval.end_date and interval.product.id == spam_interval.product:
                if (interval.up_type and spam_interval.up_type) or (not interval.up_type and not spam_interval.up_type):
                    should_be_reported.add(interval)
                    interval.spam_label = True
                    found = True
                    break
        if not found:
            should_NOT_be_reported.add(interval)

    for interval in raw_top_ranked_intervals:
        if interval in should_be_reported:
            TP += 1
        else:
            FP += 1

    intervals_evaluation_object.true_positives = TP
    intervals_evaluation_object.false_positives = FP

    true_spam_intervals_that_are_NOT_detected = set(should_be_reported.difference(raw_top_ranked_intervals))

    FN = len(true_spam_intervals_that_are_NOT_detected)

    intervals_evaluation_object.false_negatives = FN
    TN = len(all_sorted_intervals) - TP - FP - FN
    intervals_evaluation_object.true_negatives = TN

    if (TP + FP) > 0:
        intervals_evaluation_object.precision = TP / (TP + FP)
    else:
        intervals_evaluation_object.precision = 0

    if (TP + FN) > 0:
        intervals_evaluation_object.recall = TP / (TP + FN)
    else:
        intervals_evaluation_object.recall = 0

    if (intervals_evaluation_object.precision == 0) and (intervals_evaluation_object.recall == 0):
        intervals_evaluation_object.F1_score = 0
    else:
        intervals_evaluation_object.F1_score = (2 * intervals_evaluation_object.precision * intervals_evaluation_object.recall) / (intervals_evaluation_object.precision + intervals_evaluation_object.recall)

    if TP == 0 and FP == 0 and FN == 0:
        intervals_evaluation_object.precision = 1
        intervals_evaluation_object.recall = 1
        intervals_evaluation_object.F1_score = 1

    intervals_evaluation_object.tpr = intervals_evaluation_object.recall
    if (FP + TN) > 0:
        intervals_evaluation_object.fpr = FP / (FP + TN)
    else:
        intervals_evaluation_object.fpr = 0


def evaluate_defrauder_output(spam_reviews_list, products_count, users_count):
    members, targeted_products = parsing_functions.parse_defrauder_output("defrauder_reported_groups.txt")
    true_targeted_products = set()
    true_spammers = set()
    for review in spam_reviews_list:
        true_targeted_products.add(review.product)
        true_spammers.add(review.user)
    true_positives_set = set(true_targeted_products.intersection(targeted_products))
    false_positives_set = set(targeted_products.difference(true_positives_set))
    TP = len(true_positives_set)
    FP = len(false_positives_set)
    false_negatives_set = set(true_targeted_products.difference(true_positives_set))
    FN = len(false_negatives_set)
    TN = products_count - TP - FP - FN
    if (TP + FP) > 0:
        products_precision = TP / (TP + FP)
    else:
        products_precision = 0

    if (TP + FN) > 0:
        products_recall = TP / (TP + FN)
    else:
        products_recall = 0
    true_positives_set_u = set(true_spammers.intersection(members))
    false_positives_set_u = set(members.difference(true_positives_set_u))
    TP_u = len(true_positives_set_u)
    FP_u = len(false_positives_set_u)
    false_negatives_set_u = set(true_targeted_products.difference(true_positives_set_u))
    FN_u = len(false_negatives_set_u)
    TN_u = users_count - TP_u - FP_u - FN_u
    if (TP_u + FP_u) > 0:
        users_precision = TP_u / (TP_u + FP_u)
    else:
        users_precision = 0

    if (TP_u + FN_u) > 0:
        users_recall = TP_u / (TP_u + FN_u)
    else:
        users_recall = 0

    print("DeFrauder Evaluation=======================")
    print("TP = ", TP, end=", ")
    print("TN = ", TN, end=", ")
    print("FP = ", FP, end=", ")
    print("FN = ", FN)
    print("products precision = ", products_precision)
    print("products recall = ", products_recall)
    print("TP = ", TP_u, end=", ")
    print("TN = ", TN_u, end=", ")
    print("FP = ", FP_u, end=", ")
    print("FN = ", FN_u)
    print("users precision = ", users_precision)
    print("users recall = ", users_recall)
    print("===========================================")

