import random
from collections import defaultdict

import pandas as pd
from flask import Flask
from flask_restful import Api, Resource, reqparse

from Utils import *
from content_based_filtering import ContentBasedFiltering

app = Flask(__name__)
api = Api(app)
app.logger.setLevel(logging.INFO)

# Env vars
app.logger.info("ENVIRONMENT")
app.logger.info(f' RF estimators: {n_estimators}')
app.logger.info(f' RF Jobs: {n_jobs}')
app.logger.info(f' RF random_state: {random_state}')
app.logger.info(f' RF verbose: {verbose}')

app.logger.info("INITIALIZING")

users_dict = defaultdict(list)
users_ratings = pd.DataFrame(columns=["user_id", "isbn", "book_rating"])
books = []
users = []
ratings = []
books_with_mean_count = []

# get data
app.logger.info("Reading data")
books = get_books()
users = get_users()
ratings = get_ratings(books)

# get normalized data
app.logger.info("Reading normalized data")
norm_books, norm_users, norm_ratings = get_normalized_data()

# todo
app.logger.info("Read editions")
book_data = pd.read_csv("./data/editions_dump.csv", sep=",", encoding="utf-8")
books_with_mean_count = add_book_rating_mean_and_count(books, ratings)

# models
app.logger.info("ContentBasedFiltering")
cbf = ContentBasedFiltering(books_with_mean_count, book_data)

# random forest
if exists(MODEL_FILE_PKL):
    # get model
    app.logger.info("Loading RF model")
    rfc = get_model(MODEL_FILE_PKL)
else:
    app.logger.info("Training lightweight RF model")
    # train model with pre-encoded files
    encoded_books = get_encoded_books()
    encoded_users = get_encoded_users()
    # encode from scratch
    # encoded_books = hot_encode_books(norm_books)
    encoded_users = hot_encode_users(norm_users)
    rfc = train_model_rf_encoded(encoded_books, encoded_users, norm_ratings)
    # save file
    # dump_object(MODEL_FILE_PKL, rfc)

app.logger.info("INITIALIZING DONE")


# Register User
class RegisterUser(Resource):
    register_user_args = reqparse.RequestParser()
    register_user_args.add_argument("username", type=str, help="Username is required", required=True)
    register_user_args.add_argument("country", type=str, help="Country of the user")
    register_user_args.add_argument("state", type=str, help="State of the user")
    register_user_args.add_argument("city", type=str, help="City of the user")
    register_user_args.add_argument("age", type=int, help="Age of the user")

    def post(self):
        args = self.register_user_args.parse_args()
        country = args["country"]
        state = args["state"]
        city = args["city"]
        age = args["age"]

        # check if user already exist
        for uid, user_info in users_dict.items():
            if user_info["username"] == args["username"]:
                # update user info if new info us submitted
                if country:
                    user_info["country"] = country
                if state:
                    user_info["state"] = state
                if city:
                    user_info["city"] = city
                if age:
                    user_info["age"] = age

                user_info["user_id"] = uid

                app.logger.info(f'User „{user_info["username"]}“ logged in')
                return user_info

        # add a new user
        user_id = random.getrandbits(32)
        user_info = args.copy()
        users_dict[user_id] = user_info
        args["user_id"] = user_id

        app.logger.info(f'New user named „{user_info["username"]}“ registered')
        return args


# Rate book
class Ratings(Resource):

    def get(self):
        get_ratings_args = reqparse.RequestParser()
        get_ratings_args.add_argument("userId", type=int, help="User id is required and should be a number", required=True, location="args")
        args = get_ratings_args.parse_args()

        user_ratings = users_ratings[users_ratings["user_id"] == args["userId"]]

        json_str = user_ratings.to_json(orient='records')
        parsed = json.loads(json_str)
        return parsed

    def post(self):
        rate_book_args = reqparse.RequestParser()
        rate_book_args.add_argument("userId", type=int, help="User id is required and should be a number", required=True)
        rate_book_args.add_argument("isbn10", type=str, help="ISBN10 of the book to rate is required", required=True)
        rate_book_args.add_argument("rating", type=int, help="Rating for the book is required and should be a number", required=True)
        args = rate_book_args.parse_args()

        global users_ratings
        user_rating = pd.DataFrame.from_dict({"user_id": [args["userId"]], "isbn": [args["isbn10"]], "book_rating": [args["rating"]]})
        new = pd.concat([users_ratings, user_rating], ignore_index=True)
        users_ratings = new

        return f'Book with isbn {args["isbn10"]} rated successfully as {args["rating"]}', 200


