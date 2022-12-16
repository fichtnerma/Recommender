from Utils import *
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

books = get_books()

bookData = pd.read_csv("../../data/editions_dump.csv", sep=",", encoding="utf-8")

print(books.count())

bookData.rename(columns={'isbn_10': 'isbn', 'first_sentence.value': 'first_sentence', 'notes.value': 'notes'}, inplace=True)

print(bookData.head())
print(books.head())

bookData.isbn = bookData.isbn.map(lambda x: str(x).strip()[2:-2])

print(bookData.isbn)

bookData = books.merge(bookData, on="isbn", how="inner")

bookData = bookData.drop(columns=["Unnamed: 0.1", "Unnamed: 0", "isbn_13", "publishers", "title", "first_sentence.type", "notes.type"])

print(bookData.count())

bookData = bookData.fillna(" ")

bookData["book_info"] = bookData["book_title"] + " "+ bookData["subtitle"] + " " + bookData["subjects"] + " " + bookData["notes"] + " " + bookData["first_sentence"] + " " + bookData["genres"]

tfidf = TfidfVectorizer(stop_words='english')
overview_matrix = tfidf.fit_transform(bookData["book_info"])
#Output the shape of tfidf_matrix
overview_matrix.shape

similarity_matrix = linear_kernel(overview_matrix,overview_matrix)

#books index mapping
mapping = pd.Series(bookData.index,index = bookData["isbn13"])

def recommend_tf_idf(isbn13):
    book_index = mapping[isbn13]
    #get similarity values with other movies
    #similarity_score is the list of index and similarity matrix
    similarity_score = list(enumerate(similarity_matrix[book_index]))
    #sort in descending order the similarity score of movie inputted with all the other movies
    similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)
    # Get the scores of the 15 most similar movies. Ignore the first movie.
    similarity_score = similarity_score[1:15]
    #return movie names using the mapping series
    book_indices = [i[0] for i in similarity_score]
    return (bookData[["book_title", "isbn13", "isbn"]].iloc[book_indices])

print(recommend_tf_idf("9780002005012"))

print(bookData.isbn13.head())