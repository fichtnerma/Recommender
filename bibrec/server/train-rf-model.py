from Utils import *

# DATA_DIR = "./data"   # for docker
DATA_DIR = "../../data" # local testing

NORMALIZED_BOOKS_CSV = '%s/normalized_books.csv' % DATA_DIR
NORMALIZED_USERS_CSV = '%s/normalized_users.csv' % DATA_DIR
NORMALIZED_RATINGS_CSV = '%s/normalized_ratings.csv' % DATA_DIR

ENCODED_BOOKS_CSV = "%s/encoded_books.csv" % DATA_DIR
ENCODED_USERS_CSV = "%s/encoded_users.csv" % DATA_DIR

MODEL_FILE_PKL = "%s/rf-model.pkl" % DATA_DIR

print("get normalized data")
norm_books, norm_users, norm_ratings = get_normalized_data(books_path=NORMALIZED_BOOKS_CSV,
                                                           users_path=NORMALIZED_USERS_CSV,
                                                           ratings_path=NORMALIZED_RATINGS_CSV)

print("get encoded data")
encoded_books = get_encoded_books(ENCODED_BOOKS_CSV)
encoded_users = get_encoded_users(ENCODED_USERS_CSV)

print("train model")
rfc = train_model_rf_encoded(encoded_books, encoded_users, norm_ratings)

# saving model takes longer than training it
# print("save model to ", MODEL_FILE_PKL)
# dump_object(MODEL_FILE_PKL, rfc)
