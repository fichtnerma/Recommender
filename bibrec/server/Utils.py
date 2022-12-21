import logging

import numpy as np
import pandas as pd
import pickle

from os.path import exists
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def prepare_string(string):
    return str(string).strip().lower().replace('-', '_')


def read_csv(path):
    df = pd.read_csv(path, sep=";", encoding="latin-1")
    df.columns = df.columns.map(prepare_string)
    return df


def convert_isbn(id):
    isbn = str(id)
    if len(isbn) == 10:
        isbn = isbn.rstrip(isbn[-1])
        isbn = "978" + isbn
        sum = 0
        for i in range(len(isbn)):
            try:
                int(isbn[i])
            except ValueError:
                return np.nan
            if i % 2 == 0:
                sum += int(isbn[i])
            else:
                sum += int(isbn[i]) * 3
        check_digit = 10 - (sum % 10)
        if check_digit == 10:
            check_digit = 0
        isbn += str(check_digit)
        return isbn
    else:
        return np.nan


# sanitize isbn and add isbn13
def sanitize_isbn(df):
    df['isbn'] = df['isbn'].apply(lambda x: x.upper())
    df["isbn13"] = df.isbn.map(convert_isbn)
    return df


def sanitize_year_of_publication(books):
    books.year_of_publication = pd.to_numeric(books.year_of_publication, errors='coerce')
    # Replace years above 2005 with NaN (dataset was released in 2005)
    books.loc[books.year_of_publication > 2005, 'year_of_publication'] = 0
    mean_year_of_publication = round(books.year_of_publication.mean())
    # replace invalid years with mean
    books.year_of_publication.replace(0, mean_year_of_publication, inplace=True)
    books.dropna(subset=["year_of_publication"], inplace=True)
    books["year_of_publication"] = pd.to_numeric(books.year_of_publication, downcast="integer")
    return books


def get_books(path="./data/BX-Books.csv"):
    logging.info("getting books from", path)
    books = read_csv(path)

    # sanitize isbn
    books = sanitize_isbn(books)

    # sanitize year_of_publication
    books = sanitize_year_of_publication(books)

    # filter invalid books
    books = books[books.isbn13.notna()]
    books = filter_duplicate_books(books)

    return books


def sanitize_age(users):
    # replaced ages below 6 and above 110 with NaN
    users.loc[(users.age < 6) | (users.age > 110), 'age'] = np.nan
    # print("With NaN values", users.age.mean())
    # replaced NaN ages with random ages from normal distribution
    temp_age_series = pd.Series(
        np.random.normal(loc=users.age.mean(), scale=users.age.std(), size=users.user_id[users.age.isna()].count()))
    pos_age_series = np.abs(temp_age_series)
    users = users.sort_values('age', na_position='first').reset_index(drop=True)
    users.age.fillna(pos_age_series, inplace=True)
    users = users.sort_values('user_id').reset_index(drop=True)
    # print("used mean values", users.age.mean())
    return users


def split_city_state_country(users):
    # separate location into city, state and country
    location_seperated = users.location.str.split(',', 2, expand=True)
    location_seperated.columns = ['city', 'state', 'country']
    users = users.join(location_seperated)
    users.drop(columns=['location'], inplace=True)

    # replaced empty strings with NaN
    users.country.replace('', np.nan, inplace=True)
    users.state.replace('', np.nan, inplace=True)
    users.city.replace('', np.nan, inplace=True)

    # define column country as string + trim and lowercase the value
    users["country"] = users["country"].astype("string")
    users['country'] = users['country'].str.strip().str.lower()

    return users


def get_users(path="./data/BX-Users.csv"):
    logging.info("getting users from", path)
    users = read_csv(path)

    # sanitize age
    users = sanitize_age(users)
    users = split_city_state_country(users)

    # TODO: check if duplicate users present

    return users


def get_explicit_ratings(ratings):
    explicit_ratings = ratings[ratings.book_rating != 0]
    return explicit_ratings


