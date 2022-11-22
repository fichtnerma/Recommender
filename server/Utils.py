import pandas as pd
from collections import defaultdict


def book_parser(path):

    df = pd.read_csv(path, sep=";", encoding="latin-1", quotechar='"', skipinitialspace=True,)

    books = defaultdict(list)

    for row in df.itertuples():

        isbn = getattr(row, "ISBN")
        book_info = {
            "title": getattr(row, "Book-Title"),
            "author": getattr(row, "Book-Author"),
            "year": getattr(row, "Year-Of-Publication"),
            "publisher": getattr(row, "Publisher"),
            "image_s": getattr(row, "Image-URL-S"),
            "image_m": getattr(row, "Image-URL-M"),
            "image_l": getattr(row, "Image-URL-L")
        }

        books[isbn].append(book_info)
    
    return books

    
    
def user_parser(path, raw_data=False):
    df = pd.read_csv(path, sep=";", encoding="latin-1")
    users = defaultdict(list)

    for row in df.itertuples():
        user_id = getattr(row, "Index")
        user_info = {
            "location": getattr(row, "Location"),
            "age": getattr(row, "Age")
        }

        users[user_id].append(user_info)
    if (raw_data):
        return df
    return users



def rating_parser(path):
    df = pd.read_csv(path, sep=";", encoding="latin-1")
    book_ratings = defaultdict(list)
    user_ratings = defaultdict(list)
    for row in df.iterrows():
        print(row)
        # isbn = getattr(row, "ISBN")
        # rating = getattr(row, "Book-Rating")
        # user_id = getattr(row, "User-ID")
        # book_ratings[isbn].append(rating)
        # user_ratings[user_id].append(rating)
    
    return book_ratings, user_ratings