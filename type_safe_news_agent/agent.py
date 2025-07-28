# News Scraping Agent
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from models import NewsSummary
from typing import List
from database import save_news_summary

def fetch_articles_from_url(url: str) -> List[NewsSummary]:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []

    for item in soup.select('article'):
        try:
            title_tag = item.find('h2')
            link_tag = item.find('a', href=True)
            summary_tag = item.find('p')
            date_tag = item.find('time')

            news = NewsSummary(
                title=title_tag.get_text(strip=True) if title_tag else "No Title",
                url=link_tag['href'] if link_tag else url,
                summary=summary_tag.get_text(strip=True) if summary_tag else "No Summary",
                published_at=datetime.fromisoformat(date_tag['datetime']) if date_tag and date_tag.has_attr('datetime') else datetime.now(),
                source=url
            )
            articles.append(news)
        except Exception as e:
            print(f"Skipping article due to error: {e}")
    return articles

def agent_run(news_sites: List[str]):
    for site in news_sites:
        print(f"Scraping {site}")
        summaries = fetch_articles_from_url(site)
        for summary in summaries:
            save_news_summary(summary)
