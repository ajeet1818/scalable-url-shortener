# URL Shortener

A simple and efficient URL shortener API built with FastAPI and SQLAlchemy.

## Features

- **Create shortened URLs** - Convert long URLs into short, shareable codes
- **Redirect** - Automatically redirect shortened URLs to original URLs
- **Click Tracking** - Track the number of times each shortened URL is accessed
- **Statistics** - View stats for any shortened URL
- **Delete URLs** - Remove shortened URLs when no longer needed

## Project Structure

```
url-shortener/
│
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application entry point
│   ├── database.py      # Database configuration and setup
│   ├── models.py        # SQLAlchemy database models
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── utils.py         # Utility functions
│   └── routes.py        # API route handlers
│
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Requirements

- Python 3.8+
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd url-shortener
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the development server:
```bash
python app/main.py
```

Or use uvicorn directly:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Create a Shortened URL
**POST** `/api/shorten`

Request body:
```json
{
  "original_url": "https://www.example.com/very/long/url"
}
```

Response:
```json
{
  "id": 1,
  "short_code": "abc123",
  "original_url": "https://www.example.com/very/long/url",
  "clicks": 0,
  "created_at": "2024-01-15T10:30:00"
}
```

### 2. Redirect to Original URL
**GET** `/api/{short_code}`

Redirects to the original URL and increments the click counter.

### 3. Get Statistics
**GET** `/api/stats/{short_code}`

Response:
```json
{
  "short_code": "abc123",
  "original_url": "https://www.example.com/very/long/url",
  "clicks": 5,
  "created_at": "2024-01-15T10:30:00"
}
```

### 4. Delete a Shortened URL
**DELETE** `/api/{short_code}`

### 5. Health Check
**GET** `/health`

Response:
```json
{
  "status": "ok"
}
```

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Database

The application uses SQLite for data storage by default. The database file (`shortener.db`) will be created automatically in the application directory.

## Future Enhancements

- User authentication and authorization
- Custom short codes
- URL expiration dates
- Bulk URL shortening
- Analytics dashboard
- Rate limiting
- QR code generation for shortened URLs

## License

MIT License
