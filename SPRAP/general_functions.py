def copy_items_to_another_set(input_container, output_set):
    """

    :param input_container: the container we want to copy its elements
    :param output_set: the set we want to fill
    """
    for item in input_container:
        output_set.add(item)


def copy_items_to_another_list(input_container, output_list):
    """

    :param input_container: the container we want to copy its elements
    :param output_list: the list we want to fill
    """
    for item in input_container:
        output_list.append(item)
