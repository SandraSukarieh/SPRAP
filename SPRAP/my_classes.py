from datetime import *
from dateutil import parser


class Thresholds:  # a class to define a global variable among the whole project
    reviews_threshold = 2
    top_ranked_intervals_threshold = 0.4
    collusion_spamming_groups_threshold = 0.6


class IdCounter:  # a class to define a global variable among the whole project
    interval_counter = 0
    group_counter = 0


class Product:
    __slots__ = ['id', 'users', 'reviews', 'first_review', 'last_review', 'up_time_intervals', 'down_time_intervals', 'all_intervals']

    def __init__(self):
        self.id = ""
        self.users = set()
        self.reviews = set()
        self.first_review = datetime.date(parser.parse("2050-12-31"))
        self.last_review = datetime.date(parser.parse("1980-01-01"))
        self.up_time_intervals = set()
        self.down_time_intervals = set()
        self.all_intervals = set()

    def print(self):
        print("id: ", self.id, end=" ")
        print("{", end="")
        for u in self.users:
            print(u, end=" ")
        print("}")
        for review in self.reviews:
            review.print()
        print("-------------------")

    def print_all_intervals(self):
        for interval in self.all_intervals:
            interval.print()


class Review:
    __slots__ = ['id', 'user', 'product', 'rate', 'date']

    def __init__(self):
        self.id = ""
        self.user = ""
        self.product = ""
        self.rate = 0
        self.date = datetime.now()

    def print(self):
        print("id: ", self.id, end=", ")
        print("user:", self.user, end=", ")
        print("product:", self.product, end=", ")
        print("rate:", self.rate, end=", ")
        print("date:", self.date)


class TimeInterval:
    __slots__ = ['id', 'product', 'up_type', 'probability', 'f_probability', 'pairs_scores_sum', 'f_pairs_scores_sum', 'start_date', 'width', 'end_date', 'data', 'density', 'f_density', 'time_weight', 'f_time_weight', 'f_users_count', 'total_weight', 'f_total_weight', 'spamicity', 'reviews', 'users', 'counted_pairs', 'pairs_weights_sum', 'pairs_ratio', 'spam_label', 'parents']

    def __init__(self):
        self.id = -1
        self.product = Product()
        self.up_type = True
        self.probability = 1
        self.f_probability = 0
        self.pairs_scores_sum = 0
        self.f_pairs_scores_sum = 0
        self.start_date = datetime.date(parser.parse("1980-01-01"))
        self.width = 0  # number of days included in the interval
        self.end_date = datetime.date(parser.parse("2050-12-31"))
        self.data = set()  # to check how many votes of each value an interval has
        self.density = 0
        self.f_density = 0
        self.time_weight = 0
        self.f_time_weight = 0
        self.f_users_count = 0
        self.total_weight = 0
        self.f_total_weight = 0
        self.spamicity = 0
        self.reviews = set()
        self.users = set()
        self.counted_pairs = 0
        self.pairs_weights_sum = 0
        self.pairs_ratio = 0
        self.spam_label = False
        self.parents = []

    def print(self):
        print("id:", self.id, end=", ")
        print("p_id:", self.product.id, end=", ")
        print("up_type:", self.up_type, end=", ")
        print("prob:", self.probability, end=", ")
        print("start_date:", self.start_date, end=", ")
        print("width:", self.width, end=", ")
        print("end_date:", self.end_date, end=", ")
        print("density", self.density, end=", ")
        print("time_w:", self.time_weight, end=", ")
        print("total_w:", self.total_weight, end=", ")
        print("spamicity:", self.spamicity)

    def print_data(self):
        for time_data in self.data:
            time_data.print()

    def print_reviews(self):
        for review in self.reviews:
            review.print()

    def print_users(self):
        print("users: (", end="")
        for user in self.users:
            print(user, end=",")
        print(")")


class TimeData:
    __slots__ = ['rate', 'count']

    def __init__(self, rate):
        self.rate = rate
        self.count = 0

    def print(self):
        print("rate = ", self.rate, end=", ")
        print("count = ", self.count)