def get_ratings(books, path="./data/BX-Book-Ratings.csv", explicitOnly=True):
    logging.info("getting ratings from", path)
    ratings = read_csv(path)

    # sanitize isbn
    ratings = sanitize_isbn(ratings)

    # filter invalid ratings
    ratings = ratings[ratings.isbn13.notna()]
    ratings = ratings[ratings.isbn13.isin(books.isbn13)]

    if explicitOnly == True:
        ratings = get_explicit_ratings(ratings)

    return ratings


def weighted_rating(v, m, R, C):
    """
    Calculate the weighted rating

    Args:
    v -> average rating for each item (float)
    m -> minimum votes required to be classified as popular (float)
    R -> average rating for the item (pd.Series)
    C -> average rating for the whole dataset (pd.Series)

    Returns:
    pd.Series
    """
    return ((v / (v + m)) * R) + ((m / (v + m)) * C)


def assign_popular_based_score(rating_df, item_df, user_col, item_col, rating_col):
    """

    Assigned popular based score.

    Args:
    rating -> pd.DataFrame contains ['item_id', 'rating'] for each user.

    Returns
    popular_items -> pd.DataFrame contains item and weighted score.
    """

    # pre processing
    vote_count = rating_df.groupby(item_col, as_index=False).agg(
        {user_col: "count", rating_col: "mean"}
    )
    vote_count.columns = [item_col, "vote_count", "avg_rating"]

    # calculate input parameters
    C = np.mean(vote_count["avg_rating"])
    m = np.percentile(vote_count["vote_count"], 70)
    vote_count = vote_count[vote_count["vote_count"] >= m]
    R = vote_count["avg_rating"]
    v = vote_count["vote_count"]
    vote_count["weighted_rating"] = weighted_rating(v, m, R, C)

    # post processing
    vote_count = vote_count.merge(item_df, on=[item_col], how="left")
    popular_items = vote_count.loc[
                    :, [item_col, "vote_count", "avg_rating", "weighted_rating"]
                    ]

    return popular_items


# filter duplicate books
def filter_duplicate_books(books):
    return books.drop_duplicates(subset=["isbn"], ignore_index=True)


# add mean and count to books
def add_book_rating_mean_and_count(df, ratings):
    book_avg_rating = ratings.groupby('isbn13').book_rating.agg(['mean', 'count'])
    books_with_mean = df.merge(book_avg_rating, on='isbn13', how='left')
    books_with_mean.rename(columns={'mean': 'rating_mean', 'count': 'rating_count'}, inplace=True)
    books_with_mean["rating_count"].fillna(0, inplace=True)
    books_with_mean["rating_mean"].fillna(0, inplace=True)
    return books_with_mean


# add user mean and count to users
def add_user_rating_mean_and_count(df, ratings):
    user_avg_rating = ratings.groupby('user_id').book_rating.agg(['mean', 'count'])
    users_with_mean = df.merge(user_avg_rating, on='user_id', how='left')
    users_with_mean.rename(columns={'mean': 'user_mean', 'count': 'user_count'}, inplace=True)
    users_with_mean["user_count"].fillna(0, inplace=True)
    users_with_mean["user_mean"].fillna(0, inplace=True)
    return users_with_mean


top_countries = None


def normalize_country(df, all_countries, top_n=20):
    global top_countries
    if top_countries == None:
        logging.info("Creating top_countries")
        top_countries = all_countries.value_counts()[:top_n].index.tolist()
        top_countries = list(map(lambda x: str(x).strip().lower().replace(' ', '_'), top_countries))
        top_countries.append("other")
    encoded_users = df.copy()
    countries = encoded_users["country"]
    countries = list(map(lambda x: str(x).strip().lower().replace(' ', '_'), countries))
    countries = pd.Categorical(countries, categories=top_countries).fillna("other")
    encoded_users["country"] = countries
    return encoded_users


top_states = None


def normalize_state(df, top_n=20):
    global top_states
    if top_states == None:
        logging.info("Creating top_states")
        top_states = df.state.value_counts()[:top_n].index.tolist()
        top_states = list(map(lambda x: str(x).strip().lower().replace(' ', '_'), top_states))
        top_states.append("other")
    encoded_users = df.copy()
    states = encoded_users["state"]
    states = list(map(lambda x: str(x).strip().lower().replace(' ', '_'), states))
    states = pd.Categorical(states, categories=top_states).fillna("other")
    encoded_users["state"] = states
    return encoded_users


