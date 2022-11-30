from Utils import get_books, get_users, get_ratings

books = get_books("./data/BX-Books.csv")
users = get_users("./data/BX-Users.csv")
ratings = get_ratings("./data/BX-Book-Ratings.csv")
print(books)

super_users = ratings.groupby('user_id').isbn.count().sort_values(ascending=False)

print(ratings)
implicit_ratings = ratings[ratings.book_rating == 0]
explicit_ratings = ratings[ratings.book_rating != 0]

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

