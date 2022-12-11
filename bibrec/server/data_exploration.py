from Utils import get_books, get_users, get_ratings
import pandas as pd


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
    books_with_mean["rating_mean"].fillna(0, inplace=True)
    return books_with_mean

# add user mean and count to users
def add_user_mean_and_count(df, ratings):
    user_avg_rating = ratings.groupby('user_id').book_rating.agg(['mean', 'count'])
    users_with_mean  = df.merge(user_avg_rating, on='user_id', how='left')
    users_with_mean.rename(columns={'mean': 'user_mean', 'count': 'user_count'}, inplace=True)
    users_with_mean["user_count"].fillna(0, inplace=True)
    users_with_mean["user_mean"].fillna(0, inplace=True)
    return users_with_mean

# hot encoding users country
def hot_encode_country(df, top_n=10):
    top_countries = df.country.value_counts()[:top_n].index.tolist()
    top_countries.append("other")
    top_countries = list(map(lambda x :str(x).strip().lower().replace(' ', '_'), top_countries))
    encoded_users = df.copy()
    encoded_users["country"] = pd.Categorical(encoded_users["country"], categories=top_countries).fillna("other")
    encoded_users = pd.get_dummies(encoded_users, columns=['country'], prefix='country')
    return encoded_users

# hot encoding users state
def hot_encode_state(df, top_n=10):
    top_states = df.state.value_counts()[:top_n].index.tolist()
    top_states.append("other")
    top_states = list(map(lambda x :str(x).strip().lower().replace(' ', '_'), top_states))
    encoded_users = df.copy()
    encoded_users["state"] = pd.Categorical(encoded_users["state"], categories=top_states).fillna("other")
    encoded_users = pd.get_dummies(encoded_users, columns=['state'], prefix='state')
    return encoded_users

# hot encoding books publisher
def hot_encode_publisher(df, top_n=10):
    top_publishers = df.publisher.value_counts()[:top_n].index.tolist()
    top_publishers.append("other")
    top_publishers = list(map(lambda x :str(x).strip().lower().replace(' ', '_'), top_publishers))
    encoded_books = df.copy()
    encoded_books["publisher"] = pd.Categorical(encoded_books["publisher"], categories=top_publishers).fillna("other")
    encoded_books = pd.get_dummies(encoded_books, columns=['publisher'], prefix='publisher')
    return encoded_books

#normalizing ratings
def normalize_ratings_for_user (df, users_with_mean):
    normalized_ratings = df.copy()
    normalized_ratings = normalized_ratings.merge(users_with_mean, on='user_id', how='left')
    normalized_ratings['normalized_rating'] = normalized_ratings.book_rating - normalized_ratings["user_mean"]
    return normalized_ratings

# calculate age of books
def calc_age(df):
    df['age'] = df['year_of_publication'].map(lambda x: 2005 - x)
    return df

def get_most_rated_books(df, n=10):
    most_rated_books = df.sort_values('count', ascending=False)
    most_rated_books = most_rated_books[:n]
    return most_rated_books

def get_least_rated_books(df,n=10):
    least_rated_books = df.sort_values('count', ascending=True)
    most_rated_books = most_rated_books[:n]
    return least_rated_books


def remove_users_without_ratings(df, n = 3):
    users_with_ratings = df[df["count"] >= n]
    return users_with_ratings

def remove_books_without_ratings(df,n = 3):
    books_with_ratings = df[df["count"] >= n]
    return books_with_ratings
    

books = get_books()
users = get_users()
ratings = get_ratings()


# implicit_ratings = ratings[ratings.book_rating == 0]
explicit_ratings = ratings[ratings.book_rating != 0]

filtered_ratings = filter_ratings(explicit_ratings, books)

books = add_mean_and_count(books, filtered_ratings)  
users = add_user_mean_and_count(users, filtered_ratings) 
normalized_ratings = normalize_ratings_for_user(filtered_ratings, users)

books = calc_age(books)

encoded_users = hot_encode_country(users, 10)
encoded_users = hot_encode_state(encoded_users, 10)

encoded_books = hot_encode_publisher(books, 10)

def get_lowest_rated_books(books, ratings, n=10):
    lowest_rated_books = ratings.groupby('isbn').book_rating.mean().sort_values(ascending=True)
    lowest_rated_books = lowest_rated_books[:n]
    lowest_rated_books = lowest_rated_books.reset_index()
    lowest_rated_books = lowest_rated_books.merge(books, on='isbn')
    return lowest_rated_books

# get highest rated books in your country 
def get_highest_rated_books_in_country(books, ratings, country, n=10):
    get_highest_rated_books(books, ratings, n=100)

