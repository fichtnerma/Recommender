# BibRec
__Team 1__: Fabian Untermoser, Johannes Munker, Markus Fichtner

Recommending Books à la Netflix.

## Build
```sh
# start the container and show logs
make run logs
```

Change the configuration for the random forest in the `docker-compose.yml` file.
```text
# number of decision trees to build
RF_ESTIMATORS=100
# number of cpu cores to assign for training
RF_JOBS=3
```

Access the Frontend on `http://localhost:3000`.

Access the Backend on `http://localhost:4000`.

__Prerequisites__:
- Docker Compose
- Around 13GB of free RAM

## Documentation
This project is a recommendation system for books.
Users can rate a book form a scale of 1-10 stars.
Based on the information the user provides on login, the system recommends books the user might like.
When viewing a book, similar books are recommended as well.

The __Random Forest__ algorithm is used as Model-Based Collaborative Filtering Algorithm
in order to predict ratings for a potential user given his __age__, __country__ and __state__
on books given their __Year-of-Publication__ and which __Publisher__ they belong from.

A Content Based Filtering approach is used to recommend similar books.
Similarity is inferred by calculating the [_term frequency–inverse document frequency_](https://en.wikipedia.org/wiki/Tf%E2%80%93idf)
from the books title and its genres.

### System Description
- Frontend: React, Material UI
- Backend: REST API mit Flask
- Infrastructure: Docker + Compose
- Algorithms: Random Forest & Content Based Filtering

### Libraries
- Initial research with the [CaseRecommender](http://caserec.github.io/CaseRecommender/)
- RS Algorithms used from [Scikit-Learn](https://scikit-learn.org/)

### Dataset
As a base the [BookCrossing](http://www2.informatik.uni-freiburg.de/~cziegler/BX/) was used for this project.

The dataset is furthermore enhanced with genres taken from [OpenLibrary](https://openlibrary.org/).

Normalized & hot-encoded versions are stored as files as well to increase startup performance.

| Dataset                      | Original                            | Normalized                                        | Hot-Encoded                                 |
|------------------------------|-------------------------------------|---------------------------------------------------|---------------------------------------------|
| BookCrossing Books Dataset   | [Books](data/BX-Books.csv)          | [Normalized Books](data/normalized_books.csv)     | [Hot Encoded Books](data/encoded_books.csv) |
| BookCrossing Users Dataset   | [Users](data/BX-Users.csv)          | [Normalized Users](data/normalized_users.csv)     | [Hot Encoded Users](data/encoded_users.csv) |
| BookCrossing Ratings Dataset | [Ratings](data/BX-Book-Ratings.csv) | [Normalized Ratings](data/normalized_ratings.csv) |                                             |

### Data Exploration & Normalization
These Notebook files showcase the data exploration & normalization in more detail.
- [Data Exploration](data-exploration.ipynb): Exploration of the original BookCrossing Dataset
- [Data Normalization](data-normalization.ipynb): Showcase of the Data Normalization
- [Data Hot-Encoding](data-hot-encoding.ipynb): Export Hot-Encoded Dataset

__Summary__:
- Data has been filtered to remove books and ratings with invalid ISBNs, duplicate books, and ratings for non-existent users or books. Only explicit ratings are being used.
- Age and country are required evaluation parameters, while state is optional but treated equally. City is not used.
- The user dataset has undergone basic cleaning including sanitization of column names, replacing invalid ages with the average age, and splitting location into country, state, and city.
- The ratings dataset has undergone basic cleaning including sanitization of column names, filtering out ratings with non or invalid ISBNs and for unknown books, converting ISBNs to uppercase and ISBN-13 standard, and adjusting ratings for bias correction and normalizing publication years.
- The books dataset has undergone normalization including rating bias correction, publication year normalization, and publisher categorization.

### Baseline Comparison & Evaluation
- [Baseline Most Popular](baseline.ipynb): Showcase of the Baseline using the Best Rated Books Algorithm
- [Baseline CaseRecommender](baseline_case_recommender.ipynb): Showcase of the Baseline using the CaseRecommender Library
- [Random Forest Model](notebooks/rf-model-50.ipynb): Evaluation of Random Forest Algorithm
- [Random Forest Model 50](notebooks/rf-model-50.ipynb): Evaluation of Random Forest Algorithm using 50 Decision Trees
- [Content Based Filtering](contentBasedFiltering.ipynb): Showcase Content Based Filtering

### Scripts
These utility scripts were used for testing
- [Train RF Model](bibrec/server/train-rf-model-full.py): Normalize, hot-encode and train with all data from scratch
- [Train RF Model Lightweight](bibrec/server/train-rf-model.py): Uses stored normalized & hot-encoded files

### API Documentation
- [Evaluation API](bibrec/api/openapi.yaml)

__Strategy for the Evaluation API__:
- If only user data (age, country, and state) is given, books will be predicted using a random forest model with age, country, and state as features.
- If user data (age, country, and state) and a user ID are given, the user's rated books will be used to find similar books through a content-based filtering approach (such as TF-IDF) and these books will be mixed into the results list from the random forest prediction (hybrid approach).
- If user data (age, country, and state) and an item ID are given, similar books to the user's rated books will be returned. If no similar books are found, the most popular items will be returned.
- If user data (age, country, and state), a user ID, and an item ID are given, it is possible that a hybrid approach will be used.

Example Call:
```sh
http GET :4000/recommendItemsRF age==20 locationCountry=="usa" numberOfItems=3
```