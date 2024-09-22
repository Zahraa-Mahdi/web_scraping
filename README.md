# Data-science Bootcamp

# Project Overview
  This project is about scraping articles using Python, which is designed to scrape articles from the al-Mayadeen website and store the data in MongoDB, and provide access to the data using Flask API.The result then are displayed in a charts with different type of visualization.

# FEATURES
- parsing sitemap's .
- scraping articles to get detailed information.
- Store data that are scraped into JSON file.
- Store collected data in MongoDB.
- Build a simple web API using Flask to access and analysis the data.
- Create different endpoints that return useful information.

## Technologies Used

- **Python**: For web scraping, data processing, and API creation.
- **Flask**: To build the server and APIs.
- **MongoDB**: For data storage.
- **am5charts**: For generating visualizations.
- **TextBlob** and **Stanza**: For sentiment and entity analysis.
- **Bootstrap**: For front-end design and dashboard layout.
- 
# DEPENDENCIES
We need to download the MongoDB app.

This project relies on following Python libraries:
- **requests** : http requests to retrieve sitemap and articles.
- **Beautifulsoup4** : parse HTML content and extract data from articles.
- **lxml** : parser with beautifulsoup for more efficiency.
- **json** : python library used for handling JSON data , saving scraped articles.
- **ET** : module for parsing and create XML data  used for parse the sitemap.
- **pymongo** : This is the official Python driver for MongoDB. It allows you to interact with your MongoDB.
- **Flask** : A lightweight web framework for Python. It helps you create web applications and APIs.
- **bson** : A package that provides tools for working with BSON (Binary JSON) data, which is used by MongoDB to store data.
- **pandas**
- **scrapy**

you can install the libraries using :
 
```bash
pip install beautifulsoup4
pip install ET
pip install requests
pip install json
pip install pymongo
pip install flask
....
```
# screenshots


