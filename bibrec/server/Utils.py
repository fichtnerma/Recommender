import pandas as pd
import numpy as np
from collections import defaultdict


def get_books(path):
    books = pd.read_csv(path, sep=";", encoding="latin-1")
    books.columns = books.columns.map(prepare_string)
    books.year_of_publication = pd.to_numeric(books.year_of_publication, errors='coerce')
    # Replace years equal to 0 with NaN
    books.year_of_publication.replace(0, np.nan, inplace=True)

    return books

    
    
def get_users(path):
    users = pd.read_csv(path, sep=";", encoding="latin-1")
    # cleaned column names
    users.columns = users.columns.map(prepare_string)
    # replaced ages below 6 and above 110 with NaN
    users.loc[(users.age<6) | (users.age>110), 'age'] = np.nan
    # seperate location into city, state and country
    location_seperated = users.location.str.split(',', 2, expand=True)
    location_seperated.columns = ['city', 'state', 'country']
    users = users.join(location_seperated)
    users.drop(columns=['location'], inplace=True)
    # replaced empty strings with NaN
    users.country.replace('', np.nan, inplace=True)
    users.state.replace('', np.nan, inplace=True)
    users.city.replace('', np.nan, inplace=True)

    return users



def get_ratings(path):
    ratings = pd.read_csv(path, sep=";", encoding="latin-1")
    ratings.columns = ratings.columns.map(prepare_string)
    
    return ratings

def prepare_string(string):
    return str(string).strip().lower().replace('-', '_')

