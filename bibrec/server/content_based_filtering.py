from Utils import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class ContentBasedFiltering:
    def __init__(self, bookData):
        books = get_books()
        self.CHUNK_QUANTITY = 50
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.bookData = bookData
        #data cleaning
        self.bookData.rename(columns={'isbn_10': 'isbn', 'first_sentence.value': 'first_sentence', 'notes.value': 'notes'}, inplace=True)
        self.bookData.isbn = self.bookData.isbn.map(lambda x: str(x).strip()[2:-2])
        self.bookData = books.merge(self.bookData, on="isbn", how="inner")
        self.bookData = self.bookData.drop(columns=["Unnamed: 0", "isbn_13", "publishers", "title", "first_sentence.type", "notes.type"])
        self.bookData.subjects = self.bookData.subjects.map(lambda x: str(x).strip()[2:-2])
        self.bookData.genres = self.bookData.genres.map(lambda x: str(x).strip()[2:-2])
        self.bookData = self.bookData.fillna(" ")
        # end data cleaning
        self.bookData["book_info"] = self.bookData["book_title"] + " " + self.bookData["subjects"] + " " + self.bookData["genres"]
        self.similarities = []
        self.mappings = []
        for i in range(0, self.CHUNK_QUANTITY):
            len_books = self.bookData.shape[0] / self.CHUNK_QUANTITY
            chunkData = self.bookData[int(i*len_books):int((i+1)*len_books)]
            chunkData = chunkData.reset_index(drop=True)
            similarity_matrix = self.get_similarity_matrix(chunkData)
            self.similarities.append(similarity_matrix)
            self.mappings.append(pd.Series(chunkData.index,index = chunkData["isbn13"]))
        


    def get_similarity_matrix(self,bookData):
        tfidf_matrix = self.tfidf.fit_transform(bookData["book_info"])
        similarity_matrix = linear_kernel(tfidf_matrix,tfidf_matrix)
        return similarity_matrix


    def recommend_tf_idf(self, isbn13):
        book_indices = []
        for i in range(0, self.CHUNK_QUANTITY):
            if(isbn13 in self.mappings[i].index):
                similarity_matrix = self.similarities[i]
                book_index = self.mappings[i][isbn13]
                if(isinstance(book_index,pd.Series)):
                    book_index = book_index[0]
                similarity_score = list(enumerate(similarity_matrix[book_index]))
                # Sort the books based on the similarity scores
                similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)
                similarity_score = similarity_score[1:15]
                book_indices.append([i[0] for i in similarity_score])
        if(len(book_indices) == 0):
            return None
        return (self.bookData[["book_title", "isbn13", "isbn"]].iloc[book_indices[0]])