top_publishers = None


def normalize_publisher(df, top_n=20):
    global top_publishers
    if top_publishers == None:
        top_publishers = df.publisher.value_counts()[:top_n].index.tolist()
        top_publishers = list(map(lambda x: str(x).strip().lower().replace(' ', '_'), top_publishers))
        top_publishers.append("other")
    encoded_books = df.copy()
    publisher = encoded_books["publisher"]
    publisher = list(map(lambda x: str(x).strip().lower().replace(' ', '_'), publisher))
    publisher = pd.Categorical(publisher, categories=top_publishers).fillna("other")
    encoded_books["publisher"] = publisher
    return encoded_books


# normalizing ratings
def normalize_ratings_for_user(df, users_with_mean):
    tmp_ratings = df.copy()
    tmp_ratings = tmp_ratings.merge(users_with_mean, on='user_id', how='left')
    tmp_ratings['normalized_rating'] = tmp_ratings.book_rating - tmp_ratings["user_mean"]
    # normalized_ratings = df.merge(tmp_ratings[["isbn13", "normalized_rating"]], on='isbn13', how='left')
    normalized_ratings = tmp_ratings[["isbn13", "normalized_rating"]].merge(df, on='isbn13', how='left')
    return normalized_ratings


# calculate age of books
def normalize_year_of_publication(df):
    df['normalized_year_of_publication'] = df['year_of_publication'].map(lambda x: 2005 - x)
    return df


def get_most_rated_books(df, n=10) -> pd.DataFrame:
    most_rated_books = df.sort_values('rating_count', ascending=False)
    most_rated_books = most_rated_books[:n]
    return most_rated_books


def get_least_rated_books(df, n=10) -> pd.DataFrame:
    least_rated_books = df.sort_values('rating_count', ascending=True)
    least_rated_books = least_rated_books[:n]
    return least_rated_books


def get_lowest_rated_books(books, ratings, n=10):
    lowest_rated_books = ratings.groupby('isbn').book_rating.mean().sort_values(ascending=True)
    lowest_rated_books = lowest_rated_books[:n]
    lowest_rated_books = lowest_rated_books.reset_index()
    lowest_rated_books = lowest_rated_books.merge(books, on='isbn')
    return lowest_rated_books


def get_country_ratings(users, ratings, country):
    parsed_user_country = country.__str__().lower().strip()
    mask = users["country"] == parsed_user_country
    country_users = users[mask]
    logging.info(f'Found {len(country_users)} users in the specified country')
    # filter for user ratings from the specified country
    merged_country_ratings = pd.merge(ratings, country_users, on='user_id')
    filtered_country_ratings = ratings[ratings['user_id'].isin(merged_country_ratings['user_id'])]

    return filtered_country_ratings


def remove_users_without_ratings(df, n=3):
    users_with_ratings = df[df["rating_count"] >= n]
    return users_with_ratings


def remove_books_without_ratings(df, n=3):
    books_with_ratings = df[df["rating_count"] >= n]
    return books_with_ratings

def get_normalized_data(books_path='./data/normalized_books.csv',
                        users_path='./data/normalized_users.csv'
                        ratings_path='./data/normalized_ratings.csv')
    books = pd.read_csv(books_path , sep=",", encoding="utf-8")
    users = pd.read_csv(users_path, sep=",", encoding="utf-8")
    ratings = pd.read_csv(ratings_path, sep=",", encoding="utf-8")
    return books, users, ratings

def normalized_data(books, users, ratings, explicitOnly=True):

    logging.info("normalizing books")
    books = add_book_rating_mean_and_count(books, ratings)
    books = normalize_year_of_publication(books)
    books = normalize_publisher(books)

    logging.info("normalizing users")
    users = add_user_rating_mean_and_count(users, ratings)
    users = normalize_country(users, users.country)
    users = normalize_state(users)

    logging.info("normalizing ratings")
    ratings = normalize_ratings_for_user(ratings, users)

    return books, users, ratings


