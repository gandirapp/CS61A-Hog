"""A Yelp-powered Restaurant Recommendation Program"""

from abstractions import *
from data import ALL_RESTAURANTS, CATEGORIES, USER_FILES, load_user_file
from ucb import main, trace, interact
from utils import distance, mean, zip, enumerate, sample
from visualize import draw_map

##################################
# Phase 2: Unsupervised Learning #
##################################


def find_closest(location, centroids):
    """Return the centroid in centroids that is closest to location.
    If multiple centroids are equally close, return the first one.

    >>> find_closest([3.0, 4.0], [[0.0, 0.0], [2.0, 3.0], [4.0, 3.0], [5.0, 5.0]])
    [2.0, 3.0]
    """
    # BEGIN Question 3
    """if len(centroids) == 2 and distance(location, centroids[0]) == distance(location, centroids[1]):
        return centroids[0]
    else:
        distances = {distance(location, c) : c for c in centroids}
        return distances[min(distances)]
    """
    return min([centroid for centroid in centroids], key=lambda centroid: distance(centroid, location))
    # END Question 3


def group_by_first(pairs):
    """Return a list of pairs that relates each unique key in the [key, value]
    pairs to a list of all values that appear paired with that key.

    Arguments:
    pairs -- a sequence of pairs

    >>> example = [ [1, 2], [3, 2], [2, 4], [1, 3], [3, 1], [1, 2] ]
    >>> group_by_first(example)
    [[2, 3, 2], [2, 1], [4]]
    """
    keys = []
    for key, _ in pairs:
        if key not in keys:
            keys.append(key)
    return [[y for x, y in pairs if x == key] for key in keys]


def group_by_centroid(restaurants, centroids):
    """Return a list of clusters, where each cluster contains all restaurants
    nearest to a corresponding centroid in centroids. Each item in
    restaurants should appear once in the result, along with the other
    restaurants closest to the same centroid.
    """
    # BEGIN Question 4
    centroids_restaurants = [[find_closest(restaurant_location(restaurant), centroids), restaurant] for restaurant in restaurants]
    return group_by_first(centroids_restaurants)
    # END Question 4


def find_centroid(cluster):
    """Return the centroid of the locations of the restaurants in cluster."""
    # BEGIN Question 5
    "*** REPLACE THIS LINE ***"
    return [mean([restaurant_location(res)[0] for res in cluster]), mean([restaurant_location(res)[1] for res in cluster])]
    # END Question 5

def k_means(restaurants, k, max_updates=100):
    """Use k-means to group restaurants by location into k clusters."""
    assert len(restaurants) >= k, 'Not enough restaurants to cluster'
    old_centroids, n = [], 0
    # Select initial centroids randomly by choosing k different restaurants
    centroids = [restaurant_location(r) for r in sample(restaurants, k)]

    while old_centroids != centroids and n < max_updates:
        old_centroids = centroids
        # BEGIN Question 6
        "*** REPLACE THIS LINE ***"
        clusters = group_by_centroid(restaurants, old_centroids)
        centroids = [find_centroid(cluster) for cluster in clusters]
        # END Question 6
        n += 1
    return centroids


################################
# Phase 3: Supervised Learning #
################################


def find_predictor(user, restaurants, feature_fn):
    """Return a rating predictor (a function from restaurants to ratings),
    for a user by performing least-squares linear regression using feature_fn
    on the items in restaurants. Also, return the R^2 value of this model.

    Arguments:
    user -- A user
    restaurants -- A sequence of restaurants
    feature_fn -- A function that takes a restaurant and returns a number
    """
    reviews_by_user = {review_restaurant_name(review): review_rating(review)
                       for review in user_reviews(user).values()}

    xs = [feature_fn(r) for r in restaurants]
    ys = [reviews_by_user[restaurant_name(r)] for r in restaurants]

    # BEGIN Question 7
    "*** REPLACE THIS LINE ***"
    Sxx = sum([(x - mean(xs))**2 for x in xs])
    Syy = sum([(y - mean(ys))**2 for y in ys])
    Sx = [(x - mean(xs)) for x in xs]
    Sy = [(y - mean(ys)) for y in ys]
    #Sxy = sum([(x - mean(xs) * y - mean(ys)) for x, y in xs, ys])
    xy_combine = zip(Sx, Sy)
    Sxy = sum([x * y for x, y in xy_combine])
    b = Sxy / Sxx
    a, r_squared = mean(ys) - (b * mean(xs)), (Sxy**2) / (Sxx*Syy)
    # END Question 7

    def predictor(restaurant):
        return b * feature_fn(restaurant) + a

    return predictor, r_squared


