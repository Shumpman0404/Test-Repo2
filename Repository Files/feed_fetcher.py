import psycopg2
import feedparser
from datetime import datetime
import db_settings  # Import the credentials
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_connection_with_retry(retries=5, delay=5):
    """Retry database connection if it fails."""
    for attempt in range(retries):
        try:
            conn = psycopg2.connect(
                host=db_settings.DB_HOST,
                port=db_settings.DB_PORT,
                database=db_settings.DB_NAME,
                user=db_settings.DB_USER,
                password=db_settings.DB_PASSWORD,
            )
            logging.info("Database connection established successfully.")
            return conn
        except psycopg2.OperationalError as e:
            logging.warning(f"Attempt {attempt + 1}: Database connection failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                logging.error("Failed to connect to the database after multiple attempts.")
                raise

def fetch_and_store_articles():
    """Fetch articles from all active feeds and store them in the database."""
    conn = get_connection_with_retry()
    cur = conn.cursor()
    try:
        cur.execute("SELECT feed_id, feed_url FROM feeds WHERE active = TRUE")
        feeds = cur.fetchall()

        for feed in feeds:
            feed_id, feed_url = feed
            d = feedparser.parse(feed_url)
            for entry in d.entries:
                title = entry.title
                link = entry.link
                description = entry.get('description', '')
                content = entry.get('content', [{'value': ''}])[0]['value']
                pub_date = entry.get('published_parsed', None)
                publication_date = datetime(*pub_date[:6]) if pub_date else None

                # Insert article into the database
                try:
                    cur.execute("""
                        INSERT INTO articles (feed_id, title, link, description, publication_date, content)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (link) DO NOTHING
                    """, (feed_id, title, link, description, publication_date, content))
                    conn.commit()
                except Exception as e:
                    logging.error(f"Error inserting article '{title}': {e}")

    finally:
        cur.close()
        conn.close()
        logging.info("Database connection closed.")

if __name__ == '__main__':
    fetch_and_store_articles()
