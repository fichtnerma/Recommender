import json
from Utils import *

booksCopy = get_books()

json_data = None
# with open('../../data/testdata.txt') as f:
#     json_data = json.load(f)

with open('../../data/ol_dump_editions_2010-12-31.txt') as f:
    json_data = json.load(f.read())

editions_data = pd.json_normalize(json_data)

print(editions_data.columns)


editions_data = editions_data[editions_data['isbn_10'].isin(booksCopy['isbn'])]

editions_data.to_csv('../../data/editions_data.csv')
