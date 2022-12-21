from flask import current_app as app
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from Utils import *


class ContentBasedFiltering:
    def __init__(self, books, book_data):
        self.books = books
        self.CHUNK_QUANTITY = 50
        self.tfidf = TfidfVectorizer(stop_words='english')

        # data cleaning
        self.book_data = pd.DataFrame(book_data).drop_duplicates(subset=["isbn_10"], ignore_index=True)
        self.book_data.rename(columns={'isbn_10': 'isbn', 'first_sentence.value': 'first_sentence', 'notes.value': 'notes'}, inplace=True)
        self.book_data.isbn = self.book_data.isbn.map(lambda x: str(x).strip()[2:-2])
        self.book_data = self.books.merge(self.book_data, on="isbn", how="inner")
        self.book_data = self.book_data.drop(columns=["Unnamed: 0", "isbn_13", "publishers", "title", "first_sentence.type", "notes.type"])

        self.book_data.subjects = self.book_data.subjects.map(lambda x: str(x).strip()[2:-2])
        self.book_data.genres = self.book_data.genres.map(lambda x: str(x).strip()[2:-2])
        self.book_data = self.book_data.fillna(" ")
        # end data cleaning

        # add book_info column and append relevant data
        self.book_data["book_info"] = self.book_data["book_title"] + " " + self.book_data["subjects"] + " " + self.book_data["genres"]
        self.book_data_preprocessing()

        self.similarities = []
        self.mappings = []
        for i in range(0, self.CHUNK_QUANTITY):
            len_books = self.book_data.shape[0] / self.CHUNK_QUANTITY
            chunk_data = self.book_data[int(i * len_books):int((i + 1) * len_books)]
            chunk_data = chunk_data.reset_index(drop=True)
            similarity_matrix = self.get_similarity_matrix(chunk_data)
            self.similarities.append(similarity_matrix)
            self.mappings.append(pd.Series(chunk_data.index, index=chunk_data["isbn13"]))

    def book_data_preprocessing(self):
        self.book_data["book_info"] = self.book_data["book_info"].astype("string")
        self.book_data["book_info"] = self.book_data["book_info"].apply(lambda x: x.lower())
        self.book_data["book_info"] = self.book_data["book_info"].apply(lambda x: x.replace("(", ''))
        self.book_data["book_info"] = self.book_data["book_info"].apply(lambda x: x.replace(")", ''))
        self.book_data["book_info"] = self.book_data["book_info"].apply(lambda x: x.replace(',', ''))
        self.book_data["book_info"] = self.book_data["book_info"].apply(lambda x: x.replace('.', ''))
        self.book_data["book_info"] = self.book_data["book_info"].apply(lambda x: x.replace("'", ''))
        self.book_data["book_info"] = self.book_data["book_info"].apply(lambda x: x.replace("--", ''))
        self.book_data["book_info"] = self.book_data["book_info"].apply(lambda x: x.replace("  ", ' '))
        self.book_data["book_info"] = self.book_data["book_info"].apply(lambda x: ' '.join(list(set(x.split()))))

    def get_similarity_matrix(self, book_data):
        tfidf_matrix = self.tfidf.fit_transform(book_data["book_info"])
        similarity_matrix = linear_kernel(tfidf_matrix, tfidf_matrix)
        return similarity_matrix

    def recommend_tf_idf(self, isbn13, n=15):
        book_indices = []
        for i in range(0, self.CHUNK_QUANTITY):
            if isbn13 in self.mappings[i].index:
                similarity_matrix = self.similarities[i]
                book_index = self.mappings[i][isbn13]

                if isinstance(book_index, pd.Series):
                    book_index = book_index[0]
                similarity_score = list(enumerate(similarity_matrix[book_index]))
                # Sort the books based on the similarity scores
                similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)
                similarity_score = similarity_score[1:n + 1]

                # Check if all similarities are 0
                if all(i[1] == 0 for i in similarity_score):
                    app.logger.info("No similar items found")
                    return None

                book_indices.append([i[0] for i in similarity_score])

        if len(book_indices) == 0:
            app.logger.info("No similar items found")
            return None
        return self.book_data[["book_title", "isbn13", "isbn"]].iloc[book_indices[0]]
