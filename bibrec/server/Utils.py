import logging

import numpy as np
import pandas as pd


def get_books(path="./data/BX-Books.csv"):
    logging.info("getting books from", path)
    books = pd.read_csv(path, sep=";", encoding="latin-1")
    books.columns = books.columns.map(prepare_string)
    books.year_of_publication = pd.to_numeric(books.year_of_publication, errors='coerce')
    # Replace years above 2005 with NaN (dataset was released in 2005)
    books.loc[books.year_of_publication > 2005, 'year_of_publication'] = 0
    mean_year_of_publication = round(books.year_of_publication.mean())
    # replace invalid years with mean
    books.year_of_publication.replace(0, mean_year_of_publication, inplace=True)
    books.dropna(subset=["year_of_publication"], inplace=True)
    books["year_of_publication"] = pd.to_numeric(books.year_of_publication, downcast="integer")
    books['isbn'] = books['isbn'].apply(lambda x: x.upper())
    books["isbn13"] = books.isbn.map(convert_isbn)
    books = books[books.isbn13.notna()]
    books = filter_duplicate_books(books)
    return books


def get_users(path="./data/BX-Users.csv"):
    logging.info("getting users from", path)
    users = pd.read_csv(path, sep=";", encoding="latin-1")
    # cleaned column names
    users.columns = users.columns.map(prepare_string)
    # replaced ages below 6 and above 110 with NaN
    users.loc[(users.age < 6) | (users.age > 110), 'age'] = np.nan
    print("With NaN values", users.age.mean())
    # replaced NaN ages with random ages from normal distribution
    temp_age_series = pd.Series(
        np.random.normal(loc=users.age.mean(), scale=users.age.std(), size=users.user_id[users.age.isna()].count()))
    pos_age_series = np.abs(temp_age_series)
    users = users.sort_values('age', na_position='first').reset_index(drop=True)
    users.age.fillna(pos_age_series, inplace=True)
    users = users.sort_values('user_id').reset_index(drop=True)
    print("used mean values", users.age.mean())
    # separate location into city, state and country
    location_seperated = users.location.str.split(',', 2, expand=True)
    location_seperated.columns = ['city', 'state', 'country']
    users = users.join(location_seperated)
    users.drop(columns=['location'], inplace=True)
    # replaced empty strings with NaN
    users.country.replace('', np.nan, inplace=True)
    users.state.replace('', np.nan, inplace=True)
    users.city.replace('', np.nan, inplace=True)

    return users


def get_ratings(books, path="./data/BX-Book-Ratings.csv", explicitOnly=True):
    logging.info("getting ratings from", path)
    ratings = pd.read_csv(path, sep=";", encoding="latin-1")
    ratings.columns = ratings.columns.map(prepare_string)
    ratings['isbn'] = ratings['isbn'].apply(lambda x: x.upper())
    ratings["isbn13"] = ratings.isbn.map(convert_isbn)
    ratings = ratings[ratings.isbn13.notna()]
    ratings = ratings[ratings.isbn13.isin(books.isbn13)]
    if explicitOnly:
        ratings = get_explicit_ratings(ratings)
    return ratings


def get_explicit_ratings(ratings):
    explicit_ratings = ratings[ratings.book_rating != 0]
    return explicit_ratings


def prepare_string(string):
    return str(string).strip().lower().replace('-', '_')


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
    return books_with_mean


# add user mean and count to users
def add_user_rating_mean_and_count(df, ratings):
    user_avg_rating = ratings.groupby('user_id').book_rating.agg(['mean', 'count'])
    users_with_mean = df.merge(user_avg_rating, on='user_id', how='left')
    users_with_mean.rename(columns={'mean': 'user_mean', 'count': 'user_count'}, inplace=True)
    users_with_mean["user_count"].fillna(0, inplace=True)
    users_with_mean["user_mean"].fillna(0, inplace=True)
    return users_with_mean


def normalize_country(df, top_n=20):
    top_countries = df.country.value_counts()[:top_n].index.tolist()
    top_countries.append("other")
    encoded_users = df.copy()
    countries = encoded_users["country"]
    countries = pd.Categorical(countries, categories=top_countries).fillna("other")
    countries = list(map(lambda x: str(x).strip().lower().replace(' ', '_'), countries))
    encoded_users["country"] = countries
    return encoded_users


def normalize_state(df, top_n=20):
    top_states = df.state.value_counts()[:top_n].index.tolist()
    top_states.append("other")
    encoded_users = df.copy()
    states = encoded_users["state"]
    states = pd.Categorical(states, categories=top_states).fillna("other")
    states = list(map(lambda x: str(x).strip().lower().replace(' ', '_'), states))
    encoded_users["state"] = states

    return encoded_users


