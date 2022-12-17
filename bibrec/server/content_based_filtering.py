from Utils import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

books = get_books()
CHUNK_QUANTITY = 5
tfidf = TfidfVectorizer(stop_words='english')
bookData = pd.read_csv("../../data/editions_dump.csv", sep=",", encoding="utf-8")
bookData.rename(columns={'isbn_10': 'isbn', 'first_sentence.value': 'first_sentence', 'notes.value': 'notes'}, inplace=True)
bookData.isbn = bookData.isbn.map(lambda x: str(x).strip()[2:-2])
bookData = books.merge(bookData, on="isbn", how="inner")
bookData = bookData.drop(columns=["Unnamed: 0", "isbn_13", "publishers", "title", "first_sentence.type", "notes.type"])
bookData.subjects = bookData.subjects.map(lambda x: str(x).strip()[2:-2])
bookData.genres = bookData.genres.map(lambda x: str(x).strip()[2:-2])
bookData = bookData.fillna(" ")
bookData["book_info"] = bookData["book_title"] + " " + bookData["subjects"] + " " + bookData["genres"]


def get_similarity_matrix(bookData, tfidf=tfidf):
    tfidf_matrix = tfidf.fit_transform(bookData["book_info"])
    similarity_matrix = linear_kernel(tfidf_matrix,tfidf_matrix)
    return similarity_matrix

similarities = []
mappings = []
for i in range(0, CHUNK_QUANTITY):
    len_books = bookData.shape[0] / CHUNK_QUANTITY
    chunkData = bookData[int(i*len_books):int((i+1)*len_books)]
    chunkData = chunkData.reset_index(drop=True)
    similarity_matrix = get_similarity_matrix(chunkData)
    similarities.append(similarity_matrix)
    mappings.append(pd.Series(chunkData.index,index = chunkData["isbn13"]))


def recommend_tf_idf(isbn13):
    book_indices = []
    for i in range(0, CHUNK_QUANTITY):
        if(isbn13 in mappings[i].index):
            similarity_matrix = similarities[i]
            book_index = mappings[i][isbn13]
            if(isinstance(book_index,pd.Series)):
                book_index = book_index[0]
            similarity_score = list(enumerate(similarity_matrix[book_index]))
            # Sort the books based on the similarity scores
            similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)
            similarity_score = similarity_score[1:15]
            book_indices.append([i[0] for i in similarity_score])

    print("Book Indices")
    print(book_indices)
    return (bookData[["book_title", "isbn13", "isbn"]].iloc[book_indices[0]])


#in mapping 3
print(recommend_tf_idf("9780771074677"))

print(bookData.isbn13.head()) 

book_index = mappings[0]["9780393045215"]
print(mappings[1])
print(book_index)
book_index = mappings[1]["9780553580334"]
print(type(book_index))

print(mappings[1])