# Get recommendations of a user
class UserRecommendations(Resource):
    user_rec_args = reqparse.RequestParser()
    user_rec_args.add_argument("userId", type=int, help="User id is required and should be a number", required=True)
    user_rec_args.add_argument("recommendationCount", type=int, help="The amount of recommendations", default=25)

    def post(self):
        global norm_ratings
        args = self.user_rec_args.parse_args()
        app.logger.info(f'UserRecommendations run prediction for {args["userId"]}')

        user_id = args["userId"]
        user = users_dict.get(user_id)
        if user is not None:
            age = user["age"]
            country = user["country"]
        elif len(norm_users[norm_users["user_id"] == args["userId"]]) == 1:
            user = norm_users[norm_users["user_id"] == args["userId"]].iloc[0]
            age = user.age
            country = user.country
        else:
            raise Exception("No user with the specified id found!")

        if len(users_ratings) > 0:
            user_mean = users_ratings["book_rating"].mean()
            norm_user_ratings = users_ratings
            norm_user_ratings["normalized_ratings"] = users_ratings["book_rating"] - user_mean
            norm_ratings = pd.concat([norm_ratings, norm_user_ratings])

        recommendations = recommend_items_rf(rfc, norm_books, norm_users, norm_ratings, user_id=user_id, age=age, country=country,
                                             numberOfItems=args.recommendationCount)
        app.logger.info('Predictions', recommendations)
        json_str = recommendations.to_json(orient='records')
        parsed = json.loads(json_str)
        return parsed


# Get top books of the user country
class TopInCountry(Resource):
    top_in_country_args = reqparse.RequestParser()
    top_in_country_args.add_argument("userId", type=int, help="The id of the current user")
    top_in_country_args.add_argument("timezoneCountry", type=str, help="The language of the user browser", required=True)
    top_in_country_args.add_argument("recommendationCount", type=int, help="The amount of recommendations", default=25, choices=range(1, 50))

    def post(self):
        args = self.top_in_country_args.parse_args()
        country = args["timezoneCountry"]

        app.logger.info(f'Finding top books for country {country}')

        filtered_country_ratings = get_country_ratings(users, ratings, country)
        app.logger.info(f'Found {len(filtered_country_ratings)} ratings of books in the specified country')

        # get most popular books of country
        books_mean_count_country = add_book_rating_mean_and_count(books, filtered_country_ratings)
        most_rated = get_most_rated_books(books_mean_count_country, 50)
        most_rated = most_rated.sort_values("rating_mean", ascending=False)
        trimmed_most_rated = most_rated[:args["recommendationCount"]]

        app.logger.info(f'Returning {len(trimmed_most_rated)} most popular books of {country}')

        json_str = trimmed_most_rated.to_json(orient='records')
        parsed = json.loads(json_str)
        return parsed


# Get a mix of most popular and least popular items
class Browse(Resource):
    most_rated = None
    least_rated = None

    def init(self):
        if self.most_rated is not None:
            return
        if self.least_rated is not None:
            return
        self.most_rated = get_most_rated_books(books_with_mean_count, 125)
        self.most_rated = self.most_rated.sort_values('rating_mean', ascending=False)
        self.most_rated = self.most_rated[:80]
        self.least_rated = get_least_rated_books(books_with_mean_count, 200)

    def post(self):
        self.init()
        least_rated_sample = self.least_rated.sample(n=20)
        combined_books = pd.concat([self.most_rated, least_rated_sample])
        shuffled_books = combined_books.sample(n=100)
        json_str = shuffled_books.to_json(orient='records')
        parsed = json.loads(json_str)
        return parsed


