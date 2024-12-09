# Use the PostgreSQL base image with the desired version
FROM postgres:15.3

# Copy initialization scripts to the Docker image
COPY init-db.sh /docker-entrypoint-initdb.d/
COPY schema.sql /docker-entrypoint-initdb.d/

# Set environment variables for default database setup (optional)
ENV POSTGRES_USER=AI-Safety-Through-Debate
ENV POSTGRES_PASSWORD=mypassword
ENV POSTGRES_DB=AI-Safety-Through-Debate


