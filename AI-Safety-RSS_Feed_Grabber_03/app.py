import streamlit as st
import psycopg2
from psycopg2 import pool
import db_settings  # Import the credentials
from feed_fetcher import fetch_and_store_articles
import logging
import atexit

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize a connection pool
db_pool = pool.SimpleConnectionPool(
    1, 20,  # Min and max connections
    host=db_settings.DB_HOST,
    port=db_settings.DB_PORT,
    database=db_settings.DB_NAME,
    user=db_settings.DB_USER,
    password=db_settings.DB_PASSWORD,
)

def get_connection_from_pool():
    """Get a connection from the pool."""
    return db_pool.getconn()

def release_connection_to_pool(conn):
    """Release a connection back to the pool."""
    db_pool.putconn(conn)

# Register to close all connections on exit
atexit.register(lambda: db_pool.closeall())

st.title('RSS News Feed Analysis Tool')

# Section to add a new feed
st.header('Add a New Feed')
feed_url = st.text_input('Feed URL')
feed_name = st.text_input('Feed Name (optional)')

if st.button('Add Feed'):
    if feed_url:
        conn = get_connection_from_pool()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO feeds (feed_url, feed_name) 
                VALUES (%s, %s) 
                ON CONFLICT (feed_url) DO NOTHING
            """, (feed_url, feed_name))
            conn.commit()
            st.success('Feed added successfully.')
        except Exception as e:
            logging.error(f"Error adding feed: {e}")
            st.error(f'Error adding feed: {e}')
        finally:
            cur.close()
            release_connection_to_pool(conn)
    else:
        st.warning('Please enter a feed URL.')

# Section to display existing feeds
st.header('Existing Feeds')
conn = get_connection_from_pool()
cur = conn.cursor()
try:
    cur.execute("SELECT feed_id, feed_url, feed_name FROM feeds WHERE active = TRUE")
    feeds = cur.fetchall()
finally:
    cur.close()
    release_connection_to_pool(conn)

for feed in feeds:
    st.write(f"**ID**: {feed[0]}, **URL**: {feed[1]}, **Name**: {feed[2]}")

# Button to fetch articles
if st.button('Fetch Articles'):
    with st.spinner('Fetching articles...'):
        try:
            fetch_and_store_articles()
            st.success('Articles fetched successfully.')
        except Exception as e:
            logging.error(f"Error fetching articles: {e}")
            st.error(f'Error fetching articles: {e}')
