import streamlit as st
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Configure connection details (replace with actual values)
DB_HOST = "AI-Safety_postgres_db"  # e.g., "192.168.1.10"
DB_NAME = "AI-Safety-Through-Debate"
DB_USER = "AI-Safety-Through-Debate"
DB_PASSWORD = "mypassword"
DB_PORT = "5432"


# Function to connect to the database and fetch data
@st.cache_data(ttl=600)
def load_data(query):
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    with engine.connect() as conn:
        return pd.read_sql(query, conn)

st.title("RSS Feed Data Viewer")

# Dropdown for selecting data to view
view_choice = st.selectbox("Choose data to view", ["Feeds", "Articles", "Categories", "Article Categories"])

if view_choice == "Feeds":
    st.subheader("Feeds Table")
    feeds_data = load_data("SELECT * FROM feeds")
    st.dataframe(feeds_data)

elif view_choice == "Articles":
    st.subheader("Articles Table")
    articles_data = load_data("SELECT * FROM articles")
    st.dataframe(articles_data)

elif view_choice == "Categories":
    st.subheader("Categories Table")
    categories_data = load_data("SELECT * FROM categories")
    st.dataframe(categories_data)

elif view_choice == "Article Categories":
    st.subheader("Article Categories Table")
    article_categories_data = load_data("SELECT * FROM article_categories")
    st.dataframe(article_categories_data)
