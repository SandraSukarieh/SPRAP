from my_classes import UserScore


def create_detected_spammers(top_ranked_intervals, all_sorted_intervals, collusion_groups, detected_spammers):
    """

    :param collusion_groups: set of reported collusion spamming groups
    :param top_ranked_intervals: set of reported spamming intervals
    :param all_sorted_intervals: set of all created intervals
    :param detected_spammers: a set to fill with detected spammers
    """
    spammers = set()
    for interval in top_ranked_intervals:
        for user in interval.users:
            if user not in spammers:
                spammers.add(user)  # to solve redundancy
                user_score = UserScore()
                user_score.id = user
                for interval in all_sorted_intervals:
                    if user in interval.users:
                        user_score.intervals.add(interval)
                for interval in top_ranked_intervals:
                    if user in interval.users:
                        user_score.top_ranked_intervals.add(interval)
                intervals_ratio = len(user_score.top_ranked_intervals) / len(user_score.intervals)
                if check_if_collusion_group_member(user, collusion_groups):
                    user_score.spamicity = (intervals_ratio + 1) / 2
                else:
                    user_score.spamicity = intervals_ratio
                detected_spammers.add(user_score)


def check_if_collusion_group_member(user, collusion_groups):
    """

    :param user: the user we want to check if he is a member of a collusion spamming group
    :param collusion_groups: a set of reported collusion spamming groups
    :return:
    """
    for group in collusion_groups:
        if user in group.users:
            return True
    return False


def get_sorted_users_by_least_spamicity(users_set, top_ranked_intervals, all_sorted_intervals):
    temp = []
    for user in users_set:
        pair = [user, calculate_user_initial_spamicity_score(user, top_ranked_intervals, all_sorted_intervals)]
        temp.append(pair)
    sorted_users = sorted(temp, key=lambda pair: (pair[1], pair[0]))
    return sorted_users


def get_least_spammy_user(top_ranked_intervals, users_set, all_sorted_intervals):
    """

    :param top_ranked_intervals: a set of reported spamming intervals
    :param all_sorted_intervals: a set of all created intervals
    :param users_set: a set of users to check and return the least spammy member of
    :return: the least spammy member of users_set
    """

    min_score = 2
    min_user = ""
    for user in users_set:
        user_score = calculate_user_initial_spamicity_score(user, top_ranked_intervals, all_sorted_intervals)
        if user_score < min_score:
            min_score = user_score
            min_user = user
        elif user_score == min_score and user < min_user:  # if two users have the same score then take the one with the smaller ID to always get the same results
            min_score = user_score
            min_user = user
    return min_user


def calculate_user_initial_spamicity_score(user, top_ranked_intervals, all_sorted_intervals):
    """

    :param user: the user we want to calculate the pre-score of
    :param top_ranked_intervals: a set of reported spamming intervals
    :param all_sorted_intervals: a set of all created intervals
    :return: the initial spamicity score of the user
    """

    users_intervals = 0
    users_spammmy_intervals = 0
    for interval in all_sorted_intervals:
        if user in interval.users:
            users_intervals += 1
    for interval in top_ranked_intervals:
        if user in interval.users:
            users_spammmy_intervals += 1
    return users_spammmy_intervals / users_spammmy_intervals



