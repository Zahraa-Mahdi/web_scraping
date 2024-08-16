
import json
from dataclasses import dataclass, field
import time
from typing import List, Optional
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import requests

@dataclass
class Article:
    url: str
    postid: Optional[str] = None
    title: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    thumbnail: Optional[str] = None
    video_duration: Optional[str] = None
    word_count: Optional[int] = None
    lang: Optional[str] = None
    published_time: Optional[str] = None
    last_updated: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    classes: List[dict] = field(default_factory=list)
    full_text: Optional[str] = None

class SitemapParser:
    def __init__(self, sitemap_index_url):
        self.sitemap_index_url = sitemap_index_url

    def get_monthly_sitemaps(self) -> List[str]:
        response = requests.get(self.sitemap_index_url)
        root = ET.fromstring(response.content)
        ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        sitemap_urls = [element.text for element in root.findall('ns:sitemap/ns:loc', ns)]
        return sitemap_urls

    def get_article_urls(self, sitemap_url: str) -> List[str]:
        response = requests.get(sitemap_url)
        root = ET.fromstring(response.content)
        ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        article_urls = [element.text for element in root.findall('ns:url/ns:loc', ns)]
        return article_urls

class ArticleScraper:
    def scrape_article(self, url: str) -> Article:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        tawsiyat_metadata_script = soup.find('script', type='text/tawsiyat')
        if not tawsiyat_metadata_script:
            raise ValueError("NO TEXT/tawsiyat SCRIPT FOUND!")

        tawsiyat_data = json.loads(tawsiyat_metadata_script.string)
        article_bodytag = soup.find_all('p')
        full_text = ''.join([tag.get_text(strip=True) for tag in article_bodytag])

        article = Article(
            url=tawsiyat_data.get('url'),
            postid=tawsiyat_data.get('postid'),
            title=tawsiyat_data.get('title'),
            keywords=tawsiyat_data.get('keywords').split(',') if isinstance(tawsiyat_data.get('keywords'), str) else None,
            thumbnail=tawsiyat_data.get('thumbnail'),
            video_duration=tawsiyat_data.get('video_duration'),
            word_count=int(tawsiyat_data.get('word_count')) if tawsiyat_data.get('word_count') else None,
            lang=tawsiyat_data.get('lang'),
            published_time=tawsiyat_data.get('published_time'),
            last_updated=tawsiyat_data.get('last_updated'),
            description=tawsiyat_data.get('description'),
            author=tawsiyat_data.get('author'),
            classes=tawsiyat_data.get('classes'),
            full_text=full_text,
        )
        return article

class FileUtil:
    @staticmethod
    def save_article(articles: List[Article], file_name: str):
        article_data = [article.__dict__ for article in articles]
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(article_data, f, ensure_ascii=False, indent=4)

def main():
    sitemap_index_url = 'https://www.almayadeen.net/sitemaps/all.xml'
    sitemap_parser = SitemapParser(sitemap_index_url)
    article_scraper = ArticleScraper()

    monthly_sitemap_urls = sitemap_parser.get_monthly_sitemaps()
    total_articles = 0
    file_count = 1
    articles = []

    for sitemap_url in monthly_sitemap_urls:
        try:
            year_month = sitemap_url.split('/')[-1].replace('sitemap-', '').replace('.xml', '')
            article_urls = sitemap_parser.get_article_urls(sitemap_url)
            print(f"Found {len(article_urls)} articles in {sitemap_url}")

            for url in article_urls:
                try:
                    article = article_scraper.scrape_article(url)
                    articles.append(article)
                    print(f"Scraped: {url}")
                    total_articles += 1

                    if total_articles >= 2000 * file_count:
                        file_name = f"articles_{file_count}.json"
                        FileUtil.save_article(articles, file_name)
                        print(f"Saved articles to {file_name}")
                        articles = []
                        file_count += 1

                    if total_articles >= 10000:
                        break
                except Exception as e:
                    print(f"Error scraping {url}: {e}")

            if total_articles >= 10000:
                break

        except Exception as e:
            print(f"Error processing {sitemap_url}: {e}")

    if articles:
        file_name = f"articles_{file_count}.json"
        FileUtil.save_article(articles, file_name)
        print(f"Saved articles to {file_name}")

if __name__ == "__main__":
    main()