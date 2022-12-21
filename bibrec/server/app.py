import json
import random
from collections import defaultdict

from flask import Flask
from flask_restful import Api, Resource, reqparse

from Utils import *
from content_based_filtering import ContentBasedFiltering

app = Flask(__name__)
api = Api(app)

users_dict = defaultdict(list)
users_ratings = pd.DataFrame(columns=["user_id", "isbn", "book_rating"])

# get data
books = get_books()
users = get_users()
ratings = get_ratings(books)

# get normalized data
# norm_books, norm_users, norm_ratings = normalized_data(books, users, ratings)
norm_books, norm_users, norm_ratings = get_normalized_data()

# todo
bookData = pd.read_csv("./data/editions_dump.csv", sep=",", encoding="utf-8")
books_with_mean_count = add_book_rating_mean_and_count(books, ratings)

# models
cbf = ContentBasedFiltering(books_with_mean_count, bookData)

logging.info("Applicaton ready!")

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

        # check if user already exist
        for uid, user_info in users_dict.items():
            if user_info["username"] == args["username"]:
                # update user info if new info us submitted
                user_info["country"] = args["country"]
                user_info["state"] = args["state"]
                user_info["city"] = args["city"]
                user_info["age"] = args["age"]

                # create return dict
                temp_user = user_info.copy()
                temp_user["userId"] = uid

                app.logger.info(f'User „{user_info["username"]}“ logged in')
                return temp_user

        # add a new user
        user_id = random.getrandbits(32)
        user_info = args.copy()
        users_dict[user_id] = user_info
        args["userId"] = user_id

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
        args = self.user_rec_args.parse_args()
        app.logger.info(f'UserRecommendations run prediction for ', args.userId)
        user = users[users["user_id"] == args.userId]
        recommendations = recommend_items_rf(norm_books, norm_users, norm_ratings, user.userId, user.age, user.country, numberOfItems=args.recommendationCount)
        app.logger.info('Predictions', recommendations)
        json_str = recommendations.to_json(orient='records')
        parsed = json.loads(json_str)
        return parsed


# Get top books of the user country
class TopInCountry(Resource):
    top_in_country_args = reqparse.RequestParser()
    top_in_country_args.add_argument("userId", type=int, help="The id of the current user")
    top_in_country_args.add_argument("timezoneCountry", type=str, help="The language of the user browser", required=True)
    top_in_country_args.add_argument("recommendationCount", type=int, help="The amount of recommendations", default=25)

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
    most_rated = get_most_rated_books(books_with_mean_count, 125)
    most_rated = most_rated.sort_values('rating_mean', ascending=False)
    most_rated = most_rated[:80]

    least_rated = get_least_rated_books(books_with_mean_count, 200)

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

    def post(self):
        args = self.similar_Books_args.parse_args()
        isbn13 = str(convert_isbn(args["isbn10"]))
        similar_books = cbf.recommend_tf_idf(isbn13, args["recommendationCount"] + 1)

        # return sample of most popular if no similar items are found
        if similar_books is None:
            app.logger.info(f'No similar books found. Returning {args["recommendationCount"]} most popular')
            most_rated = get_most_rated_books(books_with_mean_count, 50)
            mask = most_rated["isbn"] != args["isbn10"]
            most_rated = most_rated[mask]
            most_rated = most_rated.sort_values('rating_mean', ascending=False)
            json_str = most_rated.sample(n=args["recommendationCount"]).to_json(orient='records')
            parsed = json.loads(json_str)
            return parsed

        # filter sent book out of the similar items if present
        mask = similar_books["isbn"] != args["isbn10"]
        similar_books = similar_books[mask]
        similar_books = similar_books[:args["recommendationCount"]]

        app.logger.info("Sent isbn: " + args["isbn10"])
        app.logger.info("Similar books for isbn: " + isbn13 + " are:")
        app.logger.info(similar_books)
        similar_books = books_with_mean_count.merge(similar_books, on=['isbn13', 'isbn', 'book_title'], how='inner')
        parsed = similar_books.to_json(orient='records')
        return json.loads(parsed)


# Get recommend items
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
        userId = args["userId"]
        age = args["age"]
        country = args["locationCountry"]
        state = args["locationState"]
        city = args["locationCity"]
        nItems = args["numberOfItems"]
        isbn13 = str(convert_isbn(args["itemId"]))
        cbf_recommendations = []
        rf_recommendations = []
        if isbn:
            cbf_recommendations.append(cbf.recommend_tf_idf(isbn13, nItems))
        if userId:
            rated_books = ratings[ratings["user_id"] == userId]["isbn13"].tolist()
            for book in rated_books:
                cbf_recommendations.append(cbf.recommend_tf_idf(book, 3))
        if age and country and state and city:
            rf_recommendations = rf_recommendations.concat([rf_recommendations, cbf.recommend_tf_idf(isbn13, nItems)])

        rec_cbf = []
        for book in cbf_recommendations:
            rec_cbf.append(book["isbn13"].tolist())
        rec_cbf = list(dict.fromkeys(flatten(rec_cbf)))
        app.logger.info("Recommendations for user: ")
        app.logger.info(rec_cbf)
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
        app.logger.info(f'RecommendItemsRF run prediction')
        recommendations = recommend_items_rf(norm_books,norm_users, norm_ratings, args.userId, args.age, args.locationCountry, args.locationState, args.locationCity, args.itemId, args.numberOfItems)
        app.logger.info('Predictions', recommendations[:args.numberOfItems])
        json_str = recommendations[:args.numberOfItems].to_json(orient='records')
        parsed = json.loads(json_str)
        return parsed


# Frontend APIs
api.add_resource(RegisterUser, "/registerUser")
api.add_resource(Ratings, "/ratings")
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
