import codecs
from datetime import *
from dateutil import parser

import my_classes


def print_adj_list_to_file(products_dict):
    """
    :param products_dict: dictionary where the key is the product and the values are the users who reviewed this product
    """
    output_file = codecs.open("product_user_adjacency_list.txt", "w")
    for p in products_dict:
        output_file.write(p + " : ")
        for u in products_dict[p]:
            output_file.write(u + ", ")
        output_file.write("\n")
    output_file.close()


def fill_reviews_products_dict(reviews_products_dict, rate_time_ids_set):
    """

    :param reviews_products_dict: a dictionary for reviews of each product
    :param rate_time_ids_set: a set to save rate_time_ids items to get the id, the rate and the time for each review
    """
    for item in rate_time_ids_set:

        review = my_classes.Review()
        review.product = item.product
        review.id = item.review
        review.user = item.user
        review.rate = item.rate
        review.date = datetime.date(parser.parse(item.date))

        if item.product not in reviews_products_dict:
            reviews_products_dict[item.product] = {review}
        else:
            reviews_products_dict[item.product].add(review)


def build_products(products_dict, product_reviews_dict):
    """

    :param products_dict: dictionary where the key is the product and the values are the users who reviewed this product
    :param product_reviews_dict: a dictionary for reviews of each product
     :return products_list: a list with product objects and their attributes
    """
    products_list = []
    for product_key in products_dict:
        product = my_classes.Product()
        product.id = product_key
        for user in products_dict[product_key]:
            product.users.add(user)
        for review in product_reviews_dict[product_key]:
            product.reviews.add(review)
        if len(product.users) >= my_classes.Thresholds.reviews_threshold:
            products_list.append(product)

    return products_list


def find_first_review(product):
    """

    :param product: product that we want to find the first review date for it
    """
    for review in product.reviews:
        if review.date < product.first_review:
            product.first_review = review.date


def find_last_review(product):
    """

    :param product: product that we want to find the last review date for it
    """
    for review in product.reviews:
        if review.date > product.last_review:
            product.last_review = review.date


def fill_intervals_with_spamicity(product, all_intervals):
    """

    :param product: the product we want to fill its intervals after calculating spamicity
    :param all_intervals: a set that contains all intervals with their spamicity scores
    """
    related_intervals = set()
    for interval in all_intervals:
        if interval.product.id == product.id:
            related_intervals.add(interval)
    product.all_intervals.clear()
    product.all_intervals = sorted(related_intervals, key=lambda interval: interval.spamicity, reverse=True)




