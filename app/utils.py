import string
import random


def generate_short_code(length: int = 6) -> str:
    """Generate a random short code for URL shortening."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def is_valid_url(url: str) -> bool:
    """Validate if the string is a valid URL."""
    return url.startswith(('http://', 'https://'))