def hot_encode_publisher(books):
    logging.info("hot encoding publisher")
    encoded_books = pd.get_dummies(books, columns=['publisher'], prefix='publisher')
    return encoded_books


def hot_encode_country(users):
    logging.info("hot encoding country")
    encoded_users = pd.get_dummies(users, columns=['country'], prefix='country')
    return encoded_users


def hot_encode_state(users):
    logging.info("hot encoding state")
    encoded_users = pd.get_dummies(users, columns=['state'], prefix='state')
    return encoded_users


def hot_encode_books(books):
    print("hot encoding books")
    books = hot_encode_publisher(books)
    return books


def hot_encode_users(users):
    logging.info("hot encoding books")
    users = hot_encode_country(users)
    users = hot_encode_state(users)
    return users

def get_model(path):

    if not exists(path):
        logging.info("model", path, "not found")
        raise Exception("Model not found: ", path)

    model = read_object(path)

    return model

def train_model(path, X, Y):

    # TODO: remove random_state
    logging.info("Creating new model")
    rfc = RandomForestClassifier(n_estimators=100, min_weight_fraction_leaf=0, n_jobs=3, random_state=1)

    logging.info("Training model:", path)

    # train on training data set
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.30)
    df_input = X_test

    # TODO: train on entire data set
    rfc.fit(df_input, Y)

    # Save the model to a file
    dump_object(path, rfc)

    return rfc


def dump_object(path, obj):
    # Save the object to a file
    with open(path, "wb") as file:
        pickle.dump(obj, file)

def read_object(path):
    with open(path, "rb") as file:
        return pickle.load(file)

def recommend_items_rf(norm_books, norm_users, norm_ratings, age, locationCountry, userId=None,
                       locationState=None, locationCity=None, itemId=None,
                       numberOfItems=10):

    data_path = "./data" # docker
    # data_path = "../../data" # local

    # # for local testing
    # norm_books, norm_users, norm_ratings = get_normalized_data(books_path=data_path + '/BX-Books.csv',
    #                                             users_path=data_path + '/BX-Users.csv',
    #                                             ratings_path=data_path + '/BX-Book-Ratings.csv')

    # Specify model to load/train
    model_file = data_path + "/models/rf6-ex6.pkl"

    # drop unused isbn column
    norm_books = norm_books.drop(["isbn"], axis=1)
    norm_ratings = norm_ratings.drop(["isbn"], axis=1)

    # create user input
    user = pd.DataFrame([{
        'age': age,
        'city': locationCity,
        'state': locationState,
        'country': locationCountry
    }])
    logging.info("Running prediction for user:")
    logging.info(user)

    # create users
    df_user = user
    df_user = normalize_country(df_user, norm_users.country)
    df_user = normalize_state(df_user)
    df_user = hot_encode_users(df_user)
    df_user = df_user.filter(regex="age|country_|state_", axis=1)

    # hot encode data
    encoded_books_path = data_path + "/encoded_books.csv"

    if not exists(encoded_books_path):
        raise Exception("Encoded Books does not exist")

    encoded_books = pd.read_csv(encoded_books_path, sep=",", encoding="utf-8")

    df_books = encoded_books.filter(regex="isbn13|normalized_year_of_publication|publisher_", axis=1)

    # TODO remve this after test
    df_books = df_books[:10]

    # combine dataset
    df_input = df_books.assign(**df_user.iloc[0])

    rfc = get_model(model_file)

    # predict all books and return top-rated
    logging.info("Running prediction")
    rfc_pred = rfc.predict(df_input)

    # convert predictions to books
    predictions = df_books.filter(regex="isbn13", axis=1)
    predictions = predictions.reset_index()
    predicted_ratings = pd.DataFrame(rfc_pred, columns=["predicted_book_rating"])
    predictions = predictions.join(predicted_ratings)
    predictions = predictions.merge(norm_books, on="isbn13", how="left")
    predictions = predictions.sort_values("predicted_book_rating", na_position="first", ascending=False)

    logging.info("Predictions:")
    logging.info(predictions[:numberOfItems])

    return predictions[:numberOfItems]


# print("Predictions:")
# print(recommend_items_rf(20, "usa"))

def flatten(l):
    return [item for sublist in l for item in sublist]
