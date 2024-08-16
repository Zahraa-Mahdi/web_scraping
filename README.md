# WEB_SCRAPING
This project is about web scraping using Python, which is designed to collect articles from the al-Mayadeen website by parsing the sitemaps to find the URLs, then scraping the metadata from each article and saving them in a JSON file.

# FEATURES
- parsing sitemap's .
- scraping articles to get detailed information.
- Store data that are scraped into JSON file.

# DEPENDENCIES
 
This project relies on following Python libraries:
- requests : http requests to retrieve sitemap and articles.
- Beautifulsoup4 : parse HTML content and extract data from articles.
- lxml : parser with beautifulsoup for more efficiency.
- json : python library used for handling JSON data , saving scraped articles.
- ET : module for parsing and create XML data  used for parse the sitemap.
 
you can install the libraries using :
 
```bash
pip install beautifulsoup4
pip install ET
pip install requests
pip install json