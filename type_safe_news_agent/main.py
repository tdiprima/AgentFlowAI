# Main Runner
from agent import agent_run
from database import init_db

if __name__ == "__main__":
    init_db()
    news_sites = [
        "https://example-news-site.com",  # Replace with real news URLs
        # Add more URLs as needed
    ]
    agent_run(news_sites)
    print("Done scraping and storing news summaries.")
