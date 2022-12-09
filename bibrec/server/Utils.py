import pandas as pd
import numpy as np
from collections import defaultdict


def get_books(path):
    books = pd.read_csv(path, sep=";", encoding="latin-1")
    books.columns = books.columns.map(prepare_string)
    books.year_of_publication = pd.to_numeric(books.year_of_publication, errors='coerce')
    # Replace years equal to 0 with NaN
    books.year_of_publication.replace(0, np.nan, inplace=True)
    books.fillna(round(books.year_of_publication.mean()))
    books["isbn13"] = books.isbn.map(convert_isbn)
    books = books[books.isbn13.notna()]

    return books

    
    
def get_users(path):
    users = pd.read_csv(path, sep=";", encoding="latin-1")
    # cleaned column names
    users.columns = users.columns.map(prepare_string)
    # replaced ages below 6 and above 110 with NaN
    users.loc[(users.age<6) | (users.age>110), 'age'] = np.nan
    # replaced NaN ages with random ages from normal distribution
    temp_age_series = pd.Series(np.random.normal(loc=users.age.mean(), scale=users.age.std(), size=users.user_id[users.age.isna()].count()))
    pos_age_series=np.abs(temp_age_series)
    users = users.sort_values('age',na_position='first').reset_index(drop=True)
    users.age.fillna(pos_age_series, inplace = True)  
    users = users.sort_values('user_id').reset_index(drop=True)
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
    ratings["isbn"] = ratings.isbn.map(convert_isbn)
    
    return ratings

def prepare_string(string):
    return str(string).strip().lower().replace('-', '_')

def convert_isbn(id):
    isbn = str(id)
    if len(isbn) == 10:
        isbn = isbn.rstrip(isbn[-1])
        isbn = "978" + isbn
        sum = 0
        for i in range(len(isbn)):
            try:
                int(isbn[i])
            except ValueError:
                return np.nan
            if i % 2 == 0:
                sum += int(isbn[i])
            else:
                sum += int(isbn[i]) * 3
        check_digit = 10 - (sum % 10)
        if check_digit == 10:
            check_digit = 0
        isbn += str(check_digit)
        return isbn
    elif len(isbn) == 13:
        return isbn
    else:
        return np.nan