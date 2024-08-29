import pymongo
import json

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["almayadeen"]
collection = db["articles"]

# List of JSON file names
json_files = ['articles_1.json', 'articles_2.json', 'articles_3.json', 'articles_4.json', 'articles_5.json']

# Loop through each JSON file and insert the data into MongoDB
for file_name in json_files:
    with open(file_name, encoding='utf-8') as f:
        data = json.load(f)
        collection.insert_many(data)
        print(f"Data from {file_name} inserted successfully!")

print("All data inserted successfully!")
