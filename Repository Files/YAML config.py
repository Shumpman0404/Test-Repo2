version: '3.8'  # Specify the Docker Compose file format version

services:
  db:
    image: postgres:15.3   # Use the PostgreSQL image
    container_name: AI-Safety-Through-Debate
    environment:
      POSTGRES_USER: AI-Safety-Through-Debate
      POSTGRES_PASSWORD: mypassword
      POSTGRES_DB: AI-Safety-Through-Debate/AI-Safety-Postgres_DB/
    ports:
      - "5432:5432"         # Map host port 5432 to container port 5432
    volumes:
      - postgres_data:/var/lib/postgresql/data  # Persist data across restarts
    restart: always         # Restart the container if it crashes

  app:
    build:
      context: .            # Build from the current directory (Dockerfile required)
    container_name: streamlit_app
    ports:
      - "8501:8501"         # Map host port 8501 to container port 8501
    depends_on:
      - db                  # Ensure the database starts before the app
    environment:
      DATABASE_URL: postgres://ai_safety_user:mypassword@db:5432/ai_safety_db
    restart: always

volumes:
  postgres_data:             # Define a named volume for the database