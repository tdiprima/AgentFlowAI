# Type-Safe News Agent

This project implements a type-safe agent for scraping news articles, validating their structure, and storing them in a database using Python, Pydantic, and SQLite.

## What does this project do?

- **Scrapes news articles** from one or more websites.
- **Extracts and validates** structured information (title, summary, URL, publication date, source) using Pydantic models for type safety.
- **Stores validated news summaries** in a SQLite database for further analysis or retrieval.

## How does it work?

### 1. Structured Output with Pydantic

The `NewsSummary` Pydantic model defines a strict schema for news summaries. This ensures that every article the agent processes conforms to a known, type-safe structure.

### 2. Scraping and Validation

The agent (`agent.py`) fetches HTML from news websites, parses articles using BeautifulSoup, and extracts relevant fields. For each article, it creates a `NewsSummary` instance. If the data doesn't match the schema (e.g., missing or invalid fields), the instance creation will fail, preventing bad data from entering the pipeline.

### 3. Storing Results

Validated news summaries are inserted into a SQLite database (`database.py`). Duplicate URLs are ignored to prevent storing the same article multiple times.

### 4. Running the Agent

The entry point (`main.py`) initializes the database and runs the agent against a list of news sites. You can add or change URLs in this list as needed.

## How to Use

1. **Install dependencies:**
    ```
    pip install pydantic beautifulsoup4 requests
    ```

2. **Add real news site URLs** to the `news_sites` list in `main.py`.

3. **Run the agent:**
    ```
    python main.py
    ```

4. **Check `news.db`** for stored news summaries.

## Folder Structure

```
type_safe_news_agent/
├── main.py
├── agent.py
├── models.py
├── database.py
├── news.db
└── README.md
```

---

**Note:**  
Scraping real news sites may require adjusting the HTML selectors in `agent.py` to match the site's structure, and you must respect each site's robots.txt and terms of service.

<br>
