from Utils import *

books = get_books()

bookData = pd.read_csv("../../data/editions_data5.csv", sep=",", encoding="utf-8")

print(books.count())

bookData.rename(columns={'isbn_10': 'isbn', 'first_sentence.value': 'first_sentence', 'notes.value': 'notes'}, inplace=True)

print(bookData.head())
print(books.head())

bookData.isbn = bookData.isbn.map(lambda x: str(x).strip()[2:-2])

print(bookData.isbn)

bookData = books.merge(bookData, on="isbn", how="inner")

bookData = bookData.drop(columns=["Unnamed: 0", "isbn_13", "publishers", "title", "first_sentence.type", "notes.type"])

print(bookData.count())

bookData.subjects = bookData.subjects.map(lambda x: str(x).strip()[2:-2])
bookData.genres = bookData.genres.map(lambda x: str(x).strip()[2:-2])
bookData.subject = bookData.subject.map(lambda x: str(x).strip()[2:-2])

bookData = bookData.fillna(" ")

# bookData["book_info"] = bookData["book_title"] + " "+ bookData["subtitle"] + " " + bookData["subjects"] + " " + bookData["notes"] + " " + bookData["first_sentence"] + " " + bookData["genres"]

bookData["book_info"] = bookData["book_title"] + " "+ bookData["subtitle"] + " " + bookData["subjects"] + " " + bookData["genres"]

print(bookData[bookData["subjects"] != " "]["subjects"])