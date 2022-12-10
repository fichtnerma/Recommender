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
implicit_filtered_ratings = implicit_ratings[implicit_ratings.isbn13.isin(books.isbn13)]
print(implicit_filtered_ratings.count())

print(explicit_ratings.count())
explicit_filtered_ratings = explicit_ratings[explicit_ratings.isbn13.isin(books.isbn13)]
print(explicit_filtered_ratings.count())

avg_rating = ratings.groupby('isbn13').book_rating.mean().sort_values(ascending=False)
avg_rating = avg_rating.reset_index()
avg_rating = avg_rating.merge(books, on='isbn13')

print(avg_rating.count())
print(books.count())

def get_most_rated_books(books, ratings, n=10):
    most_rated_books = ratings.groupby('isbn13').user_id.count().sort_values(ascending=False)
    most_rated_books = most_rated_books[:n]
    most_rated_books = most_rated_books.reset_index()
    most_rated_books = most_rated_books.merge(books, on='isbn13')
    return most_rated_books

def get_least_rated_books(books, ratings, n=10):
    least_rated_books = ratings.groupby('isbn13').user_id.count().sort_values(ascending=True)
    least_rated_books = least_rated_books[:n]
    least_rated_books = least_rated_books.reset_index()
    least_rated_books = least_rated_books.merge(books, on='isbn13')
    return least_rated_books


