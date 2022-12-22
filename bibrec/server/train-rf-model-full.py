from Utils import *

# DATA_DIR = "./data"   # for docker
DATA_DIR = "../../data" # local testing

NORMALIZED_BOOKS_CSV = '%s/normalized_books.csv' % DATA_DIR
NORMALIZED_USERS_CSV = '%s/normalized_users.csv' % DATA_DIR
NORMALIZED_RATINGS_CSV = '%s/normalized_ratings.csv' % DATA_DIR

ENCODED_BOOKS_CSV = "%s/encoded_books.csv" % DATA_DIR
ENCODED_USERS_CSV = "%s/encoded_users.csv" % DATA_DIR

MODEL_FILE_PKL = "%s/rf-model.pkl" % DATA_DIR

# get data
books = get_books()
users = get_users()
ratings = get_ratings(books)

# normalize data
norm_books, norm_users, norm_ratings = get_normalized_data(books_path=NORMALIZED_BOOKS_CSV,
                                                           users_path=NORMALIZED_USERS_CSV,
                                                           ratings_path=NORMALIZED_RATINGS_CSV)

# save normalized files
norm_books.to_csv(NORMALIZED_BOOKS_CSV)
norm_users.to_csv(NORMALIZED_USERS_CSV)

# hot encoded files
encoded_books = hot_encode_books(norm_books)
encoded_users = hot_encode_users(norm_users)

# save encoded files
encoded_books.to_csv(ENCODED_BOOKS_CSV)
encoded_users.to_csv(ENCODED_USERS_CSV)

# train model
rfc = train_model_rf_encoded(encoded_books, encoded_users, norm_ratings)

# saving model takes longer than training it
# print("save model to ", MODEL_FILE_PKL)
# dump_object(MODEL_FILE_PKL, rfc)
