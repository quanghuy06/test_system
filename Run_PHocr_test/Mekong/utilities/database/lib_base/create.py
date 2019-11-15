import os
import json
from pprint import pprint
from pymongo import MongoClient
from pymongo import TEXT

client = MongoClient()
db = client['Mekong']
collection = db['test_case']
collection.drop()


for root, dirs, files in os.walk('../../config/test_cases'):
    for f in files:
        if f.endswith(".json"):
            filename = os.path.join(root, f)
            try:
                with open(filename) as data_file:
                    data = json.load(data_file)
                    pprint(data)
                    collection.insert_many(data)
            except IOError:
                print ("Oops! Can not open file. try again ...")
             

# create indexes of database to support search by free text
collection.create_index([("product", TEXT), ("component", TEXT), ("functionalities", TEXT),
                         ("os", TEXT), ("tags", TEXT)])
