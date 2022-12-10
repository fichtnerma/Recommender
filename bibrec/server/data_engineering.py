from Utils import get_books
import pandas as pd
import numpy as np

books = get_books("../../data/BX-Books.csv")

editions_data = pd.read_csv("../../data/ol_dump_editions_latest.csv")

editions_data = editions_data[books['isbn'].isin(books['isbn'])]

editions_data.drop(["by_statement",""])
