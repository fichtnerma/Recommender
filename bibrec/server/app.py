import random
from collections import defaultdict

import pandas as pd
from content_based_filtering import ContentBasedFiltering
from flask import Flask
from flask_restful import Api, Resource, reqparse

from Utils import *

app = Flask(__name__)
api = Api(app)

users_dict = defaultdict(list)
books = get_books()
ratings = get_ratings()
bookData = pd.read_csv("./data/editions_dump.csv", sep=",", encoding="utf-8")
explicit_ratings = ratings[ratings.book_rating != 0]
filtered_ratings = filter_ratings(explicit_ratings, books)
books_with_mean_count = add_mean_and_count(books, filtered_ratings)

books_with_mean_count.rename(columns={'isbn': 'isbn10', 'book_title': 'title', 'book_author': 'author', 'year_of_publication': 'pubYear', 'image_url_s': 'imageUrlSmall',
                                      'image_url_m': 'imageUrlMedium', 'image_url_l': 'imageUrlLarge'}, inplace=True)


# Register User
class RegisterUser(Resource):
    user_id_key = "userId"
    username_key = "username"
    country_key = "country"
    state_key = "state"
    city_key = "city"
    age_key = "age"
    register_user_args = reqparse.RequestParser()
    register_user_args.add_argument(username_key, type=str, help="Username is required", required=True)
    register_user_args.add_argument(country_key, type=str, help="Country of the user")
    register_user_args.add_argument(state_key, type=str, help="State of the user")
    register_user_args.add_argument(city_key, type=str, help="City of the user")
    register_user_args.add_argument(age_key, type=int, help="Age of the user")

    def post(self):
        args = self.register_user_args.parse_args()

        # check if user already exist
        for uid, user_info in users_dict.items():
            if user_info[self.username_key] == args[self.username_key]:
                # update user info if new info us submitted
                user_info[self.country_key] = args[self.country_key]
                user_info[self.state_key] = args[self.state_key]
                user_info[self.city_key] = args[self.city_key]
                user_info[self.age_key] = args[self.age_key]

                # create return dict
                temp_user = user_info.copy()
                temp_user[self.user_id_key] = uid

                app.logger.info(f'User „{user_info[self.username_key]}“ logged in')
                return temp_user

        # add a new user
        user_id = random.getrandbits(32)
        user_info = args.copy()
        users_dict[user_id] = user_info
        args[self.user_id_key] = user_id

        app.logger.info(f'New user named „{user_info[self.username_key]}“ registered')
        return args


# Rate book
class RateBook(Resource):
    rate_book_args = reqparse.RequestParser()
    rate_book_args.add_argument("userId", type=int, help="User id is required and should be a number", required=True)
    rate_book_args.add_argument("isbn10", type=str, help="ISBN10 of the book to rate is required", required=True)
    rate_book_args.add_argument("rating", type=int, help="Rating for the book is required and should be a number", required=True)

    def post(self):
        args = self.rate_book_args.parse_args()

        return f'Book with isbn {args["isbn10"]} rated successfully as {args["rating"]}', 200


# Get recommendations of a user
class UserRecommendations(Resource):
    user_rec_args = reqparse.RequestParser()
    user_rec_args.add_argument("userId", type=int, help="User id is required and should be a number", required=True)
    user_rec_args.add_argument("recommendationCount", type=int, help="The amount of recommendations", default=25)

    def post(self):
        args = self.user_rec_args.parse_args()

        json_str = books_with_mean_count.sample(n=args["recommendationCount"]).to_json(orient='records')
        parsed = json.loads(json_str)
        return parsed


# Get top books of the user country
class TopInCountry(Resource):
    top_in_country_args = reqparse.RequestParser()
    top_in_country_args.add_argument("userId", type=int, help="The id of the current user")
    top_in_country_args.add_argument("browserLang", type=str, help="The language of the user browser")
    top_in_country_args.add_argument("recommendationCount", type=int, help="The amount of recommendations", default=25)

    def post(self):
        args = self.top_in_country_args.parse_args()
        json_str = books_with_mean_count.sample(n=args["recommendationCount"]).to_json(orient='records')
        parsed = json.loads(json_str)
        return parsed


# Get a mix of most popular and least popular items
class Browse(Resource):
    most_rated = get_most_rated_books(books_with_mean_count, 80)
    least_rated = get_least_rated_books(books_with_mean_count, 100)

    def post(self):
        least_rated_sample = self.least_rated.sample(n=20)
        combined_books = pd.concat([self.most_rated, least_rated_sample])
        shuffled_books = combined_books.sample(n=100)
        json_str = shuffled_books.to_json(orient='records')
        parsed = json.loads(json_str)
        return parsed


# Get similar items
class SimilarBooks(Resource):
    similar_Books_args = reqparse.RequestParser()
    similar_Books_args.add_argument("isbn10", type=str, help="The ISBN of the book for which similar books should be found", required=True)
    similar_Books_args.add_argument("userId", type=int, help="The id of the current user", default=0)
    similar_Books_args.add_argument("recommendationCount", type=int, help="The amount of recommendations", default=5)
    cbf = ContentBasedFiltering(bookData)

    def post(self):
        args = self.similar_Books_args.parse_args()
        isbn13 = convert_isbn(args["isbn10"])
        similar_books = self.cbf.recommend_tf_idf(isbn13)
        parsed = json.loads(similar_books)
        return parsed
        # return "Similar books"


# Get recommend items
class RecommendItems(Resource):
    rec_items_args = reqparse.RequestParser()
    rec_items_args.add_argument("userId", type=int, help="The id of the current user")
    rec_items_args.add_argument("age", type=int, help="The age of the user", required=True)
    rec_items_args.add_argument("locationCountry", type=str, help="The Country of the user", required=True)
    rec_items_args.add_argument("locationState", type=str, help="The State of the user")
    rec_items_args.add_argument("locationCity", type=str, help="The City of the user")
    rec_items_args.add_argument("itemId", type=int, help="The ID of the book (isbn10)")
    rec_items_args.add_argument("numberOfItems", type=int, help="Number of recommendations to provide", default=10)

    def post(self):
        args = self.rec_items_args.parse_args()

        json_str = books_with_mean_count.sample(n=args["numberOfItems"]).to_json(orient='records')
        parsed = json.loads(json_str)
        return parsed


# Evaluation API
class RecommendItemsRF(Resource):
    args = reqparse.RequestParser()
    args.add_argument("userId", type=int, help="The id of the current user")
    args.add_argument("age", type=int, help="The age of the user", required=True)
    args.add_argument("locationCountry", type=str, help="The Country of the user", required=True)
    args.add_argument("locationState", type=str, help="The State of the user")
    args.add_argument("locationCity", type=str, help="The City of the user")
    args.add_argument("itemId", type=int, help="The ID of the book (isbn10)")
    args.add_argument("numberOfItems", type=int, help="Number of recommendations to provide", default=10)

    def post(self):
        args = self.args.parse_args()
        return recommend_items_rf(args.userId, args.age, args.locationCountry, args.locationState, args.locationCity, args.itemId, args.numberOfItems)


# Frontend APIs
api.add_resource(RegisterUser, "/registerUser")
api.add_resource(RateBook, "/rateBook")
api.add_resource(UserRecommendations, "/userRecommendations")
api.add_resource(TopInCountry, "/topInCountry")
api.add_resource(Browse, "/browse")
api.add_resource(SimilarBooks, "/similarBooks")
api.add_resource(RecommendItems, "/recommendItems")
api.add_resource(RecommendItemsRF, "/recommendItemsRF")


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == "__main__":
    app.run(debug=True)