class Group:
    __slots__ = ['id', 'users', 'products', 'users_products', 'intervals', 'redundancy_intervals', 'spamicity', 'parents', 'additional_products', 'additional_reviews', 'density', 'sparsity', 'time_window', 'co_reviewing_ratio', 'f_density', 'f_sparsity', 'f_time_window', 'f_co_reviewing_ratio', 'f_users_count', 'f_products_count', 'forming_products']

    def __init__(self):
        self.id = -1
        self.users = set()
        self.products = set()
        self.users_products = set()
        self.intervals = set()  # to save the group's interval (or intervals in case of merging)
        self.redundancy_intervals = set()  # to save intervals of groups removed duw to redundancy
        self.spamicity = 0
        self.parents = []
        self.additional_products = set()
        self.additional_reviews = set()
        self.density = 0
        self.sparsity = 0
        self.time_window = 0
        self.co_reviewing_ratio = 0
        self.f_density = 0
        self.f_sparsity = 0
        self.f_time_window = 0
        self.f_co_reviewing_ratio = 0
        self.f_users_count = 0
        self.f_products_count = 0
        self.forming_products = set()

    def print(self):
        print("id = ", self.id, end=" ")
        print("u:{", end="")
        for u in self.users:
            print(u, end=" ")
        print("}", end=" ")
        print("p:{", end="")
        for p in self.products:
            print(p, end=" ")
        print("}", end=" ")
        print("t:{", end="")
        for t in self.intervals:
            print(t.id, end=" ")
        print("}", end=" ")
        print("rt:{", end="")
        for t in self.redundancy_intervals:
            print(t.id, end=" ")
        print("}", end=" ")
        print("spam = ", self.spamicity)


class UserProducts:
    __slots__ = ['id', 'products']

    def __init__(self):
        self.id = ""
        self.products = set()

    def print(self):
        print("id: ", self.id, end=" ")
        print("{", end="")
        for p in self.products:
            print(p, end=" ")
        print("}", end="")
        print()


class EvaluationObject:
    __slots__ = ['true_positives', 'true_negatives', 'false_positives', 'false_negatives', 'precision', 'recall', 'F1_score', 'tpr', 'fpr']

    def __init__(self):
        self.true_positives = 0
        self.true_negatives = 0
        self.false_positives = 0
        self.false_negatives = 0
        self.precision = 0
        self.recall = 0
        self.F1_score = 0
        self.tpr = 0
        self.fpr = 0

    def print(self):
        print("TP = ", str(self.true_positives), end=", ")
        print("TN = ", str(self.true_negatives), end=", ")
        print("FP = ", str(self.false_positives), end=", ")
        print("FN = ", str(self.false_negatives))
        print("R = ", str(self.recall))
        print("F1 = ", str(self.F1_score))
        print("P = ", str(self.precision))

    def print_for_roc(self):
        print("tpr = ", str(self.tpr))
        print("fpr = ", str(self.fpr))


class EvaluationTimeInterval:  # for the parsed "generated_spamming_intervals"
    __slots__ = ['product', 'start_date', 'width', 'end_date', 'up_type', 'members_count', 'reviews_count']

    def __init__(self):
        self.product = ""
        self.start_date = datetime.date(parser.parse("1980-01-01"))
        self.width = 0  # number of days included in the interval
        self.end_date = datetime.date(parser.parse("2050-12-31"))
        self.up_type = True
        self.members_count = 0
        self.reviews_count = 0

    def print(self):
        print("p_id:", self.product, end=", ")
        print("up_type:", self.up_type, end=", ")
        print("start_date:", self.start_date, end=", ")
        print("width:", self.width, end=", ")
        print("end_date:", self.end_date, end=", ")
        print("members_count", self.members_count, end=", ")
        print("reviews_count:", self.reviews_count)


class UserScore:  # for ranking reported users
    __slots__ = ['id', 'intervals', 'top_ranked_intervals', 'spamicity']

    def __init__(self):
        self.id = ""
        self.intervals = set()
        self.top_ranked_intervals = set()
        self.spamicity = 0

    def print(self):
        print("user_id:", self.id, end=", ")
        print("all_intervals:", str(len(self.intervals)), end=", ")
        print("top_ranked_intervals:", str(len(self.top_ranked_intervals)), end=", ")
        print("spamicity:", self.spamicity)


class DaysReviewsRecord:
    def __init__(self, checked_date):
        self.checked_date = checked_date
        self.reviews = []


class SampledGroup:
    def __init__(self):
        self.users_count = 0
        self.products_count = 0
        self.intervals_count = 0
        self.forming_products_count = 0
        self.density = 0
        self.sparsity = 0
        self.time_window = 0
        self.co_reviewing_ratio = 0