def normalize_publisher(df, top_n=20):
    top_publishers = df.publisher.value_counts()[:top_n].index.tolist()
    top_publishers.append("other")
    encoded_books = df.copy()
    publisher = encoded_books["publisher"]
    publisher = pd.Categorical(publisher, categories=top_publishers).fillna("other")
    publisher = list(map(lambda x: str(x).strip().lower().replace(' ', '_'), publisher))
    encoded_books["publisher"] = publisher
    return encoded_books


# normalizing ratings
def normalize_ratings_for_user(df, users_with_mean):
    normalized_ratings = df.copy()
    normalized_ratings = normalized_ratings.merge(users_with_mean, on='user_id', how='left')
    normalized_ratings['normalized_rating'] = normalized_ratings.book_rating - normalized_ratings["user_mean"]
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


def remove_users_without_ratings(df, n=3):
    users_with_ratings = df[df["count"] >= n]
    return users_with_ratings


def remove_books_without_ratings(df, n=3):
    books_with_ratings = df[df["count"] >= n]
    return books_with_ratings


def get_normalized_data(
        books_path='./data/BX-Books.csv',
        users_path='./data/BX-Users.csv',
        ratings_path='./data/BX-Book-Ratings.csv'):
    books = get_books(books_path)
    users = get_users(users_path)
    ratings = get_ratings(ratings_path, books)

    logging.info("normalizing books")
    books = add_book_rating_mean_and_count(books, ratings)
    books = normalize_year_of_publication(books)
    books = normalize_publisher(books)

    logging.info("normalizing users")
    users = add_user_rating_mean_and_count(users, ratings)
    users = normalize_country(users)
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


def hot_encode_data(books, users):
    logging.info("hot encoding data")
    books = hot_encode_publisher(books)
    users = hot_encode_country(users)
    users = hot_encode_state(users)
    return books, users


def recommend_items_rf(userId, age, locationCountry, locationState=None, locationCity=None, itemId=None, numberOfItems=10):
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier

    # books, users, ratings = get_normalized_data()
    books, users, ratings = get_normalized_data(books_path='../../data/BX-Books.csv',
                                                users_path='../../data/BX-Users.csv',
                                                ratings_path='../../data/BX-Book-Ratings.csv')

    limit = 1000
    logging.info("limiting data to {} ratings".format(limit))
    df_ratings = ratings.groupby('isbn13').user_id.count().sort_values(ascending=False)
    df_ratings = df_ratings[:limit]
    df_ratings = df_ratings.reset_index()

    books = books[books.isbn13.isin(df_ratings.isbn13)]
    users = users[users.user_id.isin(df_ratings.user_id)]
    books, users = hot_encode_data(books, users)

    # RF Features: Country, State, Age, Year-of-Publication, Publisher
    tmp_users = users.filter(regex="user_id|age|country_|state_", axis=1)
    tmp_books = books.filter(regex="isbn13|normalized_year_of_publication|publisher_", axis=1)
    # df = df_ratings.filter(regex="isbn13|user_id|normalized_rating", axis=1)
    df = df_ratings.filter(regex="isbn13|user_id|book_rating", axis=1)
    df = df.merge(tmp_users)
    df = df.merge(tmp_books)

    # Features
    X = df.drop(['user_id', 'isbn13', 'book_rating'], axis=1)
    # Prediction
    Y = df['book_rating']

    logging.info("splitting training/testing data")
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.30)

    from os.path import exists
    import pickle

    # Load the model from the file
    model_file = "rf-recommendItems.pkl"
    if exists(model_file):
        logging.info("loading model", model_file)
        with open(model_file, "rb") as file:
            rfc = pickle.load(file)
    else:
        logging.info("Creating new model")
        rfc = RandomForestClassifier(n_estimators=100, min_weight_fraction_leaf=0, n_jobs=3, random_state=1)

    rfc.fit(X_train, y_train)

    # Save the model to a file
    with open(model_file, "wb") as file:
        logging.info("Saving model", model_file)
        pickle.dump(rfc, file)

    logging.info("Running prediction")
    rfc_pred = rfc.predict(X_test)

    print(rfc_pred)

    # ratings = pd.DataFrame(rfc_pred, columns=["book_rating"])
    # predictions = pd.concat([y_test[:3], X_test[:3]], axis=1)
    # predictions = pd.concat([ratings, X_test], axis=1)
    # predictions = predictions.filter(regex="isbn13|book_rating", axis=1)
    # predictions

    return rfc_pred.tolist()


def flatten(l):
    return [item for sublist in l for item in sublist]
