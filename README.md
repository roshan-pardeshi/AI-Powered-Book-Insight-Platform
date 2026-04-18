# AI-Powered Book Insight Platform

A full-stack application for scraping, storing, and querying book data using AI-powered RAG (Retrieval-Augmented Generation).

## Features

- **Book Scraper**: Automated scraping using Selenium
- **AI Features**: Summary generation, genre classification, recommendations, sentiment analysis
- **RAG Pipeline**: Vector search with ChromaDB and OpenAI integration
- **REST API**: Django REST Framework APIs
- **Frontend**: React with Tailwind CSS

## Tech Stack

- Backend: Django + DRF
- Database: SQLite (for demo; switch to MySQL in production)
- Vector DB: ChromaDB
- AI: OpenAI API
- Frontend: React + Tailwind CSS
- Automation: Selenium

## Setup Instructions

### Backend Setup

1. Navigate to backend directory:
   ```
   cd backend
   ```

2. Create virtual environment:
   ```
   python -m venv venv
   ```

3. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Create .env file in backend directory:
   ```
   DB_NAME=book_platform
   DB_USER=root
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=3306
   OPENAI_API_KEY=your_openai_api_key
   CHROMA_DB_PATH=./chroma_db
   ```

6. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

7. Run the server:
   ```
   python manage.py runserver
   ```

### Frontend Setup

1. Navigate to frontend directory:
   ```
   cd frontend
   ```

2. Install Node.js (if not installed)

3. Install dependencies:
   ```
   npm install
   ```

4. Start the development server:
   ```
   npm start
   ```

## Usage

1. Start the backend server on port 8000
2. Start the frontend on port 3000
3. Use the dashboard to scrape books or ask questions

## API Endpoints

- GET /api/books/ - List all books
- GET /api/books/<id>/ - Book details
- POST /api/upload/ - Scrape books
- GET /api/recommend/ - Get recommendations
- POST /api/ask/ - Ask questions

## Notes

- For MySQL, install MySQL server and update settings.py
- Update scraper selectors for actual website
- Ensure OpenAI API key is set
- ChromaDB will create local vector database

## Production Deployment

- Use production WSGI server (gunicorn)
- Set DEBUG=False
- Configure proper database
- Use environment variables for secrets

## Docker Deployment

A fast local deployment is available using Docker.

1. Install Docker Desktop.
2. From the repository root, run:
   ```bash
   docker compose up --build
   ```
3. Open the app:
   - Frontend: `http://localhost:3000`
   - Backend: `http://localhost:8000`

> The backend requires `OPENAI_API_KEY` for AI features. Set it in your shell before running Docker compose.

Stop the app with `Ctrl+C`.
