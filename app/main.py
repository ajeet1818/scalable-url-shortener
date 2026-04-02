from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routes import router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener API",
    description="A simple URL shortener service",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to URL Shortener API",
        "docs": "/docs",
        "endpoints": {
            "create_short_url": "POST /api/shorten",
            "redirect": "GET /api/{short_code}",
            "stats": "GET /api/stats/{short_code}",
            "delete": "DELETE /api/{short_code}"
        }
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
