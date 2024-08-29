# Data-science Bootcamp
- Task 1 :This project is about web scraping using Python, which is designed to collect articles from the al-Mayadeen website by parsing the sitemaps to find the URLs, then scraping the metadata from each article and saving them in a JSON file. 
- Task 2 :This project was about to store the data i have in the JSON files in a MongoDB, and provide access to the data using Flask API.

# FEATURES
- parsing sitemap's .
- scraping articles to get detailed information.
- Store data that are scraped into JSON file.
- Store collected data in MongoDB.
- Build a simple web API using Flask to access and analysis the data.
- Create different endpoints that return useful information.

# DEPENDENCIES
We need to download the MongoDB app.

This project relies on following Python libraries:
- requests : http requests to retrieve sitemap and articles.
- Beautifulsoup4 : parse HTML content and extract data from articles.
- lxml : parser with beautifulsoup for more efficiency.
- json : python library used for handling JSON data , saving scraped articles.
- ET : module for parsing and create XML data  used for parse the sitemap.
- pymongo : This is the official Python driver for MongoDB. It allows you to interact with your MongoDB.
- Flask : A lightweight web framework for Python. It helps you create web applications and APIs.
- bson : A package that provides tools for working with BSON (Binary JSON) data, which is used by MongoDB to store data.

you can install the libraries using :
 
```bash
pip install beautifulsoup4
pip install ET
pip install requests
pip install json
pip install pymongo
pip install flask

