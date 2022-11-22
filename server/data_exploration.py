from Utils import book_parser, user_parser, rating_parser
import matplotlib.pyplot as plt
import numpy as np

books = book_parser("./data/BX-Books.csv")
users = user_parser("./data/BX-Users.csv", True)
book_ratings, user_ratings = rating_parser("./data/BX-Book-Ratings.csv")
print(users)
plt.hist(users.Age, bins=100)
plt.show()
