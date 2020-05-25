import codecs


def print_intervals_to_file(intervals_set, file_name):
    """

    :param intervals_set: a set of intervals to print
    :param file_name: the path and the name of the file to write the results to
    """
    output_file = codecs.open(file_name, "w")
    for interval in intervals_set:
        output_file.write(str(interval.id) + ", ")
        output_file.write(interval.product.id + ", ")
        output_file.write(str(interval.up_type) + ", ")
        output_file.write(str(interval.start_date) + ", ")
        output_file.write(str(interval.width) + ", ")
        output_file.write(str(interval.end_date) + ", ")
        output_file.write(str(interval.density) + ", ")
        output_file.write(str(interval.time_weight) + ", ")
        output_file.write(str(interval.total_weight) + ", ")
        output_file.write(str(interval.probability) + ", ")
        output_file.write(str(interval.pairs_scores_sum) + ", ")
        output_file.write(str(interval.spamicity))
        output_file.write("\n")
    output_file.close()


def print_intervals_f_scores_to_file(intervals_set, file_name):
    """

    :param intervals_set: a set of intervals to print
    :param file_name: the path and the name of the file to write the results to
    """
    output_file = codecs.open(file_name, "w")
    for interval in intervals_set:
        output_file.write(str(interval.id) + ", ")
        output_file.write(str(interval.f_total_weight) + ", ")
        output_file.write(str(interval.f_probability) + ", ")
        output_file.write(str(interval.f_pairs_scores_sum) + ", ")
        output_file.write(str(interval.spamicity))
        output_file.write("\n")
    output_file.close()


def print_groups_to_file(groups_set, file_name):
    """
    :param file_name: the path and the name of the file to write the results to
    :param groups_set: ta set of groups to print
    """
    output_file = codecs.open(file_name, "w")
    for group in groups_set:
        products = set()
        for interval in group.intervals:
            products.add(interval.product.id)
        for interval in group.redundancy_intervals:
            products.add(interval.product.id)

        output_file.write(str(group.id) + ", ")
        output_file.write("{")
        for user in group.users:
            output_file.write(user + ",")
        output_file.write("} , {")
        for product in products:
            output_file.write(str(product) + ",")
        output_file.write("} , ")
        output_file.write(str(group.spamicity))
        output_file.write("\n")
    output_file.close()


def print_groups_f_scores_to_file(groups_set, file_name):
    """

    :param groups_set: a set of groups to print
    :param file_name: the path and the name of the file to write the results to
    """
    output_file = codecs.open(file_name, "w")
    for group in groups_set:
        output_file.write(str(group.id) + ", ")
        output_file.write(str(group.f_products_count) + ", ")
        output_file.write(str(group.f_users_count) + ", ")
        output_file.write(str(group.f_density) + ", ")
        output_file.write(str(group.f_sparsity) + ", ")
        output_file.write(str(group.f_time_window) + ", ")
        output_file.write(str(group.f_co_reviewing_ratio) + ", ")
        output_file.write(str(group.spamicity))
        output_file.write("\n")
    output_file.close()


def print_detected_reviews_to_file(spamming_reviews, raw_top_ranked_intervals, collusion_groups, file_name):
    """

    :param spamming_reviews: a list to be filled with all spamming reviews to use in evaluation
    :param raw_top_ranked_intervals: detected top-ranked intervals before filtering
    :param collusion_groups: reported collusion spamming groups
    :param file_name: the path and the name of the file to write the results to
    """
    output_file = codecs.open(file_name, "w")
    for interval in raw_top_ranked_intervals:
        for review in interval.reviews:
            if review.id not in spamming_reviews:
                spamming_reviews.add(review.id)  # to avoid printing the same review twice
                output_file.write(review.id + ", ")
                output_file.write(review.user + ", ")
                output_file.write(review.product + ", ")
                output_file.write(str(review.rate) + ", ")
                output_file.write(str(review.date))
                output_file.write("\n")
    output_file.write("===================================")
    output_file.write("\n")
    for group in collusion_groups:
        for review in group.additional_reviews:
            if review.id not in spamming_reviews:
                spamming_reviews.add(review.id)  # to avoid printing the same review twice
                output_file.write(review.id + ", ")
                output_file.write(review.user + ", ")
                output_file.write(review.product + ", ")
                output_file.write(str(review.rate) + ", ")
                output_file.write(str(review.date))
                output_file.write("\n")
    output_file.close()


def print_detected_products_to_file(targeted_products, top_ranked_intervals, collusion_groups, file_name):
    """

    :param targeted_products: a list to be filled with all targeted products to use in evaluation
    :param top_ranked_intervals: detected top-ranked intervals after filtering (products are the same before and after filtering)
    :param collusion_groups: reported collusion spamming groups
    :param file_name: the path and the name of the file to write the results to
    """
    output_file = codecs.open(file_name, "w")
    for interval in top_ranked_intervals:
        if interval.product.id not in targeted_products:
            targeted_products.add(interval.product.id)
            output_file.write(interval.product.id)
            output_file.write("\n")
    output_file.write("===================================")
    output_file.write("\n")
    for group in collusion_groups:
        for product in group.additional_products:
            if product not in targeted_products:
                targeted_products.add(product)
                output_file.write(product)
                output_file.write("\n")
    output_file.close()


def print_spammers_to_file(detected_spammers, file_name):
    """

    :param detected_spammers: set of all detected spammers
    :param file_name: the path and the name of the file to write the results to
    """

    output_file = codecs.open(file_name, "w")
    for spammer in detected_spammers:
        output_file.write(spammer.id)
        output_file.write(" - ")
        output_file.write(str(len(spammer.top_ranked_intervals)))
        output_file.write(" - ")
        output_file.write(str(len(spammer.intervals)))
        output_file.write(" - ")
        output_file.write(str(spammer.spamicity))
        output_file.write("\n")
    output_file.close()


def print_grouped_spammers_to_file(collusion_groups, file_name):
    """

    :param collusion_groups: reported collusion spamming groups
    :param file_name: the path and the name of the file to write the results to
    """
    output_file = codecs.open(file_name, "w")
    spammers = set()
    for group in collusion_groups:
        for user in group.users:
            if user not in spammers:
                spammers.add(user)
                output_file.write(user)
                output_file.write("\n")
    output_file.close()


def print_intervals_sizes(intervals_set, file_name):
    output_file = codecs.open(file_name, "w")
    for interval in intervals_set:
        output_file.write(str(interval.width))
        output_file.write("\n")
    output_file.close()


def print_groups_sizes(groups_set, file_name):
    output_file = codecs.open(file_name, "w")
    for group in groups_set:
        output_file.write(str(len(group.users)))
        output_file.write("\n")
    output_file.close()
