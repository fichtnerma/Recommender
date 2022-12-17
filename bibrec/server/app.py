import json
import random
from collections import defaultdict

from flask import Flask
from flask_restful import Api, Resource, reqparse

from Utils import get_books

app = Flask(__name__)
api = Api(app)


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

    users_dict = defaultdict(list)

    def post(self):
        args = self.register_user_args.parse_args()

        # check if user already exist
        for uid, user_info in self.users_dict.items():
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
        self.users_dict[user_id] = user_info
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

        return f'Book with isbn {args["isbn10"]} rated successfully', 200


books = get_books()
books.rename(columns={'isbn': 'isbn10', 'book_title': 'title', 'book_author': 'author', 'year_of_publication': 'pubYear', 'image_url_s': 'imageUrlSmall',
                      'image_url_m': 'imageUrlMedium', 'image_url_l': 'imageUrlLarge'}, inplace=True)


# Get recommendations of a user
class UserRecommendations(Resource):
    user_rec_args = reqparse.RequestParser()
    user_rec_args.add_argument("userId", type=int, help="User id is required and should be a number", required=True)
    user_rec_args.add_argument("recommendationCount", type=int, help="The amount of recommendations", default=25)

    def post(self):
        args = self.user_rec_args.parse_args()

        json_str = books.sample(n=20).to_json(orient='records')
        parsed = json.loads(json_str)
        return parsed


# Get top books of the user country
class TopInCountry(Resource):
    top_in_country_args = reqparse.RequestParser()
    top_in_country_args.add_argument("userId", type=int, help="The id of the current user")
    top_in_country_args.add_argument("browserLang", type=str, help="The language of the user browser")

    def post(self):
        args = self.top_in_country_args.parse_args()
        return args


# Get a mix of most popular and least popular items
class Browse(Resource):
    browse_args = reqparse.RequestParser()
    browse_args.add_argument("userId", type=int, help="The id of the current user")

    def post(self):
        args = self.browse_args.parse_args()
        return args


# Get similar items
class SimilarBooks(Resource):
    similar_Books_args = reqparse.RequestParser()
    similar_Books_args.add_argument("isbn10", type=int, help="The ISBN of the book for which similar books should be found", required=True)
    similar_Books_args.add_argument("userId", type=int, help="The id of the current user")

    def post(self):
        args = self.similar_Books_args.parse_args()
        return args


api.add_resource(RegisterUser, "/registerUser")
api.add_resource(RateBook, "/rateBook")
api.add_resource(UserRecommendations, "/userRecommendations")
api.add_resource(TopInCountry, "/topInCountry")
api.add_resource(Browse, "/browse")
api.add_resource(SimilarBooks, "/similarBooks")

if __name__ == "__main__":
    app.run(debug=True)
