import json
import requests
from Utils import *

booksCopy = get_books()
# Test to parse json data from openlibrary dump to csv
json_data = None
# with open('../../data/testdata.txt') as f:
#     json_data = json.load(f)

with open('../../data/ol_dump_editions_2010-12-31.txt') as f:
    json_data = json.load(f.read())

editions_data = pd.json_normalize(json_data)

print(editions_data.columns)

editions_data = editions_data[editions_data['isbn_10'].isin(booksCopy['isbn'])]

editions_data.to_csv('../../data/editions_data.csv')
# ran into memory error, because dump was to large for ram, so we decided to fetch each book individually



# fetch data from openlibrary for every single isbn in the dataset

# limit amout of request for each run
testBooks = booksCopy[240000:280000]
print(testBooks.count())

bookList= testBooks['isbn13'].to_list()
editions_data = pd.DataFrame()
counter = 0
for id in bookList:
    counter = counter + 1
    print(str(counter)+"/"+str(len(bookList)))
    url = "https://openlibrary.org/isbn/" + str(id) + ".json"
    res = requests.get(url)
    if res.status_code == 200:
        response = json.loads(res.text)
    if(len(editions_data)> 0):
        editions_data = pd.concat([editions_data,pd.json_normalize(response)])
    else:
        editions_data = pd.json_normalize(response)