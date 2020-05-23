import codecs


def strip_split(line):
    """
    :param line: a string
    :return: list of individual items
    """
    line = line.strip().split("\t")

    return line


def build_products_dict(products_dict, file_name):
    """
    :param products_dict: dictionary where the key is the product and the values are the users who reviewed this product
    :param file_name: data file name
    :return: the products_dict will be filled
    """
    print("building products dictionary")
    file = codecs.open(file_name, "r", "utf-8")
    for line in file:
        line = strip_split(line)
        if line[1] not in products_dict:
            products_dict[line[1]] = [int(line[0])]
        else:
            products_dict[line[1]].append(int(line[0]))
    file.close()


def build_co_reviewing_dict(co_reviewing_dict, products_dict):
    print("building co-reviewing dictionary")
    for product in products_dict:
        users_list = products_dict[product]
        i = 0
        while i < len(users_list):
            j = i + 1
            while j < len(users_list):
                if users_list[i] not in co_reviewing_dict:
                    if users_list[j] not in co_reviewing_dict or (users_list[j] in co_reviewing_dict and users_list[i] not in co_reviewing_dict[users_list[j]]):
                        co_reviewing_dict[users_list[i]] = {users_list[j]}
                else:
                    if users_list[j] not in co_reviewing_dict or (users_list[j] in co_reviewing_dict and users_list[i] not in co_reviewing_dict[users_list[j]]):
                        co_reviewing_dict[users_list[i]].add(users_list[j])
                j += 1
            i += 1


def build_edge_list():
    file_name = "metadata"
    products_dict = dict()
    co_reviewing_dict = dict()
    build_products_dict(products_dict, file_name)
    for product in products_dict:
        sorted(products_dict[product])
    build_co_reviewing_dict(co_reviewing_dict, products_dict)
    print("writing results to output file")
    output_file = codecs.open("reviews.edgelist", "w")
    for user1 in co_reviewing_dict:
        for user2 in co_reviewing_dict[user1]:
            output_file.write(str(user1) + " ")
            output_file.write(str(user2))
            output_file.write("\n")
    output_file.close()


build_edge_list()





