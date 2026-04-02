from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import get_db
from .models import URLShortener
from .schemas import URLCreate, URLResponse, URLStats
from .utils import generate_short_code

router = APIRouter(prefix="/api", tags=["urls"])


@router.post("/shorten", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
def shorten_url(url_data: URLCreate, db: Session = Depends(get_db)):
    """Create a shortened URL."""
    short_code = generate_short_code()
    
    # Check if short code already exists
    while db.query(URLShortener).filter(URLShortener.short_code == short_code).first():
        short_code = generate_short_code()
    
    db_url = URLShortener(
        short_code=short_code,
        original_url=str(url_data.original_url)
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


@router.get("/{short_code}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    """Redirect to original URL and increment click count."""
    db_url = db.query(URLShortener).filter(URLShortener.short_code == short_code).first()
    
    if not db_url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    
    db_url.clicks += 1
    db.commit()
    
    return {"location": db_url.original_url}


@router.get("/stats/{short_code}", response_model=URLStats)
def get_stats(short_code: str, db: Session = Depends(get_db)):
    """Get statistics for a shortened URL."""
    db_url = db.query(URLShortener).filter(URLShortener.short_code == short_code).first()
    
    if not db_url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    
    return db_url


@router.delete("/{short_code}", status_code=status.HTTP_204_NO_CONTENT)
def delete_url(short_code: str, db: Session = Depends(get_db)):
    """Delete a shortened URL."""
    db_url = db.query(URLShortener).filter(URLShortener.short_code == short_code).first()
    
    if not db_url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    
    db.delete(db_url)
    db.commit()
    return None
