import pandas as pd
import numpy as np


def get_books(path="../../data/BX-Books.csv"):
    books = pd.read_csv(path, sep=";", encoding="latin-1")
    books.columns = books.columns.map(prepare_string)
    books.year_of_publication = pd.to_numeric(books.year_of_publication, errors='coerce')
    # Replace years above 2005 with NaN (dataset was released in 2005)
    books.loc[books.year_of_publication > 2005, 'year_of_publication'] = 0
    mean_year_of_publication = round(books.year_of_publication.mean())
    # replace invalid years with mean
    books.year_of_publication.replace(0, mean_year_of_publication, inplace=True)
    # Replace NaN years with mean of all years
    books["isbn13"] = books.isbn.map(convert_isbn)
    books = books[books.isbn13.notna()]

    return books


def get_users(path="../../data/BX-Users.csv"):
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


def get_ratings(path="../../data/BX-Book-Ratings.csv"):
    ratings = pd.read_csv(path, sep=";", encoding="latin-1")
    ratings.columns = ratings.columns.map(prepare_string)
    ratings["isbn13"] = ratings.isbn.map(convert_isbn)
    ratings = ratings[ratings.isbn13.notna()]

    return ratings


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
    elif len(isbn) == 13:
        return isbn
    else:
        return np.nan


# filtern von ratings, die nicht in books sind
def filter_ratings(df, books):
    explicit_filtered_ratings = df[df.isbn13.isin(books.isbn13)]
    return explicit_filtered_ratings

# add mean and count to books
def add_mean_and_count(df, ratings):
    book_avg_rating = ratings.groupby('isbn13').book_rating.agg(['mean', 'count'])
    books_with_mean = df.merge(book_avg_rating, on='isbn13', how='left')
    books_with_mean.rename(columns={'mean': 'rating_mean', 'count': 'rating_count'}, inplace=True)
    books_with_mean["rating_count"].fillna(0, inplace=True)
    return books_with_mean

# add user mean and count to users
def add_user_mean_and_count(df, ratings):
    user_avg_rating = ratings.groupby('user_id').book_rating.agg(['mean', 'count'])
    users_with_mean  = df.merge(user_avg_rating, on='user_id', how='left')
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


#normalizing ratings
def normalize_ratings_for_user (df, users_with_mean):
    normalized_ratings = df.copy()
    normalized_ratings = normalized_ratings.merge(users_with_mean, on='user_id', how='left')
    normalized_ratings['normalized_rating'] = normalized_ratings.book_rating - normalized_ratings["user_mean"]
    return normalized_ratings

# calculate age of books
def normalize_year_of_publication(df):
    df['normalized_year_of_publication'] = df['year_of_publication'].map(lambda x: 2005 - x)
    return df

def get_most_rated_books(df, n=10):
    most_rated_books = df.sort_values('count', ascending=False)
    most_rated_books = most_rated_books[:n]
    return most_rated_books

def get_least_rated_books(df,n=10):
    least_rated_books = df.sort_values('count', ascending=True)
    least_rated_books = least_rated_books[:n]
    return least_rated_books


def remove_users_without_ratings(df, n = 3):
    users_with_ratings = df[df["count"] >= n]
    return users_with_ratings

def remove_books_without_ratings(df,n = 3):
    books_with_ratings = df[df["count"] >= n]
    return books_with_ratings

def get_normalized_data(
        books_path='../../data/BX-Books.csv',
        users_path='../../data/BX-Users.csv',
        ratings_path='../../data/BX-Book-Ratings.csv'):
    books = get_books(books_path)
    users = get_users(users_path)
    ratings = get_ratings(ratings_path)

    explicit_ratings = ratings[ratings.book_rating != 0]
    filtered_ratings = filter_ratings(explicit_ratings, books)

    books = add_mean_and_count(books, filtered_ratings)
    books = normalize_year_of_publication(books)
    books = normalize_publisher(books)

    users = add_user_mean_and_count(users, filtered_ratings)
    encoded_users = normalize_country(users)
    encoded_users = normalize_state(encoded_users)

    normalized_ratings = normalize_ratings_for_user(filtered_ratings, users)

    return books, encoded_users, normalized_ratings

def hot_encode_publisher(books):
    encoded_books = pd.get_dummies(books, columns=['publisher'], prefix='publisher')
    return encoded_books

def hot_encode_country(users):
    encoded_users = pd.get_dummies(users, columns=['country'], prefix='country')
    return encoded_users

def hot_encode_state(users):
    encoded_users = pd.get_dummies(users, columns=['state'], prefix='state')
    return encoded_users

def hot_encode_data(books, users):
    encoded_books = hot_encode_publisher(books)
    encoded_users = hot_encode_country(users)
    encoded_users = hot_encode_state(users)
    return encoded_books,  encoded_users


def get_lowest_rated_books(books, ratings, n=10):
    lowest_rated_books = ratings.groupby('isbn').book_rating.mean().sort_values(ascending=True)
    lowest_rated_books = lowest_rated_books[:n]
    lowest_rated_books = lowest_rated_books.reset_index()
    lowest_rated_books = lowest_rated_books.merge(books, on='isbn')

    return lowest_rated_books