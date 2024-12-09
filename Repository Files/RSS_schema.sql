
CREATE TABLE feeds (
    feed_id SERIAL PRIMARY KEY,
    feed_url TEXT UNIQUE NOT NULL,
    feed_name TEXT,
    source_type TEXT,
    relevance_score FLOAT,
    last_updated TIMESTAMP,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE articles (
    article_id SERIAL PRIMARY KEY,
    feed_id INTEGER REFERENCES feeds(feed_id),
    title TEXT NOT NULL,
    link TEXT UNIQUE NOT NULL,
    description TEXT,
    publication_date TIMESTAMP,
    content TEXT,
    tags TEXT[],
    sentiment_score FLOAT,
    engagement_score INTEGER,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE authors (
    author_id SERIAL PRIMARY KEY,
    author_name TEXT UNIQUE NOT NULL
);

CREATE TABLE author_articles (
    article_id INTEGER REFERENCES articles(article_id),
    author_id INTEGER REFERENCES authors(author_id),
    PRIMARY KEY (article_id, author_id)
);
