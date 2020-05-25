import codecs
from datetime import *
from dateutil import parser

import my_classes


def remove_non_printable_characters(content):
    """
    :param content: the content of the file
    :return: the content after removing any in the black list
    """
    for ch in ['\u2028', '\u001D', '\u000B', '\u0085', '\u00A0', '\u2029', '\u000c', '\u0013', '\u001c', '\u001d', '\u0019']:
        if ch in content:
            content = content.replace(ch, ' ')
    return content


def strip_split(line):
    """
    :param line: a string
    :return: list of individual items
    """
    line = line.strip().split("\t")

    return line


def build_dictionaries(data_file):
    products_dict = dict()
    users_dict = dict()
    product_reviews_dict = dict()
    reviews = []
    file = codecs.open(data_file, "r", "utf-8")
    content = file.read()
    lines = remove_non_printable_characters(content).splitlines()
    # lines.pop(0)  # to remove the header row if the file is a real data file with a header of column names
    for line in lines:
        line = strip_split(line)
        review = my_classes.Review()
        review.id = line[2]
        review.user = line[1]
        review.product = line[3]
        review.rate = int(line[7])
        review.date = datetime.date(parser.parse(line[14]))
        reviews.append(review)
        if line[3] not in products_dict:
            products_dict[line[3]] = {line[1]}
        else:
            products_dict[line[3]].add(line[1])
        if line[1] not in users_dict:
            users_dict[line[1]] = {line[3]}
        else:
            users_dict[line[1]].add(line[3])
        if review.product not in product_reviews_dict:
            product_reviews_dict[review.product] = {review}
        else:
            product_reviews_dict[review.product].add(review)
    file.close()
    return products_dict, users_dict, product_reviews_dict, reviews


def build_products_dict(data_file):
    """
    :param data_file: data file full path
    :return: products_dict: dictionary where the key is the product and the values are the users who reviewed this product
    """

    products_dict = dict()
    file = codecs.open(data_file, "r", "utf-8")
    content = file.read()
    # remove_non_printable_characters(content)
    lines = remove_non_printable_characters(content).splitlines()
    # lines.pop(0)  # to remove the header row if the file is a real data file with a header of column names
    counter = 1
    
    for line in lines:
        line = strip_split(line)
        if line[0] != "US":
            # print(counter)  # unhint when there is a parsing error
            continue
        else:
            if line[3] not in products_dict:
                products_dict[line[3]] = {line[1]}
            else:
                products_dict[line[3]].add(line[1])
        counter += 1
    file.close()
    return products_dict


def build_users_dict(data_file):
    """
    :param data_file: data file full path
    :return: users_dict: dictionary where the key is the user and the values are the products reviewed by that user
    """

    users_dict = dict()
    file = codecs.open(data_file, "r", "utf-8")
    content = file.read()
    # remove_non_printable_characters(content)
    lines = remove_non_printable_characters(content).splitlines()
    # lines.pop(0)  # to remove the header row if the file is a real data file with a header of column names

    for line in lines:
        line = strip_split(line)
        if line[1] not in users_dict:
            users_dict[line[1]] = {line[3]}
        else:
            users_dict[line[1]].add(line[3])
    file.close()
    return users_dict


def build_product_reviews_dict(data_file):
    """

    :param data_file: data file full path
    :return: dictionary for the reviews of each product
    """
    product_reviews_dict = dict()
    reviews = []
    file = codecs.open(data_file, "r", "utf-8")
    content = file.read()
    # remove_non_printable_characters(content)
    lines = remove_non_printable_characters(content).splitlines()
    # lines.pop(0)  # to remove the header row if the file is a real data file with a header of column names

    for line in lines:
        line = strip_split(line)
        review = my_classes.Review()
        review.id = line[2]
        review.user = line[1]
        review.product = line[3]
        review.rate = int(line[7])
        review.date = datetime.date(parser.parse(line[14]))
        reviews.append(review)

        if review.product not in product_reviews_dict:
            product_reviews_dict[review.product] = {review}
        else:
            product_reviews_dict[review.product].add(review)

    file.close()
    return reviews, product_reviews_dict


def parse_spamming_reviews(spam_reviews_list, file_name):
    """

    :param spam_reviews_list: a list to keep the parsed reviews objects from the generated files
    :param file_name: data file name
    """
    file = codecs.open(file_name, "r", "utf-8")
    content = file.read()
    remove_non_printable_characters(content)
    lines = remove_non_printable_characters(content).splitlines()

    for line in lines:
        line = strip_split(line)
        review = my_classes.Review()
        review.user = line[1]
        review.id = line[2]
        review.product = line[3]
        review.rate = line[7]
        review.date = datetime.date(parser.parse(line[14]))
        spam_reviews_list.append(review)
    file.close()


def parse_spamming_intervals(spam_intervals_list, file_name):
    """

    :param spam_intervals_list: a list to keep the parsed intervals objects from the generated files
    :param file_name: data file name
    """
    file = codecs.open(file_name, "r", "utf-8")
    content = file.read()
    remove_non_printable_characters(content)
    lines = remove_non_printable_characters(content).splitlines()

    for line in lines:
        line = strip_split(line)
        interval = my_classes.EvaluationTimeInterval()
        interval.product = line[0]
        interval.start_date = datetime.date(parser.parse(line[1]))
        interval.width = int(line[2])
        interval.end_date = interval.start_date + timedelta(days=interval.width - 1)
        if line[3] == "False":
            interval.up_type = False
        else:
            interval.up_type = True
        interval.members_count = int(line[4])
        interval.reviews_count = int(line[5])
        spam_intervals_list.append(interval)
    file.close()


def parse_defrauder_output(defrauder_output_file):
    members = set()
    targeted_products = set()
    file = codecs.open(defrauder_output_file, "r", "utf-8")
    content = file.read()
    remove_non_printable_characters(content)
    lines = remove_non_printable_characters(content).splitlines()
    for line in lines:
        line = line.strip().split("\t")
        users_set = line[1]
        products_set = line[2]
        for char in users_set:
            if char in "{}":
                users_set = users_set.replace(char, " ")
        for char in products_set:
            if char in "{}":
                products_set = products_set.replace(char, " ")
        for u in users_set.split(' '):
            members.add(u)
        for p in products_set.split(' '):
            targeted_products.add(p)
    file.close()
    if '' in members:
        members.remove('')
    if '' in targeted_products:
        targeted_products.remove('')
    return members, targeted_products