def best_predictor(user, restaurants, feature_fns):
    """Find the feature within feature_fns that gives the highest R^2 value
    for predicting ratings by the user; return a predictor using that feature.

    Arguments:
    user -- A user
    restaurants -- A list of restaurants
    feature_fns -- A sequence of functions that each takes a restaurant
    """
    reviewed = user_reviewed_restaurants(user, restaurants)
    # BEGIN Question 8
    """
    # take min/max of left side
    distances = {distance(location, c) : c for c in centroids}
    return distances[min/max(distances)]
    # take min/max of right side
    return min/max(d, key=lambda x: d[x])
    """
    predictors = dict([(find_predictor(user, reviewed, function)) for function in feature_fns])
    # END Question 8
    return max(predictors, key = lambda x: predictors[x])


def rate_all(user, restaurants, feature_fns):
    """Return the predicted ratings of restaurants by user using the best
    predictor based on a function from feature_fns.

    Arguments:
    user -- A user
    restaurants -- A list of restaurants
    feature_fns -- A sequence of feature functions
    """
    predictor = best_predictor(user, ALL_RESTAURANTS, feature_fns)
    reviewed = user_reviewed_restaurants(user, restaurants)
    # BEGIN Question 9
    "*** REPLACE THIS LINE ***"
    #lambda Argument
    #user rating
    #combine_res = zip(restaurants, reviewed)
    #for restaurant in restaurants:
    #    for rated_res in reviewed:
    #        if restaurant_name(restaurant) == restaurant_name(rated_res):X
    ratings = dict()
    for restaurant in restaurants:
        if restaurant in user_reviewed_restaurants(user, restaurants):
            ratings.update({restaurant_name(restaurant): user_rating(user, restaurant_name(restaurant))})
        else:
            ratings.update({restaurant_name(restaurant): predictor(restaurant)})
    return ratings
    "new_rating = make_review(restaurant_name(restaurant), predictor(restaurant)"


    "restaurant = make_restaurant(restaurant_name(restaurant), restaurant_location(restaurant), restaurant_categories(restaurant), restaurant_price(restaurant), restaurant_ratings(restaurant) + new_rating)"

                
    # END Question 9

def search(query, restaurants):
    """Return each restaurant in restaurants that has query as a category.

    Arguments:
    query -- A string
    restaurants -- A sequence of restaurants
    """
    # BEGIN Question 10
    "*** REPLACE THIS LINE ***"
    return [restaurant for restaurant in restaurants for category in restaurant_categories(restaurant) if category == query]
    # END Question 10

def feature_set():
    """Return a sequence of feature functions."""
    return [restaurant_mean_rating,
            restaurant_price,
            restaurant_num_ratings,
            lambda r: restaurant_location(r)[0],
            lambda r: restaurant_location(r)[1]]


@main
def main(*args):
    import argparse
    parser = argparse.ArgumentParser(
        description='Run Recommendations',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-u', '--user', type=str, choices=USER_FILES,
                        default='test_user',
                        metavar='USER',
                        help='user file, e.g.\n' +
                        '{{{}}}'.format(','.join(sample(USER_FILES, 3))))
    parser.add_argument('-k', '--k', type=int, help='for k-means')
    parser.add_argument('-q', '--query', choices=CATEGORIES,
                        metavar='QUERY',
                        help='search for restaurants by category e.g.\n'
                        '{{{}}}'.format(','.join(sample(CATEGORIES, 3))))
    parser.add_argument('-p', '--predict', action='store_true',
                        help='predict ratings for all restaurants')
    parser.add_argument('-r', '--restaurants', action='store_true',
                        help='outputs a list of restaurant names')
    args = parser.parse_args()

    # Output a list of restaurant names
    if args.restaurants:
        print('Restaurant names:')
        for restaurant in sorted(ALL_RESTAURANTS, key=restaurant_name):
            print(repr(restaurant_name(restaurant)))
        exit(0)

    # Select restaurants using a category query
    if args.query:
        restaurants = search(args.query, ALL_RESTAURANTS)
    else:
        restaurants = ALL_RESTAURANTS

    # Load a user
    assert args.user, 'A --user is required to draw a map'
    user = load_user_file('{}.dat'.format(args.user))

    # Collect ratings
    if args.predict:
        ratings = rate_all(user, restaurants, feature_set())
    else:
        restaurants = user_reviewed_restaurants(user, restaurants)
        names = [restaurant_name(r) for r in restaurants]
        ratings = {name: user_rating(user, name) for name in names}

    # Draw the visualization
    if args.k:
        centroids = k_means(restaurants, min(args.k, len(restaurants)))
    else:
        centroids = [restaurant_location(r) for r in restaurants]
    draw_map(centroids, restaurants, ratings)