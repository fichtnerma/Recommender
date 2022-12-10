from Utils import get_books, get_users, get_ratings

books = get_books("../../data/BX-Books.csv")
users = get_users("../../data/BX-Users.csv")
ratings = get_ratings("../../data/BX-Book-Ratings.csv")
print(books.isbn13)

super_users = ratings.groupby('user_id').isbn.count().sort_values(ascending=False)

print(ratings)
implicit_ratings = ratings[ratings.book_rating == 0]
explicit_ratings = ratings[ratings.book_rating != 0]

# filtern von ratings, die nicht in books sind
print(implicit_ratings.count())
implicit_filtered_ratings = implicit_ratings[implicit_ratings.isbn.isin(books.isbn)]
print(implicit_filtered_ratings.count())

print(explicit_ratings.count())
explicit_filtered_ratings = explicit_ratings[explicit_ratings.isbn.isin(books.isbn)]
print(explicit_filtered_ratings.count())


def get_most_rated_books(books, ratings, n=10):
    most_rated_books = ratings.groupby('isbn').user_id.count().sort_values(ascending=False)
    most_rated_books = most_rated_books[:n]
    most_rated_books = most_rated_books.reset_index()
    most_rated_books = most_rated_books.merge(books, on='isbn')
    return most_rated_books

def get_least_rated_books(books, ratings, n=10):
    least_rated_books = ratings.groupby('isbn').user_id.count().sort_values(ascending=True)
    least_rated_books = least_rated_books[:n]
    least_rated_books = least_rated_books.reset_index()
    least_rated_books = least_rated_books.merge(books, on='isbn')
    return least_rated_books

def get_highest_rated_books(books, ratings, n=10):
    highest_rated_books = ratings.groupby('isbn').book_rating.mean().sort_values(ascending=False)
    highest_rated_books = highest_rated_books[:n]
    highest_rated_books = highest_rated_books.reset_index()
    highest_rated_books = highest_rated_books.merge(books, on='isbn')
    return highest_rated_books

def get_lowest_rated_books(books, ratings, n=10):
    lowest_rated_books = ratings.groupby('isbn').book_rating.mean().sort_values(ascending=True)
    lowest_rated_books = lowest_rated_books[:n]
    lowest_rated_books = lowest_rated_books.reset_index()
    lowest_rated_books = lowest_rated_books.merge(books, on='isbn')
    return lowest_rated_books

# get highest rated books in your country 
def get_highest_rated_books_in_country(books, ratings, country, n=10):
    get_highest_rated_books(books, ratings, n=100)

