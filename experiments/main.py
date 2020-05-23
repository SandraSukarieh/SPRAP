import timeit
from humanfriendly import format_timespan
import codecs
from itertools import combinations
import matplotlib.pyplot as plt
import math
import gc
import pickle


def remove_non_printable_characters(content):
    """
    :param content: the content of the file
    :return: the content after removing any in the black list
    """
    for ch in ['\u2028', '\u001D', '\u000B', '\u0085', '\u00A0', '\u2029', '\u000c', '\u0013', '\u001c', '\u001d',
               '\u0019']:
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


def build_products_dict(data_file):
    """
    :param data_file: data file full path
    :return: products_dict: dictionary where the key is the product and the values are the users who reviewed this product
    """

    products_dict = dict()
    users_set = []
    file = codecs.open(data_file, "r", "utf-8")
    content = file.read()
    remove_non_printable_characters(content)
    lines = remove_non_printable_characters(content).splitlines()
    lines.pop(0)  # to remove the header row if the file is a real data file with a header of column names
    counter = 1

    for line in lines:
        line = strip_split(line)
        if line[0] != "US":
            continue
        else:
            if line[3] not in products_dict:
                products_dict[line[3]] = {line[1]}
            else:
                products_dict[line[3]].add(line[1])
            users_set.append(line[1])
        counter += 1
    file.close()
    return products_dict, users_set


start = timeit.default_timer()

data_file = "C:/Users/Administrator/Downloads/generated_data/syntheticData"

products_dict, users_set = build_products_dict(data_file)
print("products count = ", str(len(products_dict)))
print("userss count = ", str(len(users_set)))
product_co_reviewing_count = [0]*len(products_dict)
pairs_count = math.factorial(len(users_set)) // math.factorial(2) // math.factorial(len(users_set) - 2)
print("number of pairs = "+str(pairs_count))
i = 0
while i < len(users_set):
    j = i+1
    while j < len(users_set):
        counter = 0
        for product in products_dict:
            if users_set[i] in products_dict[product] and users_set[j] in products_dict[product]:
                counter += 1
        product_co_reviewing_count[counter] += 1
        j += 1
        pairs_count -= 1
        print("pairs left = ", pairs_count, end="\r")
    i += 1
    print("update, user: {0}, pairs left = {1}".format(i, pairs_count))
users_set.clear()
del users_set
gc.collect()
x = []
for i in range(len(products_dict)):
    x.append(i)
    if product_co_reviewing_count[i] != 0:
        product_co_reviewing_count[i] = math.log10(product_co_reviewing_count[i])
end = timeit.default_timer()
execution_time_seconds = end - start
print("Total execution time = ", format_timespan(execution_time_seconds))
pickle.dump(x, open("x.p", "wb"))
pickle.dump(product_co_reviewing_count, open("product_co_reviewing_count.p", "wb"))

