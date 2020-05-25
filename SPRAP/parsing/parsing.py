from parsing import parsing_functions


def parse_files(data_file):
    """

    :param data_file: data file full path
    :return: product_users dictionary, user_products dictionary, and product_reviews dictionary
    """
    products_dict = parsing_functions.build_products_dict(data_file)
    print("number of products = " + str(len(products_dict)))
    users_dict = parsing_functions.build_users_dict(data_file)
    print("number of users = " + str(len(users_dict)))
    reviews, product_reviews_dict = parsing_functions.build_product_reviews_dict(data_file)
    print("number of reviews = " + str(len(reviews)))

    return products_dict, users_dict, product_reviews_dict, reviews