# Get similar items
class SimilarBooks(Resource):
    similar_Books_args = reqparse.RequestParser()
    similar_Books_args.add_argument("isbn10", type=str, help="The ISBN of the book for which similar books should exist", required=True)
    similar_Books_args.add_argument("userId", type=int, help="The id of the current user", default=0)
    similar_Books_args.add_argument("recommendationCount", type=int, help="The amount of recommendations", default=5)

    def post(self):
        global users_ratings
        args = self.similar_Books_args.parse_args()
        user_id = args["userId"]
        isbn = args["isbn10"]
        number_of_items = args["recommendationCount"]
        isbn13 = str(convert_isbn(args["isbn10"]))

        similar_books = get_similar_books(cbf, books_with_mean_count, ratings, users_ratings, user_id, isbn, isbn13, number_of_items)

        app.logger.info("Sent isbn: " + args["isbn10"])
        app.logger.info("Similar books for isbn: " + isbn13 + " are:")
        app.logger.info(similar_books)
        similar_books = books_with_mean_count.merge(similar_books, on=['isbn13', 'isbn', 'book_title'], how='inner')
        parsed = similar_books.to_json(orient='records')
        return json.loads(parsed)


# Evaluation API
class RecommendItems(Resource):
    rec_items_args = reqparse.RequestParser()
    rec_items_args.add_argument("userId", type=int, help="The id of the current user", location="args")
    rec_items_args.add_argument("age", type=int, help="The age of the user", required=True, location="args")
    rec_items_args.add_argument("locationCountry", type=str, help="The Country of the user", required=True, location="args")
    rec_items_args.add_argument("locationState", type=str, help="The State of the user", location="args")
    rec_items_args.add_argument("locationCity", type=str, help="The City of the user", location="args")
    rec_items_args.add_argument("itemId", type=str, help="The ID of the book (isbn10)", location="args")
    rec_items_args.add_argument("numberOfItems", type=int, help="Number of recommendations to provide", default=10, location="args")

    def get(self):
        args = self.rec_items_args.parse_args()
        isbn = args["itemId"]
        user_id = args["userId"]
        age = args["age"]
        country = args["locationCountry"]
        state = args["locationState"]
        item_count = args["numberOfItems"]
        isbn13 = str(convert_isbn(args["itemId"]))
        # state and city are not used for recommendations

        if user_id and isbn:
            app.logger.info("RANDOM FOREST + CONTENT BASED")
            # return a mix of random forest recommendations and content based recommendations

            # the mix uses 30% similar books and 70% recommendations from the RF
            similar_books_ratio = round(0.3 * item_count)
            rf_books_ratio = round(0.7 * item_count)

            user = norm_users[norm_users["user_id"] == args["userId"]].iloc[0]
            age = user.age
            country = user.country
            state = user.state

            similar_books = get_similar_books(cbf, books_with_mean_count, ratings, users_ratings, user_id, isbn, isbn13, similar_books_ratio)

            rf_books = recommend_items_rf(rfc, norm_books, norm_users, norm_ratings, user_id=user_id,
                                          age=age, country=country, state=state,
                                          numberOfItems=rf_books_ratio)

            items = pd.concat([rf_books, similar_books])
        elif isbn:
            app.logger.info("CONTENT BASED")
            # return item ids from content based filtering
            items = get_similar_books(cbf, books_with_mean_count, ratings, users_ratings, user_id, isbn, isbn13, item_count)

        else:
            # return item ids from random forest recommendations

            app.logger.info("RANDOM FOREST")
            if user_id:
                # get user info from users data set and ignore passed age and country if user_id is passed
                user = norm_users[norm_users["user_id"] == args["userId"]].iloc[0]
                age = user.age
                country = user.country
                state = user.state

            items = recommend_items_rf(rfc, norm_books, norm_users, norm_ratings,
                                       user_id=user_id, age=age, country=country, state=state,
                                       numberOfItems=item_count)

        items_list_json = items["isbn"].to_json(force_ascii=False, orient='records')
        parsed = json.loads(items_list_json)
        return parsed


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


# Frontend APIs
api.add_resource(RegisterUser, "/registerUser")
api.add_resource(Ratings, "/ratings")
api.add_resource(UserRecommendations, "/userRecommendations")
api.add_resource(TopInCountry, "/topInCountry")
api.add_resource(Browse, "/browse")
api.add_resource(SimilarBooks, "/similarBooks")
api.add_resource(RecommendItems, "/recommendItems")

if __name__ == "__main__":
    app.logger.warn("Application ready!")
    app.run(debug=False)
