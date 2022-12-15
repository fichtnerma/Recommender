from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


# Register User
class RegisterUser(Resource):
    def post(self):
        return "User registered"


# Rate book
class RateBook(Resource):
    def post(self):
        return "Book rated"


# Get recommendations of a user
class UserRecommendations(Resource):
    def post(self):
        return "User recommendations"


# Get top books of the user country
class TopInCountry(Resource):
    def post(self):
        return "Top in country"


# Get a mix of most popular and least popular items
class Browse(Resource):
    def post(self):
        return "Browsing items"


# Get similar items
class SimilarItems(Resource):
    def post(self):
        return "Similar items"


api.add_resource(RegisterUser, "/registerUser")
api.add_resource(RateBook, "/rateBook")
api.add_resource(UserRecommendations, "/userRecommendations")
api.add_resource(TopInCountry, "/topInCountry")
api.add_resource(Browse, "/browse")
api.add_resource(SimilarItems, "/similarItems")

if __name__ == "__main__":
    app.run(debug=True)
